---
name: data-normalization
description: >
  Project-agnostic data normalization patterns for the 28-file Project Brain.
  Defines 8 repeatable patterns (N1-N8) that fix common data quality issues:
  status standardization, counter reconciliation, cross-reference linking,
  field backfill, schema compliance, computed totals, date/format normalization,
  and deduplication. Safe to re-run (idempotent). Outputs a repair plan before executing.
version: 1.0.0
---

# Data Normalization

## Overview

This skill defines **8 normalization patterns** that can be applied to any ForemanOS Project Brain to fix common data quality issues. Each pattern is idempotent (safe to re-run) and produces a **repair plan** showing what will change before executing.

The patterns complement the detection layer (data-integrity-watchdog agent, conflict-detection-agent) by providing the **fix** side of the data health stack.

## Prerequisites

Before applying any pattern, the AI must:
1. Read the target JSON file(s) in full
2. Read `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` for canonical key names
3. Generate a repair plan listing every proposed change (field path, before value, after value)
4. Present the repair plan to the user for confirmation
5. Apply changes via a single atomic Python script that reads → modifies → writes all affected files
6. Validate the output (re-read and confirm changes applied)

## Repair Plan Format

Before any changes, output a table:

```
| # | File | Path | Before | After | Pattern |
|---|------|------|--------|-------|---------|
| 1 | submittal-log.json | submittal_log[1].status | "submitted" | "SUBMITTED" | N1 |
| 2 | cost-data.json | summary.contingency_remaining | (missing) | 43225 | N6 |
```

Only proceed after user confirmation.

---

## Pattern N1: Status Standardization

**Problem**: Mixed case and wording in status fields across different JSON files.

**Logic**: Each file type has canonical status enums. Normalize all status fields to match.

### Canonical Status Values

| File | Field | Valid Values |
|------|-------|-------------|
| `submittal-log.json` | `submittal_log[].status` | `APPROVED`, `SUBMITTED`, `REVIEW_PENDING`, `REJECTED`, `RESUBMIT`, `APPROVED_AS_NOTED` |
| `submittal-log.json` | `submittal_log[].compliance_matrix.compliance_status` | `COMPLIANT`, `NON_COMPLIANT`, `REVIEW_PENDING`, `PARTIAL` |
| `inspection-log.json` | `inspection_log[].result` | `pass`, `fail`, `conditional`, `pending` |
| `risk-register.json` | `risks[].status` | `open`, `closed`, `monitoring`, `mitigated` |
| `procurement-log.json` | `procurement_log[].status` | `quoted`, `executed`, `executed_with_co`, `delivered`, `cancelled` |
| `rfi-log.json` | `rfi_log[].status` | `Draft`, `Submitted`, `Responded`, `Closed` |
| `change-order-log.json` | `change_order_log[].status` | `pending`, `approved`, `rejected`, `executed` |
| `punch-list.json` | `punch_list[].status` | `open`, `in_progress`, `completed`, `verified` |
| `action-items.json` | `items[].status` | `open`, `in_progress`, `resolved`, `deferred` |
| `project-config.json` | `documents_loaded[].status` | `current`, `extracted`, `received`, `finalized`, `filed`, `template`, `submitted`, `executed`, `superseded`, `superseded_by_conformance`, `logged` |

### Normalization Rules

1. Case-insensitive match to canonical value (e.g., "submitted" -> "SUBMITTED" for submittals)
2. Synonym mapping:
   - "approved" / "APPROVED" / "Approved" -> `APPROVED`
   - "review_pending" / "Review Pending" / "REVIEW PENDING" / "pending_review" -> `REVIEW_PENDING`
   - "assumed_passed" -> `pass` (for inspections)
   - "in progress" / "In Progress" / "IN_PROGRESS" -> `in_progress`
3. If no match found, flag for manual review (do not auto-fix)

### Application

```python
# Pseudocode
for entry in submittal_log:
    normalized = normalize_status(entry["status"], SUBMITTAL_STATUSES)
    if normalized != entry["status"]:
        plan.append(change(entry, "status", entry["status"], normalized, "N1"))
```

---

## Pattern N2: Counter Reconciliation

**Problem**: Stored scalar counts drift from actual array lengths after edits.

**Logic**: Recount from source arrays, compare to stored scalar, fix if mismatched.

