---
name: safety-management
description: >
  Comprehensive safety management system for construction projects. Handles incident tracking, OSHA reporting (300/300A/301), toolbox talks, JSA/JHA creation, site safety inspections, permits, emergency planning, and safety metrics/KPIs. Integrates with schedule for activity-based hazards and daily reports for safety observations. Triggers: "incident", "near miss", "toolbox talk", "jsa", "jha", "job safety analysis", "inspection", "osha", "recordable", "first aid", "hot work", "confined space", "permit", "safety metrics", "trir", "dart", "emr", "emergency plan", "safety meeting".
version: 1.0.0
---

# Safety Management Skill

## Overview

The **safety-management** skill provides systematic construction safety management for superintendents managing OSHA compliance, incident tracking, safety communications (toolbox talks), hazard analysis (JSAs), site inspections, and safety metrics. It enables comprehensive documentation of safety performance from incident tracking through OSHA 300/301/300A recordkeeping and leading/lagging indicator dashboards.

---

## Incident Tracking & Reporting Workflow

### Incident Types & Classification

All on-site injuries, illnesses, and near-misses are classified by severity and recordability for proper tracking and OSHA compliance.

#### 1. **Recordable Incidents (OSHA 300 Log)**

**Definition**: Incidents meeting OSHA 300 Log criteria per 29 CFR 1904:
- Work-related injury or illness involving medical treatment (beyond first aid)
- Restricted work activity or job transfer
- Days away from work
- Loss of consciousness
- Significant injury or illness diagnosed by healthcare provider

**Examples**:
- Laceration requiring stitches at urgent care
- Sprain resulting in restricted duty (light duty, modified work)
- Heat exhaustion requiring medical evaluation and 2 days away from work
- Chemical burn requiring medical treatment
- Fracture or concussion
- Significant back strain diagnosed as strain/sprain requiring therapy
- Eye injury from foreign object requiring treatment

**Recording Process**:
- Immediately report to safety manager/superintendent
- Complete OSHA 300 form (see **OSHA Recordkeeping** section)
- Complete OSHA 301 incident report form
- Link to daily report with date and description
- Mark for **300A Annual Summary** if applicable
- Track in `safety-log.json` recordable_incidents array

**OSHA Recordability Determination**:
The **recordability decision tree** below helps classify incidents:

```
INCIDENT OCCURS
    │
    ├─ Work-related? (did job/work environment cause or aggravate?)
    │   ├─ NO → Not recordable; document as non-work-related
    │   └─ YES ↓
    ├─ Medical treatment provided (beyond first aid)?
    │   ├─ NO → First aid only; check other criteria
    │   └─ YES → RECORDABLE ✓
    ├─ Restricted duty / job transfer?
    │   ├─ NO → Not recordable
    │   └─ YES → RECORDABLE ✓
    ├─ Days away from work?
    │   ├─ 0 days → Not recordable
    │   └─ ≥1 days away → RECORDABLE ✓
    ├─ Diagnosed illness (medical professional)?
    │   ├─ NO → May still be first aid
    │   └─ YES → RECORDABLE ✓
    └─ Loss of consciousness?
        ├─ NO → Check other criteria
        └─ YES → RECORDABLE ✓
```

**First Aid vs. Medical Treatment Distinction**:

First aid (NOT recordable):
- Bandages, gauze, tape
- Elastic supports, slings, braces (non-rigid)
- Temporary splints for transport to medical care
- Cleaning wounds with soap/water or antiseptic
- Non-prescription medications (topical antibiotic, pain reliever)
- Eye irrigation (irritant removal)
- Assessment/observation without care

Medical treatment (RECORDABLE):
- Sutures or steri-strips
- Urgent care/emergency department visit
- Prescription medications
- X-rays
- Surgery
- Casts
- Injections (vaccines, medication)
- Therapy (physical, mental health)
- Any healthcare professional diagnosis/treatment

#### 2. **Near-Miss Incidents**

**Definition**: Incidents that could have resulted in injury but did not; incidents with potential for serious harm.

