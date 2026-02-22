---
name: drawing-control
description: >
  Manage drawing revisions, ASI incorporation, superseded sheet flagging, and current-set verification.
  Ensures the field always works from the latest approved drawings. Tracks distribution, validates
  references in daily reports and RFIs, and alerts on obsolete sheet usage. Triggers: "revision",
  "ASI", "current sheet", "superseded", "drawing log", "drawing distribution", "obsolete drawing",
  "sheet update", "field set", "current set", "drawing status", "new revision", "void drawing",
  "latest drawing", "which revision", "update the drawings", "drawing register".
version: 1.0.0
---

# Drawing Control Skill — Foreman OS

## Overview

The **drawing-control** skill is the central nervous system for managing construction drawings in Foreman OS. It tracks every revision, incorporates Architect/Engineer directives (ASIs), flags superseded sheets, and ensures the field works from the current set. Drawing management directly impacts quality, safety, cost, and schedule — this skill prevents costly rework by controlling the flow of information from the A/E to the field.

### Core Responsibilities

- **Revision Tracking**: Maintain complete drawing log with revision history, dates, and change descriptions
- **ASI Processing**: Automatically update affected sheets when directives are received; flag superseded revisions
- **Current Set Verification**: Generate discipline-based reports of the latest drawing revision for every sheet
- **Field Audit**: Compare physical field sets against digital log; alert on out-of-date usage
- **Distribution Control**: Track which team members received which revision and when
- **Change Summary**: Extract revision cloud data and summarize deltas between revisions
- **Integration Pipeline**: Feed current drawing data to RFI prep, daily reports, submittals, and look-ahead planning

---

## 1. Drawing Log Data Model

The drawing-control skill stores all drawing metadata in a JSON schema. This provides a single source of truth for the project's drawing package.

### JSON Schema

```json
{
  "project_id": "string (e.g., MOSC-825021)",
  "project_name": "string",
  "drawing_log_version": "1.0.0",
  "last_updated": "ISO 8601 timestamp",
  "updated_by": "string (user name)",
  "drawings": [
    {
      "drawing_id": "string (unique, e.g., A-101-001)",
      "sheet_number": "string (e.g., A-101)",
      "title": "string",
      "discipline": "string (Arch | Struct | Civil | Mech | Elec | Plumb | Fire | General)",
      "current_revision": "string (e.g., Rev 2)",
      "revision_date": "ISO 8601 date",
      "revision_history": [
        {
          "revision": "string (e.g., Rev 0, Rev 1, Rev 2)",
          "date": "ISO 8601 date",
          "received_from": "string (e.g., Smith Architects, LLC)",
          "description": "string (change summary)",
          "asi_number": "string or null (e.g., ASI-001)",
          "revision_clouds": {
            "summary": "string (brief description of changed areas)",
            "grid_locations": ["string (e.g., Grid 3/B-C, Zone North)"],
            "change_type": "string (minor | moderate | major)"
          }
        }
      ],
      "date_received": "ISO 8601 date",
      "date_distributed": "ISO 8601 date",
      "distribution_list": [
        {
          "recipient": "string (person or firm name)",
          "role": "string (Super | PM | Foreman | Sub | Vendor | Other)",
          "date_sent": "ISO 8601 date",
          "method": "string (email | printed | file_share | in_person)",
          "confirmed_receipt": "boolean",
          "receipt_date": "ISO 8601 date or null"
        }
      ],
      "superseded_revisions": [
        {
          "revision": "string",
          "marked_void_date": "ISO 8601 date",
          "reason": "string (e.g., ASI-001 superseded, newer revision issued)"
        }
      ],
      "status": "string (current | superseded | void | archived)",
      "file_reference": "string (path to drawing file, e.g., '/drawings/A-101-Rev2.pdf')",
      "file_size_mb": "number",
      "total_sheets": "number (if multi-sheet drawing)",
      "notes": "string (any additional context)",
      "linked_submittals": ["string (submittal numbers referencing this drawing)"],
      "linked_rfi": ["string (RFI numbers referencing this drawing)"]
    }
  ],
  "summary": {
    "total_drawings": "number",
    "total_sheets": "number",
    "disciplines": {
      "Arch": "number",
      "Struct": "number",
      "Civil": "number",
      "Mech": "number",
      "Elec": "number",
      "Plumb": "number",
      "Fire": "number",
      "General": "number"
    },
    "revisions_in_circulation": "number",
    "void_sheets": "number"
  }
}
```

---

## 2. ASI Processing Workflow

When the Architect or Engineer issues a Supplemental Instruction (ASI), the drawing-control skill manages the intake, revision updates, and distribution.

### ASI Receipt & Processing Steps

