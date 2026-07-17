# LOTUSim Task Catalog

> **Status:** working draft
> **Version:** 0.12.0
> **Date:** 2026-07-17
> **Scope:** reusable operational actions expressed as canonical verbs with typed signatures and state-based operational semantics.

## 1. Purpose

The Task Catalog defines the controlled action vocabulary used by LOTUSim missions, scenarios and derived planning artefacts.

A Task is represented by a canonical verb. Its complement is not part of the task identity: it is expressed through one or more typed signatures.

The catalog does not define HDDL methods, ordering, planner-specific predicates, execution algorithms or autonomy behaviours. It does define planner-independent operational semantics for each typed signature: state read, state changes, completion conditions and failure outcomes.

## 2. Task meta-model

```text
Task
├── Identity
├── Typed signatures
│   ├── Typing and capability classification
│   └── Operational semantics
└── Traceability
```

### 2.1 Identity

- `id`: stable identifier `TC-NNN`;
- `verb`: canonical English infinitive verb;
- `status`: `candidate`, `draft`, `validated`, `deprecated`;
- `version`: semantic version.

### 2.2 Typed signatures

A verb may expose several signatures when actor or argument types materially differ. Signatures preserve semantic precision without multiplying task identities.

**Changed in 0.3.0 — capability classification moved to signature level.** In 0.2.0, `capability_type` and `implements_capabilities` were task-level attributes. This broke the catalog's own boundary rule for verbs whose signatures carry materially different semantics (e.g. `Search`: searching an area is perception; searching a vessel is interdiction). Each signature now carries:

- `signature_id`: stable identifier `TC-NNN-SNN`;
- `semantic_family`: exactly one Semantic Family identifier `SF-NN`;
- `capability_type`: one Capability Type (editorial grouping, see §3);
- `implements_capabilities`: references to the **most specific applicable** Naval Ontology Capability classes.

The family view of a generic task is derived as the set union of the `semantic_family` values of its signatures. It is not maintained as an independent normative field.

Referencing the most specific ontology class is what makes the resolution chain to typed execution actions work: capability classes carrying an `nmo:manifestKey` annotation (e.g. `TargetFollowingCapability → navigation.follow_target`) resolve a task signature to the typed action family of the 2 ↔ 3 execution contract, by simple ontology traversal, without any additional mapping table.


### 2.3 Operational semantics

Operational semantics are defined at **signature level** because signatures of the same verb may read or modify different state concepts. They remain independent of HDDL syntax and execution implementation.

Each signature defines:

- `semantic_kind`: `primitive`, `abstract`, `external_event`, or `out_of_planning_scope`;
- `execution_pattern`: `instantaneous`, `durative`, or `continuous`;
- `parameters`: explicit typed roles and their binding sources;
- `reads`: state concepts required or consulted without being modified;
- `invariants`: state concepts that must remain true during execution;
- `applicability`: operational and execution conditions;
- `operational_effects`: separate world, knowledge and resource transitions;
- `desired_outcomes`: intent-level results, primarily for abstract tasks;
- `completion_conditions`: observable successful completion conditions;
- `termination_conditions`: normal reasons for stopping a continuous task;
- `failure_outcomes`: named failure outcomes and the state concepts they establish;
- `execution.responsibility`: the layer expected to execute or supervise the task.

Every state reference in a fully enriched signature uses `state_ref` with a stable identifier from the normative State Model. The readable symbol, category and canonical tuple signature are defined only by that model. Signatures not yet enriched contain no normative state references.

Every binding variable resolves to a typed parameter declared by the same signature. Parameter values are supplied as `task_input`, captured explicitly from `state_at_start`, or produced as `execution_output`. Removal effects identify the exact bound tuple to remove; pseudo-states representing an unknown previous value are forbidden.

#### Semantic notation

```yaml
semantics:
  semantic_kind: primitive
  execution_pattern: durative
  parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: destination
      type: nmo:SpatialRegion
      source: task_input
    - role: origin
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-001
        bindings: {entity: actor, location: origin}
  reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: WaypointNavigationCapability}
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
  completion_conditions:
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: destination}
  termination_conditions: []
  failure_outcomes: []
  execution:
    responsibility: platform_autonomy
```

### 2.4 Traceability

- `used_by_missions`: Mission Catalog references;
- `legacy_task_names`: previous compound names retained for migration.

**Changed in 0.3.0 — legacy identifier namespace.** Legacy (pre-consolidation) task identifiers are now prefixed `TCL-NNN` to eliminate collisions with the canonical `TC-NNN` namespace.

## 3. Capability Types

Capability Types are an **editorial grouping layer** over the Naval Ontology Capability hierarchy. They ease human navigation of the inventory; they carry no semantics of their own and do not map one-to-one onto the ontology hierarchy. Whether this layer is retained or replaced by the ontology hierarchy itself is an open decision (see §10).

| ID | Capability Type | Scope |
|---|---|---|
| CT-01 | Mobility | Move, position or control the motion of a platform. |
| CT-02 | Perception | Observe, detect, localize, classify, identify, track or characterize. |
| CT-03 | Assessment | Transform observations and state into operational assessments. |
| CT-04 | Protection | Preserve another entity, group, area, infrastructure or service. |
| CT-05 | Engagement and Interdiction | Constrain, intercept, engage, neutralize or apply an authorized effect. |
| CT-06 | Recovery and Emergency Response | Locate, retrieve, assist, stabilize or evacuate. |
| CT-07 | Deployment | Launch, deploy, dock or recover hosted systems and payloads. |
| CT-08 | Sustainment and Logistics | Transport, transfer, resupply, recharge, refuel or tow. |
| CT-09 | Communication | Report, share, relay, establish or transmit information. |
| CT-10 | Coordination and Command Support | Assign, coordinate, request or update collective action. |
| CT-11 | Electromagnetic Activities | Detect, characterize, monitor, jam or deceive in the electromagnetic environment. |

Capabilities are ontology concepts. The Task Catalog references them but does not redefine their physical semantics.

### 3.1 Semantic Families

Semantic Families centralize the operational meaning shared by several typed signatures. Unlike Capability Types, they are normative semantic groupings: every signature belongs to exactly one family. A generic verb may span several families when its typed signatures have materially different meanings.

| ID | Family | Operational objective |
|---|---|---|
| SF-01 | ISR | Increase force-relative knowledge of the operational environment without changing the observed reality. |
| SF-02 | Movement | Change or preserve the position, route, formation or motion of a mobile entity. |
| SF-03 | Protection | Preserve a designated entity, group, area, infrastructure or service from a threat. |
| SF-04 | Engagement | Constrain, compel, interdict, degrade or neutralize a designated target under authorization. |
| SF-05 | Support | Assist, recover or stabilize a beneficiary without owning the primary operational effect. |
| SF-06 | Command & Control | Create, exchange, maintain and coordinate operational information, tasks and plans. |
| SF-07 | Logistics | Move, transfer, deploy, recover or replenish platforms, payloads and consumable resources. |

```yaml
semantic_families:
  - id: SF-01
    name: ISR
    operational_objective: Increase force-relative knowledge without changing observed reality.
    manipulated_concepts: [observation, entity, emission, area, location, classification, identity, track, characterization, inspection]
    common_semantics:
      reads: [sensor_availability, observation_context]
      invariants: [world_knowledge_separation, force_relative_knowledge]
      transitions: [area_observed, entity_or_emission_detected, location_estimate_produced, classification_assessed, identity_assessed, track_established_or_updated, subject_characterized_or_inspected]
    terminology: [observe, detect, localize, classify, identify, track, characterize, correlate]
    validation_rules:
      - Knowledge effects identify the observing force or information holder.
      - A knowledge transition never directly changes the corresponding world fact.
      - Detection is the common basis; localization, classification and tracking are not a mandatory linear sequence.
      - Search and coverage results are relative to an explicit holder and command-defined requirement.
      - Survey, map and measurement products preserve scope and producing-platform provenance.
      - Characterization and inspection products are requirement-scoped and preserve subject, quality and producing-platform provenance.

  - id: SF-02
    name: Movement
    operational_objective: Change or preserve the position or motion of a mobile entity.
    manipulated_concepts: [mobile_entity, location, route, station, formation, followed_entity]
    common_semantics:
      reads: [mobility_capability, navigation_constraints]
      invariants: [movement_continuity, actor_identity]
      transitions: [movement_started, location_changed, station_or_formation_maintained, movement_terminated]
    terminology: [navigate, patrol, follow, shadow, approach, withdraw, transit, evade]
    validation_rules:
      - Location removal identifies the exact entity-location tuple captured at task start.
      - Continuous movement signatures declare explicit termination conditions.
      - Active movement relations are distinct from completion conditions.
      - Target-relative movement reads holder-relative location or track knowledge without asserting new knowledge.

  - id: SF-03
    name: Protection
    operational_objective: Preserve a designated entity, group, area, infrastructure or service.
    manipulated_concepts: [protected_entity, protected_area, threat, screen, guard_relation, defensive_posture]
    common_semantics:
      reads: [protection_requirement, threat_state]
      invariants: [protected_subject_identity, authorization_validity]
      transitions: [protection_established, protection_maintained, threat_handled]
    terminology: [escort, screen, guard, interpose, defend]
    validation_rules:
      - The protected subject is explicitly bound.
      - Abstract protection tasks express desired outcomes rather than direct world effects.
      - Active guarding and interposition relations remain distinct from derived protection outcomes.
      - Decoy deployment changes physical deployment and custody state, while its protective effect is derived.

  - id: SF-04
    name: Engagement
    operational_objective: Constrain, compel, interdict, degrade or neutralize a designated target.
    manipulated_concepts: [target, authorization, rules_of_engagement, engagement_action, applied_effect]
    common_semantics:
      reads: [target_state, authorization_state, rules_of_engagement]
      invariants: [target_discrimination, authorization_validity]
      transitions: [target_intercepted, target_constrained, effect_applied, target_neutralized]
    terminology: [search_vessel, block, intercept, hail, direct, compel, board, seize, engage, neutralize, jam]
    validation_rules:
      - Every effect-bearing signature binds a designated target.
      - Authorization and applicable rules of engagement are explicit applicability conditions.

  - id: SF-05
    name: Support
    operational_objective: Assist, recover or stabilize a beneficiary without owning the primary operational effect.
    manipulated_concepts: [beneficiary, condition, assistance, recovery, stabilization, evacuation]
    common_semantics:
      reads: [beneficiary_condition, support_capability]
      invariants: [beneficiary_identity, handover_continuity]
      transitions: [beneficiary_marked, assistance_provided, condition_stabilized, beneficiary_evacuated]
    terminology: [recover_person, locate_missing_entity, assist, stabilize, evacuate]
    validation_rules:
      - The beneficiary and requested support outcome are explicit.
      - Handover or completion conditions identify the receiving responsibility when applicable.

  - id: SF-06
    name: Command & Control
    operational_objective: Create, exchange, maintain and coordinate operational information, tasks and plans.
    manipulated_concepts: [report, track_information, command, tasking, plan, communication_link]
    common_semantics:
      reads: [information_state, command_relationship, communication_availability]
      invariants: [information_provenance, intended_audience, information_integrity]
      transitions: [information_reported_or_shared, action_requested_or_assigned, coordination_established, information_updated]
    terminology: [maintain_picture, maintain_link, report, share, request, assign, coordinate, relay, establish, transmit, update]
    validation_rules:
      - Information producer, recipient and provenance are explicit when applicable.
      - Knowledge transfer does not imply a world-state change.

  - id: SF-07
    name: Logistics
    operational_objective: Move, transfer, deploy, recover or replenish platforms, payloads and resources.
    manipulated_concepts: [carrier, payload, custody, resource, energy, docking_relation]
    common_semantics:
      reads: [resource_availability, compatibility, custody_state]
      invariants: [custody_continuity, platform_payload_compatibility, resource_conservation]
      transitions: [payload_deployed_or_launched, payload_recovered, platform_docked, custody_transferred, resource_replenished]
    terminology: [deploy, launch, recover, dock, transport, transfer, resupply, recharge, refuel, tow]
    validation_rules:
      - Source, destination and custody transfer are explicit when applicable.
      - Resource effects preserve units and conservation constraints.
```

For ISR, the states form a knowledge graph rather than a mandatory pipeline. Observation produces evidence about an area without asserting that an object exists. Detection establishes a holder-relative contact or emission. Localization, classification and tracking may then progress independently from detection according to available sensors and evidence. Identification normally uses a classification, but may also use direct identity evidence. Tracking is continuous and may update estimates without changing the physical target.

