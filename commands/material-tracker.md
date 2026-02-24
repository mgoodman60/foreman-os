---
description: Track materials, deliveries, and procurement status
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
argument-hint: [add|status|delivery|verify|find]
---

## Overview
Comprehensive material and procurement lifecycle management. Track materials from procurement through delivery, verification, and installation. Use this command to add materials, monitor status with color-coded indicators, log deliveries, and verify compliance with specifications.

**Skills Referenced:**
- `${CLAUDE_PLUGIN_ROOT}/skills/material-tracker/SKILL.md` - Material tracking methodology
- `${CLAUDE_PLUGIN_ROOT}/skills/submittal-intelligence/SKILL.md` - Specification verification (for verify action)

**Output Skills**: See the `xlsx` Cowork skill for procurement logs and delivery schedules in spreadsheet format.

## Execution Steps

Actions are determined by `$ARGUMENTS`. If no action specified, default to **status**.

---

## ACTION: add

Add a new material or procurement item to the project.

### Steps:
1. **Collect Item Information:**
   - Material/equipment description
   - Specification section (Division number, title)
   - Quantity required
   - Unit cost (estimated or actual)
   - Delivery address/location
   - Special handling requirements
   - Long-lead indicator (yes/no)
   - Preferred suppliers/sources

2. **Auto-Populate from Project Intelligence:**
   - Check `schedule.json` (long_lead_items) for matching materials
   - Check `specs-quality.json` (spec_sections) for material requirements and standards
   - Check existing `submittal-log.json` (submittal_log) for related product submittals
   - Check `project-config.json` (folder_mapping) for material storage locations
   - Auto-fill spec section references if found
   - Suggest related items (e.g., if adding door frames, suggest door hardware)

3. **Link to Submittal (if exists):**
   - If product has approved submittal, link to submittal ID
   - Pull product data (manufacturer, model, specs) from submittal
   - Reference approval date and any approval conditions

4. **Assign Procurement ID:**
   - Generate sequential PROC-XXX ID
   - Display to user
   - Record assignment date

5. **Save to Procurement Log:**
   - Add entry to `procurement-log.json`
   - Fields: ID, description, spec section, quantity, unit cost, total cost, delivery date, storage location, submittal link, status (Ordered/In Transit/Delivered/Verified), notes
   - Set initial status to "Pending Order" or "Ordered" based on user input

6. **Confirmation:**
   - Display: "PROC-XXX added successfully. [Material] - [quantity] units. Estimated delivery: [date]"
   - Suggest next action: "Run /material-tracker delivery to log receipt"

---

## ACTION: status

Display current material and procurement status dashboard.

### Steps:
1. **Load All Procurement Items:**
   - Read all entries from `procurement-log.json`
   - Load delivery dates, current status, notes

2. **Color-Coded Summary:**
   - **GREEN (On Track)**: Delivered items, items delivered before deadline, items without delivery deadline
   - **AMBER (Approaching)**: Items scheduled to arrive within 7 days, items ordered but not yet received, long-lead items at risk per `schedule.json`
   - **RED (Delayed/Overdue)**: Items with delivery date passed, items with noted delays, items with missing critical certifications, critical path impacts per `schedule.json`

3. **Display Summary Table:**
   ```
   Status | Count | Items
   ---|---|---
   On Track | X | [details]
   Approaching | X | [details]
   Delayed/Overdue | X | [details]
   ```

4. **Available Filter Views:**
   - **all**: All procurement items
   - **long-lead**: Items flagged as long-lead
   - **delayed**: Items with red status (overdue or at-risk)
   - **upcoming-deliveries**: Items scheduled within next 14 days
   - **missing-certs**: Items delivered but lacking certifications/testing

5. **Detailed Item Display:**
   For each item, show:
   - Procurement ID and description
   - Spec section and submittal link (if applicable)
   - Quantity and cost
   - Scheduled vs. actual delivery date
   - Storage location
   - Current status with last update date
   - Notes and blockers

6. **Action Buttons:**
   - **Log Delivery**: Quick link to delivery action
   - **Verify Specifications**: Quick link to verify action
   - **Update Status**: Change item status
   - **Request Expedite**: Flag for urgent delivery follow-up
   - **View Spec**: Link to relevant spec section

7. **Critical Path Alerts:**
   - Highlight any delayed items that impact the construction schedule
   - Suggest actions: "PROC-005 delayed by 3 days. Call supplier at [number]."
   - Recommend: "Run /prepare-rfi if material delay impacts schedule."

---

## ACTION: delivery

Log an incoming material delivery.

### Steps:
1. **Identify Material:**
   - Ask for PROC ID or material description
   - Look up in `procurement-log.json`
   - Confirm: "Logging delivery of [description]"

2. **Delivery Information:**
   - Delivery date (default: today)
   - Actual quantity received
   - Condition assessment:
     - **Good**: No damage, all items present
     - **Damaged**: Specific damage description
     - **Partial**: Quantity received vs. ordered
     - **Other**: Notes

3. **Cross-Check Against PO:**
   - Load PO data from `procurement-log.json`
   - Verify received quantity matches ordered
   - Alert if discrepancy: "Ordered 100 units, received 95. Confirm with supplier?"

4. **Verify Certifications/Documentation:**
   - Check for accompanying documentation (test reports, certs, mill certs, etc.)
   - Ask: "Include certifications? (yes/no)"
   - If yes: attach/reference files
   - Flag if missing expected certifications: "Mill certificate expected but not provided. Add to to-do?"

