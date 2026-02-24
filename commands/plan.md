---
description: Last Planner System scheduling
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [weekly|status|constraints|commitments|report]
---

# Last Planner System (LPS) Command

## Overview

Implement the Last Planner System for reliable weekly work planning based on Lean Construction Institute methodology. Create weekly work plans with trade foreman commitments, perform constraint analysis to clear blockers before they impact work, track Percent Plan Complete (PPC) to measure planning reliability, categorize variances for continuous improvement, and integrate with look-ahead schedules for make-ready planning.

## Skills Referenced
- `${CLAUDE_PLUGIN_ROOT}/skills/last-planner/SKILL.md` — Full Last Planner System: planning hierarchy, weekly workflow, constraint analysis (6 types), PPC calculation, variance categories (9 types), make-ready process
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` — Project configuration and data context
- `${CLAUDE_PLUGIN_ROOT}/agents/weekly-planning-coordinator.md` — Agent for orchestrating the weekly planning cycle with constraint analysis and PPC tracking

**Output Skills**: See the `docx` Cowork skill for .docx report generation best practices.

## Execution Steps

### Step 1: Load Project Configuration

Search for project-data files in the user's working directory (check `AI - Project Brain/` first, then root):
- `project-config.json` (project_basics, folder_mapping)
- `schedule.json` (milestones, critical_path, activities — for work planning context)
- `daily-report-data.json` (for verifying work completion against commitments)
- `directory.json` (subcontractors — for trade foreman identification)
- `procurement-log.json` (material availability — constraint check)
- `rfi-log.json` (open RFIs — design information constraint)
- `submittal-log.json` (pending submittals — design information constraint)
- `inspection-log.json` (upcoming inspections — prerequisite constraint)
- `delay-log.json` (active delays — for constraint impact)

If no project config: "No project set up yet. Run `/set-project` first."

Also check for existing weekly plan data in `{folder_mapping.ai_output}/weekly-plans/` or within project config.

### Step 2: Parse Arguments for Sub-Action

Examine `$ARGUMENTS` to determine which operation:
- **"weekly"** — Create or update the weekly work plan (commitments from trade foremen)
- **"status"** — Review current week's plan progress and PPC score
- **"constraints"** — Constraint screening for upcoming work (6-week lookahead)
- **"commitments"** — View/update individual commitments (mark complete/incomplete)
- **"report"** — Generate weekly planning report with PPC trend

If no sub-action provided, show usage:
```
Usage: /plan [weekly|status|constraints|commitments|report]
Examples:
  /plan weekly              → Create this week's work plan
  /plan status              → Review PPC and commitment status
  /plan constraints         → Screen constraints for next 6 weeks
  /plan commitments         → Update commitment completion status
  /plan report              → Generate PPC trend report
```

### Step 3: WEEKLY Sub-Action

Create the weekly work plan (Monday morning process):

**Part A — Retrospective (Review last week):**
1. Load previous week's commitments
2. For each commitment, mark as Complete or Incomplete
3. For incomplete items, assign variance category:
   - Prerequisites (prior work not done)
   - Design (information missing, RFI pending)
   - Material (not delivered, wrong material)
   - Equipment (not available, broken)
   - Labor (crew no-show, undersized)
   - Weather (conditions prevented work)
   - Rework (quality issue required redo)
   - Change of Priority (redirected by owner/PM)
   - Space/Access (area not available)
4. Calculate PPC: (Completed / Total) × 100%
5. Calculate PPC by trade (which subs are reliable?)
6. Show 4-week PPC trend

**Part B — Constraint Screening:**
1. Pull activities from schedule.json for next 1-2 weeks
2. For each activity, check 6 constraint types:
   - **Design**: Are drawings current? Any open RFIs blocking this work?
   - **Materials**: Are materials on site or scheduled for delivery?
   - **Labor**: Is the crew confirmed, sized correctly, available?
   - **Equipment**: Is required equipment on site or reserved?
   - **Prerequisites**: Is prior work complete and accepted?
   - **Space/Access**: Is the work area available and accessible?
3. Flag unresolved constraints — these block reliable commitments
4. Generate make-ready actions for each unresolved constraint

**Part C — New Commitments:**
1. For each activity with all constraints cleared:
   - Identify responsible trade foreman (from directory.json)
   - Define specific scope of work for the week
   - Set measurable completion criteria
   - Confirm crew size and days committed
2. Only commit work that is constraint-free
3. Auto-number commitments: `WP-YYYY-WNN-NNN`
4. Save weekly plan to data store

### Step 4: STATUS Sub-Action

Review current week's progress:

1. Load this week's commitments
2. Show status of each commitment: Committed, In Progress, Complete, Incomplete
3. Calculate running PPC for the week (based on items due by today)
4. Show PPC by trade
5. Flag at-risk commitments (behind expected progress)
6. Show upcoming commitments for remainder of week

### Step 5: CONSTRAINTS Sub-Action

Constraint screening for upcoming work:

1. Pull activities from schedule.json for next 6 weeks (lookahead window)
2. For each week, screen all 6 constraint types
3. Categorize constraints by severity:
   - **Cleared**: All constraints satisfied; ready for commitment
   - **Make-Ready**: Constraint identified; action in progress; expected to clear by work date
   - **Blocked**: Constraint not yet addressed; work cannot be committed until resolved
4. Generate make-ready action list with owners and deadlines
5. Flag items on critical path with blocked constraints

### Step 6: COMMITMENTS Sub-Action

Update individual commitment status:

1. Display this week's commitments in table format
2. Allow interactive updates:
   - Mark as Complete (with date)
   - Mark as Incomplete (with variance category)
   - Add notes
   - Adjust scope (with reason)
3. Support bulk updates: "All concrete commitments complete" or "Walker items done"
4. Recalculate PPC after updates

### Step 7: REPORT Sub-Action

Generate weekly planning report (.docx):

1. Include:
   - Week summary: total commitments, completed, incomplete
   - PPC score with 8-week trend chart
   - PPC by trade breakdown
   - Variance analysis: count and categorization of missed commitments
   - Pareto chart of variance categories (which reasons most common?)
   - Constraint status for next 2 weeks
   - Make-ready action items with owners
   - Recommendations for improving PPC
2. Save to `{folder_mapping.ai_output}/{PROJECT_CODE}_Weekly_Plan_Report_{date}.docx`

### Step 8: Save & Log

1. Save weekly plan data to persistent storage
2. Update `project-config.json` version_history:
   ```
   [TIMESTAMP] | plan | [sub_action] | [PPC score or commitment count]
   ```
3. If PPC drops below 70%, surface alert in next `/morning-brief`
4. If project data changed significantly, regenerate `CLAUDE.md` to reflect latest planning metrics

## Integration Points
- **Morning Brief** (`/morning-brief`): Today's committed work, constraint alerts, PPC trend
- **Look-Ahead** (`/look-ahead`): 3-week lookahead feeds Tier 3 constraint screening
- **Daily Report** (`/daily-report`): Work accomplished validates commitment completion
- **Weekly Report** (`/weekly-report`): PPC and planning metrics included
- **Dashboard** (`/dashboard`): PPC trend chart, constraint status
- **Sub Scorecard** (`/sub-scorecard`): PPC by trade feeds schedule adherence dimension
- **Material Tracker** (`/material-tracker`): Material constraint verification
- **Inspections** (`/inspections`): Prerequisite inspection constraints
