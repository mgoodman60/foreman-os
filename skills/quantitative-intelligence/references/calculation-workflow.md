# Calculation Workflow — Quantitative Intelligence

Step-by-step guide for requesting quantity calculations, understanding calculator classes, interpreting results, and integrating with downstream skills.

---

## Requesting a Quantity Calculation

### Step 1: Identify the Element

Determine what needs to be measured. Elements are identified by their mark, type, or location:

| Element Type | Identifier Examples | Where to Find |
|-------------|-------------------|---------------|
| Footing | F1, F2, F3 | Foundation plan (S2.x series) |
| Slab on Grade | SOG Area A, SOG Area B | Floor plan + structural notes |
| Wall | Wall Type 2A, 4B | Wall type legend + floor plans |
| Room | Room 107, Therapy | Floor plan + finish schedule |
| Pipe Run | 4" DWV, 2" CW | Plumbing plan + riser diagram |
| Equipment | RTU-1, LP-1 | Equipment schedule + MEP plans |
| Fixture | Duplex Outlet, WC-1 | Panel/fixture schedule + plans |
| PEMB | Bay 1-2, Column C3 | PEMB erection + reaction drawings |

### Step 2: Find the Assembly Chain

Look up the element in `plans-spatial.json` → `sheet_cross_references.assembly_chains[]`:

```json
{
  "id": "CHAIN-001",
  "description": "Footing F1 at Grid C-3",
  "links": [
    {"sheet": "S2.1", "element": "Footing F1 plan view", "data": "location, plan dimensions"},
    {"sheet": "S5.1", "element": "Detail 3 — Footing F1 section", "data": "depth, rebar, dowels"},
    {"sheet": "S1.0", "element": "Structural general notes", "data": "concrete PSI, rebar grade"}
  ]
}
```

If no pre-built chain exists, build one by:
1. Finding the element on its primary sheet (plan view)
2. Checking `detail_callouts[]` for references to detail/section sheets
3. Checking `spec_references[]` for spec notes
4. Following each link to gather dimensions and specifications

### Step 3: Run the Calculation

The `calc_bridge.py` reference script contains 10 calculator classes. Each takes assembly chain data as input and produces quantities with source attribution.

### Step 4: Get Results with Source Attribution

Every calculated value includes:
- **Value** — the numeric result
- **Unit** — measurement unit (CY, SF, LF, EA, etc.)
- **Source** — which data source provided the input (dxf, visual, takeoff, text)
- **Confidence** — high/medium/low based on source priority and cross-verification
- **Source sheets** — which drawing sheets contributed data

---

## Calculator Class Reference

### 1. ConcreteVolumeCalc

**Computes:** Volume in CY for concrete elements (footings, SOG, grade beams, piers, walls, curbs).

**Input:** Length, width, depth from assembly chain links. Waste factors applied automatically.

**Formulas:**
```
Footings: L × W × D × count / 27 × 1.10 (10% waste)
SOG:      Area SF × thickness / 12 / 27 × 1.05 (5% waste)
Walls:    L × H × T / 27 × 1.05
Piers:    π × r² × D / 27 × 1.05 (round) or L × W × D / 27 (square)
Curbs:    L × W × H / 27 × 1.05
```

**Output:** `volume_cy_each`, `volume_cy_total`, `concrete_psi`, `rebar_spec`

### 2. WallAreaCalc

**Computes:** Total linear feet, total square feet, GWB area, insulation area, stud count by wall type.

**Input:** Wall type definition (layers, thickness), lengths from plan sheets, heights from building sections.

**Formulas:**
```
Total SF = Total LF × Height
GWB SF   = Total SF × sides_with_gwb
Stud Count = (Total LF × 12 / stud_spacing) + 1 per wall segment
```

**Output:** `total_lf`, `total_sf`, `gwb_sf`, `insulation_sf`, `stud_count`

### 3. RoomAreaCalc

**Computes:** Floor area, perimeter, wall area, ceiling area for each room.

**Input:** Room boundary from DXF polylines (exact) or visual detection (approximate), ceiling height from building section or finish schedule.

**Formulas:**
```
Area SF    = Shoelace formula on polyline vertices (DXF) or pixel counting (visual)
Perimeter  = Sum of boundary segment lengths
Wall SF    = Perimeter × Ceiling Height
Ceiling SF = Floor Area (flat) or calculated from section (sloped)
```

**Output:** `area_sf`, `perimeter_lf`, `wall_sf`, `ceiling_sf`

### 4. PipeRunCalc

**Computes:** Total linear feet by system, material, and size. Fitting count, hanger count.

**Input:** Pipe runs from plumbing/mechanical plans, riser diagrams for vertical runs.

