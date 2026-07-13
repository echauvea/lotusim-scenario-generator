# LOTUSim Domain Engineering Method (DEM)

# Part 1.5 — Semantic Design Rules

**Version:** v0.1 (Draft)

---

# 1. Purpose

This document defines the modeling rules governing task semantics and the State Model used by LOTUSim.

Its purpose is to ensure that all contributors model missions, tasks and symbolic states consistently before any HDDL artifacts are produced.

---

# 2. Guiding Principles

1. The Naval Ontology is the single source of truth for concepts and types.
2. The Task Catalog is the single source of truth for operational tasks.
3. The Mission Catalog is the single source of truth for mission objectives.
4. The State Model is derived from these repositories.
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

Physical reality and each force's knowledge shall always be modeled separately.

Knowledge may differ from reality.

---

## SDR-05 — Distinguish capabilities from availability

Capabilities are structural properties.

Availability is a dynamic state.

Example:

- hasCapability(platform, RadarCapability)
- capabilityAvailable(platform, RadarCapability)

---

## SDR-06 — Distinguish abstract and primitive tasks

Abstract tasks express intent.

Primitive tasks modify the symbolic state.

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

Every task shall declare:

- applicability conditions;
- operational effects;
- completion conditions;
- failure outcomes.

---

## SDR-10 — Families share common semantics

Tasks belonging to the same semantic family shall reuse the same concepts, state transitions and terminology.

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

Each family will receive its own specification.

---

# 5. Traceability

Every modeling element shall be traceable:

Ontology
→ Task Catalog
→ Mission Catalog
→ State Model
→ HDDL Domain

No element shall appear directly in HDDL without traceability to upstream repositories.

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
