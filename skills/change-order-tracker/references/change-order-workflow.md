# Change Order Workflow Reference

Change orders are formal modifications to the construction contract's scope of work, contract sum, or completion date. Every field-identified change must move through a structured approval chain before any work proceeds or costs are incurred. This document defines the lifecycle, authority matrix, documentation standards, and integration points for all change events.

---

## COR → PCO → CO Lifecycle

### Stage 1: COR (Change Order Request)

The COR is the field-initiated record. Any superintendent, foreman, or subcontractor who identifies changed conditions, owner-directed extra work, or a design discrepancy initiates a COR. No changed work should proceed without a logged COR.

**Required Contents**
- Brief description of the change condition or direction received
- Location reference (grid lines, floor, building area)
- Estimated cost impact (rough order of magnitude — do not commit to a number)
- Estimated schedule impact (days added or saved)
- Initiating event: owner direction, RFI response, differing site condition, A/E supplemental
- Supporting photos (required for differing site conditions and damage claims)
- Reference documents: drawing numbers, spec sections, RFI number, ASI number

**COR Status Gates**

| Status | Trigger | Owner |
|--------|---------|-------|
| Draft | Superintendent identifies the change | Superintendent |
| Submitted | COR logged and sent to PM | Superintendent |
| Under Review | PM evaluating for validity and pricing approach | PM |
| Closed — Proceed to PCO | PM confirms scope is compensable | PM |
| Closed — No Cost/Time | Change determined to be within base contract | PM |
| Closed — Back-Charge | Change caused by sub performance; deduction route | PM |

---

### Stage 2: PCO (Potential Change Order)

The PCO is the PM-level pricing and negotiation document. It converts the field-identified COR into a formal cost proposal submitted to the owner or GC. A single PCO may consolidate multiple CORs if the changes are related.

**Required Contents**
- Detailed cost breakdown (see Cost Impact Analysis Template below)
- Schedule analysis with CPM fragnet reference if time is claimed
- Backup documentation: sub quotes, material invoices, equipment rental agreements
- Reference to originating COR number(s)
- Markup calculation per contract terms (OH%, Profit%, Bond%)

**PCO Status Gates**

| Status | Trigger | Owner |
|--------|---------|-------|
| Pricing | Internal cost build-up in progress | PM / Estimator |
| Submitted | PCO sent to owner or GC for review | PM |
| Negotiating | Owner has responded with comments or counter | PM / Principal |
| Agreed | Cost and schedule terms accepted by both parties | PM |
| Rejected | Owner disputes compensability; may escalate to claim | PM / Legal |

---

### Stage 3: CO (Change Order)

The CO is the executed contract modification. No PCO-covered work should appear on a pay application until the CO is fully executed (both signatures obtained).

**Required Contents**
- Final agreed price (lump sum or unit price basis)
- Schedule adjustment in calendar days (positive = extension, negative = credit)
- Updated contract completion date
- Signature blocks: Contractor authorized rep + Owner authorized rep
- Reference to originating PCO number(s)

**CO Status Gates**

| Status | Trigger | Owner |
|--------|---------|-------|
| Drafted | Legal or PM prepares formal CO document | PM |
| Signed by Contractor | GC/CM authorized rep executes | PM / Principal |
| Signed by Owner | Owner rep executes | Owner |
| Executed | Both signatures obtained; CO is contractually binding | PM |
| Void | Agreement fell through; work direction rescinded | PM |

---

## Lifecycle Flow Diagram

```
FIELD EVENT
    |
    v
[COR — Draft]
    |
    | Superintendent submits
    v
[COR — Submitted]
    |
    | PM reviews validity
    |
    +---> [No Cost/Time] ---------> Closed (no CO)
    |
    +---> [Back-Charge] ----------> Back-Charge workflow
    |
    v
[PCO — Pricing]
    |
    | Internal cost build-up complete
    v
[PCO — Submitted to Owner]
    |
    | Owner review period
    |
    +---> [Negotiating] ----------> Counter / Revised PCO
    |         |
    |         | Terms agreed
    |         v
    +-------> [PCO — Agreed]
                  |
                  v
            [CO — Drafted]
                  |
                  v
            [CO — Signed by Contractor]
                  |
                  v
            [CO — Signed by Owner]
                  |
                  v
            [CO — EXECUTED]
                  |
                  v
         Added to Contract Value
         Added to Pay Application
```

---

## Approval Authority Matrix

Dollar thresholds below govern who can approve a CO for execution. Thresholds apply to the **total CO value**, not individual line items. When multiple COs are bundled, the bundle total governs.

| Authority Level | Dollar Threshold | Typical Role | Notes |
|----------------|-----------------|--------------|-------|
| Superintendent | Up to $5,000 | Field superintendent | T&M work authorization only; formal CO still required |
| Project Manager | $5,001 – $25,000 | PM | Must have budget line or contingency available |
| VP / Division Principal | $25,001 – $100,000 | VP of Operations | Requires PM recommendation memo |
| Owner Authorization | Any value over $100,000 | Owner rep / Board | Owner signature required regardless of GC authority |
| Owner Authorization | All COs (any value) | Owner rep | Owner must execute all COs — no exceptions |

Note: Many contracts require owner approval for all COs regardless of dollar value. Always check the General Conditions (typically AIA A201 §7.2) before proceeding.

---

## Cost Impact Analysis Template

