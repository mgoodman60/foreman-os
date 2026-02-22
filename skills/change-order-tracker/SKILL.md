---
name: change-order-tracker
description: >
  Track change orders from initiation through resolution. Handles CO creation, status updates, cost/schedule impact tracking, and CO log generation. Integrates with morning brief (pending COs) and weekly report (CO summary). Triggers: "change order", "CO", "PCO", "COR", "add a change order", "CO status", "CO log", "pending change orders".
version: 1.0.0
---

# Change Order Tracker Skill

## Overview

The **change-order-tracker** skill provides comprehensive change order management for construction projects. It enables superintendents to track change orders through their complete lifecycle—from initiation through approval or rejection—while maintaining cost and schedule impact visibility for project leadership and stakeholders.

## Change Order Lifecycle

Change orders progress through a defined workflow to ensure proper review and authorization:

```
[draft] → [submitted] → [under_review] → [approved]
                                       ↓
                                    [rejected]
                                       ↓
                                      [void]
```

### Lifecycle Stages

| Stage | Description | Actions Allowed |
|-------|-------------|-----------------|
| **draft** | CO created but not yet submitted for review | Edit details, submit, discard |
| **submitted** | CO submitted to project manager/owner | Wait for review, update notes, withdraw |
| **under_review** | CO under active review by PM/owner | View review comments, provide clarifications |
| **approved** | CO approved by authorized personnel | Lock CO, implement changes, track actual costs |
| **rejected** | CO rejected by project manager/owner | Request revision or create new CO |
| **void** | CO cancelled and no longer active | Archive, reference for historical records |

## Change Order Fields

Each change order maintains the following structured data:

### Core Identification
- **id**: Unique CO identifier (CO-NNN format, immutable)
- **date_submitted**: ISO 8601 timestamp of submission (set at "submitted" status transition)
- **status**: Current position in workflow (draft|submitted|under_review|approved|rejected|void)

### Request Details
- **description**: Detailed narrative of the change requested
- **originator**: Source of request (owner|architect|field|sub) — critical for cost allocation and communication
- **notes**: Running log of review comments, clarifications, and resolution details

### Impact Tracking
- **cost_impact**: Estimated additional cost in dollars (or "TBD" if not yet quantified)
- **approved_amount**: Final authorized cost (populated when approved)
- **schedule_impact_days**: Number of calendar days impacted on project timeline
- **running_cost_total**: Aggregate of all approved COs to date
- **running_schedule_total**: Aggregate days impact from all approved COs

### Scope References
- **affected_spec_sections**: Array of specification section numbers impacted (e.g., ["05120", "08710"])
- **affected_subs**: Array of subcontractor names required to implement change
- **linked_asis**: Array of associated ASI numbers (ASI-NNN)
- **linked_rfis**: Array of associated RFI numbers (RFI-NNN)

### Authorization
- **approved_by**: Name/title of approving authority (PM, Owner, Architect)
- **resolution_date**: Date CO reached final status (approved, rejected, or voided)

## CO Numbering System

Change order IDs follow the format **CO-{NNN}** where NNN is a zero-padded three-digit counter:
- First CO: CO-001
- Second CO: CO-002
- Pattern: CO-100, CO-101, etc.

**Key Rules:**
- Numbers auto-increment based on highest existing CO
- **Numbers are locked immediately upon creation** — never reused or reassigned
- Voided COs retain their original number (CO-005 may be marked "void", but CO-006 comes next, never CO-005 again)
- System maintains sequence integrity even across multiple sessions/users

**Implementation:**
Query change_order_log at creation time, find max CO number, increment by 1, assign and lock.

## Status Workflow Rules

### Transition Rules
- **draft → submitted**: User confirms CO is ready for review (no approval required)
- **submitted → under_review**: PM/PM acknowledges and begins formal review (automatic on first review action)
- **under_review → approved**: Authorized approver (PM/owner) confirms and locks cost/schedule
- **under_review → rejected**: Approver denies and explains reason
- **Any status → void**: User can void a CO at any time (creates audit trail entry)

### Validation on Transitions
- **To approved**: Approved amount must be populated (≥ 0)
- **To rejected**: Reason/notes must be recorded
- **To void**: Reason recorded in notes
- **To submitted**: Description must be non-empty

## Cost Tracking Strategy

Change orders maintain dual cost tracking to support budgeting and financial analysis:

### Estimate vs. Approved
- **cost_impact**: Initial estimate provided by requestor (may be "TBD")
- **approved_amount**: Final authorized amount from PM/owner (set only on approval)

