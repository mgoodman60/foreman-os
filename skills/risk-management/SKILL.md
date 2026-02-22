---
name: risk-management
description: >
  Proactive risk identification, assessment, and mitigation management for construction projects. Maintain a living risk register, run 5x5 probability-impact assessments, allocate and track contingency drawdown, manage weather and force majeure contingencies, and generate risk reports with heat maps. Integrates with delay-tracker, last-planner, cost-tracking, safety-management, morning-brief, and change-order-tracker. Triggers: "risk", "risk register", "risk matrix", "risk assessment", "contingency", "mitigation", "force majeure", "weather risk", "risk review", "risk report".
version: 1.0.0
---

# Risk Management Skill

## Overview

The **risk-management** skill provides proactive risk identification and management for construction superintendents and project managers. Most construction management tools track problems **after** they happen -- this skill identifies risks **before** they materialize, enabling the project team to avoid, transfer, reduce, or accept risks through deliberate strategy rather than reactive firefighting.

Construction projects are inherently risk-laden: site conditions are uncertain, weather is unpredictable, supply chains are fragile, labor markets fluctuate, and regulatory requirements evolve. A superintendent who manages risk proactively can prevent schedule slippage, cost overruns, safety incidents, and quality failures before they occur.

This skill provides:
- Systematic risk identification using multiple methods (brainstorming, checklists, SWOT, historical review, site walk-through)
- Quantitative risk assessment using a 5x5 Probability x Impact matrix
- Construction-specific risk categories with common triggers and recommended mitigations
- A structured risk register data model for tracking risks from identification through resolution
- Mitigation strategy selection framework (avoid, transfer, reduce, accept)
- Contingency budget allocation and drawdown tracking
- Weather contingency planning with activity-specific thresholds
- Force majeure management with notice and documentation requirements
- Monthly risk review meeting structure with reporting templates
- Integration with other ForemanOS skills for holistic project management

**Key Principle**: Risk management is not a one-time exercise. The risk register is a living document reviewed monthly (at minimum) and updated whenever project conditions change. Risks are dynamic -- new risks emerge as the project progresses, and existing risks change in probability and impact as work advances.

---

## Risk Identification Methods

Effective risk management begins with thorough identification. No single method captures all risks; use multiple approaches throughout the project lifecycle.

### 1. Brainstorming (Project Kickoff Risk Workshop)

Conduct a structured brainstorming session at project kickoff with the full project team:

**Participants**: Project Manager, Superintendent, Project Engineer, Key Subcontractors (structural, MEP, civil), Owner's Representative (if willing)

**Format**:
- 60-90 minute facilitated session
- Round-robin format: each participant identifies one risk per round
- No filtering during brainstorming -- capture everything
- Categorize risks after brainstorming is complete
- Assign initial probability/impact ratings as a group
- Identify risk owners for each risk

**Timing**: Within first two weeks of project mobilization; repeat at each major phase transition

**Output**: Initial risk register populated with 20-50 risks (typical for mid-size commercial project)

### 2. Checklist-Based Identification (Construction-Specific Risk Checklist)

Walk through a structured checklist organized by risk category. This ensures common construction risks are not overlooked:

**Checklist Categories** (detailed in Construction-Specific Risk Categories section):
- Site Conditions
- Weather
- Labor
- Supply Chain
- Regulatory/Permitting
- Design Completeness
- Subcontractor Performance
- Financial
- Force Majeure
- Safety

For each category, review the common risk items and assess whether they apply to the current project. Mark each as "applicable" or "not applicable" with justification.

### 3. SWOT Analysis (Project-Level)

Perform a project-level SWOT analysis to identify risks from a strategic perspective:

- **Strengths**: What advantages does the project team have? (experienced crew, familiar building type, strong sub relationships)
- **Weaknesses**: What limitations exist? (first project in this jurisdiction, compressed schedule, tight budget, new building type)
- **Opportunities**: What external factors could benefit the project? (favorable weather season, strong labor market, owner flexibility)
- **Threats**: What external factors could harm the project? (supply chain disruptions, regulatory changes, adjacent construction, economic downturn)

Threats and Weaknesses translate directly into risk register entries.

### 4. Historical Data Review (Similar Project Lessons Learned)

Review lessons learned from similar completed projects:

