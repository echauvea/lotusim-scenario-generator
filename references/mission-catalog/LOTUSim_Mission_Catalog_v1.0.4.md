# LOTUSim Mission Catalog

> **Status:** working draft
> **Version:** 1.0.4
> **Date:** 2026-07-14
> **Scope:** military maritime missions supported or considered by LOTUSim.

## 1. Purpose

The Mission Catalog is the authoritative inventory of reusable military mission specifications supported or considered by LOTUSim.

It defines:

- the mission classification;
- the controlled operational intents and mission targets;
- the machine-readable structure of a mission entry;
- the catalog of mission specifications.

Platform instances, operational roles, scenario parameters, events, task ordering and planning methods are outside the scope of this catalog.

## 2. Mission meta-model

A LOTUSim mission is a reusable specification of an operational objective.

Each mission contains four blocks:

```text
Mission
├── Identity
├── Classification
├── Operational specification
└── Traceability
```

### 2.1 Identity

- `id`: stable identifier of the form `MC-NNN`;
- `name`: canonical English display name;
- `status`: `candidate`, `draft`, `validated`, `deprecated`;
- `version`: semantic version of the mission entry.

### 2.2 Classification

- `mission_type`: one primary operational-effect class;
- `primary_family`: one primary doctrinal family;
- `operational_intent`: controlled verb representing the intended operational effect;
- `mission_target`: abstract target on which the mission acts.

### 2.3 Operational specification

- `purpose`;
- `description`;
- `applicable_contexts`;
- `preconditions`;
- `desired_end_state`;
- `success_criteria`;
- `failure_criteria`;
- `required_capabilities`, expressed as Naval Ontology Capability references.

### 2.4 Traceability

- `ontology_concepts`: physical-world concepts required from the Naval Ontology;
- `task_candidates`: optional informative references to Task Catalog verbs; these references are non-prescriptive;
- `related_missions`: optional typed references to other missions.

The catalog does not define role assignments, force composition, task ordering or scenario-specific parameter values.

## 3. Controlled classification

### 3.1 Mission types

Mission Types classify missions by their principal operational effect. They are distinct from Operational Intents, which provide the canonical verb used to express a mission.

| ID | Mission Type | Principal effect |
|---|---|---|
| MT-01 | Situational Awareness | Acquire and maintain operational understanding through patrol, surveillance, monitoring and reconnaissance. |
| MT-02 | Search | Locate missing, concealed or otherwise non-localized entities or objects. |
| MT-03 | Survey | Systematically characterize an area, route, infrastructure or physical environment. |
| MT-04 | Protection | Preserve a platform, group, infrastructure, area, route or service against threats or harmful effects. |
| MT-05 | Interdiction and Control | Prevent, constrain, stop or regulate an activity, movement, access or use. |
| MT-06 | Neutralization and Strike | Apply effects intended to disable, neutralize or destroy a designated threat or target. |
| MT-07 | Recovery | Retrieve personnel, platforms or objects and restore them to a designated safe or usable condition. |
| MT-08 | Sustainment | Maintain the endurance, availability, connectivity or logistical support of a force. |
| MT-09 | Operational Enablement | Enable or directly support another military operation without owning its principal operational effect. |

The Mission Type is mandatory and singular. Secondary contributions to other effects may be expressed later through optional tags, but do not change the primary Mission Type.

### 3.2 Capability requirements

A mission specifies the capabilities required to achieve its objective. It does not prescribe the tasks or their ordering.

Capabilities are defined in the Naval Ontology and implemented through Task Catalog verbs.

Each mission separates:

- `mandatory`: capabilities required in every valid instance of the mission;
- `optional`: capabilities required only for particular variants, threats or execution choices.

### 3.3 Mission families

1. ISR and Operational Environment Preparation
2. Mine Warfare
3. Maritime Security and Interdiction
4. Protection and Defence
5. Maritime Combat Operations
6. Littoral and Amphibious Support
7. Sustainment and Force Support
8. Electromagnetic and Information Activities
9. Personnel Recovery and Emergency Support

### 3.4 Operational intents

| Identifier | Meaning |
|---|---|
| `conduct` | Perform a complete recognized military activity. |
| `protect` | Preserve an entity, group, area or infrastructure against threats. |
| `escort` | Accompany and provide mobile protection to an entity or group. |
| `search` | Locate one or more entities or objects in a defined search space. |
| `survey` | Systematically characterize an area, route, infrastructure or physical environment. |
| `monitor` | Maintain observation over time and detect relevant changes. |
| `interdict` | Prevent, stop or control an activity, movement or entity. |
| `recover` | Retrieve personnel, platforms, payloads or physical objects. |
| `support` | Contribute to another operation without owning its principal effect. |
| `provide` | Supply an operational service or enabling function. |

Elementary actions such as `detect`, `classify`, `identify`, `track`, `navigate` and `report` belong to the Task Catalog.

### 3.5 Mission targets

| Target | Description | Primary model reference |
|---|---|---|
| `platform` | An individual platform designated as the target of the mission. | Naval Ontology: `Platform`; role defined in the Scenario Model. |
| `platform-group` | A group of platforms treated as a single operational aggregate. | Naval Ontology: `PlatformGroup`; operational kind defined in the Scenario Model. |
| `infrastructure` | A fixed or semi-fixed physical installation. | Naval Ontology: `Infrastructure`. |
| `area` | A spatial area designated for operational action. | Naval Ontology: `SpatialRegion`; operational role defined in the Scenario Model. |
| `route` | An ordered spatial path. | Naval Ontology: `Route`. |
| `corridor` | A bounded spatial passage. | Naval Ontology: `Corridor`. |
| `physical-object` | A mine, payload, materiel, decoy or other physical object. | Naval Ontology: `PhysicalObject`. |
| `personnel` | One or more persons. | Naval Ontology: `Person` / `PersonnelGroup`. |
| `communication-service` | A communication service or technical network to protect, disrupt or provide. | Naval Ontology and Scenario Model. |
| `maritime-activity` | An operational activity or traffic flow. | Scenario Model. |

## 4. Machine-readable mission schema

Canonical source format: YAML validated by JSON Schema.

```yaml
id: MC-001
name: Conduct Maritime Patrol
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: maritime-security-and-interdiction
  operational_intent: conduct
  mission_target: area

specification:
  purpose: ...
  description: ...
  applicable_contexts: []
  preconditions: []
  desired_end_state: ...
  success_criteria: []
  failure_criteria: []

required_capabilities:
  mandatory: []
  optional: []

traceability:
  task_candidates: []
  ontology_concepts: []
  related_missions: []
```

## 5. Mission inventory

### 5.1 ISR and Operational Environment Preparation

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-001 | Conduct Maritime Patrol | MT-01 | `conduct` | maritime area | `draft` |
| MC-002 | Establish Persistent Maritime Surveillance | MT-01 | `monitor` | maritime area | `draft` |
| MC-003 | Conduct Maritime Reconnaissance | MT-01 | `conduct` | maritime area | `draft` |
| MC-004 | Conduct Route Reconnaissance | MT-01 | `conduct` | route / corridor | `draft` |
| MC-005 | Conduct Harbour Reconnaissance | MT-01 | `conduct` | harbour area | `draft` |
| MC-006 | Conduct Infrastructure Reconnaissance | MT-01 | `conduct` | maritime infrastructure | `draft` |
| MC-007 | Survey Maritime Area | MT-03 | `survey` | spatial region | `draft` |
| MC-008 | Survey Transit Route | MT-03 | `survey` | route / corridor | `draft` |
| MC-009 | Conduct Hydrographic Survey | MT-03 | `conduct` | water column / seabed / region | `draft` |
| MC-010 | Survey Seabed | MT-03 | `survey` | seabed | `draft` |
| MC-011 | Search for Underwater Object | MT-02 | `search` | underwater object | `draft` |

### 5.2 Mine Warfare

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-012 | Conduct Mine Reconnaissance | MT-02 | `conduct` | area / route / naval mines | `draft` |
| MC-013 | Conduct Minehunting | MT-02 | `search` | naval mines | `draft` |
| MC-014 | Conduct Mine Clearance | MT-06 | `conduct` | mined area / route | `draft` |
| MC-015 | Verify Mine Clearance | MT-03 | `conduct` | cleared area / route | `draft` |
| MC-016 | Lay Minefield | MT-05 | `conduct` | minefield area | `draft` |
| MC-017 | Monitor Minefield | MT-01 | `monitor` | minefield | `draft` |

### 5.3 Maritime Security and Interdiction

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-018 | Monitor Maritime Traffic | MT-01 | `monitor` | maritime traffic | `draft` |
| MC-019 | Interdict Suspect Vessel | MT-05 | `interdict` | designated vessel | `draft` |
| MC-020 | Conduct Maritime Interdiction | MT-05 | `conduct` | vessels / maritime activity | `draft` |
| MC-021 | Enforce Maritime Exclusion Zone | MT-05 | `interdict` | maritime area / traffic | `draft` |
| MC-022 | Enforce Maritime Embargo | MT-05 | `interdict` | maritime traffic / cargo | `draft` |
| MC-023 | Support Visit, Board, Search and Seizure | MT-09 | `support` | suspect vessel / boarding force | `draft` |
| MC-024 | Counter Piracy | MT-05 | `conduct` | hostile maritime activity | `draft` |
| MC-025 | Counter Maritime Terrorism | MT-05 | `conduct` | hostile maritime activity | `draft` |

### 5.4 Protection and Defence

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-026 | Escort High-Value Unit | MT-04 | `escort` | high-value unit | `draft` |
| MC-027 | Escort Convoy | MT-04 | `escort` | convoy | `draft` |
| MC-028 | Protect Maritime Task Group | MT-04 | `protect` | maritime task group | `draft` |
| MC-029 | Protect Maritime Critical Infrastructure | MT-04 | `protect` | maritime infrastructure | `draft` |
| MC-030 | Protect Harbour or Naval Base | MT-04 | `protect` | harbour / naval base | `draft` |
| MC-031 | Protect Maritime Transit Corridor | MT-04 | `protect` | corridor | `draft` |
| MC-032 | Protect Sea Line of Communication | MT-04 | `protect` | maritime route network | `draft` |
| MC-033 | Establish Protective Screen | MT-04 | `conduct` | protected force / area | `draft` |

### 5.5 Maritime Combat Operations

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-034 | Conduct Anti-Surface Patrol | MT-01 | `conduct` | surface-threat area | `candidate` |
| MC-035 | Neutralize Surface Threat | MT-06 | `conduct` | hostile surface platform | `candidate` |
| MC-036 | Conduct Anti-Submarine Patrol | MT-01 | `conduct` | submarine-threat area | `candidate` |
| MC-037 | Neutralize Submarine Threat | MT-06 | `conduct` | hostile underwater platform | `candidate` |
| MC-038 | Defend Task Group Against Air Threat | MT-04 | `protect` | maritime task group | `candidate` |
| MC-039 | Conduct Maritime Strike | MT-06 | `conduct` | designated military target | `candidate` |
| MC-040 | Deny Access to Maritime Area | MT-05 | `interdict` | adversary force / maritime area | `candidate` |
| MC-041 | Support Joint Fires | MT-09 | `support` | joint targeting / fire mission | `candidate` |

### 5.6 Littoral and Amphibious Support

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-042 | Reconnoitre Landing Area | MT-01 | `conduct` | landing area | `candidate` |
| MC-043 | Survey Littoral Access Route | MT-03 | `survey` | littoral route | `candidate` |
| MC-044 | Support Amphibious Operations | MT-09 | `support` | amphibious force / landing area | `candidate` |
| MC-045 | Support Special Operations | MT-09 | `support` | special operations force / objective area | `candidate` |
| MC-046 | Secure Littoral Access Corridor | MT-04 | `protect` | littoral corridor | `candidate` |

### 5.7 Sustainment and Force Support

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-047 | Resupply Maritime Force | MT-08 | `provide` | maritime force | `candidate` |
| MC-048 | Transport Military Payload | MT-08 | `provide` | payload / destination | `candidate` |
| MC-049 | Deliver Critical Materiel | MT-08 | `provide` | materiel / receiving force | `candidate` |
| MC-050 | Provide Communication Relay | MT-08 | `provide` | communication service | `candidate` |
| MC-051 | Provide Navigation Support | MT-08 | `provide` | force / route | `candidate` |
| MC-052 | Deploy Uncrewed Systems | MT-09 | `support` | uncrewed platforms | `candidate` |
| MC-053 | Recover Uncrewed System | MT-07 | `recover` | uncrewed platform | `candidate` |

### 5.8 Electromagnetic and Information Activities

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-054 | Conduct Electronic Surveillance | MT-01 | `conduct` | electromagnetic environment | `candidate` |
| MC-055 | Conduct Electronic Attack | MT-06 | `conduct` | adversary emitter / network | `candidate` |
| MC-056 | Protect Friendly Communications | MT-04 | `protect` | friendly communication service | `candidate` |
| MC-057 | Disrupt Adversary Communications | MT-05 | `interdict` | adversary communication service | `candidate` |
| MC-058 | Conduct Maritime Deception | MT-09 | `conduct` | adversary decision process | `candidate` |
| MC-059 | Deploy Decoy | MT-04 | `support` | decoy / protected force | `candidate` |

### 5.9 Personnel Recovery and Emergency Support

| ID | Mission | Mission Type | Intent | Mission target | Status |
|---|---|---|---|---|---|
| MC-060 | Search for Missing Personnel | MT-02 | `search` | personnel | `candidate` |
| MC-061 | Recover Personnel | MT-07 | `recover` | personnel | `candidate` |
| MC-062 | Support Combat Search and Rescue | MT-09 | `support` | recovery force / isolated personnel | `candidate` |
| MC-063 | Search for Missing Platform | MT-02 | `search` | platform | `candidate` |
| MC-064 | Recover Distressed Vessel | MT-07 | `recover` | vessel | `candidate` |
| MC-065 | Assist Disabled Military Vessel | MT-08 | `support` | disabled vessel | `candidate` |
| MC-066 | Support Casualty Evacuation | MT-07 | `support` | casualty / medical force | `candidate` |

## 6. Default capability profiles by Mission Type

| Mission Type | Mandatory capability baseline | Typical optional capabilities |
|---|---|---|
| MT-01 | MobilityCapability, PerceptionCapability, CommunicationCapability | TrackingCapability, IdentificationCapability, AssessmentCapability |
| MT-02 | MobilityCapability, DetectionCapability, LocalizationCapability | ClassificationCapability, IdentificationCapability, CommunicationCapability |
| MT-03 | MobilityCapability, SurveyCapability, PerceptionCapability | InspectionCapability, CommunicationCapability |
| MT-04 | MobilityCapability, ProtectionCapability, PerceptionCapability, CommunicationCapability | TrackingCapability, ThreatAssessmentCapability, InterdictionCapability |
| MT-05 | InterdictionCapability, MobilityCapability, CommunicationCapability | PerceptionCapability, EngagementCapability, CoordinationCapability |
| MT-06 | EngagementCapability, PerceptionCapability | TrackingCapability, NeutralizationCapability, CoordinationCapability |
| MT-07 | RecoveryCapability, MobilityCapability | DetectionCapability, LocalizationCapability, TransportCapability, CommunicationCapability |
| MT-08 | SupportCapability | TransportCapability, LogisticsCapability, CommunicationCapability, RelayCapability |
| MT-09 | SupportCapability, CoordinationCapability | MobilityCapability, PerceptionCapability, CommunicationCapability |

These profiles are defaults for candidate missions. A detailed mission specification may refine them but must justify any removal of a mandatory baseline capability.

## 7. Detailed mission specifications

This version details the complete ISR and Operational Environment Preparation, Mine Warfare, and Maritime Security and Interdiction families, together with the previously consolidated escort missions.

### MC-001 — Conduct Maritime Patrol

```yaml
id: MC-001
name: Conduct Maritime Patrol
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Maintain maritime situational awareness and contribute to maritime security within a designated maritime area.
  description: >
    Conduct a patrol within a designated maritime area to observe activity, detect relevant contacts and report significant events.
  applicable_contexts:
    - maritime-security
    - exclusive-economic-zone-surveillance
    - harbour-protection
    - critical-infrastructure-protection
    - counter-piracy
  preconditions:
    - patrol-area-defined
    - at-least-one-platform-assigned
    - patrol-objectives-defined
  desired_end_state: >
    The designated maritime area has been patrolled and relevant activity has been reported.
  success_criteria:
    - required-area-coverage-achieved
    - significant-contacts-reported
    - mission-objectives-achieved
  failure_criteria:
    - mission-aborted
    - required-area-coverage-not-achieved
    - no-assigned-platform-capable-of-continuing

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - IdentificationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: may-contribute-to
      mission: MC-018
    - relation: may-support
      mission: MC-021
```


### MC-002 — Establish Persistent Maritime Surveillance

