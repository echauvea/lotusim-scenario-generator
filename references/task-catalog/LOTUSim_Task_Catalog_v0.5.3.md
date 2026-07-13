# LOTUSim Task Catalog

> **Status:** working draft  
> **Version:** 0.3.4  
> **Date:** 2026-07-13  
> **Scope:** reusable operational actions expressed as canonical verbs with typed signatures.

## 1. Purpose

The Task Catalog defines the controlled action vocabulary used by LSG missions, scenarios and derived planning artefacts.

A Task is represented by a canonical verb. Its complement is not part of the task identity: it is expressed through one or more typed signatures.

The catalog does not define HDDL methods, ordering, predicates, execution algorithms or autonomy behaviours.

## 2. Task meta-model

```text
Task
├── Identity
├── Typed signatures (each carrying its own capability classification)
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

- `capability_type`: one Capability Type (editorial grouping, see §3);
- `implements_capabilities`: references to the **most specific applicable** Naval Ontology Capability classes.

Referencing the most specific ontology class is what makes the resolution chain to typed execution actions work: capability classes carrying an `nmo:manifestKey` annotation (e.g. `TargetFollowingCapability → navigation.follow_target`) resolve a task signature to the typed action family of the 2 ↔ 3 execution contract, by simple ontology traversal, without any additional mapping table.

### 2.3 Traceability

- `used_by_missions`: Mission Catalog references;
- `legacy_task_names`: previous compound names retained for migration.

**Changed in 0.3.0 — legacy identifier namespace.** Legacy (pre-consolidation) task identifiers are now prefixed `TCL-NNN` to eliminate collisions with the canonical `TC-NNN` namespace.

## 3. Capability Types

Capability Types are an **editorial grouping layer** over the Naval Ontology Capability hierarchy. They ease human navigation of the inventory; they carry no semantics of their own and do not map one-to-one onto the ontology hierarchy. Whether this layer is retained or replaced by the ontology hierarchy itself is an open decision (see §9).

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

## 4. Machine-readable schema

```yaml
id: TC-003
verb: Search
status: candidate
version: 0.3.0

signatures:
  - legacy_name: Search Area
    actor_description: mobile platform
    typed_complement: Area
    capability_type: CT-02
    implements_capabilities:
      - DetectionCapability
  - legacy_name: Search Vessel
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
version: 0.3.0
signatures:
- legacy_name: Navigate to Location
  actor_description: mobile platform
  typed_complement: to Location
  capability_type: CT-01
  implements_capabilities:
  - WaypointNavigationCapability
- legacy_name: Navigate Route
  actor_description: mobile platform
  typed_complement: Route
  capability_type: CT-01
  implements_capabilities:
  - RouteFollowingCapability
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
  - MC-042
  - MC-043
  - MC-044
  - MC-051
  - MC-052
  legacy_task_ids:
  - TCL-001
  - TCL-002
```

### TC-002 — Patrol

```yaml
id: TC-002
verb: Patrol
status: draft
version: 0.3.0
signatures:
- legacy_name: Patrol Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
  - PerceptionCapability
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
  - MC-042
  - MC-043
  legacy_task_ids:
  - TCL-003
```

### TC-003 — Search

```yaml
id: TC-003
verb: Search
status: candidate
version: 0.3.0
signatures:
- legacy_name: Search Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
- legacy_name: Search Vessel
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
  - MC-049
  - MC-059
  legacy_task_ids:
  - TCL-004
  - TCL-039
```

### TC-004 — Survey

```yaml
id: TC-004
verb: Survey
status: candidate
version: 0.3.0
signatures:
- legacy_name: Survey Area
  actor_description: mobile platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - SurveyCapability
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
  legacy_task_ids:
  - TCL-005
```

### TC-005 — Maintain

```yaml
id: TC-005
verb: Maintain
status: draft
version: 0.3.0
signatures:
- legacy_name: Maintain Station
  actor_description: mobile platform
  typed_complement: Station
  capability_type: CT-01
  implements_capabilities:
  - StationKeepingCapability
- legacy_name: Maintain Formation
  actor_description: platform/group
  typed_complement: Formation
  capability_type: CT-01
  implements_capabilities:
  - StationKeepingCapability
  - CoordinationCapability