- What risks materialized on past projects of similar scope, size, and type?
- What risks were underestimated or missed entirely?
- What mitigation strategies worked well and which failed?
- What schedule/cost overruns occurred and what were root causes?

**Sources**:
- Company lessons-learned database
- Post-project review reports
- Superintendent personal experience log
- Industry publications and case studies for the building type

### 5. Site Walk-Through Identification

Conduct a deliberate risk-focused site walk-through (distinct from daily quality/safety walks):

**Physical Observations**:
- Access constraints (narrow roads, limited staging, adjacent occupied buildings)
- Topography and drainage patterns (flooding risk areas)
- Existing utilities (overhead power lines, underground utilities, active services)
- Adjacent structures (settlement risk, party wall conditions, shared access)
- Soil conditions visible at surface (rock outcrops, standing water, fill areas)
- Environmental indicators (wetlands, protected species habitat, contamination signs)

**Logistical Observations**:
- Material delivery access and staging areas
- Crane placement options and swing radius constraints
- Temporary power/water availability
- Laydown area capacity vs. project needs
- Traffic patterns affecting deliveries and crew access

---

## Risk Assessment Framework

### 5x5 Probability x Impact Matrix

All risks are assessed using a standardized 5x5 matrix that quantifies both the likelihood of occurrence and the severity of impact if the risk materializes.

### Probability Scale

| Level | Rating | Description | Probability Range |
|-------|--------|-------------|-------------------|
| 1 | Rare | Highly unlikely to occur; no precedent on similar projects | < 5% |
| 2 | Unlikely | Could occur but not expected; has occurred on rare projects | 5% - 20% |
| 3 | Possible | Reasonable chance of occurring; has occurred on some similar projects | 20% - 50% |
| 4 | Likely | More likely than not; common on similar projects or conditions suggest occurrence | 50% - 80% |
| 5 | Almost Certain | Expected to occur; project conditions strongly indicate occurrence | > 80% |

### Impact Scale

| Level | Rating | Schedule Impact | Cost Impact | Description |
|-------|--------|----------------|-------------|-------------|
| 1 | Negligible | < 1 day | < $5,000 | Minor inconvenience; absorbed within normal operations |
| 2 | Minor | 1 - 5 days | $5,000 - $25,000 | Noticeable but manageable; requires minor schedule adjustment or budget reallocation |
| 3 | Moderate | 5 - 20 days | $25,000 - $100,000 | Significant disruption; requires formal schedule recovery or change order |
| 4 | Major | 20 - 60 days | $100,000 - $500,000 | Severe impact; threatens milestone dates, requires contract extension and major cost recovery |
| 5 | Critical | > 60 days | > $500,000 | Project-threatening; potential for project suspension, litigation, or fundamental scope change |

### Risk Score Calculation

```
Risk Score = Probability x Impact
```

### Risk Priority Categories

| Score Range | Priority | Color | Action Required |
|-------------|----------|-------|-----------------|
| 1 - 4 | Low | Green | Monitor; review monthly; no active mitigation required |
| 5 - 9 | Medium | Yellow | Active monitoring; mitigation plan documented; review bi-weekly |
| 10 - 15 | High | Orange | Active mitigation underway; escalate to PM; review weekly |
| 16 - 25 | Critical | Red | Immediate action required; escalate to executive leadership; daily monitoring |

### Visual Risk Matrix

```
                          I M P A C T
                 1          2          3          4          5
              Negligible   Minor    Moderate    Major    Critical
         +----------+----------+----------+----------+----------+
    5    |    5     |    10    |    15    |    20    |    25    |
 Almost  |  MEDIUM  |   HIGH   |   HIGH   | CRITICAL | CRITICAL |
 Certain |          |          |          |          |          |
         +----------+----------+----------+----------+----------+
    4    |    4     |    8     |    12    |    16    |    20    |
 Likely  |   LOW    |  MEDIUM  |   HIGH   | CRITICAL | CRITICAL |
         |          |          |          |          |          |
P        +----------+----------+----------+----------+----------+
R   3    |    3     |    6     |    9     |    12    |    15    |
O Poss-  |   LOW    |  MEDIUM  |  MEDIUM  |   HIGH   |   HIGH   |
B ible   |          |          |          |          |          |
A        +----------+----------+----------+----------+----------+
B   2    |    2     |    4     |    6     |    8     |    10    |
I Unlikely|  LOW    |   LOW    |  MEDIUM  |  MEDIUM  |   HIGH   |
L        |          |          |          |          |          |
I        +----------+----------+----------+----------+----------+
T   1    |    1     |    2     |    3     |    4     |    5     |
Y Rare   |   LOW    |   LOW    |   LOW    |   LOW    |  MEDIUM  |
         |          |          |          |          |          |
         +----------+----------+----------+----------+----------+
```