1. **Receive ASI** → Capture ASI number, date received, engineer/architect name
2. **Identify Affected Sheets** → Parse ASI document to extract sheet numbers impacted
3. **Update Revision Numbers** → Increment revision (Rev 0 → Rev 1, etc.) for each affected sheet
4. **Mark Superseded** → Flag previous revisions as superseded with ASI reference
5. **Extract Change Summary** → If revision clouds are present, summarize deltas
6. **Cross-Reference ASI Log** → Update project-config.json ASI table with drawing link
7. **Generate Distribution Notice** → List which sheets changed and who needs new copies
8. **Queue Automatic Re-distribution** → Trigger notifications to field team

### ASI Tracking Table Template

```markdown
| ASI # | Date Received | Issued By | Sheets Affected | Description | Status | Distribution Complete | Notes |
|-------|---------------|-----------|-----------------|-------------|--------|------------------------|-------|
| ASI-001 | 2026-01-15 | Smith Architects | A-101, A-102, A-103 | Floor plan revisions for door swing conflicts | Distributed | 2026-01-16 | All field copies updated |
| ASI-002 | 2026-02-05 | Yeiser Structural | S-201, S-202 | Anchor bolt layout modifications | Distributed | 2026-02-06 | Confirmed with steel sub |
| ASI-003 | 2026-02-18 | Davis HVAC | M-101, M-102 | Equipment substitution | Pending | - | Awaiting drawings from vendor |
```

### ASI-to-Revision Mapping

When an ASI requires drawing revisions, the mapping below ensures consistency:

```json
{
  "asi_number": "ASI-001",
  "date_received": "2026-01-15",
  "drawings_affected": [
    {
      "sheet_number": "A-101",
      "previous_revision": "Rev 0",
      "new_revision": "Rev 1",
      "description": "Door swing and furniture layout corrections"
    },
    {
      "sheet_number": "A-102",
      "previous_revision": "Rev 0",
      "new_revision": "Rev 1",
      "description": "Door swing and furniture layout corrections"
    }
  ],
  "distribution_initiated": "2026-01-16",
  "distribution_complete": true
}
```

---

## 3. Current Set Verification

The drawing-control skill generates on-demand reports showing the latest revision of every sheet in the project.

### Current Set Report (By Discipline)

**Command**: `/drawings status`

Sample output:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                    CURRENT DRAWING SET — 2026-02-19                        ║
╚════════════════════════════════════════════════════════════════════════════╝

ARCHITECTURAL (7 sheets)
  A-101  Floor Plan                          Rev 1  2026-01-15  Distributed ✓
  A-102  Reflected Ceiling Plan              Rev 0  2025-12-10  Distributed ✓
  A-103  Door & Hardware Schedule            Rev 1  2026-01-15  Distributed ✓
  A-201  Exterior Elevations - North/South   Rev 0  2025-12-10  Distributed ✓
  A-202  Exterior Elevations - East/West     Rev 0  2025-12-10  Distributed ✓
  A-301  Sections & Details (1 of 2)         Rev 0  2025-12-10  Distributed ✓
  A-302  Sections & Details (2 of 2)         Rev 0  2025-12-10  Distributed ✓

STRUCTURAL (6 sheets)
  S-001  Foundation Plan & Details           Rev 0  2025-12-10  Distributed ✓
  S-101  Framing Plan - Level 1              Rev 0  2025-12-10  Distributed ✓
  S-201  Anchor Bolt Schedule                Rev 1  2026-02-06  Distributed ✓
  S-202  Connection Details                  Rev 1  2026-02-06  Distributed ✓
  S-301  Roof Framing Plan                   Rev 0  2025-12-10  Distributed ✓
  S-302  Roof Details                        Rev 0  2025-12-10  Distributed ✓

CIVIL (5 sheets)
  C-001  Site Plan & Utilities               Rev 0  2026-01-20  Distributed ✓
  C-101  Grading & Drainage Plan             Rev 0  2026-01-20  Distributed ✓
  C-102  Utility Plans - Water/Sewer         Rev 0  2026-01-20  Distributed ✓
  C-201  Stormwater & Detention              Rev 0  2026-01-20  Distributed ✓
  C-301  Landscape & Hardscape               Rev 0  2026-01-20  Distributed ✓

MECHANICAL (4 sheets)
  M-001  HVAC System Diagram                 Rev 0  2025-12-10  Distributed ✓
  M-101  HVAC Plans - Level 1                Rev 0  2025-12-10  Distributed ✓
  M-102  Equipment Schedule & Details        Rev 0  2025-12-10  Distributed ✓
  M-103  Ductwork Details                    Rev 0  2025-12-10  Distributed ✓

PLUMBING (3 sheets)
  P-001  Plumbing System Diagram             Rev 0  2025-12-10  Distributed ✓
  P-101  Plumbing Plans - Level 1            Rev 0  2025-12-10  Distributed ✓
  P-102  Fixture Schedule & Details          Rev 0  2025-12-10  Distributed ✓

