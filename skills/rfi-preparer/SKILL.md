---
name: rfi-preparer
description: >
  Draft RFIs and submittal transmittals with auto-filled project intelligence. Use when the user wants
  to "write an RFI", "draft an RFI", "prepare an RFI", "send an RFI", "create a transmittal",
  "prepare a submittal transmittal", "submittal cover sheet", or any mention of RFI or transmittal preparation.
version: 1.0.0
---

# RFI Preparer Skill

## Overview

The RFI Preparer skill automates the creation of Request For Information (RFI) forms and submittal transmittals using intelligent data from your project management database. Instead of manually filling out forms and hunting through drawings for sheet numbers, this skill:

- **Auto-populates** project team information, project details, and sequential numbering from your RFI and submittal logs
- **Resolves casual location descriptions** ("east side second floor") to specific grid lines, building areas, floor levels, and drawing sheet references
- **Auto-fills spec sections** based on work type and references from your active specifications
- **Generates professional RFI text** from casual descriptions provided by site personnel
- **Formats documents** ready for signature and distribution (HTML or PDF export)
- **Maintains numbering sequences** automatically from rfi_log and submittal_log

## Document Types

### A) Question RFI
A formal request for clarification or direction from the architect or engineer regarding:
- Conflicts or ambiguities in the contract documents
- Constructability concerns
- Design questions or field conditions
- Interpretation of drawings or specifications

**Typical flow**: Field personnel describe the issue casually → Skill auto-fills technical data → Professional RFI is drafted → Sent to appropriate design professional

### B) Submittal Transmittal
A cover sheet accompanying a submittal package (product data, shop drawings, samples, test reports) being sent for architect/engineer review and approval.

**Typical flow**: Superintendent identifies submittal → Skill auto-fills project/spec data → Transmittal form is generated → Package is sent with cover sheet

## Data Sources

The skill uses project intelligence from the following sources:

- **project_basics**: Project name, number, address; project team members (Superintendent, Architect, Engineer, General Contractor)
- **grid_lines**: Building grid system (column lines, spacing, labels)
- **building_areas**: Defined areas of the project (East Wing, West Wing, Main Lobby, etc.)
- **floor_levels**: Floor names and numbers (Level 1 = Ground Floor, Level 2, Level 3, etc.)
- **spec_sections**: Active specifications organized by CSI MasterFormat (Division and Section numbers)
- **schedule**: Project timeline, key dates, current phase
- **subcontractors**: Vendor/trade contact information
- **rfi_log**: Complete history of all RFIs issued (used to determine next sequential RFI number and status tracking)
- **submittal_log**: Complete history of all submittals (used for transmittal numbering and linking)
- **documents_loaded**: List of all loaded drawing sheets with their sheet numbers and descriptions
- **room_schedule**: Room-by-room breakdown with location, area, finishes (for room-specific references)

## RFI Workflow

1. **Determine next RFI number** from rfi_log (typically auto-increment: if last RFI was RFI-047, next is RFI-048)
2. **Ask the user** to describe the question, issue, or conflict in casual language (no jargon required)
3. **Auto-resolve location references** from casual description to structured grid/area/level data
4. **Auto-resolve drawing references** by matching building area and location to loaded plan sheets
5. **Auto-resolve spec section references** by matching work type to active spec sections
6. **Auto-fill project team** with superintendent as sender, architect or engineer as recipient (based on question topic)
7. **Draft professional RFI text** transforming the user's casual description into clear, specific technical language
8. **Present formatted RFI** for review and approval before sending
9. **Save to rfi_log** with "draft" status; user can mark as "issued" when ready
10. **Offer export as PDF** with professional formatting and signature fields

## Transmittal Workflow

1. **Determine next transmittal number** from submittal_log
2. **Ask the user** to identify what is being submitted (product, shop drawings, samples, etc.)
3. **Identify spec section** where the item belongs
4. **Auto-fill project/team details** from project_basics
5. **Auto-fill manufacturer/product info** if available in subcontractors or submittal_log
6. **Present formatted transmittal** for review
7. **Save to submittal_log** with status "submitted"
8. **Offer export as PDF** for distribution with the submittal package

