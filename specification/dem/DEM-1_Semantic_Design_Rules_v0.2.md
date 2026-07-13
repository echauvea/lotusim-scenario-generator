# LSG Domain Engineering Method (DEM)

# DEM-1 — Semantic Design Rules

**Version:** v0.2 (Draft)

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

Abstract tasks express intent and expected outcomes but do not directly modify the symbolic state.

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
- completion conditions;
- failure outcomes.

---

## SDR-10 — Families share common semantics

Tasks belonging to the same Semantic Family shall reuse the same concepts, state transitions and terminology.

---

## SDR-11 — Common semantics shall be centralized

Common operational semantics shared by multiple tasks shall be defined once at the Semantic Family level within the Task Catalog.

Individual tasks shall only specify the semantic specialization required by their own signatures.

This rule minimizes duplication, guarantees consistency and simplifies derivation of the State Model.

---

# 4. Semantic Families

The following families are currently identified:

- ISR
- Movement
- Protection
- Engagement
- Support
- Command & Control
- Logistics

Semantic Families are first-class elements of the Task Catalog. Each family centralizes its common semantics; task signatures define only their specializations.

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

# 8. Changes from v0.1

- Integrated SDR-11 from the separate merge update.
- Made Semantic Families explicitly first-class Task Catalog elements.
- Clarified that abstract tasks do not directly modify symbolic state.
- Clarified the three-source derivation of the State Model and the separation between world state and force-relative knowledge.
- Standardized the product name as **LSG — LOTUSim Scenario Generator**.
