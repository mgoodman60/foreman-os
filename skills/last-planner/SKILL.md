---
name: last-planner
description: >
  Last Planner System (LPS) implementation for reliable weekly work planning based on Lean Construction Institute methodology. Tracks weekly commitments vs completions, calculates Percent Plan Complete (PPC), performs constraint analysis, identifies variance categories, and drives continuous improvement. Integrates with look-ahead-planner, daily-report-format, material-tracker, and sub-performance. Triggers: "weekly plan", "PPC", "percent plan complete", "last planner", "constraint analysis", "weekly work plan", "pull planning", "make-ready", "commitment tracking", "weekly planning meeting", "constraint log", "reliable promising".
version: 1.0.0
---

# Last Planner System (LPS) Skill for Foreman OS

## Overview

The Last Planner System is a Lean Construction Institute methodology that transforms construction planning from a top-down push system to a collaborative, constraint-driven pull system. This skill enables field superintendents to implement reliable weekly work planning at the front line of construction—where the actual work happens.

### Core Principle: Reliable Promising

Traditional project management asks: "What work is scheduled this week?" Last Planner asks: "What work can we RELIABLY PROMISE to complete this week?" This distinction is critical. A commitment is only made after:

1. All constraints are identified and cleared
2. The responsible trade foreman has reviewed the work scope and confirmed feasibility
3. Required resources (labor, materials, equipment) are available or will be available by the work start
4. Prior work is complete and accepted
5. Clear, current design information exists

A reliable promise is not optimistic; it is a commitment that will be honored more than 80% of the time. This builds trust in the schedule and enables downstream trades to plan their own work confidently.

### Why Last Planner Matters

- **Schedule Reliability**: PPC >85% correlates with on-time project delivery
- **Labor Productivity**: Crews working on constraint-free tasks are 15-30% more productive
- **Waste Reduction**: Fewer rework cycles, fewer crew stalls, less expediting
- **Team Engagement**: Foremen see their input valued; collaborative planning improves morale
- **Early Warning**: Constraint analysis surfaces problems 2-4 weeks before they block work

---

## LPS Planning Hierarchy

Last Planner operates within a four-tier planning hierarchy, each tier informing the tier below:

### Tier 1: Master Schedule (Project Level)
- Baseline schedule: 151 days for MOSC (Substantial Completion: 7/29/26)
- Phase-level milestones: Mobilization → Foundation → Erection → Rough-In → Finishes → Closeout
- Constraints and procurement lead times built in
- Maintained by Project Manager; reviewed monthly
- Example: "PEMB Erection: 03/23/26 - 04/10/26"

### Tier 2: Phase Schedule (Pull Planning Sessions)
- Detailed 4-6 week breakdown of a phase, created in a collaborative pull-planning meeting
- Trades work backward from phase finish date to identify work sequence, constraints, and dependencies
- Results in a detailed network of tasks and lead-time requirements
- Example: For the Rough-In Phase (04/21/26 - 05/29/26), pull planning identifies that CFS framing must complete before MEP installation; MEP rough-in must complete before insulation; all must complete before GWB

### Tier 3: Lookahead Planning (6-Week Constraint Screening)
- Rolling 6-week window of work from the phase schedule
- Focused on constraint identification and removal
- "Make-ready" activities scheduled to clear constraints
- Make-ready work (design finalization, long-lead procurement, prep activities) scheduled upstream of the work that depends on it
- Extends the existing look-ahead-planner skill
- Example: Week of 03/05/26 — "Anchor bolt template must be finalized and approved by 02/28 (3 weeks out) so bolts can be ordered and delivered before 03/20"

### Tier 4: Weekly Work Plan (Commitment Level)
- Specific, granular commitments made by responsible trade foremen
- Work is broken down to the daily crew level
- Constraint status verified for each commitment
- This is the core output of the last-planner skill
- Example: Week of 02/24/26 — "Excavation: trench footer line X-1 to X-3, footing QC pit drains (Walker). Concrete: mobilize batch plant, set rebar for foundation line X-1 to X-2 (W Principles). Mechanical: stub-outs for restroom plumbing to east wall (Davis & Plomin)."

