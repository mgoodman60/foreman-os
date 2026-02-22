---
name: sub-performance
description: >
  Objective, data-driven subcontractor performance scorecards based on five weighted dimensions: Schedule Adherence (25%), Quality (25%), Safety (20%), Responsiveness (15%), and Professionalism (15%). Aggregates data from daily reports, inspections, PPC tracking, safety records, and RFI/submittal turnaround. Enables informed bidding decisions, back-charge documentation, and performance improvement conversations. Triggers: "sub scorecard", "subcontractor performance", "rate sub", "sub evaluation", "vendor performance", "trade performance", "sub rating", "contractor scorecard", "performance review", "back charge", "sub report card".
version: 1.0.0
---

# Subcontractor Performance Scorecard Skill for Foreman OS

## Overview

The sub-performance skill delivers objective, data-driven performance scorecards for every subcontractor on a project. Rather than relying on gut feelings or anecdotal feedback, scorecards aggregate actual project data across five critical performance dimensions, each scored 1-10 and weighted to produce a composite score.

### Purpose

Subcontractor performance scorecards enable:

1. **Informed Bidding Decisions**: When planning the next project, access historical performance data. Prefer subs with proven track records; avoid repeat problems.
2. **Back-Charge Documentation**: Performance data (quality failures, schedule misses, safety incidents) provides objective justification for back charges or warranty claims.
3. **Performance Improvement Conversations**: Instead of vague feedback ("Your crew wasn't organized"), use data: "Your PPC was 62% this quarter; the project average is 78%. Let's discuss what blocked your work."
4. **Contract Incentives**: Reward high-performing subs (9-10 rating) with priority on future bids, multi-project discounts, or bonus incentives.
5. **Risk Mitigation**: Flag at-risk subs (<5.0 rating) early; initiate corrective action meetings or contract review before problems cascade.
6. **Preferred Vendor Lists**: Build institutional memory across projects. Track sub performance over years; promote reliable, professional subs; deprioritize problematic ones.

### Scorecard Philosophy

The sub-performance scorecard is **objective, data-driven, and fair**. It:

- Pulls data automatically from daily reports, inspections, safety logs, and RFI records (not manual opinions)
- Uses transparent scoring criteria so subs understand what they're measured on
- Separates factors within a sub's control (quality, responsiveness, professionalism) from external factors (weather delays, supplier issues)
- Generates dialogue: "Your score is 6.8. Here's where you excelled and where you can improve."

---

## The Five Scoring Dimensions

Each dimension is scored 1-10, measured against objective criteria, and weighted in a composite formula.

### 1. Schedule Adherence (25% Weight)

**Definition**: Does the subcontractor complete committed work on time, maintain promised crew size, mobilize/demobilize on schedule, and hit project milestones?

#### Scoring Criteria

**90%+ PPC (Percent Plan Complete) = 10**
- Subcontractor completes commitments more than 90% of the time
- Minimal incomplete work; when incomplete, root cause is external (weather, owner delay, supplier)
- Crew size consistent with promises
- Mobilization on time; demobilization efficient

**80-89% PPC = 8**
- Subcontractor completes commitments 80-89% of the time
- Good reliability; occasional incomplete work (5-10 items per season)
- Crew size generally consistent
- Minor delays in mobilization/demobilization

**70-79% PPC = 6**
- Subcontractor completes commitments 70-79% of the time
- Marginal; noticeable delays and scope deferrals
- Crew size inconsistency (promised 4, shows 2-3)
- Mobilization delays or early demobilization without notice

**60-69% PPC = 4**
- Subcontractor completes commitments 60-69% of the time
- Poor; significant schedule impact on downstream trades
- Chronic crew size shortages or absences
- Frequent mobilization/demobilization issues

**<60% PPC = 2**
- Subcontractor completes commitments fewer than 60% of the time
- Unacceptable; project delays directly attributable to this sub
- Crew unavailable, undersized, or uncooperative
- Critical schedule milestones missed

#### Data Sources

- **PPC by Trade** from last-planner skill (calculated weekly)
- **Crew Counts** from daily reports (promised vs. actual headcount)
- **Milestone Dates** from schedule vs. actual completion dates
- **Mobilization/Demobilization Dates** from contract documents vs. field records

#### Calculation

```
Schedule Score = PPC × 1.0 (primary), adjusted ±0.5 for crew consistency and milestone performance
```

