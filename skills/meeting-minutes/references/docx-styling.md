# Meeting Minutes Document Styling Reference

## Document Layout

| Property | Value |
|----------|-------|
| Page size | US Letter — 8.5" x 11" (21590 x 27940 twips in DXA) |
| Margin — top | 1" (1440 twips) |
| Margin — left | 1" (1440 twips) |
| Margin — right | 1" (1440 twips) |
| Margin — bottom | 0.75" (1080 twips) |
| Body font | Calibri 10pt |
| Header font | Calibri Bold (size varies by level — see Typography below) |
| Table header font | Calibri Bold 9pt |
| Line spacing | Single (240 twips) with 6pt spacing after paragraph |

---

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Document title | Calibri | 14pt | Bold | #1B2A4A |
| Section header | Calibri | 11pt | Bold | #1B2A4A |
| Subsection header | Calibri | 10pt | Bold | #1B2A4A |
| Body text | Calibri | 10pt | Regular | #000000 |
| Table header text | Calibri | 9pt | Bold | #FFFFFF |
| Table body text | Calibri | 9pt | Regular | #000000 |
| Footer text | Calibri | 8pt | Regular | #666666 |

---

## Header and Footer

**Header** (appears on all pages):
- Left: Project name (Calibri Bold 10pt, #1B2A4A)
- Center: Meeting type and number — e.g., "OAC Meeting No. 14" (Calibri 10pt)
- Right: Meeting date — e.g., "February 21, 2026" (Calibri 10pt)
- Bottom border: 1pt solid line, color #2E5EAA

**Footer** (appears on all pages):
- Left: "CONFIDENTIAL — FOR PROJECT USE ONLY" (Calibri 8pt, #666666)
- Center: Page number — "Page X of Y" (Calibri 8pt)
- Right: Company name (Calibri 8pt, #666666)
- Top border: 0.5pt solid line, color #CCCCCC

---

## Color Palette

Match Foreman OS report styling across all generated documents.

| Element | Color Name | Hex |
|---------|-----------|-----|
| Section header bar background | Light blue | #EDF2F9 |
| Section header bar left accent (border) | Blue | #2E5EAA |
| Section header text | Navy | #1B2A4A |
| Table header background | Navy | #1B2A4A |
| Table header text | White | #FFFFFF |
| Table row — standard | White | #FFFFFF |
| Table row — alternating | Light gray | #F5F5F5 |
| Table borders | Light gray | #CCCCCC |
| Action item — completed | Green | #2D8F4E |
| Action item — in progress | Blue | #2E5EAA |
| Action item — overdue | Red | #C0392B |
| Action item — open | (no highlight) | — |

---

## Section Header Bar Style

Each major agenda section (Call to Order, Schedule Update, etc.) uses a styled paragraph to visually separate sections.

```typescript
// Section header bar implementation (docx-js)
new Paragraph({
  children: [new TextRun({ text: "4. Schedule Update", bold: true, color: "1B2A4A", size: 22 })],
  shading: { type: ShadingType.CLEAR, color: "auto", fill: "EDF2F9" },
  border: {
    left: { style: BorderStyle.THICK, size: 12, color: "2E5EAA" },
  },
  spacing: { before: 120, after: 60 },
  indent: { left: 120 },
})
```

---

## Attendee Table Format

Columns: Name | Organization | Role | Present

| Property | Value |
|----------|-------|
| Total width | Full page width (9360 DXA at 1" margins) |
| Column widths | 2340 / 2340 / 2340 / 2340 DXA (25% each) |
| Header background | #1B2A4A |
| Header text | White, Bold, 9pt |
| Presence indicator | Checkmark character (✓) for present, em dash (—) for absent |
| Alternating rows | #FFFFFF / #F5F5F5 |
| Borders | All borders, 0.5pt, #CCCCCC |

---

## Action Item Table Format

Columns: ID | Description | Assigned To | Due Date | Status | Notes

| Property | Value |
|----------|-------|
| Total width | Full page width (9360 DXA) |
| Column widths | 1170 / 2808 / 1638 / 1170 / 936 / 1638 DXA |
| ID column | Calibri Bold 9pt, no wrap |
| Status cell | Color-coded background per action item status (see Color Palette) |
| Status text | White when colored background is used, Bold 9pt |
| Overdue items | Red (#C0392B) background on Status cell; entire row may optionally use #FFF5F5 |

```typescript
// Status cell shading example
shading: {
  type: ShadingType.CLEAR,
  color: "auto",
  fill: status === "completed" ? "2D8F4E"
      : status === "in_progress" ? "2E5EAA"
      : status === "overdue" ? "C0392B"
      : "FFFFFF",
}
```

---

## Discussion Items Format

Each agenda item's discussion content follows this structure:

1. **Topic line** — Bold, the agenda item title (e.g., "4.2 Critical Path — Tower Crane Removal")
2. Discussion summary — One or more paragraphs summarizing what was discussed, who said what (attribute by name/company), and key information shared
3. Decision/outcome — If a decision was made, start a new paragraph with "Decision:" in bold, followed by the decision text
4. Action item reference — If an action item was generated, append "See AI-2026-NNN" in italic at the end of the section

```
4.2 Critical Path — Tower Crane Removal

   J. Smith (ABC Construction) reported that crane demobilization is
   scheduled for March 15 and is on the critical path. Structural
   enclosure at Level 12 must be complete by March 10.

   Decision: Owner authorized weekend work on March 7–8 to meet the
   structural enclosure deadline. Overtime premium is within approved
   contingency.

   See AI-2026-041.
```

---

## Distribution List

A distribution table appears at the end of the document, after the signature block.

Columns: Name | Organization | Method | Date Sent

| Property | Value |
|----------|-------|
| Total width | Full page width |
| Column widths | 2340 / 2340 / 2340 / 2340 DXA |
| Method values | Email, Physical Copy, Portal Upload |
| Date Sent | Populated by PM when minutes are distributed |

---

## Signature Block

Two signature lines at the bottom of the final page, above the distribution list.

```
Prepared by:  _________________________________  Date:  ___________
              Name / Title

Approved by:  _________________________________  Date:  ___________
              Name / Title
```

Implemented as a 2-column table with no visible borders. Left column contains the signature line text; right column contains the date line.

---

## docx-js Implementation Notes

Follow the same patterns established in `daily-report-format` for consistency across all ForemanOS generated documents.

- **Units**: Always use `WidthType.DXA` for table and column widths. 1 inch = 1440 DXA.
- **Shading**: Use `ShadingType.CLEAR` with explicit `fill` hex values (no `#` prefix in docx-js).
- **Section header bars**: Apply `BorderStyle.THICK` on the left border at size 12 for the blue accent; set `ShadingType.CLEAR` fill to `"EDF2F9"` for the background.
- **Tables**: Always set both the table-level `columnWidths` array and individual `width` on each cell. Relying on only one causes rendering inconsistencies in Word.
- **Paragraphs**: Use separate `Paragraph` elements for each line of text. Never embed `\n` newline characters inside a `TextRun` — this breaks Word rendering.
- **Borders**: For table cell borders, specify all four sides explicitly (`top`, `bottom`, `left`, `right`) using `BorderStyle.SINGLE` at size 4 (0.5pt) with color `"CCCCCC"`.
- **Page numbers**: Use `PageNumber.CURRENT` and `PageNumber.TOTAL_PAGES` from the docx library for header/footer page numbering.
- **Header/Footer**: Define as `Header` and `Footer` objects on the `Section` — not as floating paragraphs. Use a tab stop at center (4680 DXA) and right (9360 DXA) for three-column header layout.