### Known Counter Fields

| File | Scalar Field | Source Array | Expected |
|------|-------------|-------------|----------|
| `project-config.json` | `documents_loaded_count` | `documents_loaded[]` | `len(documents_loaded)` |
| `project-config.json` | `total_documents` | `documents_loaded[]` | `len(documents_loaded)` |
| `plans-spatial.json` | `room_count` (if present) | `room_schedule[]` | `len(room_schedule)` |
| `delay-log.json` | `total_weather_days` (if present) | `delay_events[]` where type=Weather | Sum of `days_impact` |
| `safety-log.json` | `osha_300_log.total_hours` | `labor-tracking.json` labor_entries | Sum of `hours` |
| `cost-data.json` | `summary.subtotal_direct` | `budget_by_division[]` | Sum of `total` |
| `pay-app-log.json` | `schedule_of_values.total_contract` | `schedule_of_values.line_items[]` | Sum of `scheduled_value` |

### Application

```python
actual = len(data["documents_loaded"])
stored = data.get("documents_loaded_count", None)
if stored != actual:
    plan.append(change("documents_loaded_count", stored, actual, "N2"))
```

---

## Pattern N3: Cross-Reference Linking

**Problem**: Missing bidirectional references between related records across files.

**Logic**: Match by vendor name, spec section, activity ID, or other shared identifiers. Add link fields.

### Link Definitions

| Source File | Source Field | Target File | Target Field | Match On |
|------------|-------------|-------------|-------------|----------|
| `submittal-log.json` | `submittal_log[].procurement_link` | `procurement-log.json` | `procurement_log[].po_number` | Vendor name match |
| `procurement-log.json` | `procurement_log[].submittal_ids[]` | `submittal-log.json` | `submittal_log[].submittal_id` | Vendor name match |
| `rfi-log.json` | `rfi_log[].related_submittals[]` | `submittal-log.json` | `submittal_log[].submittal_id` | Spec section match |
| `schedule.json` | `activities[].linked_submittals[]` | `submittal-log.json` | `submittal_log[].submittal_id` | Activity ID match |
| `change-order-log.json` | `change_order_log[].procurement_link` | `procurement-log.json` | `procurement_log[].po_number` | Description/vendor match |
| `inspection-log.json` | `inspection_log[].linked_activity` | `schedule.json` | `activities[].id` | Activity match |
| `quality-data.json` | `inspections[].submittal_ref` | `submittal-log.json` | `submittal_log[].submittal_id` | Spec section match |

### Matching Rules

1. **Vendor match**: Case-insensitive substring match on supplier/vendor name. "Schiller" matches "Schiller Architectural Hardware".
2. **Spec section match**: Normalize to format "XX XX XX" (spaces, no dashes). "08 11 13" matches "081113".
3. **Activity ID match**: Exact match on `linked_schedule_activity_id` or `activity_id`.
4. **Only add links** — never remove existing links. If a link field already exists and has a value, skip.

### Application

```python
# Match submittals to procurement by vendor
for sub in submittal_log:
    if "procurement_link" not in sub or not sub["procurement_link"]:
        for po in procurement_log:
            if vendor_match(sub.get("vendor",""), po.get("supplier","")):
                sub["procurement_link"] = po["po_number"]
                po.setdefault("submittal_ids", [])
                if sub["submittal_id"] not in po["submittal_ids"]:
                    po["submittal_ids"].append(sub["submittal_id"])
                break
```

---

## Pattern N4: Field Backfill

**Problem**: Array entries missing required fields (status, id, type, dates).

**Logic**: Apply defaults based on existing data context.

### Required Fields by File

| File | Array | Required Fields | Default Logic |
|------|-------|----------------|---------------|
| `project-config.json` | `documents_loaded[]` | `id`, `status` | `id`: "DOC-{index+1:03d}". `status`: "extracted" if has extraction_data, "received" if has filename only |
| `submittal-log.json` | `submittal_log[]` | `submittal_id`, `status`, `spec_section` | `submittal_id`: "SUB-{index+1:03d}". `status`: "SUBMITTED" if date exists |
| `procurement-log.json` | `procurement_log[]` | `po_number`, `status`, `supplier` | `status`: "quoted" if has quote_date, "executed" if has executed_date |
| `rfi-log.json` | `rfi_log[]` | `id`, `status`, `date_created` | `id`: "RFI-{index+1:03d}". `status`: "Draft" if no response |
| `inspection-log.json` | `inspection_log[]` | `id`, `result`, `date` | `result`: "pending" if no result recorded |
| `labor-tracking.json` | `labor_entries[]` | `id`, `date`, `company` | `id`: "LBR-{index+1:03d}" |
| `risk-register.json` | `risks[]` | `id`, `status`, `probability`, `impact` | `status`: "open" if no status |