**Example (MOSC):**
- Walker Construction: PPC 87%, crew consistent, early mobilization = 8.5 → Score: 8 (round down)
- W Principles (Concrete): PPC 71%, crew undersized last 2 weeks, stem wall pour delayed 1 week = 6 → Score: 6

---

### 2. Quality (25% Weight)

**Definition**: Does the subcontractor produce work that passes inspection on first attempt, minimize punch list items, avoid rework, and maintain warranty standards?

#### Scoring Criteria

**First-Pass Inspection Rate (FPIR) 95%+ = 10**
- 95% or more of the sub's work passes inspection without corrections
- Punch list items <5 per 1,000 SF of work
- Rework frequency <2% of total work
- Post-completion warranty callbacks zero or minimal

**FPIR 90-94% = 8**
- 90-94% of work passes first inspection
- Punch list items 5-10 per 1,000 SF
- Rework frequency 2-3%
- Few warranty callbacks

**FPIR 85-89% = 6**
- 85-89% of work passes first inspection
- Punch list items 10-20 per 1,000 SF
- Rework frequency 3-5%
- Occasional warranty callbacks

**FPIR 80-84% = 4**
- 80-84% of work passes first inspection
- Punch list items 20-40 per 1,000 SF
- Rework frequency 5-8%
- Multiple warranty callbacks

**<80% FPIR = 2**
- Fewer than 80% pass first inspection
- Punch list items >40 per 1,000 SF
- Rework frequency >8%
- Recurring warranty failures

#### Data Sources

- **Inspection Tracker** from quality-management skill (pass/fail rates by trade, by phase)
- **Punch List Items** from punch-list skill (filtered by responsible trade)
- **Rework Log** from quality-management or daily-report-format (completed rework tasks)
- **Warranty Callback Records** from closeout and post-completion phase

#### Calculation

```
Quality Score = (FPIR base 1-10) + (Punch list adjustment ±1) + (Rework adjustment ±1) + (Warranty adjustment ±0.5)
```

**Example (MOSC):**
- EKD (CFS Framing/Drywall): FPIR 91%, punch list 8/1000 SF, rework 2%, zero callbacks = 8 + 0 + 0 + 0.5 = 8.5 → Score: 8
- Stidham Cabinets: FPIR 87%, punch list 15/1000 SF, rework 4%, 1 callback = 6 + 0 + (-0.5) + 0 = 5.5 → Score: 6

---

### 3. Safety (20% Weight)

**Definition**: Does the subcontractor maintain a safe worksite, train crews on safety procedures, comply with PPE and housekeeping standards, and avoid incidents?

#### Scoring Criteria

**Zero Recordable Incidents + Full Compliance = 10**
- No OSHA-recordable incidents (injuries requiring medical treatment beyond first aid)
- Zero near-miss events logged
- 100% toolbox talk attendance and documentation
- Consistent housekeeping scores (site clean, debris cleared, hazards mitigated)
- PPE compliance: Hard hats, safety glasses, hi-vis, steel-toe boots observed on all crew members every site visit
- Competent person certifications current (excavation, fall protection, scaffold)

**Zero Recordables + Minor Non-Compliance = 7**
- No recordable incidents
- 1-2 near-miss events (minor, quickly corrected)
- Toolbox talk attendance >90%
- Housekeeping good (occasional clutter, quickly cleaned)
- PPE compliance >95% (1-2 minor PPE lapses observed)
- Certifications current

**Minor Incidents + Non-Compliance = 4**
- 1 recordable incident (e.g., minor laceration, strain) during project
- 3-5 near-miss events
- Toolbox talk attendance 80-90%
- Housekeeping inconsistent (frequent debris, poor organization)
- PPE compliance 80-90% (repeated reminders needed)
- Certifications current but minimal training beyond requirements

**Serious Incidents or Chronic Non-Compliance = 1**
- Multiple recordable incidents (2+) or serious incident (hospitalization, lost-time injury)
- Chronic near-misses (6+) suggesting systemic safety culture problem
- Toolbox talk attendance <80%
- Poor housekeeping (chronic debris, tripping hazards, blocked exits)
- PPE non-compliance <80% (repeated violations despite warnings)
- Expired certifications or untrained crews

