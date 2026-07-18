# LOTUSim Method Catalog

> **Status:** pilot working draft
> **Version:** 0.2.0
> **Date:** 2026-07-18
> **Scope:** planner-independent HTN decomposition methods for abstract Task Catalog signatures.

## 1. Purpose

The Method Catalog defines how an abstract operational task may be decomposed into a partially ordered network of typed Task Catalog signatures. It is the normative source for decomposition intent; HDDL methods are derived artifacts and shall not introduce independent doctrine.

Version 0.2.0 remains deliberately limited to `TC-023-S01 Escort Unit`. It
records the validated `start/stop` projection of the close-guard alternative
while keeping operational maturity separate from technical projection
readiness.

## 2. Source boundary

Each method reuses, without redefining:

- ontology classes for parameter types;
- Task Catalog signatures for the decomposed task and every subtask;
- State Model identifiers for method applicability;
- Mission Catalog identifiers for doctrinal evidence and intended use.

A method has no direct world, knowledge or resource effects. Effects remain owned by primitive subtasks or named evaluators. A method only selects, binds, orders and synchronizes subtasks, and maps their outcomes to the parent task.

## 3. Canonical method metamodel

```yaml
id: TM-NNN-SNN-MNN
name: Human-readable method name
status: pilot | candidate | draft | validated | deprecated
version: semantic-version
decomposes: TC-NNN-SNN

parameters:
  - role: variable_name
    type: nmo:Class | SM-TY-NNN
    source:
      kind: parent_task | state_binding
      role: parent_role                 # parent_task only
      state_ref: SM-ST-NNN              # state_binding only
      bindings: {}

applicability: []

task_network:
  subtasks:
    - id: local_subtask_id
      task_ref: TC-NNN-SNN
      bindings: {}
  ordering:
    - {before: first_subtask, after: second_subtask}
  synchronization:
    - {relation: spans, spanning: continuous_subtask, contained: bounded_subtask}

completion_support: []
failure_propagation: []

projection:
  readiness: ready | partial | blocked
  blockers: []

traceability:
  missions: []
  rationale: ...
```

All variables used by state or subtask bindings are declared parameters. A method parameter inherited from the parent task may narrow its type but may not broaden it. A state-bound parameter must be bound by a State Model tuple in the method applicability conditions.

`ordering` captures classical precedence. `synchronization` captures operational relations that cannot be reduced to precedence without changing meaning. In this pilot, `spans(A, B)` means that continuous subtask `A` is active throughout bounded subtask `B`.

## 4. Escort decomposition model

The Escort signature expresses two desired outcomes: the protected unit reaches its destination and remains preserved. Neither outcome is written directly by the abstract task. The methods therefore combine:

1. movement of the protected unit along its assigned route;
2. continuous relative movement of the escort;
3. continuous protection during the transit;
4. external evaluation of destination and preservation criteria.

```text
Escort(escort, protected)
├── Follow(escort, protected) ───────────────┐
├── Guard/Screen(escort, protected) ─────────┤ spans
└── Navigate Route(protected, route) ────────┘
        │
        ├── protected_unit_at_destination
        └── protected_unit_preserved
```

The route is not guessed by the method. It is selected through `SM-ST-105 escort_route_assigned`, introduced by State Model v0.6 from the mission precondition “movement or transit objective defined”.

## 5. Pilot methods

### TM-023-S01-M01 — Close-guard route escort

