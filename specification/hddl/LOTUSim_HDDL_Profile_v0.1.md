# LOTUSim HDDL Profile

> **Version:** v0.1
> **Status:** experimental pilot
> **Scope:** projection of `TM-023-S01-M01` for `MC-026`
> **Decision date:** 2026-07-18

## 1. Purpose

This profile defines the smallest HDDL subset and compilation rules needed to
project the close-guard Escort pilot without adding business semantics to HDDL.
It is a projection contract, not an independent source of naval doctrine.

The normative inputs remain:

- the Ontology for concepts and types;
- the Mission Catalog for `MC-026` and its objective;
- the Task Catalog for typed task semantics;
- the State Model for every dynamic predicate;
- the Method Catalog for `TM-023-S01-M01` and its `spans` constraints.

The experimental fragment is located in
[`references/hddl/experimental/mc-026-close-guard/`](../../references/hddl/experimental/mc-026-close-guard/README.md).

## 2. Supported language subset

Version 0.1 uses classical HDDL with:

- typed objects and parameters (`:typing`);
- compound tasks and decomposition methods (`:hierarchy`);
- method preconditions (`:method-preconditions`);
- totally ordered task networks for the compiled pilot;
- positive preconditions and positive or negative action effects.

The pilot excludes temporal actions, numeric fluents, costs, conditional
effects, derived predicates, quantified formulae and planner-specific syntax.
The level-1 planner therefore reasons about causal structure only. Continuous
control and invariant monitoring remain execution responsibilities at levels 2
and 3, in accordance with LSG Architecture v3.2.

## 3. Traceability rules

1. Every HDDL type shall map to an Ontology class or a State Model-owned type.
2. Every HDDL predicate shall map one-to-one to a normative State Model entry.
3. Every compound task shall map to an abstract Task Catalog signature.
4. Every ordinary primitive action shall map to a primitive Task Catalog
   signature.
5. A lifecycle action may be generated from one continuous primitive signature;
   it is a projection phase and does not receive a new Task Catalog identifier.
6. An evaluator action shall map to a named external producer already declared
   by the State Model and cited by the Method Catalog.
7. HDDL names use lower-case kebab-case projections of their source symbols.
8. The compiler may lift a primitive subtask's `state_at_start` parameters into
   HDDL method variables only when each variable is constrained by the exact
   State Model tuple declared by that signature. Such variables are projection
   bindings, not additional Method Catalog parameters.

The fragment's [`traceability.yaml`](../../references/hddl/experimental/mc-026-close-guard/traceability.yaml)
records these mappings explicitly.

## 4. Continuous-task lifecycle

### 4.1 Start and stop

For a continuous primitive signature `C` whose active relation is represented by
a normative fluent `A`:

- `start-C` checks the signature's applicability conditions and invariants, then
  asserts `A`;
- `stop-C` requires `A`, then retracts it;
- the retraction is lifecycle bookkeeping derived from normal termination; it
  does not represent a new operational outcome.

This rule is only applicable when the State Model describes `A` as an active
fluent and provides an update policy compatible with assertion and retraction.
Otherwise projection shall fail.

For this pilot:

| Signature | Start/stop fluent | State Model justification |
|---|---|---|
| `TC-006-S01 Follow Designated Unit` | `SM-ST-005 following` | Active following relation; `fluent`; `assert_retract` |
| `TC-025-S01 Guard Object` | `SM-ST-059 guarding` | Active guarding relation; `fluent`; `assert_while_task_active` |

### 4.2 Compilation of `spans`

For `spans(C, B)`, where continuous subtask `C` must remain active throughout
bounded subtask `B`, version 0.1 compiles the constraint as:

```text
start-C < B < stop-C
```

The active fluent asserted by `start-C` persists across `B` and is retracted
only by `stop-C`. The execution adaptation layer shall interpret the interval
between these lifecycle commands as an active continuous objective.

When several continuous tasks span the same bounded task, all starts precede
the bounded task and all stops follow it. HDDL v0.1 linearizes otherwise
concurrent lifecycle commands to obtain a deterministic totally ordered pilot.
That relative order is technical and carries no doctrinal meaning.

The chosen linearization for `TM-023-S01-M01` is:

```text
start Follow
start Guard
Navigate Route
evaluate destination
stop Guard
stop Follow
```

### 4.3 No planner-level maintain loop

Version 0.1 generates no periodic `maintain` action. Repeated symbolic checks
would introduce an arbitrary time discretization. Instead:

- the executor monitors the Task Catalog invariants while the objective is
  active;
- normal Task Catalog termination conditions trigger the corresponding stop;
- failures and recoverable events follow the Method Catalog mappings and may
  trigger level-1 replanning.

## 5. State and outcome boundary

Only State Model symbols may appear as HDDL predicates. The compiler shall not
invent predicates such as `follow-started`, `guard-maintained` or
`escort-successful`.

`SM-ST-007 protected_unit_at_destination` is produced in the fragment by the
named `escort_goal_evaluator`, after route completion and location agreement.

`SM-ST-008 protected_unit_preserved` remains an externally evaluated,
mission-relative state. The problem initializes its planning snapshot from the
WAL; no HDDL action claims to create preservation merely because Guard is
active. The execution environment must reassess this outcome during and at the
end of the run.

## 6. Failure and replanning boundary

The first fragment is a deterministic happy-path planning experiment. HDDL v0.1
does not encode failures as selectable actions and does not claim that the plan
guarantees mission success.

The following Method Catalog decisions remain execution/replanning contracts:

- `target_lost` -> `reacquire_protected_unit`;
- `protection_capability_lost` -> `escort_capability_lost`;
- `route_blocked` -> `replan_escort_route`.

An execution adapter shall stop or invalidate affected continuous objectives
before requesting a new level-1 Planning Model.

## 7. Projection rejection rules

Generation shall fail rather than weaken the model when:

- a predicate has no normative State Model mapping;
- a continuous task has no explicit active fluent;
- a stop phase would require an untraceable effect;
- a `spans` relation cannot be compiled into lifecycle boundaries;
- a required abstract subtask lacks primitive closure;
- a mission outcome would have to be fabricated as a task effect;
- a planner requires syntax outside the declared profile.

## 8. Pilot conformance and limitations

The MC-026 fragment demonstrates syntactic projection and preservation of the
two `spans` constraints through lifecycle ordering. On 2026-07-18, Unified
Planning 1.3.0 parsed the fragment and Aries 0.5.0 returned the exact expected
six-action primitive plan. This validates the pilot against one selected
toolchain, but not against every HDDL implementation.

The pilot does not yet demonstrate:

- portability across other HDDL planners;
- execution-adapter interpretation of start/stop commands;
- runtime monitoring of continuous invariants;
- recovery and replanning under injected failures;
- convoy or platform-group escort;
- primitive closure of the screened Escort alternative.

The profile shall remain experimental until the fragment is executed through
the LSG/tsm adaptation path and the lifecycle contract is validated at runtime.

## 9. External language references

- [HDDL — A Language to Describe Hierarchical Planning Problems](https://ojs.aaai.org/index.php/AAAI/article/view/6542)
- [IPC 2020 HDDL input language and requirement tags](https://ipc2020.hierarchical-task.net/benchmarks/input-language)
