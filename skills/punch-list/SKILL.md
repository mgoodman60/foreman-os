---
name: punch-list
description: >
  Track punch list items from identification through completion. Handles item creation, status updates, photo documentation, back-charge tracking, and report generation. Groups by area or trade for efficient closeout. Integrates with project dashboard (completion % by area and trade). Triggers: "punch list", "punch item", "punchlist", "add punch", "punch status", "generate punch list", "closeout", "deficiency", "back charge", "back-charge".
version: 1.0.0
---

# Punch List Skill

## Overview
Comprehensive punch list management system for construction projects. Tracks identification and resolution of deficiencies from initial walk-through through final closeout. Supports photo documentation, back-charge management, and professional reporting for inspections and regulatory compliance.

## Punch Item Schema

### Core Fields
- **id** (string): Unique identifier, format "PUNCH-{NNN}" (e.g., "PUNCH-001", "PUNCH-042")
  - Auto-generated on creation, incremental within project
  - Never reused, immutable
  - Enables clear reference in conversations and reports

### Location Fields (One or more required)
- **room_number** (string): Room or space identifier (e.g., "Room 107", "306B", "ICU-2")
  - Used for healthcare: patient rooms, operating rooms, medication dispensary
  - Standard for office/commercial: office numbers, conference rooms
- **building_area** (string): Larger zone reference (e.g., "East Wing", "3rd Floor", "North Corridor")
  - Supports multi-floor, multi-wing projects
  - Hierarchical: "Building A > East Wing > 3rd Floor"
- **grid_reference** (string): Coordinate system, optional (e.g., "Grid C3", "Section 4B")
  - Used in large-scale or modular projects
- **floor_level** (integer): Floor number or level (e.g., 3, -1 for basement)
  - Supports vertical organization; assists in access planning

### Identification & Documentation
- **description** (string, required): Clear, specific deficiency description
  - Example: "Drywall mud pops in northeast corner, joint at ceiling"
  - Example: "Paint scuff on south wall, 5 ft from floor"
  - Example: "Nurse call button missing in Room 214"
  - Should include location detail within space and visible severity
- **trade** (string, required): Responsible trade/discipline
  - Examples: "Drywall", "Painting", "Electrical", "Plumbing", "HVAC", "Doors & Hardware", "Flooring", "Medical Equipment", "IT/Communications"
  - Used to group items and assign to responsible subs
- **responsible_sub** (string, required): Sub contractor name or entity
  - Resolved against {workspace}/subs/ directory
  - Example: "ABC Drywall Inc.", "Ready Paint Services", "Smith Plumbing"