Area-search and survey completion are requirement-relative. A search may satisfy its requirement either by resolving the sought object or by certifying the commanded search coverage without detection; neither case asserts physical absence beyond the stated confidence and coverage standard. Survey, seabed-map and measurement outputs are immutable holder-relative knowledge products with explicit spatial scope and producing-platform provenance. Measuring an environmental property produces information and never changes the measured environment.

Characterization extends classification with requirement-scoped observable properties, condition or behavior; it does not replace class or identity assessments. Inspection produces a scoped evidence record and findings about a designated object or infrastructure. Both results are immutable, holder-relative and provenance-bearing, and neither asserts that the physical subject changed.

The types represented by `SM-TY-001` through `SM-TY-009` are State Model-owned information types. They are not silently introduced as Naval Ontology classes.

| Candidate knowledge state | Producer in this increment | Current consumer |
|---|---|---|
| `observation_available`, `observation_covers` | Observe | Future correlation and assessment tasks |
| `detected` | Detect Object | Localize, Classify, Identify, Track, Characterize and Inspect |
| `emission_detected` | Detect Emission | Characterize Emission |
| `localized` | Localize | Mission goals and future assessment tasks |
| `classified`, `classification_available` | Classify | Identify and mission goals |
| `identified` | Identify | Mission goals and downstream engagement/support tasks |
| `track_established`, `track_maintained` | Track | Mission goals and future reporting/engagement tasks |
| `object_characterization_satisfies`, `emission_characterization_satisfies` | Characterize | Mission goals and future assessment/reporting tasks |
| `inspection_satisfies` | Inspect | Mission goals and future assessment/reporting tasks |

`area_designated`, `direct_identity_evidence_available` and `capability_available` are upstream inputs produced respectively by scenario/mission initialization, an external or prior information source, and execution-state synchronization.

For Movement, continuous tasks (`Patrol`, `Maintain`, `Follow`, `Shadow`) expose an active spatial relation and end only through explicit termination conditions. Durative tasks (`Navigate`, `Approach`, `Withdraw`, `Transit`, `Evade`) complete on an observable location or geometry condition. Target-relative movement consumes knowledge owned by the acting platform; it never turns an estimated target location into physical truth.

For Protection, `Screen` and `Defend` are abstract continuous tasks: they declare the protection results expected from their decomposition but write no direct world effect. `Guard` and `Interpose` expose active physical relations, while screen integrity, interposition geometry and area-protection success are evaluated as derived world states. `Deploy Decoy` performs a physical custody-to-deployment transition; the resulting protective effect remains separately evaluated and cannot be asserted merely because the decoy was released.

## 4. Machine-readable schema

```yaml
id: TC-003
verb: Search
status: candidate
version: 0.11.0

signatures:
  - signature_id: TC-003-S01
    semantic_family: SF-01
    legacy_name: Search Area
    actor_description: mobile platform
    typed_complement: Area
    capability_type: CT-02
    implements_capabilities:
      - DetectionCapability
  - signature_id: TC-003-S02
    semantic_family: SF-04
    legacy_name: Search Vessel
    actor_description: boarding/inspection force
    typed_complement: Vessel
    capability_type: CT-05
    implements_capabilities:
      - InterdictionCapability
      - InspectionCapability

traceability:
  used_by_missions: []
  legacy_task_ids:
    - TCL-004
    - TCL-039
```

## 5. Canonical Task inventory

Capability Types shown per verb are the union over its signatures.

| ID | Verb | Capability Types | Legacy signatures | Status |
|---|---|---|---|---|

| TC-001 | `Navigate` | CT-01 | Navigate to Location; Navigate Route | `draft` |
| TC-002 | `Patrol` | CT-01 | Patrol Area | `draft` |
| TC-003 | `Search` | CT-02, CT-05 | Search Area; Search Vessel | `candidate` |
| TC-004 | `Survey` | CT-02 | Survey Area | `candidate` |
| TC-005 | `Maintain` | CT-01, CT-03, CT-09 | Maintain Station; Maintain Formation; Maintain Operational Picture; Maintain Communication Link | `draft` |
| TC-006 | `Follow` | CT-01 | Follow Designated Unit | `candidate` |
| TC-007 | `Shadow` | CT-01 | Shadow Designated Unit | `candidate` |
| TC-008 | `Approach` | CT-01 | Approach Object | `candidate` |
| TC-009 | `Withdraw` | CT-01 | Withdraw from Area | `candidate` |
| TC-010 | `Transit` | CT-01 | Transit Corridor | `candidate` |
| TC-011 | `Observe` | CT-02 | Observe Area | `candidate` |
| TC-012 | `Detect` | CT-02 | Detect Object; Detect Emission | `draft` |
| TC-013 | `Localize` | CT-02 | Localize Object | `candidate` |
| TC-014 | `Classify` | CT-02 | Classify Object | `draft` |
| TC-015 | `Identify` | CT-02 | Identify Object | `draft` |
| TC-016 | `Track` | CT-02 | Track Object | `draft` |
| TC-017 | `Characterize` | CT-02, CT-11 | Characterize Object; Characterize Emission | `candidate` |
| TC-018 | `Inspect` | CT-02 | Inspect Object; Inspect Infrastructure | `candidate` |
| TC-019 | `Map` | CT-02 | Map Seabed | `candidate` |
| TC-020 | `Measure` | CT-02 | Measure Environment | `candidate` |
| TC-021 | `Assess` | CT-03 | Assess Threat | `draft` |
| TC-022 | `Correlate` | CT-03 | Correlate Observations | `candidate` |
| TC-023 | `Escort` | CT-04 | Escort Unit | `draft` |
| TC-024 | `Screen` | CT-04 | Screen Protected Force | `candidate` |
| TC-025 | `Guard` | CT-04 | Guard Object | `candidate` |
| TC-026 | `Block` | CT-01 | Block Approach | `candidate` |
| TC-027 | `Interpose` | CT-01 | Interpose | `candidate` |
| TC-028 | `Defend` | CT-04 | Defend Area | `candidate` |
| TC-029 | `Evade` | CT-01 | Evade Threat | `candidate` |
| TC-030 | `Intercept` | CT-05 | Intercept Platform | `draft` |
| TC-031 | `Hail` | CT-05 | Hail Vessel | `candidate` |
| TC-032 | `Direct` | CT-05 | Direct Vessel | `candidate` |
| TC-033 | `Compel` | CT-05 | Compel Course Change | `candidate` |
| TC-034 | `Board` | CT-05 | Board Vessel | `candidate` |
| TC-035 | `Seize` | CT-05 | Seize Object | `candidate` |
| TC-036 | `Engage` | CT-05 | Engage Threat | `candidate` |
| TC-037 | `Neutralize` | CT-05 | Neutralize Threat; Neutralize Mine | `candidate` |
| TC-038 | `Deploy` | CT-07 | Deploy Mine; Deploy Decoy; Deploy Payload | `candidate` |
| TC-039 | `Report` | CT-09 | Report Information | `draft` |
| TC-040 | `Share` | CT-09 | Share Track | `candidate` |
| TC-041 | `Request` | CT-10 | Request Support | `candidate` |
| TC-042 | `Assign` | CT-10 | Assign Task | `candidate` |
| TC-043 | `Coordinate` | CT-10 | Coordinate Action | `candidate` |
| TC-044 | `Relay` | CT-09 | Relay Communications | `candidate` |
| TC-045 | `Establish` | CT-09 | Establish Communication Link | `candidate` |
| TC-046 | `Transmit` | CT-09 | Transmit Command | `candidate` |
| TC-047 | `Update` | CT-10 | Update Mission Plan | `candidate` |
| TC-048 | `Launch` | CT-07 | Launch Platform | `candidate` |
| TC-049 | `Recover` | CT-06 | Recover Platform; Recover Payload; Recover Personnel | `candidate` |
| TC-050 | `Dock` | CT-07 | Dock Platform | `candidate` |
| TC-051 | `Transport` | CT-08 | Transport Payload | `candidate` |
| TC-052 | `Transfer` | CT-08 | Transfer Materiel | `candidate` |
| TC-053 | `Resupply` | CT-08 | Resupply Platform | `candidate` |
| TC-054 | `Recharge` | CT-08 | Recharge Platform | `candidate` |
| TC-055 | `Refuel` | CT-08 | Refuel Platform | `candidate` |
| TC-056 | `Tow` | CT-08 | Tow Platform | `candidate` |
| TC-057 | `Locate` | CT-02, CT-11 | Locate Missing Entity; Locate Emitter | `candidate` |
| TC-058 | `Mark` | CT-06 | Mark Location | `candidate` |
| TC-059 | `Assist` | CT-06 | Assist Distressed Platform | `candidate` |
| TC-060 | `Stabilize` | CT-06 | Stabilize Casualty | `candidate` |
| TC-061 | `Evacuate` | CT-06 | Evacuate Casualty | `candidate` |
| TC-062 | `Monitor` | CT-11 | Monitor Spectrum | `candidate` |
| TC-063 | `Jam` | CT-11 | Jam Communication; Jam Sensor | `candidate` |
| TC-064 | `Emit` | CT-11 | Emit Deceptive Signal | `candidate` |

## 6. Typed signatures

### TC-001 — Navigate

```yaml
id: TC-001
verb: Navigate
status: draft
version: 0.8.1
signatures:
- signature_id: TC-001-S01
  semantic_family: SF-02
  legacy_name: Navigate to Location
  actor_description: mobile platform
  typed_complement: to Location
  capability_type: CT-01
  implements_capabilities:
  - WaypointNavigationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: destination
      type: nmo:SpatialRegion
      source: task_input
    - role: origin
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-001
        bindings: {entity: actor, location: origin}
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: WaypointNavigationCapability}
    - state_ref: SM-ST-003
      bindings: {entity: actor, destination: destination}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: origin}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: WaypointNavigationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-003
        bindings: {entity: actor, destination: destination}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: WaypointNavigationCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: destination}
        remove:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: origin}
      knowledge:
        add: []
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: destination}
    termination_conditions: []
    failure_outcomes:
    - outcome: destination_unreachable
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: destination}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: WaypointNavigationCapability}
    execution:
      responsibility: platform_autonomy

- signature_id: TC-001-S02
  semantic_family: SF-02
  legacy_name: Navigate Route
  actor_description: mobile platform
  typed_complement: Route
  capability_type: CT-01
  implements_capabilities:
  - RouteFollowingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: route
      type: nmo:Route
      source: task_input
    - role: destination
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-002
        bindings: {route: route, location: destination}
    - role: origin
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-001
        bindings: {entity: actor, location: origin}
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: RouteFollowingCapability}
    - state_ref: SM-ST-004
      bindings: {route: route, entity: actor}
    - state_ref: SM-ST-002
      bindings: {route: route, location: destination}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: origin}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: RouteFollowingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-004
        bindings: {route: route, entity: actor}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: RouteFollowingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: destination}
        remove:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: origin}
      knowledge:
        add: []
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-012
      bindings: {entity: actor, route: route}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: destination}
    termination_conditions: []
    failure_outcomes:
    - outcome: route_blocked
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: route}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: RouteFollowingCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-016
  - MC-019
  - MC-026
  - MC-027
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-036
  - MC-040
  - MC-042
  - MC-043
  - MC-044
  - MC-045
  - MC-046
  - MC-047
  - MC-048
  - MC-049
  - MC-052
  - MC-059
  - MC-060
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-001
  - TCL-002
```

### TC-002 — Patrol

```yaml
id: TC-002
verb: Patrol
status: draft
version: 0.9.0
signatures:
- signature_id: TC-002-S01
  semantic_family: SF-02
  legacy_name: Patrol Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
  - PerceptionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: area, type: nmo:SpatialRegion, source: task_input}
    reads:
    - state_ref: SM-ST-009
      bindings: {area: area}
    - state_ref: SM-ST-003
      bindings: {entity: actor, destination: area}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-009
        bindings: {area: area}
      - state_ref: SM-ST-003
        bindings: {entity: actor, destination: area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: MobilityCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: PerceptionCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-039
          bindings: {actor: actor, area: area}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - {condition: parent_task_requests_stop, bindings: {actor: actor, area: area}}
    - {condition: patrol_window_elapsed, bindings: {actor: actor, area: area}}
    - {condition: patrol_objective_satisfied, bindings: {actor: actor, area: area}}
    - {condition: parent_mission_terminated, bindings: {actor: actor, area: area}}
    failure_outcomes:
    - outcome: patrol_area_unreachable
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: area}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: MobilityCapability}
    - outcome: perception_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: PerceptionCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-001
  - MC-017
  - MC-020
  - MC-021
  - MC-022
  - MC-024
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-036
  - MC-040
  - MC-046
  legacy_task_ids:
  - TCL-003
```