```yaml
id: MC-002
name: Establish Persistent Maritime Surveillance
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: monitor
  mission_target: area

specification:
  purpose: >
    Maintain continuous or recurrent observation of a designated maritime area over a specified period.
  description: >
    Establish a surveillance posture that provides sustained detection, tracking and reporting of relevant activity within a designated maritime area while managing platform endurance and coverage continuity.
  applicable_contexts:
    - maritime-domain-awareness
    - harbour-and-approach-surveillance
    - critical-infrastructure-protection
    - sea-line-of-communication-monitoring
    - pre-operation-intelligence-preparation
  preconditions:
    - surveillance-area-defined
    - surveillance-duration-or-persistence-objective-defined
    - relevant-contact-criteria-defined
    - sufficient-surveillance-assets-or-relief-plan-available
  desired_end_state: >
    The designated area has remained under the required level of observation and relevant changes or contacts have been detected, maintained and reported.
  success_criteria:
    - required-surveillance-continuity-achieved
    - required-area-coverage-maintained
    - relevant-events-and-contacts-reported
  failure_criteria:
    - surveillance-gap-exceeds-acceptable-threshold
    - required-area-coverage-not-maintained
    - no-assigned-platform-capable-of-continuing

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - CommunicationCapability
    - StationKeepingCapability
  optional:
    - MobilityCapability
    - IdentificationCapability
    - AssessmentCapability
    - RelayCapability

traceability:
  task_candidates:
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-039
    - TC-040
    - TC-044
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: specialization-of
      mission: MC-001
    - relation: may-contribute-to
      mission: MC-018
```

### MC-003 — Conduct Maritime Reconnaissance

```yaml
id: MC-003
name: Conduct Maritime Reconnaissance
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Obtain time-bounded information about maritime forces, activities and environmental conditions in a designated area.
  description: >
    Collect, correlate and report observations in a designated maritime area to reduce uncertainty and support operational planning or execution.
  applicable_contexts:
    - intelligence-preparation
    - pre-transit-assessment
    - force-disposition-assessment
    - threat-assessment
    - operational-environment-preparation
  preconditions:
    - reconnaissance-area-defined
    - information-requirements-defined
    - reconnaissance-window-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The specified information requirements have been addressed and the resulting reconnaissance information has been reported.
  success_criteria:
    - required-area-observed
    - priority-information-requirements-addressed
    - reconnaissance-report-delivered
  failure_criteria:
    - priority-information-requirements-not-addressed
    - reconnaissance-window-missed
    - mission-aborted

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
    - AssessmentCapability
  optional:
    - TrackingCapability
    - IdentificationCapability
    - DataProcessingCapability
    - RelayCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-011
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-021
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
    - Infrastructure
  related_missions:
    - relation: related-to
      mission: MC-007
    - relation: may-support
      mission: MC-026
```

### MC-004 — Conduct Route Reconnaissance

```yaml
id: MC-004
name: Conduct Route Reconnaissance
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: route

specification:
  purpose: >
    Assess a designated route or corridor to identify conditions, hazards, activity and threats relevant to subsequent transit.
  description: >
    Observe and characterize a route and its approaches before or during an operation, with emphasis on navigability, threat indicators and significant changes.
  applicable_contexts:
    - pre-transit-reconnaissance
    - convoy-preparation
    - amphibious-approach-preparation
    - mine-threat-assessment
    - contested-navigation
  preconditions:
    - route-or-corridor-defined
    - reconnaissance-requirements-defined
    - acceptable-observation-window-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The designated route has been assessed and relevant hazards, activity and threat indicators have been reported.
  success_criteria:
    - required-route-segments-observed
    - relevant-hazards-and-contacts-reported
    - route-assessment-delivered
  failure_criteria:
    - critical-route-segment-not-observed
    - route-assessment-not-delivered-before-required-time
    - mission-aborted

required_capabilities:
  mandatory:
    - RouteFollowingCapability
    - PerceptionCapability
    - CommunicationCapability
    - AssessmentCapability
  optional:
    - DetectionCapability
    - IdentificationCapability
    - SurveyCapability
    - TrackingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-010
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-017
    - TC-021
    - TC-039
  ontology_concepts:
    - Platform
    - Route
    - Corridor
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: precedes
      mission: MC-008
    - relation: may-support
      mission: MC-027
```

### MC-005 — Conduct Harbour Reconnaissance

```yaml
id: MC-005
name: Conduct Harbour Reconnaissance
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Obtain operationally relevant information about a harbour, its approaches, facilities, traffic and potential threats.
  description: >
    Observe and characterize a harbour area and its approaches to support access planning, protection, interdiction or other maritime operations.
  applicable_contexts:
    - harbour-approach-assessment
    - port-security
    - force-entry-preparation
    - critical-infrastructure-protection
    - maritime-interdiction-preparation
  preconditions:
    - harbour-area-and-approaches-defined
    - information-requirements-defined
    - relevant-infrastructure-and-traffic-categories-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The harbour and its approaches have been characterized to the required level and significant infrastructure, traffic and threat information has been reported.
  success_criteria:
    - required-harbour-sectors-observed
    - relevant-infrastructure-and-activity-characterized
    - harbour-reconnaissance-report-delivered
  failure_criteria:
    - critical-harbour-sector-not-observed
    - priority-information-requirements-not-addressed
    - mission-aborted

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
    - AssessmentCapability
  optional:
    - IdentificationCapability
    - TrackingCapability
    - InspectionCapability
    - SurveyCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-018
    - TC-021
    - TC-039
  ontology_concepts:
    - Platform
    - Infrastructure
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: related-to
      mission: MC-006
    - relation: may-support
      mission: MC-021
```

### MC-006 — Conduct Infrastructure Reconnaissance

```yaml
id: MC-006
name: Conduct Infrastructure Reconnaissance
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: infrastructure

specification:
  purpose: >
    Obtain operationally relevant information about designated maritime or coastal infrastructure and its immediate environment.
  description: >
    Observe, inspect and characterize designated infrastructure to establish its condition, configuration, activity and exposure to threats or hazards.
  applicable_contexts:
    - critical-undersea-infrastructure-assessment
    - port-facility-assessment
    - offshore-installation-protection
    - damage-assessment
    - operational-environment-preparation
  preconditions:
    - infrastructure-designated
    - inspection-or-information-requirements-defined
    - access-or-observation-area-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The designated infrastructure has been characterized to the required level and relevant findings have been reported.
  success_criteria:
    - required-infrastructure-elements-observed
    - required-characteristics-assessed
    - infrastructure-reconnaissance-report-delivered
  failure_criteria:
    - critical-infrastructure-element-not-observed
    - required-assessment-not-produced
    - mission-aborted

required_capabilities:
  mandatory:
    - PerceptionCapability
    - InspectionCapability
    - AssessmentCapability
    - CommunicationCapability
  optional:
    - MobilityCapability
    - SurveyCapability
    - IdentificationCapability
    - StationKeepingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-017
    - TC-018
    - TC-021
    - TC-039
  ontology_concepts:
    - Platform
    - Infrastructure
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: related-to
      mission: MC-005
    - relation: may-support
      mission: MC-030
```

### MC-007 — Survey Maritime Area

```yaml
id: MC-007
name: Survey Maritime Area
status: draft
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: isr-and-operational-environment-preparation
  operational_intent: survey
  mission_target: area

specification:
  purpose: >
    Systematically characterize selected properties of a designated maritime area.
  description: >
    Execute a structured coverage pattern to collect measurements and observations across a designated area and produce a spatially referenced characterization.
  applicable_contexts:
    - environmental-characterization
    - operational-environment-preparation
    - change-detection-baseline
    - sensor-performance-assessment
    - mission-planning-support
  preconditions:
    - survey-area-defined
    - survey-parameters-and-resolution-defined
    - required-coverage-level-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The designated area has been surveyed to the required coverage and resolution and the resulting data has been reported or made available.
  success_criteria:
    - required-area-coverage-achieved
    - required-measurements-collected
    - survey-product-generated
  failure_criteria:
    - coverage-below-required-threshold
    - required-data-quality-not-achieved
    - mission-aborted

required_capabilities:
  mandatory:
    - SurveyCapability
    - MobilityCapability
    - PerceptionCapability
    - DataProcessingCapability
  optional:
    - CommunicationCapability
    - SamplingCapability
    - StationKeepingCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-005
    - TC-019
    - TC-020
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: related-to
      mission: MC-003
    - relation: parent-of
      mission: MC-009
    - relation: parent-of
      mission: MC-010
```

### MC-008 — Survey Transit Route

```yaml
id: MC-008
name: Survey Transit Route
status: draft
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: isr-and-operational-environment-preparation
  operational_intent: survey
  mission_target: route

specification:
  purpose: >
    Systematically characterize a designated transit route or corridor for subsequent navigation and operational use.
  description: >
    Collect spatially referenced measurements and observations along a route and its relevant margins to assess navigability, environmental conditions and physical hazards.
  applicable_contexts:
    - route-preparation
    - convoy-transit-support
    - autonomous-navigation-preparation
    - amphibious-approach-support
    - mine-countermeasure-support
  preconditions:
    - route-or-corridor-defined
    - survey-width-resolution-and-parameters-defined
    - required-data-quality-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The designated route has been surveyed to the required extent and a usable route characterization has been produced.
  success_criteria:
    - required-route-coverage-achieved
    - required-measurements-collected
    - route-survey-product-generated
  failure_criteria:
    - critical-route-segment-not-surveyed
    - required-data-quality-not-achieved
    - mission-aborted

required_capabilities:
  mandatory:
    - RouteFollowingCapability
    - SurveyCapability
    - PerceptionCapability
    - DataProcessingCapability
  optional:
    - CommunicationCapability
    - DetectionCapability
    - SamplingCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-010
    - TC-012
    - TC-019
    - TC-020
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - Route
    - Corridor
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: follows
      mission: MC-004
    - relation: may-support
      mission: MC-027
```

### MC-009 — Conduct Hydrographic Survey

```yaml
id: MC-009
name: Conduct Hydrographic Survey
status: draft
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: isr-and-operational-environment-preparation
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Characterize hydrographic conditions relevant to safe navigation and maritime operations in a designated area.
  description: >
    Collect and process bathymetric, water-column and related environmental measurements to produce hydrographic information at the required coverage, resolution and quality.
  applicable_contexts:
    - navigation-safety
    - littoral-operation-preparation
    - amphibious-operation-support
    - harbour-and-approach-survey
    - autonomous-navigation-support
  preconditions:
    - hydrographic-survey-area-defined
    - required-parameters-resolution-and-accuracy-defined
    - reference-frame-and-data-quality-rules-defined
    - at-least-one-suitable-survey-platform-assigned
  desired_end_state: >
    The required hydrographic information has been collected, quality-controlled and delivered for the designated area.
  success_criteria:
    - required-hydrographic-coverage-achieved
    - required-measurement-quality-achieved
    - hydrographic-product-generated
  failure_criteria:
    - coverage-below-required-threshold
    - measurement-quality-below-required-threshold
    - hydrographic-product-not-generated

required_capabilities:
  mandatory:
    - SurveyCapability
    - SamplingCapability
    - MobilityCapability
    - DataProcessingCapability
  optional:
    - StationKeepingCapability
    - CommunicationCapability
    - PerceptionCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-005
    - TC-019
    - TC-020
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: specialization-of
      mission: MC-007
    - relation: related-to
      mission: MC-010
```

### MC-010 — Survey Seabed

```yaml
id: MC-010
name: Survey Seabed
status: draft
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: isr-and-operational-environment-preparation
  operational_intent: survey
  mission_target: area

specification:
  purpose: >
    Systematically characterize the seabed within a designated area and identify relevant features, anomalies or objects.
  description: >
    Execute a seabed coverage pattern, collect suitable sensor data and produce a georeferenced representation of seabed morphology and relevant contacts.
  applicable_contexts:
    - seabed-mapping
    - critical-undersea-infrastructure-support
    - mine-countermeasure-preparation
    - environmental-baseline
    - underwater-object-search-preparation
  preconditions:
    - seabed-survey-area-defined
    - required-resolution-and-detection-threshold-defined
    - environmental-and-depth-constraints-assessed
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The designated seabed area has been surveyed to the required coverage and resolution and relevant features or anomalies have been reported.
  success_criteria:
    - required-seabed-coverage-achieved
    - required-resolution-achieved
    - seabed-map-and-contact-report-generated
  failure_criteria:
    - coverage-below-required-threshold
    - required-resolution-not-achieved
    - survey-product-not-generated

required_capabilities:
  mandatory:
    - SurveyCapability
    - PerceptionCapability
    - MobilityCapability
    - DataProcessingCapability
  optional:
    - DetectionCapability
    - ClassificationCapability
    - IdentificationCapability
    - CommunicationCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-012
    - TC-013
    - TC-014
    - TC-019
    - TC-020
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: specialization-of
      mission: MC-007
    - relation: may-precede
      mission: MC-011
```

### MC-011 — Search for Underwater Object

```yaml
id: MC-011
name: Search for Underwater Object
status: draft
version: 0.1.0

classification:
  mission_type: MT-02
  primary_family: isr-and-operational-environment-preparation
  operational_intent: search
  mission_target: physical-object

specification:
  purpose: >
    Locate and establish the position of one or more designated or characterized underwater objects within a defined search space.
  description: >
    Search a defined underwater area using suitable coverage and sensing techniques, investigate relevant contacts and report the location and confidence associated with candidate objects.
  applicable_contexts:
    - lost-object-search
    - wreck-or-debris-search
    - payload-recovery-preparation
    - critical-infrastructure-inspection-support
    - underwater-threat-search
  preconditions:
    - search-area-defined
    - sought-object-description-or-search-criteria-defined
    - search-termination-conditions-defined
    - at-least-one-suitable-platform-assigned
  desired_end_state: >
    The sought object has been located with the required confidence, or the defined search space has been covered to the required standard without detection.
  success_criteria:
    - object-located-or-search-space-cleared-to-required-standard
    - search-result-reported
  failure_criteria:
    - required-search-coverage-not-achieved
    - unresolved-contact-prevents-conclusion
    - mission-aborted

required_capabilities:
  mandatory:
    - DetectionCapability
    - LocalizationCapability
    - MobilityCapability
    - CommunicationCapability
  optional:
    - ClassificationCapability
    - IdentificationCapability
    - SurveyCapability
    - MarkingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-003
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-017
    - TC-039
    - TC-057
    - TC-058
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: may-follow
      mission: MC-010
    - relation: may-precede
      mission: MC-049
```


### MC-012 — Conduct Mine Reconnaissance

```yaml
id: MC-012
name: Conduct Mine Reconnaissance
status: draft
version: 0.1.0

classification:
  mission_type: MT-02
  primary_family: mine-warfare
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Determine the presence, distribution and characteristics of a mine threat in a designated area, route or corridor.
  description: >
    Search and investigate a designated operating space to detect mine-like contacts, localize relevant objects and produce an initial assessment of the mine threat without necessarily completing full minehunting or clearance.
  applicable_contexts:
    - mine-threat-assessment
    - route-preparation
    - harbour-approach-assessment
    - amphibious-operation-preparation
    - precursor-to-minehunting
  preconditions:
    - reconnaissance-area-route-or-corridor-defined
    - mine-threat-information-requirements-defined
    - required-search-coverage-and-confidence-defined
    - at-least-one-suitable-mcm-platform-assigned
  desired_end_state: >
    The designated space has been searched to the required standard and the presence, absence or likely distribution of mine threats has been assessed and reported.
  success_criteria:
    - required-search-coverage-achieved
    - relevant-mine-like-contacts-localized-and-reported
    - mine-threat-assessment-delivered
  failure_criteria:
    - required-search-coverage-not-achieved
    - critical-contacts-remain-unresolved
    - mine-threat-assessment-not-delivered

required_capabilities:
  mandatory:
    - DetectionCapability
    - MobilityCapability
    - AssessmentCapability
    - CommunicationCapability
  optional:
    - ClassificationCapability
    - IdentificationCapability
    - SurveyCapability
    - MarkingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-003
    - TC-004
    - TC-010
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-017
    - TC-021
    - TC-039
    - TC-058
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - Corridor
    - PhysicalObject
  related_missions:
    - relation: may-precede
      mission: MC-013
    - relation: may-support
      mission: MC-014
```

### MC-013 — Conduct Minehunting

```yaml
id: MC-013
name: Conduct Minehunting
status: draft
version: 0.1.0

classification:
  mission_type: MT-02
  primary_family: mine-warfare
  operational_intent: search
  mission_target: physical-object

specification:
  purpose: >
    Detect, localize, classify and identify naval mines or mine-like objects within a designated area, route or corridor.
  description: >
    Execute systematic search and contact investigation to establish a sufficiently reliable mine-contact picture for subsequent avoidance, neutralization or clearance decisions.
  applicable_contexts:
    - mine-countermeasure-operation
    - route-clearance-preparation
    - harbour-and-approach-clearance
    - amphibious-operation-support
    - post-reconnaissance-contact-investigation
  preconditions:
    - minehunting-area-route-or-corridor-defined
    - required-search-coverage-and-contact-confidence-defined
    - contact-investigation-rules-defined
    - at-least-one-suitable-minehunting-system-assigned
  desired_end_state: >
    The designated space has been searched to the required standard and relevant contacts have been localized and classified or identified with sufficient confidence for operational decision-making.
  success_criteria:
    - required-minehunting-coverage-achieved
    - relevant-contacts-investigated
    - mine-contact-picture-produced
  failure_criteria:
    - required-coverage-not-achieved
    - unacceptable-number-of-relevant-contacts-unresolved
    - mine-contact-picture-not-produced

required_capabilities:
  mandatory:
    - DetectionCapability
    - ClassificationCapability
    - MobilityCapability
    - DataProcessingCapability
  optional:
    - IdentificationCapability
    - MarkingCapability
    - CommunicationCapability
    - StationKeepingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-003
    - TC-004
    - TC-005
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-017
    - TC-022
    - TC-039
    - TC-058
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - Corridor
    - PhysicalObject
  related_missions:
    - relation: may-follow
      mission: MC-012
    - relation: may-precede
      mission: MC-014
```

