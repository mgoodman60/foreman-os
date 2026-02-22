---
name: report-qa
description: >
  Use this skill after generating a daily report to review it for completeness,
  consistency, and accuracy against project intelligence. Catches missing inspections,
  unrecognized subs, weather threshold conflicts, and other gaps before the report
  is finalized.
version: 1.0.0
---

# Report QA

## Overview

Review a generated daily report against project intelligence to catch gaps, inconsistencies, and missing information before the report is finalized. This skill runs automatically after report generation as a quality check.

## When to Run

This skill is triggered after the daily-report-format skill generates the report content but **before** the final .docx is created. It reviews the structured report data and flags issues that should be addressed.

## QA Mode Selection

This skill operates in one of two modes, determined by the calling command:

| Mode | Triggered By | Checks Run | Output Prefix |
|---|---|---|---|
| **Daily** | `/daily-report` command, `/amend-report` command | Checks 1–10 below | "Report QA Complete" |
| **Weekly** | `/weekly-report` command | Checks W1–W6 below | "Weekly Report QA Complete" |

The calling command determines the mode. When called from `/daily-report` or `/amend-report`, run ONLY the daily checks (1–10). When called from `/weekly-report`, run ONLY the weekly checks (W1–W6). Never run both sets on the same report.

**Amended reports**: When called from `/amend-report`, run daily QA checks ONLY on the sections that were modified. Present results with the prefix "Amendment QA" and note which sections were re-checked.

## QA Check Categories

### 1. Subcontractor Validation

**Check**: Every sub mentioned in the Crew section exists in the project sub directory.

| Finding | Action |
|---|---|
| Sub name matches directory exactly | Pass |
| Sub name is close match (fuzzy) | Auto-correct and note: "Changed 'Walker' to 'Walker Construction'" |
| Sub name has no match | Flag: "'{name}' is not in the sub directory. Is this a new sub? Add them with /process-docs or confirm the name." |
| Sub in directory expected on site but not listed | Note: "{Sub name} is scheduled to be on site this week per the schedule but was not listed today. Were they absent?" |

### 2. Weather vs. Work Threshold Check

**Check**: Compare today's reported weather against weather thresholds for the work documented.

| Finding | Action |
|---|---|
| Concrete work reported + temp below cold weather threshold | Flag: "Concrete was placed today at {temp}. Cold weather threshold is {threshold} per {spec section}. Was a cold weather protection plan in effect? This should be documented." |
| Concrete work + temp above hot weather threshold | Flag: "Temperature reached {temp}. Hot weather concrete protocol required per {spec section}. Document mitigation measures." |
| Crane operations + wind above limit | Flag: "Wind reported at {speed}. Crane wind limit is {limit}. Were crane operations suspended? Document any impact." |
| Roofing work + rain/moisture | Flag: "Roofing work documented on a day with precipitation. Confirm substrate was dry per {spec section}." |
| Earthwork + heavy rain | Flag: "Earthwork documented with significant precipitation. Note site conditions and any impact on compaction." |
| No threshold conflicts | Pass |

### 3. Inspection Awareness

**Check**: Based on the work documented today, were required inspections noted?

| Finding | Action |
|---|---|
| Concrete placement documented + no pre-placement inspection mentioned | Flag: "Concrete was placed today. Was a pre-placement inspection conducted? Hold point per {spec section}." |
| Backfill/compaction documented + no compaction test mentioned | Flag: "Backfill was placed today. Compaction testing required per {spec section} every {frequency}." |
| Structural steel connections + no special inspection | Note: "Steel connections made today. Special inspection required per IBC. Was inspector present?" |
| Work at hold point + inspection documented | Pass |
| Work at witness point + no inspection | Note (not flag): "Witness point for {work type}. Inspector should have been notified." |

**Conditional Hold Point Logic:**

