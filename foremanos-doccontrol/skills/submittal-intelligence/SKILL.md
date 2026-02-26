---
name: submittal-intelligence
description: >
  Review and verify submittal compliance against project specifications. Trigger phrases include "review submittal", "check submittal", "submittal compliance", "does this meet spec", "compare to spec", "submittal review", "product data review", "shop drawing review".
version: 1.0.0
---

# Submittal Intelligence Skill

## Overview

The submittal-intelligence skill performs comprehensive compliance reviews of submitted product data, shop drawings, and samples against specification requirements from project intelligence. It automates the verification process by:

- **Extracting spec requirements** from relevant CSI sections with testable, verifiable criteria
- **Parsing submittal documents** (PDFs, data sheets, shop drawings) to extract product specifications and performance data
- **Building a compliance matrix** that cross-references each specification requirement with the submitted value
- **Determining compliance status** for each line item: Compliant, Non-Compliant, Partially Compliant, or Unable to Verify
- **Generating professional review comments** suitable for architect/engineer review cycles
- **Producing an overall recommendation**: Approved, Approved as Noted, Revise and Resubmit, or Rejected
- **Tracking submission history** and flagging changes from previous revisions

The skill produces deliverables suitable for direct inclusion in RFI responses, meeting minutes, and project correspondence.

## When to Use

- **Submittal PDFs uploaded** for review by contractors or suppliers
- **Verifying products meet specifications** before purchase or installation approval
- **Preparing review comments** for architect/engineer sign-off
- **Processing shop drawing submissions** for dimensional and detail compliance
- **Evaluating "or equal" substitutions** against original specification requirements
- **Checking certification and testing data** against spec-required standards
- **Documenting compliance decisions** in the submittal log for future reference
- **Expediting review cycles** when multiple submittals require rapid turnaround

## Data Sources

- **submittal_log** — Historical record of submitted items, spec sections, review dates, and recommendation status
- **spec_sections** — Structured project specifications with required fields:
  - `submittal_required` (boolean) — indicates if spec section requires submittal review
  - `key_req` (array) — critical requirements in natural language
  - `tolerances` (object) — dimensional and performance tolerances
  - `testing` (array) — ASTM, ASHRAE, or other standards for verification
  - `environmental` (object) — VOC, lead-free, sustainability requirements
  - `divisions` (CSI division codes) — Division 03, 05, 07, 08, 09, etc.
- **key_materials** — Material specifications database with properties, certifications, and approved equal products
- **document-intelligence skill** — Used to parse and extract data from submittal PDFs, data sheets, and shop drawings
- **project-data skill** — Used to retrieve and reference project-specific requirements and approved materials

## Workflow

### 1. Identify the Submittal
- Retrieve submittal ID from submittal_log if resubmission
- Or accept new submittal document (PDF, image, data sheet)
- Extract cover letter, item description, and submission metadata

### 2. Determine the Spec Section
- Query submittal_log by submittal ID to find associated CSI spec section
- If new submittal, ask user to specify relevant spec section (e.g., "Division 03 Concrete", "Division 08 Doors and Frames")
- Confirm with user if ambiguous

### 3. Load Spec Requirements
- Retrieve spec section from project intelligence
- Extract all relevant requirements into a structured checklist:
  - Material properties (grade, PSI, finish, color)
  - Dimensional tolerances (sizes, clearances)
  - Performance ratings (fire ratings, sound ratings, load capacity)
  - Testing standards (ASTM references with specific test methods)
  - Environmental compliance (VOC limits, lead-free, RoHS)
  - Certifications (UL, ICC, NFRC, FINEGRAIN, etc.)
- Note any "or equal" or "approved equal" clauses that allow substitutions

### 4. Parse Submittal Document
- Use document-intelligence skill to extract:
  - Product name, model, manufacturer
  - Technical specifications and properties
  - Dimensional data (from shop drawings or product data)
  - Testing certifications and lab reports
  - Material certifications and safety data
  - Installation notes and conditions
- Organize extracted data in same format as spec requirements for direct comparison