### MC-014 — Conduct Mine Clearance

```yaml
id: MC-014
name: Conduct Mine Clearance
status: draft
version: 0.1.0

classification:
  mission_type: MT-06
  primary_family: mine-warfare
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Reduce a mine threat in a designated area, route or corridor to an acceptable residual-risk level.
  description: >
    Neutralize, remove, avoid or otherwise render ineffective confirmed or assessed mine threats according to authorized clearance criteria and operational constraints.
  applicable_contexts:
    - route-clearance
    - harbour-and-approach-clearance
    - amphibious-operation-support
    - sea-line-of-communication-restoration
    - post-minehunting-neutralization
  preconditions:
    - clearance-area-route-or-corridor-defined
    - acceptable-residual-risk-defined
    - mine-contact-or-threat-picture-available
    - neutralization-authority-and-safety-constraints-defined
    - at-least-one-suitable-clearance-system-assigned
  desired_end_state: >
    The designated space satisfies the specified clearance standard and the residual mine risk is assessed as acceptable for the intended use.
  success_criteria:
    - required-clearance-actions-completed
    - residual-risk-at-or-below-accepted-threshold
    - clearance-result-reported
  failure_criteria:
    - residual-risk-remains-above-accepted-threshold
    - required-clearance-actions-cannot-be-completed
    - unacceptable-collateral-or-safety-condition

required_capabilities:
  mandatory:
    - NeutralizationCapability
    - DetectionCapability
    - MobilityCapability
    - AssessmentCapability
  optional:
    - IdentificationCapability
    - MarkingCapability
    - ManipulationCapability
    - CommunicationCapability

traceability:
  task_candidates:
    - TC-001
    - TC-003
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-021
    - TC-037
    - TC-039
    - TC-058
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - Corridor
    - PhysicalObject
  related_missions:
    - relation: may-follow
      mission: MC-013
    - relation: may-precede
      mission: MC-015
```

### MC-015 — Verify Mine Clearance

```yaml
id: MC-015
name: Verify Mine Clearance
status: draft
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: mine-warfare
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Independently assess whether a designated area, route or corridor meets the required mine-clearance standard.
  description: >
    Re-survey and inspect the cleared space using defined verification coverage, confidence and independence criteria to estimate residual mine risk and confirm or reject clearance completion.
  applicable_contexts:
    - post-clearance-verification
    - route-certification
    - harbour-reopening
    - amphibious-lane-verification
    - quality-assurance-for-mcm
  preconditions:
    - claimed-cleared-space-defined
    - clearance-standard-and-verification-method-defined
    - prior-clearance-record-available
    - verification-platform-or-system-assigned
  desired_end_state: >
    An evidence-based determination has been produced stating whether the designated space meets the required clearance and residual-risk criteria.
  success_criteria:
    - required-verification-coverage-achieved
    - residual-risk-assessed
    - clearance-accepted-or-rejected-with-evidence
  failure_criteria:
    - required-verification-coverage-not-achieved
    - verification-confidence-below-required-threshold
    - clearance-determination-not-produced

required_capabilities:
  mandatory:
    - SurveyCapability
    - DetectionCapability
    - AssessmentCapability
    - DataProcessingCapability
  optional:
    - ClassificationCapability
    - IdentificationCapability
    - CommunicationCapability
    - MarkingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-010
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-017
    - TC-021
    - TC-022
    - TC-039
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - Corridor
    - PhysicalObject
  related_missions:
    - relation: may-follow
      mission: MC-014
    - relation: may-trigger
      mission: MC-014
```

### MC-016 — Lay Minefield

```yaml
id: MC-016
name: Lay Minefield
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: mine-warfare
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Establish a controlled minefield in a designated area to deny, constrain or channel maritime movement.
  description: >
    Transport and deploy authorized naval mines according to a defined minefield plan, placement constraints, safety rules and recording requirements.
  applicable_contexts:
    - area-denial
    - route-denial
    - defensive-barrier
    - channelization-of-maritime-movement
    - protection-of-maritime-approaches
  preconditions:
    - minefield-area-and-plan-defined
    - deployment-authority-confirmed
    - mine-payloads-available-and-compatible
    - safety-exclusion-and-recording-rules-defined
    - at-least-one-suitable-deployment-platform-assigned
  desired_end_state: >
    The authorized minefield has been deployed within the specified tolerances, recorded and placed under the required control or monitoring regime.
  success_criteria:
    - required-mines-deployed
    - deployment-pattern-within-defined-tolerances
    - minefield-record-produced
  failure_criteria:
    - required-deployment-pattern-not-achieved
    - unacceptable-placement-uncertainty
    - unauthorized-or-unsafe-deployment-condition

required_capabilities:
  mandatory:
    - DeploymentCapability
    - PayloadHostingCapability
    - MobilityCapability
    - CommunicationCapability
  optional:
    - WaypointNavigationCapability
    - StationKeepingCapability
    - TransportCapability
    - MarkingCapability

traceability:
  task_candidates:
    - TC-001
    - TC-005
    - TC-038
    - TC-039
    - TC-051
    - TC-058
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: may-precede
      mission: MC-017
    - relation: opposed-by
      mission: MC-014
```

### MC-017 — Monitor Minefield

```yaml
id: MC-017
name: Monitor Minefield
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: mine-warfare
  operational_intent: monitor
  mission_target: area

specification:
  purpose: >
    Maintain awareness of the condition, integrity and relevant activity associated with a designated minefield.
  description: >
    Observe the minefield and its approaches over time to detect unauthorized entry, displacement, degradation, tampering or other changes affecting its intended operational effect or safety.
  applicable_contexts:
    - defensive-minefield-control
    - minefield-integrity-monitoring
    - route-denial-enforcement
    - safety-monitoring
    - post-deployment-assessment
  preconditions:
    - minefield-boundary-and-record-available
    - monitoring-period-and-information-requirements-defined
    - relevant-change-and-alert-criteria-defined
    - at-least-one-suitable-monitoring-system-assigned
  desired_end_state: >
    Relevant activity and changes affecting the minefield have been detected, assessed and reported throughout the required monitoring period.
  success_criteria:
    - required-monitoring-coverage-maintained
    - relevant-activity-and-changes-detected
    - required-alerts-and-reports-delivered
  failure_criteria:
    - unacceptable-monitoring-gap
    - relevant-change-not-detected-or-reported
    - minefield-status-cannot-be-assessed

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - AssessmentCapability
    - CommunicationCapability
  optional:
    - StationKeepingCapability
    - IdentificationCapability
    - DetectionCapability
    - RelayCapability

traceability:
  task_candidates:
    - TC-002
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-021
    - TC-039
    - TC-040
    - TC-044
  ontology_concepts:
    - Platform
    - SpatialRegion
    - PhysicalObject
  related_missions:
    - relation: may-follow
      mission: MC-016
    - relation: may-support
      mission: MC-021
```


### MC-018 — Monitor Maritime Traffic

```yaml
id: MC-018
name: Monitor Maritime Traffic
status: draft
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: maritime-security-and-interdiction
  operational_intent: monitor
  mission_target: maritime-activity

specification:
  purpose: >
    Maintain an operational picture of maritime traffic in a designated area and identify activity requiring further assessment or action.
  description: >
    Observe, correlate and track maritime traffic over time, compare detected activity with expected patterns and report contacts, anomalies and significant changes.
  applicable_contexts:
    - maritime-domain-awareness
    - sea-lane-monitoring
    - harbour-and-approach-monitoring
    - embargo-or-exclusion-zone-support
    - counter-piracy-and-counter-terrorism
  preconditions:
    - monitoring-area-defined
    - traffic-of-interest-and-reporting-criteria-defined
    - observation-period-defined
    - at-least-one-suitable-surveillance-asset-assigned
  desired_end_state: >
    Maritime traffic in the designated area has been monitored to the required level and relevant contacts, anomalies and changes have been reported.
  success_criteria:
    - required-monitoring-coverage-achieved
    - relevant-traffic-detected-and-tracked
    - significant-anomalies-reported
  failure_criteria:
    - monitoring-gap-exceeds-acceptable-threshold
    - priority-traffic-not-detected-or-maintained
    - no-assigned-platform-capable-of-continuing

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - AssessmentCapability
    - CommunicationCapability
  optional:
    - MobilityCapability
    - ClassificationCapability
    - IdentificationCapability
    - DataProcessingCapability
    - RelayCapability

traceability:
  task_candidates:
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-022
    - TC-039
    - TC-040
    - TC-047
    - TC-062
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: supported-by
      mission: MC-001
    - relation: may-trigger
      mission: MC-019
    - relation: supports
      mission: MC-021
    - relation: supports
      mission: MC-022
```

### MC-019 — Interdict Suspect Vessel

```yaml
id: MC-019
name: Interdict Suspect Vessel
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: interdict
  mission_target: platform

specification:
  purpose: >
    Prevent or constrain a designated suspect vessel from continuing an unauthorized or threatening activity until it complies, is controlled or is transferred to an authorized force.
  description: >
    Locate and maintain contact with a designated vessel, establish communication, direct or compel it to comply with instructions and position forces to prevent escape or unsafe manoeuvre.
  applicable_contexts:
    - maritime-law-enforcement-support
    - embargo-enforcement
    - exclusion-zone-enforcement
    - counter-smuggling
    - counter-piracy
    - counter-terrorism
  preconditions:
    - suspect-vessel-designated-or-identification-criteria-defined
    - legal-or-operational-authority-defined
    - permitted-escalation-measures-defined
    - interdiction-force-assigned
  desired_end_state: >
    The suspect vessel has complied, has been stopped or constrained, or has been handed over without unacceptable harm to protected persons, forces or traffic.
  success_criteria:
    - suspect-vessel-positively-identified
    - continuous-contact-maintained-until-resolution
    - suspect-vessel-compliance-or-control-achieved
  failure_criteria:
    - suspect-vessel-escapes-designated-control-area
    - positive-identification-not-achieved
    - unacceptable-harm-caused
    - interdiction-force-unable-to-continue

required_capabilities:
  mandatory:
    - MobilityCapability
    - TrackingCapability
    - IdentificationCapability
    - CommunicationCapability
    - InterdictionCapability
    - CoordinationCapability
  optional:
    - ProtectionCapability
    - EngagementCapability
    - TargetFollowingCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-006
    - TC-007
    - TC-008
    - TC-016
    - TC-015
    - TC-021
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-039
    - TC-043
  ontology_concepts:
    - Platform
    - SpatialRegion
    - Route
    - Person
  related_missions:
    - relation: may-follow
      mission: MC-018
    - relation: may-enable
      mission: MC-023
    - relation: component-of
      mission: MC-020
```

### MC-020 — Conduct Maritime Interdiction

```yaml
id: MC-020
name: Conduct Maritime Interdiction
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: conduct
  mission_target: maritime-activity

specification:
  purpose: >
    Detect, deter, intercept and control vessels or maritime activities that violate designated operational, legal or security constraints.
  description: >
    Conduct a coordinated maritime interdiction operation across a designated area by monitoring traffic, identifying vessels of interest, intercepting selected contacts and applying authorized control measures.
  applicable_contexts:
    - maritime-security-operation
    - embargo-enforcement
    - counter-smuggling
    - counter-piracy
    - exclusion-zone-enforcement
    - protection-of-maritime-approaches
  preconditions:
    - interdiction-area-and-objectives-defined
    - vessels-or-activities-of-interest-criteria-defined
    - authority-and-rules-of-engagement-defined
    - command-and-coordination-arrangements-established
  desired_end_state: >
    Prohibited or threatening maritime activity in the designated area has been prevented, disrupted or brought under authorized control.
  success_criteria:
    - relevant-traffic-monitored
    - vessels-of-interest-detected-and-assessed
    - designated-interdictions-completed
    - operational-control-maintained
  failure_criteria:
    - priority-vessel-or-activity-not-interdicted
    - prohibited-activity-continues-beyond-accepted-threshold
    - coordination-breakdown-prevents-mission-execution
    - unacceptable-harm-caused

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - InterdictionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - MobilityCapability
    - InspectionCapability
    - ProtectionCapability
    - EngagementCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-002
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-034
    - TC-035
    - TC-039
    - TC-043
  ontology_concepts:
    - Platform
    - PlatformGroup
    - SpatialRegion
    - Route
    - PhysicalObject
    - Person
  related_missions:
    - relation: includes
      mission: MC-018
    - relation: includes
      mission: MC-019
    - relation: may-include
      mission: MC-023
    - relation: specialization-parent-of
      mission: MC-022
```

### MC-021 — Enforce Maritime Exclusion Zone

```yaml
id: MC-021
name: Enforce Maritime Exclusion Zone
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: interdict
  mission_target: area

specification:
  purpose: >
    Prevent unauthorized maritime platforms or activities from entering, remaining within or operating inside a designated exclusion zone.
  description: >
    Monitor the boundary and interior of a declared maritime exclusion zone, identify approaching or present contacts, issue warnings and directions, and apply authorized measures to deny or terminate unauthorized access.
  applicable_contexts:
    - force-protection
    - harbour-protection
    - critical-infrastructure-protection
    - amphibious-operation-support
    - hazardous-area-control
    - temporary-operational-zone-control
  preconditions:
    - exclusion-zone-boundary-defined
    - authorized-and-unauthorized-activity-criteria-defined
    - warning-and-escalation-procedures-defined
    - enforcement-assets-assigned
  desired_end_state: >
    Unauthorized platforms and activities are absent from the exclusion zone or are under effective control, while authorized traffic is managed safely.
  success_criteria:
    - zone-boundary-and-interior-monitored
    - unauthorized-entry-detected
    - unauthorized-contact-warned-or-interdicted
    - authorized-traffic-not-unacceptably-disrupted
  failure_criteria:
    - unauthorized-contact-enters-or-remains-uncontrolled
    - priority-contact-not-detected
    - zone-enforcement-capability-lost
    - unacceptable-interference-with-authorized-traffic

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - InterdictionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - MobilityCapability
    - ProtectionCapability
    - EngagementCapability
    - StationKeepingCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-002
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-025
    - TC-026
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-039
    - TC-043
    - TC-062
  ontology_concepts:
    - Platform
    - PlatformGroup
    - SpatialRegion
    - Route
  related_missions:
    - relation: supported-by
      mission: MC-018
    - relation: may-use
      mission: MC-019
    - relation: may-support
      mission: MC-028
```

### MC-022 — Enforce Maritime Embargo

```yaml
id: MC-022
name: Enforce Maritime Embargo
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: interdict
  mission_target: maritime-activity

specification:
  purpose: >
    Prevent prohibited vessels, cargoes, personnel or services from reaching or leaving a designated area in accordance with the applicable mandate.
  description: >
    Monitor relevant sea routes and maritime approaches, identify and assess vessels and cargo movements, intercept vessels of interest and support inspection, diversion or seizure when authorized.
  applicable_contexts:
    - multinational-maritime-operation
    - sanctions-enforcement
    - blockade-or-quarantine-support
    - counter-proliferation
    - counter-smuggling
  preconditions:
    - embargo-mandate-and-geographic-scope-defined
    - prohibited-vessel-cargo-and-activity-criteria-defined
    - inspection-diversion-and-seizure-authorities-defined
    - coordination-and-information-sharing-arrangements-established
  desired_end_state: >
    Prohibited maritime movements through the designated approaches have been prevented, diverted, seized or otherwise brought under authorized control.
  success_criteria:
    - relevant-maritime-routes-monitored
    - vessels-of-interest-identified-and-assessed
    - prohibited-movements-interdicted
    - disposition-of-interdicted-vessels-or-cargo-recorded
  failure_criteria:
    - prohibited-movement-transits-uninterdicted
    - vessel-of-interest-lost-before-resolution
    - required-inspection-or-control-cannot-be-completed
    - mandate-or-rules-of-engagement-violated

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - AssessmentCapability
    - InterdictionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - InspectionCapability
    - TransportCapability
    - ProtectionCapability
    - EngagementCapability
    - DataProcessingCapability

traceability:
  task_candidates:
    - TC-002
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-018
    - TC-021
    - TC-022
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-034
    - TC-035
    - TC-039
    - TC-040
    - TC-043
  ontology_concepts:
    - Platform
    - PlatformGroup
    - SpatialRegion
    - Route
    - PhysicalObject
    - Person
  related_missions:
    - relation: specialization-of
      mission: MC-020
    - relation: supported-by
      mission: MC-018
    - relation: may-include
      mission: MC-023
```

### MC-023 — Support Visit, Board, Search and Seizure

