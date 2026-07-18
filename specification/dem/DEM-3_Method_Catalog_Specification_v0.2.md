# LSG Domain Engineering Method (DEM)

# DEM-3 — Method Catalog Specification

**Version:** v0.2 (Draft)

---

# 1. Purpose

This document defines the planner-independent metamodel and design rules for HTN decomposition methods in LSG. It complements DEM-1 task/state semantics and DEM-2 Task Catalog structure.

# 2. Authority and derivation chain

The Method Catalog is the normative source for accepted task decompositions. It consumes but does not redefine the Ontology, Mission Catalog, Task Catalog or State Model. HDDL methods are derived from it under the LOTUSim HDDL profile.

```text
Ontology ───────────────┐
Mission Catalog ────────┼─> Method Catalog ─> HDDL methods
Task Catalog ───────────┤
State Model ────────────┘
```

# 3. Method identity

Method identifiers use `TM-NNN-SNN-MNN`, where `NNN-SNN` identifies the decomposed Task Catalog signature and `MNN` identifies one alternative method for that signature. Identifiers remain stable when labels or planner projections change.

# 4. Normative rules

- **MDR-01 — Abstract parent.** A method shall decompose exactly one existing Task Catalog signature whose `semantic_kind` is `abstract`.
- **MDR-02 — Typed subtasks.** Every subtask shall reference an existing typed signature, not a verb alone.
- **MDR-03 — Explicit variables.** Every variable used in a binding shall be declared as a typed method parameter.
- **MDR-04 — Binding source.** Every parameter shall originate from the parent task or from an explicit State Model tuple.
- **MDR-05 — Type safety.** Method bindings may narrow parent types and shall be compatible with the parameter types of referenced task signatures and states.
- **MDR-06 — Applicability.** Method selection conditions shall use stable State Model identifiers and exact tuple bindings.
- **MDR-07 — No method effects.** Methods do not own world, knowledge or resource effects. Primitive subtasks and named evaluators remain the only producers.
- **MDR-08 — Outcome coverage.** Every parent desired outcome or completion condition shall identify the subtasks and evaluators that support it.
- **MDR-09 — Failure propagation.** Relevant subtask failures shall map to a declared parent outcome or an explicit replanning decision.
- **MDR-10 — Ordering versus synchronization.** Classical precedence belongs in `ordering`; overlap, spanning and handover constraints belong in `synchronization` and shall not be weakened into arbitrary ordering.
- **MDR-11 — Alternative methods.** Multiple applicable methods are valid HTN alternatives. Their discriminating conditions shall become explicit before operational validation.
- **MDR-12 — Projection readiness.** Each method declares `ready`, `partial` or `blocked` plus concrete blockers.
- **MDR-13 — Mission evidence.** Each method traces to the missions that justify or exercise it.
- **MDR-14 — Primitive closure.** A method is primitively closed only when every abstract subtask recursively has at least one applicable method leading to primitive signatures.

# 5. Canonical structure

The canonical YAML structure is defined in the current Method Catalog. The following collections are mandatory even when empty:

- `parameters`;
- `applicability`;
- `task_network.subtasks`;
- `task_network.ordering`;
- `task_network.synchronization`;
- `completion_support`;
- `failure_propagation`;
- `projection.blockers`;
- `traceability.missions`.

# 6. HDDL boundary

The Method Catalog is not planner syntax. Directly projectable concepts include typed parameters, method preconditions, subtasks and partial ordering. Synchronization constraints require an explicit rule in the LOTUSim HDDL profile.

A generator shall reject a method whose projection readiness is not `ready`; it shall not discard unsupported synchronization or failure semantics. Projection readiness is independent of the method's operational maturity status: a `pilot` method may be technically `ready`, while expert review and runtime evidence remain required before promotion to `draft`.

# 7. Escort pilot decisions

The first pilot defines two alternatives for `TC-023-S01`:

- close-guard route escort, using only semantically complete primitive signatures;
- screened route escort, retaining `Screen Protected Force` as an intermediate abstract subtask.

Both alternatives require continuous following and protection to span the
protected unit's route transit. HDDL Profile v0.1 now defines the `start/stop`
compilation for this relation. The close-guard alternative is primitively closed
and technically ready; the screened alternative remains partial because Screen
has no complete decomposition.

The pilot also requires `SM-ST-105 escort_route_assigned`, because a method cannot infer the intended route from the set of routes that happen to be traversable.

# 8. Validation requirements

A conforming Method Catalog increment shall verify:

- identifier uniqueness and conformance;
- existence and abstractness of the decomposed signature;
- existence of every subtask signature;
- parameter and binding completeness;
- State Model reference and tuple correctness;
- compatibility of ontology and State Model types;
- validity of ordering and synchronization subtask references;
- mission traceability;
- non-empty blockers for `partial` or `blocked` methods;
- outcome coverage and failure propagation references.

# 9. Next decisions

1. validate the Escort methods through the `escort-v0.1` expert campaign;
2. validate the `start/stop` lifecycle through the LSG/tsm execution-adaptation path;
3. define at least one Screen decomposition for primitive closure of the screened alternative;
4. model convoy/group movement separately instead of reusing the single-platform method implicitly.

# 10. Changes from v0.1 to v0.2

- distinguished operational method maturity from technical projection readiness;
- recorded the selected `start/stop` compilation for `spans`;
- recorded successful projection and Aries validation of the close-guard method;
- retained Screen primitive closure, expert review and runtime lifecycle validation as open work.