### Assessment Guidelines

**When rating probability**:
- Consider project-specific conditions, not just general industry statistics
- Account for current project phase (early = more uncertainty = higher probability for unknowns)
- Factor in team experience with this risk type
- Review historical data from similar projects

**When rating impact**:
- Assess both schedule AND cost impact; use the higher rating
- Consider cascading effects (one delay triggering downstream delays)
- Account for critical path sensitivity (critical path activities have amplified impact)
- Factor in contractual penalties (liquidated damages amplify schedule impact)
- Consider reputational and relationship impact (harder to quantify but real)

**Re-assessment frequency**:
- Critical risks (16-25): Weekly
- High risks (10-15): Bi-weekly
- Medium risks (5-9): Monthly
- Low risks (1-4): Monthly or at phase transitions

---

## Construction-Specific Risk Categories

Each category below lists common risk items with typical triggers, probability/impact ranges, and recommended mitigations. Use these as a starting checklist during risk identification.

### 1. Site Conditions

Risks related to physical site conditions that differ from expectations or create construction challenges.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Unforeseen subsurface conditions | Limited geotech borings, complex geology, fill areas | 3 | 4 | Additional borings pre-construction; budget contingency for foundation modifications |
| Environmental contamination | Brownfield sites, former industrial use, underground storage tanks | 2 | 4 | Phase I/II ESA review; contamination contingency; specialized sub on standby |
| Utility conflicts | Incomplete utility locates, abandoned utilities, inaccurate as-builts | 3 | 3 | Potholing/GPR survey before excavation; utility coordination meetings; buffer in excavation schedule |
| Access limitations | Narrow roads, adjacent occupied buildings, shared driveways, seasonal restrictions | 3 | 2 | Delivery scheduling; traffic management plan; alternate access routes; early coordination with neighbors |
| High water table / poor drainage | Coastal sites, low-lying areas, seasonal water table fluctuation | 3 | 3 | Dewatering plan; monitor wells; wet-weather earthwork contingency; adjust foundation schedule to dry season |
| Adjacent structure risk | Shared walls, settlement-sensitive neighbors, historic buildings | 2 | 4 | Pre-construction survey; vibration monitoring; settlement monitoring; protective measures during excavation |

### 2. Weather

Risks related to weather conditions affecting construction operations.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Extended cold weather | Winter construction, concrete/masonry operations, northern climates | 4 | 3 | Winter protection plan; heated enclosures; schedule weather-sensitive work for favorable season |
| Extreme heat | Summer concrete/asphalt, worker productivity loss, material curing issues | 3 | 2 | Early morning pours; cooling stations; adjusted work hours; ACI 305 hot weather procedures |
| Excessive precipitation | Extended rainy season, tropical storms, monsoon patterns | 3 | 3 | Weather float in schedule; temporary drainage; covered work areas; accelerated dry-in sequence |
| High winds | Elevated work, crane operations, roofing, curtain wall installation | 3 | 2 | Wind monitoring protocol; crane wind limits; schedule wind-sensitive work for calm season |
| Seasonal flooding | Floodplain proximity, poor site drainage, spring thaw | 2 | 4 | Flood contingency plan; temporary berms; schedule earthwork outside flood season; insurance review |
| Extreme weather events | Hurricanes, tornadoes, ice storms, unprecedented conditions | 1 | 5 | Force majeure provisions; emergency preparedness plan; insurance coverage review; site protection protocol |

### 3. Labor

