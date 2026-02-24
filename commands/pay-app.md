---
description: Manage pay applications (G702/G703)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [prepare|status|sov|waivers]
---

# Pay Application Management Command

## Overview

Track and manage pay applications (AIA G702/G703 format) through the complete billing cycle. This command enables construction superintendents and project managers to:
- **Create** new pay application periods with automatic schedule of values (SOV)
- **Monitor** billing status, retainage, and payment collections
- **Generate** professional G702/G703 document packages ready for submission to the owner

Auto-populates project data from subcontractor directory, integrates change orders to track revised contract amounts, manages retainage calculations, and tracks lien waiver collection status.

## Skills Referenced
- `${CLAUDE_PLUGIN_ROOT}/skills/pay-application/SKILL.md` — Core pay application lifecycle, SOV management, percentage complete calculations, retainage logic, G702/G703 formatting
- `${CLAUDE_PLUGIN_ROOT}/skills/project-data/SKILL.md` — Project configuration, subcontractor directory, change order tracking
- `${CLAUDE_PLUGIN_ROOT}/skills/document-intelligence/SKILL.md` — G702/G703 document generation and formatting

**Output Skills**: See the `docx` Cowork skill for .docx generation best practices. See the `xlsx` Cowork skill for G702/G703 spreadsheet formatting and structure.

## Execution Steps

### Step 1: Load Project Configuration
Load `project-config.json` for version_history and folder_mapping.
Load `pay-app-log.json` for existing pay applications.
Load `directory.json` for subcontractor list and contact information.
Load `change-order-log.json` for approved change orders affecting contract amounts.
Load `specs-quality.json` for budget and CSI division structure.
Load `daily-report-data.json` for field observations and % complete data.
Load `schedule.json` for schedule % complete validation.

If the config file is not found, inform the user:
> "Project configuration not found. Please run `/set-project` first to initialize your project structure."

### Step 2: Parse Arguments for Sub-Action
Examine `$ARGUMENTS` to determine which operation:
- **"prepare"** — Prepare a new pay application for a billing period
- **"status"** — Display current pay app status and collections
- **"sov"** — Create or update the Schedule of Values
- **"waivers"** — Track lien waiver collection from subs and suppliers

If no sub-action provided, show usage:
```
Usage: /pay-app [prepare|status|sov|waivers] [details]
Examples:
  /pay-app prepare
  /pay-app status
  /pay-app sov
  /pay-app waivers
```

### Step 3: Process "prepare" Sub-Action

**Purpose**: Generate a comprehensive pay application for a billing period. W Principles bills monthly with Net 30 payment terms.

**Collect Pay Application Details:**
1. **Period Number**: What period is this? (e.g., "1", "2", "3")
2. **Period Start Date**: When does this billing period begin? (e.g., "2026-02-01")
3. **Period End Date**: When does this billing period end? (e.g., "2026-02-28")
4. **Application Date**: What is the certification/application date? (defaults to today)

**Validate SOV Exists:**
- Check if SOV already created in pay-app-log.json
- If not, prompt user: "No Schedule of Values found. Run `/pay-app sov` first to create SOV."
- If yes, load SOV structure and proceed

**Auto-Populate Percentage Complete:**
- **Primary Source**: Query daily-report-data.json for field observations during this period
  - For each SOV line item, look for corresponding work entries
  - Aggregate quantities installed and materials noted
  - Calculate cumulative % complete since project start
- **Secondary Source**: Query schedule.json for schedule % complete for same period
  - Compare to field observation % complete
  - Flag if discrepancy > 10%: "Schedule shows 35% complete but field shows 28%. Review?"
- **Tertiary Source**: Allow superintendent manual override with justification

**Calculate for Each Line Item:**
- work_completed_previous: [from prior pay apps, cumulative]
- work_completed_this_period: [new work this period only from daily reports]
- materials_stored: [delivered but not yet installed, from procurement-log.json]
- total_completed: work_completed_previous + work_completed_this_period + materials_stored
- percent_complete: [total_completed / revised_contract_amount * 100]
- retainage_rate: [0.10 flat throughout the project per W Principles standard, 0.00 at substantial completion]
- retainage_amount: [total_completed * retainage_rate]
- net_due: [total_completed - retainage_amount]

**Auto-Assign Pay App Number**: Query pay-app-log.json for highest PAY-NNN, increment by 1. Lock immediately.

**Cross-Reference Change Orders:**
- Check change-order-log.json for all approved COs (status: "approved")
- Update revised_contract_amount for each line item: original + sum(applicable approved COs)
- Recalculate percent complete based on revised amount