### TC-003 — Search

```yaml
id: TC-003
verb: Search
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-003-S01
  semantic_family: SF-01
  legacy_name: Search Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
  semantics:
    semantic_kind: abstract
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: area, type: nmo:SpatialRegion, source: task_input}
    - {role: search_requirement, type: SM-TY-014, source: task_input}
    reads:
    - state_ref: SM-ST-068
      bindings: {area: area, requirement: search_requirement}
    - state_ref: SM-ST-009
      bindings: {area: area}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    invariants:
    - state_ref: SM-ST-068
      bindings: {area: area, requirement: search_requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-068
        bindings: {area: area, requirement: search_requirement}
      - state_ref: SM-ST-009
        bindings: {area: area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: DetectionCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes:
    - state_ref: SM-ST-069
      bindings: {holder: knowledge_holder, area: area, requirement: search_requirement}
    completion_conditions:
    - state_ref: SM-ST-069
      bindings: {holder: knowledge_holder, area: area, requirement: search_requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: search_requirement_not_met
      establishes:
      - state_ref: SM-ST-070
        bindings: {holder: knowledge_holder, actor: actor, area: area, requirement: search_requirement}
    - outcome: detection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: DetectionCapability}
    execution: {responsibility: level_1_planner}
- signature_id: TC-003-S02
  semantic_family: SF-04
  legacy_name: Search Vessel
  actor_description: boarding/inspection force
  typed_complement: Vessel
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - InspectionCapability
traceability:
  used_by_missions:
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-029
  - MC-030
  - MC-042
  - MC-060
  - MC-062
  - MC-063
  legacy_task_ids:
  - TCL-004
  - TCL-039
```

### TC-004 — Survey

```yaml
id: TC-004
verb: Survey
status: candidate
version: 0.11.0
signatures:
- signature_id: TC-004-S01
  semantic_family: SF-01
  legacy_name: Survey Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - SurveyCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: area, type: nmo:SpatialRegion, source: task_input}
    - {role: coverage_requirement, type: SM-TY-015, source: task_input}
    - role: survey
      type: SM-TY-016
      source: {kind: execution_output, produced_by: survey_record}
    reads:
    - state_ref: SM-ST-071
      bindings: {area: area, requirement: coverage_requirement}
    - state_ref: SM-ST-009
      bindings: {area: area}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SurveyCapability}
    invariants:
    - state_ref: SM-ST-071
      bindings: {area: area, requirement: coverage_requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SurveyCapability}
    applicability:
      operational:
      - state_ref: SM-ST-071
        bindings: {area: area, requirement: coverage_requirement}
      - state_ref: SM-ST-009
        bindings: {area: area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: SurveyCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-074
          bindings: {holder: knowledge_holder, survey: survey}
        - state_ref: SM-ST-075
          bindings: {holder: knowledge_holder, survey: survey, area: area}
        - state_ref: SM-ST-076
          bindings: {holder: knowledge_holder, survey: survey, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes:
    - state_ref: SM-ST-072
      bindings: {holder: knowledge_holder, area: area, requirement: coverage_requirement}
    completion_conditions:
    - state_ref: SM-ST-074
      bindings: {holder: knowledge_holder, survey: survey}
    - state_ref: SM-ST-072
      bindings: {holder: knowledge_holder, area: area, requirement: coverage_requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: coverage_requirement_not_met
      establishes:
      - state_ref: SM-ST-073
        bindings: {holder: knowledge_holder, actor: actor, area: area, requirement: coverage_requirement}
    - outcome: survey_quality_insufficient
      establishes:
      - state_ref: SM-ST-077
        bindings: {holder: knowledge_holder, actor: actor, area: area}
    - outcome: survey_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: SurveyCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-003
  - MC-005
  - MC-006
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-012
  - MC-013
  - MC-015
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-042
  - MC-043
  - MC-046
  legacy_task_ids:
  - TCL-005
```

### TC-005 — Maintain

```yaml
id: TC-005
verb: Maintain
status: draft
version: 0.9.0
signatures:
- signature_id: TC-005-S01
  semantic_family: SF-02
  legacy_name: Maintain Station
  actor_description: mobile platform
  typed_complement: Station
  capability_type: CT-01
  implements_capabilities:
  - StationKeepingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: station, type: nmo:SpatialRegion, source: task_input}
    reads:
    - state_ref: SM-ST-040
      bindings: {actor: actor, station: station}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: station}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: StationKeepingCapability}
    invariants:
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: station}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: StationKeepingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-040
        bindings: {actor: actor, station: station}
      - state_ref: SM-ST-001
        bindings: {entity: actor, location: station}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: StationKeepingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-041
          bindings: {actor: actor, station: station}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - {condition: station_keeping_relief_received, bindings: {actor: actor, station: station}}
    - {condition: station_keeping_window_elapsed, bindings: {actor: actor, station: station}}
    - {condition: parent_mission_terminated, bindings: {actor: actor, station: station}}
    failure_outcomes:
    - outcome: station_departed_outside_tolerance
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: station}
    - outcome: station_keeping_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: StationKeepingCapability}
    execution: {responsibility: platform_autonomy}
- signature_id: TC-005-S02
  semantic_family: SF-02
  legacy_name: Maintain Formation
  actor_description: platform/group
  typed_complement: Formation
  capability_type: CT-01
  implements_capabilities:
  - StationKeepingCapability
  - CoordinationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: formation, type: SM-TY-011, source: task_input}
    reads:
    - state_ref: SM-ST-042
      bindings: {actor: actor, formation: formation}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: StationKeepingCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: CoordinationCapability}
    invariants:
    - state_ref: SM-ST-042
      bindings: {actor: actor, formation: formation}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: StationKeepingCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: CoordinationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-042
        bindings: {actor: actor, formation: formation}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: StationKeepingCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: CoordinationCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-043
          bindings: {actor: actor, formation: formation}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - {condition: formation_change_order_received, bindings: {actor: actor, formation: formation}}
    - {condition: actor_relieved_from_formation, bindings: {actor: actor, formation: formation}}
    - {condition: parent_mission_terminated, bindings: {actor: actor, formation: formation}}
    failure_outcomes:
    - outcome: formation_broken
      establishes:
      - state_ref: SM-ST-044
        bindings: {actor: actor, formation: formation}
    - outcome: station_keeping_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: StationKeepingCapability}
    - outcome: coordination_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: CoordinationCapability}
    execution: {responsibility: platform_autonomy}
- signature_id: TC-005-S03
  semantic_family: SF-06
  legacy_name: Maintain Operational Picture
  actor_description: command/processing actor
  typed_complement: Operational Picture
  capability_type: CT-03
  implements_capabilities:
  - AssessmentCapability
  - DataProcessingCapability
- signature_id: TC-005-S04
  semantic_family: SF-06
  legacy_name: Maintain Communication Link
  actor_description: communicating actors
  typed_complement: Communication Link
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-006
  - MC-007
  - MC-009
  - MC-013
  - MC-016
  - MC-017
  - MC-018
  - MC-021
  - MC-026
  - MC-027
  - MC-028
  - MC-031
  - MC-032
  - MC-033
  - MC-050
  - MC-056
  legacy_task_ids:
  - TCL-006
  - TCL-007
  - TCL-026
  - TCL-053
```

### TC-006 — Follow

```yaml
id: TC-006
verb: Follow
status: draft
version: 0.8.1
signatures:
- signature_id: TC-006-S01
  semantic_family: SF-02
  legacy_name: Follow Designated Unit
  actor_description: mobile platform
  typed_complement: Designated Unit
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: followed_unit
      type: nmo:PhysicalEntity
      source: task_input
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: followed_unit}
    invariants:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: followed_unit}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-027
        bindings: {holder: actor, target: followed_unit}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: TargetFollowingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-005
          bindings: {follower: actor, target: followed_unit}
        remove: []
      knowledge:
        add: []
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - condition: parent_task_requests_stop
      bindings: {follower: actor, target: followed_unit}
    - condition: follow_assigned_destination_reached
      bindings: {follower: actor, target: followed_unit}
    - condition: threat_requires_task_transition
      bindings: {follower: actor, target: followed_unit}
    - condition: parent_mission_terminated
      bindings: {follower: actor, target: followed_unit}
    failure_outcomes:
    - outcome: target_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: actor, target: followed_unit}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: TargetFollowingCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-019
  - MC-023
  - MC-026
  - MC-027
  - MC-028
  - MC-033
  legacy_task_ids:
  - TCL-008
```

### TC-007 — Shadow

```yaml
id: TC-007
verb: Shadow
status: candidate
version: 0.9.0
signatures:
- signature_id: TC-007-S01
  semantic_family: SF-02
  legacy_name: Shadow Designated Unit
  actor_description: mobile platform
  typed_complement: Designated Unit
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
  - TrackingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: target, type: nmo:PhysicalEntity, source: task_input}
    - role: track
      type: SM-TY-009
      source:
        kind: state_at_start
        state_ref: SM-ST-036
        bindings: {holder: actor, target: target, track: track}
    reads:
    - state_ref: SM-ST-036
      bindings: {holder: actor, target: target, track: track}
    - state_ref: SM-ST-037
      bindings: {holder: actor, track: track}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TrackingCapability}
    invariants:
    - state_ref: SM-ST-037
      bindings: {holder: actor, track: track}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TrackingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-036
        bindings: {holder: actor, target: target, track: track}
      - state_ref: SM-ST-037
        bindings: {holder: actor, track: track}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: TargetFollowingCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: TrackingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-045
          bindings: {actor: actor, target: target}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - {condition: parent_task_requests_stop, bindings: {actor: actor, target: target}}
    - {condition: shadowing_handover_completed, bindings: {actor: actor, target: target}}
    - {condition: posture_transition_required, bindings: {actor: actor, target: target}}
    - {condition: parent_mission_terminated, bindings: {actor: actor, target: target}}
    failure_outcomes:
    - outcome: target_track_lost
      establishes:
      - state_ref: SM-ST-038
        bindings: {holder: actor, target: target, track: track}
    - outcome: following_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: TargetFollowingCapability}
    - outcome: tracking_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: TrackingCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-019
  - MC-024
  - MC-025
  - MC-034
  legacy_task_ids:
  - TCL-009
```

### TC-008 — Approach

```yaml
id: TC-008
verb: Approach
status: candidate
version: 0.9.0
signatures:
- signature_id: TC-008-S01
  semantic_family: SF-02
  legacy_name: Approach Object
  actor_description: mobile platform
  typed_complement: Object
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: target, type: nmo:PhysicalEntity, source: task_input}
    reads:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    invariants:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    applicability:
      operational:
      - state_ref: SM-ST-027
        bindings: {holder: actor, target: target}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: MobilityCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-046
          bindings: {actor: actor, target: target}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-047
      bindings: {actor: actor, target: target}
    termination_conditions: []
    failure_outcomes:
    - outcome: target_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: actor, target: target}
    - outcome: approach_navigation_failed
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: target}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: MobilityCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-019
  - MC-023
  - MC-053
  - MC-061
  - MC-064
  legacy_task_ids:
  - TCL-010
```

### TC-009 — Withdraw

```yaml
id: TC-009
verb: Withdraw
status: candidate
version: 0.9.0
signatures:
- signature_id: TC-009-S01
  semantic_family: SF-02
  legacy_name: Withdraw from Area
  actor_description: mobile platform
  typed_complement: from Area
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: area, type: nmo:SpatialRegion, source: task_input}
    - {role: destination, type: nmo:SpatialRegion, source: task_input}
    - role: origin
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-001
        bindings: {entity: actor, location: origin}
    reads:
    - state_ref: SM-ST-048
      bindings: {actor: actor, area: area}
    - state_ref: SM-ST-003
      bindings: {entity: actor, destination: destination}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: origin}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    applicability:
      operational:
      - state_ref: SM-ST-048
        bindings: {actor: actor, area: area}
      - state_ref: SM-ST-003
        bindings: {entity: actor, destination: destination}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: MobilityCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: destination}
        remove:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: origin}
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-049
      bindings: {actor: actor, area: area}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: destination}
    termination_conditions: []
    failure_outcomes:
    - outcome: withdrawal_destination_unreachable
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: destination}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: MobilityCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions: []
  legacy_task_ids:
  - TCL-011
```

### TC-010 — Transit

