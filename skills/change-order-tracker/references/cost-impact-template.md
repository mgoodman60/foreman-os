# Cost Impact Analysis Reference

This document defines the cost breakdown format, markup structure, time impact methodology, and cumulative tracking thresholds used by the change-order-tracker skill when pricing and analyzing change orders. Always verify markup percentages and contract terms before applying standard rates — many contracts specify exact figures that override industry norms.

---

## AIA G701 Change Order Form

The AIA G701 is the industry-standard executed change order form. It is the document both parties sign to make a CO contractually binding. The change-order-tracker data model maps directly to G701 fields so that a completed CO record can generate a G701-compliant output without re-entry.

### G701 Field Mapping

| G701 Field | Data Model Field | Notes |
|-----------|-----------------|-------|
| Project name | `project.name` | Full legal name on contract |
| Project number | `project.number` | Owner and/or GC number |
| Owner | `project.owner_name` | Legal entity name |
| Architect | `project.architect_name` | Design firm of record |
| Contractor | `project.gc_name` | GC or CM legal entity |
| Contract date | `project.contract_date` | Original execution date |
| Change order number | `co.number` | Sequential, format CO-XXXX |
| Date | `co.date` | Date CO is drafted |
| Description of change | `co.description` | Concise narrative |
| Amount of this change order | `co.amount` | Final agreed value (+ or −) |
| Contract sum prior to this CO | `co.previous_contract_sum` | Running total before this CO |
| Contract sum including this CO | `co.new_contract_sum` | Previous sum ± this CO |
| Contract time prior to this CO | `co.previous_days` | Substantial completion days |
| Net change by previously authorized COs | `co.prior_co_days_total` | Cumulative schedule adjustments |
| Contract time including this CO | `co.new_completion_date` | Revised substantial completion |
| Contractor signature | `co.contractor_signature` | Authorized rep name, title, date |
| Owner signature | `co.owner_signature` | Authorized rep name, title, date |
| Architect signature | `co.architect_signature` | When A/E is contract party |

Note: G701 does not include a line-item cost breakdown — that detail lives in the underlying PCO backup documents. The G701 states only the agreed lump sum total.

---

## Cost Breakdown Format

### Direct Costs

#### Labor

Bill labor at the burdened rate (base wage + payroll taxes + benefits + workers comp + liability insurance). Never bill bare wage rates on a CO — the contract almost certainly allows burdened rates.

| Trade / Classification | Hours | Burdened Rate | Total |
|-----------------------|-------|--------------|-------|
| Carpenter — Journeyman | 32 | $88.00/hr | $2,816.00 |
| Laborer | 16 | $64.00/hr | $1,024.00 |
| Foreman (working) | 8 | $102.00/hr | $816.00 |
| **Labor Subtotal** | | | **$4,656.00** |

Note: Superintendent time (non-working) is typically billed under Indirect Costs — Supervision, not as direct labor.

#### Material

Bill material at invoice cost. Attach supplier quotes or invoices as backup. Sales tax is included in material cost unless the project is tax-exempt.

| Item | Specification | Qty | Unit | Unit Cost | Total |
|------|--------------|-----|------|-----------|-------|
| Structural LVL 3.5x11.25x20 | Microlam or equal | 6 | EA | $312.00 | $1,872.00 |
| Joist hangers LUS410 | Simpson Strong-Tie | 12 | EA | $18.75 | $225.00 |
| Lag screws 1/2"x5" | HDG | 48 | EA | $1.85 | $88.80 |
| **Material Subtotal** | | | | | **$2,185.80** |

#### Equipment

Bill equipment at published rental rates or internal equipment rates per the contract. Always attach rental agreements or rate schedules.

| Equipment | Source | Hours / Days | Rate | Total |
|-----------|--------|-------------|------|-------|
| 19' scissor lift | Sunbelt Rentals | 3 days | $285.00/day | $855.00 |
| Boom truck (delivery) | Internal fleet | 2 hrs | $145.00/hr | $290.00 |
| **Equipment Subtotal** | | | | **$1,145.00** |

---

### Indirect Costs

Indirect costs are legitimate CO charges when the change extends duration or requires dedicated management resources. They are listed separately from direct costs and are subject to the same overhead and profit markup.