### 5. Build Compliance Matrix
- Create line-by-line comparison table:
  - Column 1: Spec Requirement (reference code, e.g., "03.03.01")
  - Column 2: Requirement Text (extract from spec)
  - Column 3: Submitted Value (extract from submittal document)
  - Column 4: Compliance Status (Compliant / Non-Compliant / Partially Compliant / Unable to Verify)
  - Column 5: Notes (explanation or citation)
- Sort by compliance status to highlight non-compliances first

### 5a. Auto-Populated Compliance Matrix
When `/process-docs` processes a submittal package, the compliance matrix should be auto-populated before the user runs `/submittal-review`:

1. From the submittal package, extract all product specifications (model, performance values, certifications, test reports)
2. From `specs-quality.json`, load the relevant spec section requirements for the material type
3. For each spec requirement, find the corresponding submitted value:
   - Match by property name (e.g., "compressive strength" in spec → "f'c" in submittal)
   - Match by ASTM standard (e.g., spec requires "per ASTM C39" → look for C39 test results)
   - Match by performance category (e.g., "fire rating" in spec → "UL listing" in submittal)
4. Pre-populate the compliance matrix:
   ```
   | Spec Requirement | Required Value | Submitted Value | Compliance | Source |
   |---|---|---|---|---|
   | Compressive strength | ≥4,000 PSI | 4,500 PSI | ✅ PASS | Mix design report p.2 |
   | w/c ratio | ≤0.45 | 0.42 | ✅ PASS | Mix design report p.3 |
   | Air content | 5-7% | Not provided | ❓ MISSING | — |
   ```
5. Flag any row where:
   - Submitted value < required value → FAIL
   - Submitted value is missing → MISSING DATA
   - Submitted value can't be compared (different units, different test standard) → NEEDS MANUAL REVIEW

This auto-population happens during `/process-docs` extraction. The `/submittal-review` command then presents the pre-filled matrix for the superintendent to confirm, override, or supplement with field observations.

### 6. Determine Compliance Status
- **Compliant** — Submitted value exactly matches or exceeds spec requirement
- **Non-Compliant** — Submitted value falls short of spec requirement (cite specific deficiency)
- **Partially Compliant** — Submittal addresses requirement in part but leaves ambiguities or conditions
- **Unable to Verify** — Required specification data missing from submittal (request clarification)
- See compliance-checking.md for detailed determination rules and examples

### 6a. Concrete Mix Design Submittal Review
When reviewing concrete mix design submittals, refer to the concrete-mix-design-extraction template in the foremanos-intel plugin's document-intelligence skill for detailed extraction guidance (if installed). Key compliance checks:
- Design f'c meets or exceeds specified f'c (with appropriate overdesign margin)
- w/c ratio does not exceed specified maximum
- Air content within specified range (especially for freeze-thaw exposure)
- Cement type matches spec requirement (Type I, II, III, V)
- Aggregate meets gradation and maximum size requirements
- Admixtures are from approved manufacturers list (if specified)
- Lab performing trial batch is accredited
- Cold weather and hot weather modification plans are included if project has temperature-dependent specs

### 7. Generate Overall Recommendation
Synthesize compliance matrix into recommendation:

- **Approved** — All requirements met, no deviations or exceptions. Ready for installation/procurement.
- **Approved as Noted** — All critical requirements met; minor clarifications, conditions, or non-critical deviations noted. Approved with contingencies documented.
- **Revise and Resubmit** — Specific deficiencies identified. Contractor must address identified items and resubmit. Cite section references and required corrections.
- **Rejected** — Does not meet fundamental spec requirements. Resubmit with different product/approach or escalate for waiver consideration.

### 8. Draft Review Comments
- Write in professional, objective tone suitable for RFI response or meeting minutes
- Use structured comment format: [Status] | [Spec Reference] | [Finding] | [Required Action]
- Group comments by spec section or compliance status
- Include recommendations for follow-up (additional testing, certification, shop drawings, etc.)
- Cite all references to spec sections, ASTM standards, test reports
- For non-compliances, specify corrective action required