```yaml
id: TC-010
verb: Transit
status: candidate
version: 0.9.0
signatures:
- signature_id: TC-010-S01
  semantic_family: SF-02
  legacy_name: Transit Corridor
  actor_description: mobile platform
  typed_complement: Corridor
  capability_type: CT-01
  implements_capabilities:
  - RouteFollowingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: corridor, type: nmo:Corridor, source: task_input}
    - role: destination
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-050
        bindings: {corridor: corridor, location: destination}
    - role: origin
      type: nmo:SpatialRegion
      source:
        kind: state_at_start
        state_ref: SM-ST-001
        bindings: {entity: actor, location: origin}
    reads:
    - state_ref: SM-ST-050
      bindings: {corridor: corridor, location: destination}
    - state_ref: SM-ST-051
      bindings: {corridor: corridor, entity: actor}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: origin}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: RouteFollowingCapability}
    invariants:
    - state_ref: SM-ST-051
      bindings: {corridor: corridor, entity: actor}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: RouteFollowingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-051
        bindings: {corridor: corridor, entity: actor}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: RouteFollowingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: destination}
        remove:
        - state_ref: SM-ST-001
          bindings: {entity: actor, location: origin}
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-052
      bindings: {entity: actor, corridor: corridor}
    - state_ref: SM-ST-001
      bindings: {entity: actor, location: destination}
    termination_conditions: []
    failure_outcomes:
    - outcome: corridor_transit_failed
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: corridor}
    - outcome: route_following_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: RouteFollowingCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-004
  - MC-008
  - MC-012
  - MC-015
  - MC-032
  legacy_task_ids:
  - TCL-012
```

### TC-011 — Observe

```yaml
id: TC-011
verb: Observe
status: candidate
version: 0.8.1
signatures:
- signature_id: TC-011-S01
  semantic_family: SF-01
  legacy_name: Observe Area
  actor_description: sensing platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: area
      type: nmo:SpatialRegion
      source: task_input
    - role: observation
      type: SM-TY-002
      source:
        kind: execution_output
        produced_by: observation
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    - state_ref: SM-ST-009
      bindings: {area: area}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-009
        bindings: {area: area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: PerceptionCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-016
          bindings: {holder: knowledge_holder, observation: observation}
        - state_ref: SM-ST-017
          bindings: {holder: knowledge_holder, observation: observation, area: area}
        - state_ref: SM-ST-018
          bindings: {holder: knowledge_holder, observation: observation, actor: actor}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-016
      bindings: {holder: knowledge_holder, observation: observation}
    termination_conditions: []
    failure_outcomes:
    - outcome: sensor_unavailable
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: PerceptionCapability}
    - outcome: observation_quality_insufficient
      establishes:
      - state_ref: SM-ST-019
        bindings: {holder: knowledge_holder, actor: actor, area: area}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-017
  - MC-018
  - MC-020
  - MC-021
  - MC-022
  - MC-024
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-042
  - MC-043
  - MC-054
  - MC-060
  - MC-063
  legacy_task_ids:
  - TCL-013
```

### TC-012 — Detect

```yaml
id: TC-012
verb: Detect
status: draft
version: 0.8.1
signatures:
- signature_id: TC-012-S01
  semantic_family: SF-01
  legacy_name: Detect Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: target
      type: nmo:PhysicalEntity
      source: task_input
    - role: evidence
      type: SM-TY-003
      source:
        kind: execution_output
        produced_by: detection
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    applicability:
      operational: []
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: DetectionCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-020
          bindings: {holder: knowledge_holder, target: target}
        - state_ref: SM-ST-021
          bindings: {holder: knowledge_holder, target: target, evidence: evidence}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    termination_conditions: []
    failure_outcomes:
    - outcome: detection_threshold_not_met
      establishes:
      - state_ref: SM-ST-022
        bindings: {holder: knowledge_holder, actor: actor, target: target}
    - outcome: sensor_unavailable
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: DetectionCapability}
    execution:
      responsibility: platform_autonomy
- signature_id: TC-012-S02
  semantic_family: SF-01
  legacy_name: Detect Emission
  actor_description: sensing platform
  typed_complement: Emission
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
  - ElectronicWarfareCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: emission
      type: SM-TY-004
      source: task_input
    - role: evidence
      type: SM-TY-005
      source:
        kind: execution_output
        produced_by: emission_detection
    reads:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ElectronicWarfareCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: DetectionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ElectronicWarfareCapability}
    applicability:
      operational: []
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: DetectionCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: ElectronicWarfareCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-023
          bindings: {holder: knowledge_holder, emission: emission}
        - state_ref: SM-ST-024
          bindings: {holder: knowledge_holder, emission: emission, evidence: evidence}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-023
      bindings: {holder: knowledge_holder, emission: emission}
    termination_conditions: []
    failure_outcomes:
    - outcome: detection_threshold_not_met
      establishes:
      - state_ref: SM-ST-025
        bindings: {holder: knowledge_holder, actor: actor, emission: emission}
    - outcome: sensor_unavailable
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: ElectronicWarfareCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-008
  - MC-010
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-017
  - MC-018
  - MC-020
  - MC-021
  - MC-022
  - MC-024
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-036
  - MC-038
  - MC-039
  - MC-040
  - MC-042
  - MC-043
  - MC-046
  - MC-054
  - MC-055
  - MC-056
  - MC-057
  - MC-060
  - MC-062
  - MC-063
  legacy_task_ids:
  - TCL-014
  - TCL-073
```

### TC-013 — Localize

```yaml
id: TC-013
verb: Localize
status: candidate
version: 0.8.1
signatures:
- signature_id: TC-013-S01
  semantic_family: SF-01
  legacy_name: Localize Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: target
      type: nmo:PhysicalEntity
      source: task_input
    - role: estimate
      type: SM-TY-006
      source:
        kind: execution_output
        produced_by: localization
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: target}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: PerceptionCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-026
          bindings: {holder: knowledge_holder, target: target, estimate: estimate}
        - state_ref: SM-ST-027
          bindings: {holder: knowledge_holder, target: target}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-026
      bindings: {holder: knowledge_holder, target: target, estimate: estimate}
    termination_conditions: []
    failure_outcomes:
    - outcome: localization_quality_insufficient
      establishes:
      - state_ref: SM-ST-029
        bindings: {holder: knowledge_holder, actor: actor, target: target}
    - outcome: sensor_or_processing_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: PerceptionCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-003
  - MC-010
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-029
  - MC-030
  - MC-036
  - MC-042
  - MC-054
  - MC-060
  - MC-062
  - MC-063
  legacy_task_ids:
  - TCL-015
```

### TC-014 — Classify

```yaml
id: TC-014
verb: Classify
status: draft
version: 0.8.1
signatures:
- signature_id: TC-014-S01
  semantic_family: SF-01
  legacy_name: Classify Object
  actor_description: sensing/processing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - ClassificationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: target
      type: nmo:PhysicalEntity
      source: task_input
    - role: classification
      type: SM-TY-007
      source:
        kind: execution_output
        produced_by: classification
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: target}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: ClassificationCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-030
          bindings: {holder: knowledge_holder, target: target, classification: classification}
        - state_ref: SM-ST-031
          bindings: {holder: knowledge_holder, target: target}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-030
      bindings: {holder: knowledge_holder, target: target, classification: classification}
    termination_conditions: []
    failure_outcomes:
    - outcome: classification_quality_insufficient
      establishes:
      - state_ref: SM-ST-032
        bindings: {holder: knowledge_holder, actor: actor, target: target}
    - outcome: processing_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: ClassificationCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-010
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-017
  - MC-018
  - MC-020
  - MC-021
  - MC-022
  - MC-024
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-036
  - MC-038
  - MC-042
  - MC-054
  legacy_task_ids:
  - TCL-016
```

### TC-015 — Identify

```yaml
id: TC-015
verb: Identify
status: draft
version: 0.8.1
signatures:
- signature_id: TC-015-S01
  semantic_family: SF-01
  legacy_name: Identify Object
  actor_description: sensing/processing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - IdentificationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: target
      type: nmo:PhysicalEntity
      source: task_input
    - role: identity
      type: SM-TY-008
      source:
        kind: execution_output
        produced_by: identification
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: IdentificationCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: IdentificationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: target}
      - any_of:
        - state_ref: SM-ST-031
          bindings: {holder: knowledge_holder, target: target}
        - state_ref: SM-ST-033
          bindings: {holder: knowledge_holder, target: target}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: IdentificationCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-034
          bindings: {holder: knowledge_holder, target: target, identity: identity}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-034
      bindings: {holder: knowledge_holder, target: target, identity: identity}
    termination_conditions: []
    failure_outcomes:
    - outcome: identity_evidence_insufficient
      establishes:
      - state_ref: SM-ST-035
        bindings: {holder: knowledge_holder, actor: actor, target: target}
    - outcome: processing_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: IdentificationCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-017
  - MC-018
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-024
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-035
  - MC-037
  - MC-038
  - MC-039
  - MC-041
  - MC-042
  - MC-054
  - MC-055
  - MC-057
  - MC-060
  - MC-062
  - MC-063
  legacy_task_ids:
  - TCL-017
```

### TC-016 — Track

```yaml
id: TC-016
verb: Track
status: draft
version: 0.8.1
signatures:
- signature_id: TC-016-S01
  semantic_family: SF-01
  legacy_name: Track Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - TrackingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - role: actor
      type: nmo:Platform
      source: task_input
    - role: knowledge_holder
      type: SM-TY-001
      source: task_input
    - role: target
      type: nmo:PhysicalEntity
      source: task_input
    - role: track
      type: SM-TY-009
      source:
        kind: execution_output
        produced_by: tracking
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TrackingCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TrackingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: target}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: TrackingCapability}
    operational_effects:
      world:
        add: []
        remove: []
      knowledge:
        add:
        - state_ref: SM-ST-036
          bindings: {holder: knowledge_holder, target: target, track: track}
        - state_ref: SM-ST-037
          bindings: {holder: knowledge_holder, track: track}
        remove: []
      resources:
        add: []
        remove: []
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - condition: parent_task_requests_stop
      bindings: {holder: knowledge_holder, target: target, track: track}
    - condition: surveillance_window_closed
      bindings: {holder: knowledge_holder, target: target, track: track}
    - condition: parent_mission_terminated
      bindings: {holder: knowledge_holder, target: target, track: track}
    failure_outcomes:
    - outcome: target_lost
      establishes:
      - state_ref: SM-ST-038
        bindings: {holder: knowledge_holder, target: target, track: track}
    - outcome: tracking_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: TrackingCapability}
    execution:
      responsibility: platform_autonomy
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-005
  - MC-017
  - MC-018
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-035
  - MC-036
  - MC-037
  - MC-038
  - MC-039
  - MC-040
  - MC-046
  - MC-053
  - MC-054
  - MC-055
  - MC-057
  - MC-060
  - MC-062
  - MC-063
  legacy_task_ids:
  - TCL-018
```

### TC-017 — Characterize

```yaml
id: TC-017
verb: Characterize
status: draft
version: 0.12.0
signatures:
- signature_id: TC-017-S01
  semantic_family: SF-01
  legacy_name: Characterize Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - ClassificationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: target, type: nmo:PhysicalEntity, source: task_input}
    - {role: requirement, type: SM-TY-019, source: task_input}
    - role: characterization
      type: SM-TY-020
      source: {kind: execution_output, produced_by: object_characterization}
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: target}
    - state_ref: SM-ST-087
      bindings: {target: target, requirement: requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: target}
      - state_ref: SM-ST-087
        bindings: {target: target, requirement: requirement}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: ClassificationCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-088
          bindings: {holder: knowledge_holder, characterization: characterization}
        - state_ref: SM-ST-089
          bindings: {holder: knowledge_holder, characterization: characterization, target: target}
        - state_ref: SM-ST-090
          bindings: {holder: knowledge_holder, characterization: characterization, requirement: requirement}
        - state_ref: SM-ST-091
          bindings: {holder: knowledge_holder, characterization: characterization, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-090
      bindings: {holder: knowledge_holder, characterization: characterization, requirement: requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: characterization_quality_insufficient
      establishes:
      - state_ref: SM-ST-092
        bindings: {holder: knowledge_holder, actor: actor, target: target, requirement: requirement}
    - outcome: characterization_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: ClassificationCapability}
    execution: {responsibility: platform_autonomy}
- signature_id: TC-017-S02
  semantic_family: SF-01
  legacy_name: Characterize Emission
  actor_description: sensing/processing actor
  typed_complement: Emission
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
  - ClassificationCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: emission, type: SM-TY-004, source: task_input}
    - {role: requirement, type: SM-TY-019, source: task_input}
    - role: characterization
      type: SM-TY-021
      source: {kind: execution_output, produced_by: emission_characterization}
    reads:
    - state_ref: SM-ST-023
      bindings: {holder: knowledge_holder, emission: emission}
    - state_ref: SM-ST-093
      bindings: {emission: emission, requirement: requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ElectronicWarfareCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ElectronicWarfareCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: ClassificationCapability}
    applicability:
      operational:
      - state_ref: SM-ST-023
        bindings: {holder: knowledge_holder, emission: emission}
      - state_ref: SM-ST-093
        bindings: {emission: emission, requirement: requirement}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: ElectronicWarfareCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: ClassificationCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-094
          bindings: {holder: knowledge_holder, characterization: characterization}
        - state_ref: SM-ST-095
          bindings: {holder: knowledge_holder, characterization: characterization, emission: emission}
        - state_ref: SM-ST-096
          bindings: {holder: knowledge_holder, characterization: characterization, requirement: requirement}
        - state_ref: SM-ST-097
          bindings: {holder: knowledge_holder, characterization: characterization, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-096
      bindings: {holder: knowledge_holder, characterization: characterization, requirement: requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: characterization_quality_insufficient
      establishes:
      - state_ref: SM-ST-098
        bindings: {holder: knowledge_holder, actor: actor, emission: emission, requirement: requirement}
    - outcome: electronic_warfare_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: ElectronicWarfareCapability}
    - outcome: classification_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: ClassificationCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-011
  - MC-012
  - MC-013
  - MC-015
  - MC-017
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-054
  legacy_task_ids:
  - TCL-019
  - TCL-074
```