5. **Storage Location:**
   - Ask where material is being stored
   - Note: weather protection requirements, security, accessibility for installation
   - Store in procurement_log

6. **Update Procurement Log in `procurement-log.json`:**
   - Set status to "Delivered"
   - Record actual delivery date
   - Note condition, storage location, received quantity
   - Record certifications attached
   - Add any delivery notes (damage, delays, supplier issues)

7. **Trigger Next Steps:**
   - If condition = "Good" and certifications present: offer to run /material-tracker verify
   - If condition = "Damaged": suggest RFI for damaged goods
   - If partial: suggest follow-up call to supplier
   - Update look-ahead if material was blocking an activity

8. **Confirmation:**
   - Display: "PROC-XXX delivery logged. [Material] stored at [location]. Condition: [status]. Next: [suggested action]"

---

## ACTION: verify

Run specification verification on a delivered material.

### Steps:
1. **Identify Material:**
   - Ask for PROC ID or material description
   - Confirm: "Verifying [material]"

2. **Confirm Material is Delivered:**
   - Check `procurement-log.json` status
   - If status not "Delivered": ask "Material not yet delivered. Continue? (yes/no)"

3. **Load Product Specifications:**
   - From `procurement-log.json`, pull manufacturer and model data
   - From attached submittal (if linked), extract product specs
   - From certifications/documentation, extract performance data

4. **Load Spec Requirements:**
   - Determine spec section from `procurement-log.json`
   - Load requirements from `specs-quality.json` spec_sections
   - Load criteria: material quality, performance standards, certifications required, testing required

5. **Run Compliance Check (using submittal-intelligence methodology):**
   - Build compliance matrix:
     ```
     Spec Requirement | Standard/Spec | Provided Data | Compliance | Notes
     ---|---|---|---|---
     [Requirement] | [Spec] | [Product data] | Pass/Fail | [Detail]
     ```
   - Determine for each requirement:
     - **Pass**: Provided data meets or exceeds requirement
     - **Fail**: Does not meet requirement
     - **Conditional**: Meets with conditions or further testing
     - **Unable to Verify**: Insufficient data provided

6. **Check Certifications:**
   - Verify expected certifications are present:
     - Mill certificates (for metals)
     - Testing reports (for performance-critical items)
     - Code compliance documentation (for building materials)
     - Manufacturer certifications (for equipment)
   - Flag any missing critical certifications

7. **Determine Acceptance:**
   - **Approved**: All requirements met, all certifications present, material acceptable for installation
   - **Conditional Approval**: Meets requirements with notes, acceptable pending follow-up testing or installation verification
   - **Rejected**: Critical non-compliance, material unsuitable, recommend return/replacement
   - **Unable to Determine**: Insufficient data to approve; request additional documentation

8. **Generate Verification Report:**
   - Create structured record with:
     - Compliance matrix
     - Certification checklist (present/missing)
     - Overall determination
     - Deficiencies (if any) and corrective actions
     - Date verified

9. **Update Procurement Log in `procurement-log.json`:**
   - Set verification_status: Approved / Conditional / Rejected
   - Record verification date and reviewer
   - Store compliance matrix
   - Note any deficiencies or follow-up required

10. **Present to User:**
    - Display compliance matrix
    - Show certification status
    - State overall determination (Approved/Conditional/Rejected)
    - If Approved: "Material ready for installation. [Activity] can proceed."
    - If Conditional: "Pending [specific follow-up], then ready for installation."
    - If Rejected: "Material does not meet specifications. Recommend: [action]"

11. **Next Steps:**
    - If Approved: update look-ahead if this material was blocking work
    - If Conditional: create task for follow-up testing or verification
    - If Rejected: suggest RFI or change order for approved substitute
    - Link to installation schedule once approved

---

## ACTION: find

Search for vendors and suppliers for project materials. Routes to the material-tracker skill's "Source / Find Vendor" action (Action E).

### Steps:
1. **Parse Input:**
   - Check for material name, spec section, or general category after "find"
   - Examples: `/material-tracker find door frames`, `/material-tracker find 08 1000`
   - If no material specified, ask: "What material or spec section are you looking for vendors for?"

2. **Execute Vendor Search:**
   - Read and follow the material-tracker skill (`${CLAUDE_PLUGIN_ROOT}/skills/material-tracker/SKILL.md`), specifically Action E: Source / Find Vendor
   - Search existing vendor_database in `directory.json` (vendor_database) first
   - If spec section provided, extract material requirements from `specs-quality.json` (spec_sections)
   - Display existing vendor matches with contact info, capabilities, and project history

3. **Offer Web Search:**
   - If insufficient vendors found in database: "Search the web for additional vendors? (yes/no)"
   - If yes, run targeted web searches for suppliers

4. **Save Results:**
   - Add selected vendor(s) to vendor_database in `directory.json`
   - Link to procurement item if one exists for this material
   - Suggest: "Run /material-tracker add to create a procurement item for this material"

---

## Default Behavior
If `$ARGUMENTS` is empty or unrecognized, execute **status** action and display the material dashboard.

## Save & Log
1. Write updated `procurement-log.json`
2. Update `project-config.json` version_history:
   ```
   [TIMESTAMP] | material-tracker | [action] | [PROC-NNN or "status reviewed"]
   ```
3. If project data changed significantly, regenerate `CLAUDE.md` to reflect the latest project state
