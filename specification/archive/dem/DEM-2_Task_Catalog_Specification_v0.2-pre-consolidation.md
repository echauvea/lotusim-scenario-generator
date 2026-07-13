# LOTUSim Domain Engineering Method (DEM)

# DEM-2 — Task Catalog Specification

**Version:** v0.2 (Draft)

---

# 1. Purpose

This document specifies the normative metamodel of the LOTUSim Task Catalog.

---

# 2. Scope

The Task Catalog is the normative repository describing operational behaviour.

It contains:

- Semantic Families
- Tasks
- Typed Signatures
- Operational Semantics
- Execution Semantics
- Traceability

It does **not** contain HDDL constructs.

---

# 3. Task Catalog Organization

```
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
- common state transitions;
- invariants;
- common terminology;
- validation rules.

Tasks inherit these common semantics and only define their specialization.

---

# 5. Task Metamodel

Each task defines:

- identifier;
- definition;
- semantic family;
- required capabilities;
- typed signatures;
- traceability.

A task never duplicates concepts already defined by its family.

---

# 6. Signature Metamodel

Each signature defines:

- typed parameters;
- applicability;
- operational semantics;
- execution semantics;
- specialization of its semantic family.

---

# 7. Signature Semantic Structure

```yaml
semantics:
  semantic_kind:
  execution_pattern:

  applicability:
    operational:
    execution:

  operational_effects:
    world:
      add:
      remove:
    knowledge:
      add:
      remove:
    resources:
      add:
      remove:

  desired_outcomes:
  completion_conditions:
  termination_conditions:
  failure_outcomes:

  execution:
```

---

# 8. Validation Rules

- Every task belongs to exactly one semantic family.
- Every family contains at least one task.
- Common semantics shall be defined only once at family level.
- Tasks only define their specialization.
- Every signature shall define complete semantics.

---

# 9. Traceability

Ontology → Mission Catalog → Task Catalog → State Model → HDDL Domain

The State Model is derived from the complete Task Catalog (families + tasks).