**Store in `pay-app-log.json`** with complete structure:
```json
{
  "id": "PAY-001",
  "period_number": 1,
  "period_start_date": "2026-02-01",
  "period_end_date": "2026-02-28",
  "application_date": "2026-03-01",
  "status": "draft",
  "schedule_of_values": [
    {
      "line_item_id": "SOV-001",
      "description": "Sitework & Excavation",
      "csi_division": "02",
      "original_contract_value": 220000,
      "change_orders_applied": [],
      "revised_contract_amount": 220000,
      "work_completed_previous": 0,
      "work_completed_this_period": 85000,
      "materials_stored": 0,
      "total_work_completed": 85000,
      "percent_complete": 38.64,
      "retainage_rate": 0.10,
      "retainage_note": "W Principles standard: 10% flat until substantial completion",
      "retainage_amount": 8500,
      "net_due": 76500
    }
  ],
  "original_contract_amount": 2770000,
  "change_orders_approved_to_date": [],
  "revised_contract_amount": 2770000,
  "total_work_completed_to_date": 150000,
  "total_materials_stored": 16000,
  "total_billable": 166000,
  "percent_complete_project": 5.99,
  "retainage_rate_active": 0.10,
  "retainage_work_completed": 15000,
  "retainage_materials_stored": 1600,
  "total_retainage": 16600,
  "amount_due_this_period": 149400,
  "previous_payments": 0,
  "cumulative_billing": 166000,
  "balance_to_finish": 2604000,
  "lien_waivers_required": {
    "conditional_progress": ["Walker", "W Principles", "Stidham", "Hek Glass", "EKD", "Alexander", "Davis & Plomin"],
    "status_summary": "7 required, 0 received"
  },
  "sub_pay_apps": [],
  "created_date": "2026-03-01",
  "submitted_date": null,
  "paid_date": null,
  "paid_amount": null,
  "notes": ""
}
```

**Output to User:**
- Display summary: "PAY-001 prepared. Period 02/01–02/28. Total billable: $166,000. Retainage (10%): $16,600. Amount due: $149,400. Status: Draft. 7 lien waivers required."
- Suggest next steps: "Run `/pay-app waivers` to track lien waiver collection or `/pay-app generate` to create G702/G703 documents."

### Step 4: Process "status" Sub-Action

**Purpose**: Display current billing status, payment collections, and lien waiver tracking.

**Display Summary Dashboard:**
1. **Color-Coded Status Indicators:**
   - **GREEN**: All pay apps submitted, paid, and lien waivers in order; project on track
   - **AMBER**: Pay apps pending, awaiting lien waivers, or payment pending from owner; attention needed in 1–2 weeks
   - **RED**: Pay app overdue, lien waivers significantly overdue (>7 days), payment delayed >30 days; immediate action required

2. **Billing Summary (All Pay Apps):**
   - Total Contract Amount: [$X]
   - Total Billed to Date: [$Y]
   - Percent of Contract Billed: [Y/X%]
   - Total Retainage Currently Held: [$Z]
   - Balance Remaining (unbilled): [$X - Y]
   - Total Retainage to Be Released (at substantial completion): [$cumulative retainage held]

3. **Pay Application History Table:**
   For each pay app in pay-app-log.json, display:
   - Pay App Number and Period (e.g., "PAY-001 (02/01–02/28)")
   - Status (draft | submitted | pending payment | paid)
   - Amount Billed This Period
   - Retainage Applied
   - Net Amount Due This Period
   - Lien Waiver Status (e.g., "7 required, 0 received")
   - Payment Status (date paid, if applicable; or "pending X days")

4. **Payment Performance Metrics:**
   - Average days from submission to payment (trend across prior pay apps)
   - Any payments significantly delayed (>30 days from submission)
   - Flag if owner or architect payment processing is slower than expected

5. **Drill-Down Capabilities:**
   - User can select a pay app number (e.g., "show PAY-002") to see:
     - Detailed SOV line-by-line breakdown with % complete for each division/sub
     - List of approved change orders and their impact on contract amount
     - Complete lien waiver status by subcontractor (type, date received, document reference)
     - All historical payments with dates and amounts
   - Provide comparison to schedule: "Schedule is 35% complete, but billing is at 28%. Review progress?"

6. **Action Suggestions:**
   - If pay app is draft: "Run `/pay-app generate` to create G702/G703 submission package."
   - If lien waivers missing: "Run `/pay-app waivers` to track outstanding waivers."
   - If payment overdue: "Contact owner to confirm payment status. Consider escalation."

### Step 5: Process "sov" Sub-Action