- **date_identified** (date): Date item was discovered
  - Auto-populated on creation (today's date)
  - Supports historical tracking and aging analysis
- **identified_by** (string): Name of person who identified the item
  - Usually superintendent or foreman
  - Accountability and follow-up contact

### Status & Workflow
- **status** (enum): Current state of item
  - **open**: Newly identified, awaiting assignment
  - **in_progress**: Sub notified and work initiated
  - **completed**: Work finished, may be pending inspection
  - **back_charge**: Assigned back-charge (sub failed to correct)
  - **disputed**: Item contested by sub or stakeholder; requires resolution meeting
- **date_completed** (date, optional): When work was finished
  - Populated on transition to "completed"
  - Blank until completion
- **completed_by** (string, optional): Name of person who verified completion
  - Usually superintendent or inspector
  - Supports audit trail

### Priority Classification
- **priority** (enum): Urgency and impact level
  - **A (Critical)**: Safety violation or code non-compliance
    - Must be corrected before occupancy
    - Examples: Missing handrails, electrical safety hazards, ADA accessibility failures, infection control violations
    - Blocks final sign-off
  - **B (Functional)**: Affects proper use or function
    - Should be corrected before final inspection
    - Examples: Non-functioning door, HVAC controls not working, plumbing leaks, paint color mismatch affecting space function
    - May delay closeout
  - **C (Cosmetic)**: Appearance only, no safety/function impact
    - Minor touch-ups acceptable during or after occupancy
    - Examples: Small paint scuff, minor drywall finish, cosmetic grout gaps
    - Does not block closeout if agreed with owner

### Photos & Documentation
- **photos** (array of objects): Visual documentation
  - Each photo object contains:
    - **filename** (string): File path or reference (e.g., "/data/photos/PUNCH-001-1.jpg")
    - **description** (string): What the photo shows (e.g., "Overview of mud pops in NE corner")
    - **date_taken** (date): When photo was captured
  - Supports multiple photos per item
  - Embedded in .docx reports (with file size limits)
  - Clarity: well-lit, straight-on, includes reference object for scale

### Back-Charge Tracking
- **back_charge_amount** (decimal, optional): Dollar amount to charge to sub
  - Only populated if status = "back_charge"
  - Example: 250.00 (for corrective work cost)
  - Supports billing and dispute resolution
- **back_charge_sub** (string, optional): Sub entity assigned back-charge
  - Populated when status = "back_charge"
  - May differ from responsible_sub if sub contracted work to another party
- **back_charge_reason** (string, optional): Why back-charge was issued
  - Example: "Sub failed to correct deficiency within agreed timeframe"
  - Example: "GC performed corrective work due to sub non-response"

### Notes & Communication
- **notes** (string, optional): Running log of updates, decisions, disputes
  - Example: "First notice 1/15. Re-notified 1/22. Completed 1/25. Inspector approved."
  - Example: "Sub claims material supplier error. Requested photos from supplier."
  - Example: "Owner approved temporary closeout pending final correction in Phase 2."
  - Supports audit trail and communication history

## Status Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    NORMAL FLOW                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  open ──→ in_progress ──→ completed                      │
│   ↓                           ↓                           │
│   └────→ back_charge ────────→┘ (with back-charge amount)│
│                                                           │
│  Any state ──→ disputed (requires resolution)            │
│                  ↓                                        │
│             (return to open/in_progress after resolve)   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Transitions
1. **open → in_progress**: Sub acknowledged and beginning work (via status update)
2. **in_progress → completed**: Work finished, verified by superintendent (date_completed, completed_by set)
3. **open/in_progress → back_charge**: Sub failed to correct; back-charge issued (amount and reason required)
4. **back_charge → completed**: GC corrected work or sub completed after back-charge warning
5. **Any state → disputed**: Item contested (reason required; typically returns to prior state after resolution)

## Completion Statistics Calculations

### By Location
- **Room/Area Completion %** = (completed items in location / total items in location) × 100
- Supports dashboard display: "Room 107: 4/5 items done (80%)"

### By Trade
- **Trade Completion %** = (completed items by trade / total items by trade) × 100
- Supports dashboard display: "Drywall: 12/15 items done (80%)"

### By Priority
- **Priority A Completion %** = (completed A items / total A items) × 100 [**must = 100% for final sign-off**]
- **Priority B Completion %** = (completed B items / total B items) × 100
- **Priority C Completion %** = (completed C items / total C items) × 100 [**may be <100% if owner accepts**]

### Overall Project
- **Overall Completion %** = (total completed items / total punch items) × 100
- **Open Count** = items with status = "open"
- **In Progress Count** = items with status = "in_progress"
- **Back-Charge Count** = items with status = "back_charge"
- **Disputed Count** = items with status = "disputed"

## Bulk Operations

### Bulk Add
User input: *"I found 5 items in Room 107: mud pops, paint scuff, missing outlet, cracked tile, missing grout."*

Process:
1. Extract location: "Room 107"
2. Parse items: Create array of 5 items
3. Prompt for common fields once: Trade (prompt per item or once for all?)
   - If same trade: ask "All drywall?" → apply to all
   - If mixed: ask per item or accept trade in bulk input
4. Auto-assign responsible_sub: resolve from project subs directory
5. Auto-generate IDs: PUNCH-001 through PUNCH-005
6. Set all: date_identified = today, identified_by = current user, status = "open", priority = ?
7. Save to punch list

### Bulk Status Update
User input: *"All drywall items in Room 107 are done. Mark them completed."*

Process:
1. Query punch list: filter by room_number="Room 107" AND trade="Drywall"
2. Display matching items for confirmation
3. Update all: status = "completed", date_completed = today, completed_by = user
4. Save and log bulk update in version_history

## Report Generation

### .docx Format Options

#### Header Section
- Project name and address
- Report date and time generated
- Report type: "Punch List by Area" or "Punch List by Trade"
- Superintendent name and signature line

#### Completion Statistics Section
- **Overall Project**: X% complete, N items remaining, breakdown by status
- **By Area/Location** (if grouped by area):
  ```
  Room 107:        80% (4/5 items) | A: 1/1 | B: 2/2 | C: 1/2
  Conference Room: 100% (3/3)      | A: 0/0 | B: 2/2 | C: 1/1
  ```
- **By Trade** (if grouped by trade):
  ```
  Drywall:         75% (9/12)  | A: 2/2 | B: 5/6 | C: 2/4
  Painting:        90% (9/10)  | A: 0/0 | B: 3/3 | C: 6/7
  ```
- **By Priority**:
  ```
  Priority A (Safety/Code):       100% (8/8) - READY FOR FINAL
  Priority B (Functional):         85% (17/20)
  Priority C (Cosmetic):           70% (14/20) - Optional for closeout
  ```

#### Items by Area (if option selected)
For each location (Room 107, Room 108, etc.):
- **Section Header**: Room/Area name, floor level, grid reference if applicable
- **Items Table**:
  | ID       | Description                | Trade      | Sub            | Status      | Priority | Days Open |
  |----------|----------------------------|------------|----------------|------------|----------|-----------|
  | PUNCH-001| Drywall mud pops NE corner | Drywall    | ABC Drywall    | completed  | B        | 8 days    |
  | PUNCH-002| Paint scuff south wall     | Painting   | Ready Paint    | in_progress| C        | 6 days    |
- **Photos**: Thumbnail or full-size embedded below each item (if available)
- **Notes**: Any back-charge or dispute info, completion dates

#### Items by Trade (if option selected)
For each responsible sub (ABC Drywall, Ready Paint, etc.):
- **Section Header**: Sub name, contact info (if in subs directory), total items assigned
- **Items Table**: Same as above, but sorted by location within trade
- **Summary**: X/Y items completed, back-charge info

#### Back-Charge Summary Section (if back-charges exist)
- **Total Back-Charge Amount**: $XXXX.XX
- **Items Flagged**:
  | ID        | Location   | Description        | Sub             | Amount  | Reason                 |
  |-----------|------------|-------------------|-----------------|---------|------------------------|
  | PUNCH-008 | Room 112   | Electrical hazard  | Smith Electric  | 500.00  | Non-compliance, GC fix |
  | PUNCH-015 | Room 201   | HVAC not functional| ABC Mechanical  | 350.00  | Sub non-response       |

#### Footer
- Project info and contact
- Report generated by: [superintendent name]
- Date/time: [timestamp]
- Page numbers and total pages
- Confidentiality notice if applicable

### Healthcare/Senior Care Special Handling
- **ADA Items**: Flag all Priority A items related to accessibility
  - Examples: Grab bars, accessible routes, door widths, bathroom clearances
  - Separate section: "ADA Compliance Items — 100% Completion Required"
- **Infection Control**: Flag items affecting sanitation
  - Examples: Shower/tub sealing, hand washing stations, sharps containers, supply storage
  - Separate section: "Infection Control Items"
- **Nurse Call System**: Track all nurse call button installations and functionality
  - Separate tracking: "Nurse Call Items — Room-by-Room"
  - Report completion status per room

## Integration Points

### Project Dashboard (`/project-dashboard`)
- **Punch Completion Widget**: Overall % complete, trending over time
- **By Area Chart**: Bar chart showing % complete per room/area
- **By Trade Chart**: Bar chart showing % complete per sub discipline
- **Priority Status**: Count of open A/B/C items
- **Days Open Trending**: Aging analysis; items open >14 days highlighted
- **Back-Charge Summary**: Total amount, count of flagged items

### Daily Report (`/daily-report`)
- **Punch Walk Findings** section: Can reference new items identified during day
  - Example: "Punch walk identified 3 new items in Room 107 (see punch list PUNCH-041, PUNCH-042, PUNCH-043)"
- **Completion Status**: Reference punch completion % for area worked that day
- **Back-Charge Updates**: Log any back-charges issued or resolved

### Closeout Workflow
- **Pre-Final Punch List**: All items listed and assigned; Priority A completion required
- **Final Punch List**: All Priority A done, Priority B >90% complete; Priority C completion optional if owner approved
- **Block Conditions**:
  - Disputed items halt final sign-off
  - Priority A items must = 100%
  - All back-charges must be resolved or owner must accept liability

## Rules & Constraints

1. **No Item Deletion**: Punch items are immutable history; status changes only (set to "completed" or "back_charge")
2. **Priority Cannot Decrease**: Cannot downgrade A → B or B → C once set (can only escalate: C → B → A if severity discovered)
3. **Back-Charge Amount Required**: If status = "back_charge", back_charge_amount must be >0 and back_charge_reason must be provided
4. **Completion Metadata**: Transition to "completed" requires date_completed and completed_by fields populated
5. **Location Required**: Every item must have at least room_number OR building_area defined
6. **Responsible Sub Required**: Every item must reference a valid sub from subs directory
7. **Priority A = 100% for Final**: Project cannot reach final sign-off without all Priority A items completed
8. **Disputes Block Closeout**: Status = "disputed" requires resolution before completion

## Project Intelligence Auto-Population

When project intelligence is loaded, auto-populate punch item fields from the data store to reduce manual entry and improve accuracy.

### Location Auto-Resolution
When the user provides a room number or casual location:
- Read `plans-spatial.json` → `room_schedule` → match `room_number`
- Auto-fill: `building_area` from room's building area, `floor_level` from room's floor level, `grid_reference` from the building area's grid range
- Example: User says "Room 107" → auto-fill building_area="East Wing", floor_level="Level 1", grid_reference="E-G / 3-5"

### Subcontractor Auto-Resolution
When the user names a responsible sub (by name, trade, or casual reference):
- Read `directory.json` → `subcontractors[]` → match by name (partial match) or trade
- Auto-fill: `responsible_sub` with full company name, resolve trade if not provided
- Pull foreman name and phone for the sub notification workflow
- Example: User says "Walker" → resolve to "Walker Construction", trade="Excavation/Sitework", foreman="Mike Johnson"

### Spec Cross-Reference
When a punch item's trade is identified:
- Read `specs-quality.json` → `spec_sections[]` → find sections matching the trade's CSI division
- Include relevant spec section number and acceptance criteria in the punch item notes for context
- Example: trade="Concrete" → pull Section 03 30 00 tolerances and finish requirements

### Drawing Reference
When a punch item location is resolved to a grid/area:
- Read `plans-spatial.json` → `sheet_cross_references.drawing_index[]` → find relevant sheets for that location and discipline
- Include sheet numbers in the punch report for easy plan reference
- Example: Location at Grid E-5, trade="Electrical" → reference sheets E-100, E-101

### Schedule Impact Check
When Priority A items exist:
- Read `schedule.json` → `milestones[]` → check if `final_completion` or `substantial_completion` milestone is at risk
- If open Priority A count > 0 and closeout milestone is within 30 days → flag schedule risk in punch summary
- Include remaining Priority A items in `/morning-brief` when closeout is approaching

## Triggers & Activation Phrases
- "punch list"
- "punch item"
- "punchlist"
- "add punch"
- "punch status"
- "generate punch list"
- "closeout"
- "deficiency"
- "back charge" / "back-charge"
- "punch walk"
- "punch report"

## Version History
- **v1.0.0** (2026-02-17): Initial release. Core CRUD, status workflow, report generation, healthcare specialization.