**Formulas:**
```
Total LF = Sum of all run segments (plan) + vertical runs (riser)
Fittings = Count of elbows, tees, reducers from plan symbols
Hangers  = Total LF / hanger_spacing (typically 8-10 ft for horizontal)
```

**Output:** `total_lf`, `fitting_count`, `hanger_count` per system/size

### 5. FootingCalc

**Computes:** Comprehensive footing quantities — volume, rebar weight, form area.

**Input:** Plan dimensions + detail section + structural notes via assembly chain.

**Formulas:**
```
Volume CY  = L × W × D / 27 × 1.10
Rebar Lbs  = (bars_each_way × bar_length × weight_per_lf) × layers
Form SF    = 2 × (L + W) × D (perimeter × depth for continuous)
```

**Output:** `volume_cy`, `rebar_weight_lbs`, `form_area_sf`

### 6. SlabCalc

**Computes:** SOG area, concrete volume, vapor barrier area, reinforcement quantity.

**Input:** Floor plan area + structural notes (thickness, reinforcement, vapor barrier spec).

**Formulas:**
```
Area SF       = Plan area
Volume CY     = Area × Thickness / 12 / 27 × 1.05
Vapor Barrier = Area SF × 1.10 (10% overlap)
WWF/Rebar     = Area SF (mesh) or calculated from spacing (rebar)
```

**Output:** `area_sf`, `volume_cy`, `vapor_barrier_sf`, `reinforcement_qty`

### 7. RoofCalc

**Computes:** Roof area (flat projection and true/sloped area), insulation area.

**Input:** Roof plan (flat area) + building section (slope).

**Formulas:**
```
Flat Area SF  = Plan measurement
Slope Factor  = 1 / cos(slope_angle)
True Area SF  = Flat Area × Slope Factor
Insulation SF = True Area SF × 1.05 (5% waste)
```

**Output:** `flat_area_sf`, `true_area_sf`, `insulation_sf`, `slope_factor`

### 8. PEMBCalc

**Computes:** PEMB-specific quantities — bay areas, tributary areas, wall/roof panels, gutter, downspouts.

**Input:** PEMB erection drawings, reaction sheets, building sections.

**Formulas:**
```
Bay Area SF         = Bay Length × Bay Width
Tributary Area      = Bay Spacing × Frame Spacing
Wall Panel SF       = Eave Height × Perimeter − Openings
Roof Panel SF       = Ridge Length × Slope Length × 2
Gutter LF           = Eave Length (both sides)
Downspout Count     = Gutter LF / 50 (1 per 40-50 LF)
```

**Output:** `bay_areas_sf[]`, `tributary_areas[]`, `wall_panel_sf`, `roof_panel_sf`, `gutter_lf`, `downspout_count`

### 9. SymbolCountCalc

**Computes:** Fixture and device counts from visual detection, validated against schedules.

**Input:** Visual symbol detection from plan sheets + schedule counts.

**Formulas:**
```
Plan Count    = Sum of detected symbols across all plan sheets (dedup overlapping sheets)
Schedule Count = Count from door/fixture/panel schedule
Discrepancy   = |Plan Count − Schedule Count| / Schedule Count > 10%
```

**Output:** `plan_count`, `schedule_count`, `discrepancy` flag

### 10. AggregateCalc

**Computes:** CSI division totals — roll up individual item quantities into division-level summaries.

**Input:** All individual quantities from above calculators.

**Formulas:**
```
Division Total = Sum of all items matching CSI division
Example: Div 03 = Footings CY + SOG CY + Walls CY + Piers CY + Curbs CY
```

**Output:** `csi_division`, `total_qty`, `unit`, itemized breakdown

---

## Result Interpretation Guide

### Source Priority Levels

| Priority | Source | Meaning | When to Trust |
|----------|--------|---------|--------------|
| 1 (highest) | DXF | Exact CAD coordinates | Always — this is the authoritative source |
| 2 | Visual | Claude Vision analysis of plan images | Good for areas and counts; ±5-10% on dimensions |
| 3 | Takeoff | Scale-calibrated manual measurement | Good when properly calibrated; ±2-5% |
| 4 (lowest) | Text | Parsed from PDF text annotations | Verify against other sources; values may be notes not dimensions |

### Confidence Scores

| Level | Criteria | Action |
|-------|----------|--------|
| **VERIFIED** | 3+ sources agree | High confidence — use directly |
| **CONFIRMED** | 2 sources agree | Good confidence — use directly |
| **LIKELY CORRECT** | 2 sources within 5% | Acceptable — note minor variance |
| **CHECK** | 2 sources 5-10% apart | Moderate concern — may be rounding or scale error |
| **DISCREPANCY** | 2 sources >10% apart | Flag for superintendent review — do not auto-resolve |
| **UNVERIFIED** | 1 source only | Use with caution — note in output |