**Examples**:
- Unplanned fall from 4 feet onto foam pads (no injury, near-serious)
- Near-contact with power line while erecting scaffolding (hazard avoided by spotter)
- Trench nearly collapsed during excavation; shoring prevented it
- Equipment nearly struck worker (spotter intervened)
- Chemical spill contained before skin contact

**Reporting Process**:
- Encourage crew to report near-misses (no retaliation)
- Document in daily report with date and description
- Include in safety-log.json near_misses array
- Track near-miss ratio (near-miss to incident ratio; higher ratio indicates good safety culture)
- Use near-misses to trigger JSA review and corrective actions
- Near-miss ratio of 5:1 or better indicates effective safety program

**Near-Miss Documentation**:
```json
{
  "id": "NEAR-MISS-001",
  "date": "2026-02-16",
  "time": "14:30",
  "location": "Structural steel erection area, Bay 3-4",
  "description": "During PEMB erection, momentary loss of guy-wire tension caused beam drift. Spotter noticed and halted lift. Operator re-checked tension and resumed. No employee exposure.",
  "potential_severity": "critical",
  "craft_involved": ["ironworker", "crane_operator"],
  "potential_consequence": "Falling steel beam; potential fatality",
  "root_cause": "Guy-wire tension not verified by both operator and spotter before lift",
  "corrective_actions": [
    "PEMB erection procedure updated: require written sign-off by both operator and spotter after tension check",
    "Toolbox talk held same day on critical lifts",
    "Daily safety meeting point: lifting safety protocols"
  ],
  "closed_date": "2026-02-18"
}
```

#### 3. **First Aid Log**

**Definition**: Minor injuries receiving first aid treatment only; not recordable on OSHA 300 log.

**Examples**:
- Minor laceration with bandage and topical antibiotic
- Minor burn with topical treatment
- Bruise, abrasion cleaned and bandaged
- Muscle soreness not requiring medical intervention
- Splinter removal
- Reaction to insect bite

**First Aid Documentation**:
- Minor injuries tracked separately from recordable incidents
- Documented in safety-log.json first_aid_log array
- Linked to daily report
- Used to monitor trends (repeated injuries in same area = hazard)
- First aid log supports argument for strong safety culture if many near-misses and first aid incidents are reported

**First Aid Log Entry**:
```json
{
  "id": "FIRST-AID-001",
  "date": "2026-02-15",
  "employee_name": "[redacted - privacy]",
  "craft": "carpenter",
  "injury_type": "minor laceration",
  "body_part": "right hand",
  "description": "Cut on hand while removing form work. Self-reported to first aid station. Cleaned with soap and water, antibiotic ointment applied, bandaged.",
  "treatment_provided": "Cleaning, bandage, antibiotic ointment",
  "location": "Formwork removal, Bay 2",
  "witness": "Crew foreman",
  "first_aid_provider": "On-site first aid trained staff",
  "linked_daily_report": "2026-02-15",
  "notes": "Proper tool usage protocol reviewed with crew"
}
```

### Incident Investigation Workflow

**Step 1: Immediate Response**
- Isolate hazard/scene if safe to do so
- Provide medical care (first aid or call 911 for serious injuries)
- Notify superintendent and safety manager
- Document scene with photos before alterations
- Preserve evidence (failed equipment, materials, etc.)
- Begin preliminary investigation within 2 hours

**Step 2: Injury Assessment**
- Determine if work-related
- Assess severity (first aid, medical treatment, hospitalization, fatality)
- Identify if potentially recordable
- Document medical treatment facility (if applicable)
- Collect employee statement

**Step 3: Root Cause Analysis**

**STEP 1: Define the Incident**
What exactly happened? Document observable facts:
- Date, time, location
- Employees involved
- Work activity being performed
- Equipment/materials involved
- Immediate injury/damage

**Example**:
```
Incident: Employee fell from 6-foot ladder while installing light fixture.
Date: 2026-02-16, 10:45 AM
Location: Mechanical room, north wall
Employee: Carpenter (experienced)
Activity: Installing electrical light fixture in ceiling cavity
Equipment: 6-foot aluminum ladder, work light
Injury: Laceration to right forehead (3 stitches), possible mild concussion
```

**STEP 2: Identify Direct Causes (What)**

