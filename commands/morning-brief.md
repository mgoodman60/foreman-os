---
description: Daily briefing with weather and alerts
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
argument-hint: (none — generates briefing for today)
---

Generate a morning briefing for the superintendent. Pulls from project intelligence, previous report data, current weather, and MasterFormat best practices to give a quick overview of what to expect today.

Read the project-data skill at `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` before proceeding. Also read the dashboard-intelligence-analyst agent at `${CLAUDE_PLUGIN_ROOT}/agents/dashboard-intelligence-analyst.md` for daily pulse briefing methodology, and the deadline-sentinel agent at `${CLAUDE_PLUGIN_ROOT}/agents/deadline-sentinel.md` for comprehensive deadline monitoring across all project data. Reference `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/references/masterformat-reference.md` for MasterFormat best practices when enriching today's activities. For field-specific knowledge (concrete operations, steel erection, earthwork, BMPs, equipment), reference the appropriate document from `${CLAUDE_PLUGIN_ROOT}/skills/field-reference/references/` based on today's scheduled work types. If the project is in closeout phase, also read `${CLAUDE_PLUGIN_ROOT}/skills/closeout-commissioning/SKILL.md` to surface closeout deadlines and commissioning status.

## Step 1: Load Data

Search for project-data files in the user's working directory (check `AI - Project Brain/` first, then root):
- `project-config.json` (project_basics, version_history)
- `schedule.json` (milestones, critical_path, weather_sensitive_activities)
- `procurement-log.json` (expected_delivery, cert_status)
- `rfi-log.json` (open RFIs)
- `submittal-log.json` (submittals under review)
- `change-order-log.json` (COs pending)
- `inspection-log.json` (inspections, permit_log)
- `meeting-log.json` (action_items)
- `punch-list.json` (punch_list)
- `plans-spatial.json` (quantities, assembly chains, sheet_cross_references)
- `daily-report-data.json` (report history)
- `specs-quality.json` (weather_thresholds, hold_points)
- `delay-log.json` (active delays, critical path impact)
- `safety-log.json` (open incidents, near-misses, upcoming toolbox talks)
- `labor-tracking.json` (yesterday's headcount for comparison, productivity trends)
- `drawing-log.json` (superseded sheets, pending distribution, recent ASIs)
- `cost-data.json` (budget variance alerts, at-risk cost divisions)
- `quality-data.json` (open corrective actions, failed inspections pending re-work)
- `closeout-data.json` (if in closeout phase: warranty expirations, commissioning status)
- `pay-app-log.json` (upcoming pay app deadlines, retainage status)

If no project config: "No project set up yet. Run /set-project to get started, then /morning-brief will have context to work with."

If no report history: Continue with whatever config data exists — just skip the carry-forward items.

## Step 2: Current Weather

Use web search to get the current weather and today's forecast for the project location (from `project_basics.address` in `project-config.json`). Include:

- Current temperature and conditions
- Today's high/low forecast
- Precipitation chance
- Wind speed

If no address is saved, ask the user: "What's the project location so I can pull the weather?"

## Step 3: Weather Threshold Check

Compare today's forecast against the project's weather thresholds:

- If forecast low is below a cold weather threshold → Flag: "Cold weather protocol likely needed for [work type]. Threshold: [temp] per [spec section]."
- If forecast high is above a hot weather threshold → Flag
- If wind forecast exceeds crane limits → Flag
- If rain is forecasted and weather-sensitive work is scheduled → Flag

### Recent Threshold Changes

Check `version_history` in `project-config.json` for any weather threshold changes in the last 7 days. If found, surface a note:
- Format: "UPDATED: [Threshold type] changed to [new limit] (was: [old limit]) — per revised spec [Section], processed [date]"
- Example: "UPDATED: Roofing humidity limit changed to <60% (was: no limit) — per revised spec Section 07 50 00, processed Feb 16"
- This ensures the crew is aware of threshold changes that may affect today's work

## Step 4: Schedule Context

From `schedule.json`, pull:

- **Current phase** and overall percent complete
- **Milestones approaching** in the next 7 days
- **Critical path activities** in progress
- **Subs expected on site today** (based on schedule dates and recent attendance)

## Step 4.5: Lookahead & Procurement Context

From project-data files, also pull:

- **Lookahead context**: If a lookahead schedule has been generated, note what's planned for today and this week
- **Upcoming deliveries**: Check `procurement-log.json` for expected_delivery dates in the next 7 days. Flag any that are critical path or delayed.
- **Pending RFIs**: Check `rfi-log.json` for any open RFIs older than 7 days — these may need follow-up. Include location context from the location field: "RFI-003 (Grid C-3, Foundation Level) — Footing depth clarification — 12 days open"
- **Pending submittals**: Check `submittal-log.json` for submittals under review for more than 10 business days
- **Material Certification Check**: For materials scheduled to be installed this week, check `procurement-log.json` for cert status. If material is delivered but `cert_status` ≠ "verified", flag: "Rebar (PROC-012) delivered but certs not yet verified — cannot place until mill certs confirmed". If material has `certs_required` populated but `certs_received` is incomplete, flag it as a blocker
- **Pending change orders**: Check `change-order-log.json` for COs with status "submitted" or "under_review" — note cost/schedule impact
- **Upcoming inspections**: Check `inspection-log.json` for inspections scheduled in the next 3 days. Flag any failed inspections awaiting re-inspection
- **Permit Expiration Check**: Check `inspection-log.json` for the permit_log section. Flag any permits expiring within 30 days:
  - Within 30 days: INFO — "Building permit expires Mar 15 (25 days)"
  - Within 7 days: WARNING — "Grading permit expires Feb 22 (4 days) — renew immediately"
  - Expired: CRITICAL — "SWPPP permit expired Feb 10 — work may need to stop until renewed"
- **Overdue action items**: Check `meeting-log.json` action_items for items past due_date with status "open" — list assignee and description
- **Punch list status**: If `punch-list.json` has items, show summary — "X open items (Y priority A)" — only if project is in closeout phase

## Step 4.7: MasterFormat Best Practices

For each activity identified in Steps 4 and 4.5 (today's scheduled work, critical path activities), cross-reference with the MasterFormat knowledge base (`masterformat-reference.md`) and `specs-quality.json` to surface:

- **Hold points**: Required inspections before proceeding (from `hold_points` in `specs-quality.json`, e.g., pre-placement inspection before concrete pour)
- **Weather sensitivities**: Temperature, moisture, or wind limits for today's work types vs. today's forecast (from `weather_thresholds` in `specs-quality.json`)
- **QC reminders**: Common field problems to watch for on today's specific work
- **Testing requirements**: Any tests due for work in progress (e.g., concrete cylinders, compaction, bolt torque)
- **PEMB-specific**: If today involves PEMB work (erection, panels, insulation), note special requirements

Only include the most relevant 2-3 reminders — don't overwhelm the briefing. Prioritize items where today's weather or schedule creates a specific risk.

## Step 4.9: Quantity Context

From `plans-spatial.json` `quantities` section (populated by the quantitative-intelligence skill), pull relevant quantities for today's planned work:

- **For each activity**: Include the relevant measurement — "Room 107 Therapy: 450 SF VCT flooring, 86 LF vinyl base"
- **Progress percentages**: If work has been tracked against quantities, show completion — "East Wing VCT: 1,240 of 4,800 SF installed (26%)"
- **Material needs**: For concrete pours, show volume — "Footings at C-3 to D-5: 12.4 CY (4,000 PSI per S1.0)"

### Sheet References for Today's Work

For each scheduled activity today, look up the relevant assembly chain(s) in `plans-spatial.json`:
- Surface the key sheet references so crews know which drawings to pull: "Foundation work today — See S2.1 (footing plan), S5.1 Detail 3 (rebar), S1.0 General Notes (concrete spec 03 30 00)"
- Only show this for activities where assembly chains exist
- Keep it brief — just the sheet numbers and what they contain

From the `sheet_cross_references` section in `plans-spatial.json`, surface relevant assembly chain data:
- If today's work involves a specific element with a multi-sheet chain, note all relevant sheets
- If there are unresolved discrepancies for today's work area, flag them

Only include quantities for today's active work areas — don't dump the entire quantity database. If no quantities are available, skip this section.

## Step 4.95: v3.1 Tracking System Alerts

Pull from the advanced tracking data files to surface actionable alerts:

**Delays** (from `delay-log.json`):
- Active delays with critical path impact: "DELAY-003 (Weather) — 3 calendar days, critical path impacted. Contract extension request pending."
- Delays approaching contract notification deadlines
- Cumulative delay days this month vs. last month

**Safety** (from `safety-log.json`):
- Open incidents requiring follow-up or corrective action
- Near-misses from the last 7 days: "2 near-misses reported last week — review at next toolbox talk"
- Toolbox talk due: "Weekly toolbox talk due today — suggested topic: [based on this week's work types]"
- TRIR/DART trend if tracking: "Current TRIR: 2.1 (project goal: <3.0)"

**Labor** (from `labor-tracking.json`):
- Yesterday's total headcount vs. expected (from schedule): "Yesterday: 24 workers (expected: 30 — 6 short)"
- Overtime hours trending: "Overtime: 12 hrs this week across 3 subs"
- Certified payroll deadlines approaching

**Drawings** (from `drawing-log.json`):
- New revisions received but not yet distributed: "3 sheets revised (A2.1, A2.3, S3.1) — distribute to field"
- ASIs pending acknowledgment: "ASI-007 received Feb 17 — affects door hardware at east wing"
- Superseded sheets still in use per last field audit

**Cost** (from `cost-data.json`):
- Budget divisions with >10% variance: "Division 03 (Concrete) at 112% of budget — $8,400 over"
- CPI below 0.95: "Cost Performance Index: 0.92 — trending over budget"
- Upcoming payment milestones

**Quality** (from `quality-data.json`):
- Open corrective actions: "2 corrective actions open — drywall finish (Room 203), grout coverage (lobby)"
- Failed inspections needing re-work before next inspection
- First-pass inspection rate trend: "FPIR this month: 87% (target: 95%)"

Only include sections where data exists — skip empty tracking files silently.

## Step 5: Carry-Forward Items

From the most recent daily report in the history:

- **Open items** still unresolved
- **Active delays** and their current status
- **Failed inspections** needing re-inspection
- **Missing subs** from yesterday that should be followed up on
- **Upcoming inspections** scheduled for today or this week

## Step 6: Present the Briefing

Format as a concise briefing:

"**Morning Brief — [Date]**

**Weather:** [Current temp], [conditions]. High [X]°F, Low [Y]°F. [Precipitation]. [Wind].
[Any threshold alerts]

**Schedule:** [Phase] — [%] complete. [Milestone approaching if any].

**Deliveries Expected:**
- [Material] from [Supplier] — expected [date]
- [Any delayed items flagged]

**Today's Focus:**
- [Key activities expected today, with quantities: "Room 107 VCT — 450 SF", "Footings F1-F4 — 9.5 CY"]
- [Sheet references for today's work: "Have S2.1, S5.1 Detail 3 on hand"]
- [Carry-forward items needing attention]
- [Inspections due]

**Action Items:**
- [Overdue RFIs needing follow-up]
- [Submittals needing review]
- [Missing certs to chase]

**QC & Hold Points:**
- [MasterFormat reminders for today's work — hold points, testing, weather limits]

**Heads Up:**
- [Open items, delays, follow-ups]

Ready to start logging? Use /log throughout the day, then /daily-report when you're done."
