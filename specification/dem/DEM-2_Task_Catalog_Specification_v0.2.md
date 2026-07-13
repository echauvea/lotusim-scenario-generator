# LSG Domain Engineering Method (DEM)

# DEM-2 — Task Catalog Specification

**Version:** v0.2 (Draft)

---

# 1. Purpose

This document specifies the normative metamodel of the Task Catalog for **LSG — LOTUSim Scenario Generator**.

---

# 2. Scope

The Task Catalog is the normative repository for operational tasks and their signature-level semantics.

It contains:

- Semantic Families;
- Tasks;
- Typed Signatures;
- Operational Semantics;
- Execution Semantics;
- Traceability.

It does **not** contain HDDL constructs, planner-specific predicates, simulator algorithms or autonomy implementation details. No separate Task Semantics Catalog shall be maintained.

---

# 3. Task Catalog Organization

```text
Task Catalog
│
├── Semantic Families
│     ├── ISR
│     ├── Movement
│     ├── Protection
│     ├── Engagement
│     ├── Support
│     ├── Command & Control
│     └── Logistics
│
└── Tasks
      ├── Detect
      ├── Track
      ├── Navigate
      ├── Escort
      └── ...
```

Semantic Families are first-class elements of the Task Catalog.

---

# 4. Semantic Family Metamodel

Each family defines once:

- operational objective;
- manipulated concepts;
- common state reads and transitions;
- invariants;
- common terminology;
- validation rules.

Tasks reuse these common semantics and only define the specialization required by their typed signatures.

---

# 5. Task Metamodel

Each task defines:

- identifier;
- canonical verb and definition;
- semantic family;
- one or more typed signatures;
- traceability.

A task never duplicates concepts or semantics already defined by its family.

---

# 6. Signature Metamodel

Each signature defines:

- typed parameters;
- required capabilities;
- applicability;
- operational semantics;
- execution semantics;
- specialization of its Semantic Family;
- traceability to missions and ontology concepts where applicable.

Semantics belong to the typed signature, not to the generic task alone.

---

# 7. Signature Semantic Structure

```yaml
semantics:
  semantic_kind: # primitive | abstract | external_event | out_of_planning_scope
  execution_pattern: # instantaneous | durative | continuous

  parameters: []
  reads: []
  invariants: []

  applicability:
    operational: []
    execution: []

  operational_effects:
    world:
      add: []
      remove: []
    knowledge:
      add: []
      remove: []
    resources:
      add: []
      remove: []

  desired_outcomes: []
  completion_conditions: []
  termination_conditions: []
  failure_outcomes: []

  execution:
    responsibility:
```

World state and force-relative knowledge are distinct. Execution information describes how a task may be realized but shall not define its operational meaning.

Abstract tasks express desired outcomes, completion conditions and failure outcomes; their `operational_effects` shall not directly add or remove symbolic state. Primitive tasks may produce symbolic state transitions.

State references remain planner-independent and shall resolve to stable State Model identifiers once that derived artifact exists.

---

# 8. Validation Rules

- Every task belongs to exactly one Semantic Family.
- Every family contains at least one task.
- Every task defines at least one typed signature.
- Common semantics are defined only once at family level.
- Task signatures define only their specialization of family semantics.
- Every signature defines typed parameters, required capabilities where applicable, state reads and/or effects, completion conditions and failure outcomes.
- Abstract signatures do not directly modify symbolic state.
- World-state effects and force-relative knowledge effects are not conflated.
- Ontology concepts and capabilities referenced by a signature exist in the Naval Maritime Ontology.

---

# 9. Traceability and State Model Derivation

```text
Naval Maritime Ontology ─┐
Mission Catalog ─────────┼─> State Model ─> HDDL Domain / Problems
Task Catalog ────────────┘
```

The State Model is derived from relevant ontology relations, task reads and effects, and mission preconditions and objectives. HDDL artifacts are then derived from the State Model; they do not introduce independent business semantics.

---

# 10. v0.2 Consolidation Notes

This v0.2 remains the current draft. The coherence review with DEM-1 added only the elements required to make explicit:

- the absence of a separate Task Semantics Catalog;
- the first-class status of Semantic Families;
- signature-level capability and semantic ownership;
- state reads and invariants;
- the separation of world state and force-relative knowledge;
- the non-mutating nature of abstract tasks;
- the three-source derivation of the State Model.