Direct causes are the immediate conditions or actions that directly resulted in the incident.

**Categories**:
- **Unsafe Condition**: Equipment failure, inadequate guarding, hazardous material, environmental condition
- **Unsafe Act**: Worker behavior, procedure violation, improper tool use, failure to use PPE

**Questioning Process**:
- What failed or went wrong?
- What was the worker doing?
- What tool/equipment was being used?
- What PPE should have been used?
- What guards or safeguards were missing?

**Example**:
```
Direct Causes:
  1. Ladder not secured/stabilized (no one holding base, not on level surface)
  2. Worker reached beyond ladder width (unstable position)
  3. Work light used instead of hands-free task light (balance/visibility issue)
  4. No fall protection (harness/lanyard) used for 6-foot height
  5. No safety briefing before climbing ladder at that height
```

**STEP 3: Identify Root Causes (Why)**

Root causes are the underlying reasons why the direct causes occurred. Ask "Why?" multiple times (5 Whys Method):

```
Level 1: Why did the ladder tip?
  → Ladder was not secured/stabilized

Level 2: Why was ladder not secured?
  → No one available to hold base; single-person task

Level 3: Why was there no second person assigned?
  → Supervisor did not assess job hazard requirements
  → No JSA completed for electrical fixture installation

Level 4: Why was no JSA completed?
  → Electrical work is routine (supervisor assumption)
  → No procedure requiring JSA for all elevated work

Level 5: Why was there no procedure requiring JSA?
  → Company safety program did not mandate JSA for all work over 4 feet
  → Lack of formal safety program enforcement
```

**Root Causes Identified**:
1. **Inadequate job planning**: No JSA for elevated task
2. **Lack of procedure**: No mandatory JSA for work > 4 feet
3. **Supervisor judgment**: Assumed low-risk task did not require fall protection
4. **Training gap**: Supervisor not trained on fall protection requirements for ladders
5. **System issue**: Safety program not consistently enforced

**STEP 4: Identify Contributing Factors**

Contributing factors are secondary conditions that worsened the incident or prevented mitigation:
- Time pressure (task rushed)
- Fatigue (long hours, previous incidents)
- Environmental (poor lighting, wet surfaces, temperature)
- Communication breakdown
- Previous near-misses ignored
- Maintenance defect (broken equipment)

**Example Contributing Factors**:
```
1. Work light dimmed by dust on lens (visibility degraded)
2. Supervisor called away to address another issue (no supervision during ladder work)
3. Employee worked alone (no second person to assist/observe)
4. High heat in mechanical room (fatigue factor)
5. Previous incident same week (normalizing risk)
```

**STEP 5: Corrective Actions**

Corrective actions address root causes to prevent recurrence. They should be:
- **Specific**: Not vague; clearly defined
- **Assignable**: Assigned to responsible person with deadline
- **Measurable**: Can verify completion
- **Timely**: Implement before similar work resumes

**Action Types** (Hierarchy of Controls):
1. **Eliminate the hazard**: Remove the task or hazard entirely (best)
2. **Substitute**: Replace with less hazardous method/material
3. **Engineering control**: Redesign equipment, install guardrail, improve lighting
4. **Administrative control**: Procedure, training, supervision, JSA requirement
5. **PPE**: Last resort; personal protective equipment alone (worst)

**Example Corrective Actions**:
```
ROOT CAUSE 1: No JSA completed
  ACTION: Develop and implement JSA for "Electrical fixture installation from ladder"
    Requirement: All work ≥4 feet requires JSA before start
    Responsible: Safety Manager
    Deadline: 2026-02-20
    Verification: Post JSA on job board; supervisor initials before work

ROOT CAUSE 2: Supervisor not trained on fall protection
  ACTION: Provide fall protection training to all supervisors (OSHA standard 1926.500)
    Content: Fall hazard identification, ladder safety, harness use, anchor points
    Responsible: HR/Safety Manager
    Deadline: 2026-03-10
    Verification: Training attendance log; competency assessment

ROOT CAUSE 3: Inadequate fall protection on ladder work
  ACTION: Procure extension ladder stabilizers and require for all work >6 feet
    Install ladder stabilizers on all extension ladders
    Responsible: Site Supervisor
    Deadline: 2026-02-22
    Verification: Equipment inventory; daily pre-use inspection

ROOT CAUSE 4: Single-worker task
  ACTION: Require second person as spotter for any ladder work >4 feet
    Policy: No solo ladder work; spotter must be present
    Responsible: Foreman
    Deadline: Immediate
    Verification: Daily toolbox talk; crew acknowledgment

ROOT CAUSE 5: No JSA program enforcement
  ACTION: Mandatory JSA requirement integrated into work planning
    Procedure: All new activities require written JSA before work begins
    Responsible: Project Management
    Deadline: 2026-03-01
    Verification: Daily report includes JSA status; toolbox talks reference JSA
```

