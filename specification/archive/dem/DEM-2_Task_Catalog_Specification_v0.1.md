# LOTUSim Domain Engineering Method (DEM)

# DEM-2 — Task Catalog Specification

**Version:** v0.1 (Draft)

---

# 1. Purpose

This document specifies the normative metamodel of the LOTUSim Task Catalog.

It defines how operational tasks shall be modeled independently of HDDL, simulators and autonomy implementations.

The objective is to ensure that every task is modeled consistently and that the State Model and HDDL Domain can be systematically derived.

---

# 2. Scope

The Task Catalog defines:

- operational tasks;
- typed signatures;
- required capabilities;
- operational semantics;
- execution semantics;
- traceability.

It does **not** define:

- HDDL methods;
- HDDL predicates;
- planner-specific concepts;
- simulation algorithms.

---

# 3. Task Metamodel

Each task contains:

- Identifier
- Name
- Definition
- Category
- Semantic family
- Required capabilities
- One or more signatures
- Traceability

A task is an operational verb.

---

# 4. Signature Metamodel

Each signature defines:

- typed parameters;
- operational semantics;
- execution semantics.

Semantics are always attached to the signature, never to the generic task alone.

---

# 5. Semantic Structure

```yaml
semantics:

  semantic_kind:
    # primitive | abstract | external_event

  execution_pattern:
    # instantaneous | durative | continuous

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

# 6. Semantic Families

Every task belongs to one semantic family.

Initial families:

- ISR
- Movement
- Protection
- Engagement
- Support
- Command & Control
- Logistics

A family defines:

- common concepts;
- common state transitions;
- shared terminology;
- validation rules.

---

# 7. Traceability

Each task shall reference:

- Naval Ontology concepts;
- Mission Catalog entries;
- required capabilities.

The Task Catalog shall become the primary source used to derive the State Model.

---

# 8. Validation Rules

Every task shall:

- belong to exactly one semantic family;
- define at least one signature;
- define complete semantics for every signature;
- reference existing ontology concepts only;
- reference existing capabilities only.

Every signature shall define:

- applicability;
- operational effects;
- completion conditions;
- failure outcomes.

---

# 9. Relationships

```
Mission
      │
      ▼
Task
      │
      ▼
Signature
      │
      ▼
Semantics
      │
      ▼
State Model
      │
      ▼
HDDL Domain
```

---

# 10. Roadmap

Semantic families will be specified incrementally:

1. ISR
2. Movement
3. Protection
4. Engagement
5. Support
6. Command & Control
7. Logistics

Once all families are completed, the State Model will be automatically derived and normalized before defining the HDDL Domain.
