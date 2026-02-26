---
description: Data health sweep — detect issues, apply normalization fixes, generate confidence report
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [scan|fix|report]
---

# Data Health Command

## Overview

Orchestrates a full data quality sweep across the 28-file Project Brain. Combines detection (data-integrity-watchdog patterns) with normalization (data-normalization skill patterns N1-N8) and reporting (confidence scoring).

## Skills Referenced
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` -- Project data access and JSON file locations
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/references/cross-reference-patterns.md` -- 12 cross-reference patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/references/conflict-detection-rules.md` -- 25 detection rules (if available)

For normalization patterns, reference the canonical `data-normalization` skill in the `foremanos-intel` plugin. If not installed, the 8 pattern definitions are:
- **N1**: Status Standardization (canonical enums per file)
- **N2**: Counter Reconciliation (recount arrays vs stored scalars)
- **N3**: Cross-Reference Linking (bidirectional links by vendor/spec/activity)
- **N4**: Field Backfill (missing required fields: id, status, type)
- **N5**: Key Schema Compliance (canonical key names)
- **N6**: Computed Totals (sum child records to parent)
- **N7**: Date/Format Normalization (ISO 8601, numbers as numbers)
- **N8**: Deduplication (ID match + fuzzy match)

## Subcommands

### `/data-health` (no argument) -- Full Sweep

Runs all three stages: scan -> fix -> report.

### `/data-health scan` -- Detection Only

1. **Locate Project Brain**: Read `project-config.json` to find `folder_mapping.ai_output` (typically `AI - Project Brain/`). If not found, check current working directory.

2. **Inventory all 28 files**:
   ```
   For each expected JSON file:
     - Exists? (yes/no)
     - Valid JSON? (yes/no)
     - Empty or populated? (check for empty arrays/objects)
     - Last modified date
   ```

3. **Run V1 integrity checks** (from data-integrity-watchdog methodology):
   - Orphan detection: entries referencing IDs that don't exist in target files
   - Schema gaps: missing required top-level keys per canonical schema
   - Cross-file conflicts: mismatched data between files (e.g., different totals)
   - Staleness: files not updated in expected cadence
   - Broken reference chains: links that point to non-existent records

4. **Run normalization scan** (dry run of N1-N8):
   - N1: Count status fields not matching canonical enums
   - N2: Count scalar/array mismatches
   - N3: Count missing bidirectional links
   - N4: Count entries missing required fields
   - N5: Count non-canonical key names
   - N6: Count missing computed totals
   - N7: Count non-ISO dates and string numbers
   - N8: Count potential duplicates

5. **Classify issues**:
   - **Auto-fixable**: Issues that N1-N8 patterns can resolve without human judgment
   - **Manual**: Issues requiring PM decision (conflicting data, missing source docs, ambiguous values)

6. **Output scan report**:
   ```
   ## Data Health Scan — {Project Name}
   Date: {today}

   ### File Inventory
   | File | Status | Records | Last Updated |
   |------|--------|---------|-------------|

   ### Issues Found
   | # | File | Issue | Pattern | Auto-Fix? |
   |---|------|-------|---------|-----------|

   ### Summary
   - Total issues: X
   - Auto-fixable: Y (patterns N1-N8)
   - Manual review: Z
   ```

### `/data-health fix` -- Apply Normalization

1. **Run scan first** (if not already done in this session)

2. **Generate repair plan**: For each auto-fixable issue, show:
   ```
   | # | File | Path | Before | After | Pattern |
   |---|------|------|--------|-------|---------|
   ```

3. **Confirm with user**: Present the repair plan and wait for approval. Group by pattern for readability.

4. **Execute fixes**: Apply approved patterns using a single atomic Python script per file:
   - Read all target files
   - Apply patterns in order: N5 -> N7 -> N8 -> N1 -> N4 -> N2 -> N3 -> N6
   - Write all files
   - Print change summary

5. **Post-fix validation**: Re-read all modified files and verify:
   - All files are valid JSON
   - All proposed changes applied correctly
   - No new issues introduced
   - Counter fields match actual counts

6. **Log normalization**: Add entry to `project-config.json` version_history:
   ```json
   {
     "date": "YYYY-MM-DD",
     "action": "data_normalization",
     "patterns_applied": ["N1", "N3", "N6"],
     "changes_count": 12,
     "files_modified": ["submittal-log.json", "cost-data.json"]
   }
   ```

### `/data-health report` -- Generate Health Report

Calculate and display a phase-aware confidence score for the Project Brain. The score only evaluates files that **should** have data at the current project phase -- it does not penalize for legitimately empty files (e.g., no punch list at 15% complete).

#### Step 1: Detect Project Phase

Read `schedule.json` for current phase and `project-config.json` for percent complete. Classify each of the 28 files as `active` (should have data) or `not_yet` (legitimately empty at this phase):

| Phase | % Complete | Active Files | Not-Yet Files |
|-------|-----------|-------------|---------------|
| Pre-Construction | 0% | project-config, plans-spatial, specs-quality, schedule, directory, cost-data | All others (22) |
| Site Work / Foundations | 5-20% | Above + daily-report-data, labor-tracking, procurement-log, submittal-log, drawing-log, safety-log, inspection-log, delay-log, quality-data, risk-register, environmental-log, rfi-log, change-order-log, meeting-log, action-items | punch-list, closeout-data, claims-log, pay-app-log, rendering-log, visual-context, annotation-log, daily-report-intake (8) |
| Structure / Dry-In | 20-50% | Above + pay-app-log | punch-list, closeout-data, claims-log, rendering-log, visual-context, annotation-log (6) |
| Interior / MEP | 50-80% | Above + punch-list | closeout-data, claims-log, rendering-log, visual-context, annotation-log (5) |
| Closeout | 80-100% | All 28 files | None |

**Note:** `daily-report-intake.json` is a transient buffer (cleared after each report generation) -- always classified as `not_yet` unless it has content right now.

#### Step 2: Score 4 Dimensions

**Total score: 0-100, weighted across 4 dimensions (active files only):**

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Data Completeness | 30% | Per active file: record count + required sub-structures present |
| Cross-Reference Integrity | 25% | % of bidirectional links valid + counter math correct |
| Status & Schema Quality | 25% | % of entries with canonical status + required fields + correct key names |
| Extraction Depth | 20% | How thoroughly source documents have been processed into structured data |

#### Dimension 1: Data Completeness (30%)

For each **active** file, score 0.0-1.0 based on meaningful content:

| Score | Criteria |
|-------|----------|
| 1.0 | Populated with substantial data (>3 meaningful entries or sub-structures) |
| 0.8 | Populated but thin for the project phase (e.g., 1 RFI at month 2 is fine, but 1 RFI at month 6 is thin) |
| 0.5 | Partial -- has data but missing expected sub-structures (e.g., plans-spatial with rooms but no grid lines) |
| 0.0 | Empty or only has stub/template data |

**File-specific depth checks** (score higher when these sub-structures exist):
- `plans-spatial.json`: room_schedule + grid_lines + quantities + building_areas
- `cost-data.json`: budget_by_division with line_items + contingency tracking (used/remaining)
- `schedule.json`: activities (>10) + milestones + schedule_versions
- `submittal-log.json`: compliance_matrix on entries + procurement_link
- `procurement-log.json`: line_items or building_spec on entries + submittal_ids

Final: `sum(active_file_scores) / count(active_files)`

#### Dimension 2: Cross-Reference Integrity (25%)

Check every cross-file link and counter:

| Check | Source | Target | Match On |
|-------|--------|--------|----------|
| Submittal -> Procurement | `submittal_log[].procurement_link` | `procurement_log[].po_number` | PO number |
| Procurement -> Submittal | `procurement_log[].submittal_ids[]` | `submittal_log[].submittal_id` | Submittal ID |
| RFI -> Drawing | `rfi_log[].drawing_ref` | `drawing-log.json` sheets | Sheet number |
| Schedule -> Submittal | `submittal_log[].linked_schedule_activity_id` | `schedule.json` activities | Activity ID |
| Doc counter | `documents_loaded_count` | `len(documents_loaded)` | Exact match |
| Cost math | `summary.subtotal_direct` | `sum(budget_by_division[].total)` | Exact match |
| Contingency math | `contingency - contingency_used` | `contingency_remaining` | Exact match |

Final: `valid_checks / total_checks`

#### Dimension 3: Status & Schema Quality (25%)

Combined check across all active files:

1. **Status enums** (N1): Every status field matches canonical values per file type
2. **Required fields** (N4): Every array entry has its required fields (id, status, date, etc.)
3. **Canonical keys** (N5): Top-level keys match expected names (not synonyms)
4. **Cost division schema**: All budget_by_division entries have the 6 canonical cost keys

Final: `passing_checks / total_checks`

#### Dimension 4: Extraction Depth (20%)

Measures how thoroughly source documents have been turned into structured data:

| Source | Full Score (1.0) | Partial Score |
|--------|-----------------|---------------|
| Plans | All pages processed, rooms extracted with grid refs, quantities populated | Pages processed but rooms/quantities missing |
| Specs | spec_sections + key_materials + weather_thresholds all populated | Some sections but missing materials or thresholds |
| Submittals | compliance_matrix on all entries + mix_designs where applicable | Entries exist but no compliance matrices |
| Cost | Line items on all divisions + contingency tracking | Division totals only, no line items |
| Daily Reports | `report_count / project_elapsed_days` (1.0 at full coverage) | Proportional |
| Procurement | Deep PO detail (line_items, building_spec, delivery_schedule) | Basic entries only |

Final: `sum(source_scores) / count(scored_sources)`

#### Step 3: Calculate Total

```
Total = (Completeness * 0.30) + (CrossRef * 0.25) + (Quality * 0.25) + (Depth * 0.20)
```

#### Confidence Tiers

| Score | Tier |
|-------|------|
| 90-100% | Production Ready |
| 75-89% | Good (minor gaps) |
| 60-74% | Fair (normalization recommended) |
| 40-59% | Needs Work (significant gaps) |
| 0-39% | Initial (extraction needed) |

#### Report Format

```
## Project Brain Health Report -- {Project Name}
Date: {today}
Phase: {phase_name} (~{percent}% complete)
Overall Confidence: {score}% ({tier})