Use this line-item format for all PCO cost proposals. Attach backup (quotes, invoices, time cards) for each line.

| Item | Description | Qty | Unit | Unit Cost | Total |
|------|-------------|-----|------|-----------|-------|
| L-1 | Labor — Carpenter (Journeyman) | 24 | hrs | $85.00/hr (burdened) | $2,040.00 |
| L-2 | Labor — Laborer | 8 | hrs | $62.00/hr (burdened) | $496.00 |
| M-1 | Lumber — 2x10x16 (LVL) | 40 | EA | $38.50/EA | $1,540.00 |
| M-2 | Hardware — joist hangers, fasteners | 1 | LS | $215.00 | $215.00 |
| E-1 | Equipment — scissor lift rental | 2 | days | $285.00/day | $570.00 |
| **Subtotal Direct Costs** | | | | | **$4,861.00** |
| OH | Overhead (12%) | | | | $583.32 |
| Profit | Profit (10%) | | | | $544.40 |
| Bond | Bond premium (1.5%) | | | | $89.83 |
| **Total CO Value** | | | | | **$6,078.55** |

**Supplemental Fields**

| Field | Entry |
|-------|-------|
| Schedule impact | +3 calendar days |
| Critical path affected? | Yes / No |
| CPM fragnet reference | Fragnet CO-0047 |
| Work classification | Extra work (owner-directed) |
| Justification narrative | Owner directed relocation of structural beam per email from [Name] dated [MM/DD/YYYY]. Original design at Grid B/7 conflicts with MEP chase added by A/E via ASI-12. |

---

## Back-Charge Integration

When a change event results from subcontractor non-performance, defective work, or damage caused by another trade, it may be processed as a back-charge rather than a conventional CO.

**When a Back-Charge Becomes a CO Deduction**

1. Document the deficiency on a punch list or non-conformance notice
2. Issue written notification to the responsible sub (specify cure period — typically 48–72 hours)
3. Sub fails to cure; GC self-performs or directs a second sub to remedy
4. GC accumulates T&M costs with time cards, material receipts, equipment logs
5. Costs are compiled into a formal back-charge notice
6. If sub disputes, the back-charge may become a CO deduction on the sub's next pay application

**Documentation Requirements for Back-Charges Becoming COs**

- Written cure notice with proof of delivery (email confirmation or certified mail)
- Photographic documentation of defect before and after remediation
- Signed time cards for all labor performing the remedy work
- Material receipts and equipment logs with timestamps
- Inspector confirmation (if remediation required re-inspection)

**Deduction vs. Separate CO**

| Approach | When to Use |
|----------|-------------|
| Pay application deduction | Sub agrees; no prime contract CO needed |
| CO deduction (owner contract) | Defect caused delay impacting prime contract completion date |
| Separate owner-directed CO | Owner bore cost and is billing GC (rare) |

---

## Standard CO Form Fields

All change orders must include these fields at minimum. Forms that omit required fields will be returned for correction before routing.

| Field | Notes |
|-------|-------|
| CO Number | Sequential; format CO-XXXX |
| Date | Date CO document is drafted |
| Project Name | Full project name as on contract |
| Project Number | Owner and/or GC project number |
| Contract Date | Original contract execution date |
| Description of Change | Concise narrative of scope modification |
| Cost Adjustment | Dollar amount: add (+) or deduct (−) |
| Updated Contract Sum | Previous contract sum ± this CO |
| Schedule Adjustment | Calendar days: add (+) or deduct (−) |
| Updated Completion Date | Revised substantial completion date |
| Spec Sections Affected | List all specification sections modified |
| Drawings Affected | List all drawing numbers modified or added |
| Originating COR/PCO Numbers | Reference chain back to field initiation |
| Originator | Name and title of person who initiated the COR |
| Contractor Signature Block | Name, title, date, signature |
| Owner Signature Block | Name, title, date, signature |

---

## Status Tracking Integration

CO status data feeds directly into these reporting streams. The change-order-tracker skill populates each output automatically based on the current status of all logged COs.

### Morning Brief
- Pending CORs requiring PM review (action item)
- PCOs in negotiation (status flag)
- COs awaiting owner signature (aging alert if >5 business days)

### Weekly Report
CO summary section includes:
- Total COs executed this week: count and dollar value
- Cumulative approved CO value vs. original contract (% variance)
- PCOs under negotiation: count and pending value
- CORs under review: count

### Project Dashboard
- Original contract value
- Total executed CO value (running total)
- Current contract value = Original + Executed COs
- Pending CO exposure (unexecuted PCOs)
- CO count by category (owner-directed, differing site, A/E error, value engineering)

### Pay Application
- Approved, executed COs are added to Schedule of Values before each pay app
- CO must be fully executed (both signatures) before inclusion — PCOs in negotiation are excluded
- CO line items appear separately from original SOV line items for audit clarity

---

## Abbreviations Quick Reference

| Abbreviation | Meaning |
|-------------|---------|
| COR | Change Order Request (field-initiated) |
| PCO | Potential Change Order (PM-level pricing) |
| CO | Change Order (executed contract modification) |
| T&M | Time and Material |
| OH | Overhead |
| SOV | Schedule of Values |
| CPM | Critical Path Method |
| ASI | Architect's Supplemental Instruction |
| RFI | Request for Information |
| GC | General Contractor |
| CM | Construction Manager |
| AIA | American Institute of Architects |
| DSC | Differing Site Condition |
