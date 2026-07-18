from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from typing import Any

import yaml

VALIDATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VALIDATION_DIR))

from validate_referentials import ValidationReport, load_data  # noqa: E402


def parse_sexpression(text: str) -> list[Any]:
    clean = "\n".join(line.split(";", 1)[0] for line in text.splitlines())
    tokens = re.findall(r"\(|\)|[^\s()]+", clean)
    index = 0

    def parse_list() -> list[Any]:
        nonlocal index
        if index >= len(tokens) or tokens[index] != "(":
            raise ValueError(f"expected '(' at token {index}")
        index += 1
        result: list[Any] = []
        while index < len(tokens) and tokens[index] != ")":
            if tokens[index] == "(":
                result.append(parse_list())
            else:
                result.append(tokens[index])
                index += 1
        if index >= len(tokens):
            raise ValueError("unclosed parenthesis")
        index += 1
        return result

    expression = parse_list()
    if index != len(tokens):
        raise ValueError(f"unexpected tokens after root expression at token {index}")
    return expression


def named_sections(expression: list[Any], keyword: str) -> dict[str, list[Any]]:
    return {
        item[1]: item
        for item in expression
        if isinstance(item, list) and len(item) > 1 and item[0] == keyword
    }


def section_value(section: list[Any], keyword: str) -> Any:
    index = section.index(keyword)
    return section[index + 1]


def contains_atom(expression: Any, name: str) -> bool:
    if not isinstance(expression, list):
        return False
    if expression and expression[0] == name:
        return True
    return any(contains_atom(item, name) for item in expression)


def contains_negated_atom(expression: Any, name: str) -> bool:
    if not isinstance(expression, list):
        return False
    if len(expression) == 2 and expression[0] == "not":
        atom = expression[1]
        return isinstance(atom, list) and bool(atom) and atom[0] == name
    return any(contains_negated_atom(item, name) for item in expression)


def typed_variables(parameters: list[Any]) -> list[str]:
    return [token for token in parameters if isinstance(token, str) and token.startswith("?")]


def ground(expression: Any, bindings: dict[str, str]) -> Any:
    if isinstance(expression, list):
        return [ground(item, bindings) for item in expression]
    return bindings.get(expression, expression)


def positive_atoms(expression: Any) -> list[tuple[str, ...]]:
    if not isinstance(expression, list) or not expression:
        return []
    if expression[0] == "and":
        return [atom for item in expression[1:] for atom in positive_atoms(item)]
    if expression[0] == "not":
        return []
    return [tuple(expression)]


def negative_atoms(expression: Any) -> list[tuple[str, ...]]:
    if not isinstance(expression, list) or not expression:
        return []
    if expression[0] == "and":
        return [atom for item in expression[1:] for atom in negative_atoms(item)]
    if expression[0] == "not" and isinstance(expression[1], list):
        return [tuple(expression[1])]
    return []


class HDDLPilotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[3]
        cls.fragment = cls.root / "references/hddl/experimental/mc-026-close-guard"
        cls.domain = parse_sexpression((cls.fragment / "domain.hddl").read_text(encoding="utf-8"))
        cls.problem = parse_sexpression((cls.fragment / "problem.hddl").read_text(encoding="utf-8"))
        cls.traceability = yaml.safe_load((cls.fragment / "traceability.yaml").read_text(encoding="utf-8"))
        report = ValidationReport()
        cls.data = load_data(cls.root, report)
        if cls.data is None or report.errors:
            raise AssertionError(report.errors)
        cls.states = {item["id"]: item for item in cls.data.states}
        cls.signatures = {item["signature_id"]: item for item in cls.data.signatures}
        cls.methods = {item["id"]: item for item in cls.data.method_records}

    def test_domain_and_problem_are_balanced_single_expressions(self) -> None:
        self.assertEqual(self.domain[0], "define")
        self.assertEqual(self.problem[0], "define")
        problem_domain = next(item for item in self.problem if isinstance(item, list) and item[0] == ":domain")
        domain_name = next(item for item in self.domain if isinstance(item, list) and item[0] == "domain")
        self.assertEqual(problem_domain[1], domain_name[1])

    def test_every_predicate_maps_to_the_exact_state_model_symbol(self) -> None:
        predicate_section = next(item for item in self.domain if isinstance(item, list) and item[0] == ":predicates")
        declared = {item[0] for item in predicate_section[1:]}
        mappings = {item["hddl"]: item["state_ref"] for item in self.traceability["predicates"]}
        self.assertEqual(declared, set(mappings))
        for hddl_name, state_ref in mappings.items():
            state = self.states[state_ref]
            self.assertEqual(hddl_name, state["symbol"].replace("_", "-"))

    def test_task_method_and_mission_references_exist(self) -> None:
        for item in self.traceability["compound_tasks"]:
            self.assertIn(item["task_ref"], self.signatures)
        for item in self.traceability["methods"]:
            self.assertIn(item["method_ref"], self.methods)
        self.assertIn(self.traceability["mission"], {item["id"] for item in self.data.mission_records})

    def test_lifted_projection_variables_match_state_at_start_bindings(self) -> None:
        for item in self.traceability["projection_variables"]:
            signature = self.signatures[item["task_ref"]]["semantics"]
            parameter = next(parameter for parameter in signature["parameters"] if parameter["role"] == item["hddl"])
            self.assertEqual(parameter["source"]["kind"], "state_at_start")
            self.assertEqual(parameter["source"]["state_ref"], item["state_ref"])
            self.assertIn(item["state_ref"], self.states)

    def test_lifecycle_actions_use_continuous_task_active_fluents(self) -> None:
        actions = named_sections(self.domain, ":action")
        for mapping in self.traceability["actions"]:
            action = actions[mapping["hddl"]]
            task_ref = mapping.get("task_ref")
            if task_ref:
                self.assertIn(task_ref, self.signatures)
            phase = mapping.get("lifecycle_phase")
            if not phase:
                continue
            signature = self.signatures[task_ref]["semantics"]
            self.assertEqual(signature["execution_pattern"], "continuous")
            state_ref = mapping["active_state_ref"]
            state = self.states[state_ref]
            self.assertEqual(state["persistence"], "fluent")
            self.assertIn(state["update_policy"], {"assert_retract", "assert_while_task_active"})
            produced = {
                item["state_ref"]
                for item in signature["operational_effects"]["world"]["add"]
            }
            self.assertIn(state_ref, produced)
            effect = section_value(action, ":effect")
            predicate = state["symbol"].replace("_", "-")
            if phase == "start":
                self.assertTrue(contains_atom(effect, predicate))
                self.assertFalse(contains_negated_atom(effect, predicate))
            else:
                self.assertTrue(contains_negated_atom(effect, predicate))

    def test_evaluator_action_uses_a_declared_external_producer(self) -> None:
        mapping = next(item for item in self.traceability["actions"] if "external_producer" in item)
        state = self.states[mapping["produces_state_ref"]]
        producers = {item["ref"] for item in state["producers"] if item["kind"] == "external"}
        self.assertIn(mapping["external_producer"], producers)

    def test_compiled_method_preserves_both_spans_boundaries(self) -> None:
        method = named_sections(self.domain, ":method")["close-guard-route-escort"]
        ordered = section_value(method, ":ordered-subtasks")
        sequence = [item[0] for item in ordered[1:]]
        self.assertEqual(
            sequence,
            [
                "start-follow-designated-unit",
                "start-guard-object",
                "navigate-route",
                "evaluate-escort-destination",
                "stop-guard-object",
                "stop-follow-designated-unit",
            ],
        )
        transit = sequence.index("navigate-route")
        for start, stop in (
            ("start-follow-designated-unit", "stop-follow-designated-unit"),
            ("start-guard-object", "stop-guard-object"),
        ):
            self.assertLess(sequence.index(start), transit)
            self.assertGreater(sequence.index(stop), transit)

    def test_method_subtask_arities_match_declared_actions(self) -> None:
        actions = named_sections(self.domain, ":action")
        method = named_sections(self.domain, ":method")["close-guard-route-escort"]
        ordered = section_value(method, ":ordered-subtasks")
        for subtask in ordered[1:]:
            parameters = section_value(actions[subtask[0]], ":parameters")
            declared_variables = [token for token in parameters if isinstance(token, str) and token.startswith("?")]
            self.assertEqual(len(subtask) - 1, len(declared_variables), subtask[0])

    def test_mc026_method_is_applicable_and_expected_plan_reaches_goal(self) -> None:
        actions = named_sections(self.domain, ":action")
        method = named_sections(self.domain, ":method")["close-guard-route-escort"]
        initial_section = next(item for item in self.problem if isinstance(item, list) and item[0] == ":init")
        state = {tuple(atom) for atom in initial_section[1:]}

        method_bindings = {
            "?escort": "escort-1",
            "?protected": "protected-hvu-1",
            "?route": "escort-route-1",
            "?destination": "transit-destination",
            "?origin": "transit-origin",
        }
        grounded_method_precondition = ground(section_value(method, ":precondition"), method_bindings)
        self.assertTrue(set(positive_atoms(grounded_method_precondition)).issubset(state))

        plan = [
            ("start-follow-designated-unit", "escort-1", "protected-hvu-1"),
            ("start-guard-object", "escort-1", "protected-hvu-1"),
            ("navigate-route", "protected-hvu-1", "escort-route-1", "transit-destination", "transit-origin"),
            ("evaluate-escort-destination", "protected-hvu-1", "escort-route-1", "transit-destination"),
            ("stop-guard-object", "escort-1", "protected-hvu-1"),
            ("stop-follow-designated-unit", "escort-1", "protected-hvu-1"),
        ]
        for step in plan:
            action = actions[step[0]]
            variables = typed_variables(section_value(action, ":parameters"))
            bindings = dict(zip(variables, step[1:], strict=True))
            precondition = ground(section_value(action, ":precondition"), bindings)
            missing = set(positive_atoms(precondition)) - state
            self.assertFalse(missing, f"{step[0]} missing preconditions: {missing}")
            if step[0] == "navigate-route":
                self.assertIn(("following", "escort-1", "protected-hvu-1"), state)
                self.assertIn(("guarding", "escort-1", "protected-hvu-1"), state)
            effect = ground(section_value(action, ":effect"), bindings)
            state.difference_update(negative_atoms(effect))
            state.update(positive_atoms(effect))

        goal_section = next(item for item in self.problem if isinstance(item, list) and item[0] == ":goal")
        self.assertTrue(set(positive_atoms(goal_section[1])).issubset(state))
        self.assertNotIn(("following", "escort-1", "protected-hvu-1"), state)
        self.assertNotIn(("guarding", "escort-1", "protected-hvu-1"), state)


if __name__ == "__main__":
    unittest.main()