### Running Totals
- **running_cost_total**: Sum of all approved_amount values from approved COs only
- **pending_cost**: Sum of cost_impact estimates for all draft, submitted, under_review COs
- Used in morning briefs, daily reports, and weekly summaries for visibility

### Cost Reports
- Total CO cost by originator (owner changes vs. architect vs. field requests)
- Approved vs. pending cost comparison
- Cost impact by affected spec section (helps identify problem areas)

## Schedule Tracking Strategy

Schedule impacts are tracked to maintain visibility on critical path:

### Daily Impact
- **schedule_impact_days**: Per-CO calendar day impact (positive or negative)
- Negative values if CO accelerates work (e.g., fast-track material procurement)

### Aggregation
- **running_schedule_total**: Sum of schedule_impact_days across all approved COs
- Used in project forecasting and completion date projections
- Surfaced in weekly reports with trending analysis

### Critical Path Management
- COs affecting critical path activities flagged in morning briefs
- Schedule impacts highlighted when total cumulative impact exceeds threshold (configurable, default: 10 days)

## CO Log Document Generation

The CO Log is a professional archival document suitable for owner distribution and project records:

### Document Format
- **Format**: Microsoft Word (.docx)
- **Filename**: `CO_Log_[YYYYMMDD].docx` (timestamp at generation)
- **Location**: `{{folder_mapping.change_orders}}/`

### Table Contents
Main table contains one row per CO with columns:

| Column | Content | Notes |
|--------|---------|-------|
| CO ID | CO-001, CO-002, etc. | Links to originating request |
| Description | Full CO description text | Truncated to 100 chars with ellipsis if needed |
| Originator | owner / architect / field / sub | Helps trace responsibility |
| Date Submitted | ISO format (YYYY-MM-DD) | Submission date |
| Status | Approved / Rejected / Void / Pending | Color-coded badges |
| Cost Impact | Approved amount if approved, "—" if pending/rejected | Formatted with $ and commas |
| Schedule Impact | Days (positive or negative) | N/A if zero |
| Approved By | Name/title of approver | Blank if not yet approved |

### Summary Section
Below the table, include executive summary:
- **Total COs**: Count by status (Approved | Pending | Rejected | Void)
- **Total Approved Cost**: Sum of approved amounts
- **Total Pending Cost**: Sum of estimates for under-review items
- **Total Schedule Impact**: Cumulative days (approved COs only)
- **Cost by Originator**: Breakdown showing which source is driving costs
- **High-Impact Items**: Any CO exceeding $50,000 or schedule impact > 5 days

### Design Standards
- Header with project name, project number, date generated
- Professional formatting with borders and shading
- Status badges with color coding:
  - Green: Approved
  - Yellow: Pending/Under Review
  - Red: Rejected
  - Gray: Void
- Page numbering and footer with "Confidential Project Document"

## Integration Points

### Morning Brief (`/morning-brief`)
Surfaces:
- Count of pending COs (submitted + under_review)
- List of COs requiring action today
- Total pending cost exposure
- Any COs exceeding cost/schedule thresholds
- Approvers with pending actions

### Daily Report (`/daily-report`)
Allows:
- Reference to specific COs in daily entry narratives
- Linking CO implementation progress to daily activities
- Notation of CO-related site meetings or clarifications
- Auto-suggestion of relevant COs based on daily scope description

### Weekly Report (`/weekly-report`)
Includes:
- CO summary section with week-over-week comparison
- New COs submitted during week
- COs approved during week with cost/schedule impact
- Pending COs aging analysis (submitted >5 days)
- Weekly cost impact trending
- Rolling 4-week total cost and schedule impact

### ASI Tracker (`/asis`)
- Auto-link COs when ASI references a change
- Surface related ASIs in CO record
- Track ASI-to-CO conversion (ASI initiates CO)

### RFI Tracker (`/rfis`)
- Auto-link COs when RFI resolves with scope change
- Surface related RFIs in CO record
- Track RFI impact on CO cost/schedule

## Configuration & Storage

### Storage Location
- **File**: `{{folder_mapping.config}}/change-order-log.json`
- **Section**: `change_order_log` array
- **Project Config Reference**: `{{folder_mapping.config}}/project-config.json` (for project_basics, folder_mapping, version_history)
- **Backup**: Each save creates timestamped backup in `{{folder_mapping.config}}/backups/`

### Version History
- All CO additions, status changes logged in `project-config.json` `version_history` array with:
  - Timestamp (ISO 8601)
  - Action type (CO-add, CO-status, CO-log-generated)
  - CO ID and status transition
  - User/actor (if tracked)

