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


TASK_FILE = Path("references/task-catalog/LOTUSim_Task_Catalog_v0.10.0.md")
MISSION_FILE = Path("references/mission-catalog/LOTUSim_Mission_Catalog_v1.0.4.md")
STATE_FILE = Path("references/state-model/LOTUSim_State_Model_v0.3.yaml")
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


@dataclass
class RepoData:
    root: Path
    task_records: list[dict[str, Any]]
    mission_records: list[dict[str, Any]]
    families: list[dict[str, Any]]
    state_model: dict[str, Any]
    ontology: set[str]
    ontology_parents: dict[str, set[str]]

    @property
    def states(self) -> list[dict[str, Any]]:
        return self.state_model.get("states", [])

    @property
    def model_types(self) -> list[dict[str, Any]]:
        return self.state_model.get("state_model_types", [])

    @property
    def candidates(self) -> list[dict[str, Any]]:
        return self.state_model.get("deferred_candidates", [])

    @property
    def signatures(self) -> list[dict[str, Any]]:
        return [signature for task in self.task_records for signature in task.get("signatures", [])]


def extract_section(text: str, start: str, end: str | None = None) -> str:
    start_match = re.search(start, text, re.MULTILINE)
    if not start_match:
        raise ValueError(f"section start not found: {start}")
    section = text[start_match.end() :]
    end_match = re.search(end, section, re.MULTILINE) if end else None
    return section[: end_match.start()] if end_match else section


def yaml_documents(text: str) -> list[Any]:
    documents: list[Any] = []
    buffer: list[str] = []
    in_yaml = False
    for line in text.splitlines():
        marker = line.strip()
        if not in_yaml and marker == "```yaml":
            in_yaml = True
            buffer = []
        elif in_yaml and marker == "```":
            documents.append(yaml.safe_load("\n".join(buffer)))
            in_yaml = False
        elif in_yaml:
            buffer.append(line)
    return documents