### TC-018 — Inspect

```yaml
id: TC-018
verb: Inspect
status: draft
version: 0.12.0
signatures:
- signature_id: TC-018-S01
  semantic_family: SF-01
  legacy_name: Inspect Object
  actor_description: inspection platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - InspectionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: subject, type: nmo:PhysicalEntity, source: task_input}
    - {role: requirement, type: SM-TY-022, source: task_input}
    - role: inspection
      type: SM-TY-023
      source: {kind: execution_output, produced_by: inspection_record}
    reads:
    - state_ref: SM-ST-020
      bindings: {holder: knowledge_holder, target: subject}
    - state_ref: SM-ST-099
      bindings: {subject: subject, requirement: requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: InspectionCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: InspectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-020
        bindings: {holder: knowledge_holder, target: subject}
      - state_ref: SM-ST-099
        bindings: {subject: subject, requirement: requirement}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: InspectionCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-100
          bindings: {holder: knowledge_holder, inspection: inspection}
        - state_ref: SM-ST-101
          bindings: {holder: knowledge_holder, inspection: inspection, subject: subject}
        - state_ref: SM-ST-102
          bindings: {holder: knowledge_holder, inspection: inspection, requirement: requirement}
        - state_ref: SM-ST-103
          bindings: {holder: knowledge_holder, inspection: inspection, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-102
      bindings: {holder: knowledge_holder, inspection: inspection, requirement: requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: inspection_quality_insufficient
      establishes:
      - state_ref: SM-ST-104
        bindings: {holder: knowledge_holder, actor: actor, subject: subject, requirement: requirement}
    - outcome: inspection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: InspectionCapability}
    execution: {responsibility: platform_autonomy}
- signature_id: TC-018-S02
  semantic_family: SF-01
  legacy_name: Inspect Infrastructure
  actor_description: inspection platform
  typed_complement: Infrastructure
  capability_type: CT-02
  implements_capabilities:
  - InspectionCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: subject, type: nmo:Infrastructure, source: task_input}
    - {role: requirement, type: SM-TY-022, source: task_input}
    - role: inspection
      type: SM-TY-023
      source: {kind: execution_output, produced_by: inspection_record}
    reads:
    - state_ref: SM-ST-099
      bindings: {subject: subject, requirement: requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: InspectionCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: InspectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-099
        bindings: {subject: subject, requirement: requirement}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: InspectionCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-100
          bindings: {holder: knowledge_holder, inspection: inspection}
        - state_ref: SM-ST-101
          bindings: {holder: knowledge_holder, inspection: inspection, subject: subject}
        - state_ref: SM-ST-102
          bindings: {holder: knowledge_holder, inspection: inspection, requirement: requirement}
        - state_ref: SM-ST-103
          bindings: {holder: knowledge_holder, inspection: inspection, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-102
      bindings: {holder: knowledge_holder, inspection: inspection, requirement: requirement}
    termination_conditions: []
    failure_outcomes:
    - outcome: inspection_quality_insufficient
      establishes:
      - state_ref: SM-ST-104
        bindings: {holder: knowledge_holder, actor: actor, subject: subject, requirement: requirement}
    - outcome: inspection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: InspectionCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-005
  - MC-006
  - MC-022
  - MC-023
  - MC-029
  - MC-030
  legacy_task_ids:
  - TCL-020
  - TCL-021
```

### TC-019 — Map

```yaml
id: TC-019
verb: Map
status: candidate
version: 0.11.0
signatures:
- signature_id: TC-019-S01
  semantic_family: SF-01
  legacy_name: Map Seabed
  actor_description: underwater/surface platform
  typed_complement: Seabed
  capability_type: CT-02
  implements_capabilities:
  - SurveyCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: seabed_area, type: nmo:SeabedArea, source: task_input}
    - {role: coverage_requirement, type: SM-TY-015, source: task_input}
    - role: map_product
      type: SM-TY-017
      source: {kind: execution_output, produced_by: map_product}
    reads:
    - state_ref: SM-ST-071
      bindings: {area: seabed_area, requirement: coverage_requirement}
    - state_ref: SM-ST-072
      bindings: {holder: knowledge_holder, area: seabed_area, requirement: coverage_requirement}
    - state_ref: SM-ST-009
      bindings: {area: seabed_area}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SurveyCapability}
    invariants:
    - state_ref: SM-ST-072
      bindings: {holder: knowledge_holder, area: seabed_area, requirement: coverage_requirement}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SurveyCapability}
    applicability:
      operational:
      - state_ref: SM-ST-071
        bindings: {area: seabed_area, requirement: coverage_requirement}
      - state_ref: SM-ST-072
        bindings: {holder: knowledge_holder, area: seabed_area, requirement: coverage_requirement}
      - state_ref: SM-ST-009
        bindings: {area: seabed_area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: SurveyCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-078
          bindings: {holder: knowledge_holder, map: map_product}
        - state_ref: SM-ST-079
          bindings: {holder: knowledge_holder, map: map_product, seabed: seabed_area}
        - state_ref: SM-ST-080
          bindings: {holder: knowledge_holder, map: map_product, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-078
      bindings: {holder: knowledge_holder, map: map_product}
    termination_conditions: []
    failure_outcomes:
    - outcome: mapping_quality_insufficient
      establishes:
      - state_ref: SM-ST-081
        bindings: {holder: knowledge_holder, actor: actor, seabed: seabed_area}
    - outcome: survey_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: SurveyCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-042
  - MC-043
  - MC-051
  legacy_task_ids:
  - TCL-022
```

### TC-020 — Measure

```yaml
id: TC-020
verb: Measure
status: candidate
version: 0.11.0
signatures:
- signature_id: TC-020-S01
  semantic_family: SF-01
  legacy_name: Measure Environment
  actor_description: sensing platform
  typed_complement: Environment
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
  - SamplingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: knowledge_holder, type: SM-TY-001, source: task_input}
    - {role: area, type: nmo:SpatialRegion, source: task_input}
    - {role: property, type: nmo:PhysicalProperty, source: task_input}
    - role: measurement
      type: SM-TY-018
      source: {kind: execution_output, produced_by: measurement_record}
    reads:
    - state_ref: SM-ST-009
      bindings: {area: area}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SamplingCapability}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: PerceptionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: SamplingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-009
        bindings: {area: area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: PerceptionCapability}
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: SamplingCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge:
        add:
        - state_ref: SM-ST-082
          bindings: {holder: knowledge_holder, measurement: measurement}
        - state_ref: SM-ST-083
          bindings: {holder: knowledge_holder, measurement: measurement, property: property}
        - state_ref: SM-ST-084
          bindings: {holder: knowledge_holder, measurement: measurement, area: area}
        - state_ref: SM-ST-085
          bindings: {holder: knowledge_holder, measurement: measurement, actor: actor}
        remove: []
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-082
      bindings: {holder: knowledge_holder, measurement: measurement}
    termination_conditions: []
    failure_outcomes:
    - outcome: measurement_quality_insufficient
      establishes:
      - state_ref: SM-ST-086
        bindings: {holder: knowledge_holder, actor: actor, area: area, property: property}
    - outcome: perception_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: PerceptionCapability}
    - outcome: sampling_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: SamplingCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-042
  - MC-043
  - MC-054
  legacy_task_ids:
  - TCL-023
```

### TC-021 — Assess

```yaml
id: TC-021
verb: Assess
status: draft
version: 0.7.0
signatures:
- signature_id: TC-021-S01
  semantic_family: SF-01
  legacy_name: Assess Threat
  actor_description: command/processing actor
  typed_complement: Threat
  capability_type: CT-03
  implements_capabilities:
  - ThreatAssessmentCapability
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-012
  - MC-014
  - MC-015
  - MC-017
  - MC-018
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-035
  - MC-037
  - MC-038
  - MC-039
  - MC-041
  - MC-042
  - MC-043
  - MC-051
  - MC-054
  - MC-055
  - MC-056
  - MC-057
  - MC-058
  - MC-059
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-024
```

### TC-022 — Correlate

```yaml
id: TC-022
verb: Correlate
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-022-S01
  semantic_family: SF-01
  legacy_name: Correlate Observations
  actor_description: processing actor
  typed_complement: Observations
  capability_type: CT-03
  implements_capabilities:
  - DataProcessingCapability
traceability:
  used_by_missions:
  - MC-003
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-013
  - MC-015
  - MC-018
  - MC-022
  - MC-025
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  legacy_task_ids:
  - TCL-025
```

### TC-023 — Escort

```yaml
id: TC-023
verb: Escort
status: draft
version: 0.8.1
signatures:
- signature_id: TC-023-S01
  semantic_family: SF-03
  legacy_name: Escort Unit
  actor_description: escort platform or escort force
  typed_complement: Unit
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - TargetFollowingCapability
  semantics:
    semantic_kind: abstract
    execution_pattern: durative
    parameters:
    - role: escort_actor
      type: nmo:PhysicalEntity
      source: task_input
    - role: protected_unit
      type: nmo:PhysicalEntity
      source: task_input
    reads:
    - state_ref: SM-ST-006
      bindings: {escort: escort_actor, protected: protected_unit}
    - state_ref: SM-ST-010
      bindings: {entity: escort_actor, capability: ProtectionCapability}
    - state_ref: SM-ST-027
      bindings: {holder: escort_actor, target: protected_unit}
    invariants:
    - state_ref: SM-ST-010
      bindings: {entity: escort_actor, capability: ProtectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-006
        bindings: {escort: escort_actor, protected: protected_unit}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: escort_actor, capability: ProtectionCapability}
      - state_ref: SM-ST-027
        bindings: {holder: escort_actor, target: protected_unit}
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
    desired_outcomes:
    - state_ref: SM-ST-007
      bindings: {protected: protected_unit}
    - state_ref: SM-ST-008
      bindings: {protected: protected_unit}
    completion_conditions:
    - state_ref: SM-ST-007
      bindings: {protected: protected_unit}
    - state_ref: SM-ST-008
      bindings: {protected: protected_unit}
    termination_conditions: []
    failure_outcomes:
    - outcome: protected_unit_lost
      establishes:
      - state_ref: SM-ST-015
        bindings: {escort: escort_actor, protected: protected_unit}
    - outcome: escort_capability_lost
      establishes:
      - state_ref: SM-ST-014
        bindings: {escort: escort_actor, protected: protected_unit}
    execution:
      responsibility: level_1_planner
traceability:
  used_by_missions:
  - MC-023
  - MC-024
  - MC-026
  - MC-027
  - MC-031
  - MC-032
  - MC-044
  - MC-046
  - MC-048
  - MC-049
  - MC-062
  - MC-064
  legacy_task_ids:
  - TCL-027
```

### TC-024 — Screen