## Example Change Order Record

```json
{
  "id": "CO-005",
  "description": "Owner request: Add secondary electrical subpanel to south wing for future tenant TI. Includes conduit runs, breaker integration, and final connections.",
  "originator": "owner",
  "date_submitted": "2025-02-15T09:30:00Z",
  "status": "approved",
  "cost_impact": 18500,
  "approved_amount": 17800,
  "schedule_impact_days": 3,
  "affected_spec_sections": ["26", "26050"],
  "affected_subs": ["AAA Electric", "ABC Contracting"],
  "linked_asis": ["ASI-0008", "ASI-0009"],
  "linked_rfis": ["RFI-0012"],
  "running_cost_total": 65300,
  "running_schedule_total": 12,
  "approved_by": "Jennifer Smith, Project Manager",
  "resolution_date": "2025-02-17",
  "notes": "Approved with cost reduction from contractor value engineering. Schedule impact acceptable to critical path."
}
```

## Output Routing

All generated documents route to project folder structure:
- **CO Records**: Stored in `change-order-log.json` `change_order_log` array
- **CO Log Documents**: `{{folder_mapping.change_orders}}/CO_Log_[YYYYMMDD].docx`
- **Version History**: Logged in `project-config.json` `version_history` array
- **Backup Copies**: `{{folder_mapping.config}}/backups/change-order-log_[TIMESTAMP].json`

## Project Intelligence Integration

When project intelligence is loaded, auto-enrich change orders with schedule impact analysis, cost context, spec references, drawing references, and subcontractor identification.

### Schedule Impact Auto-Analysis
When a CO affects a specific work scope or activity:
- Read `schedule.json` → `critical_path[]` → check if any critical path activity matches the CO's affected scope
- If on critical path: auto-flag `schedule_impact` and estimate days based on the change scope
- Read `schedule.json` → `milestones[]` → check if the CO pushes any milestone at risk
- Example: CO affects structural steel erection → critical_path includes "PEMB Erection" → auto-flag "Critical path activity — schedule impact likely"

### Cost Impact Context
When creating or reviewing a CO:
- Read `cost-data.json` → pull `current_contract_value` and `contingency.available_contingency`
- Display CO cost as percentage of remaining contingency: "This CO ($17,800) represents 15.5% of remaining contingency ($115,000)"
- If CO would draw contingency below 50% threshold → flag "Contingency alert: approval would reduce contingency to 44%"

### Spec Section Linking
When a CO description mentions a work type or scope:
- Read `specs-quality.json` → `spec_sections[]` → auto-link CO to affected spec sections
- Include spec section numbers in `affected_spec_sections[]` for the cost proposal and documentation
- Example: CO for "additional electrical subpanel" → auto-link spec sections 26 00 00, 26 05 00

### Drawing Reference
When a CO affects a specific location or building system:
- Read `plans-spatial.json` → `sheet_cross_references.drawing_index[]` → find drawings related to the affected discipline and location
- Auto-populate affected drawing numbers for the CO record and cost proposal
- Example: CO at south wing electrical → reference sheets E-100, E-200, E-301

### Sub Identification
When a CO affects a trade scope:
- Read `directory.json` → `subcontractors[]` → match trade or scope to the CO's affected work
- Auto-identify the responsible sub and include their name in `affected_subs[]`
- Pull sub's contract scope for context on whether the CO is within or outside their original scope
- Example: CO for "additional excavation" → directory shows "Walker Construction" handles Excavation/Sitework → auto-populate affected_subs

## Error Handling & Validation

- **Missing config**: Inform user to run `/set-project` first
- **Invalid CO reference**: Suggest list of valid COs with status
- **Status transition not allowed**: Show valid next states for current status
- **Cost/schedule not quantified**: Allow "TBD" for estimate, require amount at approval
- **Circular dependencies**: Warn if CO references ASI/RFI that hasn't been created yet

## Audit & Compliance

- All CO records timestamped and immutable after approval
- Version history maintains complete audit trail
- Voided COs retained in records (never deleted)
- Original request details preserved even if status changes
- Approved amounts locked to prevent post-approval cost drift

## Time & Material (T&M) Tag Tracking

The T&M tag system captures real-time field work that may generate change orders. This is the field observation layer that feeds into CO creation and cost tracking.

### T&M Tag Data Model