## Output

- **Formatted HTML display** for on-screen review (shows all fields, ready-to-sign state)
- **PDF export** with professional styling, matching project brand palette, US Letter size, signature lines
- **Log entries** created in rfi_log or submittal_log with appropriate metadata
- **Email draft** ready to send to recipient (if email integration is available)

## Cross-References

- **project-data skill**: Source for all project intelligence (grid lines, building areas, floor levels, spec sections, team info, logs)
- **document-intelligence skill**: Advanced sheet reference matching and drawing metadata lookup
- **PDF styling conventions**: Navy #1B2A4A headers, Blue #2E5EAA section labels, Light Blue #EDF2F9 cell backgrounds (consistent across all Foreman OS document outputs)

## Professional Standards

All RFIs and transmittals follow construction industry best practices:
- Clear, specific language (no ambiguity)
- Explicit references to drawings and specifications (sheet numbers, division/section numbers)
- State the conflict or ambiguity clearly
- Suggest a resolution if possible (shows collaboration, speeds response)
- Appropriate urgency level (Routine/Urgent/Critical) with justification
- Required response date linked to schedule impact
- Professional tone and format matching industry standards

## Integration Notes

This skill requires:
- Access to project_basics, rfi_log, submittal_log, documents_loaded
- Grid line, building area, floor level, and spec section data populated in project intelligence
- Document list (documents_loaded) with accurate sheet numbers and descriptions
- Current project schedule for date calculations and response deadlines

If any required data is missing, the skill will prompt the user to provide it or use defaults.

---

## Project Intelligence Integration

When project intelligence is loaded, auto-populate RFI and transmittal fields from the data store instead of requiring manual entry.

### Location Resolution
Resolve casual location descriptions to structured references:
- Read `plans-spatial.json` → `building_areas[]` + `room_schedule[]` → match user's casual description (e.g., "east side second floor") to specific grid reference, floor level, and building area
- Read `plans-spatial.json` → `grid_lines[]` → resolve to column/row intersection for the RFI location field
- Example: "near the bathroom on the second floor" → Grid D-3, Level 2, East Wing, Room 204

### Drawing Reference Auto-Fill
Automatically identify affected drawing sheets:
- Read `plans-spatial.json` → `sheet_cross_references.drawing_index[]` → match the resolved location and work type to relevant drawing sheet numbers
- Auto-populate the "Affected Drawings" field with sheet numbers and descriptions
- Example: Grid D-3 plumbing issue → Sheets P-2.1 (Second Floor Plumbing Plan), A-2.1 (Second Floor Plan)

### Spec Section Auto-Fill
Match work type to specification references:
- Read `specs-quality.json` → `spec_sections[]` → match the RFI subject's trade/work type to the relevant CSI division and section number
- Auto-populate the "Specification Reference" field
- Example: Drywall question → Division 09, Section 09 29 00 (Gypsum Board)

### Team Distribution
Auto-fill routing and contact information:
- Read `directory.json` → `project_team[]` → auto-fill architect, engineer, and owner representative contacts for the RFI routing fields
- Read `directory.json` → `subcontractors[]` → identify the affected sub for CC distribution
- Example: Structural question → Route to SE (from project_team), CC to Alexander Construction (PEMB sub)

### Numbering Sequence
Maintain sequential numbering automatically:
- Read `rfi-log.json` → find max RFI `id` number → auto-assign next sequential ID (e.g., last RFI-047 → next is RFI-048)
- Read `submittal-log.json` → find max submittal `id` → auto-assign next transmittal number

### Related Item Cross-Reference
Surface related open items for context:
- Read `rfi-log.json` → filter by matching `location` or `subject` keywords → surface related open/pending RFIs
- Read `submittal-log.json` → filter by matching `spec_section` → surface related submittals and their approval status
- Read `procurement-log.json` → check if the RFI subject relates to any items with `delivery_status` = "delayed" → flag procurement impacts