```yaml
id: TM-023-S01-M01
name: Close-guard route escort
status: pilot
version: 0.2.0
decomposes: TC-023-S01
parameters:
- role: escort_actor
  type: nmo:Platform
  source: {kind: parent_task, role: escort_actor}
- role: protected_unit
  type: nmo:Platform
  source: {kind: parent_task, role: protected_unit}
- role: route
  type: nmo:Route
  source:
    kind: state_binding
    state_ref: SM-ST-105
    bindings: {escort: escort_actor, protected: protected_unit, route: route}
applicability:
- state_ref: SM-ST-006
  bindings: {escort: escort_actor, protected: protected_unit}
- state_ref: SM-ST-105
  bindings: {escort: escort_actor, protected: protected_unit, route: route}
- state_ref: SM-ST-055
  bindings: {protector: escort_actor, protected: protected_unit}
- state_ref: SM-ST-027
  bindings: {holder: escort_actor, target: protected_unit}
- state_ref: SM-ST-004
  bindings: {route: route, entity: protected_unit}
- state_ref: SM-ST-010
  bindings: {entity: escort_actor, capability: TargetFollowingCapability}
- state_ref: SM-ST-010
  bindings: {entity: escort_actor, capability: ProtectionCapability}
- state_ref: SM-ST-010
  bindings: {entity: escort_actor, capability: StationKeepingCapability}
- state_ref: SM-ST-010
  bindings: {entity: protected_unit, capability: RouteFollowingCapability}
task_network:
  subtasks:
  - id: follow_protected_unit
    task_ref: TC-006-S01
    bindings: {actor: escort_actor, followed_unit: protected_unit}
  - id: guard_protected_unit
    task_ref: TC-025-S01
    bindings: {guard_actor: escort_actor, guarded_object: protected_unit}
  - id: transit_protected_unit
    task_ref: TC-001-S02
    bindings: {actor: protected_unit, route: route}
  ordering: []
  synchronization:
  - {relation: spans, spanning: follow_protected_unit, contained: transit_protected_unit}
  - {relation: spans, spanning: guard_protected_unit, contained: transit_protected_unit}
completion_support:
- state_ref: SM-ST-007
  bindings: {protected: protected_unit}
  supported_by: [transit_protected_unit, escort_goal_evaluator]
- state_ref: SM-ST-008
  bindings: {protected: protected_unit}
  supported_by: [guard_protected_unit, protection_outcome_evaluator]
failure_propagation:
- from: follow_protected_unit.target_lost
  decision: reacquire_protected_unit
- from: guard_protected_unit.protection_capability_lost
  parent_outcome: escort_capability_lost
  establishes: {state_ref: SM-ST-014, bindings: {escort: escort_actor, protected: protected_unit}}
- from: transit_protected_unit.route_blocked
  decision: replan_escort_route
projection:
  readiness: ready
  blockers: []
traceability:
  missions: [MC-026, MC-027]
  rationale: Close protection alternative using only signatures with complete operational semantics.
```

### TM-023-S01-M02 — Screened route escort

