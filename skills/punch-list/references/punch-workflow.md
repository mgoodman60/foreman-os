# Punch List Workflow Reference

## Overview

The punch list process is the systematic identification and resolution of construction deficiencies before final project closeout. A well-managed punch list protects the GC's reputation, ensures owner satisfaction, and is often a prerequisite for Certificate of Occupancy and final payment.

Effective punch list management requires clear communication with subcontractors, disciplined documentation, and consistent follow-through. The superintendent owns this process.

---

## End-to-End Workflow

### Phase 1: Pre-Punch Preparation

Before inviting the owner or architect to a formal punch walk, the GC conducts an internal self-inspection to identify and resolve obvious deficiencies.

- GC superintendent walks each area independently before formal walk
- Trade-specific QC checklists completed and signed by sub foremen
- All areas cleaned, lit, and accessible for inspection
- Temporary protection removed where final finish review is required
- Punch list template pre-loaded with room list and area breakdown
- Keys and access credentials confirmed for all spaces

### Phase 2: Identification (Walk-Through)

- **Participants**: Owner representative, Architect/EOR, GC Superintendent. Sub foremen may attend by area.
- **Method**: Room-by-room systematic inspection following a predetermined sweep order
- **Sweep Order**: Ceiling → Walls → Floor → MEP devices → Hardware → Finishes
- **Trade Grouping**: Identify and record the responsible trade for every item as it is noted
- **Documentation**: Each item receives a photo (close-up + wide shot), written description, and exact room/area location before moving on

Do not skip rooms or areas. If access is blocked, note it and schedule a return visit within 24 hours.

### Phase 3: Documentation & Assignment

- Each item is assigned a unique punch ID using format: `PUNCH-{NNN}` (e.g., `PUNCH-047`)
- Item record includes: ID, description, location, trade, photo links, priority, due date, and assigned sub
- Priority classification assigned at time of documentation (see Priority Classification below)
- Subcontractor notified via written notice (email or platform message) containing:
  - Itemized list of their assigned punch items
  - Photo documentation for each item
  - Priority and deadline for each item
  - Reference to subcontract punch list requirements

### Phase 4: Correction

- Subcontractor performs corrective work within the assigned deadline
- Sub notifies GC superintendent when each item is complete
- Sub provides photo documentation of correction (before/after)
- No GC verification is required before sub marks item as completed — verification is a separate step

### Phase 5: Verification

- Superintendent re-inspects each item marked completed by the sub
- Items that pass inspection are marked **verified** with date and inspector name
- Items that fail re-inspection are returned to **in_progress** status with written notes explaining what remains deficient
- Three failed re-inspections on a single item may trigger back-charge evaluation (see back-charge-procedures.md)

### Phase 6: Close-Out

- All items reach **closed** status
- Final punch list report generated showing 100% completion with verification dates
- Report signed by superintendent and included in the closeout package
- Closeout package delivered to owner per contract requirements

---

## Status Lifecycle

```
identified → assigned → in_progress → completed → verified → closed
                                           ↓
                                       disputed
```

| Status | Entry Criteria | Exit Criteria |
|--------|---------------|---------------|
| `identified` | Item observed and documented during walk | Assigned to responsible sub |
| `assigned` | Responsible sub determined, notice sent | Sub acknowledges and begins work |
| `in_progress` | Sub has accepted assignment | Sub marks item complete |
| `completed` | Sub self-reports item finished, photo submitted | GC verifies or returns for re-work |
| `verified` | GC superintendent confirms correction is acceptable | Admin close confirmed |
| `closed` | Item included in final completion report | Final — no further action |
| `disputed` | Sub contests responsibility or adequacy | Resolved through documentation review or contract mechanism |

---

## Priority Classification

| Priority | Definition | Target Resolution | Example Items |
|----------|-----------|-------------------|---------------|
| Critical | Blocks CO, occupancy, or life safety | 24–48 hours | Missing fire caulk, non-functional exit sign, unsecured electrical panel |
| Major | Visible deficiency or code compliance issue | 3–5 business days | Damaged door, wrong paint color, missing trim, non-functioning hardware |
| Minor | Cosmetic only, will not delay closeout | 7–14 business days | Small paint touch-up, hairline caulk gap, scuffed base trim |
| Deferred | Owner-accepted deficiency, to be addressed post-occupancy | Per written agreement | Seasonal landscaping, future-phase items, owner-caused changes |

Deferred items must be documented in a separate deferred items log signed by the owner. They do not count against punch list completion percentage.

---

## Walkthrough Protocol

Use this sequence consistently for every room or area during the formal inspection walk.

1. **Enter and orient** — Note room number, area name, and floor level. Confirm lighting is functional.
2. **Ceiling** — Scan for stains, cracks, incomplete drywall finish, missing ceiling tiles, incomplete paint, missing or mis-located devices (sprinkler heads, diffusers, light fixtures, speakers).
3. **Walls (clockwise)** — Paint coverage, sheen consistency, drywall quality, trim installation, outlet and switch plate alignment and installation, wall protection or corner guards.
4. **Floor** — Flooring material condition, transitions between materials, base trim installation and caulking, cleanliness.
5. **MEP Devices** — Light fixture operation, HVAC register installation and airflow, plumbing fixtures (function, finish, caulk), electrical devices tested.
6. **Hardware** — Door latch and lock function, closer adjustment, threshold installation, kick plates, signage.
7. **Accessibility** — ADA-required signage, clearances, hardware heights, and ramp slopes where applicable.
8. **Document and move on** — Confirm all items for this room are logged before proceeding to the next space.

---

## Reporting

- **Daily punch summary**: Items opened, items closed, items overdue — distributed each morning to sub foremen
- **Weekly punch report**: Overall completion percentage by trade and area, trend against closeout schedule
- **Final punch report**: Complete item-by-item log with photos, verifier, and close date — included in owner closeout package

Completion percentage is calculated as: `(closed items / total items) × 100`. Disputed items are excluded from the denominator until resolved.