**Purpose**: Create or update the Schedule of Values — the foundation for all pay applications.

**Check if SOV Already Exists:**
- Query pay-app-log.json for existing SOV
- If SOV exists: "SOV already created. Show current structure? (yes/no)"
  - If yes, display current SOV and prompt: "Modify SOV? (add item / remove item / edit item / rebalance totals)"
  - If no, proceed to status sub-action

**Create New SOV:**
1. **Select Organization Method:**
   - "Organize by CSI Division?" (yes/no)
   - If yes: use CSI 01–50 structure; group subs by division
   - If no: organize by Subcontractor name; list each sub as primary line item

2. **Auto-Suggest Line Items:**
   - Query specs-quality.json spec_sections for all divisions mentioned
   - Query directory.json for all active subcontractors
   - Query project-config.json budget for any pre-established contract structure
   - Compile list and present to user: "Found 12 potential SOV line items. Review and adjust?"

3. **Collect Line Item Details:**
   For each line item:
   - Description (CSI Division title or Subcontractor name + trade)
   - Contract Amount (from directory.json sub contract amounts or budget breakdown)
   - CSI Division (if organized by CSI)
   - Related Subcontractors (if organized by CSI)

4. **Validate Total Balance:**
   - Sum all SOV line items
   - Compare to total contract amount from specs-quality.json or project-config.json
   - If not equal, prompt: "SOV total $X, but contract is $Y. Adjust line items to balance?"
   - User can rebalance: increase/decrease individual line items proportionally or manually

5. **Lock and Store SOV:**
   - Mark SOV as locked: "SOV locked. Cannot be modified without approval."
   - Save to pay-app-log.json with timestamp
   - Generate unique SOV-001, SOV-002, etc. for each line item
   - Record that SOV applies to baseline contract; future change orders reference it but do not alter it

6. **Output to User:**
   - Display complete SOV table
   - Confirm total = contract amount
   - Suggest: "SOV created. Run `/pay-app prepare` to create first pay application."

**SOV Storage Format:**
```json
{
  "sov_version": 1,
  "sov_locked_date": "2026-03-01",
  "organization_method": "subcontractor",
  "line_items": [
    {
      "line_item_id": "SOV-001",
      "subcontractor_name": "Walker Land Company",
      "trade": "Sitework & Excavation",
      "description": "Site demolition, excavation, fill removal, grading",
      "csi_divisions": ["02"],
      "original_contract_value": 220000
    },
    {
      "line_item_id": "SOV-002",
      "subcontractor_name": "W Principles",
      "trade": "Concrete",
      "description": "Foundation, floor slab, exterior concrete work",
      "csi_divisions": ["03"],
      "original_contract_value": 185000
    }
  ],
  "total_scheduled_value": 2770000
}
```

### Step 6: Process "waivers" Sub-Action

**Purpose**: Track lien waiver collection from all subcontractors and suppliers.

**Display Waiver Tracking Dashboard:**
1. **Waiver Status Summary:**
   - For the current or pending pay application:
     - Total subs/suppliers that worked this period: [X]
     - Conditional progress waivers received: [Y]
     - Conditional progress waivers pending: [X - Y]
     - Unconditional waivers received (if final pay app): [count]

2. **Waiver Status by Subcontractor:**
   For each sub/vendor in directory.json with active contracts:
   - Sub Name
   - Trade / Scope
   - Waiver Type Required (conditional progress / unconditional final)
   - Through Date (date waiver covers)
   - Received? (Yes/No)
   - Date Received (if yes)
   - Document Reference (filename or path)
   - Amount Covered (scope or contract amount)
   - Status (required | requested | received | verified)

3. **Blocking Logic:**
   - If any conditional progress waivers pending: "Cannot process payment from owner until all conditional waivers received. [X] still pending."
   - If at final pay app and any unconditional final waivers missing: "Final payment cannot be processed. [X] unconditional final waivers still needed."

4. **Collection Actions:**
   - User can select "Request waiver from [Sub Name]" → generate email template
   - User can upload/attach received waiver → mark received with date
   - User can verify waiver (check format, through-date, signature) → mark verified

5. **Escalation Warnings:**
   - If waiver >7 days overdue: "W Principles conditional waiver 7 days overdue. Escalate?"
   - Suggest follow-up: "Call sub at [phone] to confirm waiver submission."