Risks related to workforce availability, capability, and productivity.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Skilled labor shortage | Market boom, remote location, specialized trades, competing projects | 3 | 3 | Early sub procurement; labor agreements; travel/per diem packages; phased mobilization |
| Skill/quality gaps | Complex work, new building type, inexperienced crews | 3 | 3 | Pre-qualification requirements; mock-ups; additional QC inspection; mentoring/training |
| Productivity below plan | Weather impact, site congestion, morale issues, learning curve | 3 | 3 | Realistic productivity rates in schedule; weekly production tracking; early intervention protocol |
| Jurisdictional disputes | Multi-trade work areas, union vs. non-union, craft assignment conflicts | 2 | 3 | Pre-job conference with trades; clear scope boundaries in subcontracts; labor counsel on standby |
| Strikes / work stoppages | Contract expiration, labor disputes, sympathy strikes | 1 | 5 | Monitor labor contract expiration dates; strike contingency plan; non-union backup plan |
| Key personnel turnover | Superintendent leaves, critical sub foreman reassigned | 2 | 4 | Knowledge documentation; cross-training; contractual key-person requirements; succession planning |

### 4. Supply Chain

Risks related to materials, equipment, and procurement.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Extended lead times | Structural steel, switchgear, elevators, custom millwork, specialty equipment | 4 | 4 | Early procurement; lead time tracking; pre-order with deposits; design-assist for long-lead items |
| Sole-source materials | Owner-specified products, proprietary systems, specialty finishes | 3 | 4 | Identify sole-source items early; negotiate supply agreements; identify acceptable alternates; stockpile critical items |
| Price escalation | Commodity volatility (steel, lumber, copper), tariffs, inflation | 3 | 3 | Escalation clauses in contracts; early material purchase; fixed-price POs; budget escalation contingency |
| Shipping/logistics disruption | Port congestion, trucking shortage, international supply chain issues | 2 | 3 | Domestic alternatives; early shipping; warehousing for critical materials; multiple supplier relationships |
| Material quality defects | Off-spec materials, damaged shipments, counterfeit products | 2 | 3 | Incoming inspection protocol; approved supplier list; factory witness testing for critical items; reject/replace procedures |
| Equipment availability | Crane rental market, specialty equipment, seasonal demand | 3 | 3 | Early equipment reservations; backup rental sources; schedule flexibility for equipment-dependent activities |

### 5. Regulatory

Risks related to permits, inspections, code compliance, and authority-having-jurisdiction (AHJ) decisions.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Permit delays | Plan review backlog, incomplete applications, new jurisdiction | 3 | 3 | Pre-application meetings; complete submittals; expediter services; parallel permit tracks |
| Inspection failures | Non-compliant work, inspector interpretation differences, incomplete systems | 3 | 2 | Pre-inspection self-checks; inspector relationship building; code compliance checklists; punch before inspection |
| Code changes mid-project | New code edition adoption, local amendments, retroactive requirements | 1 | 4 | Monitor code change calendar; grandfather clause documentation; early permit issuance to lock in code edition |
| AHJ interpretation disputes | Ambiguous code language, jurisdictional differences, new inspector | 2 | 3 | Pre-construction code review with AHJ; documented interpretations; code consultant involvement |
| Environmental compliance | Stormwater permits, erosion control, noise ordinances, dust control | 3 | 3 | SWPPP compliance monitoring; erosion control maintenance; noise/dust monitoring; environmental consultant |
| Utility connection delays | Utility company scheduling, infrastructure capacity, connection fees | 3 | 3 | Early utility applications; pre-construction utility meetings; temporary service planning; parallel connection requests |

### 6. Design Completeness

Risks related to the quality and completeness of construction documents.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Incomplete drawings | Fast-track delivery, phased design, design-build transitions | 4 | 3 | Constructability review; RFI log tracking; design completion schedule; hold points for incomplete areas |
| Specification conflicts | Multiple spec writers, outdated references, copy-paste errors | 3 | 2 | Spec review during estimating; conflict log; early RFI for known conflicts; specification hierarchy clause |
| RFI-heavy design areas | Complex details, unusual conditions, interdisciplinary interfaces | 3 | 3 | Pre-construction RFI submission for known issues; design coordination meetings; BIM clash detection |
| Addenda volume | Active design changes, owner scope evolution, code compliance adjustments | 3 | 3 | Addenda tracking log; pricing impact assessment; schedule impact review for each addendum; change order for scope additions |
| Coordination conflicts (MEP/structural) | 3D coordination gaps, ceiling congestion, riser shaft sizing | 4 | 3 | BIM coordination; pre-rough-in coordination meetings; ceiling mock-ups; prioritized routing rules |
| Missing details at transitions | Building envelope interfaces, waterproofing terminations, expansion joints | 3 | 3 | Transition detail review checklist; mock-up at critical transitions; warranty coordination meetings |