Some hold points are conditional — they only apply when certain thresholds are met:
- Concrete volume > X CY may trigger additional testing requirements
- Steel connections above certain heights may require special inspection
- Work in specific zones (healthcare, clean room) may require additional sign-offs

When checking hold points against reported work:

1. Load hold points for the work type from `specs-quality.json`
2. If the hold point has a `condition` field, evaluate it against the reported work details
3. Only flag missing inspections when the condition is met
4. If the condition can't be evaluated (missing data), flag as INFO rather than WARNING: "Hold point may apply — verify if [condition] is met"

### 4. Schedule Consistency

**Check**: Report's schedule section aligns with known project intelligence.

| Finding | Action |
|---|---|
| Milestone approaching within 7 days + not mentioned | Note: "{Milestone} is due in {X} days. Consider mentioning in schedule updates." |
| Milestone date passed + not marked complete | Flag: "{Milestone} was scheduled for {date}. Is it complete? Update status." |
| Critical path activity mentioned with delay | Flag: "This is a critical path activity. Document the delay cause, duration, and recovery plan." |
| Percent complete decreased from last report | Flag: "Percent complete dropped from {old}% to {new}%. Is this intentional?" |

### 5. Photo Coverage

**Check**: Photos are present for major work activities.

| Finding | Action |
|---|---|
| Concrete placement documented + no photos | Note: "No photos of today's concrete pour. Consider adding photos for documentation." |
| Major milestone hit + no photos | Note: "A milestone was achieved today. Photos are recommended for project records." |
| Inspection conducted + no photos | Note: "Inspection documented but no photos. Photos of inspection results are recommended." |
| Contract requires photos + none uploaded | Flag: "Contract requires {requirement}. No photos included in today's report." |

### 6. Completeness Check

**Check**: All report sections have content or are intentionally blank.

| Finding | Action |
|---|---|
| Crew section has workers but no work described | Flag: "Subs are listed but work performed is blank for {sub}." |
| Materials received but no condition noted | Note: "Material condition defaulted to 'Good'. Confirm this is accurate." |
| Equipment listed as "Down" with no reason | Flag: "Equipment marked as down but no reason given. Document the issue." |
| Delay documented with no cause | Flag: "Delay noted but cause not specified. Categorize as weather/material/labor/design/inspection." |
| Materials marked as partial delivery with no `backorder_expected` date | Flag: "Partial delivery of {material} noted but no expected backorder date. When is the remainder arriving?" |
| Materials with `quantity_short` > 0 but `partial_delivery` not marked `true` | Note: "{material} shows a short quantity ({quantity_short}) but isn't flagged as a partial delivery. Is the remainder coming, or was the order shorted?" |
| Materials with `quantity_received` > `quantity_ordered` | Note: "{material} received quantity ({quantity_received}) exceeds ordered quantity ({quantity_ordered}). Was extra material ordered or is this an overage?" |
| General Notes section empty | Note: "General Notes section is empty. Anything to document? (RFIs, coordination, directives, upcoming work)" |

**Quantity Discrepancy Check:**

When a daily report documents concrete placement, flooring installation, or any measurable work:

1. Look up the relevant quantities in `plans-spatial.json` for that element/location
2. Check the `data_sources.discrepancies` array for any flagged conflicts
3. If discrepancies exist for the work being documented, add a NOTE: "Quantity discrepancy flagged for [element] — [source A] shows [value] vs [source B] shows [value]. Verify actual field measurement."
4. If the reported quantity in the daily report differs from ALL extracted sources by >15%, flag: "Reported [quantity] for [element] differs significantly from plan quantities. Confirm measurement."

### 6.1 New Hold Point Detection

**Check**: After `/process-docs` adds new spec sections, verify if new hold points were added to `specs-quality.json`:

When running report-qa on any report following a spec update:
- Compare current hold_points in `specs-quality.json` against the report-qa's cached list
- If new hold points exist that weren't previously tracked, add a NOTE to the current report: "New hold point added from spec section [XX XX XX]: [description]. Future reports involving [work type] will be checked against this."
- Update the cached hold points list to include the newly discovered entries