```json
{
  "id": "TM-001",
  "date": "2026-02-18",
  "description": "Additional excavation for unforeseen rock at Grid C-3",
  "subcontractor": "ABC Excavation",
  "labor": [
    { "worker_count": 3, "hours": 6.5, "trade": "Operator", "rate": null }
  ],
  "materials": [
    { "item": "Hydraulic breaker rental", "quantity": 1, "unit": "day", "cost": null }
  ],
  "equipment": [
    { "item": "CAT 330 Excavator", "hours": 6.5, "rate": null }
  ],
  "superintendent_signature": false,
  "sub_signature": false,
  "photos": [],
  "linked_co": null,
  "status": "draft | field_signed | submitted_to_gc | incorporated_in_co | disputed",
  "notes": ""
}
```

**T&M Tag Fields:**
- `id`: Unique T&M identifier (TM-NNN format)
- `date`: Date work was performed (ISO 8601)
- `description`: Detailed narrative of work performed
- `subcontractor`: Responsible trade contractor
- `labor`: Array of labor entries (worker_count, hours, trade, rate)
- `materials`: Array of material entries (item, quantity, unit, cost)
- `equipment`: Array of equipment entries (item, hours, rate)
- `superintendent_signature`: Boolean; true when field superintendent approves
- `sub_signature`: Boolean; true when sub foreman approves (same day as superintendent)
- `photos`: Array of time-stamped photo URLs or file paths
- `linked_co`: CO ID if this T&M was incorporated into a change order (CO-NNN)
- `status`: Current T&M status (draft → field_signed → submitted_to_gc → incorporated_in_co or disputed)
- `notes`: Disputes, clarifications, or processing notes

### T&M Tracking Workflow

**Daily Field Observation → CO Request Cycle:**

1. **Field Observation**: Superintendent identifies unplanned work (rock excavation, rework, scope change)
2. **Create T&M Tag**: Open new T&M tag with description, subcontractor, location
3. **Document Work**: Log labor (hours + trades), materials (items + quantities), equipment (type + hours)
4. **Photo Documentation**: Time-stamped photos of work in progress, materials on site, equipment deployed
5. **Field Sign-Off (Same Day)**: Superintendent and sub foreman both sign off on quantities and costs
6. **Submit to GC/PM**: T&M submitted to general contractor or office within 48 hours for review
7. **Incorporate into CO**: When accepted, create CO (or add to pending CO) and link via `linked_co` field

### Processing Timeline

- **Best Practice**: Field sign-off by superintendent + sub foreman same day work is completed
- **Submission Window**: Submit T&M documentation to GC/PM within 48 hours of work completion
- **CO Creation**: Once T&M is accepted by PM, incorporate into change order within 1 week
- **Payment**: Process payment for incorporated T&M work as part of CO approval cycle

### Photo Documentation Requirements

T&M tags MUST include time-stamped photos documenting:
- Work in progress (showing scope and conditions)
- Materials on site (quantities, condition, delivery date if applicable)
- Equipment deployed (type, hours worked)
- Site conditions that justify the change (e.g., rock encountered, existing condition discrepancy)

Photo metadata (timestamp, location) is critical for dispute resolution and PM verification.

### Disputed T&M Handling

When quantities or costs are contested:

1. **Document Both Positions**: Record superintendent's observed quantities AND sub's claimed quantities
2. **Flag Status**: Set status to `disputed` with clear description of discrepancy
3. **Collect Supporting Evidence**: Additional photos, measurements, witness statements
4. **PM Review**: Project manager arbitrates based on documentation
5. **Resolution**: Accept agreed quantities, adjust costs, and update status (incorporated_in_co or disputed_resolved)

### T&M to Change Order Integration

**Linking T&M to COs:**
- T&M tag `linked_co` field references the CO ID that incorporated the work
- CO `linked_tm_tags` array references all T&M tags that contributed to the CO scope
- CO description should reference the T&M tag IDs: "Incorporates work documented in TM-001, TM-002"

**Cost Accumulation:**
- Multiple T&M tags can be incorporated into a single CO
- CO cost_impact = sum of all incorporated T&M labor + materials + equipment costs
- T&M status transitions to `incorporated_in_co` when CO is approved

### T&M Storage & Reporting

- **Storage Location**: `{{folder_mapping.config}}/tm-tags.json` with `tm_tags` array
- **Morning Brief**: Surface pending T&M tags (submitted but not yet incorporated) with totals
- **Daily Report**: Reference T&M work performed during the day
- **CO Log**: Include summary of incorporated T&M work with references to tag IDs
- **Metrics**: Track T&M velocity (tags per week), average incorporation lag, dispute rate