**STEP 6: Documentation & Communication**

Incident investigation report documents the full analysis:

**Report Structure**:
```
INCIDENT INVESTIGATION REPORT
Project: Morehead One Senior Care
Date of Incident: 2026-02-16
Report Date: 2026-02-18
Investigator: [Superintendent Name]

INCIDENT SUMMARY:
  Describe what happened in objective, factual terms (1-2 paragraphs)

DIRECT CAUSES:
  List immediate conditions/actions that caused incident

ROOT CAUSES:
  5 Whys analysis; underlying system/procedural failures

CONTRIBUTING FACTORS:
  Secondary conditions that worsened severity

CORRECTIVE ACTIONS:
  ✓ Action description
  ✓ Root cause addressed
  ✓ Responsible person & deadline
  ✓ Verification method

EMPLOYEE STATEMENT:
  Employee's account of what happened (if applicable)

WITNESS STATEMENTS:
  Any witnesses present during/shortly after incident

PHOTOS/EVIDENCE:
  Scene photos, equipment inspection, material samples

DISTRIBUTION:
  Safety Manager, Project Manager, Owner, Subcontractor, Foreman
```

## Project Intelligence Integration

When project intelligence is loaded, auto-enrich safety management with spec-based hazard data, location context, and subcontractor safety profiles.

### Activity-Based Weather Alerts
When today's weather is known and outdoor work is active:
- Read `specs-quality.json` → `weather_thresholds[]` → check all active work types
- Cross-reference today's temperature, wind, and precipitation against each threshold
- Auto-flag if any threshold is exceeded: "Cold weather alert: Concrete placement today at 35°F — below 40°F minimum per Spec 03 30 00. Cold weather measures required."
- Include `mitigation_measures` from the spec in the alert
- Surface weather alerts in `/morning-brief` and `/daily-report` safety sections

### Safety Zone Mapping
When creating JSAs or conducting safety inspections:
- Read `specs-quality.json` → `safety` → pull `fall_protection_zones[]`, `confined_spaces[]`, `hot_work_areas[]`, `crane_exclusion_zones[]`, `overhead_power_lines[]`
- Auto-populate JSA location hazards based on the work area's proximity to safety zones
- Example: Work at Grid C-3 near `crane_exclusion_zones` → auto-include crane hazard in JSA

### Location-Based Hazard Context
When logging an incident or near-miss:
- Read `plans-spatial.json` → resolve incident location to grid reference using building_areas and room_schedule
- Read `plans-spatial.json` → `site_utilities` → identify nearby underground utilities (storm, sanitary, water, gas, electrical) for utility strike context
- Auto-include utility proximity data in incident investigation when the incident involves excavation or ground disturbance
- Example: Incident at Grid B-2 → site_utilities shows 6" gas line at Grid B-3 → flag proximity for root cause analysis

### Sub Safety Performance
When conducting pre-task planning or toolbox talks:
- Read `directory.json` → `subcontractors[]` → match the active sub
- Pull sub's status, trade, and scope for context
- Cross-reference with `safety-log.json` → filter incidents by sub's company name → calculate sub-specific incident count and near-miss ratio
- Include sub safety performance in pre-task safety briefing context

### Integration with Daily Reports

Safety incidents auto-populate in daily reports:
- Superintendent checks "incidents today?" section
- Incident type, description, injury assessment, photo links added
- Auto-link to safety-log.json for tracking
- Triggers safety alert in morning brief if serious incident

---


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
