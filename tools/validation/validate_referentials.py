#!/usr/bin/env python3
"""Validate consistency across the LOTUSim normative referentials."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


TASK_FILE = Path("references/task-catalog/LOTUSim_Task_Catalog_v0.8.1.md")
MISSION_FILE = Path("references/mission-catalog/LOTUSim_Mission_Catalog_v1.0.4.md")
STATE_FILE = Path("references/state-model/LOTUSim_State_Model_v0.1.yaml")
ONTOLOGY_FILE = Path("references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl")


@dataclass
class ValidationReport:
    errors: list[tuple[str, str, str]] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def error(self, code: str, location: str, message: str) -> None:
        self.errors.append((code, location, message))

    @property
    def ok(self) -> bool:
        return not self.errors


def extract_section(text: str, start: str, end: str | None = None) -> str:
    start_match = re.search(start, text, re.MULTILINE)
    if not start_match:
        raise ValueError(f"section start not found: {start}")
    section = text[start_match.end() :]
    if end:
        end_match = re.search(end, section, re.MULTILINE)
        if end_match:
            section = section[: end_match.start()]
    return section


def yaml_documents(text: str) -> list[Any]:
    documents: list[Any] = []
    for match in re.finditer(r"```yaml\s*\n(.*?)\n```", text, re.DOTALL):
        documents.append(yaml.safe_load(match.group(1)))
    return documents


def duplicates(values: Iterable[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def ontology_classes(text: str) -> tuple[set[str], dict[str, set[str]]]:
    classes: set[str] = set()
    parents: dict[str, set[str]] = defaultdict(set)
    blocks = re.finditer(
        r"^nmo:([A-Za-z][\w-]*)\s+a\s+owl:Class\s*;(.*?)(?=^nmo:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    for block in blocks:
        child, body = block.groups()
        classes.add(child)
        for parent in re.findall(r"rdfs:subClassOf\s+nmo:([A-Za-z][\w-]*)", body):
            classes.add(parent)
            parents[child].add(parent)
    return classes, parents


def is_ontology_subtype(child: str, parent: str, parents: dict[str, set[str]]) -> bool:
    if child == parent:
        return True
    seen: set[str] = set()
    pending = [child]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        direct = parents.get(current, set())
        if parent in direct:
            return True
        pending.extend(direct)
    return False


def type_compatible(
    actual: str,
    expected: str,
    model_types: dict[str, dict[str, Any]],
    ontology_parents: dict[str, set[str]],
) -> bool:
    if actual == expected:
        return True
    if expected.startswith("nmo:") and actual.startswith("nmo:"):
        return is_ontology_subtype(actual[4:], expected[4:], ontology_parents)
    if expected.startswith("SM-TY-"):
        definition = model_types.get(expected, {})
        options = definition.get("union_of", []) + definition.get("compatible_realizations", [])
        return any(type_compatible(actual, option, model_types, ontology_parents) for option in options)
    if actual.startswith("SM-TY-"):
        definition = model_types.get(actual, {})
        options = definition.get("union_of", []) + definition.get("compatible_realizations", [])
        return bool(options) and all(
            type_compatible(option, expected, model_types, ontology_parents) for option in options
        )
    return False


def task_state_occurrences(semantics: dict[str, Any]) -> list[tuple[str, dict[str, Any], str]]:
    occurrences: list[tuple[str, dict[str, Any], str]] = []

    def add(value: Any, use: str) -> None:
        if isinstance(value, dict):
            if value.get("state_ref"):
                occurrences.append((value["state_ref"], value, use))
                return
            for nested in value.values():
                add(nested, use)
        elif isinstance(value, list):
            for nested in value:
                add(nested, use)

    for parameter in semantics.get("parameters", []):
        source = parameter.get("source")
        if isinstance(source, dict) and source.get("kind") == "state_at_start":
            add([source], "consumer")
    add(semantics.get("reads"), "consumer")
    add(semantics.get("invariants"), "consumer")
    for items in (semantics.get("applicability") or {}).values():
        add(items, "consumer")
    add(semantics.get("desired_outcomes"), "consumer")
    add(semantics.get("completion_conditions"), "completion")
    add(semantics.get("termination_conditions"), "consumer")
    effects = semantics.get("operational_effects") or {}
    for category, group in effects.items():
        for operation in ("add", "remove"):
            add((group or {}).get(operation), f"effect:{category}")
    for outcome in semantics.get("failure_outcomes", []):
        add(outcome.get("establishes"), "failure")
    return occurrences


def validate_repository(root: Path) -> ValidationReport:
    report = ValidationReport()
    task_path, mission_path = root / TASK_FILE, root / MISSION_FILE
    state_path, ontology_path = root / STATE_FILE, root / ONTOLOGY_FILE
    required = [task_path, mission_path, state_path, ontology_path]
    missing = [path for path in required if not path.is_file()]
    for path in missing:
        report.error("FILE001", str(path.relative_to(root)), "required referential is missing")
    if missing:
        return report

    try:
        task_text = task_path.read_text(encoding="utf-8")
        mission_text = mission_path.read_text(encoding="utf-8")
        state_model = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        ontology_text = ontology_path.read_text(encoding="utf-8")
        task_section = extract_section(task_text, r"^## 6\. Typed signatures\s*$", r"^## 7\.")
        mission_section = extract_section(mission_text, r"^## 7\. Detailed mission specifications\s*$", r"^## Appendix A")
        task_records = [doc for doc in yaml_documents(task_section) if isinstance(doc, dict) and doc.get("id", "").startswith("TC-")]
        mission_records = [doc for doc in yaml_documents(mission_section) if isinstance(doc, dict) and doc.get("id", "").startswith("MC-") and "specification" in doc]
        family_docs = [doc for doc in yaml_documents(task_text) if isinstance(doc, dict) and "semantic_families" in doc]
    except (OSError, ValueError, yaml.YAMLError) as exc:
        report.error("PARSE001", "referentials", str(exc))
        return report

    families = (family_docs[0].get("semantic_families", []) if family_docs else [])
    states = state_model.get("states", [])
    model_type_list = state_model.get("state_model_types", [])
    candidates = state_model.get("deferred_candidates", [])
    ontology, ontology_parents = ontology_classes(ontology_text)
    task_ids = [item.get("id", "") for item in task_records]
    mission_ids = [item.get("id", "") for item in mission_records]
    signature_records = [signature for task in task_records for signature in task.get("signatures", [])]
    signature_ids = [item.get("signature_id", "") for item in signature_records]
    family_ids = [item.get("id", "") for item in families]
    state_ids = [item.get("id", "") for item in states]
    state_symbols = [item.get("symbol", "") for item in states]
    model_type_ids = [item.get("id", "") for item in model_type_list]
    candidate_ids = [item.get("id", "") for item in candidates]
    task_by_id = {item["id"]: item for item in task_records}
    signature_by_id = {item["signature_id"]: item for item in signature_records}
    state_by_id = {item["id"]: item for item in states}
    model_types = {item["id"]: item for item in model_type_list}

    report.counts = {
        "missions": len(mission_records), "tasks": len(task_records),
        "signatures": len(signature_records), "families": len(families),
        "states": len(states), "state_types": len(model_type_list),
        "deferred_candidates": len(candidates),
    }

    identifier_sets = [
        ("ID001", "task", task_ids, r"TC-\d{3}"),
        ("ID002", "mission", mission_ids, r"MC-\d{3}"),
        ("ID003", "signature", signature_ids, r"TC-\d{3}-S\d{2}"),
        ("ID004", "semantic family", family_ids, r"SF-\d{2}"),
        ("ID005", "state", state_ids, r"SM-ST-\d{3}"),
        ("ID006", "state-model type", model_type_ids, r"SM-TY-\d{3}"),
        ("ID007", "deferred candidate", candidate_ids, r"SM-CAND-\d{3}"),
    ]
    for code, label, values, pattern in identifier_sets:
        for value in values:
            if not re.fullmatch(pattern, value or ""):
                report.error(code, label, f"invalid identifier: {value!r}")
        for value in duplicates(values):
            report.error(code, label, f"duplicate identifier: {value}")
    for symbol in duplicates(state_symbols):
        report.error("ID008", "state model", f"duplicate state symbol: {symbol}")
    expected_tasks = [f"TC-{number:03d}" for number in range(1, 65)]
    expected_missions = [f"MC-{number:03d}" for number in range(1, 67)]
    if task_ids != expected_tasks:
        report.error("ID009", str(TASK_FILE), "canonical task inventory must be ordered and contiguous from TC-001 to TC-064")
    if mission_ids != expected_missions:
        report.error("ID010", str(MISSION_FILE), "canonical mission inventory must be ordered and contiguous from MC-001 to MC-066")

    family_use = Counter()
    for task in task_records:
        for index, signature in enumerate(task.get("signatures", []), 1):
            sid = signature.get("signature_id", "")
            expected_sid = f"{task['id']}-S{index:02d}"
            if sid != expected_sid:
                report.error("TASK001", task["id"], f"expected signature {expected_sid}, found {sid}")
            family = signature.get("semantic_family")
            if family not in family_ids:
                report.error("TASK002", sid, f"unknown or missing semantic family: {family}")
            else:
                family_use[family] += 1
            for capability in signature.get("implements_capabilities", []):
                if capability not in ontology:
                    report.error("ONTO001", sid, f"unknown ontology capability: nmo:{capability}")
                elif not is_ontology_subtype(capability, "PhysicalCapability", ontology_parents):
                    report.error("ONTO002", sid, f"nmo:{capability} is not a PhysicalCapability")
    for family in family_ids:
        if not family_use[family]:
            report.error("TASK003", family, "semantic family has no signature")

    forward: dict[str, set[str]] = defaultdict(set)
    for mission in mission_records:
        for task_id in (mission.get("traceability") or {}).get("task_candidates", []):
            if task_id not in task_by_id:
                report.error("TRACE001", mission["id"], f"unknown task candidate: {task_id}")
            else:
                forward[task_id].add(mission["id"])
    for task in task_records:
        actual = set((task.get("traceability") or {}).get("used_by_missions", []))
        unknown = actual - set(mission_ids)
        if unknown:
            report.error("TRACE002", task["id"], f"unknown reverse mission references: {sorted(unknown)}")
        if actual != forward[task["id"]]:
            report.error("TRACE003", task["id"], f"reverse mission trace differs; expected {sorted(forward[task['id']])}, found {sorted(actual)}")

    def valid_type(type_name: str, location: str) -> None:
        if type_name.startswith("nmo:"):
            if type_name[4:] not in ontology:
                report.error("TYPE001", location, f"unknown ontology type: {type_name}")
        elif type_name not in model_types:
            report.error("TYPE002", location, f"unknown State Model type: {type_name}")

    for model_type in model_type_list:
        for type_name in model_type.get("union_of", []) + model_type.get("compatible_realizations", []):
            valid_type(type_name, model_type["id"])

    for state in states:
        location = state["id"]
        if state.get("category") not in {"world", "knowledge", "execution", "resource"}:
            report.error("STATE001", location, f"invalid category: {state.get('category')}")
        arguments = state.get("arguments", [])
        roles = [argument.get("role", "") for argument in arguments]
        if not roles or any(not role for role in roles) or duplicates(roles):
            report.error("STATE002", location, "argument roles must be non-empty and unique")
        for argument in arguments:
            valid_type(argument.get("type", ""), location)
        if state.get("category") == "knowledge" and "holder" not in roles:
            report.error("STATE003", location, "knowledge state must have a holder argument")
        if not state.get("producers") or not state.get("consumers"):
            report.error("STATE004", location, "state must have at least one producer and one consumer")
        if not set(state.get("key", [])).issubset(roles):
            report.error("STATE005", location, "state key contains an undeclared argument")
        for side in ("producers", "consumers"):
            for reference in state.get(side, []):
                ref = str(reference.get("ref", ""))
                if re.fullmatch(r"TC-\d{3}-S\d{2}", ref) and ref not in signature_by_id:
                    report.error("STATE006", location, f"unknown task signature in {side}: {ref}")
        for constraint in state.get("constraints", []):
            match = re.search(r"mutually_exclusive_with_(SM-ST-\d{3})", str(constraint))
            if match and match.group(1) not in state_by_id:
                report.error("STATE007", location, f"unknown state in constraint: {match.group(1)}")
        for mission_id in (state.get("evidence") or {}).get("missions", []):
            if mission_id not in mission_ids:
                report.error("STATE008", location, f"unknown mission evidence: {mission_id}")
    for candidate in candidates:
        for mission_id in candidate.get("mission_evidence", []):
            if mission_id not in mission_ids:
                report.error("STATE009", candidate["id"], f"unknown mission evidence: {mission_id}")

    allowed_kinds = {"primitive", "abstract", "external_event"}
    allowed_patterns = {"instantaneous", "durative", "continuous"}
    state_producers = {
        state["id"]: {item.get("ref") for item in state.get("producers", []) if item.get("kind") == "task"}
        for state in states
    }
    state_consumers = {
        state["id"]: {item.get("ref") for item in state.get("consumers", []) if item.get("kind") == "task"}
        for state in states
    }
    enriched = 0
    for signature in signature_records:
        sid = signature["signature_id"]
        semantics = signature.get("semantics")
        if not semantics:
            continue
        enriched += 1
        kind, pattern = semantics.get("semantic_kind"), semantics.get("execution_pattern")
        if kind not in allowed_kinds:
            report.error("SEM001", sid, f"invalid semantic_kind: {kind}")
        if pattern not in allowed_patterns:
            report.error("SEM002", sid, f"invalid execution_pattern: {pattern}")
        parameters = semantics.get("parameters", [])
        parameter_by_role = {parameter.get("role"): parameter for parameter in parameters}
        if len(parameter_by_role) != len(parameters) or None in parameter_by_role:
            report.error("SEM003", sid, "parameter roles must be present and unique")
        for parameter in parameters:
            valid_type(parameter.get("type", ""), sid)
            source = parameter.get("source")
            source_kind = source if isinstance(source, str) else (source or {}).get("kind")
            if source_kind not in {"task_input", "state_at_start", "execution_output"}:
                report.error("SEM004", sid, f"invalid parameter source for {parameter.get('role')}: {source_kind}")
            if source_kind == "state_at_start" and (
                not isinstance(source, dict) or not (source.get("state_ref") and source.get("bindings"))
            ):
                report.error("SEM005", sid, f"state_at_start source for {parameter.get('role')} needs state_ref and bindings")
            if source_kind == "execution_output" and (
                not isinstance(source, dict) or not source.get("produced_by")
            ):
                report.error("SEM006", sid, f"execution_output source for {parameter.get('role')} needs produced_by")
        if pattern == "continuous":
            if not semantics.get("termination_conditions") or semantics.get("completion_conditions"):
                report.error("SEM007", sid, "continuous task needs termination conditions and no completion conditions")
        elif pattern in {"instantaneous", "durative"} and not semantics.get("completion_conditions"):
            report.error("SEM008", sid, "instantaneous or durative task needs completion conditions")
        if not semantics.get("failure_outcomes"):
            report.error("SEM009", sid, "enriched task needs at least one failure outcome")
        effects = semantics.get("operational_effects") or {}
        if kind == "abstract" and any(
            (group or {}).get(operation)
            for group in effects.values() for operation in ("add", "remove")
        ):
            report.error("SEM010", sid, "abstract task must not declare direct operational effects")

        for state_ref, occurrence, use in task_state_occurrences(semantics):
            if state_ref in candidate_ids:
                report.error("SEM011", sid, f"deferred candidate used as normative state: {state_ref}")
                continue
            state = state_by_id.get(state_ref)
            if not state:
                report.error("SEM012", sid, f"unknown state reference: {state_ref}")
                continue
            expected_roles = {argument["role"] for argument in state.get("arguments", [])}
            bindings = occurrence.get("bindings") or {}
            if set(bindings) != expected_roles:
                report.error("SEM013", sid, f"bindings for {state_ref} must be {sorted(expected_roles)}, found {sorted(bindings)}")
            argument_types = {argument["role"]: argument["type"] for argument in state.get("arguments", [])}
            for role, value in bindings.items():
                if role not in argument_types:
                    continue
                if value in parameter_by_role:
                    actual_type = parameter_by_role[value].get("type", "")
                    if not type_compatible(actual_type, argument_types[role], model_types, ontology_parents):
                        report.error("SEM014", sid, f"parameter {value}:{actual_type} is incompatible with {state_ref}.{role}:{argument_types[role]}")
                elif isinstance(value, str) and value.endswith("Capability"):
                    if value not in ontology or not type_compatible("nmo:" + value, argument_types[role], model_types, ontology_parents):
                        report.error("SEM015", sid, f"invalid capability constant for {state_ref}.{role}: {value}")
                else:
                    report.error("SEM016", sid, f"binding value is not a declared parameter or capability constant: {value}")
            if use.startswith("effect:"):
                effect_category = use.split(":", 1)[1]
                expected_category = "resource" if effect_category == "resources" else effect_category
                if state.get("category") != expected_category:
                    report.error("SEM017", sid, f"{effect_category} effect references {state_ref}, a {state.get('category')} state")
                if sid not in state_producers[state_ref]:
                    report.error("SEM018", sid, f"{state_ref} does not declare this signature as a producer")
                if effect_category == "knowledge" and "holder" not in bindings:
                    report.error("SEM019", sid, f"knowledge effect on {state_ref} must bind holder")
            elif use == "failure":
                if sid not in state_producers[state_ref]:
                    report.error("SEM020", sid, f"failure state {state_ref} does not declare this signature as a producer")
            elif use == "completion":
                if sid not in state_consumers[state_ref] and sid not in state_producers[state_ref]:
                    report.error("SEM021", sid, f"completion state {state_ref} does not declare this signature as producer or consumer")
            elif sid not in state_consumers[state_ref]:
                report.error("SEM021", sid, f"consumed state {state_ref} does not declare this signature as a consumer")
    report.counts["enriched_signatures"] = enriched

    link_files = [root / "README.md", root / "specification/INDEX.md", root / "specification/state-model/LOTUSim_State_Model_Specification_v0.1.md"]
    for document in link_files:
        if not document.is_file():
            report.error("DOC001", str(document.relative_to(root)), "expected documentation index is missing")
            continue
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\((?!https?://|#|mailto:)([^)]+)\)", text):
            clean_target = target.split("#", 1)[0].strip().strip("<>")
            if clean_target and not (document.parent / clean_target).resolve().exists():
                report.error("DOC002", str(document.relative_to(root)), f"broken local link: {target}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    report = validate_repository(args.root.resolve())
    for code, location, message in report.errors:
        if os.getenv("GITHUB_ACTIONS") == "true":
            print(f"::error title={code}::{location}: {message}")
        else:
            print(f"ERROR [{code}] {location}: {message}")
    summary = ", ".join(f"{name}={value}" for name, value in report.counts.items())
    if report.ok:
        print(f"Referential validation passed ({summary}).")
        return 0
    print(f"Referential validation failed with {len(report.errors)} error(s) ({summary}).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