### Application

```python
for i, doc in enumerate(documents_loaded):
    if "id" not in doc:
        doc["id"] = f"DOC-{i+1:03d}"
        plan.append(change(f"documents_loaded[{i}].id", "(missing)", doc["id"], "N4"))
    if "status" not in doc:
        status = infer_status(doc)
        doc["status"] = status
        plan.append(change(f"documents_loaded[{i}].status", "(missing)", status, "N4"))
```

---

## Pattern N5: Key Schema Compliance

**Problem**: Wrong key names or missing required top-level keys.

**Logic**: Check against canonical keys from the project-data skill. Rename or add missing keys.

### Canonical Top-Level Keys

Reference: `foremanos-core/skills/project-data/references/json-schema-reference.md`

| File | Required Top-Level Keys |
|------|------------------------|
| `schedule.json` | `activities`, `milestones`, `critical_path`, `weather_sensitive_activities` |
| `delay-log.json` | `delay_events` |
| `rfi-log.json` | `rfi_log` |
| `meeting-log.json` | `meeting_log` |
| `inspection-log.json` | `inspection_log`, `permit_log` |

### Common Renames

| Wrong Key | Correct Key | File |
|-----------|------------|------|
| `construction_activities` | `activities` | schedule.json |
| `delays` | `delay_events` | delay-log.json |
| `rfis` | `rfi_log` | rfi-log.json |
| `meetings` | `meeting_log` | meeting-log.json |

### Application

```python
if "construction_activities" in schedule and "activities" not in schedule:
    schedule["activities"] = schedule.pop("construction_activities")
    plan.append(rename("construction_activities", "activities", "N5"))
```

---

## Pattern N6: Computed Totals

**Problem**: Missing aggregated values that should be computed from child records.

**Logic**: Sum from child records, write to parent field.

### Computed Fields

| File | Computed Field | Formula |
|------|---------------|---------|
| `cost-data.json` | `summary.subtotal_direct` | `sum(budget_by_division[].total)` |
| `cost-data.json` | `summary.contingency_used` | `sum(change_orders where source=contingency)` or from CO log |
| `cost-data.json` | `summary.contingency_remaining` | `contingency - contingency_used` |
| `cost-data.json` | `summary.total_committed` | `sum(budget_by_division[].committed_costs)` |
| `cost-data.json` | `budget_by_division[].current_amount` | `total + sum(applied_cos[].amount)` |
| `risk-register.json` | `total_exposure` | `sum(risks[].exposure)` |
| `pay-app-log.json` | `current_retainage` | Computed from pay app percentages |
| `labor-tracking.json` | `total_hours` | `sum(labor_entries[].hours)` |
| `delay-log.json` | `total_delay_days` | `sum(delay_events[].days_impact)` |

### Application

```python
used = sum(co["amount"] for co in change_orders if co.get("source") == "contingency")
# Or from known COs:
used = 6775  # Nucor CO#1
remaining = summary["contingency"] - used
if "contingency_used" not in summary:
    summary["contingency_used"] = used
    plan.append(change("summary.contingency_used", "(missing)", used, "N6"))
if "contingency_remaining" not in summary:
    summary["contingency_remaining"] = remaining
    plan.append(change("summary.contingency_remaining", "(missing)", remaining, "N6"))
```

---

## Pattern N7: Date/Format Normalization

**Problem**: Inconsistent date formats and number types across files.

**Logic**: Standardize all dates to ISO 8601, all numeric values as numbers (not strings).

### Rules

1. **Dates**: All date fields must be ISO 8601 format: `YYYY-MM-DD`
   - "01/22/2026" -> "2026-01-22"
   - "Jan 22, 2026" -> "2026-01-22"
   - "1/22/26" -> "2026-01-22"
   - If ambiguous (e.g., "02/03/26"), prefer US format (MM/DD/YY)