### 9. Update Submittal Log
- Record review date, reviewer, recommendation, and comments
- Link to compliance matrix and any supporting documents
- If resubmission, note previous revision status and what changed
- Flag for escalation if needed (structural engineer, code official, etc.)

## Review Comment Language Standards

### Approved
> The submitted [product/material] meets all applicable specification requirements and is approved for [procurement/installation].

### Approved as Noted
> The submitted [product/material] meets specification requirements subject to the following conditions/clarifications:
> - [Condition 1]: [explanation, deadline, or required action]
> - [Condition 2]: ...
> Approval granted pending completion of noted items.

### Revise and Resubmit
> The submitted [product/material] does not meet specification in the following respects:
> - [Reference code] [Requirement]: Specification requires [required value]. Submittal provides [submitted value]. [Specific corrective action required].
> - [Reference code] [Requirement]: ...
> Please resubmit with corrections or request formal waiver if waiver is intended.

### Rejected
> The submitted [product/material] is not acceptable due to non-compliance with fundamental specification requirements:
> - [Critical deficiency 1]
> - [Critical deficiency 2]
> Resubmit with alternative product meeting all spec requirements, or submit formal waiver request for architect/engineer consideration.

## Lead-Time Alert System

The submittal-intelligence skill tracks submittal timelines and flags items at risk of missing critical path deadlines. This system prevents procurement delays, schedule impacts, and last-minute rush approvals.

### Must-Submit-By Calculation

Working backwards from each submittal's critical path impact:

**Timeline Logic**:
1. **Activity Start Date** (from `schedule.json` → activities linked to this submittal)
2. **Minus Material Lead Time** (from procurement specs or supplier standard terms)
3. **Minus Fabrication Time** (manufacturer lead time after order placed; typically 2-8 weeks)
4. **Minus Approval Cycle Time** (architect/engineer review to approval):
   - Standard products (common, pre-approved): 2-4 weeks
   - Complex/custom products (engineered, mock-ups, samples): 4-6 weeks
5. **Minus Preparation Time** (contractor prep of drawings, samples, certifications): 1-2 weeks

**Example Calculation**:
```
Activity start date (PEMB erection): 03/23/2026
Minus: PEMB lead time: 30 days
Minus: Fabrication time: Already in PEMB lead time, covered
Minus: Approval cycle (engineered): 4 weeks
Minus: Preparation (drawings ready): 1 week
───────────────────────────────────
Must-submit-by date: 02/02/2026
```

### Alert Tiers

Three escalating alert levels based on days remaining until must-submit-by date:

| Tier | Days Remaining | Status | Action |
|------|---|---|---|
| **CRITICAL** | Past due (negative) | Red flag | Submittal missed deadline. Escalate to PM/engineer immediately. Assess schedule impact. May require expedited review or change order. |
| **WARNING** | 0-7 days | Yellow flag | Due within one week. Verify submittal ready for submission. Confirm with architect review slot reserved. Prepare expedited review package if needed. |
| **WATCH** | 8-21 days | Blue flag | Due within 3 weeks. Monitor preparation progress. Confirm no blockers (missing data, approvals, samples). Schedule architect review. |
| **NORMAL** | >21 days | Green | On track. No action needed. Continue normal schedule. |

### Daily Morning-Brief Auto-Check

The `/morning-brief` command automatically scans `submittal-log.json` and generates an alert summary:

**Query logic**:
- Find all submittals with `status` != "approved"
- Calculate `must-submit-by` date working backwards from linked schedule activities
- Compare to today's date
- Generate alert for each tier