### File Classification
Active files (scored): {active_count}
Not-yet files (excluded): {not_yet_count} (correct for {phase_name} phase)

### Score Breakdown
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Data Completeness | {d1}% | 30% | {w1} |
| Cross-Reference Integrity | {d2}% | 25% | {w2} |
| Status & Schema Quality | {d3}% | 25% | {w3} |
| Extraction Depth | {d4}% | 20% | {w4} |
| **Total** | | | **{total}%** |

### Active File Detail
| File | Completeness | Cross-Refs | Schema | Notes |
|------|-------------|------------|--------|-------|

### Not-Yet Files (legitimately empty at this phase)
{list of not_yet files -- no scoring, just acknowledgment}

### Gaps to Close
{files scoring below 1.0, sorted by impact, with specific recommendations}

### Improvement Recommendations
1. {highest-impact improvement}
2. {second-highest}
3. {third}
```

## Workflow Integration

### With Other Commands
- After `/process-docs` -- Run `/data-health scan` to check extraction quality
- After `/conflicts` -- Run `/data-health fix` to resolve auto-fixable items
- Before `/weekly-report` -- Run `/data-health report` for confidence score
- Before `/morning-brief` -- Quick scan for overnight data staleness

### With Agents
- **data-integrity-watchdog** (foremanos-intel): Provides the V1 detection patterns used in scan
- **conflict-detection-agent** (foremanos-intel): Provides the V2 cross-discipline conflict detection
- **project-health-monitor** (foremanos-core): Consumes the confidence score for dashboard KPIs

## Error Handling

- If a JSON file is malformed, report the error and skip that file (do not attempt repair)
- If the Project Brain path cannot be found, prompt the user to run `/set-project` first
- If no issues are found, report "All clear" with the confidence score
- If the user declines the repair plan, exit without changes

## Constraints

- **Read-only by default**: `/data-health scan` and `/data-health report` never modify files
- **Confirmation required**: `/data-health fix` always presents a repair plan before changes
- **Atomic writes**: All changes to a file happen in one write operation
- **Backup recommendation**: Suggest the user commit or snapshot before running fix on large change sets