```yaml
id: MC-023
name: Support Visit, Board, Search and Seizure
status: draft
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: maritime-security-and-interdiction
  operational_intent: support
  mission_target: platform

specification:
  purpose: >
    Enable an authorized boarding force to approach, board, inspect and, when directed, seize a designated vessel, persons or physical objects.
  description: >
    Provide surveillance, vessel control, protection, coordination, communications and platform support required for a boarding team to conduct a visit, board, search and seizure action.
  applicable_contexts:
    - maritime-interdiction-operation
    - embargo-enforcement
    - counter-smuggling
    - counter-piracy
    - maritime-law-enforcement-support
  preconditions:
    - target-vessel-designated-and-positively-identified
    - boarding-authority-and-objectives-defined
    - boarding-force-and-support-platforms-assigned
    - safety-and-escalation-procedures-defined
  desired_end_state: >
    The boarding force has completed the authorized visit, search and any directed seizure, and has safely returned or transferred custody.
  success_criteria:
    - target-vessel-controlled-for-boarding
    - boarding-force-safely-inserted-and-recovered-or-transferred
    - inspection-objectives-completed
    - seized-persons-or-objects-secured-when-directed
  failure_criteria:
    - boarding-force-cannot-safely-board-or-withdraw
    - target-vessel-escapes-or-breaks-control
    - required-search-objectives-not-completed
    - unacceptable-harm-to-boarding-force-or-protected-persons

required_capabilities:
  mandatory:
    - SupportCapability
    - CoordinationCapability
    - CommunicationCapability
    - MobilityCapability
    - TrackingCapability
    - InspectionCapability
  optional:
    - ProtectionCapability
    - TransportCapability
    - EngagementCapability
    - RecoveryCapability
    - ManipulationCapability

traceability:
  task_candidates:
    - TC-006
    - TC-008
    - TC-016
    - TC-018
    - TC-021
    - TC-023
    - TC-024
    - TC-025
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-034
    - TC-035
    - TC-039
    - TC-040
    - TC-043
    - TC-051
    - TC-052
    - TC-059
  ontology_concepts:
    - Platform
    - PlatformGroup
    - Person
    - PersonnelGroup
    - PhysicalObject
  related_missions:
    - relation: enabled-by
      mission: MC-019
    - relation: may-be-part-of
      mission: MC-020
    - relation: may-be-part-of
      mission: MC-022
```

### MC-024 — Counter Piracy

```yaml
id: MC-024
name: Counter Piracy
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: conduct
  mission_target: maritime-activity

specification:
  purpose: >
    Deter, prevent, disrupt and terminate acts of piracy or armed robbery at sea while protecting threatened vessels and persons.
  description: >
    Monitor designated waters and traffic, identify piracy indicators, respond to threats or attacks, protect endangered vessels, interdict suspect craft and support recovery or boarding actions when authorized.
  applicable_contexts:
    - commercial-shipping-protection
    - sea-lane-security
    - regional-maritime-security
    - convoy-or-independent-transit-support
    - hostage-or-distress-response
  preconditions:
    - counter-piracy-area-or-protected-traffic-defined
    - threat-indicators-and-response-authority-defined
    - coordination-with-relevant-forces-and-shipping-established
    - response-assets-assigned
  desired_end_state: >
    Piracy threats in the designated context have been deterred, disrupted or controlled, and threatened vessels and persons are no longer under immediate pirate coercion.
  success_criteria:
    - piracy-threat-detected-or-reported-in-time
    - threatened-vessel-protected-or-released
    - hostile-craft-deterred-interdicted-or-controlled
    - relevant-incident-information-shared
  failure_criteria:
    - protected-vessel-captured-or-unacceptably-damaged
    - threatened-personnel-remain-under-hostile-control
    - hostile-craft-escapes-after-priority-interdiction
    - unacceptable-collateral-harm-caused

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - InterdictionCapability
    - ProtectionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - EngagementCapability
    - TransportCapability
    - RecoveryCapability
    - InspectionCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-002
    - TC-007
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-023
    - TC-024
    - TC-027
    - TC-028
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-034
    - TC-036
    - TC-039
    - TC-043
    - TC-049
    - TC-059
  ontology_concepts:
    - Platform
    - PlatformGroup
    - Person
    - PersonnelGroup
    - SpatialRegion
    - Route
  related_missions:
    - relation: may-use
      mission: MC-019
    - relation: may-include
      mission: MC-023
    - relation: may-require
      mission: MC-061
```

### MC-025 — Counter Maritime Terrorism

```yaml
id: MC-025
name: Counter Maritime Terrorism
status: draft
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-security-and-interdiction
  operational_intent: conduct
  mission_target: maritime-activity

specification:
  purpose: >
    Detect, deter, disrupt and contain terrorist threats directed through or against the maritime domain.
  description: >
    Monitor designated maritime areas, platforms and approaches for terrorist indicators, assess and track suspect activity, protect threatened assets and interdict hostile platforms or actors under authorized command.
  applicable_contexts:
    - critical-maritime-infrastructure-protection
    - harbour-and-port-security
    - high-value-unit-protection
    - maritime-event-security
    - response-to-maritime-terrorist-threat
  preconditions:
    - protected-assets-or-security-area-defined
    - threat-indicators-and-priority-intelligence-requirements-defined
    - command-authority-and-rules-of-engagement-defined
    - coordination-with-security-and-response-forces-established
  desired_end_state: >
    The designated terrorist threat has been deterred, identified, disrupted or contained, and protected maritime assets and persons are not under immediate unacceptable threat.
  success_criteria:
    - relevant-threat-indicators-detected-and-assessed
    - suspect-platform-or-activity-maintained-under-observation
    - hostile-action-prevented-disrupted-or-contained
    - protected-assets-remain-within-accepted-damage-thresholds
  failure_criteria:
    - hostile-action-achieves-principal-objective
    - priority-threat-not-detected-before-critical-point
    - suspect-platform-or-actor-lost-before-resolution
    - unacceptable-harm-to-protected-assets-or-persons

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - ThreatAssessmentCapability
    - InterdictionCapability
    - ProtectionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - EngagementCapability
    - NeutralizationCapability
    - ElectronicWarfareCapability
    - InspectionCapability
    - RecoveryCapability

traceability:
  task_candidates:
    - TC-002
    - TC-007
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-022
    - TC-024
    - TC-025
    - TC-027
    - TC-028
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-036
    - TC-037
    - TC-039
    - TC-040
    - TC-043
    - TC-063
  ontology_concepts:
    - Platform
    - PlatformGroup
    - Infrastructure
    - Person
    - PersonnelGroup
    - SpatialRegion
    - Route
  related_missions:
    - relation: may-use
      mission: MC-019
    - relation: may-require
      mission: MC-028
    - relation: may-require
      mission: MC-030
```

### MC-026 — Escort High-Value Unit

```yaml
id: MC-026
name: Escort High-Value Unit
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: escort
  mission_target: platform

specification:
  purpose: >
    Preserve the survivability and freedom of movement of a designated high-value platform.
  description: >
    Protect and accompany a designated platform during its movement or operational activity so that it can complete its assigned objective.
  applicable_contexts:
    - force-protection
    - contested-transit
    - task-group-operations
  preconditions:
    - protected-platform-designated
    - at-least-one-escort-platform-assigned
    - movement-or-operational-objective-defined
  desired_end_state: >
    The protected platform completes its assigned objective while remaining operational.
  success_criteria:
    - protected-platform-objective-completed
    - protected-platform-remains-operational
    - identified-threats-managed
  failure_criteria:
    - protected-platform-lost
    - protected-platform-unable-to-complete-objective
    - mission-aborted

required_capabilities:
  mandatory:
    - MobilityCapability
    - ProtectionCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - ThreatAssessmentCapability
    - InterdictionCapability

traceability:
  task_candidates:
    - TC-001
    - TC-005
    - TC-006
    - TC-016
    - TC-021
    - TC-023
    - TC-024
    - TC-025
    - TC-027
    - TC-028
    - TC-030
    - TC-036
    - TC-039
    - TC-040
    - TC-043
  ontology_concepts:
    - Platform
    - Route
    - SpatialRegion
    - PhysicalObject
  related_missions: []
```

### MC-027 — Escort Convoy

```yaml
id: MC-027
name: Escort Convoy
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: escort
  mission_target: platform-group

specification:
  purpose: >
    Preserve the integrity and freedom of movement of a designated platform group.
  description: >
    Protect and accompany a convoy during transit so that its members can reach the assigned destination or complete the assigned movement.
  applicable_contexts:
    - convoy-protection
    - sea-line-of-communication-protection
    - contested-transit
  preconditions:
    - convoy-defined
    - convoy-members-assigned
    - at-least-one-escort-platform-or-group-assigned
    - transit-objective-defined
  desired_end_state: >
    The convoy completes its assigned transit with the required level of integrity.
  success_criteria:
    - convoy-reaches-destination
    - required-convoy-integrity-maintained
    - identified-threats-managed
  failure_criteria:
    - convoy-integrity-below-acceptable-threshold
    - convoy-unable-to-complete-transit
    - mission-aborted

required_capabilities:
  mandatory:
    - MobilityCapability
    - ProtectionCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - ThreatAssessmentCapability
    - InterdictionCapability

traceability:
  task_candidates:
    - TC-001
    - TC-005
    - TC-006
    - TC-016
    - TC-021
    - TC-023
    - TC-024
    - TC-025
    - TC-027
    - TC-028
    - TC-030
    - TC-036
    - TC-039
    - TC-040
    - TC-043
  ontology_concepts:
    - Platform
    - PlatformGroup
    - Route
    - SpatialRegion
    - PhysicalObject
  related_missions: []
```


### MC-028 — Protect Maritime Task Group

```yaml
id: MC-028
name: Protect Maritime Task Group
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: protect
  mission_target: platform-group

specification:
  purpose: >
    Preserve the operational effectiveness, survivability and freedom of action of a designated maritime task group.
  description: >
    Organize and conduct layered protection around a maritime task group by detecting, assessing, tracking and countering threats across the relevant maritime approaches and operational sectors.
  applicable_contexts:
    - task-group-operations
    - contested-maritime-area
    - force-protection
    - high-threat-transit
  preconditions:
    - protected-task-group-defined
    - protection-sectors-and-priorities-defined
    - command-and-coordination-arrangements-established
    - threat-picture-or-priority-intelligence-requirements-available
  desired_end_state: >
    The task group retains the required operational effectiveness and freedom of action while identified threats are deterred, controlled or defeated.
  success_criteria:
    - protected-task-group-remains-operational
    - critical-task-group-functions-preserved
    - priority-threats-detected-and-managed-before-critical-impact
    - required-freedom-of-action-maintained
  failure_criteria:
    - task-group-operational-effectiveness-falls-below-required-threshold
    - critical-platform-lost-or-mission-killed
    - threat-penetrates-protective-disposition-with-unacceptable-effect
    - task-group-unable-to-continue-assigned-operation

required_capabilities:
  mandatory:
    - ProtectionCapability
    - PerceptionCapability
    - TrackingCapability
    - ThreatAssessmentCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - IdentificationCapability
    - InterdictionCapability
    - EngagementCapability
    - ElectronicWarfareCapability
    - MobilityCapability

traceability:
  task_candidates:
    - TC-002
    - TC-005
    - TC-006
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-022
    - TC-024
    - TC-025
    - TC-027
    - TC-028
    - TC-030
    - TC-036
    - TC-039
    - TC-040
    - TC-042
    - TC-043
    - TC-062
    - TC-063
  ontology_concepts:
    - Platform
    - PlatformGroup
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: may-include
      mission: MC-026
    - relation: may-include
      mission: MC-027
    - relation: may-use
      mission: MC-033
```

### MC-029 — Protect Maritime Critical Infrastructure

```yaml
id: MC-029
name: Protect Maritime Critical Infrastructure
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: protect
  mission_target: infrastructure

specification:
  purpose: >
    Prevent or limit hostile, accidental or unauthorized effects against designated maritime critical infrastructure.
  description: >
    Maintain surveillance and protective control around designated offshore, coastal or subsea infrastructure, detect and assess suspicious activity, and coordinate an appropriate defensive or interdiction response.
  applicable_contexts:
    - offshore-infrastructure-protection
    - subsea-infrastructure-protection
    - coastal-energy-security
    - elevated-maritime-threat
  preconditions:
    - protected-infrastructure-designated
    - protective-area-and-access-rules-defined
    - threat-indicators-and-response-authorities-defined
    - infrastructure-status-information-available
  desired_end_state: >
    The protected infrastructure remains functional within accepted limits and no unresolved threat is capable of producing unacceptable damage.
  success_criteria:
    - protected-infrastructure-remains-within-operational-thresholds
    - unauthorized-approaches-detected-and-assessed
    - confirmed-threats-deterred-interdicted-or-neutralized
    - protective-area-control-maintained
  failure_criteria:
    - critical-infrastructure-function-lost
    - unacceptable-physical-or-cyber-physical-damage-caused
    - priority-threat-reaches-critical-zone-undetected
    - protective-response-not-available-before-required-time

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - ThreatAssessmentCapability
    - ProtectionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - InterdictionCapability
    - EngagementCapability
    - InspectionCapability
    - ElectronicWarfareCapability
    - SurveyCapability

traceability:
  task_candidates:
    - TC-002
    - TC-003
    - TC-004
    - TC-011
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-018
    - TC-021
    - TC-022
    - TC-024
    - TC-025
    - TC-026
    - TC-028
    - TC-030
    - TC-031
    - TC-032
    - TC-036
    - TC-037
    - TC-039
    - TC-040
    - TC-043
    - TC-058
    - TC-062
  ontology_concepts:
    - Infrastructure
    - Platform
    - SpatialRegion
    - PhysicalObject
    - Sensor
  related_missions:
    - relation: may-use
      mission: MC-018
    - relation: may-require
      mission: MC-030
    - relation: may-use
      mission: MC-033
```

### MC-030 — Protect Harbour or Naval Base

```yaml
id: MC-030
name: Protect Harbour or Naval Base
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: protect
  mission_target: infrastructure

specification:
  purpose: >
    Preserve the security, operational availability and controlled accessibility of a designated harbour or naval base.
  description: >
    Conduct layered surveillance, access control and defensive activity across harbour approaches, entrances, anchorages and internal waters to detect and respond to surface, subsurface, airborne or land-originating maritime threats.
  applicable_contexts:
    - naval-base-defence
    - harbour-security
    - heightened-force-protection
    - deployment-or-reception-of-high-value-units
  preconditions:
    - protected-harbour-or-base-designated
    - security-zones-and-access-rules-defined
    - command-authorities-and-response-forces-identified
    - recognized-local-maritime-picture-available
  desired_end_state: >
    The harbour or naval base remains operational, authorized movements can continue, and no unresolved threat controls or penetrates a critical security zone.
  success_criteria:
    - critical-base-functions-remain-available
    - authorized-maritime-traffic-managed-within-security-rules
    - unauthorized-or-hostile-approaches-detected-and-resolved
    - critical-security-zones-remain-controlled
  failure_criteria:
    - harbour-or-base-critical-function-disrupted
    - hostile-platform-or-device-reaches-protected-asset
    - unauthorized-access-to-critical-zone-not-contained
    - protected-unit-unable-to-enter-exit-or-operate-as-required

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - IdentificationCapability
    - ProtectionCapability
    - InterdictionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - InspectionCapability
    - ThreatAssessmentCapability
    - NeutralizationCapability
    - ElectronicWarfareCapability
    - SurveyCapability

traceability:
  task_candidates:
    - TC-002
    - TC-003
    - TC-004
    - TC-011
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-018
    - TC-021
    - TC-022
    - TC-024
    - TC-025
    - TC-026
    - TC-028
    - TC-030
    - TC-031
    - TC-032
    - TC-033
    - TC-036
    - TC-037
    - TC-039
    - TC-040
    - TC-043
    - TC-045
    - TC-058
    - TC-062
  ontology_concepts:
    - Harbour
    - NavalBase
    - Infrastructure
    - Platform
    - SpatialRegion
    - Route
    - PhysicalObject
  related_missions:
    - relation: may-use
      mission: MC-018
    - relation: may-include
      mission: MC-021
    - relation: may-use
      mission: MC-033
```

### MC-031 — Protect Maritime Transit Corridor

```yaml
id: MC-031
name: Protect Maritime Transit Corridor
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: protect
  mission_target: corridor

specification:
  purpose: >
    Maintain a designated maritime corridor sufficiently secure and usable for authorized transit.
  description: >
    Monitor, patrol and protect a bounded maritime transit corridor and its approaches, identify hazards and threats, and coordinate escorts, screening or interdiction actions required to preserve passage.
  applicable_contexts:
    - contested-transit
    - chokepoint-security
    - evacuation-or-redeployment-route
    - protected-commercial-or-military-movement
  preconditions:
    - protected-corridor-geometrically-defined
    - authorized-users-and-transit-rules-defined
    - corridor-threat-and-hazard-assessment-available
    - protection-and-response-assets-assigned
  desired_end_state: >
    Authorized platforms can transit the corridor within accepted risk and timing limits, while relevant threats and hazards are controlled.
  success_criteria:
    - corridor-remains-available-for-authorized-transit
    - required-transits-completed-within-accepted-risk
    - priority-threats-and-hazards-detected-and-managed
    - corridor-control-and-situational-awareness-maintained
  failure_criteria:
    - corridor-closed-or-rendered-unusable
    - authorized-transit-suffers-unacceptable-loss
    - critical-threat-or-hazard-remains-unresolved-in-corridor
    - required-transit-window-missed-due-to-protection-failure

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - TrackingCapability
    - ProtectionCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - IdentificationCapability
    - SurveyCapability
    - InterdictionCapability
    - EscortCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-004
    - TC-005
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-021
    - TC-022
    - TC-023
    - TC-024
    - TC-025
    - TC-026
    - TC-028
    - TC-030
    - TC-032
    - TC-039
    - TC-040
    - TC-043
    - TC-045
    - TC-047
    - TC-058
    - TC-062
  ontology_concepts:
    - Route
    - SpatialRegion
    - Platform
    - PlatformGroup
    - PhysicalObject
  related_missions:
    - relation: may-include
      mission: MC-027
    - relation: may-require
      mission: MC-017
    - relation: broader-or-overlapping
      mission: MC-032
```