def duplicates(values: Iterable[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def ontology_classes(text: str) -> tuple[set[str], dict[str, set[str]]]:
    classes: set[str] = set()
    parents: dict[str, set[str]] = defaultdict(set)
    starts = list(re.finditer(r"^nmo:", text, re.MULTILINE))
    for index, start in enumerate(starts):
        stop = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[start.start() : stop]
        header = re.match(r"nmo:([A-Za-z][\w-]*)\s+a\s+owl:Class\s*;", block)
        if not header:
            continue
        child = header.group(1)
        classes.add(child)
        for parent in re.findall(r"rdfs:subClassOf\s+nmo:([A-Za-z][\w-]*)", block):
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


def nested_state_occurrences(value: Any, use: str) -> list[tuple[str, dict[str, Any], str]]:
    if isinstance(value, list):
        return [item for nested in value for item in nested_state_occurrences(nested, use)]
    if not isinstance(value, dict):
        return []
    if value.get("state_ref"):
        return [(value["state_ref"], value, use)]
    return [item for nested in value.values() for item in nested_state_occurrences(nested, use)]


def task_state_occurrences(semantics: dict[str, Any]) -> list[tuple[str, dict[str, Any], str]]:
    occurrences: list[tuple[str, dict[str, Any], str]] = []
    for parameter in semantics.get("parameters", []):
        source = parameter.get("source")
        if isinstance(source, dict) and source.get("kind") == "state_at_start":
            occurrences.extend(nested_state_occurrences(source, "consumer"))
    for field_name in ("reads", "invariants", "desired_outcomes"):
        occurrences.extend(nested_state_occurrences(semantics.get(field_name), "consumer"))
    occurrences.extend(nested_state_occurrences(semantics.get("applicability"), "consumer"))
    occurrences.extend(nested_state_occurrences(semantics.get("completion_conditions"), "completion"))
    occurrences.extend(nested_state_occurrences(semantics.get("termination_conditions"), "consumer"))
    for category, group in (semantics.get("operational_effects") or {}).items():
        for operation in ("add", "remove"):
            occurrences.extend(nested_state_occurrences((group or {}).get(operation), f"effect:{category}"))
    for outcome in semantics.get("failure_outcomes", []):
        occurrences.extend(nested_state_occurrences(outcome.get("establishes"), "failure"))
    return occurrences


def load_data(root: Path, report: ValidationReport) -> RepoData | None:
    paths = [root / path for path in (TASK_FILE, MISSION_FILE, STATE_FILE, ONTOLOGY_FILE)]
    for path in paths:
        if not path.is_file():
            report.error("FILE001", str(path.relative_to(root)), "required referential is missing")
    if report.errors:
        return None
    try:
        task_text = paths[0].read_text(encoding="utf-8")
        mission_text = paths[1].read_text(encoding="utf-8")
        state_model = yaml.safe_load(paths[2].read_text(encoding="utf-8"))
        ontology_text = paths[3].read_text(encoding="utf-8")
        task_section = extract_section(task_text, r"^## 6\. Typed signatures\s*$", r"^## 7\.")
        mission_section = extract_section(mission_text, r"^## 7\. Detailed mission specifications\s*$", r"^## Appendix A")
        task_records = [doc for doc in yaml_documents(task_section) if is_catalog_record(doc, "TC-", None)]
        mission_records = [doc for doc in yaml_documents(mission_section) if is_catalog_record(doc, "MC-", "specification")]
        family_docs = [doc for doc in yaml_documents(task_text) if isinstance(doc, dict) and "semantic_families" in doc]
        ontology, ontology_parents = ontology_classes(ontology_text)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        report.error("PARSE001", "referentials", str(exc))
        return None
    families = family_docs[0].get("semantic_families", []) if family_docs else []
    return RepoData(root, task_records, mission_records, families, state_model, ontology, ontology_parents)


def is_catalog_record(document: Any, prefix: str, required_field: str | None) -> bool:
    if not isinstance(document, dict) or not str(document.get("id", "")).startswith(prefix):
        return False
    return required_field is None or required_field in document


def validate_identifiers(data: RepoData, report: ValidationReport) -> None:
    groups = [
        ("ID001", "task", [item.get("id", "") for item in data.task_records], r"TC-\d{3}"),
        ("ID002", "mission", [item.get("id", "") for item in data.mission_records], r"MC-\d{3}"),
        ("ID003", "signature", [item.get("signature_id", "") for item in data.signatures], r"TC-\d{3}-S\d{2}"),
        ("ID004", "semantic family", [item.get("id", "") for item in data.families], r"SF-\d{2}"),
        ("ID005", "state", [item.get("id", "") for item in data.states], r"SM-ST-\d{3}"),
        ("ID006", "state-model type", [item.get("id", "") for item in data.model_types], r"SM-TY-\d{3}"),
        ("ID007", "deferred candidate", [item.get("id", "") for item in data.candidates], r"SM-CAND-\d{3}"),
    ]
    for code, label, values, pattern in groups:
        for value in values:
            if not re.fullmatch(pattern, value or ""):
                report.error(code, label, f"invalid identifier: {value!r}")
        for value in duplicates(values):
            report.error(code, label, f"duplicate identifier: {value}")
    for symbol in duplicates(item.get("symbol", "") for item in data.states):
        report.error("ID008", "state model", f"duplicate state symbol: {symbol}")
    validate_inventory_order(data, report)


def validate_inventory_order(data: RepoData, report: ValidationReport) -> None:
    task_ids = [item.get("id", "") for item in data.task_records]
    mission_ids = [item.get("id", "") for item in data.mission_records]
    if task_ids != [f"TC-{number:03d}" for number in range(1, 65)]:
        report.error("ID009", str(TASK_FILE), "canonical task inventory must be ordered and contiguous from TC-001 to TC-064")
    if mission_ids != [f"MC-{number:03d}" for number in range(1, 67)]:
        report.error("ID010", str(MISSION_FILE), "canonical mission inventory must be ordered and contiguous from MC-001 to MC-066")


def validate_tasks(data: RepoData, report: ValidationReport) -> None:
    family_ids = {item.get("id", "") for item in data.families}
    family_use: Counter[str] = Counter()
    for task in data.task_records:
        for index, signature in enumerate(task.get("signatures", []), 1):
            validate_signature_identity(task, signature, index, family_ids, family_use, data, report)
    for family in family_ids:
        if not family_use[family]:
            report.error("TASK003", family, "semantic family has no signature")


def validate_signature_identity(
    task: dict[str, Any], signature: dict[str, Any], index: int, family_ids: set[str],
    family_use: Counter[str], data: RepoData, report: ValidationReport,
) -> None:
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
        if capability not in data.ontology:
            report.error("ONTO001", sid, f"unknown ontology capability: nmo:{capability}")
        elif not is_ontology_subtype(capability, "PhysicalCapability", data.ontology_parents):
            report.error("ONTO002", sid, f"nmo:{capability} is not a PhysicalCapability")


def validate_traceability(data: RepoData, report: ValidationReport) -> None:
    task_by_id = {item["id"]: item for item in data.task_records}
    mission_ids = {item["id"] for item in data.mission_records}
    forward: dict[str, set[str]] = defaultdict(set)
    for mission in data.mission_records:
        for task_id in (mission.get("traceability") or {}).get("task_candidates", []):
            if task_id not in task_by_id:
                report.error("TRACE001", mission["id"], f"unknown task candidate: {task_id}")
            else:
                forward[task_id].add(mission["id"])
    for task in data.task_records:
        validate_task_reverse_trace(task, forward, mission_ids, report)


def validate_task_reverse_trace(
    task: dict[str, Any], forward: dict[str, set[str]], mission_ids: set[str], report: ValidationReport,
) -> None:
    actual = set((task.get("traceability") or {}).get("used_by_missions", []))
    unknown = actual - mission_ids
    if unknown:
        report.error("TRACE002", task["id"], f"unknown reverse mission references: {sorted(unknown)}")
    expected = forward[task["id"]]
    if actual != expected:
        report.error("TRACE003", task["id"], f"reverse mission trace differs; expected {sorted(expected)}, found {sorted(actual)}")


def validate_type_name(type_name: str, location: str, data: RepoData, report: ValidationReport) -> None:
    if type_name.startswith("nmo:"):
        if type_name[4:] not in data.ontology:
            report.error("TYPE001", location, f"unknown ontology type: {type_name}")
    elif type_name not in {item["id"] for item in data.model_types}:
        report.error("TYPE002", location, f"unknown State Model type: {type_name}")


def validate_model_types(data: RepoData, report: ValidationReport) -> None:
    for model_type in data.model_types:
        options = model_type.get("union_of", []) + model_type.get("compatible_realizations", [])
        for type_name in options:
            validate_type_name(type_name, model_type["id"], data, report)


def validate_states(data: RepoData, report: ValidationReport) -> None:
    signature_ids = {item["signature_id"] for item in data.signatures}
    state_ids = {item["id"] for item in data.states}
    mission_ids = {item["id"] for item in data.mission_records}
    for state in data.states:
        validate_state_definition(state, signature_ids, state_ids, mission_ids, data, report)
    for candidate in data.candidates:
        validate_mission_evidence(candidate["id"], candidate.get("mission_evidence", []), mission_ids, report, "STATE009")
    validate_normalization_decisions(data, report)


def validate_normalization_decisions(data: RepoData, report: ValidationReport) -> None:
    state_ids = {item["id"] for item in data.states}
    type_ids = {item["id"] for item in data.model_types}
    for decision in data.state_model.get("normalization_decisions", []):
        state_ref = decision.get("canonical_state")
        type_ref = decision.get("canonical_type")
        if state_ref and state_ref not in state_ids:
            report.error("STATE011", "normalization_decisions", f"unknown canonical state: {state_ref}")
        if type_ref and type_ref not in type_ids:
            report.error("STATE012", "normalization_decisions", f"unknown canonical type: {type_ref}")


def validate_state_definition(
    state: dict[str, Any], signature_ids: set[str], state_ids: set[str], mission_ids: set[str],
    data: RepoData, report: ValidationReport,
) -> None:
    location = state["id"]
    if state.get("category") not in {"world", "knowledge", "execution", "resource"}:
        report.error("STATE001", location, f"invalid category: {state.get('category')}")
    arguments = state.get("arguments", [])
    roles = [argument.get("role", "") for argument in arguments]
    if not roles or any(not role for role in roles) or duplicates(roles):
        report.error("STATE002", location, "argument roles must be non-empty and unique")
    for argument in arguments:
        validate_type_name(argument.get("type", ""), location, data, report)
    if state.get("category") == "knowledge" and "holder" not in roles:
        report.error("STATE003", location, "knowledge state must have a holder argument")
    if not state.get("producers") or not state.get("consumers"):
        report.error("STATE004", location, "state must have at least one producer and one consumer")
    if not set(state.get("key", [])).issubset(roles):
        report.error("STATE005", location, "state key contains an undeclared argument")
    validate_state_references(state, signature_ids, state_ids, report)
    validate_mission_evidence(location, (state.get("evidence") or {}).get("missions", []), mission_ids, report, "STATE008")


def validate_state_references(
    state: dict[str, Any], signature_ids: set[str], state_ids: set[str], report: ValidationReport,
) -> None:
    for side in ("producers", "consumers"):
        for reference in state.get(side, []):
            ref = str(reference.get("ref", ""))
            if re.fullmatch(r"TC-\d{3}-S\d{2}", ref) and ref not in signature_ids:
                report.error("STATE006", state["id"], f"unknown task signature in {side}: {ref}")
    for constraint in state.get("constraints", []):
        match = re.search(r"mutually_exclusive_with_(SM-ST-\d{3})", str(constraint))
        if match and match.group(1) not in state_ids:
            report.error("STATE007", state["id"], f"unknown state in constraint: {match.group(1)}")


def validate_mission_evidence(
    location: str, references: Iterable[str], mission_ids: set[str], report: ValidationReport, code: str,
) -> None:
    for mission_id in references:
        if mission_id not in mission_ids:
            report.error(code, location, f"unknown mission evidence: {mission_id}")


def task_state_links(data: RepoData, side: str) -> dict[str, set[str]]:
    return {
        state["id"]: {item.get("ref") for item in state.get(side, []) if item.get("kind") == "task"}
        for state in data.states
    }


def validate_semantics(data: RepoData, report: ValidationReport) -> int:
    producers = task_state_links(data, "producers")
    consumers = task_state_links(data, "consumers")
    enriched = 0
    for signature in data.signatures:
        semantics = signature.get("semantics")
        if semantics:
            enriched += 1
            validate_signature_semantics(signature, semantics, producers, consumers, data, report)
    return enriched


def validate_reverse_task_state_links(data: RepoData, report: ValidationReport) -> None:
    usages: dict[tuple[str, str], set[str]] = defaultdict(set)
    for signature in data.signatures:
        semantics = signature.get("semantics")
        if not semantics:
            continue
        sid = signature["signature_id"]
        for state_ref, _occurrence, use in task_state_occurrences(semantics):
            usages[(sid, state_ref)].add(use)
    for state in data.states:
        validate_reverse_state_side(state, "producers", usages, report)
        validate_reverse_state_side(state, "consumers", usages, report)


def validate_reverse_state_side(
    state: dict[str, Any], side: str, usages: dict[tuple[str, str], set[str]], report: ValidationReport,
) -> None:
    for reference in state.get(side, []):
        if reference.get("kind") != "task":
            continue
        sid = reference.get("ref", "")
        actual = usages.get((sid, state["id"]), set())
        expected = {"failure", "completion"} if side == "producers" else {"consumer", "completion"}
        matches = bool(actual & expected) or (side == "producers" and any(use.startswith("effect:") for use in actual))
        if not matches:
            report.error(
                "STATE010", state["id"],
                f"{side[:-1]} task reference {sid} has no matching semantic use",
            )


def validate_signature_semantics(
    signature: dict[str, Any], semantics: dict[str, Any], producers: dict[str, set[str]],
    consumers: dict[str, set[str]], data: RepoData, report: ValidationReport,
) -> None:
    sid = signature["signature_id"]
    kind = semantics.get("semantic_kind")
    pattern = semantics.get("execution_pattern")
    if kind not in {"primitive", "abstract", "external_event"}:
        report.error("SEM001", sid, f"invalid semantic_kind: {kind}")
    if pattern not in {"instantaneous", "durative", "continuous"}:
        report.error("SEM002", sid, f"invalid execution_pattern: {pattern}")
    parameter_by_role = validate_parameters(sid, semantics.get("parameters", []), data, report)
    validate_lifecycle(sid, kind, pattern, semantics, report)
    state_by_id = {item["id"]: item for item in data.states}
    candidate_ids = {item["id"] for item in data.candidates}
    model_types = {item["id"]: item for item in data.model_types}
    for state_ref, occurrence, use in task_state_occurrences(semantics):
        validate_occurrence(
            sid, state_ref, occurrence, use, parameter_by_role, state_by_id,
            candidate_ids, model_types, producers, consumers, data, report,
        )


def validate_parameters(
    sid: str, parameters: list[dict[str, Any]], data: RepoData, report: ValidationReport,
) -> dict[str, dict[str, Any]]:
    parameter_by_role = {parameter.get("role"): parameter for parameter in parameters}
    if len(parameter_by_role) != len(parameters) or None in parameter_by_role:
        report.error("SEM003", sid, "parameter roles must be present and unique")
    for parameter in parameters:
        validate_type_name(parameter.get("type", ""), sid, data, report)
        validate_parameter_source(sid, parameter, report)
    return parameter_by_role


def validate_parameter_source(sid: str, parameter: dict[str, Any], report: ValidationReport) -> None:
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


def validate_lifecycle(
    sid: str, kind: str, pattern: str, semantics: dict[str, Any], report: ValidationReport,
) -> None:
    if pattern == "continuous" and (
        not semantics.get("termination_conditions") or semantics.get("completion_conditions")
    ):
        report.error("SEM007", sid, "continuous task needs termination conditions and no completion conditions")
    if pattern in {"instantaneous", "durative"} and not semantics.get("completion_conditions"):
        report.error("SEM008", sid, "instantaneous or durative task needs completion conditions")
    if not semantics.get("failure_outcomes"):
        report.error("SEM009", sid, "enriched task needs at least one failure outcome")
    effects = semantics.get("operational_effects") or {}
    direct_effect = any((group or {}).get(op) for group in effects.values() for op in ("add", "remove"))
    if kind == "abstract" and direct_effect:
        report.error("SEM010", sid, "abstract task must not declare direct operational effects")


def validate_occurrence(
    sid: str, state_ref: str, occurrence: dict[str, Any], use: str,
    parameters: dict[str, dict[str, Any]], states: dict[str, dict[str, Any]], candidate_ids: set[str],
    model_types: dict[str, dict[str, Any]], producers: dict[str, set[str]], consumers: dict[str, set[str]],
    data: RepoData, report: ValidationReport,
) -> None:
    if state_ref in candidate_ids:
        report.error("SEM011", sid, f"deferred candidate used as normative state: {state_ref}")
        return
    state = states.get(state_ref)
    if not state:
        report.error("SEM012", sid, f"unknown state reference: {state_ref}")
        return
    bindings = occurrence.get("bindings") or {}
    argument_types = {argument["role"]: argument["type"] for argument in state.get("arguments", [])}
    if set(bindings) != set(argument_types):
        report.error("SEM013", sid, f"bindings for {state_ref} must be {sorted(argument_types)}, found {sorted(bindings)}")
    for role, value in bindings.items():
        validate_binding(sid, state_ref, role, value, parameters, argument_types, model_types, data, report)
    validate_occurrence_direction(sid, state_ref, use, bindings, state, producers, consumers, report)


def validate_binding(
    sid: str, state_ref: str, role: str, value: Any, parameters: dict[str, dict[str, Any]],
    argument_types: dict[str, str], model_types: dict[str, dict[str, Any]], data: RepoData,
    report: ValidationReport,
) -> None:
    if role not in argument_types:
        return
    if value in parameters:
        actual_type = parameters[value].get("type", "")
        if not type_compatible(actual_type, argument_types[role], model_types, data.ontology_parents):
            report.error("SEM014", sid, f"parameter {value}:{actual_type} is incompatible with {state_ref}.{role}:{argument_types[role]}")
        return
    if isinstance(value, str) and value.endswith("Capability"):
        compatible = value in data.ontology and type_compatible(
            "nmo:" + value, argument_types[role], model_types, data.ontology_parents
        )
        if not compatible:
            report.error("SEM015", sid, f"invalid capability constant for {state_ref}.{role}: {value}")
        return
    report.error("SEM016", sid, f"binding value is not a declared parameter or capability constant: {value}")


def validate_occurrence_direction(
    sid: str, state_ref: str, use: str, bindings: dict[str, Any], state: dict[str, Any],
    producers: dict[str, set[str]], consumers: dict[str, set[str]], report: ValidationReport,
) -> None:
    if use.startswith("effect:"):
        validate_effect(sid, state_ref, use, bindings, state, producers, report)
    elif use == "failure" and sid not in producers[state_ref]:
        report.error("SEM020", sid, f"failure state {state_ref} does not declare this signature as a producer")
    elif use == "completion" and sid not in consumers[state_ref] and sid not in producers[state_ref]:
        report.error("SEM021", sid, f"completion state {state_ref} does not declare this signature as producer or consumer")
    elif use == "consumer" and sid not in consumers[state_ref]:
        report.error("SEM021", sid, f"consumed state {state_ref} does not declare this signature as a consumer")


def validate_effect(
    sid: str, state_ref: str, use: str, bindings: dict[str, Any], state: dict[str, Any],
    producers: dict[str, set[str]], report: ValidationReport,
) -> None:
    effect_category = use.split(":", 1)[1]
    expected_category = "resource" if effect_category == "resources" else effect_category
    if effect_category == "world" and state.get("persistence") == "derived_fluent":
        report.error("SEM022", sid, f"direct effect references derived state {state_ref}")
    if state.get("category") != expected_category:
        report.error("SEM017", sid, f"{effect_category} effect references {state_ref}, a {state.get('category')} state")
    if sid not in producers[state_ref]:
        report.error("SEM018", sid, f"{state_ref} does not declare this signature as a producer")
    if effect_category == "knowledge" and "holder" not in bindings:
        report.error("SEM019", sid, f"knowledge effect on {state_ref} must bind holder")


def validate_links(data: RepoData, report: ValidationReport) -> None:
    relative_paths = [
        Path("README.md"), Path("specification/INDEX.md"),
        Path("specification/state-model/LOTUSim_State_Model_Specification_v0.3.md"),
    ]
    for relative_path in relative_paths:
        validate_document_links(data.root, relative_path, report)


def validate_document_links(root: Path, relative_path: Path, report: ValidationReport) -> None:
    document = root / relative_path
    if not document.is_file():
        report.error("DOC001", str(relative_path), "expected documentation index is missing")
        return
    text = document.read_text(encoding="utf-8")
    targets = re.findall(r"\[[^\]]+\]\((?!https?://|#|mailto:)([^)]+)\)", text)
    for target in targets:
        clean_target = target.split("#", 1)[0].strip().strip("<>")
        if clean_target and not (document.parent / clean_target).resolve().exists():
            report.error("DOC002", str(relative_path), f"broken local link: {target}")


def populate_counts(data: RepoData, report: ValidationReport, enriched: int) -> None:
    report.counts = {
        "missions": len(data.mission_records), "tasks": len(data.task_records),
        "signatures": len(data.signatures), "families": len(data.families),
        "states": len(data.states), "state_types": len(data.model_types),
        "deferred_candidates": len(data.candidates), "enriched_signatures": enriched,
    }


def validate_repository(root: Path) -> ValidationReport:
    report = ValidationReport()
    data = load_data(root, report)
    if data is None:
        return report
    validate_identifiers(data, report)
    validate_tasks(data, report)
    validate_traceability(data, report)
    validate_model_types(data, report)
    validate_states(data, report)
    enriched = validate_semantics(data, report)
    validate_reverse_task_state_links(data, report)
    validate_links(data, report)
    populate_counts(data, report, enriched)
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
