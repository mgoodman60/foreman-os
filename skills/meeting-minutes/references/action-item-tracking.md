# Action Item Tracking Reference

## Action Item Schema

Every action item extracted from meeting minutes is stored as a structured record. This schema is the canonical format used across all meeting types (OAC, progress, pre-install, etc.).

| Field | Type | Description |
|-------|------|-------------|
| id | string | Format: AI-{YYYY}-{NNN} — e.g., AI-2026-001 (sequential per project per year) |
| description | string | Clear, specific action required — written as an imperative ("Submit revised shop drawings for structural steel") |
| assigned_to | string | Person or company responsible — use full name and company where possible |
| due_date | date | Target completion date — ISO 8601 (YYYY-MM-DD) |
| status | enum | open, in_progress, completed, carry_forward |
| priority | enum | critical, high, normal, low |
| category | enum | schedule, budget, rfi, submittal, change_order, quality, safety, coordination, closeout, other |
| meeting_originated | string | Meeting ID where item was created (e.g., OAC-2026-014) |
| meetings_carried | number | Count of meetings the item has been carried forward without resolution |
| resolution_notes | string | How the item was resolved — include any decisions made |
| date_completed | date | Actual completion date (populated when status set to completed) |

---

## Action Item ID Format

```
AI-{YEAR}-{SEQUENCE}

Examples:
  AI-2026-001   First action item created in 2026
  AI-2026-047   47th action item created in 2026
```

Sequence numbers are project-scoped and reset each calendar year. IDs must be unique and never reused, even if an item is deleted.

---

## Carry-Forward Logic

Items not completed by their due date automatically appear at the top of the "Old Business / Action Items" section in the next meeting agenda.

- Each carry-forward increments the `meetings_carried` counter by 1
- Items carried forward display an aging flag in the minutes
- Display format in meeting minutes:

```
CARRY-FORWARD (x3) — Submit approved shop drawings for structural steel
  Assigned: J. Martinez (Acme Steel)  |  Due: 2026-01-15  |  OVERDUE 18 days
  Notes: Awaiting engineer response to RFI-2026-022
```

- Original due date is preserved; do not update it unless formally revised by all parties
- Revised due dates must be documented as a decision in the meeting minutes

---

## Escalation Rules

Escalation is based on the number of consecutive meetings an item has been carried forward without resolution.

| Condition | Meetings Carried | Flag | Action Required |
|-----------|-----------------|------|-----------------|
| On track | 0 | None | No action |
| First carry-forward | 1 | Yellow | Remind assignee verbally at meeting; note in minutes |
| Second carry-forward | 2 | Orange | PM notified in writing; assignee must provide updated timeline |
| Third carry-forward | 3 | Red | Formal written notice to assignee's company; PM escalates to owner |
| Fourth+ carry-forward | 4+ | Critical | Escalate to owner; include in weekly progress report; document potential schedule/cost impact |

Escalation notices are generated as formal letters or emails by the PM and attached to the meeting minutes record for that period.

---

## Priority Definitions

| Priority | Definition | Response Expectation |
|----------|------------|---------------------|
| critical | Blocking active construction work or triggering a schedule delay today | Resolve within 24 hours |
| high | Will impact schedule or cost if not resolved within the current meeting cycle | Resolve before next meeting |
| normal | Standard coordination item with adequate lead time | Resolve by stated due date |
| low | Informational or administrative; no immediate schedule/cost impact | Resolve within 30 days or next applicable milestone |

---

## Integration Points

The action item database is the shared source of truth referenced by multiple meeting-minutes skill outputs and other ForemanOS skill integrations.

- **morning-brief**: Overdue action items (any priority) appear in the morning briefing agenda section. Critical items are called out individually.
- **weekly-report-format**: Action item summary table included in weekly owner reports — columns: new this week, closed this week, overdue count, total open.
- **project-dashboard**: Action item aging chart and resolution rate metric displayed in the project health panel. Overdue critical items trigger a dashboard alert.
- **daily-report-format**: Action items are referenced in daily log entries when related work is documented (e.g., "Per AI-2026-031, confirmed concrete pour sequence with structural EOR").

---

## Reporting Metrics

Track these metrics at each OAC meeting and include in the weekly report summary.

**Resolution Rate**
- Meeting-to-meeting resolution rate = items closed this period / items that were open at start of period
- Target: 80% or higher resolution rate per meeting cycle
- Trend: report 4-week rolling average to show improving or declining performance

**Aging Distribution**
Report the count of open items in each age band:

| Age Band | Count | % of Total |
|----------|-------|-----------|
| 0–7 days | | |
| 8–14 days | | |
| 15–30 days | | |
| 31+ days | | |

**Assignee Summary**
| Assignee | Open Items | Overdue | % Overdue |
|----------|-----------|---------|-----------|
| (Name / Company) | | | |

- Top 3 assignees by open item count are highlighted in the weekly report
- Items overdue by 30+ days receive individual line-item callout

**Average Days to Resolution**
- Track by category (RFI, submittal, quality, safety, etc.)
- Benchmark against project averages to identify systemic delays

---

## Action Item Language Standards

When extracting or writing action items from meeting discussion, use these conventions:

- Start with an imperative verb: "Submit," "Provide," "Confirm," "Schedule," "Review," "Resolve," "Coordinate"
- Name the responsible party explicitly — never write "contractor" or "team" without a specific company or person
- Include a specific deliverable or measurable outcome — not "look into it" but "provide written confirmation from structural EOR"
- Include the due date in the item description as well as the due_date field

**Example — Poor:** "Someone needs to check on the steel delivery."

**Example — Good:** "AI-2026-033 — Acme Steel (J. Martinez) to provide confirmed delivery date for W-flange columns (Grid Lines A–D). Due: 2026-02-28."