### MC-032 — Protect Sea Line of Communication

```yaml
id: MC-032
name: Protect Sea Line of Communication
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: protect
  mission_target: route-network

specification:
  purpose: >
    Preserve the sustained use of a designated maritime route network for military, governmental or commercial movement.
  description: >
    Protect a sea line of communication through persistent monitoring, route-risk assessment, escort, area control and coordinated response across multiple maritime segments and supporting nodes.
  applicable_contexts:
    - strategic-maritime-mobility
    - coalition-sustainment
    - commercial-shipping-protection
    - prolonged-contested-maritime-operations
  preconditions:
    - sea-line-of-communication-defined
    - critical-route-segments-and-nodes-identified
    - authorized-traffic-and-priorities-defined
    - sustained-protection-and-information-arrangements-established
  desired_end_state: >
    The sea line of communication remains sufficiently available and predictable to support required movement over the specified period.
  success_criteria:
    - required-traffic-flow-sustained
    - critical-route-segments-remain-usable
    - cumulative-loss-and-delay-remain-within-accepted-thresholds
    - threat-and-hazard-picture-maintained-across-route-network
  failure_criteria:
    - strategic-flow-requirement-not-met
    - critical-route-segment-denied-for-unacceptable-duration
    - losses-or-delays-exceed-accepted-thresholds
    - protection-effort-cannot-be-sustained

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - ProtectionCapability
    - CommunicationCapability
    - CoordinationCapability
    - MobilityCapability
  optional:
    - EscortCapability
    - InterdictionCapability
    - SurveyCapability
    - LogisticsCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-004
    - TC-005
    - TC-010
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-021
    - TC-022
    - TC-023
    - TC-024
    - TC-025
    - TC-028
    - TC-030
    - TC-032
    - TC-039
    - TC-040
    - TC-042
    - TC-043
    - TC-044
    - TC-047
    - TC-053
    - TC-062
  ontology_concepts:
    - Route
    - SpatialRegion
    - Platform
    - PlatformGroup
    - Infrastructure
  related_missions:
    - relation: may-include
      mission: MC-027
    - relation: may-include
      mission: MC-031
    - relation: may-require
      mission: MC-018
```

### MC-033 — Establish Protective Screen

```yaml
id: MC-033
name: Establish Protective Screen
status: draft
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: protection-and-defence
  operational_intent: conduct
  mission_target: protected-force-or-area

specification:
  purpose: >
    Create and maintain a protective disposition that provides warning, separation and defensive reaction time for a designated force, platform or area.
  description: >
    Position and coordinate assigned platforms or sensors along designated sectors, bearings or boundaries to detect, classify, track and, when authorized, delay or counter approaching threats.
  applicable_contexts:
    - task-group-protection
    - amphibious-force-protection
    - harbour-or-infrastructure-defence
    - contested-transit
  preconditions:
    - protected-object-or-area-designated
    - screen-sectors-boundaries-or-stations-defined
    - screen-assets-and-command-relationships-assigned
    - reporting-and-engagement-criteria-defined
  desired_end_state: >
    A coherent protective screen is maintained, providing the required warning and defensive depth without unacceptable gaps.
  success_criteria:
    - assigned-screen-sectors-covered
    - required-detection-and-warning-time-achieved
    - contacts-crossing-screen-assessed-and-reported
    - screen-integrity-maintained-or-restored
  failure_criteria:
    - unacceptable-gap-persists-in-priority-sector
    - threat-crosses-screen-without-required-warning
    - screen-assets-lose-coordination-or-positioning
    - protected-object-exposed-beyond-accepted-threshold

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - TrackingCapability
    - CommunicationCapability
    - CoordinationCapability
    - ProtectionCapability
  optional:
    - IdentificationCapability
    - InterdictionCapability
    - EngagementCapability
    - ElectronicWarfareCapability
    - ThreatAssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-005
    - TC-006
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-021
    - TC-024
    - TC-025
    - TC-026
    - TC-027
    - TC-028
    - TC-030
    - TC-036
    - TC-038
    - TC-039
    - TC-040
    - TC-042
    - TC-043
    - TC-045
    - TC-062
  ontology_concepts:
    - Platform
    - PlatformGroup
    - SpatialRegion
    - Route
    - Sensor
  related_missions:
    - relation: may-support
      mission: MC-028
    - relation: may-support
      mission: MC-029
    - relation: may-support
      mission: MC-030
    - relation: may-support
      mission: MC-031
```


## 8. Phase A consolidation — Mission Type assignment

All 66 candidate missions have been assigned to one and only one Mission Type.

Assignment principles:

- patrol, surveillance, reconnaissance and monitoring missions belong to `MT-01`;
- location of an unknown or missing target belongs to `MT-02`;
- systematic characterization and clearance verification belong to `MT-03`;
- escort, defence, screening and preservation belong to `MT-04`;
- embargo, exclusion, denial and control activities belong to `MT-05`;
- mine clearance, strike and threat neutralization belong to `MT-06`;
- retrieval and evacuation effects belong to `MT-07`;
- logistics, transport, relay and assistance belong to `MT-08`;
- amphibious support, special-operations support, joint fires support and other enabling activities belong to `MT-09`.

Potentially ambiguous assignments remain `candidate` until their detailed mission specification is reviewed. In particular:

- `Conduct Mine Reconnaissance` is classified as Search;
- `Verify Mine Clearance` is classified as Survey;
- `Lay Minefield` is classified as Interdiction and Control;
- `Deploy Decoy` is classified as Protection;
- `Support Casualty Evacuation` is classified as Recovery.

## 9. Changes 0.6.0 → 0.7.0

- Completed the `protection-and-defence` family by adding detailed specifications for MC-028 through MC-033.
- Added mission-to-task traceability for the six new mission specifications.
- Recomputed inverse `used_by_missions` references in the Task Catalog.

## 10. Earlier changes

### Changes 0.3.0 → 0.3.1

- Ontology references corrected against the Naval Ontology v2.0: `Area` and `SpatialEntity` (which do not exist as ontology classes) replaced by `SpatialRegion` in the mission-target table (§3.5) and in the `ontology_concepts` lists of MC-001, MC-026 and MC-027. `SpatialRegion` is retained rather than a specific subclass because a mission-target area may be coastal, harbour, restricted or seabed; introducing an intermediate `nmo:Area` class grouping the `*Area` subclasses is a candidate ontology change (v2.1), not a catalog decision.

## 10. Changes 0.4.0 → 0.5.0

- Completed detailed specifications for the six Mine Warfare missions MC-012 to MC-017.
- Added capability requirements, task candidates, ontology concepts and typed mission relationships for the Mine Warfare family.
- Promoted MC-012 to MC-017 from `candidate` to `draft`.
- Regenerated Task Catalog `used_by_missions` references from Mission Catalog `task_candidates`.

## 11. Open consolidation points

- Review the naming and scope of lethal combat missions before validation.
- Replace operational labels such as high-value unit, convoy, suspect vessel and threat by Scenario Model roles rather than ontology classes.
- Complete detailed specifications iteratively and validate all task references against the Task Catalog.


## 12. Detailed mission specifications — Maritime Combat Operations

The specifications in this section use the mission identities and classifications defined in the canonical inventory in section 5.

### MC-034 — Conduct Anti-Surface Patrol

```yaml
id: MC-034
name: Conduct Anti-Surface Patrol
status: candidate
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: maritime-combat-operations
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Establish and maintain maritime situational awareness over hostile or potentially hostile
    surface vessels within an assigned area while ensuring freedom of manoeuvre for friendly
    forces. The mission aims to detect, classify, identify, track and, when authorized,
    engage hostile surface contacts.
  description: >
    A force conducts a patrol within a designated maritime area to search for surface contacts,
    maintain a recognized maritime picture, monitor hostile activity and react to emerging
    threats. Depending on the rules of engagement, the mission may remain limited to
    surveillance or escalate to interception and engagement.
  applicable_contexts:
    - sea-control
    - maritime-security
    - force-protection
    - high-intensity-warfare
  preconditions:
    - assigned-patrol-area-defined
    - patrol-force-available
    - rules-of-engagement-established
  desired_end_state: >
    The patrol area is monitored, relevant surface contacts are classified, hostile units are
    tracked or neutralized as authorized, and maritime situational awareness is maintained.
  success_criteria:
    - assigned-patrol-completed
    - no-hostile-surface-activity-remains-undetected
    - threats-reported-or-neutralized-according-to-rules-of-engagement
  failure_criteria:
    - patrol-area-insufficiently-covered
    - hostile-unit-remains-undetected
    - friendly-force-surprised-by-surface-threat

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - NavigationCapability
    - CommunicationCapability
  optional:
    - EngagementCapability
    - ElectronicWarfareCapability
    - CoordinationCapability

traceability:
  task_candidates:
    - TC-002
    - TC-001
    - TC-011
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-039
    - TC-030
    - TC-007
    - TC-036
    - TC-021
  ontology_concepts:
    - SurfacePlatform
    - MaritimeArea
    - SpatialRegion
  related_missions:
    - relation: related-to
      mission: MC-035
    - relation: may-contribute-to
      mission: MC-018
    - relation: may-support
      mission: MC-028
  notes: >
    This mission represents continuous ASuW presence and surveillance. Engagement is optional
    and depends on the operational context and Rules of Engagement.
```



### MC-035 — Neutralize Surface Threat

```yaml
id: MC-035
name: Neutralize Surface Threat
status: candidate
version: 0.1.0

classification:
  mission_type: MT-06
  primary_family: maritime-combat-operations
  operational_intent: conduct
  mission_target: platform

specification:
  purpose: >
    Neutralize or destroy a hostile surface platform that poses an immediate or anticipated
    threat to friendly forces or mission accomplishment.
  description: >
    The assigned force detects, tracks, identifies and engages a designated hostile surface
    contact in accordance with the Rules of Engagement until the threat is neutralized or
    rendered incapable of continuing its mission.
  applicable_contexts:
    - sea-control
    - high-intensity-warfare
    - force-protection
  preconditions:
    - hostile-surface-contact-identified
    - engagement-authorized
    - weapon-systems-available
  desired_end_state: >
    The hostile surface threat is neutralized and the friendly force retains freedom of manoeuvre.
  success_criteria:
    - threat-rendered-ineffective
    - friendly-objectives-preserved
  failure_criteria:
    - threat-remains-operational
    - friendly-force-suffers-unacceptable-losses

required_capabilities:
  mandatory:
    - TrackingCapability
    - EngagementCapability
    - CommunicationCapability
  optional:
    - CoordinationCapability
    - ElectronicWarfareCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-016
    - TC-015
    - TC-042
    - TC-036
    - TC-021
  ontology_concepts:
    - SurfacePlatform
    - WeaponSystem
  related_missions:
    - relation: related-to
      mission: MC-034
    - relation: may-support
      mission: MC-028
```



### MC-036 — Conduct Anti-Submarine Patrol

```yaml
id: MC-036
name: Conduct Anti-Submarine Patrol
status: candidate
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: maritime-combat-operations
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Detect, classify, localize and continuously monitor hostile or potentially hostile submarines
    within an assigned patrol area in order to maintain undersea situational awareness and protect
    friendly forces.
  description: >
    Assigned ASW assets patrol a designated maritime area to search for submarines using available
    sensors. Contacts are detected, classified, localized, tracked and reported. Engagement may
    be initiated only when authorized by the Rules of Engagement.
  applicable_contexts:
    - sea-control
    - force-protection
    - high-intensity-warfare
  preconditions:
    - patrol-area-defined
    - anti-submarine-warfare-assets-available
    - rules-of-engagement-established
  desired_end_state: >
    The undersea situation is established and hostile submarines are tracked or contained.
  success_criteria:
    - patrol-area-searched
    - relevant-submarine-contacts-detected-and-reported
  failure_criteria:
    - hostile-submarine-remains-undetected
    - friendly-force-surprised-by-underwater-threat

required_capabilities:
  mandatory:
    - DetectionCapability
    - TrackingCapability
    - NavigationCapability
    - CommunicationCapability
  optional:
    - EngagementCapability
    - ElectronicWarfareCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-012
    - TC-014
    - TC-013
    - TC-016
    - TC-039
  ontology_concepts:
    - Submarine
    - MaritimeArea
    - SpatialRegion
  related_missions:
    - relation: related-to
      mission: MC-037
    - relation: may-support
      mission: MC-028
```



### MC-037 — Neutralize Submarine Threat

```yaml
id: MC-037
name: Neutralize Submarine Threat
status: candidate
version: 0.1.0

classification:
  mission_type: MT-06
  primary_family: maritime-combat-operations
  operational_intent: conduct
  mission_target: platform

specification:
  purpose: >
    Neutralize a hostile submarine threatening friendly forces or mission accomplishment.
  description: >
    Following detection and positive identification, assigned forces track and engage the
    hostile submarine in accordance with the Rules of Engagement until it is destroyed,
    forced to withdraw or rendered incapable of continuing its mission.
  applicable_contexts:
    - sea-control
    - high-intensity-warfare
    - force-protection
  preconditions:
    - hostile-submarine-localized
    - engagement-authorized
    - anti-submarine-warfare-weapon-systems-available
  desired_end_state: >
    The hostile submarine is neutralized and the undersea threat is removed.
  success_criteria:
    - submarine-rendered-ineffective
    - friendly-force-remains-protected
  failure_criteria:
    - submarine-escapes-or-remains-operational
    - friendly-forces-sustain-unacceptable-losses

required_capabilities:
  mandatory:
    - TrackingCapability
    - EngagementCapability
    - CommunicationCapability
  optional:
    - CoordinationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-016
    - TC-015
    - TC-042
    - TC-036
    - TC-021
  ontology_concepts:
    - Submarine
    - WeaponSystem
  related_missions:
    - relation: related-to
      mission: MC-036
    - relation: may-support
      mission: MC-028
```



### MC-038 — Defend Task Group Against Air Threat

```yaml
id: MC-038
name: Defend Task Group Against Air Threat
status: candidate
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: maritime-combat-operations
  operational_intent: protect
  mission_target: platform-group

specification:
  purpose: >
    Protect a maritime task group against hostile aircraft, helicopters, missiles and other
    airborne threats in order to preserve combat effectiveness and mission accomplishment.
  description: >
    Assigned air-defence assets continuously detect, classify, identify, track and, when
    required, engage airborne threats in accordance with the Rules of Engagement while
    coordinating the recognized air picture across the force.
  applicable_contexts:
    - air-defence
    - force-protection
    - sea-control
    - high-intensity-warfare
  preconditions:
    - task-group-established
    - air-defence-assets-available
    - rules-of-engagement-established
  desired_end_state: >
    The task group is protected, air threats are intercepted or deterred, and local air
    superiority is maintained around the task group.
  success_criteria:
    - no-protected-unit-lost-due-to-air-threat
    - air-threats-detected-and-handled-in-time
  failure_criteria:
    - air-threat-penetrates-defensive-screen
    - protected-force-suffers-unacceptable-losses

required_capabilities:
  mandatory:
    - PerceptionCapability
    - TrackingCapability
    - EngagementCapability
    - CommunicationCapability
  optional:
    - CoordinationCapability
    - ElectronicWarfareCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-012
    - TC-014
    - TC-015
    - TC-016
    - TC-042
    - TC-036
    - TC-021
  ontology_concepts:
    - Aircraft
    - PlatformGroup
    - PhysicalObject
  related_missions:
    - relation: related-to
      mission: MC-028
    - relation: related-to
      mission: MC-034
    - relation: related-to
      mission: MC-043
```

### MC-039 — Conduct Maritime Strike

```yaml
id: MC-039
name: Conduct Maritime Strike
status: candidate
version: 0.1.0

classification:
  mission_type: MT-06
  primary_family: maritime-combat-operations
  operational_intent: conduct
  mission_target: physical-object

specification:
  purpose: >
    Deliver a controlled maritime strike against a designated military target in order to
    neutralize it while limiting unintended effects.
  description: >
    Assigned forces locate, identify and engage a designated target using authorized weapon
    effects in accordance with mission objectives and Rules of Engagement. The strike may be
    conducted independently or as part of a wider joint operation.
  applicable_contexts:
    - high-intensity-warfare
    - littoral-warfare
    - joint-operations
  preconditions:
    - designated-target-identified
    - strike-authorized
    - suitable-weapon-system-available
    - rules-of-engagement-established
  desired_end_state: >
    The designated military target is neutralized to the required degree and unintended effects
    remain within authorized limits.
  success_criteria:
    - designated-target-neutralized-to-required-degree
    - strike-effects-confirmed
    - unintended-effects-within-authorized-limits
  failure_criteria:
    - designated-target-remains-effective
    - strike-cannot-be-completed-within-authorization
    - unintended-effects-exceed-authorized-limits

required_capabilities:
  mandatory:
    - IdentificationCapability
    - EngagementCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - CoordinationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-012
    - TC-015
    - TC-016
    - TC-042
    - TC-036
    - TC-021
    - TC-039
  ontology_concepts:
    - PhysicalObject
    - WeaponSystem
    - Platform
  related_missions:
    - relation: supported-by
      mission: MC-041
    - relation: may-follow
      mission: MC-003
```

