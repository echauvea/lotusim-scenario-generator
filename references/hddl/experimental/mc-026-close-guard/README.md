# MC-026 close-guard HDDL fragment

This directory contains the first experimental HDDL projection for LSG. It
projects `TM-023-S01-M01` against `MC-026` under the
[LOTUSim HDDL Profile v0.1](../../../../specification/hddl/LOTUSim_HDDL_Profile_v0.1.md).

## Files

- [`domain.hddl`](domain.hddl): minimal domain fragment and compiled Escort method;
- [`problem.hddl`](problem.hddl): one deterministic MC-026 happy-path instance;
- [`traceability.yaml`](traceability.yaml): explicit mappings to normative sources.

## Expected primitive sequence

```text
start-follow-designated-unit escort-1 protected-hvu-1
start-guard-object escort-1 protected-hvu-1
navigate-route protected-hvu-1 escort-route-1 transit-destination transit-origin
evaluate-escort-destination protected-hvu-1 escort-route-1 transit-destination
stop-guard-object escort-1 protected-hvu-1
stop-follow-designated-unit escort-1 protected-hvu-1
```

The lifecycle boundaries preserve both `spans` constraints in the symbolic
plan. Follow and Guard remain active execution objectives while Navigate Route
runs. Their actual continuous control and invariant monitoring are outside the
level-1 planner.

## Planner validation

On 2026-07-18, the fragment was parsed and solved without modification using
Unified Planning 1.3.0 and Aries 0.5.0. Aries returned
`SOLVED_SATISFICING` and exactly the primitive sequence above.

To reproduce the check in an isolated Python 3.12 environment:

```text
python -m pip install -r tools/planning/requirements-aries.txt
python tools/planning/run_mc026_aries.py
```

The runner checks both solvability and exact primitive ordering. The CI repeats
this test whenever the HDDL fragment, profile or planner tooling changes.

## Interpretation limits

- The fragment is derived and non-normative.
- `protected-unit-preserved` is supplied as an externally evaluated planning
  snapshot; Guard does not create it.
- Failures are runtime events leading to supervision or replanning, not planner
  choices in this deterministic fragment.
- Convoy escort and the screened Escort method are outside this pilot.