### Tier 4b: Daily Coordination (Adaptive Management)
- 15-minute standup each morning at 7:00 AM on site
- Review today's committed work
- Surface blockers in real time
- Confirm crew size, equipment, material status
- Adjust as needed to maintain PPC

---

## Weekly Planning Workflow (5-Step Process)

### Step 1: Retrospective Analysis (Monday morning, 1 hour)

Before planning forward, review the previous week's performance:

- **List all commitments** from last week's weekly work plan
- **Mark each as Complete or Incomplete**
- **For each incomplete item, assign a variance category** (see Variance Categories section below)
- **Calculate Percent Plan Complete (PPC)**: (Completed / Total) × 100
- **Trend PPC** across last 4 weeks to identify improvement patterns
- **Perform PPC by Trade breakdown**: Which subs are reliable? Which are struggling?
- **Note any pattern**: Is rework recurring? Are material delays systemic? Is labor availability the bottleneck?

**Example from MOSC Week 2 (02/10 - 02/14, 2026):**
- 8 commitments made: 6 completed, 2 incomplete
- PPC = 6/8 = 75%
- Incomplete items:
  1. "Excavation north of grid line H" — Incomplete → Variance: **Prerequisites** (site wet, compaction testing failed, couldn't proceed)
  2. "Footing rebar tie-off, grids X-1 to X-3" — Incomplete → Variance: **Rework** (rebar spacing corrected per Building Official note; retied)
- Trend: Week 1 PPC = 68%, Week 2 PPC = 75%, trending up
- PPC by Trade: Walker (Excavation) = 5/6 = 83% reliable; W Principles (Concrete) = 1/2 = 50% struggling

### Step 2: Constraint Screening (Monday morning, 1.5-2 hours)

For each task planned for the upcoming week, verify that ALL SIX constraint categories are cleared. If even one constraint is unresolved, the task cannot be committed.

#### The Six Constraints

**1. Design Constraint**
- Is the drawing current and approved?
- Are all RFIs related to this work answered in writing?
- Are critical details present on the sheet set?
- Are sequences and elevations clear?
- Status check: "Design ready?" YES / NO

*MOSC Example: "CFS wall framing install, corridor C" — YES, current plans reviewed by EKD (drywall sub); all framing details on Sheets S-3.1 and S-3.2; RFI #8 (stud sizing re: structural loads) resolved 02/16 → Design cleared*

**2. Material Constraint**
- Is material on site or confirmed to arrive by work start date?
- Has material been inspected and approved (lab certs, mill test reports)?
- Are quantities correct and accounted for in inventory?
- Are long-lead items already ordered?
- Status check: "Material ready?" YES / NO

*MOSC Example: "Pour concrete SOG, Building Interior" — materials status pulled from material-tracker: (a) Concrete ready — Wells Concrete batch plant on standby, mix designs approved 02/18, can place by 02/26; (b) Rebar — 35 tons delivered 02/10, inspected, certs on file; (c) Vapor barrier — 10,000 SF polyethylene delivered 02/12, approved — Material cleared*

**3. Labor Constraint**
- Is the crew available with sufficient headcount?
- Are crew members qualified for the task (trade card, license, orientation complete)?
- Is the crew briefed on the scope, sequence, safety, and quality expectations?
- Is the foreman available to supervise?
- Status check: "Labor ready?" YES / NO

*MOSC Example: "Install hollow metal doors and hardware, entryways 1-4" — Hek Glass frames + Schiller hardware (note: Schiller submittals OVERDUE, hard to confirm readiness; escalate) — Labor: Hek Glass crew of 2 glaziers + 1 hardware installer available; hardware installer briefed on fire-rated door installation per code — Labor cleared (contingent on Schiller approval)*

**4. Equipment Constraint**
- Is equipment available (crane, lift, scaffolding, power tools)?
- Has equipment passed daily inspection?
- Is equipment scheduled and confirmed on site?
- Do crew members have current certifications (crane ops, aerial lift, etc.)?
- Status check: "Equipment ready?" YES / NO

*MOSC Example: "Erect PEMB frames, 3 frames per day (Alexander Construction)" — Equipment status: (a) Mobile crane 50-ton reserved for 03/23 - 04/10; (b) Bolting crew with hydro-wrench kits available; (c) Anchor bolt survey scheduled for 03/16 (HOLD POINT HP-007 must clear first) — Equipment cleared pending anchor bolt survey*

**5. Prerequisites Constraint**
- Is the prior work complete?
- Has prior work been inspected and accepted by Building Official / owner?
- Are subgrade conditions (compaction, flatness, cleanliness) acceptable?
- Are connections and interfaces with prior work confirmed fit and function?
- Status check: "Prerequisites complete?" YES / NO

*MOSC Example: "Install CFS metal studs for Bedroom framing, grid X-2 to X-4" — Prerequisites: (a) SOG cure time 28 days (if placed 02/26, ready 03/26); (b) Anchor bolts inspected and survey completed (HP-007); (c) Building Official inspection of stem walls passed 02/20 — Prerequisites cleared; frame install can start 03/27*

**6. Space/Access Constraint**
- Is the work area clear of other trades and prior clutter?
- Is temporary access (stairs, ramps, scaffolding) in place and safe?
- Are utility lines marked and locates confirmed?
- Does coordination with other trades allow work to proceed?
- Status check: "Space/Access ready?" YES / NO

*MOSC Example: "Install rough-in mechanical ductwork, Zones 1-3 (Davis & Plomin)" — Space/Access: (a) CFS framing must be complete and inspected first (prerequisite); (b) Temporary power and compressed air lines staged in mechanical room; (c) Ductwork materials staged outside building — Space/Access cleared after framing complete*

#### Constraint Status Matrix (Weekly Plan Form)

| Task | Trade | Design | Material | Labor | Equipment | Prerequisites | Space/Access | Constraint-Free? |
|------|-------|--------|----------|-------|-----------|----------------|--------------|------------------|
| Excavate north lot | Walker | ✓ | ✓ | ✓ | ✓ | Waiting | — | NO (wet ground) |
| Set footing rebar X-1 to X-3 | W Principles | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | YES → Commit |
| Install anchor bolts | W Principles | ✓ | ✓ | ✓ | Pending survey | ✓ | ✓ | NO (bolt survey HP-007) |

### Step 3: Commitment (Monday afternoon, 1.5 hours)

Trade foremen (or their representatives) sit down with the Super and Scheduler. For each constraint-free task:

- **Trade Foreman states clearly**: "I commit to completing [scope] by [end of day Friday]."
- **Foreman initials the commitment** on the Weekly Work Plan document
- **Potential obstacles are discussed**: If the foreman has reservations, they voice them now. Better to commit to less work than to overcommit and fail
- **Tasks are sequenced** to avoid idle time and maximize crew efficiency
- **Backup work is identified** in case upstream work finishes early
- **Crew daily assignments are sketched** to show who does what, where

**Example Commitments for Week of 02/24 - 02/28, 2026:**

| Task | Trade | Committed By | Notes |
|------|-------|--------------|-------|
| Excavate south footing trench, lines X-1 to X-3, 2.5' deep | Walker | Juan Rodriguez (Crew Lead) | Weather: 40F+ rising, ground thawed. Equipment: Excavator + loader staged. Compaction testing slot booked for Wed 02/26. |
| Set footing rebar X-1 to X-3, tie-off all connections | W Principles | Marcus Chen (Concrete Foreman) | Rebar on site, certs in file. Rebar crew 4 people, 2 days. Building Official notification sent for HP-002 inspection scheduled Thu 02/27 morning. |
| Build stem walls X-1 to X-4, cure and cover | W Principles | Marcus Chen | Concrete batch from Wells Concrete, delivery Fri 02/28. Pour only if footing cure is 7 days minimum (OK for pour 03/07). Backup: place stem wall forms Wed/Thu, pour following Friday. |
| Install temporary safety railing, south site perimeter | W Principles (Self) | Marcus Chen | Site safety. Railing material delivered; crew 1-1.5 days. OSHA Subpart P compliance. |

### Step 4: Daily Huddles (Every morning, 15 minutes)

Each workday, the Super and trade foremen gather at 7:00 AM on site for a quick standup:

- **Review committed tasks for today**: Are all planned crews present and ready?
- **Status check**: Is work progressing on schedule? Any crew departures or absences?
- **Surface blockers immediately**: "We found rebar is wet, can't start tying." → Escalate to Super for material correction
- **Adjust if needed**: Can we shift crew to backup work? Should we pause and replan?
- **Safety**: Any hazards or near-misses from yesterday?
- **Tomorrow preview**: What needs to be ready tonight (material delivery, crew briefing, equipment staging)?

Daily huddles keep promises real-time and catch problems before they cascade.

### Step 5: End-of-Week Scoring (Friday afternoon, 1 hour)

Friday at 4:00 PM (or EOD):

- **Walk the site** with each trade foreman to verify completion status
- **Mark each commitment**: Complete ✓ or Incomplete ✗
- **For each incomplete, assign variance category** (see Variance Categories below)
- **Collect photos** and notes
- **Calculate PPC** = (Completed / Total) × 100
- **Calculate PPC by trade**: Did this sub deliver?
- **Summarize variance categories**: What blocked work this week?
- **Document for next week's retrospective**

**Example EOW Scoring for Week of 02/24 - 02/28, 2026:**

| Task | Status | Variance (if Incomplete) | Notes |
|------|--------|-------------------------|-------|
| Excavate south footing trench, X-1 to X-3 | ✓ Complete | — | Finished Wed, 1 day ahead. Soil conditions good. Compaction test passed Wed. |
| Set footing rebar X-1 to X-3 | ✓ Complete | — | Crew worked Tue-Wed, tied off all connections by Thu morning. HP-002 inspection passed Thu 02/27. |
| Build stem walls X-1 to X-4 | ✗ Incomplete | **Prerequisites** | Concrete not poured Fri as planned. Supply chain delay: Wells Concrete batch plant had breakdown, pushed delivery to Mon 03/03. Crew available, all set to pour Monday. Commitment deferred 1 week. |
| Install temporary safety railing | ✓ Complete | — | Completed Wed. Meets OSHA Subpart P. Site safer now. |

**Weekly Metrics:**
- Total Commitments: 4
- Completed: 3
- Incomplete: 1
- **PPC = 3/4 = 75%**
- Variance breakdown: 100% Prerequisites (1 of 1)
- Next week action: Follow Wells Concrete closely on concrete delivery; confirm Monday morning pour before crediting the commitment.

---

## PPC Calculation and Interpretation

### PPC Formula

**Percent Plan Complete (PPC) = (Completed Commitments / Total Commitments) × 100**

### Scoring Definitions

- **Completed**: Task fully done, inspected if required, meets scope and quality standard
- **Incomplete**: Task started but not finished, or not started due to constraint
- **Abandoned**: Task removed from plan mid-week due to unforeseen circumstance (rare; treated as incomplete for PPC)

### PPC Performance Bands

| PPC Range | Interpretation | Status | Action |
|-----------|----------------|--------|--------|
| 90%+ | High-performing; schedule is reliable | Green | Maintain discipline; identify and export best practices |
| 80-89% | Reliable; acceptable for most projects | Green | Continue improvement focus |
| 70-79% | Marginal; schedule slipping due to missing constraints | Yellow | Implement constraint analysis discipline; assign owner for top 3 blockers |
| 60-69% | Poor; systemic constraint management failure | Red | Weekly strategy session with senior leadership; root cause analysis; recovery plan |
| <60% | Critical failure; project at risk | Red | STOP. Emergency intervention. Pause work to redesign plan and constraint process. |

### 4-Week Rolling Average

Volatile PPC (high swings week-to-week) indicates inconsistent planning. Track a 4-week rolling average to see the true trend:

**Example:**
- Week 1: 68% PPC
- Week 2: 75% PPC
- Week 3: 82% PPC
- Week 4: 71% PPC
- 4-Week Average: (68 + 75 + 82 + 71) / 4 = 74% ← True baseline

If rolling average is trending up (68→74→78), improvement is happening. If trending down (85→80→75), systemic problems emerging.

### PPC by Trade (Sub Scorecards)

Calculate PPC for each sub to identify reliability patterns:

**MOSC Example (Weeks 1-2):**

| Trade | Commitments | Completed | PPC | Reliability |
|-------|-------------|-----------|-----|-------------|
| Walker (Excavation) | 5 | 4 | 80% | Reliable |
| W Principles (Concrete) | 6 | 4 | 67% | Marginal |
| Stidham Cabinets | 0 | 0 | — | Not yet active |
| Hek Glass | 0 | 0 | — | Not yet active |
| EKD (CFS Framing) | 0 | 0 | — | Not yet active |
| Alexander (PEMB) | 0 | 0 | — | Not yet active |
| Davis & Plomin (Mech) | 0 | 0 | — | Not yet active |

Use this to flag struggling subs early. A sub at 50% PPC deserves escalation; invite the sub owner to help diagnose constraint problems.

### PPC Trend Analysis

Track 4-week rolling average on a simple line chart:

```
100% |
 90% |           ★ Target
 80% |     ●───●
 70% | ●──●
 60% |
     └──────────────────
      W1 W2 W3 W4 W5 W6
```

Upward trend (left to right) = improving plan discipline. Downward = systemic issues surfacing.

---


## Project Intelligence Integration

When project intelligence is loaded, auto-populate weekly planning inputs from project data files instead of requiring manual assembly of activity lists, constraint data, and resource availability.

### Activity Pool
Pull schedulable activities for the planning window:
- Read `schedule.json` → `activities[]` (or `milestones[]` + `critical_path[]`) → filter activities scheduled to start or continue within the planning week
- Sort by priority: critical path activities first, then near-critical (float < 5 days), then standard
- Auto-populate the weekly plan form with activity name, baseline duration, and scheduled start/finish
- Example: Week of 03/03 → pull "Set footing rebar X-4 to X-6", "Pour stem walls X-1 to X-4", "Install temporary power"

### Sub Availability
Identify which subcontractors are mobilized and available:
- Read `directory.json` → `subcontractors[]` → identify subs with active scope and crew availability for the planning week
- Cross-reference `labor-tracking.json` → recent crew attendance → verify actual crew sizes vs. committed headcount
- Auto-populate the "Labor" constraint column on the constraint status matrix
- Example: Walker (Excavation) crew of 4 available, W Principles (Concrete) crew of 6 available, EKD (CFS) not yet mobilized

### Location Constraints
Identify spatial conflicts between trades:
- Read `plans-spatial.json` → `building_areas[]` → for each planned activity, check if multiple trades are scheduled in the same building area during the same week
- Flag space/access conflicts in the constraint status matrix
- Example: CFS framing and MEP rough-in both planned for East Wing corridor → flag space conflict, sequence framing before MEP

### Weather Planning
Flag weather-sensitive activities for the planning week:
- Read `specs-quality.json` → `weather_thresholds[]` → identify which planned activities have weather restrictions (temp, wind, rain)
- Cross-reference with weather forecast data → flag if planned outdoor activities conflict with forecast conditions
- Auto-populate the constraint status matrix "Equipment/Weather" column
- Example: Concrete pour planned Thursday → weather_thresholds require min 40F → forecast shows 35F → flag weather constraint

### Material Readiness
Verify materials are available for planned activities:
- Read `procurement-log.json` → for each planned activity, check `expected_delivery` date against activity start date
- Flag activities where material delivery date is after planned start → mark "Material" constraint as blocked
- Check `cert_status` → flag materials delivered but not yet verified as "Material (pending certs)"
- Example: Stem wall pour needs rebar → procurement-log shows rebar delivered 02/10, certs verified → Material cleared

### Prerequisite Inspection
Verify required inspections are complete before next phase:
- Read `specs-quality.json` → `hold_points[]` → for each planned activity, check if a hold point inspection is required before work can proceed
- Cross-reference `inspection-log.json` → verify hold point inspection result (pass/fail/scheduled)
- Flag activities where prerequisite inspection has not passed → mark "Prerequisites" constraint as blocked
- Example: CFS framing requires HP-002 (foundation inspection) to pass first → check inspection-log → HP-002 passed 02/27 → Prerequisites cleared

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