```yaml
id: TC-024
verb: Screen
status: candidate
version: 0.10.0
signatures:
- signature_id: TC-024-S01
  semantic_family: SF-03
  legacy_name: Screen Protected Force
  actor_description: screening unit/group
  typed_complement: Protected Force
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - TargetFollowingCapability
  semantics:
    semantic_kind: abstract
    execution_pattern: continuous
    parameters:
    - {role: screen_actor, type: nmo:PhysicalEntity, source: task_input}
    - {role: protected_force, type: nmo:PhysicalEntity, source: task_input}
    - {role: screen_plan, type: SM-TY-012, source: task_input}
    reads:
    - state_ref: SM-ST-055
      bindings: {protector: screen_actor, protected: protected_force}
    - state_ref: SM-ST-056
      bindings: {protected: protected_force, plan: screen_plan}
    - state_ref: SM-ST-027
      bindings: {holder: screen_actor, target: protected_force}
    - state_ref: SM-ST-010
      bindings: {entity: screen_actor, capability: ProtectionCapability}
    invariants:
    - state_ref: SM-ST-056
      bindings: {protected: protected_force, plan: screen_plan}
    - state_ref: SM-ST-027
      bindings: {holder: screen_actor, target: protected_force}
    - state_ref: SM-ST-010
      bindings: {entity: screen_actor, capability: ProtectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-055
        bindings: {protector: screen_actor, protected: protected_force}
      - state_ref: SM-ST-056
        bindings: {protected: protected_force, plan: screen_plan}
      - state_ref: SM-ST-027
        bindings: {holder: screen_actor, target: protected_force}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: screen_actor, capability: ProtectionCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes:
    - state_ref: SM-ST-057
      bindings: {protected: protected_force, plan: screen_plan}
    - state_ref: SM-ST-058
      bindings: {protected: protected_force, plan: screen_plan}
    - state_ref: SM-ST-008
      bindings: {protected: protected_force}
    completion_conditions: []
    termination_conditions:
    - {condition: parent_task_requests_stop, bindings: {screen_actor: screen_actor, protected_force: protected_force}}
    - {condition: screening_period_elapsed, bindings: {screen_actor: screen_actor, protected_force: protected_force}}
    - {condition: screening_handover_completed, bindings: {screen_actor: screen_actor, protected_force: protected_force}}
    - {condition: parent_mission_terminated, bindings: {screen_actor: screen_actor, protected_force: protected_force}}
    failure_outcomes:
    - outcome: persistent_screen_gap
      establishes:
      - state_ref: SM-ST-066
        bindings: {protector: screen_actor, protected: protected_force}
    - outcome: protected_force_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: screen_actor, target: protected_force}
    - outcome: protection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: screen_actor, capability: ProtectionCapability}
    execution: {responsibility: level_1_planner}
traceability:
  used_by_missions:
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  legacy_task_ids:
  - TCL-028
```

### TC-025 — Guard

```yaml
id: TC-025
verb: Guard
status: candidate
version: 0.10.0
signatures:
- signature_id: TC-025-S01
  semantic_family: SF-03
  legacy_name: Guard Object
  actor_description: guarding platform
  typed_complement: Object
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - StationKeepingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: continuous
    parameters:
    - {role: guard_actor, type: nmo:Platform, source: task_input}
    - {role: guarded_object, type: nmo:PhysicalEntity, source: task_input}
    reads:
    - state_ref: SM-ST-055
      bindings: {protector: guard_actor, protected: guarded_object}
    - state_ref: SM-ST-027
      bindings: {holder: guard_actor, target: guarded_object}
    - state_ref: SM-ST-010
      bindings: {entity: guard_actor, capability: ProtectionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: guard_actor, capability: StationKeepingCapability}
    invariants:
    - state_ref: SM-ST-027
      bindings: {holder: guard_actor, target: guarded_object}
    - state_ref: SM-ST-010
      bindings: {entity: guard_actor, capability: ProtectionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: guard_actor, capability: StationKeepingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-055
        bindings: {protector: guard_actor, protected: guarded_object}
      - state_ref: SM-ST-027
        bindings: {holder: guard_actor, target: guarded_object}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: guard_actor, capability: ProtectionCapability}
      - state_ref: SM-ST-010
        bindings: {entity: guard_actor, capability: StationKeepingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-059
          bindings: {guard: guard_actor, protected: guarded_object}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions: []
    termination_conditions:
    - {condition: parent_task_requests_stop, bindings: {guard_actor: guard_actor, guarded_object: guarded_object}}
    - {condition: guard_relief_received, bindings: {guard_actor: guard_actor, guarded_object: guarded_object}}
    - {condition: guarding_period_elapsed, bindings: {guard_actor: guard_actor, guarded_object: guarded_object}}
    - {condition: parent_mission_terminated, bindings: {guard_actor: guard_actor, guarded_object: guarded_object}}
    failure_outcomes:
    - outcome: guarded_object_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: guard_actor, target: guarded_object}
    - outcome: protection_criteria_violated
      establishes:
      - state_ref: SM-ST-066
        bindings: {protector: guard_actor, protected: guarded_object}
    - outcome: protection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: guard_actor, capability: ProtectionCapability}
    - outcome: station_keeping_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: guard_actor, capability: StationKeepingCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-021
  - MC-023
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-046
  legacy_task_ids:
  - TCL-029
```

### TC-026 — Block

```yaml
id: TC-026
verb: Block
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-026-S01
  semantic_family: SF-04
  legacy_name: Block Approach
  actor_description: mobile platform
  typed_complement: Approach
  capability_type: CT-01
  implements_capabilities:
  - StationKeepingCapability
traceability:
  used_by_missions:
  - MC-021
  - MC-029
  - MC-030
  - MC-031
  - MC-033
  - MC-040
  - MC-046
  - MC-057
  legacy_task_ids:
  - TCL-030
```

### TC-027 — Interpose

```yaml
id: TC-027
verb: Interpose
status: candidate
version: 0.10.0
signatures:
- signature_id: TC-027-S01
  semantic_family: SF-03
  legacy_name: Interpose
  actor_description: mobile platform
  typed_complement: context
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: protected_subject, type: nmo:PhysicalEntity, source: task_input}
    - {role: threat, type: nmo:PhysicalEntity, source: task_input}
    reads:
    - state_ref: SM-ST-055
      bindings: {protector: actor, protected: protected_subject}
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: protected_subject}
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: threat}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    invariants:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: protected_subject}
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: threat}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: TargetFollowingCapability}
    applicability:
      operational:
      - state_ref: SM-ST-055
        bindings: {protector: actor, protected: protected_subject}
      - state_ref: SM-ST-027
        bindings: {holder: actor, target: protected_subject}
      - state_ref: SM-ST-027
        bindings: {holder: actor, target: threat}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: TargetFollowingCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-060
          bindings: {actor: actor, protected: protected_subject, threat: threat}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-061
      bindings: {actor: actor, protected: protected_subject, threat: threat}
    termination_conditions: []
    failure_outcomes:
    - outcome: protected_subject_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: actor, target: protected_subject}
    - outcome: threat_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: actor, target: threat}
    - outcome: interposition_navigation_failed
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: threat}
    - outcome: target_following_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: TargetFollowingCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions:
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-033
  legacy_task_ids:
  - TCL-031
```

### TC-028 — Defend

```yaml
id: TC-028
verb: Defend
status: candidate
version: 0.10.0
signatures:
- signature_id: TC-028-S01
  semantic_family: SF-03
  legacy_name: Defend Area
  actor_description: force/group
  typed_complement: Area
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - EngagementCapability
  semantics:
    semantic_kind: abstract
    execution_pattern: continuous
    parameters:
    - {role: defender, type: nmo:PhysicalEntity, source: task_input}
    - {role: protected_area, type: nmo:SpatialRegion, source: task_input}
    - {role: defense_plan, type: SM-TY-012, source: task_input}
    reads:
    - state_ref: SM-ST-055
      bindings: {protector: defender, protected: protected_area}
    - state_ref: SM-ST-056
      bindings: {protected: protected_area, plan: defense_plan}
    - state_ref: SM-ST-009
      bindings: {area: protected_area}
    - state_ref: SM-ST-010
      bindings: {entity: defender, capability: ProtectionCapability}
    - state_ref: SM-ST-010
      bindings: {entity: defender, capability: EngagementCapability}
    invariants:
    - state_ref: SM-ST-056
      bindings: {protected: protected_area, plan: defense_plan}
    - state_ref: SM-ST-010
      bindings: {entity: defender, capability: ProtectionCapability}
    applicability:
      operational:
      - state_ref: SM-ST-055
        bindings: {protector: defender, protected: protected_area}
      - state_ref: SM-ST-056
        bindings: {protected: protected_area, plan: defense_plan}
      - state_ref: SM-ST-009
        bindings: {area: protected_area}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: defender, capability: ProtectionCapability}
      - state_ref: SM-ST-010
        bindings: {entity: defender, capability: EngagementCapability}
    operational_effects:
      world: {add: [], remove: []}
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes:
    - state_ref: SM-ST-062
      bindings: {area: protected_area, plan: defense_plan}
    completion_conditions: []
    termination_conditions:
    - {condition: parent_task_requests_stop, bindings: {defender: defender, protected_area: protected_area}}
    - {condition: defense_period_elapsed, bindings: {defender: defender, protected_area: protected_area}}
    - {condition: defense_handover_completed, bindings: {defender: defender, protected_area: protected_area}}
    - {condition: parent_mission_terminated, bindings: {defender: defender, protected_area: protected_area}}
    failure_outcomes:
    - outcome: area_protection_criteria_violated
      establishes:
      - state_ref: SM-ST-066
        bindings: {protector: defender, protected: protected_area}
    - outcome: protection_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: defender, capability: ProtectionCapability}
    - outcome: engagement_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: defender, capability: EngagementCapability}
    execution: {responsibility: level_1_planner}
traceability:
  used_by_missions:
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-044
  - MC-046
  - MC-056
  - MC-062
  legacy_task_ids:
  - TCL-032
```

### TC-029 — Evade

```yaml
id: TC-029
verb: Evade
status: candidate
version: 0.9.0
signatures:
- signature_id: TC-029-S01
  semantic_family: SF-02
  legacy_name: Evade Threat
  actor_description: mobile platform
  typed_complement: Threat
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: actor, type: nmo:Platform, source: task_input}
    - {role: threat, type: nmo:PhysicalEntity, source: task_input}
    reads:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: threat}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    invariants:
    - state_ref: SM-ST-027
      bindings: {holder: actor, target: threat}
    - state_ref: SM-ST-010
      bindings: {entity: actor, capability: MobilityCapability}
    applicability:
      operational:
      - state_ref: SM-ST-027
        bindings: {holder: actor, target: threat}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: actor, capability: MobilityCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-053
          bindings: {actor: actor, threat: threat}
        remove: []
      knowledge: {add: [], remove: []}
      resources: {add: [], remove: []}
    desired_outcomes: []
    completion_conditions:
    - state_ref: SM-ST-054
      bindings: {actor: actor, threat: threat}
    termination_conditions: []
    failure_outcomes:
    - outcome: threat_location_lost
      establishes:
      - state_ref: SM-ST-028
        bindings: {holder: actor, target: threat}
    - outcome: evasion_navigation_failed
      establishes:
      - state_ref: SM-ST-013
        bindings: {entity: actor, objective: threat}
    - outcome: mobility_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: actor, capability: MobilityCapability}
    execution: {responsibility: platform_autonomy}
traceability:
  used_by_missions: []
  legacy_task_ids:
  - TCL-033
```

### TC-030 — Intercept

```yaml
id: TC-030
verb: Intercept
status: draft
version: 0.7.0
signatures:
- signature_id: TC-030-S01
  semantic_family: SF-04
  legacy_name: Intercept Platform
  actor_description: mobile platform
  typed_complement: Platform
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - TargetFollowingCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-040
  legacy_task_ids:
  - TCL-034
```

### TC-031 — Hail

```yaml
id: TC-031
verb: Hail
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-031-S01
  semantic_family: SF-04
  legacy_name: Hail Vessel
  actor_description: communication-capable platform
  typed_complement: Vessel
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-029
  - MC-030
  legacy_task_ids:
  - TCL-035
```

### TC-032 — Direct

```yaml
id: TC-032
verb: Direct
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-032-S01
  semantic_family: SF-04
  legacy_name: Direct Vessel
  actor_description: command/interdiction actor
  typed_complement: Vessel
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  legacy_task_ids:
  - TCL-036
```

### TC-033 — Compel

```yaml
id: TC-033
verb: Compel
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-033-S01
  semantic_family: SF-04
  legacy_name: Compel Course Change
  actor_description: interdiction actor
  typed_complement: Course Change
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-030
  - MC-040
  legacy_task_ids:
  - TCL-037
```

### TC-034 — Board

```yaml
id: TC-034
verb: Board
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-034-S01
  semantic_family: SF-04
  legacy_name: Board Vessel
  actor_description: boarding force
  typed_complement: Vessel
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - ManipulationCapability
traceability:
  used_by_missions:
  - MC-020
  - MC-022
  - MC-023
  - MC-024
  legacy_task_ids:
  - TCL-038
```