```yaml
id: TM-023-S01-M02
name: Screened route escort
status: pilot
version: 0.2.0
decomposes: TC-023-S01
parameters:
- role: escort_actor
  type: nmo:Platform
  source: {kind: parent_task, role: escort_actor}
- role: protected_unit
  type: nmo:Platform
  source: {kind: parent_task, role: protected_unit}
- role: route
  type: nmo:Route
  source:
    kind: state_binding
    state_ref: SM-ST-105
    bindings: {escort: escort_actor, protected: protected_unit, route: route}
- role: screen_plan
  type: SM-TY-012
  source:
    kind: state_binding
    state_ref: SM-ST-056
    bindings: {protected: protected_unit, plan: screen_plan}
applicability:
- state_ref: SM-ST-006
  bindings: {escort: escort_actor, protected: protected_unit}
- state_ref: SM-ST-105
  bindings: {escort: escort_actor, protected: protected_unit, route: route}
- state_ref: SM-ST-055
  bindings: {protector: escort_actor, protected: protected_unit}
- state_ref: SM-ST-056
  bindings: {protected: protected_unit, plan: screen_plan}
- state_ref: SM-ST-027
  bindings: {holder: escort_actor, target: protected_unit}
- state_ref: SM-ST-004
  bindings: {route: route, entity: protected_unit}
- state_ref: SM-ST-010
  bindings: {entity: escort_actor, capability: TargetFollowingCapability}
- state_ref: SM-ST-010
  bindings: {entity: escort_actor, capability: ProtectionCapability}
- state_ref: SM-ST-010
  bindings: {entity: protected_unit, capability: RouteFollowingCapability}
task_network:
  subtasks:
  - id: follow_protected_unit
    task_ref: TC-006-S01
    bindings: {actor: escort_actor, followed_unit: protected_unit}
  - id: screen_protected_unit
    task_ref: TC-024-S01
    bindings: {screen_actor: escort_actor, protected_force: protected_unit, screen_plan: screen_plan}
  - id: transit_protected_unit
    task_ref: TC-001-S02
    bindings: {actor: protected_unit, route: route}
  ordering: []
  synchronization:
  - {relation: spans, spanning: follow_protected_unit, contained: transit_protected_unit}
  - {relation: spans, spanning: screen_protected_unit, contained: transit_protected_unit}
completion_support:
- state_ref: SM-ST-007
  bindings: {protected: protected_unit}
  supported_by: [transit_protected_unit, escort_goal_evaluator]
- state_ref: SM-ST-008
  bindings: {protected: protected_unit}
  supported_by: [screen_protected_unit, protection_outcome_evaluator]
failure_propagation:
- from: follow_protected_unit.target_lost
  decision: reacquire_protected_unit
- from: screen_protected_unit.protection_capability_lost
  parent_outcome: escort_capability_lost
  establishes: {state_ref: SM-ST-014, bindings: {escort: escort_actor, protected: protected_unit}}
- from: screen_protected_unit.persistent_screen_gap
  decision: reconfigure_screen
- from: transit_protected_unit.route_blocked
  decision: replan_escort_route
projection:
  readiness: partial
  blockers:
  - Screen Protected Force requires at least one complete decomposition method before primitive closure is achieved.
traceability:
  missions: [MC-026, MC-027, MC-031, MC-032]
  rationale: Layered-protection alternative selected when a protection plan is available.
```

## 6. Pilot findings

The Escort pilot establishes five design decisions:

1. Decomposition belongs to a Method Catalog, not to the Task Catalog or generated HDDL.
2. Methods reference typed signatures, never verb names alone.
3. Method-specific type narrowing is required: the current generic Escort signature admits any physical entity, while these two methods apply only to a mobile `nmo:Platform` protecting another `nmo:Platform`.
4. A route must be explicitly assigned; route selection cannot be inferred from all traversable routes.
5. Operational overlap remains explicit in the Method Catalog and is compiled
   by the LOTUSim HDDL profile; projection does not weaken `spans` into ordinary
   precedence.

Convoy escort is not silently treated as single-platform escort. `MC-027` may use these methods only when its protected subject is represented by a lead platform. A canonical `nmo:PlatformGroup` movement and integrity decomposition remains a separate method increment.

## 7. HDDL projection status

The LOTUSim HDDL Profile v0.1 compiles `spans` through explicit `start/stop`
lifecycle actions. `TM-023-S01-M01` is primitively closed and has been projected
to the experimental MC-026 fragment. Unified Planning 1.3.0 parsed the fragment
and Aries 0.5.0 returned the expected six-action primitive plan.

`TM-023-S01-M01` is therefore `projection.readiness: ready`. Its method status
remains `pilot`: projection readiness is a technical property, whereas promotion
to `draft` additionally requires operational expert review and validation of the
execution-adapter lifecycle contract.

`TM-023-S01-M02` remains `partial` only because `TC-024-S01 Screen Protected
Force` lacks a complete decomposition method. The continuous-task compilation
is no longer a blocker shared by the two alternatives.

## 8. Changes from v0.1.0 to v0.2.0

- recorded the selected `start/stop` compilation from HDDL Profile v0.1;
- promoted the close-guard method projection readiness from `partial` to `ready`;
- removed the obsolete continuous-task blocker from both Escort alternatives;
- retained primitive closure of Screen as the only projection blocker for the
  screened alternative;
- separated technical projection readiness from operational method maturity.
