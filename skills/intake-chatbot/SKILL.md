---
name: intake-chatbot
description: >
  Use this skill when processing conversational field input from a superintendent
  via /log. Handles natural language classification, section assignment, entity
  resolution, and enrichment of field observations into structured daily report
  data. Also handles reviewing and clearing the intake log.
  Trigger phrases: "log this", "just got back from site", "here's what
  happened today", or any casual construction field observation.
  Review triggers: "show my log", "what's logged", "review today's entries",
  "what have I logged", "show logged entries", "review the log".
  Clear triggers: "clear the log", "start over", "wipe today's log",
  "reset the log", "clear my entries".
version: 1.0.0
---

# Intake Chatbot — Conversational Field Data Classification

## Overview

Transform casual, natural-language field observations from a construction superintendent into structured daily report data. The superintendent talks; the system classifies, enriches, and stores.

## Design Philosophy

Superintendents type like they talk — fast, informal, abbreviation-heavy. They're on a job site, not at a desk. The intake system must:

1. **Accept anything** — fragments, run-on sentences, mixed topics, typos, abbreviations
2. **Classify accurately** — route each piece of information to the correct report section
3. **Enrich silently** — add grid lines, full sub names, spec references without asking
4. **Confirm briefly** — short acknowledgment, never a wall of text
5. **Never block** — if something can't be classified, put it in General Notes and move on

## Classification Rules

Every piece of input maps to one or more daily report sections. Use these signals:

### Weather / Site Conditions
**Signals**: temperature, weather words (rain, snow, wind, sun, hot, cold, muddy, frozen, wet, dry), site condition descriptions, work stoppages due to weather
**Examples**: "rained all morning", "35 degrees at 7am", "site is a mud pit", "wind picked up around 2"

### Crew / Work Performed
**Signals**: company names, trade names, headcounts, work descriptions, action verbs (poured, framed, hung, pulled, set, installed, stripped, backfilled, graded, excavated, welded)
**Examples**: "Walker had 6 guys doing backfill", "electricians pulling wire on 2", "poured footings at grid C"

### Materials / Deliveries
**Signals**: delivery verbs (delivered, showed up, arrived, received, got), material names (concrete, rebar, steel, lumber, drywall, pipe, duct, roofing), supplier names, quantities, conditions (good, damaged, wrong, short)
**Examples**: "got 12 tons of rebar from Harris", "concrete truck showed up at 9", "wrong pipe delivered"

### Equipment
**Signals**: equipment names (excavator, crane, loader, bobcat, roller, lift, forklift, generator, pump, compressor), status words (down, broken, idle, mobilized, demobilized), hours
**Examples**: "excavator broke down after lunch", "new crane coming tomorrow", "roller ran all day"

### Schedule Updates
**Signals**: phase mentions, percent complete, milestone references, delay language (behind, ahead, on track, delayed, pushed back, accelerated, slipped), coordination mentions
**Examples**: "we're at about 20% now", "foundation should be done by Friday", "steel delivery pushed to next week"

### Delays / Impacts
**Signals**: delay language with impact/cause — stopped work, couldn't work, shut down, held up, waiting on, standby, suspended, out of sequence, no-showed, can't proceed, blocked by, on hold
**Captures**: delay_type, description, activities_impacted, estimated_duration, critical_path_impact, linked_delay_id, responsible_party, supporting_references

**Classification rule**: When input describes work being prevented, stopped, or impacted by an external cause, classify as BOTH the relevant work section (crew, equipment, etc.) AND as a `delay_event`. The delay event captures the cause, duration, and impact; the work section captures the effect on the crew/schedule.

**Delay type classification**: Match to one of 8 standard categories:
1. **Weather** — temperature, precipitation, wind, flooding, seasonal conditions
2. **Owner-Directed** — stop work orders, scope holds, access restrictions from owner
3. **Design/Spec** — missing details, RFI holds, design errors, incomplete drawings
4. **Material/Supply Chain** — late deliveries, wrong materials, backorders, fabrication delays
5. **Sub Performance** — no-shows, insufficient crew, quality failures requiring rework
6. **Force Majeure** — acts of God, pandemics, civil unrest, utility failures beyond control
7. **Permit/Regulatory** — permit delays, failed inspections blocking work, code holds
8. **Differing Site Conditions** — unexpected subsurface, hazmat discovery, utility conflicts