ELECTRICAL (4 sheets)
  E-001  Power & Lighting Diagram            Rev 0  2025-12-10  Distributed ✓
  E-101  Power Plans - Level 1               Rev 0  2025-12-10  Distributed ✓
  E-102  Lighting Plans - Level 1            Rev 0  2025-12-10  Distributed ✓
  E-103  Panel Schedules & Details           Rev 0  2025-12-10  Distributed ✓

FIRE PROTECTION (2 sheets)
  FP-001 Fire Alarm & Detection Plan         Rev 0  2025-12-10  Distributed ✓
  FP-102 Fire Protection Details             Rev 0  2025-12-10  Distributed ✓

GENERAL (1 sheet)
  G-001  Title Sheet & General Notes         Rev 0  2025-12-10  Distributed ✓

SUMMARY
  Total Drawings:        32 sheets
  Revisions:            Rev 0: 26 sheets | Rev 1: 6 sheets
  Distribution:        100% complete
  Void/Superseded:     0 sheets
  Last Update:         2026-02-06 (ASI-002 revisions)
```

### Field Set Audit

**Command**: `/drawings audit`

This command compares field documentation (daily reports, RFI submittals, payment apps) against the current drawing log and alerts on any references to superseded revisions.

```
Field Set Audit Results — 2026-02-19

✓ Scan completed: 7 daily reports, 3 RFIs, 2 submittals analyzed
⚠ 1 ISSUE FOUND:

  Daily Report (2026-02-18) references S-202 Rev 0
  ALERT: Current revision is S-202 Rev 1 (issued 2026-02-06 per ASI-002)
  Action: Notify crew to use latest revision from trailer/SharePoint
  Issued to: Walker Construction
```

---

## 4. Revision Cloud Summary

When new drawing revisions are received, the drawing-control skill extracts and summarizes revision cloud data (if available in PDFs).

### Revision Delta Extraction

```json
{
  "drawing_id": "A-101-001",
  "sheet_number": "A-101",
  "comparison": {
    "from_revision": "Rev 0",
    "to_revision": "Rev 1",
    "change_date": "2026-01-15",
    "change_summary": "Door swing corrections in Patient Rooms A-101, A-102. Furniture layout adjusted to ADA path of travel. Casework dimensions verified per Stidham quote.",
    "revision_clouds": [
      {
        "location": "Grid 3/B-C (Patient Room 101)",
        "description": "Door swing corrected from inward to outward swing; casework depth reduced 6 inches",
        "change_type": "major"
      },
      {
        "location": "Grid 4/C-D (Patient Room 102)",
        "description": "Door swing reversed; ADA clearance verified",
        "change_type": "moderate"
      },
      {
        "location": "Grid 2/A-B (Corridor)",
        "description": "Furniture layout clarification; no dimension changes",
        "change_type": "minor"
      }
    ],
    "affected_systems": ["Doors", "Casework", "Layout"],
    "impact_assessment": "Affects EKD (drywall/framing) and Stidham (casework) scope. Review with subs before framing."
  }
}
```

---

## 5. Drawing Distribution Log

The drawing-control skill tracks who received which revision and when, providing accountability and re-distribution triggers.

### Distribution Log Entry

```json
{
  "sheet_number": "A-101",
  "revision": "Rev 1",
  "distribution_round": 1,
  "date_distributed": "2026-01-16",
  "distribution_list": [
    {
      "recipient": "W Principles (Super - Miles Goodman)",
      "role": "Super",
      "method": "email",
      "date_sent": "2026-01-16",
      "email": "miles.goodman@wprinciples.com",
      "confirmed_receipt": true,
      "receipt_date": "2026-01-16"
    },
    {
      "recipient": "Andrew Eberle (PM)",
      "role": "PM",
      "method": "email",
      "date_sent": "2026-01-16",
      "email": "andrew.eberle@wprinciples.com",
      "confirmed_receipt": true,
      "receipt_date": "2026-01-16"
    },
    {
      "recipient": "EKD (Drywall/CFS Sub - Foreman)",
      "role": "Sub",
      "method": "email",
      "date_sent": "2026-01-16",
      "email": "foreman@ekd-drywall.com",
      "confirmed_receipt": false,
      "receipt_date": null
    },
    {
      "recipient": "Stidham Cabinets (Casework Sub)",
      "role": "Sub",
      "method": "email",
      "date_sent": "2026-01-16",
      "email": "office@stidhamcabinets.com",
      "confirmed_receipt": true,
      "receipt_date": "2026-01-17"
    }
  ],
  "re_distribution_required": false,
  "notes": "ASI-001 revision; follow-up call made to EKD on 2026-01-17 to confirm receipt."
}
```

### Automatic Re-distribution Triggers

The skill automatically initiates re-distribution when:
- New revision issued for a sheet already in circulation
- ASI affects multiple sheets in one directive
- Field reports reference superseded revision
- Submittal review flagged a drawing as outdated

---


---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
