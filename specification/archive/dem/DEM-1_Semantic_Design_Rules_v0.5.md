# LSG Domain Engineering Method (DEM)

# DEM-1 — Semantic Design Rules

**Version:** v0.5 (Draft)

---

# 1. Purpose

This document defines the modeling rules governing task semantics and the State Model used by **LSG — LOTUSim Scenario Generator**.

Its purpose is to ensure that all contributors model missions, tasks and symbolic states consistently before any HDDL artifacts are produced.

---

# 2. Guiding Principles

1. The Naval Maritime Ontology is the single source of truth for concepts and types.
2. The Mission Catalog is the single source of truth for missions and mission objectives.
3. The Task Catalog is the single source of truth for operational tasks and their signature-level semantics.
4. The State Model is derived from these three repositories.
5. HDDL is an implementation artifact derived from the State Model.

---

# 3. Modeling Rules

## SDR-01 — Model concepts, not implementation

Operational meaning shall never depend on the planning engine, simulator or autonomy plugin.

---

## SDR-02 — One concept, one definition

A domain concept shall have exactly one definition and one identifier.

Synonyms shall be eliminated during normalization.

---

## SDR-03 — Distinguish objects, states and events

- Objects exist permanently (Ontology).
- States describe the current situation (State Model).
- Events represent instantaneous occurrences.
- Tasks produce transitions between states.

---

## SDR-04 — Distinguish world state from knowledge

Physical reality and each force’s knowledge shall always be modeled separately.

Knowledge may differ from reality.

---

## SDR-05 — Distinguish capabilities from availability

Capabilities are structural properties.

Availability is a dynamic state.

Example:

- `hasCapability(platform, RadarCapability)`
- `capabilityAvailable(platform, RadarCapability)`

---

## SDR-06 — Distinguish abstract and primitive tasks

Abstract tasks express intent through `desired_outcomes`, completion conditions and failure outcomes, but do not directly modify the symbolic state.

Primitive tasks may modify the symbolic state.

---

## SDR-07 — Semantics belong to task signatures

Each typed signature owns its own semantic definition.

---

## SDR-08 — Every state has producers and consumers

Each dynamic state shall:

- be produced by at least one task;
- be consumed by at least one task.

---

## SDR-09 — Every task reads and/or writes state

Every task signature shall declare:

- applicability conditions;
- state reads and/or operational effects;
- failure outcomes.

Instantaneous and durative signatures shall additionally declare completion conditions. Continuous signatures shall instead declare normal termination conditions.

---

## SDR-10 — Families share common semantics

Signatures belonging to the same Semantic Family shall reuse the same concepts, state transitions and terminology.

Family membership is defined at typed-signature level. A task with several signatures may therefore participate in several families without duplicating or splitting its canonical verb identity.

---

## SDR-11 — Common semantics shall be centralized

Common operational semantics shared by multiple signatures shall be defined once at the Semantic Family level within the Task Catalog.

Individual signatures shall only specify the semantic specialization required for their typed operational use.

This rule minimizes duplication, guarantees consistency and simplifies derivation of the State Model.

---

## SDR-12 — Bindings shall be explicit and typed

Every variable used in a state reference shall resolve to a typed parameter declared by the same signature.

A parameter may be supplied as a task input, captured explicitly from the state at task start, or produced by execution as an output value. A captured or produced value remains bound for the execution of that task instance.

An `execution_output` shall identify a typed value actually produced or estimated by the executor, such as an observation, location estimate, classification, identity assessment or track. It shall not be used to hide a required task input or an initial-state binding.

State removal shall identify the exact state tuple to remove. Pseudo-states such as `previous_location`, `old_value` or `located_at_previous_location` shall not be introduced to represent an unknown prior value.

---

## SDR-13 — Execution patterns and termination shall be explicit

Every signature shall declare whether it is `instantaneous`, `durative` or `continuous`.

A continuous task has no implicit natural completion. It shall declare its normal termination conditions separately from failure outcomes. A request from a parent task, mission termination or an operational transition may terminate a continuous task without constituting failure.