### Visitors / Inspections
**Signals**: visitor language (came by, stopped by, was here, visited), inspector mentions, inspection types (footing, framing, rough-in, final, special, compaction), results (passed, failed, conditional)
**Examples**: "inspector came at 10, passed the footings", "owner walked the site", "fire marshal stopped by"

### Photos
**Signals**: image uploads attached to the message
**Action**: Analyze the photo content and classify it into the appropriate section

### General Notes
**Signals**: anything that doesn't clearly fit another section — conversations, coordination items, upcoming work, RFI mentions, directives, observations
**Examples**: "talked to the architect about the stair detail", "need to get the crane permit sorted", "tomorrow we're doing the pre-pour meeting"

## Multi-Section Input

A single user message often contains information for multiple sections. Parse each piece separately:

**Input**: "Walker had 6 guys backfilling the east side, got a load of structural fill from Martin Marietta, and the compaction tester came out and we passed"

**Classification**:
1. Crew → Walker Construction, 6 workers, backfill at east wing
2. Materials → Structural fill delivery from Martin Marietta
3. Inspections → Compaction test, passed

## Entity Resolution

When project intelligence is loaded, resolve casual references to official data:

### Subcontractor Resolution
- "Walker" → "Walker Construction" (match on partial name)
- "the concrete guys" → match sub with trade = "Concrete"
- "electricians" → match sub with trade containing "Electric"
- If no match found → use the name as-is, mark `sub_matched: false` in the entry, and flag for resolution during report-qa. The report-qa skill will attempt fuzzy matching and auto-correction; the intake step only flags, never auto-corrects unmatched names.

### Location Resolution
- "east side" → "East Wing, Grid Lines E-G" (match building area)
- "second floor" → "Level 2" (match floor level)
- "by the elevator" → "Central Core, Grid Lines C-E / 4-7" (match building area by feature)
- "grid C" → direct reference, resolve to building area

### Material Resolution
- "concrete" → reference spec section if work type known (e.g., "per Section 03 30 00, 4000 PSI")
- "rebar" → "ASTM A615 Grade 60" (from key materials)
- Generic terms → enrich with spec data if available

### Spec-Based Enrichment
When a work type is identified from the intake entry (e.g., "poured footings", "hung drywall", "pulled wire"):
- Read `specs-quality.json` → `spec_sections[]` → find the matching CSI section for the work type
- Pull key requirements: concrete mix design, testing frequency, acceptance criteria
- Add as enrichment context in the classified entry (not displayed to user unless relevant)
- Example: "poured footings" → pull Section 03 30 00, mix design 4000 PSI, testing every 50 CY

### Schedule-Aware Context
When an activity is mentioned in an intake entry:
- Read `schedule.json` → `critical_path[]` → check if the logged activity matches a critical path item
- If on critical path: add `critical_path: true` flag to the intake entry for emphasis in the daily report
- Example: "Steel erection started" + critical_path includes "PEMB Erection" → flag entry as critical path activity

### Weather-Work Cross-Check
When outdoor work is logged AND weather has been reported for today:
- Read `specs-quality.json` → `weather_thresholds[]` → match the work type
- Cross-check today's reported weather against the threshold
- If threshold exceeded: auto-flag in the intake entry: "Note: Today's temp (35°F) is below the 40°F minimum for concrete placement per Spec 03 30 00"
- Do not block the entry — just flag for awareness

### Quantity Context
When work with measurable output is logged (concrete poured, flooring installed, outlets wired):
- Read `plans-spatial.json` → `quantities` → find the total plan quantity for that element type
- Add total plan quantity as context: "12 CY poured today of 42.3 CY total footings (28%)"
- This enables automatic progress percentage calculations in the daily report

### Inspection Reminder
When the logged work type has a hold point in the specs:
- Read `specs-quality.json` → `hold_points[]` → match the work type
- If a hold point exists and the work is at the trigger stage: prompt the superintendent
- "Concrete pre-placement — did this need an inspection before proceeding? (Hold point HP-02)"
- Accept dismissal — this is a reminder, not a blocker

### Sub Absence Detection

When the user mentions a sub is absent ("nobody from the plumber", "electricians didn't show", "Walker was a no-show", "[sub] not on site"):

1. Log a crew entry with `headcount: 0` and work description: "Not on site"
2. If the sub is in the directory AND was scheduled this week (from schedule.json), add to `expected_subs_missing` in the daily summary
3. Prompt for reason if not given: "Any reason they weren't here?"
4. If the user provides a reason, prompt for impact: "Is this causing any delay?"
5. If it caused a delay, also classify as a `delay_event` with type: Sub Performance