### Discrepancy Flags

When sources disagree by >10%, the system flags the discrepancy:

```json
{
  "item": "Footing F1 volume",
  "source_a": "dxf",
  "value_a": 0.44,
  "source_b": "visual",
  "value_b": 0.52,
  "variance_pct": 18.2,
  "resolution": "",
  "resolved": false
}
```

**Resolution workflow:** Present both values to the superintendent with source attribution. The superintendent decides which value to use. Never auto-resolve discrepancies.

---

## Integration Examples

### Cost Tracking — Budget Verification

`cost-tracking` reads quantities to verify budget line items:

```
1. Read plans-spatial.json → quantities.concrete
2. Sum volume_cy_total for all footings
3. Compare against Division 03 budget in cost-data.json
4. Calculate: Budget CY × unit rate vs Plan CY × unit rate
5. Flag if plan quantities exceed budget by >5%
```

### Daily Report — Progress Tracking

`/daily-report` reads quantities to calculate progress percentages:

```
1. User logs: "Poured footings F1-F4 today"
2. Read plans-spatial.json → quantities.concrete → F1, F2, F3, F4
3. Sum CY poured today: 1.76 CY
4. Total footing CY from quantities: 8.2 CY
5. Report: "Poured F1-F4: 1.76 CY of 8.2 CY total footings (21%)"
```

### Labor Tracking — Productivity Benchmarking

`labor-tracking` reads quantities to calculate output per labor-hour:

```
1. Crew logged: 6 workers × 8 hours = 48 labor-hours on concrete
2. Read plans-spatial.json → quantities.concrete → footings poured today
3. CY poured: 1.76 CY
4. Productivity: 1.76 CY / 48 hrs = 0.037 CY/labor-hour
5. Benchmark: 0.040 CY/labor-hour for formed footings
6. Efficiency: 0.037 / 0.040 = 92% (Good)
```

### Morning Brief — Quantity Context

`/morning-brief` uses quantities to add context to today's work:

```
Today's Work: Footing pour at Grid D-3 through E-5
  Footings F5-F8: 3.2 CY concrete (4,000 PSI)
  Rebar: #5 @ 12" EW, pre-inspected ✓
  Hold Point: Pre-placement inspection required (HP-02)
  Weather: 45°F — above 40°F minimum ✓
```

---

## Discrepancy Resolution Workflow

When sources disagree by >10%, follow this process:

1. **Present the discrepancy** to the superintendent with both values and their sources
2. **Show the context** — which sheets each value came from, what method was used
3. **Suggest investigation** — the most likely cause of the discrepancy:
   - Scale calibration error (visual vs DXF)
   - Revision mismatch (different sheet revisions)
   - Interpretation difference (net vs gross area)
   - Drawing coordination error (plan vs detail don't match)
4. **Record the resolution** — superintendent picks the authoritative value
5. **Update the quantity** — set the resolved value and mark `resolved: true`
6. **Note for future** — if the discrepancy reveals a drawing error, suggest an RFI

---

## Waste Factor Application

When any calculator class applies waste factors, source the waste percentage using this hierarchy:

### Sourcing Hierarchy

1. **First**: Check `project-config.json` for project-specific waste factors (`waste_factors` object keyed by material type). If the project has defined a waste factor for the material in question, use it.
2. **Second**: If not found in project config, use defaults from `estimating-intelligence/SKILL.md` → Waste Factor Reference table. Match by material type and use the "Typical Waste %" column as the default. Adjust toward "Low" or "High" based on project conditions (geometry complexity, access, storage quality).
3. **Third**: For unusual materials not in either source, use 5% as a conservative default and flag for superintendent review.

### Reporting Waste Factor Source

Report waste factor source in every calculation output that includes waste:

- `waste_factor_percent`: The applied percentage (e.g., `5`)
- `waste_factor_source`: One of `"project_config"` | `"estimating_default"` | `"conservative_default"`

Example output:
```json
{
  "item": "Footing F1 concrete volume",
  "net_quantity_cy": 0.44,
  "waste_factor_percent": 3,
  "waste_factor_source": "project_config",
  "gross_quantity_cy": 0.45
}
```

### Procurement Cross-Reference

Cross-reference applied waste factors with procurement data to catch ordering discrepancies:

- Read `procurement-log.json` → for each material line item, compare `ordered_quantity` against `net_quantity`
- Calculate the implied waste factor: `(ordered_quantity / net_quantity - 1) × 100`
- If the implied waste factor differs from the applied waste factor by >5 percentage points, flag for superintendent review
- Example: Net concrete quantity = 38 CY, applied waste = 5% (expect 39.9 CY ordered), but `procurement-log.json` shows `ordered_quantity: 45 CY` → implied waste = 18.4% → difference = 13.4 points → **flag for review**