### MC-040 — Deny Access to Maritime Area

```yaml
id: MC-040
name: Deny Access to Maritime Area
status: candidate
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: maritime-combat-operations
  operational_intent: interdict
  mission_target: area

specification:
  purpose: >
    Prevent or constrain an adversary force from entering, crossing or using a designated
    maritime area for a specified operational period.
  description: >
    Assigned forces establish and maintain an access-denial posture over a designated maritime
    area. Relevant contacts are detected, tracked, warned, intercepted or engaged as authorized
    so that adversary use of the area is prevented or made operationally ineffective.
  applicable_contexts:
    - sea-denial
    - force-protection
    - littoral-warfare
    - high-intensity-warfare
  preconditions:
    - maritime-area-defined
    - access-policy-defined
    - assigned-forces-available
    - rules-of-engagement-established
  desired_end_state: >
    The adversary cannot make effective operational use of the designated maritime area during
    the required period, while authorized friendly access is preserved.
  success_criteria:
    - designated-area-denied-for-required-period
    - relevant-adversary-contacts-handled-according-to-authorization
    - authorized-friendly-access-preserved
  failure_criteria:
    - adversary-achieves-effective-use-of-designated-area
    - denial-posture-cannot-be-maintained
    - authorized-friendly-movement-is-unacceptably-disrupted

required_capabilities:
  mandatory:
    - InterdictionCapability
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - EngagementCapability
    - CoordinationCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-012
    - TC-016
    - TC-026
    - TC-030
    - TC-033
    - TC-036
    - TC-039
  ontology_concepts:
    - MaritimeArea
    - SpatialRegion
    - Platform
    - PlatformGroup
  related_missions:
    - relation: may-require
      mission: MC-034
    - relation: may-require
      mission: MC-036
    - relation: broader-or-overlapping
      mission: MC-021
```

### MC-041 — Support Joint Fires

```yaml
id: MC-041
name: Support Joint Fires
status: candidate
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: maritime-combat-operations
  operational_intent: support
  mission_target: physical-object

specification:
  purpose: >
    Enable accurate and timely joint fires against designated targets by providing maritime
    sensing, coordination, targeting, engagement or assessment support.
  description: >
    Maritime forces contribute to a joint fires process by sharing target information,
    coordinating fire requests, supporting target identification and, when assigned, delivering
    or assessing authorized effects in support of another force's operation.
  applicable_contexts:
    - joint-operations
    - amphibious-operations
    - littoral-warfare
    - high-intensity-warfare
  preconditions:
    - supported-operation-identified
    - joint-coordination-arrangements-established
    - fire-support-request-or-tasking-authorized
    - target-information-available
  desired_end_state: >
    The supported joint force receives the information, coordination or effects required to
    execute its fire mission within the requested timing and accuracy.
  success_criteria:
    - requested-joint-fires-support-delivered
    - required-coordination-and-information-exchange-achieved
    - supported-fire-mission-enabled
  failure_criteria:
    - support-not-delivered-within-required-time
    - target-information-insufficient-for-authorized-action
    - coordination-failure-prevents-supported-fire-mission

required_capabilities:
  mandatory:
    - CoordinationCapability
    - CommunicationCapability
  optional:
    - IdentificationCapability
    - EngagementCapability
    - AssessmentCapability
    - TrackingCapability

traceability:
  task_candidates:
    - TC-041
    - TC-043
    - TC-040
    - TC-015
    - TC-042
    - TC-036
    - TC-021
    - TC-039
  ontology_concepts:
    - WeaponSystem
    - PhysicalObject
    - Platform
  related_missions:
    - relation: supports
      mission: MC-039
    - relation: may-support
      mission: MC-044
```

### MC-042 — Reconnoitre Landing Area

```yaml
id: MC-042
name: Reconnoitre Landing Area
status: candidate
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: littoral-and-amphibious-support
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Establish operational understanding of a prospective landing area in order to support
    amphibious planning and reduce uncertainty before force commitment.
  description: >
    Assigned forces observe and characterize a designated littoral landing area, its approaches
    and relevant activity. They detect, localize and report terrain, obstacles, infrastructure,
    contacts and hazards that may affect an amphibious operation.
  applicable_contexts:
    - amphibious-operations
    - littoral-warfare
    - pre-operation-intelligence-preparation
    - contested-environment
  preconditions:
    - prospective-landing-area-defined
    - reconnaissance-objectives-defined
    - suitable-sensing-assets-available
    - reporting-arrangements-established
  desired_end_state: >
    The designated landing area and its approaches are sufficiently understood to support
    amphibious planning, with relevant hazards, contacts and access constraints reported.
  success_criteria:
    - required-landing-area-observations-completed
    - relevant-hazards-and-contacts-reported
    - required-operational-understanding-established
  failure_criteria:
    - required-area-cannot-be-observed
    - critical-hazard-or-contact-remains-unassessed
    - collected-information-insufficient-for-amphibious-planning

required_capabilities:
  mandatory:
    - MobilityCapability
    - PerceptionCapability
    - DetectionCapability
    - CommunicationCapability
  optional:
    - SurveyCapability
    - LocalizationCapability
    - ClassificationCapability
    - IdentificationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-003
    - TC-004
    - TC-011
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-019
    - TC-020
    - TC-021
    - TC-039
  ontology_concepts:
    - SpatialRegion
    - MaritimeArea
    - Infrastructure
    - PhysicalObject
  related_missions:
    - relation: may-enable
      mission: MC-043
    - relation: may-enable
      mission: MC-044
```

### MC-043 — Survey Littoral Access Route

```yaml
id: MC-043
name: Survey Littoral Access Route
status: candidate
version: 0.1.0

classification:
  mission_type: MT-03
  primary_family: littoral-and-amphibious-support
  operational_intent: survey
  mission_target: route

specification:
  purpose: >
    Systematically characterize a littoral access route and its immediate surroundings to
    determine whether it can support the intended movement of amphibious forces.
  description: >
    Assigned forces traverse or remotely survey a designated route from the maritime approach
    toward a landing area. They map the route, measure relevant environmental characteristics,
    detect obstacles and hazards, and report constraints affecting access and manoeuvre.
  applicable_contexts:
    - amphibious-operations
    - littoral-access-planning
    - route-preparation
    - contested-environment
  preconditions:
    - candidate-littoral-route-defined
    - survey-criteria-defined
    - suitable-survey-assets-available
    - required-access-authorization-established
  desired_end_state: >
    The littoral access route is characterized to the required level and its suitability,
    constraints, hazards and access conditions are reported.
  success_criteria:
    - required-route-coverage-achieved
    - relevant-route-characteristics-measured
    - obstacles-and-hazards-reported
    - route-suitability-assessed
  failure_criteria:
    - required-route-segment-not-surveyed
    - critical-route-condition-remains-unknown
    - survey-information-insufficient-for-access-decision

required_capabilities:
  mandatory:
    - SurveyCapability
    - NavigationCapability
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - DetectionCapability
    - AssessmentCapability
    - PositionEstimationCapability

traceability:
  task_candidates:
    - TC-001
    - TC-004
    - TC-011
    - TC-012
    - TC-019
    - TC-020
    - TC-021
    - TC-039
  ontology_concepts:
    - Route
    - Corridor
    - SpatialRegion
    - MaritimeArea
  related_missions:
    - relation: enabled-by
      mission: MC-042
    - relation: may-enable
      mission: MC-044
    - relation: may-enable
      mission: MC-046
```

### MC-044 — Support Amphibious Operations

```yaml
id: MC-044
name: Support Amphibious Operations
status: candidate
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: littoral-and-amphibious-support
  operational_intent: support
  mission_target: platform-group

specification:
  purpose: >
    Enable an amphibious force to approach, land, manoeuvre or withdraw by providing the
    maritime support required by the supported operation.
  description: >
    Assigned maritime forces coordinate and deliver selected mobility, transport, deployment,
    protection, communication, sensing or engagement support to an amphibious force. The exact
    support package depends on the phase, threat and objectives of the supported operation.
  applicable_contexts:
    - amphibious-landing
    - amphibious-manoeuvre
    - amphibious-withdrawal
    - littoral-warfare
    - joint-operations
  preconditions:
    - supported-amphibious-operation-defined
    - support-requirements-defined
    - coordination-arrangements-established
    - assigned-support-assets-available
  desired_end_state: >
    The amphibious force receives the required maritime support and can complete the supported
    phase of its operation under the specified access, timing and protection conditions.
  success_criteria:
    - required-amphibious-support-delivered
    - supported-force-reaches-required-operational-condition
    - coordination-with-supported-force-maintained
  failure_criteria:
    - critical-support-not-delivered
    - supported-force-cannot-complete-required-phase
    - coordination-failure-compromises-supported-operation

required_capabilities:
  mandatory:
    - SupportCapability
    - CoordinationCapability
    - CommunicationCapability
    - MobilityCapability
  optional:
    - TransportCapability
    - DeploymentCapability
    - ProtectionCapability
    - EngagementCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-023
    - TC-028
    - TC-036
    - TC-038
    - TC-039
    - TC-043
    - TC-051
    - TC-059
  ontology_concepts:
    - PlatformGroup
    - Platform
    - SpatialRegion
    - MaritimeArea
    - PhysicalObject
  related_missions:
    - relation: may-require
      mission: MC-042
    - relation: may-require
      mission: MC-043
    - relation: may-require
      mission: MC-046
    - relation: supported-by
      mission: MC-041
```

### MC-045 — Support Special Operations

```yaml
id: MC-045
name: Support Special Operations
status: candidate
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: littoral-and-amphibious-support
  operational_intent: support
  mission_target: personnel

specification:
  purpose: >
    Enable a designated special operations force to deploy, operate, sustain or recover in a
    maritime or littoral objective area.
  description: >
    Assigned maritime forces provide selected transport, deployment, recovery, communication,
    sensing, protection or coordination support to a special operations force while preserving
    the timing, discretion and operational constraints of the supported activity.
  applicable_contexts:
    - special-operations
    - littoral-warfare
    - covert-or-discreet-support
    - joint-operations
  preconditions:
    - supported-special-operation-defined
    - support-requirements-and-constraints-defined
    - coordination-and-communication-arrangements-established
    - suitable-support-assets-available
  desired_end_state: >
    The supported special operations force receives the required maritime support and reaches
    the specified operational condition without unacceptable compromise or delay.
  success_criteria:
    - required-special-operations-support-delivered
    - supported-force-reaches-required-operational-condition
    - required-discretion-and-timing-preserved
  failure_criteria:
    - critical-support-not-delivered
    - supported-force-cannot-reach-required-operational-condition
    - support-activity-causes-unacceptable-compromise-or-delay

required_capabilities:
  mandatory:
    - SupportCapability
    - CoordinationCapability
    - CommunicationCapability
  optional:
    - MobilityCapability
    - TransportCapability
    - DeploymentCapability
    - RecoveryCapability
    - ProtectionCapability
    - PerceptionCapability

traceability:
  task_candidates:
    - TC-001
    - TC-038
    - TC-039
    - TC-040
    - TC-043
    - TC-044
    - TC-049
    - TC-051
    - TC-059
  ontology_concepts:
    - PersonnelGroup
    - Person
    - Platform
    - PhysicalObject
    - SpatialRegion
  related_missions:
    - relation: may-require
      mission: MC-042
    - relation: may-require
      mission: MC-046
    - relation: may-require
      mission: MC-061
```

### MC-046 — Secure Littoral Access Corridor

```yaml
id: MC-046
name: Secure Littoral Access Corridor
status: candidate
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: littoral-and-amphibious-support
  operational_intent: protect
  mission_target: corridor

specification:
  purpose: >
    Establish and maintain a sufficiently secure littoral corridor for the movement of a
    designated friendly force between the maritime approach and its objective area.
  description: >
    Assigned forces survey, monitor and protect a designated access corridor. They detect and
    handle relevant hazards and threats, preserve route availability and report changes that
    could affect the authorized movement of the supported force.
  applicable_contexts:
    - amphibious-operations
    - littoral-access
    - force-protection
    - contested-environment
  preconditions:
    - littoral-corridor-defined
    - supported-movement-defined
    - corridor-security-criteria-defined
    - assigned-protection-assets-available
  desired_end_state: >
    The designated littoral corridor remains available and sufficiently secure for the required
    friendly movement during the specified operational period.
  success_criteria:
    - corridor-surveyed-and-monitored
    - relevant-hazards-and-threats-handled
    - supported-movement-completed-under-required-protection-conditions
  failure_criteria:
    - corridor-becomes-unavailable
    - unresolved-threat-prevents-supported-movement
    - required-protection-continuity-not-maintained

required_capabilities:
  mandatory:
    - ProtectionCapability
    - MobilityCapability
    - PerceptionCapability
    - CommunicationCapability
  optional:
    - SurveyCapability
    - DetectionCapability
    - TrackingCapability
    - EngagementCapability
    - InterdictionCapability

traceability:
  task_candidates:
    - TC-001
    - TC-002
    - TC-004
    - TC-012
    - TC-016
    - TC-023
    - TC-025
    - TC-026
    - TC-028
    - TC-036
    - TC-039
  ontology_concepts:
    - Corridor
    - Route
    - SpatialRegion
    - PlatformGroup
  related_missions:
    - relation: enabled-by
      mission: MC-043
    - relation: supports
      mission: MC-044
    - relation: may-support
      mission: MC-045
```

### MC-047 — Resupply Maritime Force

```yaml
id: MC-047
name: Resupply Maritime Force
status: candidate
version: 0.1.0

classification:
  mission_type: MT-08
  primary_family: sustainment-and-force-support
  operational_intent: provide
  mission_target: platform-group

specification:
  purpose: >
    Restore or extend the endurance of a designated maritime force by providing the supplies,
    fuel, energy or consumables required for continued operations.
  description: >
    Assigned support assets rendezvous with the receiving force and transfer the authorized
    resources under the required safety and readiness conditions. Resupply may occur alongside,
    at anchor or while underway according to the supported force and available capabilities.
  applicable_contexts:
    - maritime-sustainment
    - extended-deployment
    - high-tempo-operations
    - distributed-operations
  preconditions:
    - receiving-force-and-requirements-defined
    - required-supplies-available
    - transfer-arrangements-established
    - rendezvous-or-support-location-defined
  desired_end_state: >
    The designated maritime force has received the required resources and can continue its
    assigned operation at the specified readiness and endurance level.
  success_criteria:
    - required-resources-transferred
    - receiving-force-endurance-restored-to-required-level
    - transfer-completed-under-required-safety-conditions
  failure_criteria:
    - critical-resource-not-transferred
    - receiving-force-remains-below-required-endurance
    - transfer-aborted-or-causes-unacceptable-damage

required_capabilities:
  mandatory:
    - LogisticsCapability
    - TransportCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - EnergySupplyCapability
    - DockingCapability
    - ManipulationCapability
    - MobilityCapability

traceability:
  task_candidates:
    - TC-001
    - TC-043
    - TC-050
    - TC-051
    - TC-052
    - TC-053
    - TC-054
    - TC-055
    - TC-039
  ontology_concepts:
    - PlatformGroup
    - Platform
    - Materiel
    - Payload
  related_missions:
    - relation: may-use
      mission: MC-048
    - relation: may-use
      mission: MC-049
```

### MC-048 — Transport Military Payload

```yaml
id: MC-048
name: Transport Military Payload
status: candidate
version: 0.1.0

classification:
  mission_type: MT-08
  primary_family: sustainment-and-force-support
  operational_intent: provide
  mission_target: physical-object

specification:
  purpose: >
    Move a designated military payload from an origin to a destination while preserving its
    required integrity, custody and availability.
  description: >
    An assigned carrier receives, secures and transports a military payload along an authorized
    route before transferring or making it available at the destination. The payload may be
    equipment, stores, mission modules or another transportable physical object.
  applicable_contexts:
    - maritime-logistics
    - force-deployment
    - distributed-operations
    - littoral-support
  preconditions:
    - payload-origin-and-destination-defined
    - payload-compatible-with-assigned-carrier
    - authorized-route-or-movement-area-defined
    - transfer-arrangements-established
  desired_end_state: >
    The designated payload is available at the required destination in the specified condition
    and within the required delivery window.
  success_criteria:
    - payload-delivered-to-required-destination
    - payload-integrity-and-custody-preserved
    - delivery-completed-within-required-window
  failure_criteria:
    - payload-not-delivered
    - payload-lost-damaged-or-compromised
    - delivery-window-missed

required_capabilities:
  mandatory:
    - TransportCapability
    - MobilityCapability
    - NavigationCapability
    - PayloadHostingCapability
  optional:
    - LogisticsCapability
    - ManipulationCapability
    - CommunicationCapability
    - ProtectionCapability

traceability:
  task_candidates:
    - TC-001
    - TC-023
    - TC-039
    - TC-051
    - TC-052
  ontology_concepts:
    - Payload
    - PhysicalObject
    - Platform
    - Route
  related_missions:
    - relation: may-support
      mission: MC-047
    - relation: broader-or-overlapping
      mission: MC-049
    - relation: may-support
      mission: MC-052
```