### TC-035 — Seize

```yaml
id: TC-035
verb: Seize
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-035-S01
  semantic_family: SF-04
  legacy_name: Seize Object
  actor_description: authorized force
  typed_complement: Object
  capability_type: CT-05
  implements_capabilities:
  - InterdictionCapability
  - ManipulationCapability
traceability:
  used_by_missions:
  - MC-020
  - MC-022
  - MC-023
  legacy_task_ids:
  - TCL-040
```

### TC-036 — Engage

```yaml
id: TC-036
verb: Engage
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-036-S01
  semantic_family: SF-04
  legacy_name: Engage Threat
  actor_description: authorized effector
  typed_complement: Threat
  capability_type: CT-05
  implements_capabilities:
  - EngagementCapability
traceability:
  used_by_missions:
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-033
  - MC-034
  - MC-035
  - MC-037
  - MC-038
  - MC-039
  - MC-040
  - MC-041
  - MC-044
  - MC-046
  - MC-062
  legacy_task_ids:
  - TCL-041
```

### TC-037 — Neutralize

```yaml
id: TC-037
verb: Neutralize
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-037-S01
  semantic_family: SF-04
  legacy_name: Neutralize Threat
  actor_description: authorized effector
  typed_complement: Threat
  capability_type: CT-05
  implements_capabilities:
  - NeutralizationCapability
- signature_id: TC-037-S02
  semantic_family: SF-04
  legacy_name: Neutralize Mine
  actor_description: MCM system
  typed_complement: Mine
  capability_type: CT-05
  implements_capabilities:
  - NeutralizationCapability
traceability:
  used_by_missions:
  - MC-014
  - MC-025
  - MC-029
  - MC-030
  legacy_task_ids:
  - TCL-042
  - TCL-043
```

### TC-038 — Deploy

```yaml
id: TC-038
verb: Deploy
status: candidate
version: 0.10.0
signatures:
- signature_id: TC-038-S01
  semantic_family: SF-04
  legacy_name: Deploy Mine
  actor_description: minelaying platform
  typed_complement: Mine
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
- signature_id: TC-038-S02
  semantic_family: SF-03
  legacy_name: Deploy Decoy
  actor_description: platform
  typed_complement: Decoy
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
  semantics:
    semantic_kind: primitive
    execution_pattern: durative
    parameters:
    - {role: carrier, type: nmo:Platform, source: task_input}
    - {role: decoy, type: nmo:Decoy, source: task_input}
    - {role: deployment_location, type: nmo:SpatialRegion, source: task_input}
    - {role: protected_subject, type: SM-TY-013, source: task_input}
    reads:
    - state_ref: SM-ST-055
      bindings: {protector: carrier, protected: protected_subject}
    - state_ref: SM-ST-009
      bindings: {area: deployment_location}
    - state_ref: SM-ST-063
      bindings: {carrier: carrier, deployable: decoy}
    - state_ref: SM-ST-010
      bindings: {entity: carrier, capability: DeploymentCapability}
    invariants:
    - state_ref: SM-ST-063
      bindings: {carrier: carrier, deployable: decoy}
    - state_ref: SM-ST-010
      bindings: {entity: carrier, capability: DeploymentCapability}
    applicability:
      operational:
      - state_ref: SM-ST-055
        bindings: {protector: carrier, protected: protected_subject}
      - state_ref: SM-ST-009
        bindings: {area: deployment_location}
      - state_ref: SM-ST-063
        bindings: {carrier: carrier, deployable: decoy}
      execution:
      - state_ref: SM-ST-010
        bindings: {entity: carrier, capability: DeploymentCapability}
    operational_effects:
      world:
        add:
        - state_ref: SM-ST-064
          bindings: {deployable: decoy, location: deployment_location}
        remove: []
      knowledge: {add: [], remove: []}
      resources:
        add: []
        remove:
        - state_ref: SM-ST-063
          bindings: {carrier: carrier, deployable: decoy}
    desired_outcomes:
    - state_ref: SM-ST-065
      bindings: {decoy: decoy, protected: protected_subject}
    completion_conditions:
    - state_ref: SM-ST-064
      bindings: {deployable: decoy, location: deployment_location}
    - state_ref: SM-ST-065
      bindings: {decoy: decoy, protected: protected_subject}
    termination_conditions: []
    failure_outcomes:
    - outcome: decoy_deployment_failed
      establishes:
      - state_ref: SM-ST-067
        bindings: {carrier: carrier, deployable: decoy}
    - outcome: decoy_effect_not_established
      establishes:
      - state_ref: SM-ST-066
        bindings: {protector: carrier, protected: protected_subject}
    - outcome: deployment_capability_lost
      establishes:
      - state_ref: SM-ST-011
        bindings: {entity: carrier, capability: DeploymentCapability}
    execution: {responsibility: platform_autonomy}
- signature_id: TC-038-S03
  semantic_family: SF-07
  legacy_name: Deploy Payload
  actor_description: carrier platform
  typed_complement: Payload
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
traceability:
  used_by_missions:
  - MC-016
  - MC-033
  - MC-044
  - MC-045
  - MC-052
  - MC-058
  - MC-059
  legacy_task_ids:
  - TCL-044
  - TCL-045
  - TCL-059
```

### TC-039 — Report

```yaml
id: TC-039
verb: Report
status: draft
version: 0.7.0
signatures:
- signature_id: TC-039-S01
  semantic_family: SF-06
  legacy_name: Report Information
  actor_description: any communicating actor
  typed_complement: Information
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-001
  - MC-002
  - MC-003
  - MC-004
  - MC-005
  - MC-006
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-015
  - MC-016
  - MC-017
  - MC-018
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-034
  - MC-036
  - MC-039
  - MC-040
  - MC-041
  - MC-042
  - MC-043
  - MC-044
  - MC-045
  - MC-046
  - MC-047
  - MC-048
  - MC-049
  - MC-050
  - MC-051
  - MC-052
  - MC-053
  - MC-054
  - MC-055
  - MC-056
  - MC-057
  - MC-058
  - MC-059
  - MC-060
  - MC-061
  - MC-062
  - MC-063
  - MC-064
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-046
```

### TC-040 — Share

```yaml
id: TC-040
verb: Share
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-040-S01
  semantic_family: SF-06
  legacy_name: Share Track
  actor_description: communicating actor
  typed_complement: Track
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
  - DataProcessingCapability
traceability:
  used_by_missions:
  - MC-002
  - MC-017
  - MC-018
  - MC-022
  - MC-023
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-041
  - MC-045
  - MC-051
  - MC-058
  legacy_task_ids:
  - TCL-047
```

### TC-041 — Request

```yaml
id: TC-041
verb: Request
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-041-S01
  semantic_family: SF-06
  legacy_name: Request Support
  actor_description: actor/force
  typed_complement: Support
  capability_type: CT-10
  implements_capabilities:
  - CoordinationCapability
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-041
  legacy_task_ids:
  - TCL-048
```

### TC-042 — Assign

```yaml
id: TC-042
verb: Assign
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-042-S01
  semantic_family: SF-06
  legacy_name: Assign Task
  actor_description: command actor
  typed_complement: Task
  capability_type: CT-10
  implements_capabilities:
  - CoordinationCapability
traceability:
  used_by_missions:
  - MC-028
  - MC-032
  - MC-033
  - MC-035
  - MC-037
  - MC-038
  - MC-039
  - MC-041
  - MC-052
  legacy_task_ids:
  - TCL-049
```

### TC-043 — Coordinate

```yaml
id: TC-043
verb: Coordinate
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-043-S01
  semantic_family: SF-06
  legacy_name: Coordinate Action
  actor_description: command/group actor
  typed_complement: Action
  capability_type: CT-10
  implements_capabilities:
  - CoordinationCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-020
  - MC-021
  - MC-022
  - MC-023
  - MC-024
  - MC-025
  - MC-026
  - MC-027
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-041
  - MC-044
  - MC-045
  - MC-047
  - MC-049
  - MC-050
  - MC-051
  - MC-052
  - MC-055
  - MC-056
  - MC-058
  - MC-059
  - MC-062
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-050
```

### TC-044 — Relay

```yaml
id: TC-044
verb: Relay
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-044-S01
  semantic_family: SF-06
  legacy_name: Relay Communications
  actor_description: relay-capable platform
  typed_complement: Communications
  capability_type: CT-09
  implements_capabilities:
  - RelayCapability
traceability:
  used_by_missions:
  - MC-002
  - MC-017
  - MC-032
  - MC-045
  - MC-050
  - MC-051
  - MC-056
  legacy_task_ids:
  - TCL-051
```

### TC-045 — Establish

```yaml
id: TC-045
verb: Establish
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-045-S01
  semantic_family: SF-06
  legacy_name: Establish Communication Link
  actor_description: communicating actors
  typed_complement: Communication Link
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-030
  - MC-031
  - MC-033
  - MC-050
  - MC-051
  - MC-056
  legacy_task_ids:
  - TCL-052
```

### TC-046 — Transmit

```yaml
id: TC-046
verb: Transmit
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-046-S01
  semantic_family: SF-06
  legacy_name: Transmit Command
  actor_description: command actor
  typed_complement: Command
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-050
  - MC-051
  - MC-052
  - MC-058
  legacy_task_ids:
  - TCL-054
```

### TC-047 — Update

```yaml
id: TC-047
verb: Update
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-047-S01
  semantic_family: SF-06
  legacy_name: Update Mission Plan
  actor_description: command/planning actor
  typed_complement: Mission Plan
  capability_type: CT-10
  implements_capabilities:
  - CoordinationCapability
  - DataProcessingCapability
traceability:
  used_by_missions:
  - MC-018
  - MC-031
  - MC-032
  - MC-051
  legacy_task_ids:
  - TCL-055
```

### TC-048 — Launch

```yaml
id: TC-048
verb: Launch
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-048-S01
  semantic_family: SF-07
  legacy_name: Launch Platform
  actor_description: host/support platform
  typed_complement: Platform
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
  - PayloadHostingCapability
traceability:
  used_by_missions:
  - MC-052
  - MC-059
  legacy_task_ids:
  - TCL-056
```

### TC-049 — Recover

```yaml
id: TC-049
verb: Recover
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-049-S01
  semantic_family: SF-07
  legacy_name: Recover Platform
  actor_description: host/support platform
  typed_complement: Platform
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
- signature_id: TC-049-S02
  semantic_family: SF-07
  legacy_name: Recover Payload
  actor_description: carrier platform
  typed_complement: Payload
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
- signature_id: TC-049-S03
  semantic_family: SF-05
  legacy_name: Recover Personnel
  actor_description: recovery actor
  typed_complement: Personnel
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
traceability:
  used_by_missions:
  - MC-024
  - MC-045
  - MC-053
  - MC-059
  - MC-061
  - MC-062
  - MC-064
  - MC-066
  legacy_task_ids:
  - TCL-057
  - TCL-060
  - TCL-069
```

### TC-050 — Dock

```yaml
id: TC-050
verb: Dock
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-050-S01
  semantic_family: SF-07
  legacy_name: Dock Platform
  actor_description: mobile platform/docking station
  typed_complement: Platform
  capability_type: CT-07
  implements_capabilities:
  - DockingCapability
traceability:
  used_by_missions:
  - MC-047
  - MC-053
  legacy_task_ids:
  - TCL-058
```

### TC-051 — Transport

```yaml
id: TC-051
verb: Transport
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-051-S01
  semantic_family: SF-07
  legacy_name: Transport Payload
  actor_description: transport platform
  typed_complement: Payload
  capability_type: CT-08
  implements_capabilities:
  - TransportCapability
traceability:
  used_by_missions:
  - MC-016
  - MC-023
  - MC-044
  - MC-045
  - MC-047
  - MC-048
  - MC-049
  - MC-052
  - MC-053
  - MC-061
  - MC-066
  legacy_task_ids:
  - TCL-061
```

### TC-052 — Transfer

```yaml
id: TC-052
verb: Transfer
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-052-S01
  semantic_family: SF-07
  legacy_name: Transfer Materiel
  actor_description: support actor
  typed_complement: Materiel
  capability_type: CT-08
  implements_capabilities:
  - LogisticsCapability
traceability:
  used_by_missions:
  - MC-023
  - MC-047
  - MC-048
  - MC-049
  - MC-053
  - MC-065
  legacy_task_ids:
  - TCL-062
```

### TC-053 — Resupply

```yaml
id: TC-053
verb: Resupply
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-053-S01
  semantic_family: SF-07
  legacy_name: Resupply Platform
  actor_description: support platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - LogisticsCapability
traceability:
  used_by_missions:
  - MC-032
  - MC-047
  - MC-065
  legacy_task_ids:
  - TCL-063
```