**Morning Brief Output Example**:
```
SUBMITTAL STATUS — ALERTS ONLY (3 items at risk)

🔴 CRITICAL — Past Due
  • Nucor PEMB Reaction Drawing (SUB-008)
    Status: "under_review" (submitted 02/09, 9 days ago)
    Needed by: 02/02 (7 DAYS PAST DUE)
    Impact: PEMB erection critical path blocked
    Action: Call Nucor today; escalate to CMW architect

🟡 WARNING — Due in 3 Days
  • Schiller Door Hardware (SUB-012)
    Status: "revision_submitted" (resubmit 02/15)
    Needed by: 02/18 (3 days)
    Impact: Door procurement dependent
    Action: Confirm with architect; hold time slot for review

🔵 WATCH — Due in 18 Days
  • Davis & Plomin HVAC Equipment (SUB-015)
    Status: "under_review" (submitted 02/10)
    Needed by: 03/05 (18 days)
    Impact: HVAC procurement, MEP rough-in scheduled 04/27
    Action: No urgent action; normal tracking
```

## Project Intelligence Integration

When reviewing submittals or generating alerts, automatically enrich with data from the project intelligence store. These cross-references improve review accuracy and catch procurement/schedule risks early.

### Procurement Lead Time Enrichment
Read `procurement-log.json` → For each submittal, look up the corresponding procurement entry by `submittal_id`. Pull `expected_delivery`, `lead_time_weeks`, and `delivery_status` → auto-populate `fabrication_days` and `material_lead_time_days` in the submittal record. If procurement entry shows `delivery_status` = "delayed", escalate the submittal alert tier accordingly.

### Sub Contact Resolution
Read `directory.json` → `subcontractors[]` → When a submittal is overdue or needs follow-up, resolve the responsible sub's foreman name, phone, and email from the directory. Auto-fill contact information in alert action items: "Contact {foreman} at {phone} ({sub_name}) to expedite SUB-{id}."

### Inspection Hold Point Linking
Read `specs-quality.json` → `hold_points[]` → For each submittal's `spec_section`, check if any hold points require submittal approval before the inspection can proceed. Flag linked hold points: "SUB-{id} approval is a prerequisite for hold point HP-{hp_id} ({inspection_name}). Inspection cannot proceed until this submittal is approved."

### Cost Impact Flagging
Read `cost-data.json` → For submittals linked to critical path activities or high-value budget line items, show the budget amount at risk if approval is delayed. Include in alert output: "Budget line item {division} — {description}: ${amount} at risk if SUB-{id} delays procurement by {N} days."

### Quality Test Correlation
Read `quality-data.json` → After a submittal is approved (status = "approved"), link subsequent material test results back to the approved submittal. For example, an approved concrete mix design (SUB-XXX) should be cross-referenced when 7-day and 28-day break results arrive: "Break test results for {mix_id} — 28-day f'c = {value} PSI vs. approved design f'c = {design_value} PSI. Status: {pass/fail}."

### Installation Verification
Read `daily-report-data.json` → Flag if materials from a submittal are documented as installed in a daily report before the submittal status = "approved": "WARNING: {material} from SUB-{id} appears installed per daily report #{report_number} on {date}, but submittal status is still '{status}'. Verify approval before installation proceeds."

### Submittal-Log Data Structure

For lead-time tracking, each submittal in `submittal-log.json` must include:

```json
{
  "id": "SUB-008",
  "item": "PEMB Reaction Drawing",
  "spec_section": "05 42 00",
  "submitting_sub": "Alexander Construction / Nucor",
  "status": "under_review",
  "submitted_date": "2026-02-09",
  "must_submit_by_date": "2026-02-02",
  "approval_cycle_days": 4,
  "material_lead_time_days": 30,
  "fabrication_days": 0,
  "preparation_days": 7,
  "linked_schedule_activity_id": "A45-PEMB-Erection",
  "linked_activity_start_date": "2026-03-23",
  "critical_path_blocked": true,
  "days_past_due": 7,
  "alert_tier": "CRITICAL",
  "notes": "Nucor sent initial, needs revisions for anchor bolt details"
}
```

### Rejection/Resubmission Workflow

When a submittal is rejected or returned for revisions, auto-calculate new timeline impact:

**Trigger**: Submittal status changes from "under_review" to "revise_and_resubmit" or "rejected"