| Item | Basis | Amount |
|------|-------|--------|
| Supervision — Superintendent | 3 additional days x $850/day fully loaded | $2,550.00 |
| Temporary facilities — extended GCs | 3 days x allocated daily GC rate | Per project rate |
| Extended home office overhead | Apply Eichleay formula if schedule extended >30 days | Per claim analysis |
| Safety/layout — additional staking | 1 LS based on field estimate | $350.00 |

Note: Extended home office overhead (Eichleay) requires formal claim documentation and is typically reserved for significant duration extensions. Consult legal before applying.

---

### Markup Structure

Markup is applied to the total of direct costs + indirect costs. The order of application matters: overhead is calculated first, then profit is applied to direct + indirect + overhead, then bond is applied to the grand total.

| Component | Typical Range | Application Basis | Notes |
|-----------|--------------|------------------|-------|
| Overhead (OH) | 10 – 15% | Direct + indirect costs | Covers field and home office overhead allocation |
| Profit | 10 – 15% | Direct + indirect + OH | May be lower for large COs or negotiated projects |
| Bond premium | 1 – 2% | Total CO value (all above) | Only if project is bonded; verify bond rate with surety |
| Sub markup (if GC to sub) | 5 – 10% | Sub's CO value | GC administrative markup on sub-originated COs |

**Critical: Always check contract terms first.** Many AIA and ConsensusDocs contracts specify exact markup percentages in Article 7 or Supplementary Conditions. Common contract-specified structures:
- 15% combined OH+profit on labor and material
- 10% GC markup on subcontractor COs
- No markup on owner-furnished material

**Example Markup Calculation**

| Line | Amount |
|------|--------|
| Direct costs (labor + material + equipment) | $7,986.80 |
| Indirect costs (supervision + temp facilities) | $2,900.00 |
| Subtotal before markup | $10,886.80 |
| Overhead @ 12% | $1,306.42 |
| Profit @ 10% | $1,219.32 |
| Subtotal before bond | $13,412.54 |
| Bond premium @ 1.5% | $201.19 |
| **Total CO Value** | **$13,613.73** |

---

## Time Impact Analysis

### CPM Fragment Insertion Method (Fragnet)

When a CO adds scope that affects the schedule, a schedule fragment (fragnet) must be prepared and inserted into the project CPM to quantify the time impact. Verbal or estimated schedule claims are not sufficient for contract time extensions — a fragnet is the contractually defensible method.

**Step-by-Step Process**

1. Identify the activity or activities in the current CPM that are affected by the CO scope.
2. Create a fragnet: a mini-schedule containing only the new CO activities, with realistic durations and logic (FS, SS, FF ties as appropriate).
3. Connect the fragnet to the existing CPM with proper predecessor and successor logic ties.
4. Run the forward and backward pass with the fragnet inserted.
5. Compare the critical path completion date before insertion vs. after insertion.
6. The delta (difference in completion dates) is the compensable time impact of the CO.

**Before / After Example**

```
BEFORE fragnet insertion:
  A (5d) --> B (3d) --> C (7d) --> D (4d) --> FINISH: Day 19
             ^
         (critical path)

AFTER fragnet insertion (CO adds work between B and C):
  A (5d) --> B (3d) --> [CO-01a (4d) --> CO-01b (2d)] --> C (7d) --> D (4d) --> FINISH: Day 25

  Critical path now passes through CO activities.
  Delta = Day 25 - Day 19 = +6 calendar days time extension.
```

If the CO work runs concurrently with existing critical path activities and does not extend the longest path, the schedule impact is 0 days — even if the CO adds real work. Concurrent delay is not compensable for time extension purposes (though cost may still be).

**When a Fragnet is Not Required**

- CO adds cost only (material substitution, allowance adjustment) with no field installation time
- CO duration is fully absorbed within existing float on non-critical activities
- Owner explicitly waives schedule impact in CO agreement language

---

## Cumulative CO Tracking

### Running Total Dashboard

Track these values at all times. Update after each CO execution and after each PCO submission.