- legacy_name: Maintain Operational Picture
  actor_description: command/processing actor
  typed_complement: Operational Picture
  capability_type: CT-03
  implements_capabilities:
  - AssessmentCapability
  - DataProcessingCapability
- legacy_name: Maintain Communication Link
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
status: candidate
version: 0.3.0
signatures:
- legacy_name: Follow Designated Unit
  actor_description: mobile platform
  typed_complement: Designated Unit
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
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
version: 0.3.0
signatures:
- legacy_name: Shadow Designated Unit
  actor_description: mobile platform
  typed_complement: Designated Unit
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
  - TrackingCapability
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
version: 0.3.0
signatures:
- legacy_name: Approach Object
  actor_description: mobile platform
  typed_complement: Object
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
traceability:
  used_by_missions:
  - MC-019
  - MC-023
  - MC-048
  legacy_task_ids:
  - TCL-010
```

### TC-009 — Withdraw

```yaml
id: TC-009
verb: Withdraw
status: candidate
version: 0.3.0
signatures:
- legacy_name: Withdraw from Area
  actor_description: mobile platform
  typed_complement: from Area
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
traceability:
  used_by_missions:
  - MC-047
  legacy_task_ids:
  - TCL-011
```

### TC-010 — Transit

```yaml
id: TC-010
verb: Transit
status: candidate
version: 0.3.0
signatures:
- legacy_name: Transit Corridor
  actor_description: mobile platform
  typed_complement: Corridor
  capability_type: CT-01
  implements_capabilities:
  - RouteFollowingCapability
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
version: 0.3.0
signatures:
- legacy_name: Observe Area
  actor_description: sensing platform
  typed_complement: Area
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
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
  - MC-059
  legacy_task_ids:
  - TCL-013
```

### TC-012 — Detect

```yaml
id: TC-012
verb: Detect
status: draft
version: 0.3.0
signatures:
- legacy_name: Detect Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
- legacy_name: Detect Emission
  actor_description: sensing platform
  typed_complement: Emission
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
  - ElectronicWarfareCapability
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
  - MC-040
  - MC-041
  - MC-057
  - MC-058
  - MC-062
  legacy_task_ids:
  - TCL-014
  - TCL-073
```

### TC-013 — Localize

```yaml
id: TC-013
verb: Localize
status: candidate
version: 0.3.0
signatures:
- legacy_name: Localize Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
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
  legacy_task_ids:
  - TCL-015
```

### TC-014 — Classify

```yaml
id: TC-014
verb: Classify
status: draft
version: 0.3.0
signatures:
- legacy_name: Classify Object
  actor_description: sensing/processing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - ClassificationCapability
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
  - MC-058
  legacy_task_ids:
  - TCL-016
```

### TC-015 — Identify

```yaml
id: TC-015
verb: Identify
status: draft
version: 0.3.0
signatures:
- legacy_name: Identify Object
  actor_description: sensing/processing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - IdentificationCapability
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
  - MC-040
  - MC-041
  legacy_task_ids:
  - TCL-017
```

### TC-016 — Track

```yaml
id: TC-016
verb: Track
status: draft
version: 0.3.0
signatures:
- legacy_name: Track Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - TrackingCapability
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
  legacy_task_ids:
  - TCL-018
```

### TC-017 — Characterize

```yaml
id: TC-017
verb: Characterize
status: candidate
version: 0.3.0
signatures:
- legacy_name: Characterize Object
  actor_description: sensing platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - ClassificationCapability
- legacy_name: Characterize Emission
  actor_description: sensing/processing actor
  typed_complement: Emission
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
  - ClassificationCapability
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
  - MC-058
  legacy_task_ids:
  - TCL-019
  - TCL-074
```

### TC-018 — Inspect

```yaml
id: TC-018
verb: Inspect
status: candidate
version: 0.3.0
signatures:
- legacy_name: Inspect Object
  actor_description: inspection platform
  typed_complement: Object
  capability_type: CT-02
  implements_capabilities:
  - InspectionCapability
