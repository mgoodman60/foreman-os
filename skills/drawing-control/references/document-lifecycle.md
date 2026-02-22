# Drawing Document Lifecycle Reference

## Overview
Every construction drawing follows a defined lifecycle from receipt through archival. The drawing-control skill manages this lifecycle to ensure the field always works from the latest approved documents, superseded drawings are clearly identified, and distribution is tracked and acknowledged.

## Document Lifecycle Stages

### Stage 1: Receipt
- Drawing package received from Architect/Engineer
- Source documented: firm name, transmittal number, date received, delivery method
- Package logged in drawing-control with receipt timestamp
- Initial quality check: Are all expected sheets present? Are files readable?

### Stage 2: Registration
- Each sheet registered in the drawing log with:
  - Sheet number, title, discipline
  - Revision number and date
  - File reference (path to digital copy)
- New drawings get a "new" flag; revised drawings get revision incremented
- Drawing log updated with complete revision history

### Stage 3: Review (Completeness Check)
- Verify all sheets match the transmittal list
- Check revision numbers against ASI or revision request
- Verify file quality (readable, correct scale, complete content)
- Flag any discrepancies with A/E for resolution

### Stage 4: Distribution
- Determine distribution list based on affected disciplines/trades
- Distribute via established method (email, SharePoint, printed, in-person)
- Record distribution: recipient, date sent, method
- Request acknowledgment for critical revisions (structural, life safety)
- Track acknowledgment receipt

### Stage 5: Supersession
- When a new revision arrives, all previous revisions are marked "superseded"
- Superseded drawings get:
  - Status changed to "superseded"
  - Void date recorded
  - Reason noted (ASI number, revision request, etc.)
- Field sets must be updated within 24 hours of new revision distribution
- Any RFI referencing a superseded sheet gets flagged for review

### Stage 6: Archival
- At project closeout, all drawings are archived as the final record set
- Archive includes: all revisions (not just latest), all ASIs, revision history
- Record set is part of the closeout package for the owner
- Archived drawings are read-only — no further modifications

## Transmittal Tracking

Every document package sent or received gets a transmittal record:

| Field | Description |
|-------|------------|
| Transmittal number | Sequential: TR-{YYYY}-{NNN} |
| Date | Date sent or received |
| Direction | Incoming (from A/E) or Outgoing (to field/subs) |
| Sender | Firm and person |
| Recipient(s) | List of recipients |
| Contents | List of drawings/documents with revision numbers |
| Purpose | For review, for construction, for record, as noted |
| Acknowledgment | Required Y/N, received date |

## Revision Supersession Rules

### Core Rules
1. When a new revision is received, ALL previous revisions of that sheet are marked "superseded"
2. Only one revision of each sheet can have status = "current" at any time
3. Superseded drawings are never deleted — they remain in the log for audit trail
4. Field sets (physical or digital) must be updated within 24 hours

### Flagging Rules
- Any RFI referencing a superseded sheet → Warning flag in rfi-preparer
- Any daily report referencing a superseded sheet → Warning flag in report-qa
- Any submittal referencing a superseded sheet → Warning flag in submittal-intelligence
- Any punch item referencing a superseded sheet → Warning in punch-list

### Field Set Update Protocol
1. Superintendent notified of new revision
2. Digital file updated in project file share
3. Physical field set updated (if maintained): old sheet marked "VOID" with date stamp
4. Affected subcontractors notified with new sheet
5. Confirmation collected from each affected sub

## Distribution Tracking

### Who Gets What
| Discipline | Primary Recipients | Secondary Recipients |
|------------|-------------------|---------------------|
| Architectural | GC Super, PM, affected subs | Owner (via transmittal) |
| Structural | GC Super, PM, steel/concrete subs | Structural inspector |
| MEP | GC Super, PM, MEP subs | Commissioning agent |
| Civil | GC Super, PM, site/utility subs | Civil inspector |
| Fire Protection | GC Super, PM, FP sub | Fire marshal |

### Acknowledgment Requirements
- Standard drawings: Email confirmation sufficient
- Critical revisions (structural changes, life safety): Written acknowledgment required
- ASI-driven changes: Acknowledgment with confirmation of scope understanding

## ISO 19650 Naming Conventions

For projects following international CDE (Common Data Environment) standards:

Format: `{Project}-{Originator}-{Volume}-{Level}-{Type}-{Role}-{Number}`

Example: `MOSC-SA-ZZ-L01-DR-A-0101`
- MOSC = Project code
- SA = Smith Architects (originator)
- ZZ = All volumes
- L01 = Level 1
- DR = Drawing
- A = Architectural
- 0101 = Sheet number

(Most US commercial projects use simpler conventions like A-101, S-201, etc.)

## Integration with Other Skills

| Skill | How Drawing Control Feeds It |
|-------|---------------------------|
| rfi-preparer | Current sheet numbers and revision status for RFI references |
| daily-report-format | Drawing references in work descriptions verified against current set |
| submittal-intelligence | Spec-to-drawing cross-references; submittal sheet references validated |
| document-intelligence | Drawing metadata for classification and extraction |
| punch-list | Drawing references on punch items verified against current set |
| meeting-minutes | Drawing revision status updates for OAC meeting agenda |
