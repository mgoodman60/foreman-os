# report-qa — Detailed Reference

Extended documentation, examples, templates, and detailed criteria for the report-qa skill.

## Comprehensive QA Checklist Matrix

Organize by check category. For each category, list specific checks:

### Subcontractor Validation (S1-S5)
- S1: Every sub listed in crew section matches the project directory (fuzzy match for typos)
- S2: Headcount > 0 for every sub listed (no zero-count entries)
- S3: Work descriptions present for every sub (not blank)
- S4: No duplicate sub entries in the same report
- S5: Expected subs from schedule are accounted for (present or noted as absent with reason)

### Weather Threshold Checks (W1-W5)
- W1: If concrete placement documented AND temperature <40°F → Flag: cold weather protocol required
- W2: If roofing work documented AND wind >25 mph → Flag: check wind restrictions
- W3: If exterior painting AND humidity >85% or temperature <50°F → Flag: coating application limits
- W4: If earthwork documented AND precipitation >0.25" → Flag: compaction testing validity
- W5: Weather readings present for all three standard times (7AM, 12PM, 4PM)

### Safety Checks (SF1-SF4)
- SF1: If crane operations documented → verify crane inspection noted
- SF2: If excavation >4' deep → verify shoring/sloping noted
- SF3: If any safety incident mentioned → verify incident report reference number
- SF4: If hot work documented → verify hot work permit noted

### Inspection Checks (I1-I4)
- I1: If inspection was scheduled today (from inspection-log.json) → verify it appears in report
- I2: Inspection results include inspector name and result (pass/fail/conditional)
- I3: Failed inspections have corrective action noted
- I4: If work requiring inspection was performed → flag if no inspection mentioned

### Quantity & Progress Checks (Q1-Q3)
- Q1: Quantities use appropriate units (CY for concrete, LF for pipe, SF for area, etc.)
- Q2: If progress % reported → consistent with prior reports (not jumping unrealistically)
- Q3: Quantities reported align with plan quantities (not exceeding total scope)

### Photo Documentation (P1-P3)
- P1: Major activities have at least one photo
- P2: Photos have captions with location references
- P3: If inspection documented → photo of inspection or result recommended

### Schedule References (SC1-SC2)
- SC1: Current phase matches schedule.json current phase
- SC2: Milestone references use current milestone dates (not superseded)

### Cost Code Checks (CC1-CC2)
- CC1: Work descriptions map to valid cost codes
- CC2: No mismatch between work type described and cost code applied

### Cross-Reference Checks (XR1-XR4)
- XR1: Material deliveries noted → should appear in material-tracker
- XR2: RFI references use current RFI numbers from rfi-log.json
- XR3: Drawing references use current revision (not superseded per drawing-control)
- XR4: If safety incident mentioned → incident report should exist

## Scoring Rubric

Each check produces one of three results:
| Result | Symbol | Meaning |
|--------|--------|---------|
| Pass | ✓ | Check passed, no issues |
| Warning | ⚠ | Should consider addressing, not critical |
| Flag | ✗ | Must address before finalizing |

### Overall Completeness Score
```
Score = (Passes / Total Checks Run) × 100

90-100%: Excellent — report is thorough and consistent
80-89%:  Good — minor gaps, review flagged items
70-79%:  Fair — several gaps need attention
<70%:    Poor — significant gaps, review entire report
```

Reports scoring <80% get flagged with specific remediation items listed in priority order.

## Common Error Patterns — Top 10

For each, provide the error, example, and fix:

1. **Missing subcontractor headcount** — "ABC Plumbing was on site" with no crew count → Fix: Add headcount or note "headcount not available"
2. **Weather-activity conflict** — Concrete pour documented on a day with rain → Fix: Add cold/wet weather protocol notes or clarify work was interior
3. **Scheduled inspection not noted** — Inspection-log shows inspection today but report doesn't mention → Fix: Add inspection result or note postponement
4. **Unrecognized subcontractor name** — "Johnson's guys" doesn't match directory → Fix: Resolve to official sub name from directory.json
5. **Missing photo documentation** — Major concrete pour with zero photos → Fix: Add at minimum 1 placement photo and 1 finished surface photo
6. **Superseded schedule milestone** — Report references "Foundation Complete: 03/01" but schedule shows 03/15 → Fix: Update to current milestone date
7. **Cost code mismatch** — Work described as "electrical rough-in" but coded to Division 03 (Concrete) → Fix: Correct to Division 26 (Electrical)
8. **Safety incident without report reference** — "Worker cut hand" noted but no incident report # → Fix: Add IR reference or create incident report
9. **Material delivery not in tracker** — "Steel delivered today" but no entry in procurement-log → Fix: Log delivery in material-tracker
10. **Visitors without safety orientation** — Visitors listed but no orientation noted → Fix: Add orientation confirmation or note existing visitor badge

## Weekly QA Checks (W1-W6)

Additional checks run across multiple reports:
- W1: **Missing day detection** — Are there gaps in the report sequence? (Monday report missing but Tue-Fri exist)
- W2: **Week-over-week consistency** — Headcount trending (sudden 50% drop without explanation)
- W3: **Cumulative progress** — % complete progression should be monotonically increasing (or explained)
- W4: **Sub continuity** — If a sub was on site Mon-Wed but not Thu-Fri, was this expected per schedule?
- W5: **Weather pattern** — Precipitation days should correlate with reduced outdoor work
- W6: **Photo frequency** — At least 3-5 photos per report; flag if multiple reports have zero photos

## QA Output Format

Present findings in three tiers:

### Flags (Must Address)
Issues that should be resolved before finalizing the report.

### Notes (Should Consider)
Items the user should be aware of but can choose to skip.

### Passes (All Good)
Categories where everything checked out.

### Example Output
```
Report QA Complete — 2 flags, 3 notes

FLAGS:
• Cold weather concrete: Temperature hit 35°F at 7 AM. Concrete placement documented
  but no cold weather plan noted. Per Section 03 30 00, protection required below 40°F.
  → Add cold weather measures to the concrete work description?

• Missing sub: "Johnson Electric" not in sub directory. New sub?
  → Add to directory or correct the name?

NOTES:
• Foundation Complete milestone is 8 days away. Consider mentioning in Schedule Updates.
• No photos of today's compaction testing. Recommended for records.
• General Notes section is empty.

PASSES:
✓ All other subs match directory
✓ Schedule percent complete is consistent
✓ Inspection documented for backfill compaction
✓ Equipment status fully documented
```

## QA Data for Dashboard

Save QA results in the report history entry so the dashboard can track report quality over time:

```json
{
  "qa_results": {
    "report_type": "daily|weekly",
    "score": 85,
    "flags": 2,
    "notes": 3,
    "passes": 12,
    "total_checks": 17,
    "categories_checked": ["subs", "weather_thresholds", "inspections", "schedule", "photos", "completeness", "swppp", "safety", "delay_documentation", "claims_compliance"],
    "flags_resolved": 1,
    "flags_skipped": 1,
    "flag_details": [
      {"check": "W1", "category": "weather_thresholds", "severity": "flag", "message": "Cold weather concrete protocol required"},
      {"check": "S1", "category": "subs", "severity": "flag", "message": "Unrecognized sub: Johnson Electric"}
    ]
  }
}
```