### 7. SWPPP Check (if applicable)

**Check**: If project has a SWPPP and rain was reported, was an inspection documented?

| Finding | Action |
|---|---|
| Rain > threshold + no SWPPP inspection noted | Flag: "Rainfall of {amount} exceeds SWPPP inspection trigger of {threshold}. Was a BMP inspection conducted?" |
| SWPPP inspection noted + no corrective actions but issues visible | Note: "SWPPP inspection conducted. Any corrective actions needed?" |
| No rain + no SWPPP notes | Pass |

### 8. Safety Check (if applicable)

**Check**: If work in safety-sensitive areas was documented, were safety measures noted?

| Finding | Action |
|---|---|
| Work at height + no fall protection mention | Note: "Work at elevation documented in {area}. Fall protection zone per safety plan. Consider noting safety measures." |
| Hot work documented + no permit mention | Note: "Welding/cutting documented. Hot work permit area per safety plan." |
| Confined space entry + no mention | Flag: "Work in {location} which is a designated confined space. Permit and safety measures should be documented." |

### 9. Delay Documentation Completeness

If delay events are documented in today's report, verify they contain sufficient detail for the delay-tracker and (if applicable) claims-documentation skills.

| Finding | Action |
|---|---|
| Delay logged without `delay_type` | Flag: "Delay documented but type not specified. Classify as: Weather, Owner-Directed, Design/Spec, Material/Supply Chain, Sub Performance, Force Majeure, Permit/Regulatory, or Differing Site Conditions." |
| Delay logged without `activities_impacted` | Flag: "Delay documented but affected activities not listed. Which schedule activities are impacted?" |
| Delay on critical path but `critical_path_impact` not set | Flag: "This delay impacts a critical path activity per schedule.json but critical_path_impact is not flagged. Confirm critical path status." |
| Weather delay logged but weather section shows no adverse conditions | Flag: "Weather delay documented but Weather Conditions section shows normal conditions. Reconcile — was it weather-related?" |
| Delay logged without `estimated_duration` | Note: "Delay duration not estimated. Can you estimate how long this impact will last?" |
| Delay logged without `responsible_party` | Note: "Delay responsibility not assigned. Who bears responsibility — owner, architect, sub, GC, or force majeure?" |
| Delay logged with all required fields complete | Pass |
| No delay events documented and no delay language detected in General Notes | Pass |

### 10. Claims Mode Compliance

**Only runs when** `claims_mode: true` in project-config.json. When claims mode is inactive, skip this entire section.

Verify that claims-grade detail is captured where available. These are notes and flags, not hard requirements — the superintendent can dismiss any of them.

| Finding | Action |
|---|---|
| Crew entry without `claims_detail.worker_names` | Note: "Claims mode — worker names not captured for {sub}. Consider adding for claims documentation." |
| Crew entry without `claims_detail.start_time` / `end_time` | Note: "Claims mode — start/end times not captured for {sub}." |
| Equipment entry without `claims_detail.equipment_id` | Note: "Claims mode — equipment ID not captured for {equipment}." |
| Equipment with status "Idle" or "Down" without `claims_detail.idle_reason` | Note: "Claims mode — {equipment} logged as {status} but no reason documented." |
| Material delivery without `claims_detail.delivery_ticket_number` | Note: "Claims mode — delivery ticket number not captured for {material} from {supplier}." |
| Material delivery with timing variance > 2 hours | Note: "Claims mode — {material} delivery was {variance} hours late. Document impact on work activities." |
| Delay event without specific start/stop times | Flag: "Claims mode — delay event '{description}' lacks specific start/stop times. Add timing for claims support." |
| Delay event without `activities_impacted` list | Flag: "Claims mode — delay event '{description}' doesn't list affected activities. Add schedule activity references." |
| All claims-grade fields populated | Pass: "Claims documentation complete for today's report." |