### MC-049 — Deliver Critical Materiel

```yaml
id: MC-049
name: Deliver Critical Materiel
status: candidate
version: 0.1.0

classification:
  mission_type: MT-08
  primary_family: sustainment-and-force-support
  operational_intent: provide
  mission_target: physical-object

specification:
  purpose: >
    Deliver designated critical materiel to a receiving force or location within the operational
    time window required to preserve mission continuity.
  description: >
    Assigned support assets collect, transport and transfer high-priority materiel whose delayed
    or failed delivery would materially affect the supported operation. Planning emphasizes
    priority, delivery assurance, receiving-force coordination and protection when required.
  applicable_contexts:
    - urgent-logistics
    - contested-logistics
    - maintenance-support
    - operational-recovery
  preconditions:
    - critical-materiel-and-priority-defined
    - receiving-force-or-location-defined
    - materiel-available-for-transfer
    - delivery-window-defined
  desired_end_state: >
    The critical materiel is transferred to the designated recipient in usable condition before
    the operational need can no longer be met.
  success_criteria:
    - critical-materiel-delivered-to-designated-recipient
    - materiel-delivered-in-usable-condition
    - operational-delivery-window-met
  failure_criteria:
    - critical-materiel-not-delivered
    - materiel-unusable-on-delivery
    - delivery-delay-compromises-supported-operation

required_capabilities:
  mandatory:
    - LogisticsCapability
    - TransportCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - ProtectionCapability
    - ManipulationCapability
    - MobilityCapability

traceability:
  task_candidates:
    - TC-001
    - TC-023
    - TC-039
    - TC-043
    - TC-051
    - TC-052
  ontology_concepts:
    - Materiel
    - PhysicalObject
    - Platform
  related_missions:
    - relation: specialization-of
      mission: MC-048
    - relation: may-support
      mission: MC-047
```

### MC-050 — Provide Communication Relay

```yaml
id: MC-050
name: Provide Communication Relay
status: candidate
version: 0.1.0

classification:
  mission_type: MT-08
  primary_family: sustainment-and-force-support
  operational_intent: provide
  mission_target: communication-service

specification:
  purpose: >
    Establish and maintain a communication relay service between designated participants that
    cannot otherwise exchange the required information with sufficient reliability.
  description: >
    An assigned relay platform or system establishes the required links, forwards authorized
    information and monitors service continuity for the specified participants, coverage area
    and operational period.
  applicable_contexts:
    - beyond-line-of-sight-communications
    - distributed-operations
    - degraded-communications-environment
    - joint-operations
  preconditions:
    - communication-participants-defined
    - relay-service-requirements-defined
    - compatible-communication-resources-available
    - relay-position-or-coverage-area-defined
  desired_end_state: >
    The designated participants can exchange the required information through a relay service
    that meets the specified coverage, availability and continuity requirements.
  success_criteria:
    - required-relay-links-established
    - authorized-information-forwarded
    - service-continuity-maintained-for-required-period
  failure_criteria:
    - required-participant-remains-unreachable
    - relay-service-below-required-availability
    - information-forwarding-fails-or-is-compromised

required_capabilities:
  mandatory:
    - RelayCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - MobilityCapability
    - StationKeepingCapability
    - SelfMonitoringCapability

traceability:
  task_candidates:
    - TC-005
    - TC-039
    - TC-043
    - TC-044
    - TC-045
    - TC-046
    - TC-062
  ontology_concepts:
    - CommunicationDevice
    - Platform
  related_missions:
    - relation: may-support
      mission: MC-044
    - relation: may-support
      mission: MC-045
    - relation: may-support
      mission: MC-051
```

### MC-051 — Provide Navigation Support

```yaml
id: MC-051
name: Provide Navigation Support
status: candidate
version: 0.1.0

classification:
  mission_type: MT-08
  primary_family: sustainment-and-force-support
  operational_intent: provide
  mission_target: route

specification:
  purpose: >
    Enable a designated force to navigate an assigned route or operating area with the required
    positional confidence and movement safety.
  description: >
    Supporting assets provide route, position, guidance or environmental information needed by
    the supported force. They may establish reference information, relay updates, monitor route
    conditions and report changes affecting safe or accurate navigation.
  applicable_contexts:
    - degraded-navigation-environment
    - littoral-navigation
    - convoy-or-group-movement
    - route-preparation
  preconditions:
    - supported-force-and-route-defined
    - navigation-support-requirements-defined
    - required-reference-or-route-information-available
    - communication-arrangements-established
  desired_end_state: >
    The supported force has the information and service continuity required to navigate the
    designated route or area within the specified accuracy and safety constraints.
  success_criteria:
    - required-navigation-information-provided
    - supported-force-maintains-required-positional-confidence
    - relevant-route-changes-reported
  failure_criteria:
    - required-navigation-information-unavailable
    - positional-confidence-below-required-threshold
    - unreported-route-change-compromises-supported-movement

required_capabilities:
  mandatory:
    - NavigationCapability
    - CommunicationCapability
    - PositionEstimationCapability
  optional:
    - RelayCapability
    - CoordinationCapability
    - PerceptionCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-019
    - TC-021
    - TC-039
    - TC-040
    - TC-043
    - TC-044
    - TC-045
    - TC-046
    - TC-047
    - TC-062
  ontology_concepts:
    - Route
    - SpatialRegion
    - CommunicationDevice
    - Platform
  related_missions:
    - relation: supported-by
      mission: MC-050
    - relation: may-support
      mission: MC-043
    - relation: may-support
      mission: MC-046
```

### MC-052 — Deploy Uncrewed Systems

```yaml
id: MC-052
name: Deploy Uncrewed Systems
status: candidate
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: sustainment-and-force-support
  operational_intent: support
  mission_target: platform-group

specification:
  purpose: >
    Place one or more uncrewed systems into their required operating environment and condition
    so that they can support an assigned operation.
  description: >
    A carrier or support force prepares, launches or transfers designated uncrewed systems,
    establishes required control or communication arrangements and confirms that the deployed
    systems are available for their assigned activities.
  applicable_contexts:
    - distributed-sensing
    - mine-warfare
    - maritime-surveillance
    - contested-environment
  preconditions:
    - uncrewed-systems-and-deployment-area-defined
    - systems-ready-for-deployment
    - carrier-or-launch-arrangement-available
    - control-and-communication-arrangements-established
  desired_end_state: >
    The designated uncrewed systems are deployed in the required operating area, responsive to
    the assigned control arrangements and available to perform their intended activities.
  success_criteria:
    - required-uncrewed-systems-deployed
    - deployed-systems-operationally-available
    - required-control-and-communication-links-established
  failure_criteria:
    - required-system-not-deployed
    - deployed-system-not-operationally-available
    - control-or-communication-arrangement-not-established

required_capabilities:
  mandatory:
    - DeploymentCapability
    - SupportCapability
    - CommunicationCapability
    - CoordinationCapability
  optional:
    - TransportCapability
    - PayloadHostingCapability
    - ManipulationCapability
    - MobilityCapability

traceability:
  task_candidates:
    - TC-001
    - TC-038
    - TC-039
    - TC-042
    - TC-043
    - TC-046
    - TC-048
    - TC-051
  ontology_concepts:
    - UncrewedSurfaceVehicle
    - AutonomousUnderwaterVehicle
    - UncrewedAerialVehicle
    - Platform
  related_missions:
    - relation: may-use
      mission: MC-048
    - relation: precedes
      mission: MC-053
```

### MC-053 — Recover Uncrewed System

```yaml
id: MC-053
name: Recover Uncrewed System
status: candidate
version: 0.1.0

classification:
  mission_type: MT-07
  primary_family: sustainment-and-force-support
  operational_intent: recover
  mission_target: platform

specification:
  purpose: >
    Retrieve a designated uncrewed system from its operating environment and return it to a
    specified safe, controlled or transportable condition.
  description: >
    Assigned recovery assets locate and approach the designated system, establish control when
    possible, retrieve or dock it, and transfer it to the required receiving platform or location.
  applicable_contexts:
    - post-mission-recovery
    - system-malfunction
    - contested-environment
    - maritime-logistics
  preconditions:
    - uncrewed-system-designated-for-recovery
    - last-known-location-or-search-area-available
    - compatible-recovery-asset-assigned
    - receiving-platform-or-location-defined
  desired_end_state: >
    The designated uncrewed system is under friendly control at the required receiving platform
    or location and is no longer exposed in the operating environment.
  success_criteria:
    - designated-system-located
    - system-retrieved-or-docked
    - system-transferred-to-required-receiving-condition
  failure_criteria:
    - designated-system-not-located
    - recovery-attempt-unsuccessful
    - system-lost-or-damaged-beyond-acceptable-limit

required_capabilities:
  mandatory:
    - RecoveryCapability
    - LocalizationCapability
    - MobilityCapability
    - CommunicationCapability
  optional:
    - TrackingCapability
    - DockingCapability
    - ManipulationCapability
    - TransportCapability

traceability:
  task_candidates:
    - TC-008
    - TC-016
    - TC-039
    - TC-049
    - TC-050
    - TC-051
    - TC-052
    - TC-057
  ontology_concepts:
    - UncrewedSurfaceVehicle
    - AutonomousUnderwaterVehicle
    - UncrewedAerialVehicle
    - Platform
  related_missions:
    - relation: follows
      mission: MC-052
    - relation: may-require
      mission: MC-063
```

### MC-054 — Conduct Electronic Surveillance

```yaml
id: MC-054
name: Conduct Electronic Surveillance
status: candidate
version: 0.1.0

classification:
  mission_type: MT-01
  primary_family: electromagnetic-and-information-activities
  operational_intent: conduct
  mission_target: area

specification:
  purpose: >
    Acquire and maintain awareness of relevant electromagnetic activity within a designated
    operating area and period.
  description: >
    Assigned assets monitor the radio-frequency environment, detect and characterize relevant
    emissions, associate them with sources when possible, and report changes or activity of
    operational interest without prescribing a subsequent effect.
  applicable_contexts:
    - maritime-domain-awareness
    - threat-warning
    - force-protection
    - operational-environment-preparation
  preconditions:
    - surveillance-area-and-period-defined
    - electronic-surveillance-objectives-defined
    - suitable-sensors-available
    - reporting-arrangements-established
  desired_end_state: >
    Relevant electromagnetic activity in the designated area is detected, characterized and
    reported to the required level of confidence and continuity.
  success_criteria:
    - required-electromagnetic-coverage-achieved
    - relevant-emissions-detected-and-characterized
    - significant-electromagnetic-activity-reported
  failure_criteria:
    - required-coverage-not-achieved
    - significant-emission-remains-undetected
    - collected-information-insufficient-for-required-awareness

required_capabilities:
  mandatory:
    - ElectronicWarfareCapability
    - PerceptionCapability
    - DetectionCapability
    - CommunicationCapability
  optional:
    - LocalizationCapability
    - ClassificationCapability
    - IdentificationCapability
    - TrackingCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-011
    - TC-012
    - TC-013
    - TC-014
    - TC-015
    - TC-016
    - TC-017
    - TC-020
    - TC-021
    - TC-039
    - TC-062
  ontology_concepts:
    - RadioFrequencyPerception
    - RadioFrequencySensor
    - Sensor
    - Platform
    - SpatialRegion
  related_missions:
    - relation: may-enable
      mission: MC-055
    - relation: may-enable
      mission: MC-057
    - relation: may-contribute-to
      mission: MC-018
```

### MC-055 — Conduct Electronic Attack

```yaml
id: MC-055
name: Conduct Electronic Attack
status: candidate
version: 0.1.0

classification:
  mission_type: MT-06
  primary_family: electromagnetic-and-information-activities
  operational_intent: conduct
  mission_target: physical-object

specification:
  purpose: >
    Apply authorized electromagnetic effects to degrade, deceive, disable or neutralize a
    designated adversary emitter, sensor or electronic system.
  description: >
    Assigned electronic-warfare assets identify the designated target, select an authorized
    effect and apply jamming or deceptive emissions for the required duration. They monitor the
    target response and assess whether the requested operational effect has been achieved.
  applicable_contexts:
    - high-intensity-warfare
    - force-protection
    - strike-support
    - contested-electromagnetic-environment
  preconditions:
    - electronic-attack-target-designated
    - target-sufficiently-identified
    - electronic-attack-authorized
    - suitable-effect-capability-available
  desired_end_state: >
    The designated adversary electronic system is degraded, deceived, disabled or neutralized
    to the degree and for the duration required by the supported operation.
  success_criteria:
    - authorized-electromagnetic-effect-applied
    - required-target-degradation-or-deception-achieved
    - effect-assessed-and-reported
  failure_criteria:
    - required-effect-not-achieved
    - target-remains-operationally-effective
    - unacceptable-interference-affects-friendly-or-protected-systems

required_capabilities:
  mandatory:
    - ElectronicWarfareCapability
    - IdentificationCapability
    - EngagementCapability
    - CommunicationCapability
  optional:
    - DetectionCapability
    - TrackingCapability
    - CoordinationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-012
    - TC-015
    - TC-016
    - TC-021
    - TC-039
    - TC-043
    - TC-063
    - TC-064
  ontology_concepts:
    - RadioFrequencySensor
    - CommunicationDevice
    - Sensor
    - PhysicalObject
  related_missions:
    - relation: enabled-by
      mission: MC-054
    - relation: may-support
      mission: MC-039
    - relation: broader-or-overlapping
      mission: MC-057
```

### MC-056 — Protect Friendly Communications

```yaml
id: MC-056
name: Protect Friendly Communications
status: candidate
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: electromagnetic-and-information-activities
  operational_intent: protect
  mission_target: communication-service

specification:
  purpose: >
    Preserve the availability, integrity and authorized use of designated friendly communication
    services against interference, disruption or electromagnetic attack.
  description: >
    Assigned assets monitor protected communication links and networks, detect degradation or
    hostile interference, coordinate protective measures and maintain or restore the required
    service level for designated users.
  applicable_contexts:
    - force-protection
    - degraded-communications-environment
    - contested-electromagnetic-environment
    - distributed-operations
  preconditions:
    - protected-communication-service-defined
    - required-service-level-defined
    - monitoring-and-protection-resources-available
    - authorized-users-and-priorities-defined
  desired_end_state: >
    The designated friendly communication service remains available to authorized users at the
    required level despite relevant interference or attack.
  success_criteria:
    - protected-service-meets-required-availability
    - harmful-interference-detected-and-handled
    - authorized-communications-preserved
  failure_criteria:
    - protected-service-falls-below-required-availability
    - authorized-users-lose-critical-connectivity
    - harmful-interference-remains-unhandled

required_capabilities:
  mandatory:
    - ProtectionCapability
    - CommunicationCapability
    - ElectronicWarfareCapability
    - SelfMonitoringCapability
  optional:
    - DetectionCapability
    - CoordinationCapability
    - RelayCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-005
    - TC-012
    - TC-021
    - TC-028
    - TC-039
    - TC-043
    - TC-044
    - TC-045
    - TC-062
  ontology_concepts:
    - CommunicationLink
    - CommunicationNetwork
    - CommunicationDevice
    - RadioTransceiver
  related_missions:
    - relation: opposed-by
      mission: MC-057
    - relation: may-use
      mission: MC-050
```

### MC-057 — Disrupt Adversary Communications

```yaml
id: MC-057
name: Disrupt Adversary Communications
status: candidate
version: 0.1.0

classification:
  mission_type: MT-05
  primary_family: electromagnetic-and-information-activities
  operational_intent: interdict
  mission_target: communication-service

specification:
  purpose: >
    Prevent or constrain designated adversary participants from using a communication service
    effectively during a specified operational period.
  description: >
    Assigned electronic-warfare assets identify relevant adversary communication activity and
    apply authorized jamming or deceptive emissions. They monitor service degradation and adapt
    the effect while limiting interference with friendly or protected communications.
  applicable_contexts:
    - command-and-control-disruption
    - force-protection
    - high-intensity-warfare
    - contested-electromagnetic-environment
  preconditions:
    - adversary-communication-service-designated
    - disruption-effect-and-period-defined
    - disruption-authorized
    - suitable-electronic-warfare-assets-available
  desired_end_state: >
    The designated adversary communication service cannot support effective operational use for
    the required period, without unacceptable impact on protected communications.
  success_criteria:
    - required-adversary-service-degradation-achieved
    - disruption-maintained-for-required-period
    - protected-communications-remain-within-authorized-impact-limits
  failure_criteria:
    - adversary-service-remains-operationally-effective
    - disruption-cannot-be-maintained
    - unacceptable-interference-affects-protected-communications

required_capabilities:
  mandatory:
    - InterdictionCapability
    - ElectronicWarfareCapability
    - CommunicationCapability
  optional:
    - DetectionCapability
    - IdentificationCapability
    - TrackingCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-012
    - TC-015
    - TC-016
    - TC-021
    - TC-026
    - TC-039
    - TC-063
    - TC-064
  ontology_concepts:
    - CommunicationLink
    - CommunicationNetwork
    - CommunicationDevice
    - RadioTransceiver
  related_missions:
    - relation: enabled-by
      mission: MC-054
    - relation: opposed-by
      mission: MC-056
    - relation: specialization-of
      mission: MC-055
```

### MC-058 — Conduct Maritime Deception

