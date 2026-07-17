# LOTUSim State Model Specification

> **Status:** working draft
> **Version:** 0.2
> **Date:** 2026-07-17
> **Archived data source:** [`LOTUSim_State_Model_v0.2.yaml`](../../../references/state-model/archive/LOTUSim_State_Model_v0.2.yaml)

## 1. Purpose

The LOTUSim State Model defines the controlled dynamic-state vocabulary shared by missions, task semantics and derived planning artifacts. It is planner-independent: HDDL predicates and simulator bindings are derived from it and do not redefine its operational meaning.

Version 0.2 extends the initial pilot and ISR baseline to the complete Movement family. It covers 19 enriched signatures: the four semantic-pilot signatures, the seven core ISR signatures and the eight Movement signatures completed in this increment.

## 2. Sources and scope

The model is derived from three normative inputs:

1. relevant physical types and capabilities in the Naval Maritime Ontology;
2. task reads, effects, completion conditions and failure outcomes in the Task Catalog;
3. mission preconditions, desired end states and success/failure criteria in the Mission Catalog.

The v0.2 normative inventory contains:

- 54 states;
- 11 State Model-owned types;
- 4 categories: world, knowledge, execution and resource;
- 5 mission-derived candidates deferred until their producing tasks or aggregation rules are modeled.

No resource state is required by the current 19 signatures. The category remains part of the metamodel and will be populated by later sustainment and logistics increments.

## 3. Identifier and reference policy

State identifiers use `SM-ST-NNN`. State Model-owned type identifiers use `SM-TY-NNN`. Identifiers are opaque and stable: renaming a symbol or changing a category does not change the identifier.

Each state also has a readable `symbol`. Task signatures reference the stable identifier through `state_ref`; the symbol is resolved from the State Model and is not duplicated in the task record.

```yaml
- state_ref: SM-ST-020
  bindings: {holder: knowledge_holder, target: target}
```

Deferred candidates use `SM-CAND-NNN`. They are traceable design inputs but are not valid task `state_ref` targets until promoted to the normative `states` collection.

## 4. State metamodel

Each normative state defines:

```yaml
id: SM-ST-020
symbol: detected
category: knowledge
definition: ...
arguments:
  - role: holder
    type: SM-TY-001
  - role: target
    type: nmo:PhysicalEntity
persistence: fluent
update_policy: assert_retract_by_evidence_policy
key: [holder, target]
initialization: optional_external_information
producers: []
consumers: []
constraints: []
evidence:
  missions: []
```

The ordered `arguments` list defines the canonical tuple signature. Every task binding shall use exactly those role names, without missing or additional roles.

## 5. Categories

| Category | Meaning | Examples in v0.2 |
|---|---|---|
| `world` | Physical or operational reality independent of who knows it. | `located_at`, `following`, `route_traversable` |
| `knowledge` | Information valid for an explicit holder. | `detected`, `localized`, `classified`, `identified`, `track_maintained` |
| `execution` | Assignment, capability availability, task progress or execution outcome. | `capability_available`, `route_completed`, `navigation_failed` |
| `resource` | Consumable or renewable quantity relevant to planning. | None in v0.2 |

All knowledge states bind `holder`. An inconclusive sensing attempt is an execution outcome and never proves that a target is physically absent.

## 6. Types and ontology boundary

Physical types reuse the ontology with the `nmo:` prefix. Dynamic information artifacts belong to the State Model because the ontology intentionally excludes observations, operational knowledge and planning state.

State Model-owned types in v0.2 include information holders, observations, evidence, estimates, assessments, tracks and formation references. `SM-TY-010 navigation_objective` is an explicit union admitting `nmo:SpatialRegion`, `nmo:Route` and `nmo:PhysicalEntity`; it gives `navigation_failed` one stable tuple shape for destination-, route- and target-relative movement.

`information_holder` and `emission` remain ontology-mapping decisions. Their State Model identifiers allow work to continue without silently adding classes to the physical ontology. In v0.2, a platform or physical operational entity may realize `information_holder`; this compatibility is explicit in the YAML and does not classify every physical entity as a knowledge holder in the ontology.

## 7. Canonical state inventory