- legacy_name: Inspect Infrastructure
  actor_description: inspection platform
  typed_complement: Infrastructure
  capability_type: CT-02
  implements_capabilities:
  - InspectionCapability
traceability:
  used_by_missions:
  - MC-005
  - MC-006
  - MC-022
  - MC-023
  - MC-029
  - MC-030
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-020
  - TCL-021
```

### TC-019 — Map

```yaml
id: TC-019
verb: Map
status: candidate
version: 0.3.0
signatures:
- legacy_name: Map Seabed
  actor_description: underwater/surface platform
  typed_complement: Seabed
  capability_type: CT-02
  implements_capabilities:
  - SurveyCapability
traceability:
  used_by_missions:
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  legacy_task_ids:
  - TCL-022
```

### TC-020 — Measure

```yaml
id: TC-020
verb: Measure
status: candidate
version: 0.3.0
signatures:
- legacy_name: Measure Environment
  actor_description: sensing platform
  typed_complement: Environment
  capability_type: CT-02
  implements_capabilities:
  - PerceptionCapability
  - SamplingCapability
traceability:
  used_by_missions:
  - MC-007
  - MC-008
  - MC-009
  - MC-010
  - MC-066
  legacy_task_ids:
  - TCL-023
```

### TC-021 — Assess

```yaml
id: TC-021
verb: Assess
status: draft
version: 0.3.0
signatures:
- legacy_name: Assess Threat
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
  - MC-040
  - MC-041
  - MC-056
  - MC-062
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-024
```

### TC-022 — Correlate

```yaml
id: TC-022
verb: Correlate
status: candidate
version: 0.3.0
signatures:
- legacy_name: Correlate Observations
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
version: 0.3.0
signatures:
- legacy_name: Escort Unit
  actor_description: escort platform
  typed_complement: Unit
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - TargetFollowingCapability
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
  - MC-047
  legacy_task_ids:
  - TCL-027
```

### TC-024 — Screen

```yaml
id: TC-024
verb: Screen
status: candidate
version: 0.3.0
signatures:
- legacy_name: Screen Protected Force
  actor_description: screening unit/group
  typed_complement: Protected Force
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - TargetFollowingCapability
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
version: 0.3.0
signatures:
- legacy_name: Guard Object
  actor_description: guarding platform
  typed_complement: Object
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
  - StationKeepingCapability
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
  legacy_task_ids:
  - TCL-029
```

### TC-026 — Block

```yaml
id: TC-026
verb: Block
status: candidate
version: 0.3.0
signatures:
- legacy_name: Block Approach
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
  legacy_task_ids:
  - TCL-030
```

### TC-027 — Interpose

```yaml
id: TC-027
verb: Interpose
status: candidate
version: 0.3.0
signatures:
- legacy_name: Interpose
  actor_description: mobile platform
  typed_complement: context
  capability_type: CT-01
  implements_capabilities:
  - TargetFollowingCapability
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
version: 0.3.0
signatures:
- legacy_name: Defend Area
  actor_description: force/group
  typed_complement: Area
  capability_type: CT-04
  implements_capabilities:
  - ProtectionCapability
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
  - MC-031
  - MC-032
  - MC-033
  - MC-045
  - MC-047
  - MC-050
  legacy_task_ids:
  - TCL-032
```

### TC-029 — Evade

```yaml
id: TC-029
verb: Evade
status: candidate
version: 0.3.0
signatures:
- legacy_name: Evade Threat
  actor_description: mobile platform
  typed_complement: Threat
  capability_type: CT-01
  implements_capabilities:
  - MobilityCapability
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
version: 0.3.0
signatures:
- legacy_name: Intercept Platform
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
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-034
```

### TC-031 — Hail

```yaml
id: TC-031
verb: Hail
status: candidate
version: 0.3.0
signatures:
- legacy_name: Hail Vessel
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
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-035
```

### TC-032 — Direct

```yaml
id: TC-032
verb: Direct
status: candidate
version: 0.3.0
signatures:
- legacy_name: Direct Vessel
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
version: 0.3.0
signatures:
- legacy_name: Compel Course Change
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
  legacy_task_ids:
  - TCL-037