**Lien Waiver Tracking Structure:**
```json
{
  "pay_app_id": "PAY-001",
  "lien_waivers": {
    "conditional_progress": [
      {
        "subcontractor": "W Principles",
        "trade": "Concrete",
        "amount_covered": 45000,
        "period_start": "2026-02-01",
        "period_end": "2026-02-28",
        "status": "pending",
        "date_requested": "2026-03-01",
        "date_received": null,
        "document_reference": null
      }
    ],
    "unconditional_progress": [],
    "conditional_final": [],
    "unconditional_final": []
  },
  "waiver_summary": {
    "total_required": 7,
    "conditional_progress_required": 7,
    "conditional_progress_received": 0,
    "payment_blocked": true,
    "days_overdue": 0,
    "critical_blocking_subs": ["Walker", "W Principles", "Alexander"]
  }
}
```

### Step 7: Save & Log

1. **Write Updated Data Files:**
   - Write updated `pay-app-log.json` with complete pay app or SOV structure
   - Write updated `directory.json` if lien waiver status modified
   - Write updated `project-config.json` version_history with timestamp and action

2. **Version History Entry:**
   ```
   [ISO 8601 TIMESTAMP] | pay-app | [sub-action] | [details]
   Examples:
   2026-03-01T09:15:00Z | pay-app | prepare | PAY-001 (Period 02/01–02/28, $166,000 billable)
   2026-03-01T09:45:00Z | pay-app | sov | SOV created, 8 line items, locked
   2026-03-02T14:30:00Z | pay-app | waivers | Waiver request sent to W Principles
   ```

3. **Confirm Completion:**
   - Display summary of changes made
   - Show next recommended action based on sub-action

4. **Suggest Next Steps:**
   - For "prepare": "PAY-001 created in draft status. Next: `/pay-app waivers` to track collection, or `/pay-app generate` to create G702/G703 documents."
   - For "status": "Billing summary complete. Next: `/pay-app waivers` to request missing waivers, or `/pay-app prepare` to create next pay app."
   - For "sov": "SOV locked and saved. Next: `/pay-app prepare` to begin first pay application."
   - For "waivers": "Waiver tracking updated. Next: `/pay-app status` to view payment readiness, or follow up on specific subs."

5. If project data changed significantly, regenerate `CLAUDE.md` to reflect the latest project state

## Integration Points

- **Morning Brief** (`/morning-brief`):
  - Flags any overdue payments (>30 days from submission)
  - Surfaces lien waivers required for pending pay apps
  - Highlights blocking issues: "Cannot submit PAY-001 — 3 lien waivers pending"

- **Daily Report** (`/daily-report`):
  - Captures % complete observations by trade/division
  - These observations feed into pay-app prepare calculations
  - Can note any work delays impacting billing

- **Weekly Report** (`/weekly-report`):
  - Comprehensive financial summary: "This week: $50,000 billed, $5,000 retainage applied. YTD: $166,000 billed, $16,600 retainage held."
  - Cash flow impact: projected payment from owner
  - Retainage analysis: amount held, expected release dates

- **Change Order System** (`/change-order`):
  - When CO reaches "approved" status, next `/pay-app prepare` automatically incorporates revised contract amount
  - G702/G703 documents show original contract, CO adjustments, and revised contract

- **Project Dashboard**:
  - Real-time % complete by division
  - Cumulative billing vs. budget curve
  - Retainage held vs. schedule progress

- **Subcontractor Directory** (`/directory`):
  - Links to individual sub contact info for lien waiver collection
  - Tracks sub payment history and final lien waiver status

## Key Business Rules

1. **Schedule of Values** is locked at first pay app; subsequent pay apps may show revised contract amounts due to COs, but SOV structure remains constant
2. **Retainage Calculation**:
   - Standard: 10% of work completed until project reaches 50% complete
   - At 50% and beyond: 5% retainage
   - Materials stored subject to same retainage rates
   - Retainage released at Substantial Completion (user-defined milestone)
3. **Percent Complete** cannot decrease; once work is marked complete, it stays complete
4. **Lien Waivers** required from all subcontractors:
   - Conditional Progress Waiver: Required prior to payment this period
   - Unconditional Progress Waiver: Conditional for final payment
   - Conditional Final Waiver: Required with final payment app
   - Unconditional Final Waiver: Absolute lien release (typically required for substantial completion)
5. **Sub Pay Apps** submitted to GC must aggregate into master pay app; GC certifies total accuracy

## Notes

- All pay app numbers are immutable once assigned
- SOV line items are locked at creation to maintain historical accuracy
- Change orders automatically update revised contract amounts but do not alter SOV structure
- Retainage calculation is automatic based on percent complete; user can override rates if contract specifies different percentages
- G702/G703 documents are read-only archives; modifications require creating a new pay application period