| ID | Symbol | Category | Main producer |
|---|---|---|---|
| SM-ST-001 | `located_at` | world | Navigate or simulator synchronization |
| SM-ST-002 | `route_destination` | world | Scenario initialization |
| SM-ST-003 | `destination_reachable` | world | Reachability evaluator |
| SM-ST-004 | `route_traversable` | world | Route-constraint evaluator |
| SM-ST-005 | `following` | world | Follow |
| SM-ST-006 | `assigned_to_escort` | execution | Scenario or command assignment |
| SM-ST-007 | `protected_unit_at_destination` | world | Escort-goal evaluator |
| SM-ST-008 | `protected_unit_preserved` | world | Protection-outcome evaluator |
| SM-ST-009 | `area_designated` | execution | Mission or scenario initialization |
| SM-ST-010 | `capability_available` | execution | Execution-state synchronization |
| SM-ST-011 | `capability_unavailable` | execution | Execution-state synchronization or task failure |
| SM-ST-012 | `route_completed` | execution | Navigate Route |
| SM-ST-013 | `navigation_failed` | execution | Navigate failure |
| SM-ST-014 | `escort_degraded` | execution | Escort failure outcome |
| SM-ST-015 | `escort_failed` | execution | Escort failure outcome |
| SM-ST-016 | `observation_available` | knowledge | Observe |
| SM-ST-017 | `observation_covers` | knowledge | Observe |
| SM-ST-018 | `observation_produced_by` | knowledge | Observe |
| SM-ST-019 | `observation_attempt_inconclusive` | execution | Observe failure |
| SM-ST-020 | `detected` | knowledge | Detect Object |
| SM-ST-021 | `detection_evidence_available` | knowledge | Detect Object |
| SM-ST-022 | `detection_attempt_inconclusive` | execution | Detect Object failure |
| SM-ST-023 | `emission_detected` | knowledge | Detect Emission |
| SM-ST-024 | `emission_detection_evidence_available` | knowledge | Detect Emission |
| SM-ST-025 | `emission_detection_attempt_inconclusive` | execution | Detect Emission failure |
| SM-ST-026 | `localized` | knowledge | Localize |
| SM-ST-027 | `location_known` | knowledge | Localize or knowledge projection |
| SM-ST-028 | `location_unknown` | knowledge | Follow failure or knowledge projection |
| SM-ST-029 | `localization_attempt_inconclusive` | execution | Localize failure |
| SM-ST-030 | `classified` | knowledge | Classify |
| SM-ST-031 | `classification_available` | knowledge | Classify or knowledge projection |
| SM-ST-032 | `classification_attempt_inconclusive` | execution | Classify failure |
| SM-ST-033 | `direct_identity_evidence_available` | knowledge | External information source |
| SM-ST-034 | `identified` | knowledge | Identify |
| SM-ST-035 | `identification_attempt_inconclusive` | execution | Identify failure |
| SM-ST-036 | `track_established` | knowledge | Track |
| SM-ST-037 | `track_maintained` | knowledge | Track |
| SM-ST-038 | `track_lost` | knowledge | Track failure |

The YAML source is authoritative for definitions, argument order, lifecycle, producers, consumers, constraints and evidence.

## 8. Normalization decisions

Four inconsistencies in the candidate vocabulary are resolved:

- `target_location_known` and `protected_unit_location_known` become `SM-ST-027 location_known`;
- `target_location_unknown` becomes `SM-ST-028 location_unknown`;
- `protection_capability_available` becomes the generic `SM-ST-010 capability_available`, bound to `ProtectionCapability`;
- the two differently shaped uses of `navigation_failed` become one tuple `(entity, objective)`, where `objective` is `SM-TY-010 navigation_objective`.

`localized(holder, target, estimate)` retains the actual estimate. `location_known(holder, target)` is a derived projection used by tasks that need only to know whether a usable estimate exists.

## 9. Producer and consumer rules

Every state declares at least one producer and one consumer. A producer may be:

- a primitive task effect or failure outcome;
- scenario or command initialization;
- simulator or execution-state synchronization;
- a named derived evaluator;
- imported external information.

Abstract-task desired outcomes and completion conditions are consumers, not producers. In particular, Escort does not directly produce `protected_unit_at_destination` or `protected_unit_preserved`.

Entries labeled `future_task` record an identified downstream consumer that is outside the current enrichment increment. They prevent premature duplication while making the next semantic work explicit.

## 10. Persistence and update policies

- `static` states remain fixed unless an explicit scenario or command update is allowed.
- `fluent` states may be asserted, updated or retracted during execution.
- `derived_fluent` states are recomputed from other authoritative state.
- `terminal_for_task_instance` and `terminal_for_attempt` record a completion or failure outcome for the relevant execution instance.

The `key` identifies the tuple components used for replacement or mutual-exclusion checks. For example, a new `located_at` value replaces the previous planning location for the same entity.

## 11. Deferred mission-derived candidates

Five mission-level concepts remain deliberately unpromoted in v0.2:

- area coverage achieved;
- surveillance continuity achieved;
- information requirement satisfied;
- contact or assessment reported;
- confidence requirement satisfied.

They require temporal aggregation, confidence modeling or semantics for Search, Survey, Assess, Report and Share. Keeping them in `deferred_candidates` preserves mission traceability without creating states that have no valid producer.

## 12. Validation requirements

A conforming increment shall verify that:

- state and type identifiers are unique;
- symbols are unique within their collection;
- every task `state_ref` resolves to a normative state;
- task bindings exactly match the state argument roles;
- ontology-prefixed types and capability constants resolve in the ontology;
- State Model-owned type references resolve to `SM-TY-NNN` entries;
- every knowledge state binds a `holder` argument;
- every state declares a producer and a consumer;
- no task directly writes a derived world state; it changes authoritative state and the named evaluator recomputes the derived relation;
- mutually exclusive states have compatible keys;
- no deferred candidate is used as a task state reference.

## 13. Movement extension in v0.2

Movement adds states for patrol, station keeping, formation maintenance, shadowing, approach, withdrawal, corridor transit and evasion. Three distinctions are normative:

- an active movement relation such as `patrolling`, `shadowing` or `evading` is not itself a completion condition;
- target-relative movement reads holder-relative knowledge (`location_known` or a maintained track) without converting that knowledge into a world fact;
- geometric results such as `approach_envelope_satisfied`, `inside_area` and `threat_separation_satisfied` are derived from authoritative position and geometry data.

`SM-TY-011 formation_reference` remains outside the physical ontology because it represents a command-defined relative geometry, not a physical entity. `navigation_objective` is extended to admit a physical entity for target-relative maneuvers while preserving the stable identifier `SM-TY-010`.

## 14. Planned extension

Version 0.2 is the baseline for enriching the remaining 60 signatures. New states shall be added only when a task or mission requirement cannot reuse an existing definition. Each family increment shall update producers, consumers and deferred candidates before its task semantics are considered complete.