```

### TC-034 — Board

```yaml
id: TC-034
verb: Board
status: candidate
version: 0.3.0
signatures:
- legacy_name: Board Vessel
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
  - MC-047
  - MC-050
  - MC-063
  - MC-064
  legacy_task_ids:
  - TCL-038
```

### TC-035 — Seize

```yaml
id: TC-035
verb: Seize
status: candidate
version: 0.3.0
signatures:
- legacy_name: Seize Object
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
  - MC-064
  legacy_task_ids:
  - TCL-040
```

### TC-036 — Engage

```yaml
id: TC-036
verb: Engage
status: candidate
version: 0.3.0
signatures:
- legacy_name: Engage Threat
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
  - MC-045
  legacy_task_ids:
  - TCL-041
```

### TC-037 — Neutralize

```yaml
id: TC-037
verb: Neutralize
status: candidate
version: 0.3.0
signatures:
- legacy_name: Neutralize Threat
  actor_description: authorized effector
  typed_complement: Threat
  capability_type: CT-05
  implements_capabilities:
  - NeutralizationCapability
- legacy_name: Neutralize Mine
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
version: 0.3.0
signatures:
- legacy_name: Deploy Mine
  actor_description: minelaying platform
  typed_complement: Mine
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
- legacy_name: Deploy Decoy
  actor_description: platform
  typed_complement: Decoy
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
- legacy_name: Deploy Payload
  actor_description: carrier platform
  typed_complement: Payload
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
traceability:
  used_by_missions:
  - MC-016
  - MC-033
  - MC-045
  - MC-050
  - MC-065
  - MC-066
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
version: 0.3.0
signatures:
- legacy_name: Report Information
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
version: 0.3.0
signatures:
- legacy_name: Share Track
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
  - MC-059
  legacy_task_ids:
  - TCL-047
```

### TC-041 — Request

```yaml
id: TC-041
verb: Request
status: candidate
version: 0.3.0
signatures:
- legacy_name: Request Support
  actor_description: actor/force
  typed_complement: Support
  capability_type: CT-10
  implements_capabilities:
  - CoordinationCapability
  - CommunicationCapability
traceability:
  used_by_missions: []
  legacy_task_ids:
  - TCL-048
```

### TC-042 — Assign

```yaml
id: TC-042
verb: Assign
status: candidate
version: 0.3.0
signatures:
- legacy_name: Assign Task
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
  - MC-040
  - MC-041
  legacy_task_ids:
  - TCL-049
```

### TC-043 — Coordinate

```yaml
id: TC-043
verb: Coordinate
status: candidate
version: 0.3.0
signatures:
- legacy_name: Coordinate Action
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
  - MC-039
  - MC-046
  - MC-048
  - MC-051
  - MC-054
  - MC-055
  - MC-060
  - MC-061
  - MC-065
  legacy_task_ids:
  - TCL-050
```

### TC-044 — Relay

```yaml
id: TC-044
verb: Relay
status: candidate
version: 0.3.0
signatures:
- legacy_name: Relay Communications
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
  - MC-060
  legacy_task_ids:
  - TCL-051
```

### TC-045 — Establish

```yaml
id: TC-045
verb: Establish
status: candidate
version: 0.3.0
signatures:
- legacy_name: Establish Communication Link
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
  - MC-045
  legacy_task_ids:
  - TCL-052
```

### TC-046 — Transmit

```yaml
id: TC-046
verb: Transmit
status: candidate
version: 0.3.0
signatures:
- legacy_name: Transmit Command
  actor_description: command actor
  typed_complement: Command
  capability_type: CT-09
  implements_capabilities:
  - CommunicationCapability
traceability:
  used_by_missions:
  - MC-043
  - MC-060
  legacy_task_ids:
  - TCL-054
```

### TC-047 — Update

```yaml
id: TC-047
verb: Update
status: candidate
version: 0.3.0
signatures:
- legacy_name: Update Mission Plan
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
  legacy_task_ids:
  - TCL-055