### TC-054 — Recharge

```yaml
id: TC-054
verb: Recharge
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-054-S01
  semantic_family: SF-07
  legacy_name: Recharge Platform
  actor_description: energy source/host
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - EnergySupplyCapability
traceability:
  used_by_missions:
  - MC-047
  - MC-065
  legacy_task_ids:
  - TCL-064
```

### TC-055 — Refuel

```yaml
id: TC-055
verb: Refuel
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-055-S01
  semantic_family: SF-07
  legacy_name: Refuel Platform
  actor_description: support platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - EnergySupplyCapability
traceability:
  used_by_missions:
  - MC-047
  - MC-065
  legacy_task_ids:
  - TCL-065
```

### TC-056 — Tow

```yaml
id: TC-056
verb: Tow
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-056-S01
  semantic_family: SF-07
  legacy_name: Tow Platform
  actor_description: towing platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - TransportCapability
traceability:
  used_by_missions:
  - MC-064
  - MC-065
  legacy_task_ids:
  - TCL-066
```

### TC-057 — Locate

```yaml
id: TC-057
verb: Locate
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-057-S01
  semantic_family: SF-01
  legacy_name: Locate Missing Entity
  actor_description: search platform
  typed_complement: Missing Entity
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
- signature_id: TC-057-S02
  semantic_family: SF-01
  legacy_name: Locate Emitter
  actor_description: sensing/processing actor
  typed_complement: Emitter
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
  - DetectionCapability
traceability:
  used_by_missions:
  - MC-011
  - MC-053
  - MC-060
  - MC-061
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-067
  - TCL-075
```

### TC-058 — Mark

```yaml
id: TC-058
verb: Mark
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-058-S01
  semantic_family: SF-05
  legacy_name: Mark Location
  actor_description: platform
  typed_complement: Location
  capability_type: CT-06
  implements_capabilities:
  - MarkingCapability
traceability:
  used_by_missions:
  - MC-011
  - MC-012
  - MC-013
  - MC-014
  - MC-016
  - MC-029
  - MC-030
  - MC-031
  - MC-060
  legacy_task_ids:
  - TCL-068
```

### TC-059 — Assist

```yaml
id: TC-059
verb: Assist
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-059-S01
  semantic_family: SF-05
  legacy_name: Assist Distressed Platform
  actor_description: support actor
  typed_complement: Distressed Platform
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
traceability:
  used_by_missions:
  - MC-023
  - MC-024
  - MC-044
  - MC-045
  - MC-061
  - MC-062
  - MC-064
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-070
```

### TC-060 — Stabilize

```yaml
id: TC-060
verb: Stabilize
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-060-S01
  semantic_family: SF-05
  legacy_name: Stabilize Casualty
  actor_description: medical actor
  typed_complement: Casualty
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
traceability:
  used_by_missions:
  - MC-061
  - MC-064
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-071
```

### TC-061 — Evacuate

```yaml
id: TC-061
verb: Evacuate
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-061-S01
  semantic_family: SF-05
  legacy_name: Evacuate Casualty
  actor_description: transport/recovery actor
  typed_complement: Casualty
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
  - TransportCapability
traceability:
  used_by_missions:
  - MC-061
  - MC-066
  legacy_task_ids:
  - TCL-072
```

### TC-062 — Monitor

```yaml
id: TC-062
verb: Monitor
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-062-S01
  semantic_family: SF-01
  legacy_name: Monitor Spectrum
  actor_description: sensing platform
  typed_complement: Spectrum
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
  - DetectionCapability
traceability:
  used_by_missions:
  - MC-018
  - MC-021
  - MC-028
  - MC-029
  - MC-030
  - MC-031
  - MC-032
  - MC-033
  - MC-050
  - MC-051
  - MC-054
  - MC-056
  legacy_task_ids:
  - TCL-076
```

### TC-063 — Jam

```yaml
id: TC-063
verb: Jam
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-063-S01
  semantic_family: SF-04
  legacy_name: Jam Communication
  actor_description: authorized EW actor
  typed_complement: Communication
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
- signature_id: TC-063-S02
  semantic_family: SF-04
  legacy_name: Jam Sensor
  actor_description: authorized EW actor
  typed_complement: Sensor
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
traceability:
  used_by_missions:
  - MC-025
  - MC-028
  - MC-055
  - MC-057
  - MC-058
  legacy_task_ids:
  - TCL-077
  - TCL-078
```

### TC-064 — Emit

```yaml
id: TC-064
verb: Emit
status: candidate
version: 0.7.0
signatures:
- signature_id: TC-064-S01
  semantic_family: SF-04
  legacy_name: Emit Deceptive Signal
  actor_description: EW/decoy actor
  typed_complement: Deceptive Signal
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
traceability:
  used_by_missions:
  - MC-055
  - MC-057
  - MC-058
  - MC-059
  legacy_task_ids:
  - TCL-079
```

## 7. Boundary rules

- Actor types, physical arguments and capabilities reference the Naval Ontology.
- Each signature references the most specific applicable ontology Capability class — never a generic ancestor when a specific class exists.
- Each signature has one stable `signature_id` and references exactly one Semantic Family.
- A task-level family view is derived from its signatures and is never maintained independently.
- Operational roles, target status and task progress belong to the Scenario Model.
- Completion outcomes and planning predicates belong to planning or execution state.
- A lexical verb is not merged when its semantics cannot be represented by typed signatures without ambiguity; signature-level capability classification is the mechanism that preserves this rule under merging.

## 8. Changes 0.2.0 → 0.3.0

1. **Capability classification moved from task level to signature level** (`capability_type` and `implements_capabilities` per signature). Resolves the Search/Maintain inconsistency without splitting canonical verbs.
2. **`implements_capabilities` refined to the most specific ontology classes** (46-class Capability hierarchy of the Naval Ontology v2.0). This closes the resolution chain verb → capability → `nmo:manifestKey` → typed action family.
3. **Legacy identifiers renamed `TCL-NNN`** to eliminate namespace collision with canonical `TC-NNN` identifiers.
4. **Signature-level reclassifications** (to be reviewed by naval domain experts):

| Signature | 0.2.0 | 0.3.0 |
|---|---|---|
| Search Area | CT-05 | CT-02 |
| Maintain Operational Picture | CT-01 | CT-03 |
| Maintain Communication Link | CT-01 | CT-09 |
| Characterize Emission | CT-02 | CT-11 |
| Correlate Observations | CT-02 | CT-03 |
| Locate Missing Entity | CT-06 | CT-02 |
| Locate Emitter | CT-06 | CT-11 |

## 8.1 Semantic foundation introduced in v0.6.0

The first semantic implementation covers TC-001 Navigate, TC-006 Follow and TC-023 Escort. Candidate state names are intentionally provisional until normalization into the LOTUSim State Model.

## 8.2 Semantic pilot closed in v0.6.1

- Aligned the four pilot signatures with the canonical DEM-2 v0.3 semantic structure.
- Added mandatory `execution_pattern`, explicit parameter sources, applicability, desired outcomes, completion conditions and termination conditions.
- Replaced `located_at_previous_location` with tuple-exact removal of `located_at(actor, origin)`, where `origin` is captured from state at task start.
- Made the Route signature bind both its destination and origin explicitly instead of relying on the implicit `route_destination` variable.
- Declared Follow as continuous and separated normal termination from failure.
- Removed the direct `escort_completed` effect from abstract Escort and expressed its intent as desired outcomes.
- Kept all state names as controlled candidates pending derivation of stable State Model identifiers.

## 8.3 Traceability refresh for Mission Catalog v1.0.4

- Regenerated every `used_by_missions` list from all 66 active mission specifications MC-001 through MC-066.
- Removed links inherited from the divergent non-normative mission proposals.
- No task identity, typed signature or operational semantics changed.

## 8.4 Semantic Families stabilized in v0.7.0

- Defined seven normative Semantic Families with objectives, shared concepts, transitions, invariants, terminology and validation rules.
- Assigned a stable `TC-NNN-SNN` identifier and exactly one `semantic_family` to each of the 79 typed signatures.
- Kept generic verbs multi-family when required: their family view is the derived union of their signatures.
- Added the canonical multi-family example `Search`: `Search Area` belongs to ISR, while `Search Vessel` belongs to Engagement.

## 8.5 Core ISR semantics introduced in v0.8.0

- Added complete operational semantics to the seven signatures of Observe, Detect, Localize, Classify, Identify and Track.
- Made every ISR knowledge effect relative to an explicit `knowledge_holder`.
- Kept all world effects empty: perception changes knowledge, not the observed physical reality.
- Added typed `execution_output` bindings for observations, evidence, estimates, assessments and tracks.
- Defined ISR as a branching knowledge progression rather than a mandatory linear pipeline.
- Declared Track as continuous, with explicit normal termination conditions and `target_lost` as a failure outcome.

## 8.6 State Model alignment in v0.8.1

- Replaced every candidate state name in the 11 enriched signatures with a stable `SM-ST-NNN` reference from State Model v0.1.
- Replaced generic parameter type names with explicit `nmo:` or `SM-TY-NNN` references and verified their compatibility with State Model arguments.
- Normalized location knowledge across Follow, Localize and Escort through `SM-ST-027 location_known` and `SM-ST-028 location_unknown`.
- Replaced the Escort-specific capability state with generic `SM-ST-010 capability_available`, explicitly bound to `ProtectionCapability`.
- Gave `SM-ST-013 navigation_failed` one canonical tuple shape through the `navigation_objective` union type.
- Added the `location_known` projection as a Localize knowledge effect.

## 8.7 Movement family completed in v0.9.0

- Added complete semantics to the eight remaining Movement signatures: Patrol Area, Maintain Station, Maintain Formation, Shadow, Approach, Withdraw, Transit Corridor and Evade.
- Distinguished continuous active relations from durative completion conditions.
- Reused holder-relative location and track knowledge for target-relative movement.
- Added explicit origin capture for withdrawal and corridor transit location replacement.
- Aligned all new state references with State Model v0.2.

## 8.8 Protection family completed in v0.10.0

- Added complete semantics to Screen Protected Force, Guard Object, Interpose, Defend Area and Deploy Decoy.
- Kept Screen and Defend abstract and effect-free, with explicit desired outcomes and normal termination conditions.
- Distinguished active guarding and interposition from derived protection and geometry criteria.
- Modeled decoy deployment as an atomic custody-to-world transition and kept the decoy's protective effect derived.
- Aligned all Protection state references with State Model v0.3.

## 8.9 ISR coverage and products introduced in v0.11.0

- Added complete semantics to Search Area, Survey Area, Map Seabed and Measure Environment.
- Made Search Area abstract and requirement-driven, without direct knowledge or world effects.
- Promoted area coverage to a normative holder- and requirement-relative derived state.
- Added typed survey, map and measurement products with explicit scope and provenance.
- Kept all four signatures free of direct world effects and aligned them with State Model v0.4.

## 8.10 ISR characterization and inspection introduced in v0.12.0

- Added complete semantics to Characterize Object, Characterize Emission, Inspect Object and Inspect Infrastructure.
- Distinguished characterization from classification and identification through explicit requirement-scoped assessment products.
- Added immutable inspection records with subject, requirement satisfaction and producing-platform provenance.
- Kept all four signatures free of direct world effects and aligned them with State Model v0.5.

## 9. Changes 0.3.1 → 0.3.2

- Regenerated `used_by_missions` from the Mission Catalog v0.5.0, including the completed Mine Warfare family MC-012 to MC-017.
- No task identity or signature semantics changed.

## 10. Open points

- **Fate of the Capability Type layer (CT-01…CT-11):** now that signatures reference fine-grained ontology classes, the CT layer is derivable from the ontology hierarchy and does not superpose cleanly onto it (CT-04/05/06/07 all fall under `InteractionCapability`; CT-03 and CT-10 sit under `SupportCapability`). Decision pending: keep as editorial grouping, or drop in favour of the ontology hierarchy.
- **Target localization:** `nmo:LocalizationCapability` denotes platform self-localization (subclass of `NavigationCapability`). No ontology class covers *target* localization; `Localize Object` and Mission Catalog MT-02 baselines currently fall back to `DetectionCapability`/`PerceptionCapability`. Candidate ontology addition: `TargetLocalizationCapability` under `PerceptionCapability`.
- Continue regenerating `used_by_missions` from Mission Catalog `task_candidates` after each mission-family consolidation; do not maintain the reverse links manually.


## Changes 0.3.3 → 0.3.4

- Recomputed `used_by_missions` after completion of MC-028 through MC-033.