**In the report**: Absent subs appear in the Crew on Site table with headcount 0 and a note explaining the absence.

### Duplicate Sub Entry Merging

When a new intake entry references a sub that already has an entry for today:

1. **Same sub, additional workers or work**: Merge into the existing entry. Update headcount (take the higher number unless the user explicitly says "plus", "also", or "more"). Append the new work description.
   - Example: "Walker had 6 guys backfilling" + "Walker also had 2 guys on grading" → Walker: 8 workers, backfill + grading

2. **Same sub, corrected headcount**: Replace the old value.
   - Example: "Actually Walker had 8, not 6" → update to 8

3. **Same sub, different location**: Keep as separate line items under the same sub name.
   - Example: "Walker had 4 at the east wing" + "Walker had 3 at the west wing" → two entries

4. **Confirm the merge**: "Updated Walker to 8 workers — backfill + grading at east wing. That right?"

**Key rule**: When in doubt, ask: "Is that 8 total for Walker, or 8 more on top of the 6?"

## Claims Mode

When `project-config.json` has `claims_mode: true`, the intake system captures claims-grade detail on top of standard classification. This enhanced capture supports the claims-documentation skill's evidence requirements.

**Crew entries**: After logging a sub, prompt: "Claims mode — can you give me names and hours for that crew?"
- Capture: worker_names[], start_time, end_time, total_hours, overtime_hours
- If user declines: proceed without — claims detail is recommended, not required

**Equipment entries**: After logging equipment, prompt: "Got the [equipment]. Unit number? Any idle or standby time today?"
- Capture: equipment_id, idle_hours, idle_reason, standby_hours, standby_reason

**Material deliveries**: After logging a delivery, prompt: "Delivery ticket number? Was it on time?"
- Capture: delivery_ticket_number, scheduled_delivery_time, actual_delivery_time

**Delay events**: Always capture the full delay classification when claims mode is active.

**Prompting etiquette**: Claims-mode prompts follow the same rules as standard prompts — ask one at a time, accept dismissals ("skip", "no", silence), never block the user from continuing to log.

## Auto-Context

Based on what's been logged so far today, the system can proactively prompt for related information. See `references/auto-context.md` for the full rule set.

Key principle: suggest, don't require. If the user ignores a prompt, move on.

## Conversational Flow

See `references/conversational-flow.md` for patterns on handling multi-turn interactions, corrections, and follow-up questions.

## Edge Cases

See `references/edge-cases.md` for handling ambiguous input, contradictions, and unusual scenarios.

## Review Log

When the user asks to review today's logged entries ("show my log", "what's logged", "review today's entries"), perform the following:

1. Search for `daily-report-intake.json` in the user's working directory
2. If not found: "Nothing logged today yet. Use /log to start capturing field observations."
3. If found, load entries and group by report section (weather, crew, materials, equipment, schedule, visitors, photos, general notes)
4. Present a summary organized by section:
   - Show entry count per section
   - Show key details (sub names, material names, etc.)
   - Highlight any sections with no entries yet
5. Offer next steps:
   - "Anything to add or correct before generating the report?"
   - "Run /daily-report when you're ready to generate"
   - "Say 'clear the log' to start over"

## Clear Log

When the user asks to clear the intake log ("clear the log", "start over", "wipe today's log", "reset the log"):

1. Search for `daily-report-intake.json` in the user's working directory
2. If not found: "No intake log to clear — nothing has been logged today."
3. If found, show the user how many entries will be cleared:
   "You have [X] entries logged today across [Y] report sections. Clear everything and start fresh?"
4. **Wait for explicit confirmation. Do NOT clear without user approval.**
5. If confirmed:
   - Archive the current log as `daily-report-intake-{YYYY-MM-DD}-cleared.json` (entries aren't permanently lost)
   - Create a fresh empty intake file:
     ```json
     {
       "date": "YYYY-MM-DD",
       "entries": []
     }
     ```
   - Confirm: "Log cleared. Use /log to start fresh."

## Additional Resources

- **`references/intake-schema.md`** — JSON schema for intake log entries
- **`references/classification-examples.md`** — 50+ classification examples for training
- **`references/auto-context.md`** — proactive prompting rules
- **`references/conversational-flow.md`** — multi-turn interaction patterns
- **`references/proactive-prompting.md`** — smart follow-up question rules
- **`references/edge-cases.md`** — handling ambiguous and unusual input