**Output format**: Claims compliance results appear in a separate "Claims Mode" tier after the standard flags/notes/passes:

```
CLAIMS MODE:
• Worker names missing for Smith Electric (3 workers). Recommended for claims documentation.
• Delivery ticket not captured for rebar delivery from Harris Steel.
✓ Delay events fully documented with timing and activities
✓ Equipment IDs captured for all equipment
```

## Project Intelligence Integration

When running QA checks, automatically cross-reference the report against the full project intelligence store. These checks supplement the category-specific checks above by catching gaps that span multiple data sources.

### Punch List Cross-Check
Read `punch-list.json` → If the daily report documents work in a location that has open punch items (`status` = "open" or "in_progress"), verify the report mentions punch item status. Flag if work is documented on punch items without an update: "Work documented at {location} where PUNCH-{id} is open. Was punch item addressed? Update punch status if so."

### Cost Authorization Check
Read `change-order-log.json` → For any new scope of work described in the report, verify it traces to an approved change order or is within original contract scope. Flag if unapproved scope work is documented: "Work on '{description}' does not match any approved CO or original contract scope. Was this authorized? If owner-directed, document the directive for CO processing."

### Procurement Verification
Read `procurement-log.json` → If the report documents materials as "installed" or "in place," verify that `procurement-log.json` shows `delivery_status` = "delivered" for those materials. Flag mismatch: "{material} documented as installed but procurement-log shows delivery_status = '{status}'. Verify material was actually received and update procurement log."

### Quality Record Correlation
Read `quality-data.json` → If the report mentions inspection results (pass/fail), verify that matching records exist in `quality-data.json` inspections. Flag if daily report mentions an inspection result not yet recorded: "Report states {inspection_type} passed at {location}, but no matching record in quality-data.json. Ensure inspection is formally logged."

### Safety Incident Cross-Check
Read `safety-log.json` → If the report documents any safety incident, near miss, or first aid event, verify a corresponding entry exists in `safety-log.json`. Flag if missing: "Safety incident '{description}' documented in daily report but not found in safety-log.json. Log the incident with `safety-management` to maintain OSHA records."

### Schedule Milestone Validation
Read `schedule.json` → `milestones[]` → If the report documents a milestone as "complete" or "achieved," verify that `schedule.json` shows the milestone status updated. Flag mismatch: "Report states '{milestone}' is complete but schedule.json still shows status = '{status}'. Update schedule to reflect completion."

### Weather Threshold Verification
Read `specs-quality.json` → `weather_thresholds[]` + daily report weather data → For each weather-sensitive work type documented in the report, cross-check the reported conditions against spec thresholds. Flag if weather-sensitive work was performed during conditions below/above thresholds and no mitigation is documented: "{work_type} performed at {temp}°F but spec threshold is {threshold}°F per {spec_reference}. No mitigation measures documented — was a protection plan in effect?"

## User Response Handling

After presenting QA results:

- **If user provides corrections**: Apply them to the report data, regenerate affected sections, and re-run QA on those sections only.
- **If user says "looks good" or "skip"**: Proceed to .docx generation with the report as-is.
- **If user addresses some flags but not others**: Apply the corrections provided, note the unaddressed flags, and proceed.

## Weekly Report QA Checks

When called from the `/weekly-report` pipeline (after section narratives are drafted but before .docx generation), run these weekly-specific checks instead of the daily checks above.

### W1. Schedule Narrative vs. Actual Milestone Movement

**Check**: Does the schedule section accurately reflect what happened to milestones this week?