### 7. Subcontractor Performance

Risks related to subcontractor capability, reliability, and quality.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Financial instability | Low-bid subs, new companies, overextended firms | 2 | 5 | Financial pre-qualification; bonding requirements; progress payment monitoring; early warning indicators |
| Capacity constraints | Sub overcommitted, competing project demands, limited crew size | 3 | 3 | Capacity verification pre-award; contractual staffing requirements; mobilization milestones; backup sub identification |
| Quality deficiencies | Inexperienced crews, poor supervision, rushed work | 3 | 3 | Quality expectations in pre-construction meeting; mock-ups; increased QC inspection; rework provisions in contract |
| Schedule adherence | Optimistic durations, poor planning, crew shuffling between projects | 3 | 3 | Contractual milestone obligations; look-ahead schedule participation; weekly progress meetings; notice-to-perform protocol |
| Scope disputes | Ambiguous subcontract language, scope gaps between trades, change conditions | 3 | 2 | Clear scope of work exhibits; scope boundary meetings; gap analysis during buyout; change order protocol |
| Sub default/abandonment | Bankruptcy, loss of key personnel, dispute escalation | 1 | 5 | Performance bonding; payment bond; replacement sub pre-identification; contract termination provisions |

### 8. Financial

Risks related to project funding, cash flow, and cost management.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Cash flow gaps | Slow owner payments, front-loaded schedule, retainage accumulation | 3 | 3 | Cash flow projection; early billing; retainage reduction clause; line of credit |
| Owner payment delays | Owner financing issues, disputed pay applications, lender requirements | 2 | 4 | Payment terms in contract; lien rights awareness; prompt payment statutes; suspension-for-nonpayment clause |
| Change order disputes | Scope disagreements, pricing disagreements, authorization delays | 3 | 3 | Change order pricing protocol; pre-approved T&M rates; COR tracking; dispute resolution clause |
| Cost overruns | Estimating errors, scope creep, productivity losses, market escalation | 3 | 4 | Monthly cost-to-complete forecasting; contingency management; value engineering options; early warning reporting |
| Bond capacity limitations | Surety concerns, company financial health, project size relative to bonding | 2 | 4 | Early surety notification; financial reporting; work-in-progress management; project-specific surety review |
| Insurance claim exposure | Incidents, property damage, third-party claims, pollution events | 2 | 4 | Insurance coverage review; claims reporting protocol; loss control program; umbrella coverage adequacy |

### 9. Force Majeure

Risks related to extraordinary events beyond any party's control.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Natural disasters | Earthquake zones, hurricane regions, flood plains, wildfire areas | 1 | 5 | Geographic risk assessment; emergency response plan; insurance coverage; site protection measures |
| Pandemic/epidemic | Public health emergencies, government shutdowns, workforce quarantine | 1 | 5 | Remote work capability; essential worker documentation; supply chain diversification; force majeure clause review |
| Civil unrest | Social disruption, protests, curfews affecting site access | 1 | 4 | Security plan; site protection; alternative access routes; communication protocol |
| Utility failures | Extended power outage, water main break, gas leak, telecom failure | 2 | 3 | Backup generator; temporary water supply; utility company emergency contacts; redundant communication |
| Government actions | Moratoriums, emergency orders, regulatory shutdowns | 1 | 5 | Monitor regulatory environment; government relations; contract force majeure provisions; insurance review |
| Cyberattack | Ransomware, data breach, system failure affecting project management | 2 | 3 | Backup systems; cybersecurity protocols; offline documentation capability; incident response plan |

### 10. Safety

Risks related to worker safety, health, and regulatory compliance.

**Common Risk Items**:

| Risk | Common Triggers | Typical P | Typical I | Recommended Mitigation |
|------|----------------|-----------|-----------|----------------------|
| Fall hazards | Multi-story work, roof work, scaffold operations, steel erection | 3 | 4 | 100% fall protection policy; leading edge plan; scaffold inspection program; safety nets |
| Struck-by hazards | Crane operations, overhead work, material handling, excavation adjacent to traffic | 3 | 4 | Exclusion zones; barricades; flagging operations; load path planning; hard hat compliance |
| Excavation/trench collapse | Deep excavation, unstable soils, adjacent structures, utility crossings | 2 | 5 | Competent person designation; trench shoring/sloping; daily inspection; soil classification; OSHA compliance |
| Confined space incidents | Manholes, tanks, crawl spaces, mechanical rooms during testing | 2 | 5 | Confined space program; atmospheric monitoring; rescue plan; trained entrants/attendants |
| Electrical hazards | Temporary power, live utilities, energized systems during commissioning | 2 | 5 | LOTO procedures; GFCI protection; arc flash analysis; qualified electrical workers only |
| Heat/cold stress | Extreme temperatures, physically demanding work, inadequate hydration | 3 | 3 | Heat illness prevention program; cold stress protocol; hydration stations; work/rest cycles; acclimatization |
| New trade mobilization | Unfamiliar crews, different safety cultures, language barriers | 3 | 3 | Site-specific safety orientation; toolbox talk on day 1; dedicated safety watch first week; bilingual safety materials |

---


## Project Intelligence Integration

When project intelligence is loaded, auto-populate risk register entries with data-driven evidence from project files instead of relying solely on manual assessment.

### Schedule Risk Identification
Auto-flag schedule-driven risks from critical path analysis:
- Read `schedule.json` → `critical_path[]` → identify activities with zero or low float as schedule risk items
- Flag activities where float < 5 days as "near-critical" schedule risks
- Auto-populate risk register entries with activity name, planned dates, and float available
- Example: "MEP Rough-In" has 3 days float → auto-create risk item: "MEP rough-in schedule risk — 3 days float, any delay extends critical path"

### Weather Risk Thresholds
Pre-populate weather-sensitive activity risks with contractual limits:
- Read `specs-quality.json` → `weather_thresholds[]` → for each threshold (concrete min temp, roofing wind limit, etc.), create risk register entries with specific trigger conditions
- Cross-reference `schedule.json` → identify when weather-sensitive activities are scheduled → assess seasonal risk
- Example: Concrete pours scheduled March → weather_thresholds show min 40F → auto-create risk: "Cold weather concrete risk, P=4, I=3, Score=12"

### Subcontractor Performance Risk
Assess sub-specific risks from directory and performance data:
- Read `directory.json` → `subcontractors[]` → pull EMR (Experience Modification Rate) and safety record for risk assessment
- Read `quality-data.json` → FPIR per trade → flag subs with quality performance below 85% as quality risk items
- Read `labor-tracking.json` → `productivity_ratios[]` → flag subs with productivity below benchmark as schedule risk
- Example: Sub with EMR 1.3 and FPIR 78% → auto-create risk: "Sub quality/safety performance risk, P=4, I=3, Score=12"

### Cost/Contingency Context
Show risk exposure relative to available contingency:
- Read `cost-data.json` → `contingency.available_contingency` → calculate total risk exposure as percentage of remaining contingency
- Auto-populate risk report summary with contingency drawdown projections
- Flag when cumulative high/critical risk cost exposure exceeds 75% of available contingency
- Example: 5 active high risks with combined exposure $180,000, contingency remaining $200,000 → flag: "90% contingency at risk"

### Historical Delay Patterns
Seed risk register with evidence-based risks from delay history:
- Read `delay-log.json` → `delay_events[]` → identify recurring delay types (weather, sub performance, material) and their frequency
- Auto-create risk register entries for delay categories that have occurred 2+ times
- Include historical average duration and cost impact in the risk description
- Example: 3 weather delays averaging 4 days each → auto-create risk: "Recurring weather delay pattern, avg 4 days, P=4 based on history"

### Procurement Risk
Flag supply chain risks from procurement status:
- Read `procurement-log.json` → filter items with `category` = "long_lead" or `delivery_status` = "delayed" → auto-create procurement risk entries
- Read `submittal-log.json` → filter items with `status` = "revise_and_resubmit" or overdue → flag as procurement delay risks
- Example: PEMB steel delivery delayed 2 weeks → auto-create risk: "PEMB delivery delay risk, critical path impact, P=5, I=4, Score=20"

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