2. **Numbers**: Numeric fields must be actual numbers, not strings
   - `"184500"` -> `184500`
   - `"$184,500"` -> `184500`
   - `"15.5%"` -> `0.155` (for rate fields) or `15.5` (for display fields — context-dependent)

3. **Booleans**: Boolean fields must be actual booleans
   - `"true"` / `"yes"` / `"Y"` -> `true`
   - `"false"` / `"no"` / `"N"` -> `false`

### Date Fields to Check

| File | Date Fields |
|------|------------|
| `project-config.json` | `documents_loaded[].date`, `version_history[].date` |
| `submittal-log.json` | `submittal_log[].date`, `[].review_date`, `[].must_submit_by_date` |
| `procurement-log.json` | `procurement_log[].quote_date`, `[].executed_date`, `[].delivery_schedule.*` |
| `schedule.json` | `milestones[].date`, `activities[].start`, `[].finish` |
| `rfi-log.json` | `rfi_log[].date_created`, `[].date_responded` |
| `change-order-log.json` | `change_order_log[].date`, `[].approved_date` |
| `inspection-log.json` | `inspection_log[].date`, `[].next_date` |

---

## Pattern N8: Deduplication

**Problem**: Duplicate entries in arrays from multiple extraction passes or manual entry.

**Logic**: Detect by ID field or fuzzy match on description + date. Merge or flag.

### Detection Rules

1. **Exact ID match**: Two entries with same `id` / `submittal_id` / `po_number` -> merge (keep the one with more fields populated)
2. **Fuzzy match**: Same `vendor` + same `spec_section` + dates within 7 days -> flag for review
3. **Content match**: Same `description` (case-insensitive, trimmed) + same `date` -> merge

### Merge Strategy

When merging duplicates:
1. Keep the entry with more populated fields
2. Copy any non-null fields from the less-complete entry that are missing in the keeper
3. Record the merge in a `_merge_note` field: "Merged from duplicate entry on {date}"
4. Never delete — mark the duplicate with `_duplicate_of: "{keeper_id}"` and remove from the main array

### Application

```python
seen = {}
for entry in submittal_log:
    key = entry.get("submittal_id")
    if key in seen:
        # Merge: keep entry with more fields
        keeper = seen[key] if len(seen[key]) >= len(entry) else entry
        donor = entry if keeper is seen[key] else seen[key]
        for k, v in donor.items():
            if k not in keeper or keeper[k] is None:
                keeper[k] = v
        keeper["_merge_note"] = f"Merged duplicate {donor.get('submittal_id')}"
        plan.append(merge(key, "N8"))
    else:
        seen[key] = entry
```

---

## Execution Order

When running all 8 patterns on a Project Brain:

1. **N5** (Schema Compliance) — Fix key names first so other patterns find data
2. **N7** (Date/Format) — Normalize types before comparisons
3. **N8** (Deduplication) — Remove duplicates before counting
4. **N1** (Status Standardization) — Normalize status values
5. **N4** (Field Backfill) — Fill missing required fields
6. **N2** (Counter Reconciliation) — Recount after dedup and backfill
7. **N3** (Cross-Reference Linking) — Link after all entries are clean
8. **N6** (Computed Totals) — Compute aggregates last

## Integration with `/data-health` Command

The `/data-health` command in the `foremanos-compliance` plugin orchestrates these patterns:
- `/data-health scan` — Runs detection only (finds issues that N1-N8 would fix)
- `/data-health fix` — Applies patterns with confirmation
- `/data-health report` — Generates health score including normalization coverage

## Constraints

- **Never delete data** — Only add, rename, or modify fields
- **Always confirm** — Present repair plan before any changes
- **Atomic writes** — All changes to a file happen in one write operation
- **Preserve formatting** — Use `json.dumps(data, indent=2, ensure_ascii=False)` for output
- **Log changes** — After applying, add a `_normalization_log` entry to `project-config.json` version_history:
  ```json
  {
    "date": "2026-02-26",
    "action": "data_normalization",
    "patterns_applied": ["N1", "N3", "N6"],
    "changes_count": 12,
    "files_modified": ["submittal-log.json", "procurement-log.json", "cost-data.json"]
  }
  ```