**Auto-Calculation**:
1. Set new `revision_number` (increment from previous)
2. Capture original `must_submit_by_date`
3. Record `rejection_reason` from architect's comments
4. Estimate resubmission time (typically 3-5 business days for major revisions, 1-2 for minor)
5. Add resubmission lead time to today to get new `expected_resubmit_date`
6. Recalculate new `must_submit_by_date` (if 2nd revision, time is even tighter)
7. Compare new deadline to original; flag if slipping past must-submit-by
8. Alert to PM: "Resubmission due [date]. New approval cycle leaves [N] day margin."

**Example Rejection Timeline**:
```
SUB-008 PEMB Reaction Drawing (Nucor)
Original submission: 02/09
Original must-submit-by: 02/02 (MISSED by 7 days)
Rejection date: 02/12
Rejection reason: "Anchor bolt embedment depth needs verification per geotechnical report"
Estimated resubmission: 02/15 (3 days for revisions)
New approval cycle: 4 days (expedited given past-due status)
New must-submit-by: 02/19 (16 days past original deadline!)
Action: Flag to PM; assess schedule impact; consider change order if erection delayed
```

### Resubmission Tracking

Track each revision with separate entries to maintain history:

**In `submittal-log.json`**:
```json
{
  "id": "SUB-008",
  "item": "PEMB Reaction Drawing",
  "revision_history": [
    {
      "revision_number": 1,
      "submitted_date": "2026-02-09",
      "status": "revise_and_resubmit",
      "rejection_reason": "Anchor bolt embedment depth needs verification per geotechnical report",
      "rejection_date": "2026-02-12",
      "approval_cycle_days": 4,
      "must_submit_by_date": "2026-02-02",
      "days_late": 7
    },
    {
      "revision_number": 2,
      "submitted_date": "2026-02-15",
      "expected_approval_date": "2026-02-19",
      "status": "under_review",
      "approval_cycle_days": 4,
      "must_submit_by_date": "2026-02-19",
      "days_late": 17,
      "turnaround_time_days": 3,
      "notes": "Expedited review requested; geotechnical verification confirmed"
    }
  ],
  "current_revision_number": 2,
  "total_revisions": 2
}
```

### Critical Path Submittal Flagging

Cross-reference each submittal with `schedule.json` critical path to flag items that will block the schedule if delayed:

**Linking logic**:
- Submittal's `spec_section` maps to `schedule.json` material requirement
- Check if linked activity has `float` = 0 or < 5 days
- If yes, set `critical_path_blocked` = true
- These submittals get priority flagging in alerts

**Example**:
```
SUB-008 PEMB Reaction Drawing
  Linked activity: A45-PEMB-Erection (critical path)
  Float: 0 days
  Flag: CRITICAL_PATH_BLOCKED = true
  Alert priority: Highest — any delay impacts substantial completion

SUB-015 HVAC Equipment Data
  Linked activity: A72-MEP-Rough-In (near-critical, float = 5)
  Float: 5 days
  Flag: CRITICAL_PATH_BLOCKED = false (but near-critical)
  Alert priority: Medium — some schedule cushion but tight
```

### Integration with /morning-brief and /daily-report

**Morning Brief (`/morning-brief`)**:
- Scan all submittals with `status` != "approved"
- List only CRITICAL and WARNING tiers (skip WATCH/NORMAL unless requested)
- Include must-submit-by dates and linked activities
- Provide action items for each flagged item

**Daily Report (`/daily-report`)**:
- Include new rejections or resubmissions in "Open Items" section
- Note any submittals that crossed into CRITICAL or WARNING during the day
- Track turnaround time for resubmissions (days between rejection and resubmit)
- Update schedule impact assessment if critical path activities are affected

## Cross-References

- **project-data skill** — Retrieves project-specific spec sections, approved materials, and submittal requirements
- **document-intelligence skill** — Parses PDFs and extracts structured data from submittal documents, data sheets, test reports, and shop drawings
- **spec-requirement-extraction.md** — Detailed guidance on identifying and structuring testable requirements from CSI specs
- **compliance-checking.md** — Detailed determination rules, evaluation methodology, and review comment templates