```

### TC-048 — Launch

```yaml
id: TC-048
verb: Launch
status: candidate
version: 0.3.0
signatures:
- legacy_name: Launch Platform
  actor_description: host/support platform
  typed_complement: Platform
  capability_type: CT-07
  implements_capabilities:
  - DeploymentCapability
  - PayloadHostingCapability
traceability:
  used_by_missions: []
  legacy_task_ids:
  - TCL-056
```

### TC-049 — Recover

```yaml
id: TC-049
verb: Recover
status: candidate
version: 0.3.0
signatures:
- legacy_name: Recover Platform
  actor_description: host/support platform
  typed_complement: Platform
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
- legacy_name: Recover Payload
  actor_description: carrier platform
  typed_complement: Payload
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
- legacy_name: Recover Personnel
  actor_description: recovery actor
  typed_complement: Personnel
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
traceability:
  used_by_missions:
  - MC-024
  - MC-049
  - MC-052
  - MC-053
  - MC-056
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
version: 0.3.0
signatures:
- legacy_name: Dock Platform
  actor_description: mobile platform/docking station
  typed_complement: Platform
  capability_type: CT-07
  implements_capabilities:
  - DockingCapability
traceability:
  used_by_missions: []
  legacy_task_ids:
  - TCL-058
```

### TC-051 — Transport

```yaml
id: TC-051
verb: Transport
status: candidate
version: 0.3.0
signatures:
- legacy_name: Transport Payload
  actor_description: transport platform
  typed_complement: Payload
  capability_type: CT-08
  implements_capabilities:
  - TransportCapability
traceability:
  used_by_missions:
  - MC-016
  - MC-023
  - MC-046
  - MC-050
  - MC-051
  - MC-052
  - MC-053
  - MC-054
  legacy_task_ids:
  - TCL-061
```

### TC-052 — Transfer

```yaml
id: TC-052
verb: Transfer
status: candidate
version: 0.3.0
signatures:
- legacy_name: Transfer Materiel
  actor_description: support actor
  typed_complement: Materiel
  capability_type: CT-08
  implements_capabilities:
  - LogisticsCapability
traceability:
  used_by_missions:
  - MC-023
  - MC-048
  - MC-055
  legacy_task_ids:
  - TCL-062
```

### TC-053 — Resupply

```yaml
id: TC-053
verb: Resupply
status: candidate
version: 0.3.0
signatures:
- legacy_name: Resupply Platform
  actor_description: support platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - LogisticsCapability
traceability:
  used_by_missions:
  - MC-032
  - MC-048
  - MC-055
  legacy_task_ids:
  - TCL-063
```

### TC-054 — Recharge

```yaml
id: TC-054
verb: Recharge
status: candidate
version: 0.3.0
signatures:
- legacy_name: Recharge Platform
  actor_description: energy source/host
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - EnergySupplyCapability
traceability:
  used_by_missions:
  - MC-055
  - MC-056
  legacy_task_ids:
  - TCL-064
```

### TC-055 — Refuel

```yaml
id: TC-055
verb: Refuel
status: candidate
version: 0.3.0
signatures:
- legacy_name: Refuel Platform
  actor_description: support platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - EnergySupplyCapability
traceability:
  used_by_missions:
  - MC-048
  - MC-055
  legacy_task_ids:
  - TCL-065
```

### TC-056 — Tow

```yaml
id: TC-056
verb: Tow
status: candidate
version: 0.3.0
signatures:
- legacy_name: Tow Platform
  actor_description: towing platform
  typed_complement: Platform
  capability_type: CT-08
  implements_capabilities:
  - TransportCapability
traceability:
  used_by_missions:
  - MC-056
  legacy_task_ids:
  - TCL-066
```

### TC-057 — Locate

```yaml
id: TC-057
verb: Locate
status: candidate
version: 0.3.0
signatures:
- legacy_name: Locate Missing Entity
  actor_description: search platform
  typed_complement: Missing Entity
  capability_type: CT-02
  implements_capabilities:
  - DetectionCapability
- legacy_name: Locate Emitter
  actor_description: sensing/processing actor
  typed_complement: Emitter
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
  - DetectionCapability
traceability:
  used_by_missions:
  - MC-011
  - MC-049
  - MC-053
  legacy_task_ids:
  - TCL-067
  - TCL-075
