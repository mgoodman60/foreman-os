---
description: Generate weekly owner/PM summary report
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [optional: week-ending date]
---

## Overview
Generate comprehensive weekly owner/project manager reports aggregating daily field reports, weather, progress, inspections, and open items. Output is professional owner-facing documentation suitable for distribution and project records.

**Skills Referenced:**
- `${CLAUDE_PLUGIN_ROOT}/skills/weekly-report-format/SKILL.md` - Report format and structure
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` - Project context and data
- `${CLAUDE_PLUGIN_ROOT}/skills/report-qa/SKILL.md` - Weekly report QA checks (W1-W6)
- `${CLAUDE_PLUGIN_ROOT}/agents/report-quality-auditor.md` - Automated quality review after generation
- If available, the `docx` Cowork skill for professional Word document formatting best practices

**Output Skills**: See the `docx` Cowork skill for .docx generation best practices. See the `pdf` Cowork skill if PDF export is requested.

## Execution Steps

### 1. Determine Target Week
- If `$ARGUMENTS` contains date: parse and use as week-ending date
- Otherwise: use most recent complete week (Monday-Sunday)
- Validate date is in current or past project timeline
- Display: "Generating weekly report for week ending [date]"

### 2. Load Daily Reports
From `daily-report-data.json` (in `folder_mapping.ai_output` or the user's working directory):
- Retrieve all daily reports for the target week (7 days)
- If fewer than 3 reports exist, warn user: "Only X days of data available. Some sections may be incomplete."
- Proceed with available data
- Sort chronologically
- Also load supporting files: `project-config.json`, `schedule.json`, `procurement-log.json`, `rfi-log.json`, `submittal-log.json`, `change-order-log.json`, `inspection-log.json`, `meeting-log.json`, `punch-list.json`, `delay-log.json`, `labor-tracking.json`, `safety-log.json`, `cost-data.json`, `drawing-log.json`, `pay-app-log.json`, `quality-data.json`

### 3. Aggregate Weekly Data

**Headcount & Labor:**
- Total man-hours by trade/subcontractor
- Average crew size
- Notable staffing changes or impacts
- Attendance/safety incidents if any

**Weather:**
- Summary by day (temperature range, conditions, precipitation)
- Weather-related work stoppages or delays
- Forecast for upcoming week
- Impact on schedule

**Inspections & Approvals:**
- Inspections completed (code, safety, progress)
- Inspection results (pass/conditional/failed)
- Items requiring correction
- Pending inspections

**Materials & Procurement:**
- Material deliveries received
- Delivery issues or delays
- Long-lead items status
- Procurement critical path items

**Schedule Progress:**
- Activities completed
- Schedule adherence (ahead/on-track/behind)
- Critical path status
- Percentage complete by major scope area
- Activities for upcoming week

**Open Items & Blockers:**
- RFIs pending response (from `rfi-log.json` rfi_log: open status)
- Submittals pending review/approval (from `submittal-log.json` submittal_log: pending status)
- Change orders in process (from `change-order-log.json` change_order_log: submitted/under_review status with cost/schedule impact)
- Permit or approval items outstanding (from `inspection-log.json` permit_log: pending or expiring permits)
- Outstanding site issues requiring correction
- Overdue meeting action items (from `meeting-log.json` meeting_log: action_items with status "open" and past due_date)

**Change Order Summary:**
- Pull from `change-order-log.json` (change_order_log): new COs this week, status changes, approved/rejected
- Running totals: total approved cost impact, total schedule impact days
- Pending COs with cost exposure

**Punch List Status** (if applicable):
- Pull from `punch-list.json` (punch_list): items added this week, items completed, current open count
- Completion % by area and by priority
- Back-charge items pending resolution

**Delays & Contract Extension** (from `delay-log.json`):
- New delays logged this week (type, cause, responsible party)
- Calendar days impacted and cumulative delay total
- Critical path impact assessment
- Contract extension status (submitted, pending, approved)
- Recovery plan status for active delays

**Labor & Productivity** (from `labor-tracking.json`):
- Total man-hours by trade/subcontractor
- Labor productivity metrics (output per hour where tracked)
- Overtime/double-time hours and trend vs. prior weeks
- Certified payroll compliance status
- Headcount comparison: actual vs. scheduled

**Safety** (from `safety-log.json`):
- Safety incidents and near-misses this week
- TRIR and DART rates (if tracking)
- Toolbox talks conducted (topic, attendance)
- Open corrective actions from incidents
- Safety KPI trend vs. project goal

**Quality** (from `quality-data.json`):
- First-Pass Inspection Rate (FPIR) this week
- Failed inspections and corrective actions
- Rework items: cost and schedule impact
- Quality observations by trade
- Three-phase inspection status for active work

**Cost & Budget** (from `cost-data.json`):
- Budget vs. actual by major division
- Cost Performance Index (CPI) and trend
- Estimate at Completion (EAC) vs. budget
- At-risk cost items flagged
- Pay application status (from `pay-app-log.json`): current billing %, retainage held

**Drawing & Document Status** (from `drawing-log.json`):
- New revisions received this week
- ASIs processed and pending
- Distribution status (sheets distributed vs. pending)
- Superseded sheets still in field use

### 4. Draft Executive Summary
- 2-3 sentences capturing overall week
- Tone: professional, objective, owner-focused
- Examples:
  - "Work progressed on schedule with X activities completed. Weather delays of [X hours] recorded on [date]. One RFI issued pending resolution."
  - "Critical path activities remain on track. Structural framing at [X%] complete. Two inspections passed; one permit pending."

### 5. Draft Section Narratives
For each category, write 2-4 sentences in professional, owner-facing language:
- **Headcount**: "Averaging X personnel daily with main trades being [list]. Y subcontractor added crew on [date] to support [activity]."
- **Weather**: "Week experienced [conditions] with [temperature range]. [X hours] of work delays due to [precipitation/temperature]. Forecast for next week: [summary]."
- **Inspections**: "[X] inspections completed. Building permit inspection on [date] resulted in [result] with notes on [items]. Final punch list items: [list]."
- **Materials**: "[X] deliveries received on schedule. Long-lead mechanical equipment on track for [delivery date]. [Item] experienced 2-day delay; recovery plan: [details]."
- **Schedule**: "[X] activities completed on schedule. [Activity] remains on critical path, [X%] complete. [Activity] slightly ahead of schedule by [days]. Next week priorities: [list]."
- **Open Items**: "[X] RFIs pending response. Submittal review results: [X approved, Y revisions required, Z pending]. Change orders: [summary]."
- **Safety/Quality**: "[X incidents/near-misses]/ [X quality observations]. Corrective actions: [list]. All personnel passed [safety training/certification] this week."

### 6. Select Representative Photos
- From all daily report photo attachments
- Select up to 5 most representative images showing:
  - Progress on visible work (structural, systems, finishes)
  - Safety/quality measures
  - Site conditions (weather, activity, logistics)
- Include captions describing date and subject
- Organize by chronological or activity grouping

### 7. Run Weekly Report QA
Before generating the .docx, run the **report-qa** skill's weekly QA checks (W1-W6) against the drafted report content:
- W1: Schedule narrative vs. actual milestone movement in `schedule.json`
- W2: Crew trend consistency vs. daily report headcounts
- W3: Open items accuracy vs. `rfi-log.json`, `submittal-log.json`, `change-order-log.json`
- W4: Weather impact reconciliation vs. daily weather/delay entries
- W5: Photo coverage (day spread, activity representation)
- W6: Distribution list verification from `specs-quality.json`

Present findings as Flags / Notes / Passes. If user addresses flags, update the drafted sections. If user says "looks good" or "skip", proceed to .docx generation as-is.

### 8. Generate Report (.docx with optional PDF)
Create file: `{PROJECT_CODE}_Weekly_Report_{week-ending-date}.docx` and save to `folder_mapping.weekly_reports` (or `folder_mapping.oac_reports` if no weekly_reports folder exists). Fall back to the user's output folder if folder_mapping is not populated.

After generating the .docx, ask: "Also export as PDF?" If yes, convert via LibreOffice headless and save the PDF alongside the .docx.

Format with:
- **Header**: Project name, project number, week-ending date, report date
- **Executive Summary**: Highlighted summary box
- **Sections**: Headcount, Weather, Inspections, Materials, Schedule Progress, Open Items, Safety/Quality
- **Photos**: 5 photos with captions
- **Footer**: Distribution list, contact information, confidentiality notice if applicable
- **Visual Identity**: Navy headers, alternating white/light gray rows, professional typography

### 9. Save to Project Configuration
Update `project-config.json` (report_tracking section):
- Add entry to owner_reports array:
  - Date, file path, week-ending date
  - Summary metadata: activities completed, blockers identified
  - Distribution sent to (list)
  - Date generated

### 10. Present Report to User
Display:
- Executive summary
- Key highlights (activities completed, major blockers, next steps)
- Section-by-section overview
- Link to generated .docx (and PDF if exported)
- Next suggested actions

### 11. Distribution Reminder
Display standard distribution list from contract documentation_requirements:
- **To**: Owner/Project Manager contact(s)
- **Cc**: Architect, GC superintendent, QA lead
- **Bcc**: Project file/document repository
- Remind user to attach the report file and add any project-specific notes before sending

