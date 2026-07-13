# LOTUSim Domain Engineering Method (DEM)

## Part 1 --- Task Semantics & State Model

**Version:** v0.1 (Draft)

------------------------------------------------------------------------

# 1. Purpose

This document defines the engineering principles governing task
semantics and the symbolic state manipulated by the LOTUSim scenario
generation framework.

The objective is to establish a rigorous, traceable and
planner-independent methodology from which the HDDL domain can be
systematically derived.

------------------------------------------------------------------------

# 2. Overall Architecture

LOTUSim is organized around four domain reference models:

``` text
Naval Ontology
        │
        ▼
Mission Catalog
        │
        ▼
Task Catalog
        │
        ▼
State Model
        │
        ▼
HDDL Domain
```

The **State Model** and the **HDDL Domain** are not primary domain
repositories. They are derived artifacts.

------------------------------------------------------------------------

# 3. Architecture Decisions

## DD-01 --- The Task Catalog is the normative task repository

The Task Catalog is the unique reference describing all supported
LOTUSim tasks.

Task semantics are integrated directly into the Task Catalog.

No separate *Task Semantics Catalog* shall be maintained.

------------------------------------------------------------------------

## DD-02 --- Semantics are defined per task signature

A task may expose multiple typed signatures.

Each signature owns its own semantics.

Example:

-   `Follow(Platform, Platform)`
-   `Follow(Platform, Route)`

These are considered distinct semantic definitions.

------------------------------------------------------------------------

## DD-03 --- Tasks are organized by semantic families

Tasks are grouped into semantic families sharing common concepts.

Initial families are:

-   ISR
-   Movement
-   Protection
-   Engagement
-   Support
-   Command & Control
-   Logistics

------------------------------------------------------------------------

## DD-04 --- The State Model is derived

The State Model is systematically derived from:

-   task inputs;
-   task effects;
-   mission objectives.

It is never authored independently.

------------------------------------------------------------------------

## DD-05 --- Operational semantics and execution are separated

Task semantics distinguish:

-   operational semantics;
-   execution semantics.

Execution mechanisms (plugins, manifests, autonomy services) shall never
define operational meaning.

------------------------------------------------------------------------

## DD-06 --- Abstract tasks do not directly modify the world state

Abstract tasks define:

-   desired outcomes;
-   success conditions;
-   failure conditions.

Only primitive tasks modify the symbolic state.

------------------------------------------------------------------------

## DD-07 --- ISR tasks manipulate knowledge

ISR tasks primarily evolve knowledge rather than the physical world.

Reference knowledge progression:

``` text
Unknown
    ↓
Observed
    ↓
Detected
    ↓
Localized
    ↓
Tracked
    ↓
Classified
    ↓
Identified
```

ISR tasks represent transitions along this progression.

------------------------------------------------------------------------

## DD-08 --- Ground truth and knowledge are distinct

LOTUSim explicitly separates:

-   Ground Truth
-   Force Knowledge

This is consistent with the generation of one HDDL Problem per force.

------------------------------------------------------------------------

# 4. Task Signature Semantic Model

Each task signature is enriched with the following semantic structure:

``` yaml
semantics:

  semantic_kind:

  execution_pattern:

  applicability:

    operational:

    execution:

  operational_effects:

    world:

    knowledge:

    resources:

  desired_outcomes:

  completion_conditions:

  termination_conditions:

  failure_outcomes:

  execution:
```

This model remains independent from HDDL.

------------------------------------------------------------------------

# 5. State Model Construction Method

The State Model is produced through the following workflow:

1.  Extract concepts and relations from the Naval Ontology.
2.  Extract task inputs and effects from the Task Catalog.
3.  Extract mission goals and preconditions from the Mission Catalog.
4.  Merge equivalent state candidates.
5.  Normalize terminology.
6.  Classify states.
7.  Derive the HDDL predicates.

------------------------------------------------------------------------

# 6. Traceability Rules

The following consistency rules shall hold:

-   Every mission references at least one task.
-   Every task owns a semantic specification.
-   Every dynamic state has at least one producer.
-   Every dynamic state has at least one consumer.
-   Every state traces back to the Naval Ontology.
-   Every HDDL predicate originates from the State Model.
-   Every capability is used by at least one task.
-   Every task signature is semantically specified.

------------------------------------------------------------------------

# 7. Roadmap

Semantic families will be specified incrementally in the following
order:

1.  ISR
2.  Movement
3.  Protection
4.  Engagement
5.  Support
6.  Command & Control
7.  Logistics

Each family must be fully validated before moving to the next one.