| Metric | Formula | Current Value |
|--------|---------|--------------|
| Original contract value | Base contract at award | $[base] |
| Executed COs — count | Count of COs in Executed status | [n] |
| Executed COs — value | Sum of all executed CO amounts | $[sum] |
| Current contract value | Original + executed CO value | $[current] |
| % variance from original | (Executed CO value / Original) x 100 | [x]% |
| Pending PCOs — count | Count of PCOs in Pricing / Submitted / Negotiating | [n] |
| Pending PCOs — value | Sum of PCO amounts not yet executed | $[sum] |
| Rejected COs — count | Count of COs or PCOs in Rejected status | [n] |
| Rejected COs — value | Sum of rejected amounts (exposure avoided or in dispute) | $[sum] |

### Variance Threshold Alerts

| Variance Level | % Range | Required Action |
|---------------|---------|----------------|
| Normal | 0 – 3% | Track and report in monthly owner report |
| Caution | 3 – 5% | Flag in weekly report; notify PM; verify contingency balance |
| Warning | 5 – 10% | Escalate to owner in writing; schedule OAC discussion; review CO trend causes |
| Critical | > 10% | Formal written owner notification; trigger contingency review; evaluate claim exposure |

Note: Some owner contracts set tighter thresholds (e.g., 2% triggers notification). Check the contract's allowable CO provisions before applying these defaults.

---

## Common CO Categories

Understanding CO source categories helps identify systemic problems (design deficiencies, poor site investigation) and supports claim analysis.

| Category | Description | Responsible Party | Typical Cost Range |
|----------|-------------|------------------|-------------------|
| Owner-directed changes | Owner elects to modify scope, finish level, or program | Owner pays | Varies widely |
| Design errors | Missing details, conflicting drawings, specification ambiguity | A/E; owner bears cost unless design-build | $500 – $50,000+ per occurrence |
| Design omissions | Scope required by code or function, not shown in documents | A/E; owner bears cost | $1,000 – $100,000+ |
| Differing site conditions (Type I) | Subsurface conditions differ materially from contract documents | Owner pays; GC must provide timely notice | $5,000 – $500,000+ |
| Differing site conditions (Type II) | Unknown physical condition of unusual nature | Owner pays with proper notice | $5,000 – $500,000+ |
| Code / regulatory changes | Authority having jurisdiction (AHJ) requires change after permit | Owner typically pays | $1,000 – $50,000 |
| Value engineering (credit) | GC proposes scope change that reduces cost; savings shared | Credit CO; GC retains agreed portion | (−$500) to (−$100,000) |
| Allowance adjustments | Actual cost of allowance item differs from allowance amount | True-up CO (add or deduct) | Per allowance line item |
| Acceleration directives | Owner directs GC to complete earlier than contract date | Owner pays premium labor costs | $10,000 – $500,000+ |
| Sub back-charge COs | GC remedied sub defect; seeks deduction from sub's contract | Sub responsible | $500 – $50,000 |

### Notice Requirements by Category

Most CO categories require timely written notice as a condition of entitlement. Failure to provide notice on time can result in waiver of the CO claim entirely.

| Category | Typical Notice Window | Notice To |
|----------|----------------------|-----------|
| Differing site conditions | Immediately upon discovery; before disturbing | Owner and A/E |
| Owner-directed extra work | Before proceeding (oral direction followed by written confirmation) | Owner |
| Design error / omission | Upon discovery; submit RFI before proceeding | A/E via RFI |
| Code / regulatory change | Upon receipt of AHJ directive | Owner and A/E |

Always cite the contract notice provision (typically AIA A201 §4.3 or equivalent) in the COR when providing notice.

---

## Abbreviations Quick Reference

| Abbreviation | Meaning |
|-------------|---------|
| AIA G701 | American Institute of Architects Change Order Form |
| CPM | Critical Path Method |
| DSC | Differing Site Condition |
| AHJ | Authority Having Jurisdiction |
| OAC | Owner / Architect / Contractor (meeting) |
| OH | Overhead |
| T&M | Time and Material |
| FS | Finish-to-Start (schedule logic) |
| SS | Start-to-Start (schedule logic) |
| FF | Finish-to-Finish (schedule logic) |
| SOV | Schedule of Values |
| PCO | Potential Change Order |
| COR | Change Order Request |
| CO | Change Order (executed) |
| VE | Value Engineering |
