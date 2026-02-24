---
description: Generate construction daily reports
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [optional: past date for backfill]
---

Generate a professional construction daily report as a .docx file (matching the W Principles template) with optional PDF export. Uses the daily-report-format skill.

Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/daily-report-format/SKILL.md` and all files in `${CLAUDE_PLUGIN_ROOT}/skills/daily-report-format/references/` before proceeding. Also read the project-data skill at `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` for data retrieval patterns and the report-qa skill at `${CLAUDE_PLUGIN_ROOT}/skills/report-qa/SKILL.md` for the QA process. After report generation, read the report-quality-auditor agent at `${CLAUDE_PLUGIN_ROOT}/agents/report-quality-auditor.md` for automated quality review. For enriching work descriptions with trade-specific language and field standards, reference the appropriate document from `${CLAUDE_PLUGIN_ROOT}/skills/field-reference/references/` based on the day's work types (e.g., concrete-field-operations.md for concrete pours, structural-steel-field-guide.md for steel erection). If available, also read the `docx` Cowork skill for professional Word document formatting best practices. If site photos are included, also read `${CLAUDE_PLUGIN_ROOT}/skills/photo-documentation/SKILL.md` for photo classification and naming conventions.

**Output Skills**: See the `docx` Cowork skill for .docx generation best practices. See the `pdf` Cowork skill if PDF export is requested.

## Step 1: Load Project Config, Intake Log, Review Log, and Assign Report Number

Search for project-data files in the user's working directory (check `AI - Project Brain/` first, then root):
- `project-config.json` (project_basics, folder_mapping, report_tracking)
- `daily-report-data.json` (report history)
- `directory.json` (subcontractors)
- `schedule.json` (milestones, critical_path)
- `procurement-log.json` (deliveries)
- `rfi-log.json` (open RFIs)
- `submittal-log.json` (pending submittals)
- `inspection-log.json` (inspections, failed items)
- `plans-spatial.json` (quantities, sheet_cross_references, grid lines, building areas)
- `specs-quality.json` (weather_thresholds, hold_points, testing requirements)
- `daily-report-intake.json` (field observations from /log commands)
- `delay-log.json` (active delays for context and linking)
- `safety-log.json` (incidents/near-misses to cross-reference)
- `labor-tracking.json` (logged crew hours for headcount validation)
- `drawing-log.json` (current drawing revisions for sheet verification)
- `quality-data.json` (open corrective actions for follow-up)

If found, load the project info and folder mapping for output routing. If an intake log exists for today, load it — this contains pre-classified field observations from /log commands. These entries will pre-populate the report sections, so the user only needs to fill gaps rather than re-enter everything.

**Automatic Log Review:** If an intake log exists with entries, immediately present a summary of what's been logged (organized by report section — weather, crew, materials, equipment, schedule, visitors, photos, notes). Show entry count per section and highlight any sections with no entries yet. Then ask: "Here's what you've logged today. Anything to add or correct before I start generating?"

This replaces the need for a separate review-log step — the review is built into report generation.

If no config file exists, tell the user: "No project is set up yet. Run /set-project first to save your project details, or tell me the project info and I'll include it in this report."

### Report Number Assignment

The report number auto-increments and must never duplicate. Follow this process:

1. Read `last_report_number` from the config (e.g., `4`)
2. Read `daily-report-data.json` and collect all existing `report_number` values (e.g., `["MOSC-001", "MOSC-002", "MOSC-003", "MOSC-004"]`)
3. Increment: `last_report_number + 1` → candidate number `5`
4. Format: `{PROJECT_CODE}-{NUMBER padded to 3 digits}` → `MOSC-005`
5. **Duplicate check**: Verify the candidate does NOT already exist in the report history. If it does (e.g., from a manual edit or data corruption), keep incrementing until a unique number is found.
6. **Immediately** write the new `last_report_number` back to the config file BEFORE starting to collect report info. This prevents a second session from grabbing the same number if two reports are started close together.

The report number is locked in at the start — it does not change even if the user cancels partway through. If the report is abandoned, the number is simply skipped (gaps are fine; duplicates are not).

## Step 2: Determine the Date

**Always auto-populate today's date by default.** Do not ask the user for the date — just use today's date automatically.

The only exception is if the user explicitly provides a past date as an argument ($ARGUMENTS), which means they're backfilling a report for a previous day. In that case, use the date they provided and mention it: "Got it, creating a report for [date]."

## Step 3: Collect Report Information

**If intake log entries exist:** Present a summary of what's already been logged (organized by section) and ask the user to confirm, correct, or add to each section. For sections with no logged entries, ask as normal. This way the user doesn't re-enter data they already provided via /log.

**If no intake log exists:** Walk through each section conversationally as below.

Walk through each section conversationally. Do NOT present a giant form — ask about a few sections at a time to keep it natural. Sections to collect:

1. **Weather** — "What was the weather like today? Temps, conditions, any impact on work?"
2. **Crew & Work** — "Who was on site today and what did they work on?" (subs, headcounts, tasks)
3. **Materials** — "Any deliveries today?" (what, from who, quantities, any issues)
4. **Equipment** — "What equipment was on site? Anything down or new?"
5. **Schedule** — "Any schedule updates? What phase are you in, any delays or milestones hit?"
6. **Visitors/Inspections** — "Anyone visit site today? Any inspections?"
7. **Photos** — "Upload any site photos and I'll caption them and place them in the right sections."
8. **Notes** — "Anything else to document today?"
9. **Labor Hours** — If `labor-tracking.json` has entries for today, present them: "I see [X] hours logged for [subs] via /labor. Include in report?" If no labor data, ask: "Any labor hours to track? (subs, headcounts, hours worked)"
10. **Safety** — If `safety-log.json` has incidents today, present them: "Safety incident logged today — include in report?" Otherwise: "Any safety observations, incidents, or near-misses today?"
11. **Quality** — If `quality-data.json` has open corrective actions in today's work areas: "Open quality items: [list]. Any updates or new observations?"
12. **Delays / Impacts** — "Was work impacted or prevented by anything today?"
    - If intake log contains `delay_event` entries: present them for confirmation
    - If no delay events but the user confirms impacts: collect structured data:
      - **Delay type**: "What caused it? Weather, owner direction, design issue, material delay, sub performance, permit hold, or something else?"
      - **Activities impacted**: "Which activities or work areas were affected?"
      - **Duration**: "How long was work stopped or impacted?"
      - **Critical path**: "Is this on the critical path?" (check schedule.json to auto-suggest)
      - **Responsible party**: owner, architect, sub, GC, force majeure, other
    - If a DELAY-NNN entry already exists in `delay-log.json`, link to it
    - If it's a new delay: assign next DELAY-NNN number
    - **Claims mode enhancement**: Also collect specific start/stop times, affected workers by name, equipment on standby with unit IDs

The user may provide all info at once in a single message or across multiple messages. Adapt to their style. If they give everything in one dump, process it all. If they want to go section by section, walk them through it.

## Step 4: Smart Retrieval

Using the project-data skill's retrieval patterns, pull relevant project intelligence based on the work documented today:

- For each work type mentioned → pull relevant spec sections, weather_thresholds, hold_points, tolerances, testing_requirements from `specs-quality.json`
- For each sub mentioned → match to subcontractors in `directory.json` (subcontractors array), pull their scope, schedule dates from `schedule.json`
- For each location mentioned → resolve to grid_lines, building_areas, floor_levels from `plans-spatial.json`
- For today's weather → check against weather_thresholds from `specs-quality.json` for all work types documented
- For schedule updates → pull current milestones, critical_path, approaching deadlines from `schedule.json`

Use this data to enrich the report in Step 5.

## Step 5: AI Processing

Apply the language standards from the skill references:
- Rewrite all input into professional third-person, past-tense construction language
- Quantify work where possible
- Reference locations specifically using project intelligence (grid lines, building areas, floor levels)
- Use standard construction terminology
- Enrich with spec references, testing requirements, and schedule context from smart retrieval
- Note weather threshold conflicts if any (e.g., cold weather concrete protocol)
- Reference hold points and inspections relevant to today's work

For uploaded photos:
- Analyze each photo to determine subject, location, and context
- Generate a professional caption using project intelligence (grid lines, compass orientation, building areas)
- Determine which report section the photo belongs in
- Apply the smart placement rules from the photo guidelines

## Step 6: Report QA

Before generating the .docx, run the report-qa skill checks against the structured report data:

1. Validate all sub names against the directory
2. Check weather vs. work type thresholds
3. Verify required inspections are documented for the work performed
4. Check schedule consistency (milestones approaching, percent complete)
5. Review photo coverage for major activities
6. Check completeness of all sections
7. Check SWPPP requirements if rain was reported
8. Check safety documentation for work in sensitive areas

Present any flags and notes to the user. Apply corrections if the user provides them. Proceed to .docx generation after the user confirms or skips.

## Step 7: Generate the .docx

Use the `docx` npm library (docx-js) and the docx skill's guidelines to create the report following the template spec in `references/template-spec.md`. The output must match the W Principles DailyReport_v5_Fillable.docx template exactly — same colors, fonts, section header bars, table styling, and logo placement.

Key generation steps:
1. Extract or locate the company logo (check AI - Project Brain/company_logo.png, then extract from template)
2. Build the document using docx-js with the exact page setup, header, footer, and section structures from template-spec.md
3. Generate the .docx buffer and write to file

Name the file: `{M_D_YY}_Daily_Report_{PROJECT_CODE}.docx`

Save to `folder_mapping.daily_reports` (e.g., `11 - Daily Reports/`). If folder_mapping is not populated, fall back to the user's output folder.

### Step 7B: PDF Export (Optional)

After generating the .docx, ask: "Also export as PDF?"

If yes, convert via LibreOffice headless:
```bash
python3 {soffice_script_path} --headless --convert-to pdf {docx_path}
```
Save the PDF alongside the .docx in `folder_mapping.daily_reports`.

## Step 8: Save Report Data

After generating the .docx, save a structured copy of the report data to `daily-report-data.json` in `folder_mapping.ai_output` following the report history schema in the project-data skill. This data feeds the project dashboard.

Use other project-data files for enrichment:
- Reference subcontractors from `directory.json` (subcontractors array)
- Reference weather thresholds from `specs-quality.json` (weather_thresholds)
- Reference schedule context from `schedule.json` (milestones, critical_path)
- Reference inspection requirements from `inspection-log.json` (inspection_log)
- Reference deliveries from `procurement-log.json` (procurement_log)
- Reference RFIs from `rfi-log.json` (rfi_log)
- Reference submittals from `submittal-log.json` (submittal_log)

The structured entry should include all report sections as structured data (not just narrative text), plus:
- Weather readings, impact level, thresholds triggered
- Crew list with headcounts, expected subs missing
- Materials with conditions
- Equipment with status
- Schedule status, delays, milestones hit/approaching
- Inspection results
- Photo metadata (captions, sections, subjects)
- Open items (carried forward from previous report + new)
- QA results (flags, notes, passes)
- Safety and SWPPP notes

## Step 9: Verify Config

The report number was already written to `project-config.json` in Step 1 to prevent duplicates. Verify the config is consistent — if any other project data changed during the report (e.g., a new sub was identified), update the config now.

## Step 9B: Generate Carry-Forward Items

After saving report data, automatically generate carry-forward items for the morning brief by scanning the completed report:

1. **Failed inspections** — Any inspection with result = "Fail" or "Conditional" → `type: "failed_inspection"`, `priority: "high"`
2. **Open RFIs** — RFIs referenced in notes or delays that are still open → `type: "open_rfi"`, priority based on age (>7 days = "high", otherwise "medium")
3. **Unresolved delays** — Delay events with no `date_end` → `type: "unresolved_delay"`, `priority: "high"` if critical path impact
4. **Missing crews** — Subs in `expected_subs_missing` → `type: "missing_crew"`, `priority: "medium"`
5. **Skipped QA flags** — Report-qa flags the user declined to address → `type: "qa_flag"`, `priority: "medium"`
6. **Open items** — Items from previous report that remain unresolved + new items → `type: "open_item"`, priority based on age

Save the `carry_forward_items` array to the report entry in `daily-report-data.json`. The `/morning-brief` command reads this array directly in its Step 5.

**Auto-population rule**: This step runs automatically — the user does not need to manually identify carry-forward items.

## Step 10: Present to User

Share the .docx link and give a brief summary: "Here's your daily report for [date]. [X] subs on site, [total headcount] workers. [Key highlight of the day]."

If a PDF was also generated, share both links.

If any QA flags were skipped, note them briefly: "Heads up — [brief note about skipped flags]."