**Critical Safety Failure = 0**
- OSHA citation
- Willful safety violation
- Incident resulting in fatality or permanent disability
- Shut down by OSHA inspector
- Repeated violations after formal notice

#### Data Sources

- **Safety Management Records** from safety-management skill (incident log, near-miss reports)
- **Daily Site Observations** from daily-report-format (housekeeping notes, PPE compliance)
- **Toolbox Talk Log** from safety procedures (attendance by crew)
- **OSHA Records** (citations, inspections)
- **Safety Audit Scores** from project-wide safety audits

#### Calculation

```
Safety Score = Base (0-10) adjusted by incident severity and pattern analysis
```

**Example (MOSC):**
- Walker Construction: Zero recordables, 1 near-miss (remediated), toolbox talks 100%, housekeeping 95%, PPE compliance 100%, certs current = 10
- Davis & Plomin (HVAC): Zero recordables, zero near-misses, toolbox talks 95%, housekeeping good, PPE compliance 95%, certs current = 9 → Score: 9

---

### 4. Responsiveness (15% Weight)

**Definition**: How quickly does the subcontractor respond to RFIs, submit required documents, resolve issues, and communicate with the project team?

#### Scoring Criteria

**<3 Day Average RFI Response + <5 Day Submittal Turnaround = 10**
- RFI responses average <3 business days (questions answered in writing within 3 days)
- Submittals reviewed and returned with approval/corrections within 5 days
- All requested information provided on first submission (no back-and-forth delays)
- Communication clear, complete, professional
- Proactive issue resolution: Sub flags potential problems before they escalate

**3-5 Day RFI Response + 5-7 Day Submittal = 8**
- RFI responses average 3-5 business days
- Submittals turnaround 5-7 days
- Minor information gaps requiring 1-2 follow-up requests
- Good communication; responsive to requests
- Issues addressed when raised

**5-7 Day RFI Response + 7-10 Day Submittal = 6**
- RFI responses average 5-7 business days
- Submittals turnaround 7-10 days
- Information gaps or incomplete submissions requiring clarification
- Communication adequate but sometimes unclear
- Reactive: Issues addressed after they become critical

**7-14 Day RFI Response + 10-14 Day Submittal = 4**
- RFI responses average 7-14 business days
- Submittals turnaround 10-14 days
- Frequent incomplete submissions; multiple follow-ups required
- Communication poor; difficult to reach, vague responses
- Slow issue resolution; delays cascade to downstream work

**>14 Day RFI Response + >14 Day Submittal = 2**
- RFI responses >14 days or no response without escalation
- Submittals overdue; extended back-and-forth delays
- Consistently incomplete submissions; requires constant chasing
- Communication unreliable; poor responsiveness
- Issues unresolved for weeks; impacts project schedule

#### Data Sources

- **RFI Log** from rfi-preparer skill (date issued → date answered, tracked per trade)
- **Submittal Tracking** from submittal-intelligence skill (date received → date approved, by supplier)
- **Communication Records** (email response times, meeting attendance, call logs)
- **Issue Resolution Log** (tickets opened → closed, time-to-resolve)

#### Calculation

```
Responsiveness Score = (RFI response time score 1-10) + (Submittal turnaround score 1-10) / 2
+ (Communication quality manual score 1-10) / 3
```

**Example (MOSC):**
- Schiller (Doors/Hardware): RFI avg 12 days, submittal avg 24 days (OVERDUE), communication poor = 3 + 2 + 2 / 3 ≈ 2.3 → Score: 2
- Alexander (PEMB): RFI avg 2 days, submittal avg 4 days, communication clear, proactive = 10 + 10 + 9 / 3 ≈ 9.7 → Score: 10

---

### 5. Professionalism (15% Weight)

**Definition**: Does the subcontractor conduct business ethically, manage their crews professionally, cooperate with other trades, and maintain contract compliance?

#### Scoring Criteria

**Excellent Professionalism = 10**
- Crew conduct exemplary: respectful, cooperative, courteous to other trades
- Site cleanliness maintained by sub crew (no excessive debris, orderly staging)
- Strong cooperation with other trades: coordinates, communicates, accommodates sequencing
- Insurance, documentation, paperwork always on time and complete
- Contract compliance: invoices accurate, change orders negotiated fairly, requests reasonable
- Superintendent rates: "This sub is a pleasure to work with; model contractor"