| Finding | Action |
|---|---|
| Milestone date changed in `schedule.json` version_history this week but not mentioned in schedule narrative | Flag: "{Milestone} date changed from {old} to {new} on {date} but isn't mentioned in the weekly schedule section." |
| Narrative says "on track" but daily reports documented delays on critical path activities | Flag: "Schedule narrative says 'on track' but daily reports from {dates} documented critical path delays. Reconcile." |
| Percent complete in weekly report differs from latest daily report by >5% | Flag: "Weekly says {X}% complete but latest daily report shows {Y}%. Which is correct?" |
| Milestone completed this week but not called out as an accomplishment | Note: "{Milestone} was completed on {date}. Consider highlighting in Executive Summary." |

### W2. Crew Trend Consistency

**Check**: Does the headcount narrative match what the daily reports actually show?

| Finding | Action |
|---|---|
| Weekly says "averaging X personnel" but daily report average is >15% different | Flag: "Weekly states average of {X} but daily reports show average of {Y}. Verify." |
| Sub listed in weekly but absent from all daily reports that week | Flag: "{Sub} mentioned in weekly report but not logged in any daily report this week." |
| Sub on site 3+ days this week but not mentioned in weekly narrative | Note: "{Sub} was on site {X} days this week but isn't mentioned in the weekly narrative." |
| Significant headcount swing (>30% day-over-day) not explained | Note: "Crew count went from {X} on {day} to {Y} on {day}. Consider noting the reason." |

### W3. Open Items Accuracy

**Check**: Do the open items in the weekly match the actual log data?

| Finding | Action |
|---|---|
| Weekly says X RFIs pending but `rfi-log.json` shows Y open | Flag: "Weekly states {X} pending RFIs but log shows {Y}. Reconcile." |
| Weekly says X submittals pending but `submittal-log.json` shows Y | Flag: "Weekly states {X} pending submittals but log shows {Y}. Reconcile." |
| RFI resolved this week but not mentioned as a closed item | Note: "RFI-{XXX} was resolved on {date}. Consider noting in Open Items section." |
| Submittal approved this week but not mentioned | Note: "SUB-{XXX} was approved on {date}. Consider noting in Materials/Open Items." |
| Change order status changed this week but not reflected | Flag: "CO-{XXX} status changed to {status} on {date} but isn't reflected in the weekly CO summary." |

### W4. Weather Impact Reconciliation

**Check**: Does the weather summary accurately reflect daily conditions and their impact?

| Finding | Action |
|---|---|
| Daily reports show weather delays on X days but weekly doesn't mention weather impact | Flag: "Daily reports documented weather delays on {dates} but weekly weather section shows no impact." |
| Weekly claims no weather delays but daily reports have weather-related notes in delays section | Flag: "Weekly says no weather impact but {date} daily report noted: '{delay description}'. Reconcile." |
| Temperature data in weekly doesn't match daily report readings | Note: "Weekly says temp range was {X}-{Y} but daily reports show {A}-{B}. Verify." |

### W5. Photo Coverage

**Check**: Are photos included and representative?

| Finding | Action |
|---|---|
| No photos included in the weekly report | Note: "No photos selected. Weekly reports typically include 3-5 representative progress photos." |
| All photos are from the same day | Note: "All photos are from {date}. Consider selecting from multiple days to show progression." |
| Major work activity documented in dailies but no photo of it in weekly | Note: "{Activity} was a significant activity this week but has no photo representation." |

### W6. Distribution List Verification

**Check**: Is the distribution list current?

| Finding | Action |
|---|---|
| Distribution list in `specs-quality.json` contract.documentation_requirements is empty | Note: "No distribution list configured. The user should verify who receives the weekly report." |
| Distribution list exists and is populated | Pass |

### Weekly QA Output Format

Same tiered format as daily QA (Flags / Notes / Passes), but prefix the output:

```
Weekly Report QA Complete — X flags, Y notes

FLAGS:
• [weekly-specific flags]

NOTES:
• [weekly-specific notes]

PASSES:
✓ Schedule narrative matches milestone data
✓ Headcount averages match daily reports
✓ Open items counts match log data
✓ Weather summary matches daily conditions
```

---


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