```

### TC-058 — Mark

```yaml
id: TC-058
verb: Mark
status: candidate
version: 0.3.0
signatures:
- legacy_name: Mark Location
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
  legacy_task_ids:
  - TCL-068
```

### TC-059 — Assist

```yaml
id: TC-059
verb: Assist
status: candidate
version: 0.3.0
signatures:
- legacy_name: Assist Distressed Platform
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
  - MC-046
  - MC-051
  - MC-052
  - MC-053
  - MC-056
  legacy_task_ids:
  - TCL-070
```

### TC-060 — Stabilize

```yaml
id: TC-060
verb: Stabilize
status: candidate
version: 0.3.0
signatures:
- legacy_name: Stabilize Casualty
  actor_description: medical actor
  typed_complement: Casualty
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
traceability:
  used_by_missions:
  - MC-049
  - MC-053
  legacy_task_ids:
  - TCL-071
```

### TC-061 — Evacuate

```yaml
id: TC-061
verb: Evacuate
status: candidate
version: 0.3.0
signatures:
- legacy_name: Evacuate Casualty
  actor_description: transport/recovery actor
  typed_complement: Casualty
  capability_type: CT-06
  implements_capabilities:
  - RecoveryCapability
  - TransportCapability
traceability:
  used_by_missions:
  - MC-049
  legacy_task_ids:
  - TCL-072
```

### TC-062 — Monitor

```yaml
id: TC-062
verb: Monitor
status: candidate
version: 0.3.0
signatures:
- legacy_name: Monitor Spectrum
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
  - MC-062
  - MC-065
  - MC-066
  legacy_task_ids:
  - TCL-076
```

### TC-063 — Jam

```yaml
id: TC-063
verb: Jam
status: candidate
version: 0.3.0
signatures:
- legacy_name: Jam Communication
  actor_description: authorized EW actor
  typed_complement: Communication
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
- legacy_name: Jam Sensor
  actor_description: authorized EW actor
  typed_complement: Sensor
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
traceability:
  used_by_missions:
  - MC-025
  - MC-028
  - MC-057
  - MC-061
  legacy_task_ids:
  - TCL-077
  - TCL-078
```

### TC-064 — Emit

```yaml
id: TC-064
verb: Emit
status: candidate
version: 0.3.0
signatures:
- legacy_name: Emit Deceptive Signal
  actor_description: EW/decoy actor
  typed_complement: Deceptive Signal
  capability_type: CT-11
  implements_capabilities:
  - ElectronicWarfareCapability
traceability:
  used_by_missions:
  - MC-057
  - MC-061
  legacy_task_ids:
  - TCL-079
```

## 7. Boundary rules

- Actor types, physical arguments and capabilities reference the Naval Ontology.
- Each signature references the most specific applicable ontology Capability class — never a generic ancestor when a specific class exists.
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

## 9. Changes 0.3.1 → 0.3.2

- Regenerated `used_by_missions` from the Mission Catalog v0.5.0, including the completed Mine Warfare family MC-012 to MC-017.
- No task identity or signature semantics changed.

## 10. Open points

- **Fate of the Capability Type layer (CT-01…CT-11):** now that signatures reference fine-grained ontology classes, the CT layer is derivable from the ontology hierarchy and does not superpose cleanly onto it (CT-04/05/06/07 all fall under `InteractionCapability`; CT-03 and CT-10 sit under `SupportCapability`). Decision pending: keep as editorial grouping, or drop in favour of the ontology hierarchy.
- **Target localization:** `nmo:LocalizationCapability` denotes platform self-localization (subclass of `NavigationCapability`). No ontology class covers *target* localization; `Localize Object` and Mission Catalog MT-02 baselines currently fall back to `DetectionCapability`/`PerceptionCapability`. Candidate ontology addition: `TargetLocalizationCapability` under `PerceptionCapability`.
- Continue regenerating `used_by_missions` from Mission Catalog `task_candidates` after each mission-family consolidation; do not maintain the reverse links manually.


## Changes 0.3.3 → 0.3.4

- Recomputed `used_by_missions` after completion of MC-028 through MC-033.
