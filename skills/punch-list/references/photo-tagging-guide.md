# Punch List Photo Documentation Guide

## Overview

Photo documentation is not optional — it is the evidentiary backbone of the punch list process. Clear, well-organized photos protect the GC in disputes, provide unambiguous direction to subcontractors, and demonstrate due diligence in the closeout package.

---

## Photo Requirements

Every punch item requires a minimum of two photos:

1. **Close-up photo**: Shows the specific deficiency clearly. Camera should be 12–24 inches from the subject. Deficiency should fill at least 50% of the frame.
2. **Wide shot**: Shows context — the room, area, or wall where the deficiency is located. Room number or area signage should be visible in frame when possible.

Additional photos are required for:
- Complex deficiencies spanning multiple surfaces
- Items where the deficiency requires multiple angles to fully convey
- Items where the location is ambiguous from the close-up alone

---

## Photo Standards

| Requirement | Specification |
|-------------|--------------|
| Minimum resolution | 1920 x 1080 (Full HD) |
| Lighting | Adequate — use flash or supplemental light in dim areas |
| Focus | Sharp focus on the deficiency; blur is not acceptable |
| Obstructions | Clear sightline from camera to subject |
| Scale reference | Include tape measure, hand, or door frame when deficiency size is not self-evident |
| Timestamp | Device timestamp must be enabled; date/time embedded in EXIF data |

Never crop photos before uploading to the punch list record. Cropped originals cannot be verified. Annotated versions are acceptable as supplements, but unaltered originals must be stored.

---

## File Naming Convention

```
PUNCH-{NNN}_{area}_{trade}_{date}_{type}.jpg
```

| Token | Description | Example |
|-------|-------------|---------|
| `PUNCH-{NNN}` | Punch item ID, zero-padded to 3 digits | `PUNCH-007` |
| `{area}` | Room number or area code, no spaces | `Room-107`, `Corridor-B`, `Lobby` |
| `{trade}` | Responsible trade abbreviation | `paint`, `electrical`, `plumbing`, `flooring` |
| `{date}` | ISO 8601 date (YYYY-MM-DD) | `2026-02-21` |
| `{type}` | `before` or `after` for correction documentation | `before`, `after` |

**Examples:**
- `PUNCH-001_Room-107_paint_2026-02-21_before.jpg`
- `PUNCH-015_Corridor-B_electrical_2026-02-21_before.jpg`
- `PUNCH-042_Lobby_flooring_2026-02-22_before.jpg`
- `PUNCH-001_Room-107_paint_2026-02-24_after.jpg`

---

## Location Tagging

Each punch item record must include the following location fields in addition to the photo:

- **Floor/Level**: Building floor or level (e.g., Level 1, Basement, Roof)
- **Building area/zone**: Wing, phase, or zone designation if applicable
- **Room number**: Per architectural drawings when applicable
- **GPS coordinates**: Auto-captured when the mobile device supports it — do not disable
- **Cardinal direction**: Required for exterior items (e.g., North elevation, East wall at Grid Line 5)
- **Drawing reference**: Sheet number and grid coordinates for items verifiable against the contract documents

Location data is used to generate area-based punch list reports and to guide subcontractor crews to deficiency locations without requiring a GC escort.

---

## Annotation Requirements

Annotated photos aid subcontractors in identifying the exact deficiency, particularly for items where the defect is subtle.

- **Close-up photo**: Draw a circle or arrow pointing directly to the deficiency using red markup
- **Wide shot**: Ensure room number or area identifier is visible; add a text label if not
- **Color convention**: Red markup for deficiencies; green markup for completed corrections in after photos
- **Text annotations**: Brief only — 3 to 5 words maximum (e.g., "missing caulk bead", "paint holiday")
- **Tool**: Use the platform's built-in annotation tool or a consistent third-party markup app

Annotated versions supplement the original. Both versions must exist in the item record.

---

## Before/After Documentation

Correct before/after documentation is required for every item that proceeds to verification.

- The "after" photo must be taken from the same angle and approximate distance as the "before" photo
- Match lighting conditions when possible — if the before photo used flash, the after photo should as well
- Both photos are stored together within the punch item record, linked by the same punch ID
- The platform displays before/after photos side by side in the verification view
- Superintendent uses the side-by-side view during re-inspection to confirm adequacy of correction

Subcontractors who do not submit an after photo cannot have their item marked `completed`. The superintendent should enforce this consistently to maintain documentation integrity.

---

## Photo Organization and Storage

```
punch-list-photos/
  Level-1/
    Room-101/
    Room-102/
    Corridor-A/
  Level-2/
    ...
  Exterior/
    North-Elevation/
    South-Elevation/
  Roof/
```

- Full-resolution originals are preserved permanently — do not delete after project closeout
- Thumbnails are generated automatically for report embedding
- Photos are linked to punch item records by punch ID
- Area subdirectories mirror the walkthrough room sequence for navigability

---

## Integration with Daily Reports

Punch list walkthrough photos may be included in the daily report photo section when the walk is a significant daily activity.

Caption format for daily report inclusion:

```
Punch item PUNCH-{NNN}: [brief deficiency description] — [current status]
```

Example: `Punch item PUNCH-033: Damaged ceiling tile in Room 204 — assigned to drywall, due 2026-02-24`

Do not include every punch photo in daily reports. Select representative items or critical items that affect schedule to keep daily reports concise and readable.