---

## SDR-14 — Knowledge effects shall be holder-relative and evidence-preserving

Every knowledge-state effect shall bind the force, organization, platform or other information holder for which the assertion is valid. A knowledge effect shall never be interpreted as a direct change to the observed physical entity.

An unsuccessful observation or detection attempt establishes an inconclusive attempt or execution failure. It shall not establish the physical absence of a target unless a separate assessment task produces that conclusion from sufficient evidence.

ISR stages form a knowledge graph, not a mandatory linear pipeline. Detection is the common basis for target-relative localization, classification and tracking; these branches may progress independently. Identification may consume a classification or direct identity evidence.

---

# 4. Semantic Families

The canonical families are:

- `SF-01` — ISR;
- `SF-02` — Movement;
- `SF-03` — Protection;
- `SF-04` — Engagement;
- `SF-05` — Support;
- `SF-06` — Command & Control;
- `SF-07` — Logistics.

Semantic Families are first-class elements of the Task Catalog. Each family centralizes its common semantics; signatures define only their specializations.

Every typed signature belongs to exactly one Semantic Family. A task-level family list, when displayed, is derived as the set union of the families of its signatures and is never maintained as an independent source field.

This cardinality preserves both principles:

- one stable canonical verb may expose materially different typed uses;
- each operational use still inherits one unambiguous body of common semantics.

---

# 5. Traceability

Every modeling element shall be traceable through the following derivation chain:

```text
Naval Maritime Ontology ─┐
Mission Catalog ─────────┼─> State Model ─> HDDL Domain / Problems
Task Catalog ────────────┘
```

No element shall appear directly in HDDL without traceability to the State Model and its upstream repositories.

---

# 6. Quality Gates

Before a release, the following checks shall succeed:

- No orphan mission.
- No orphan task.
- No orphan state.
- No unused capability.
- No undefined semantic.
- No undefined state transition.
- No unresolved or untyped binding variable.
- Every knowledge effect identifies its information holder.
- Every execution output is typed and declares how it is produced.
- Every state removal identifies an exact bound tuple.
- Every continuous signature declares at least one termination condition.
- No abstract signature declares direct operational effects.
- No HDDL predicate outside the State Model.
- Complete traceability chain.

---

# 7. Expected Benefits

Applying these rules ensures:

- consistency across contributors;
- planner independence;
- systematic derivation of the State Model;
- systematic derivation of HDDL;
- easier maintenance and evolution.

---

# 8. Changes from v0.4 to v0.5

- Added `execution_output` as the binding source for values produced or estimated during execution.
- Required holder-relative knowledge effects and prohibited interpreting an inconclusive sensing attempt as physical absence.
- Defined the ISR progression as a branching knowledge graph rather than a mandatory linear pipeline.

---

# 9. Changes from v0.3 to v0.4

- Moved Semantic Family membership from task level to typed-signature level.
- Required every signature to reference exactly one canonical family identifier.
- Defined any task-level family list as a derived union rather than an independently maintained field.
- Stabilized the seven canonical family identifiers `SF-01` through `SF-07`.

---

# 10. Changes from v0.2 to v0.3

- Made typed, explicit bindings mandatory for every state reference.
- Defined state-at-start capture for prior values needed by exact state removal.
- Prohibited pseudo-states used as placeholders for an unknown previous value.
- Made `execution_pattern` mandatory and separated normal termination of continuous tasks from completion and failure.
- Clarified that abstract-task intent is represented by `desired_outcomes`, not direct operational effects.

---

# 11. Earlier changes from v0.1

- Integrated SDR-11 from the separate merge update.
- Made Semantic Families explicitly first-class Task Catalog elements.
- Clarified that abstract tasks do not directly modify symbolic state.
- Clarified the three-source derivation of the State Model and the separation between world state and force-relative knowledge.
- Standardized the product name as **LSG — LOTUSim Scenario Generator**.