**Good Professionalism = 8**
- Crew generally well-behaved; occasional minor conflicts or coordination issues
- Site organization generally good; periodic cleanup reminders needed
- Good cooperation; generally accommodates other trades
- Insurance and paperwork mostly timely; 1-2 minor gaps
- Fair contract compliance; reasonable in change order discussions
- Superintendent rates: "Solid, professional contractor"

**Adequate Professionalism = 6**
- Crew behavior acceptable; occasional complaints or minor discipline issues
- Site cleanliness inconsistent; requires frequent reminders to clean up
- Cooperation adequate; sometimes slow to coordinate with other trades
- Insurance/paperwork sometimes late; requires follow-up
- Contract compliance marginal; change orders negotiated with difficulty
- Superintendent rates: "Acceptable; some professionalism concerns"

**Poor Professionalism = 4**
- Crew behavior problematic: conflicts with other trades, disrespectful, complaints from other contractors or owner
- Poor site cleanliness; chronic debris, messy staging areas
- Uncooperative; resistant to schedule changes, poor coordination
- Insurance/paperwork frequently late; requires constant chasing
- Contract disputes: unreasonable change order requests, invoicing inaccuracies
- Superintendent rates: "Difficult to work with; unprofessional"

**Unacceptable Professionalism = 1-2**
- Crew behavior serious issues: multiple conflicts, threats, unsafe conduct toward others
- Very poor housekeeping; safety hazard from debris
- Uncooperative/obstructive; blocking other trades, refusing coordination
- Insurance lapsed or missing; paperwork delinquent
- Contract violations: false invoices, refusal to correct deficiencies, litigation-level disputes
- Superintendent rates: "Cannot work with this contractor; recommend termination"

#### Data Sources

- **Superintendent Manual Rating** (weekly or phase-end assessment, 1-10 scale, with notes)
- **Daily Report Observations** (crew conduct, site cleanliness, cooperation notes)
- **Incident Reports** (conflicts, complaints filed by other trades or owner)
- **Document Compliance Tracking** (insurance certificates, licenses, submittals timeliness)
- **Change Order Audit** (reasonableness of requests, fairness of negotiations)
- **Owner/Architect Feedback** (site visits, correspondence, satisfaction comments)

#### Calculation

```
Professionalism Score = Superintendent manual rating (primary, 1-10) + adjustments based on incident/compliance records (±0-1)
```

**Example (MOSC):**
- EKD (CFS Framing): Excellent crew conduct, clean site, strong cooperation, all insurance timely, fair in negotiations. Super rates 9/10. Score: 9
- W Principles (Concrete): Good crew, mostly clean, cooperation adequate, insurance 1 week late last month, change orders negotiated fairly. Super rates 7/10. Score: 7

---

## Composite Score Calculation

Once all five dimensions are scored 1-10, combine using this weighted formula:

```
COMPOSITE SCORE = (Schedule × 0.25) + (Quality × 0.25) + (Safety × 0.20)
                  + (Responsiveness × 0.15) + (Professionalism × 0.15)
```

### Rating Scale

| Composite Score | Rating | Status | Action |
|---|---|---|---|
| 9.0-10.0 | **Excellent** | Preferred Bidder | Recognition, incentives, preferred bid list |
| 7.0-8.9 | **Good** | Standard Operations | Continue; monitor annually |
| 5.0-6.9 | **Needs Improvement** | At Risk | Performance meeting; improvement plan; increased monitoring |
| <5.0 | **At Risk** | Critical | Formal corrective action; contract review; potential termination |

### Scorecard Example: MOSC Project

**Walker Construction (Excavation/Sitework)**
- Schedule (PPC 87%): 8.5 → 8
- Quality (FPIR 93%, punch list 6/1000 SF): 8
- Safety (zero recordables, 100% compliance): 10
- Responsiveness (RFI avg 2 days, clear communication): 9
- Professionalism (excellent crew conduct, clean, cooperative): 9
- **Composite = (8 × 0.25) + (8 × 0.25) + (10 × 0.20) + (9 × 0.15) + (9 × 0.15) = 2.0 + 2.0 + 2.0 + 1.35 + 1.35 = 8.7**
- **Rating: GOOD** ✓