```yaml
id: MC-058
name: Conduct Maritime Deception
status: candidate
version: 0.1.0

classification:
  mission_type: MT-09
  primary_family: electromagnetic-and-information-activities
  operational_intent: conduct
  mission_target: maritime-activity

specification:
  purpose: >
    Influence an adversary's understanding or decision process by presenting a controlled false,
    ambiguous or misleading representation of friendly maritime activity.
  description: >
    Assigned forces coordinate observable actions, emissions, information or physical signatures
    intended to create a specified adversary perception. Execution is monitored and adjusted to
    support the protected operation without compromising friendly intent.
  applicable_contexts:
    - force-protection
    - manoeuvre-support
    - strike-support
    - contested-information-environment
  preconditions:
    - deception-objective-and-audience-defined
    - desired-adversary-perception-defined
    - deception-plan-authorized
    - observable-actions-or-signatures-available
  desired_end_state: >
    The adversary acts, delays or allocates attention in a manner that supports the friendly
    operation, while the protected friendly intent remains acceptably concealed.
  success_criteria:
    - planned-deception-signatures-presented
    - indicators-support-desired-adversary-perception
    - protected-friendly-intent-not-unacceptably-exposed
  failure_criteria:
    - deception-signatures-not-presented-as-planned
    - adversary-behaviour-inconsistent-with-required-effect
    - deception-compromises-protected-friendly-operation

required_capabilities:
  mandatory:
    - SupportCapability
    - CoordinationCapability
    - CommunicationCapability
  optional:
    - ElectronicWarfareCapability
    - DeploymentCapability
    - AssessmentCapability
    - MobilityCapability

traceability:
  task_candidates:
    - TC-021
    - TC-038
    - TC-039
    - TC-040
    - TC-043
    - TC-046
    - TC-063
    - TC-064
  ontology_concepts:
    - Decoy
    - CommunicationDevice
    - Platform
    - PhysicalObject
  related_missions:
    - relation: may-use
      mission: MC-059
    - relation: may-support
      mission: MC-039
    - relation: may-support
      mission: MC-040
```

### MC-059 — Deploy Decoy

```yaml
id: MC-059
name: Deploy Decoy
status: candidate
version: 0.1.0

classification:
  mission_type: MT-04
  primary_family: electromagnetic-and-information-activities
  operational_intent: support
  mission_target: physical-object

specification:
  purpose: >
    Protect a designated friendly force or activity by placing a decoy where it can create the
    required false signature, attraction or ambiguity.
  description: >
    An assigned platform transports and deploys a designated decoy at the required location and
    time, activates or configures its observable signature when applicable, and confirms that it
    contributes to the intended protective or deceptive effect.
  applicable_contexts:
    - force-protection
    - threat-deflection
    - maritime-deception
    - contested-environment
  preconditions:
    - protected-force-or-activity-defined
    - decoy-and-deployment-location-defined
    - intended-protective-effect-defined
    - compatible-deployment-platform-available
  desired_end_state: >
    The decoy is deployed and presents the required signature or attraction so that exposure of
    the protected force or activity is reduced to the specified level.
  success_criteria:
    - decoy-deployed-at-required-location-and-time
    - required-decoy-signature-or-effect-established
    - protected-force-exposure-reduced-as-required
  failure_criteria:
    - decoy-not-deployed
    - decoy-fails-to-present-required-effect
    - deployment-increases-risk-to-protected-force

required_capabilities:
  mandatory:
    - ProtectionCapability
    - DeploymentCapability
    - SupportCapability
  optional:
    - ElectronicWarfareCapability
    - TransportCapability
    - CommunicationCapability
    - AssessmentCapability

traceability:
  task_candidates:
    - TC-001
    - TC-021
    - TC-038
    - TC-039
    - TC-043
    - TC-048
    - TC-049
    - TC-064
  ontology_concepts:
    - Decoy
    - PhysicalObject
    - Platform
  related_missions:
    - relation: may-support
      mission: MC-058
    - relation: may-support
      mission: MC-028
```



## 13. Changes v1.0.3 → v1.0.4

- Confirmed the section 5 inventory as the authoritative source for mission identities MC-001 through MC-066.
- Normalized MC-034 through MC-038 to the canonical mission schema.
- Added canonical specifications for MC-039 through MC-041 by reusing relevant material from the divergent proposals under their correct mission identities.
- Added canonical specifications for the Littoral and Amphibious Support family MC-042 through MC-046.
- Added canonical specifications for the Sustainment and Force Support family MC-047 through MC-053.
- Added canonical specifications for the Electromagnetic and Information Activities family MC-054 through MC-059.
- Replaced free-text task references in MC-034 through MC-038 with stable Task Catalog identifiers.
- Replaced unavailable capability and ontology references with concepts defined by the current Naval Ontology.
- Isolated the conflicting former MC-039 through MC-066 blocks as non-normative legacy proposals pending reassignment or reuse.

## Appendix A — Archived divergent mission proposals

The blocks below are preserved as non-normative source material. Their former `MC-NNN` mappings conflict with the canonical mission identities in section 5 and shall not be treated as active Mission Catalog entries.

### Legacy proposal formerly mapped to MC-039 — Conduct Naval Fire Support

```yaml
legacy_source_id: MC-039
name: Conduct Naval Fire Support
status: draft

mission_family: Naval Combat
mission_type: Offensive Support
operational_intent: Support
mission_target: Shore Objective

purpose: >
  Deliver accurate and timely naval fires in support of friendly forces operating ashore.

description: >
  Naval platforms provide planned or responsive fire support against designated land targets
  to enable friendly manoeuvre, suppress enemy positions or destroy critical objectives.

applicable_contexts:
  - Amphibious Operations
  - Littoral Warfare
  - High Intensity Warfare

preconditions:
  - Fire support request approved.
  - Targets designated.
  - Weapons available.

desired_end_state:
  - Requested fires delivered.
  - Supported force enabled to accomplish its mission.

success_criteria:
  - Fire missions executed within required accuracy and timing.
  - Supported force objectives facilitated.

failure_criteria:
  - Fires ineffective or delayed.
  - Excessive collateral damage.

required_capabilities:
  - FireControlCapability
  - SurfaceStrikeCapability
  - CommunicationCapability

optional_capabilities:
  - TargetingCapability
  - BattleDamageAssessmentCapability

task_candidates:
  - Coordinate
  - Identify
  - Assign
  - Engage
  - Assess
  - Report

ontology_concepts:
  - ShoreTarget
  - WeaponSystem

related_missions:
  - MC-040
  - MC-041
```



### Legacy proposal formerly mapped to MC-040 — Conduct Precision Strike

```yaml
legacy_source_id: MC-040
name: Conduct Precision Strike
status: draft

mission_family: Naval Combat
mission_type: Offensive Action
operational_intent: Strike
mission_target: High-Value Target

purpose: >
  Deliver a precise strike against a designated high-value target while minimizing collateral damage.

description: >
  Assigned forces detect, identify and engage a designated target using precision-guided
  effects in accordance with mission objectives and Rules of Engagement.

applicable_contexts:
  - High Intensity Warfare
  - Littoral Warfare
  - Joint Operations

preconditions:
  - Target positively identified.
  - Strike authorized.
  - Precision weapons available.

desired_end_state:
  - Designated target neutralized.
  - Collateral damage minimized.

success_criteria:
  - Target neutralized with required precision.
  - Mission objectives achieved.

failure_criteria:
  - Target survives.
  - Excessive collateral damage.

required_capabilities:
  - PrecisionStrikeCapability
  - TargetingCapability
  - FireControlCapability
  - CommunicationCapability

optional_capabilities:
  - BattleDamageAssessmentCapability
  - CooperativeEngagementCapability

task_candidates:
  - Detect
  - Identify
  - Assign
  - Engage
  - Assess
  - Report

ontology_concepts:
  - HighValueTarget
  - WeaponSystem

related_missions:
  - MC-039
  - MC-041
```

### Legacy proposal formerly mapped to MC-041 — Neutralize Time-Sensitive Target

```yaml
legacy_source_id: MC-041
name: Neutralize Time-Sensitive Target
status: draft
purpose: Neutralize a time-sensitive target before the engagement opportunity is lost.
task_candidates:
  - Detect
  - Identify
  - Assign
  - Engage
  - Assess
  - Report
related_missions:
  - MC-040
```

### Legacy proposal formerly mapped to MC-042 — Conduct Demonstration of Force

```yaml
legacy_source_id: MC-042
name: Conduct Demonstration of Force
status: draft
purpose: Demonstrate credible military capability to deter or influence an adversary.
task_candidates:
  - Navigate
  - Patrol
  - Observe
  - Report
related_missions:
  - MC-043
```

### Legacy proposal formerly mapped to MC-043 — Conduct Show of Presence

```yaml
legacy_source_id: MC-043
name: Conduct Show of Presence
status: draft
purpose: Maintain a visible naval presence to reassure friendly actors and deter hostile behaviour.
task_candidates:
  - Navigate
  - Patrol
  - Observe
  - Transmit
  - Report
related_missions:
  - MC-042
```

### Legacy proposal formerly mapped to MC-044 — Conduct Amphibious Landing Support

```yaml
legacy_source_id: MC-044
name: Conduct Amphibious Landing Support
status: draft
purpose: Support the landing of friendly amphibious forces.
task_candidates:
  - Navigate
  - Escort
  - Engage
  - Assist
  - Report
related_missions:
  - MC-039
```

### Legacy proposal formerly mapped to MC-045 — Secure Beachhead

```yaml
legacy_source_id: MC-045
name: Secure Beachhead
status: draft
purpose: Establish and maintain a secure beachhead for follow-on forces.
task_candidates:
  - Deploy
  - Establish
  - Defend
  - Engage
  - Report
related_missions:
  - MC-044
```

### Legacy proposal formerly mapped to MC-046 — Support Amphibious Maneuver

```yaml
legacy_source_id: MC-046
name: Support Amphibious Maneuver
status: draft
purpose: Support manoeuvre of amphibious forces from sea to inland objectives.
task_candidates:
  - Assist
  - Transport
  - Escort
  - Coordinate
  - Report
related_missions:
  - MC-044
  - MC-045
```

### Legacy proposal formerly mapped to MC-047 — Conduct Amphibious Withdrawal

```yaml
legacy_source_id: MC-047
name: Conduct Amphibious Withdrawal
status: draft
purpose: Safely withdraw amphibious forces from the objective area.
task_candidates:
  - Board
  - Escort
  - Defend
  - Report
  - Withdraw
related_missions:
  - MC-044
```

### Legacy proposal formerly mapped to MC-048 — Conduct Tactical Replenishment at Sea

```yaml
legacy_source_id: MC-048
name: Conduct Tactical Replenishment at Sea
status: draft
purpose: Sustain naval forces through tactical replenishment at sea.
task_candidates:
  - Approach
  - Coordinate
  - Transfer
  - Refuel
  - Resupply
  - Report
```

### Legacy proposal formerly mapped to MC-049 — Conduct Personnel Recovery

```yaml
legacy_source_id: MC-049
name: Conduct Personnel Recovery
status: draft
purpose: Recover isolated friendly personnel in a maritime environment.
task_candidates:
  - Search
  - Locate
  - Recover
  - Evacuate
  - Report
  - Stabilize
```

### Legacy proposal formerly mapped to MC-050 — Conduct Non-combatant Evacuation Support

```yaml
legacy_source_id: MC-050
name: Conduct Non-combatant Evacuation Support
status: draft
purpose: Support the evacuation of non-combatants from a threatened area.
task_candidates:
  - Board
  - Transport
  - Defend
  - Deploy
  - Report
related_missions:
  - MC-049
```

### Legacy proposal formerly mapped to MC-051 — Conduct Humanitarian Assistance Support

```yaml
legacy_source_id: MC-051
name: Conduct Humanitarian Assistance Support
status: draft
purpose: Support humanitarian assistance operations in the maritime domain.
task_candidates:
  - Navigate
  - Transport
  - Assist
  - Coordinate
  - Report
```

### Legacy proposal formerly mapped to MC-052 — Conduct Disaster Relief Support

```yaml
legacy_source_id: MC-052
name: Conduct Disaster Relief Support
status: draft
purpose: Support disaster relief operations following a natural or technological disaster.
task_candidates:
  - Navigate
  - Transport
  - Assist
  - Recover
  - Report
related_missions:
  - MC-051
```

### Legacy proposal formerly mapped to MC-053 — Conduct Medical Evacuation Support

```yaml
legacy_source_id: MC-053
name: Conduct Medical Evacuation Support
status: draft
purpose: Evacuate injured personnel to an appropriate medical facility.
task_candidates:
  - Locate
  - Recover
  - Transport
  - Assist
  - Report
  - Stabilize
related_missions:
  - MC-049
```

### Legacy proposal formerly mapped to MC-054 — Conduct Strategic Sealift Support

```yaml
legacy_source_id: MC-054
name: Conduct Strategic Sealift Support
status: draft
purpose: Transport personnel, equipment and supplies in support of strategic deployment.
task_candidates:
  - Transport
  - Coordinate
  - Report
```

### Legacy proposal formerly mapped to MC-055 — Conduct Maritime Logistics Support

```yaml
legacy_source_id: MC-055
name: Conduct Maritime Logistics Support
status: draft
purpose: Sustain maritime operations through logistics support.
task_candidates:
  - Transfer
  - Resupply
  - Refuel
  - Coordinate
  - Report
  - Recharge
related_missions:
  - MC-048
```

### Legacy proposal formerly mapped to MC-056 — Conduct Maintenance Support

```yaml
legacy_source_id: MC-056
name: Conduct Maintenance Support
status: draft
purpose: Restore or preserve operational availability of deployed assets.
task_candidates:
  - Assess
  - Assist
  - Recover
  - Report
  - Recharge
  - Tow
related_missions:
  - MC-055
```

### Legacy proposal formerly mapped to MC-057 — Conduct Electronic Warfare Support

```yaml
legacy_source_id: MC-057
name: Conduct Electronic Warfare Support
status: draft
purpose: Support operations through electronic warfare effects.
task_candidates:
  - Detect
  - Jam
  - Emit
  - Report
```

### Legacy proposal formerly mapped to MC-058 — Conduct Electromagnetic Surveillance

```yaml
legacy_source_id: MC-058
name: Conduct Electromagnetic Surveillance
status: draft
purpose: Monitor and characterize the electromagnetic environment.
task_candidates:
  - Detect
  - Classify
  - Characterize
  - Report
related_missions:
  - MC-057
```

### Legacy proposal formerly mapped to MC-059 — Conduct Information Collection Support

```yaml
legacy_source_id: MC-059
name: Conduct Information Collection Support
status: draft
purpose: Collect operationally relevant information for decision support.
task_candidates:
  - Search
  - Observe
  - Report
  - Share
```

### Legacy proposal formerly mapped to MC-060 — Conduct Communication Relay Support

```yaml
legacy_source_id: MC-060
name: Conduct Communication Relay Support
status: draft
purpose: Extend or maintain communications between dispersed forces.
task_candidates:
  - Relay
  - Transmit
  - Coordinate
  - Report
related_missions:
  - MC-059
```

### Legacy proposal formerly mapped to MC-061 — Conduct Deception Operations

```yaml
legacy_source_id: MC-061
name: Conduct Deception Operations
status: draft
purpose: Mislead an adversary regarding friendly intentions, capabilities or dispositions.
task_candidates:
  - Emit
  - Jam
  - Coordinate
  - Report
related_missions:
  - MC-057
```

### Legacy proposal formerly mapped to MC-062 — Conduct Cyber Defence Support

```yaml
legacy_source_id: MC-062
name: Conduct Cyber Defence Support
status: draft
purpose: Protect mission-critical systems against cyber threats during operations.
task_candidates:
  - Detect
  - Monitor
  - Assess
  - Report
related_missions:
  - MC-057
```

### Legacy proposal formerly mapped to MC-063 — Conduct Maritime Interdiction Support

```yaml
legacy_source_id: MC-063
name: Conduct Maritime Interdiction Support
status: draft
purpose: Support maritime interdiction operations against designated vessels.
task_candidates:
  - Intercept
  - Hail
  - Board
  - Inspect
  - Report
related_missions:
  - MC-021
  - MC-022
```

### Legacy proposal formerly mapped to MC-064 — Conduct Visit, Board, Search and Seizure (VBSS)

```yaml
legacy_source_id: MC-064
name: Conduct Visit, Board, Search and Seizure (VBSS)
status: draft
purpose: Board, inspect and, when authorized, seize a vessel in accordance with applicable rules.
task_candidates:
  - Intercept
  - Hail
  - Board
  - Inspect
  - Seize
  - Report
related_missions:
  - MC-063
```

### Legacy proposal formerly mapped to MC-065 — Conduct Training Support

```yaml
legacy_source_id: MC-065
name: Conduct Training Support
status: draft
purpose: Support training and experimentation activities in a representative operational environment.
task_candidates:
  - Deploy
  - Coordinate
  - Monitor
  - Assess
  - Report
related_missions:
  - MC-001
```

### Legacy proposal formerly mapped to MC-066 — Conduct Experimentation Support

```yaml
legacy_source_id: MC-066
name: Conduct Experimentation Support
status: draft
purpose: Support experimentation, validation and evaluation of new concepts, systems or tactics.
task_candidates:
  - Deploy
  - Monitor
  - Measure
  - Assess
  - Report
related_missions:
  - MC-065
```
