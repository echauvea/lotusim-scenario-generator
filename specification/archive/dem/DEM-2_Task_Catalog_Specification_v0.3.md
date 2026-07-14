# LSG Domain Engineering Method (DEM)

# DEM-2 — Task Catalog Specification

**Version:** v0.3 (Draft)

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

## 6.1 Parameter and binding sources

Every parameter defines a unique role, a controlled type reference and its source:

- `task_input`: supplied when the task instance is created;
- `state_at_start`: captured by matching an explicit state tuple before any task effect is applied.

```yaml
parameters:
  - role: actor
    type: MobilePlatform
    source: task_input
  - role: origin
    type: Location
    source:
      kind: state_at_start
      state: located_at
      bindings: {entity: actor, location: origin}
```

Every variable appearing in `bindings` shall resolve to a declared parameter. Ontology concepts used as constants, such as a capability class, are exempt from parameter declaration but shall resolve in the ontology.

A removal effect shall name the same State Model identifier as the tuple it removes and bind every component needed to identify that tuple. Placeholder identifiers such as `located_at_previous_location` are invalid.

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

For `instantaneous` and `durative` signatures, `completion_conditions` define successful completion. For `continuous` signatures, `termination_conditions` define the normal reasons why execution stops; termination is not failure unless a matching `failure_outcome` is established.

---

# 8. Validation Rules

- Every task belongs to exactly one Semantic Family.
- Every family contains at least one task.
- Every task defines at least one typed signature.
- Common semantics are defined only once at family level.
- Task signatures define only their specialization of family semantics.
- Every signature defines typed parameters, required capabilities where applicable, state reads and/or effects, and failure outcomes.
- Instantaneous and durative signatures define completion conditions; continuous signatures define normal termination conditions.
- Every signature declares exactly one execution pattern.
- Every binding variable resolves to a parameter declared by the same signature.
- Every parameter declares a valid binding source.
- Every state removal identifies a complete, explicitly bound tuple and does not use a pseudo-state for a previous value.
- Every continuous signature declares at least one normal termination condition.
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

Version v0.2 consolidated the elements required to make explicit:

- the absence of a separate Task Semantics Catalog;
- the first-class status of Semantic Families;
- signature-level capability and semantic ownership;
- state reads and invariants;
- the separation of world state and force-relative knowledge;
- the non-mutating nature of abstract tasks;
- the three-source derivation of the State Model.

---

# 11. Changes from v0.2 to v0.3

- Stabilized the signature semantic structure used by the semantic pilot.
- Added explicit parameter sources and state-at-start capture.
- Required complete typed bindings for all state references and tuple-exact state removal.
- Prohibited placeholder state identifiers for unknown previous values.
- Made execution patterns mandatory and clarified normal termination of continuous tasks.
- Confirmed that abstract tasks express desired outcomes but have no direct operational effects.