**W Principles (Concrete - Self-Perform)**
- Schedule (PPC 71%, crew undersized): 6
- Quality (FPIR 88%, punch list 14/1000 SF): 6
- Safety (zero recordables, 95% compliance): 9
- Responsiveness (RFI avg 4 days, timely submittals): 8
- Professionalism (crew adequate, occasional cleanup issues): 7
- **Composite = (6 × 0.25) + (6 × 0.25) + (9 × 0.20) + (8 × 0.15) + (7 × 0.15) = 1.5 + 1.5 + 1.8 + 1.2 + 1.05 = 7.05**
- **Rating: GOOD** ✓

**Schiller (Doors/Hardware)**
- Schedule (PPC cannot assess — material/supply; apply default 5 for supplier reliability): 5
- Quality (FPIR pending; apply default 5): 5
- Safety (N/A — no onsite crew; rate 5 default): 5
- Responsiveness (RFI avg 12 days, submittal avg 24 days OVERDUE): 2
- Professionalism (insurance on file, but poor communication): 5
- **Composite = (5 × 0.25) + (5 × 0.25) + (5 × 0.20) + (2 × 0.15) + (5 × 0.15) = 1.25 + 1.25 + 1.0 + 0.30 + 0.75 = 4.55**
- **Rating: AT RISK** ✗
- **Action: Formal corrective action letter sent 02/18/26. Require daily submittal status updates. Consider alternate supplier for future work.**

---


## Project Intelligence Integration

When project intelligence is loaded, auto-populate scorecard data from project files instead of requiring manual data collection for each scoring dimension.

### Sub Roster
Build the complete subcontractor list from directory:
- Read `directory.json` → `subcontractors[]` → get complete sub list with trade, contract scope, contact info, and contract amount
- Auto-populate scorecard headers with sub name, trade, contract value, and mobilization date
- Example: Walker Construction — Excavation/Sitework — $185,000 — Mobilized 01/21/26

### Schedule Adherence (25% Weight)
Pull attendance and milestone data for schedule scoring:
- Read `daily-report-data.json` → crew attendance records → calculate days present vs. scheduled for each sub
- Read `schedule.json` → planned activities → compare against actual work logged in daily reports
- Read `labor-tracking.json` → `crew_summaries[]` → verify promised crew headcount vs. actual on-site headcount
- Calculate PPC by trade from weekly commitment tracking data
- Example: Walker scheduled 20 work days, present 18 → 90% attendance; PPC 87% → Schedule Score: 8

### Quality Score (25% Weight)
Aggregate quality metrics from inspection and punch data:
- Read `inspection-log.json` → filter by sub → calculate pass/fail rates per sub (FPIR)
- Read `quality-data.json` → `quality_metrics` → pull FPIR and corrective action count per trade
- Read `punch-list.json` → filter by `responsible_sub` → count punch items per 1,000 SF for each sub
- Example: EKD — 91% FPIR, 8 punch items per 1,000 SF, 2% rework rate → Quality Score: 8

### Safety Score (20% Weight)
Pull safety records from safety log:
- Read `safety-log.json` → `recordable_incidents[]` → filter by sub → count recordable incidents per sub
- Read `safety-log.json` → `near_misses[]` → filter by sub → count near-miss events
- Read `safety-log.json` → `toolbox_talks[]` → calculate attendance rate per sub's crew
- Read `daily-report-data.json` → housekeeping and PPE compliance observations per sub
- Example: Walker — zero recordables, 1 near-miss, 100% toolbox talks, 100% PPE → Safety Score: 10

### Responsiveness (15% Weight)
Calculate turnaround times from RFI and submittal logs:
- Read `rfi-log.json` → filter by originating sub → calculate average days from `date_issued` to response
- Read `submittal-log.json` → filter by sub → calculate average submittal turnaround time and resubmission rate
- Flag subs with average RFI response > 7 days or submittal turnaround > 14 days as "at risk" responsiveness
- Example: Schiller — RFI avg 12 days, submittal avg 24 days (OVERDUE) → Responsiveness Score: 2

### Crew Productivity
Benchmark productivity against plan quantities:
- Read `labor-tracking.json` → `productivity_ratios[]` → pull output-per-labor-hour by trade and sub
- Compare against industry benchmarks or project-specific targets
- Flag subs with productivity ratio below 80% of benchmark for performance discussion
- Example: W Principles concrete — 0.85 CY/labor-hour vs. benchmark 1.0 CY/labor-hour → 85% of benchmark → flag for review

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
