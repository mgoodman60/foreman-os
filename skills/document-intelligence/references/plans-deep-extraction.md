# Plans & Drawings - Deep Extraction Guide

Extract comprehensive, field-actionable data from construction drawings. Focus on schedules, specifications, and coordination data that enable daily reporting and project management.

---

## Extraction Priority Matrix

| Priority | Data Type | Use Case | Completeness Target |
|----------|-----------|----------|-------------------|
| **CRITICAL** | Grid lines, floor levels | Spatial reference in daily reports | 100% |
| **CRITICAL** | Room schedule (all rooms) | Progress tracking by room | 100% |
| **HIGH** | Finish schedule | Room completion tracking | 100% if present |
| **HIGH** | Door/window schedules | Procurement and installation tracking | 100% if present |
| **HIGH** | MEP equipment schedules | Coordination and startup | 100% if present |
| **HIGH** | Structural specs (notes) | Field verification of installations | Extract all specific values |
| **HIGH** | *RENDERING DATA* Exterior elevations | Visual rendering and design documentation | Extract all visual details |
| **HIGH** | *RENDERING DATA* Casework/millwork | Interior appearance and finish tracking | Extract all finishes and colors |
| **HIGH** | Building sections | Heights, foundation depth, roof slope, structure depth | 100% if present |
| **HIGH** | Wall sections | Assembly layers, fire ratings, total thickness | 100% if present |
| **HIGH** | Exterior elevation materials | Cladding zones, colors, manufacturer codes per face | 100% if present |
| **HIGH** | Accessibility data | ADA routes, restrooms, ramps, signage, parking, counters | 100% if present |
| **HIGH** | Keynote schedules | Keynote number → description → spec section linking | 100% if present |
| **MEDIUM** | Hatch refinement | Improved material zone classification using standard patterns | All hatched zones |
| **MEDIUM** | General notes | Numbered construction notes with category classification | 100% if present |
| **MEDIUM** | Site coordinates (laydown, etc.) | Site logistics | Extract if clearly marked |
| **MEDIUM** | Detailed dimensions | Verification and layout | Extract key dimensions only |

---

## STRUCTURAL DRAWINGS (S-series)

### Grid Lines - Foundation/Framing Plans

**ALWAYS EXTRACT**:
- **Column identifiers**: Letters (A, B, C) or alphanumeric (A.1, A.2)
- **Row identifiers**: Numbers (1, 2, 3) or combinations
- **Grid spacing**: If dimensioned (e.g., "30'-0" typ.")
- **Skewed/offset grids**: Note angles and offsets
- **Orientation notes**: "Grid A = west side", "Grid 1 = south"

**Output format**:
```json
{
  "columns": ["1", "2", "3", "4", "5", "6"],
  "rows": ["A", "B", "C", "D", "E", "F", "G", "H"],
  "spacing": "Varies: 20'-30' typical",
  "notes": "Rectangular PEMB grid layout, Grid 1 south side"
}
```

### Structural General Notes (S-001 or similar)

**CRITICAL - Extract ALL specific numerical values**:

#### Concrete Specifications
For each element type (footings, walls, SOG, elevated slabs, columns):
- **Design strength**: _____ PSI at 28 days
- **W/C ratio max**: e.g., "0.45"
- **Slump**: e.g., "4 inches ± 1"
- **Air content**: e.g., "5.5% ± 1.5%"
- **Max aggregate size**: e.g., "3/4 inch"
- **Curing duration**: e.g., "7 days wet cure for slabs"

**Weather thresholds**:
- Cold weather: Below ___°F threshold, protection method and duration
- Hot weather: Above ___°F threshold, mitigation measures

**Example extraction**:
```
Footings: 3,000 PSI, w/c 0.50 max, slump 4"±1", cure 3 days
SOG: 4,000 PSI, w/c 0.45 max, slump 4"±1", air 5%±1.5%, cure 7 days
Cold weather: <40°F, maintain 50°F for 72 hours after placement
Hot weather: >90°F, ice in mix, cool aggregates, night pour if >95°F
```

#### Reinforcing Steel
- **Rebar grade**: e.g., "Grade 60", "ASTM A615"
- **Standard sizes used**: #4, #5, #6, etc.
- **Lap splice lengths by size**: "#4: 24\", #5: 30\", #6: 36\""
- **Cover requirements by element**:
  - Footings against earth: ___"
  - Walls against earth: ___"
  - SOG: ___"
  - Elevated slabs: ___" top, ___" bottom

**Example**:
```
Rebar: Grade 60 (ASTM A615)
Lap splices: #4 = 24", #5 = 30", #6 = 36"
Cover: Footings 3", walls 2", SOG 2", elevated slabs 3/4" top/2" bottom
```

#### Structural Steel
- **Grades by member**: "W-shapes: A992", "HSS: A500 Grade C"
- **Bolt specs**: Grade (A325/A490), sizes used, torque values
- **Weld specs**: Electrode (E70XX), weld sizes, inspection %
- **Fireproofing**: Type, thickness by rating (1-hr, 2-hr, 3-hr)

**Example**:
```
Steel: Beams A992, columns A500 Gr.C, A325 bolts 3/4" @ 150 ft-lb torque
Welds: E70XX, fillet welds per AWS D1.1, inspect 100% of moment connections
Fireproofing: Spray-applied 1.5" for 2-hour rating on columns/beams
```

#### Anchor Bolts & Embeds
- Grades: e.g., "F1554 Grade 36"
- Embedment depths by diameter
- Tolerance: plan location (±__"), elevation (±__")
- Grout requirements

#### Foundation Details
- Footing types and typical sizes
- Foundation wall thickness/height
- Bearing depth below grade
- Vapor barrier specs

#### Slab Details
- Thickness (SOG, elevated)
- Reinforcing (WWF designation, rebar spacing)
- Control joint spacing and method
- FF/FL numbers if specified
- Sub-base: material, thickness, compaction

---

## BUILDING AND WALL SECTIONS (A-300, A-400, S-300 series)

### Building Sections (Data Source: Pass 10 of Visual Pipeline / Pass 4F of Claude Vision)

Building sections are full-height cross-cuts through the building, typically found on A-300 series sheets. They are the **primary source** for vertical dimensioning that cannot be obtained from plan views.

**ALWAYS EXTRACT** from every building section on the sheet:

1. **Section identification**: Section mark (e.g., "1/A-300"), cut location (which grid line), direction of view
2. **Elevation markers**: ALL named elevation markers (T.O. STEEL, FFE, B.O. FOOTING, RIDGE, etc.) with their elevation values
3. **Key heights** (calculated from elevation markers):
   - Floor-to-structure height (FFE to T.O. Steel/Wall)
   - Foundation depth (FFE to B.O. Footing)
   - Ridge height (FFE to Ridge)
   - Eave/parapet height
   - Ceiling height (FFE to ceiling line)
4. **Roof slope**: From slope triangle symbols or text notation
5. **Structural members**: Type (rafter, truss, joist, beam, purlin) and depth
6. **SOG thickness**: Slab-on-grade thickness from section

**Store in**: `plans-spatial.json → sections.building[]`

**Cross-checks**:
- Foundation depth vs geotech minimum embedment (e.g., 24" below grade)
- Ceiling height vs RCP height zones (should match within 2")
- Roof slope vs structural framing slope
- Floor-to-structure height vs PEMB eave height (for PEMB projects)

### Wall Sections

Wall sections are enlarged cross-cuts through wall assemblies, typically on A-300/A-400 series sheets at 1-1/2"=1'-0" or 3"=1'-0" scale. They define the **layer-by-layer composition** of every wall type.

**ALWAYS EXTRACT** from every wall section:

1. **Wall type identifier**: Match to wall type legend or plan annotations (Type 1, Type 2, etc.)
2. **Fire rating**: If annotated (1-HR, 2-HR, UL assembly number)
3. **Layer-by-layer assembly** (from exterior to interior):
   - Material name with full specification (e.g., "5/8\" Type X GWB")
   - Thickness of each layer
   - Position classification: exterior_finish, sheathing, air_barrier, insulation, stud_cavity, interior_finish
   - R-value for insulation layers
4. **Total wall thickness**: From overall dimension or sum of layers
5. **Connection conditions**: Base (floor), top (structure/ceiling), head (at openings), sill (at windows)

**Store in**: `plans-spatial.json → sections.wall[]`

**Cross-checks**:
- Wall type labels on plans should each have a corresponding wall section
- Fire-rated partitions on plans should match section fire rating annotations
- Layer sum should equal total thickness within ±0.25"
- Exterior walls should have insulation (flag if missing in Climate Zone 4+)
- 1-HR walls require min 5/8" Type X GWB each side

**Downstream consumers**:
- **Estimating / Takeoff**: Wall layers × wall areas = GWB SF, insulation SF, stud LF
- **Quality Management**: Fire rating → inspection checklist items
- **Rendering**: Assembly appearance → 3D model material assignment
- **Scheduling**: Wall complexity → framing/finishing duration estimate

---

## ARCHITECTURAL DRAWINGS (A-series)

### Exterior Elevations - Visual Data

**[RENDERING DATA]** Extract from elevation sheets (A-200 series) for visual design documentation and rendering systems.

**Wall Cladding by Elevation**:
For each building elevation (North, South, East, West):
- **Material type**: Metal panels, CMU, brick, stone veneer, composite board, etc.
- **Color/finish**: Specific color name AND manufacturer code if available
  - Example: "South elevation: Vertical metal panels, champagne tan (Nucor color code 12)")
  - Example: "East elevation: Split-face CMU, warm gray with decorative brick band")
- **Pattern/texture**: Smooth, ribbed, board-and-batten, running bond, etc.
- **Material transitions**: Where materials change, note the transition type (trim, flashing, etc.)

**Roof Material and Color**:
- **Membrane type**: Standing seam, asphalt shingle, metal shingle, TPO, EPDM, etc.
- **Color**: Specific color name (e.g., "Charcoal gray standing seam", "Slate blue")
- **Manufacturer code** if specified
- **Ridge/hip material**: Material and color (metal vs. shingles)

**Trim/Fascia and Architectural Details**:
- **Trim material**: Aluminum, steel, vinyl, fiber cement, wood, etc.
- **Trim color/finish**: Anodized bronze, painted white, natural finish, etc.
- **Fascia profile**: Open, boxed, exposed rafter tails, etc.
- **Coping/parapet edge**: Material and color
- **Soffit**: Vented or solid, material, color

**Foundation/Base Visible Material**:
- **Below-grade visible element**: CMU plinth, brick, stone base, exposed concrete, etc.
- **Height from grade**: e.g., "12\" above grade"
- **Color**: Match to main wall or contrast
- **Base flashing**: Material visible (aluminum, stainless, flashing color)

**Accent Materials and Colors**:
- **Stone veneer**: Type (limestone, granite, sandstone), color, size/pattern
- **Brick banding**: Color, texture (smooth, tumbled, handmade), mortar color
- **Decorative panels**: Material, color, mounting method
- **Accent stripes or reveals**: Material, width, color

**Canopy/Entry Features**:
- **Portico/canopy structure**: Beam material (steel, aluminum, wood), color/finish
- **Canopy membrane**: If fabric or metal, material and color
- **Entry surround**: Cladding material, color, trim details
- **Signage area**: Location and dimensions (if visible on elevation)

**Example extraction**:
```json
{
  "south_elevation": {
    "primary_cladding": {
      "material": "Vertical metal panels",
      "color": "Champagne tan",
      "mfg_code": "Nucor 12-45"
    },
    "accent": {
      "type": "Split-face CMU band at grade",
      "color": "Warm gray",
      "height": "4 feet"
    }
  },
  "roof": {
    "material": "Standing seam metal",
    "color": "Charcoal gray",
    "mfg": "Nucor Turf Product"
  },
  "trim": {
    "fascia_color": "Painted to match panels",
    "soffit": "Vented aluminum, white"
  }
}
```

---

### Complete Room Schedule

**EXTRACT EVERY ROOM** - critical for progress tracking.

For each room:
- **Room number**: e.g., "101", "B-12", "MDF-1"
- **Room name**: e.g., "Conference Room", "Janitor Closet"
- **Area**: Square footage
- **Department/zone**: e.g., "Administration", "Patient Care"

**Output format**:
```json
{
  "room_schedule": [
    {"number": "101", "name": "Office", "area": "120 SF", "department": "Admin"},
    {"number": "102", "name": "Conference", "area": "240 SF", "department": "Admin"},
    ...
  ]
}
```

### Finish Schedule (R-series sheet)

**EXTRACT ALL ROOMS** - enables room-by-room completion tracking.

For each room, extract:

**Floor Finish**:
- Material: VCT, carpet, ceramic tile, porcelain, LVT, polished concrete, etc.
- Product code if given: "Armstrong VCT 51910"
- **[RENDERING DATA]** Color/pattern code with full manufacturer name
  - Example: "Armstrong VCT 51910 Cool White" not just "white"
  - Example: "Shaw carpet ES-401 Wheat" with product number

**Base**:
- Type: vinyl, ceramic, wood, rubber
- Height: 4", 6", 8"
- **[RENDERING DATA]** Color code with manufacturer reference

**Wall Finish**:
- Material: paint, FRP, ceramic tile, wallcovering
- Paint: Sheen (flat, eggshell, semi-gloss) and **[RENDERING DATA]** color code with manufacturer
  - Example: "SW 7006 Extra White" (Sherwin Williams code), not just "white"
- **[RENDERING DATA]** Tile: Size (e.g., "12x24"), grout color with manufacturer code

**Ceiling**:
- Type: ACT, drywall (GWB), exposed, wood, metal
- ACT: Grid size (2x2, 2x4), tile product
- **[RENDERING DATA]** ACT tile color and manufacturer: "USG Eclipse #7870, white"
- GWB: Type (1/2" Type X, 5/8" Type X), finish level (Level 3-5), **[RENDERING DATA]** paint color

**Wall Protection (NEW)**:
- **[RENDERING DATA]** Chair rail: Material, height, color/finish
- **[RENDERING DATA]** Corner guards: Type (metal, rubber), color
- **[RENDERING DATA]** Crash rails: Height, material, color/finish

**Example**:
```
Room 107 (Nurse Station):
- Floor: VCT, Armstrong 51910 Cool White, wax finish
- Base: 4" vinyl base, Johnsonite color VB-101 Dark Gray
- Wall: Paint, semi-gloss, SW 7006 Extra White
- Ceiling: ACT 2x2, USG Eclipse #7870 white
- Protection: 36" chair rail, Johnsonite rubber in VB-101 Dark Gray
```

### Door Schedule

**EXTRACT ALL DOORS** - critical for procurement and installation tracking:
- **Mark**: Door number/ID
- **Size**: Width x height x thickness (e.g., "3'-0\" x 7'-0\" x 1-3/4\"")
- **Type**: Hollow metal (HM), wood, aluminum, glass
- **Fire rating**: 20-min, 45-min, 60-min, 90-min, 3-hr
- **Frame**: HM, wood, aluminum
- **Hardware group**: e.g., "HW-01", "Group A"
- **Remarks**: Vision lite, closer, panic, etc.

**[RENDERING DATA] - Visual Appearance**:
- **Door color/finish**: "Natural wood stain", "Painted white", "Factory primed gray"
  - Example: "Solid core wood door, natural oak stain" vs. "Hollow metal, painted to match wall (SW 7006)"
- **Frame color/finish**:
  - "Hollow metal frame, painted to match door" or
  - "Anodized aluminum frame, dark bronze" or
  - "Wood frame, natural finish stain to match door"
- **Vision lite glazing type** (if applicable):
  - Clear, frosted, wired, privacy tint
  - Example: "3/4\" wide vision lite, frosted glass"
- **Sidelight/transom** (if present):
  - Dimensions (width x height)
  - Glazing type and color (clear, tinted, privacy)
  - Frame color to match or contrast with main door

**Output**:
```json
{
  "door_schedule": [
    {
      "mark": "101",
      "size": "3'-0\" x 7'-0\" x 1-3/4\"",
      "type": "HM",
      "rating": "90-min",
      "frame": "HM",
      "hardware": "HW-01",
      "remarks": "Closer, vision lite",
      "rendering_data": {
        "door_finish": "Hollow metal, painted white (SW 7006)",
        "frame_finish": "Painted to match door",
        "vision_lite": "Clear glass, 12\" x 36\"",
        "sidelights": "None"
      }
    },
    ...
  ]
}
```

### Window Schedule

**EXTRACT ALL WINDOWS**:
- Mark, size, type (fixed, casement, awning, etc.)
- Glazing (double, triple, low-E, tempered, laminated)
- U-value, SHGC, VT
- Rough opening dimensions

**[RENDERING DATA] - Visual Appearance**:
- **Frame color/finish**:
  - "Anodized bronze", "White painted aluminum", "Clear anodized", "Bronze anodized", etc.
  - Example: "Aluminum frame, anodized dark bronze finish"
- **Mullion pattern**:
  - Divided lite configuration (e.g., "6-lite, 2x3 grid", "4-lite, 1x4 horizontal")
  - Muntins: true or simulated, color match frame
  - Example: "True divided lite, bronze-finish muntins match frame"
- **Sill detail**:
  - Material: aluminum, vinyl, wood, stone, etc.
  - Profile: sloped exterior, sloped interior, etc.
  - **[RENDERING DATA]** Color to match frame or accent
- **Head/jamb detail**:
  - Visible trim or casing: none, aluminum trim, wood casing, etc.
  - **[RENDERING DATA]** Color/finish
  - Example: "1\" aluminum trim cap, anodized bronze to match frame"
- **Window dimensions** (width x height):
  - Provide actual dimensions in feet-inches (e.g., 3'-0\" x 4'-6\")
  - NOT just relative sizing

**Example**:
```json
{
  "window_schedule": [
    {
      "mark": "W-101",
      "size": "3'-0\" x 4'-6\"",
      "type": "Fixed casement",
      "glazing": "Double low-E, tempered",
      "u_value": 0.28,
      "frame_material": "Aluminum",
      "rendering_data": {
        "frame_color": "Anodized dark bronze",
        "mullion_pattern": "6-lite, 2x3 grid, true divided lite",
        "sill_material": "Aluminum, sloped",
        "sill_color": "Anodized to match frame",
        "head_trim": "1\" aluminum cap trim, anodized bronze"
      }
    },
    ...
  ]
}
```

### Casework and Millwork

**[RENDERING DATA]** Extract from interior elevation sheets (A-400/A-500 series) and dedicated casework/millwork drawings for finish tracking and visual rendering.

**Cabinet Style and Construction**:
- **Door style**: Shaker, flat panel, raised panel, slab, frame-and-panel, etc.
- **Construction method**: Face frame (traditional) or frameless (European), hollow core or solid core
- **Cabinet material**:
  - Thermofoil over MDF
  - Wood veneer (species: oak, maple, cherry, walnut, etc.)
  - Painted MDF or plywood
  - Plastic laminate over particleboard
  - Solid wood (hardwood species)

**Cabinet Color/Finish**:
- **Paint finish**:
  - "White painted MDF" with paint color code (e.g., "SW 7006 Extra White")
  - "Gray painted", "Black painted", with specific color code
- **Stain finish**:
  - "Natural oak stain", "Dark walnut stain", "Light maple stain"
  - Sheen level: matte, satin, semi-gloss
- **Laminate finish**:
  - "Warm gray plastic laminate", "White thermofoil", with product code if specified
- **Example**: "White painted MDF cabinets, SW 7006 Extra White satin finish"

**Hardware Style and Finish**:
- **Hardware type**:
  - Bar pulls (length: 96mm, 128mm, etc.), cup pulls, knob (round, square, etc.)
  - Handles vs. pulls, recessed grips
- **Hardware finish**:
  - Brushed nickel, polished chrome, oil-rubbed bronze, matte black, stainless steel, etc.
- **Hardware spacing** for pulls: Standard spacing (e.g., "96mm cc" = center-to-center)
- **Example**: "Bar pulls, 128mm cc, brushed nickel finish"

**Countertop Material**:
- Type: Solid surface, engineered quartz, natural stone (granite, marble, limestone), laminate, butcher block, concrete, etc.
- Thickness: 1-1/4" for most countertops, custom for some
- Edge profile: Square, bullnose, ogee, etc.

**Countertop Color**:
- **[RENDERING DATA]** Full color description with product code:
  - "White quartz with gray veining, Cambria Brittanica" (brand + product name)
  - "Warm gray solid surface, DuPont Corian Lava Stone"
  - "Walnut butcher block with natural edge"
- Include photo reference if in submittal

**Backsplash**:
- **Material**: Ceramic tile, porcelain, glass, stone, stainless steel, natural materials
- **Size**: e.g., "3x6 subway", "1x1 glass", "12x24 large format porcelain"
- **Color**: With manufacturer code if available
  - Example: "3x6 white ceramic subway tile with contrasting dark grout"
  - Example: "12x24 warm beige porcelain with charcoal grout"
- **Pattern**: Running bond, stacked, herringbone, random, etc.
- **Grout color**: Contrasting or matching, specific color code
- **Height**: How far up the wall (full height, 18\" above countertop, etc.)

**Casework Locations**:
- **Which rooms**: List all rooms with casework (kitchen, bathrooms, service areas, etc.)
- **Cabinet configuration**: Upper only, lower only, full height to soffit, open shelving, etc.
- **Lineal footage** if specified
- **Specialty elements**: Beverage cooler, pull-out spice racks, pantry roll-out shelves, etc.

**Example extraction**:
```json
{
  "casework_and_millwork": [
    {
      "location": "Room 105 - Nurse Break Room",
      "cabinet_type": "Kitchen casework",
      "style": "Flat panel",
      "material": "Thermofoil over MDF",
      "color_finish": "White thermofoil, semi-gloss",
      "configuration": "Lower cabinets (30\" tall) + upper cabinets (15\" tall) around perimeter",
      "hardware": {
        "type": "Bar pulls",
        "spacing": "96mm cc",
        "finish": "Brushed nickel"
      },
      "countertop": {
        "material": "Engineered quartz",
        "color": "White quartz with gray veining (Cambria Brittanica)",
        "thickness": "1-1/4\"",
        "edge_profile": "Beveled"
      },
      "backsplash": {
        "material": "Ceramic tile",
        "size": "3x6 subway",
        "color": "Bright white",
        "pattern": "Running bond",
        "grout_color": "Dark gray",
        "height": "Full height to soffit"
      }
    },
    ...
  ]
}
```

---

## MEP DRAWINGS (M/E/P-series)

**CRITICAL**: MEP extraction must go beyond equipment tags. Extract FULL schedule data — capacities, ratings, electrical requirements, fixture details — from MEP schedule sheets (M-300, E-300, P-400 series). See `references/mep-deep-extraction.md` for complete field-by-field templates.

### HVAC Equipment Schedule (M-300 Series)

**EXTRACT EVERY UNIT** from mechanical schedules:

Per equipment item:
- **Tag**: RTU-1, AHU-2, EF-3, MAU-1, UH-1, FCU-1, HP-1
- **Type**: Rooftop Unit, Air Handler, Exhaust Fan, Make-Up Air, Unit Heater, Fan Coil, Split System, Mini-Split, Heat Pump, ERV/HRV, VRF
- **Location**: Roof/mech room/ceiling space + grid ref or room + mounting (curb, pad, ceiling-hung, wall)
- **Cooling**: Tons or MBH, type (DX, chilled water), refrigerant (R-410A, R-32, R-454B)
- **Heating**: MBH or KW, type (gas, electric, heat pump, hydronic)
- **Airflow**: CFM, external static pressure (in. w.c.)
- **Efficiency**: SEER, EER, AFUE, COP, HSPF
- **Electrical**: Voltage/phase/Hz, MCA, MOCP, FLA, LRA
- **Physical**: Weight (lbs), dimensions (L×W×H), sound rating (dBA), gas connection size
- **Controls**: DDC/standalone, economizer type (dry-bulb/enthalpy/none), VFD (yes/no)
- **Served areas**: Room numbers, zone name, main duct size leaving unit
- **Manufacturer/model**: From submittals if available

**Example**:
```json
{
  "tag": "RTU-1", "type": "rooftop_unit",
  "location": {"grid": "C-D/3-4", "room": "Roof", "mounting": "curb"},
  "cooling": {"tons": 10, "type": "DX", "refrigerant": "R-410A"},
  "heating": {"mbh": 250, "type": "gas"},
  "airflow": {"cfm": 4000, "esp_inwc": 1.5},
  "efficiency": {"seer": 14.3, "afue": 81},
  "electrical": {"voltage": 208, "phase": 3, "hz": 60, "mca": 48, "mocp": 60, "fla": 38, "lra": 190},
  "physical": {"weight_lbs": 1450, "dimensions": "96x60x42", "sound_dba": 72, "gas_conn": "1\""},
  "controls": {"type": "DDC", "economizer": "dry-bulb", "vfd": true},
  "served_rooms": ["101", "102", "103", "104", "105"],
  "manufacturer": null, "model": null,
  "source_sheet": "M-301"
}
```

### Exhaust Fan Schedule

Per fan:
- **Tag**: EF-1, EF-2, etc.
- **Type**: Centrifugal, inline, roof-mounted, wall-mounted, utility set
- **CFM**, static pressure (in. w.c.), HP
- **Voltage/phase**, MCA, MOCP
- **Served rooms/areas**
- **Speed control**: Single-speed, multi-speed, VFD
- **Duct size**: At fan connection

### Diffuser/Grille Schedule

Per device:
- **Tag/type**: CD (ceiling diffuser), RG (return grille), EG (exhaust grille), SD (slot diffuser)
- **Size**: Neck or face dimensions
- **CFM**: Rated airflow
- **Throw pattern**: 1-way, 2-way, 3-way, 4-way, radial
- **Rooms**: Where installed
- **Mounting**: Ceiling, wall, floor, linear slot
- **Served by**: Equipment tag (RTU-1, AHU-2, etc.)

### Ductwork Sizes and Routing

Extract all duct sizes from M-100 plan sheets:
- **Size format**: Rectangular = W×H (e.g., "24×12"), Round = diameter (e.g., "10\" RD")
- **System type**: Supply (S), return (R), exhaust (E), outside air (OA)
- **Material**: Galvanized sheet metal, flex duct, lined, external wrap, fiberglass duct board
- **Main trunk runs**: Trace from each air handler with sizes at key points
- **Branch sizes**: At tees/takeoffs to rooms
- **Insulation**: Internal lined, external wrap, none (note where specified)

### Electrical Panel Schedule (E-300 Series)

**EXTRACT EVERY PANEL — the most critical electrical data.**

Panel header:
- **Designation**: LP-1, PP-2, DP-3, MDP, etc.
- **Location**: Room number or grid reference
- **Voltage/phase/wires**: 208/120V 3ph 4W, 480/277V 3ph 4W, etc.
- **Main breaker**: Amps
- **Bus rating**: Amps (may differ from main breaker)
- **Fed from**: Which upstream panel/switchboard
- **Mounting**: Surface, flush, NEMA type
- **AIC rating**: kAIC (interrupting capacity)

Per circuit:
- **Number**: 1, 2, 3... (odd = left side, even = right side)
- **Breaker size**: Amps
- **Poles**: 1, 2, or 3
- **Load description**: "Lighting Rooms 101-103", "RTU-1", "Receptacles 201"
- **Connected VA**: Load in volt-amps
- **Phase**: A, B, or C

Panel totals:
- **Connected VA** per phase (A, B, C)
- **Demand VA** (with demand factors applied)
- **Spare breakers**: Count of installed but unused breakers
- **Space slots**: Count of empty slots with no breaker

### Single-Line Diagram (E-001 or E-100)

Complete power distribution hierarchy:
- **Utility service**: Voltage, phase, service entrance size (amps)
- **Main switchboard/MDP**: Rating, main breaker
- **Transformers**: kVA, primary/secondary voltage, impedance
- **Distribution panels**: Fed-from tree (MDP → Panel A → Sub-panel A1)
- **ATS (Automatic Transfer Switch)**: Rating, transfer time, bypass
- **Generator**: KW, fuel type (diesel/natural gas), voltage, phase, enclosure, run time
- **UPS**: kVA, battery runtime, load served

### Lighting Fixture Schedule (E-200 Series)

**EXTRACT ALL FIXTURE TYPES**:

Per fixture type:
- **Mark**: A, B, C or Type 1, Type 2
- **Description**: Recessed LED troffer, pendant, wall sconce, etc.
- **Manufacturer/catalog**: From submittals if available
- **Wattage**: Per fixture
- **Lumens**: Initial lumens per fixture
- **Color temperature**: K (3000K, 3500K, 4000K, 5000K)
- **CRI**: Color rendering index (typically 80-90+)
- **Mounting**: Recessed, surface, pendant, wall, track
- **Lens type**: Frosted, prismatic, parabolic, open, opal
- **Voltage**: 120V, 277V, etc.
- **Dimming**: 0-10V, DALI, Lutron, non-dimming
- **Emergency battery**: Yes/no, duration (90 min typical)
- **Controls**: Switched, dimmed, occupancy sensor, daylight harvesting
- **Total quantity**: Count from schedules or plan count

**[RENDERING DATA] - Visual Appearance**:
- **Fixture appearance/style**:
  - "Recessed 2x2 flat panel LED" (clean, flush-mount appearance)
  - "4-foot linear LED strip" (continuous line light)
  - "Round downlight 4\" diameter" (traditional recessed can)
  - "Pendant with frosted shade" (decorative hanging fixture)
  - "LED edge-lit wall sconce" (contemporary decorative)
- **Fixture color/housing**:
  - "White trim ring", "Brushed nickel finish", "Matte black housing", etc.
- **Lens type**: Frosted, prismatic, open, parabolic, clear, opal
- **Decorative fixtures** (if any):
  - Pendant style: modern, transitional, traditional, industrial, etc.
  - Sconce style: direct, indirect, up-down light, etc.
  - Finish options: chrome, bronze, nickel, copper, etc.

**Example**:
```json
{
  "mark": "Type A",
  "description": "Recessed 2x4 LED troffer",
  "manufacturer": null, "catalog_number": null,
  "wattage": 40, "lumens": 5000, "cct_k": 4000, "cri": 85,
  "mounting": "Recessed in ACT", "lens_type": "Frosted acrylic",
  "voltage": "277V", "dimming": "0-10V", "emergency_battery": false,
  "controls": "Occupancy sensor + daylight harvesting",
  "quantity": 48,
  "rendering_data": {
    "appearance": "Recessed 2x4 flat panel LED",
    "trim_finish": "White trim ring",
    "lens_type": "Frosted acrylic"
  }
}
```

### Receptacle/Device Counts (E-100 Power Plans)

Count per room from power plans:
- **Duplex receptacles**: Standard 120V
- **GFCI receptacles**: Wet locations, countertops
- **Dedicated circuits**: Equipment-specific outlets
- **240V outlets**: Dryers, welders, special equipment
- **Data/telecom outlets**: RJ45 jacks
- **Special devices**: Card readers, cameras, motion sensors, occupancy sensors

### Plumbing Fixture Schedule (P-400 Series)

**EXTRACT EVERY FIXTURE**:

Per fixture:
- **Tag**: WC-1, LAV-1, SK-1, UR-1, MOP-1, DF-1, EW-1, FD-1
- **Type**: Water Closet, Lavatory, Sink, Urinal, Mop Sink, Drinking Fountain, Eye Wash, Floor Drain
- **Manufacturer/model**: Full catalog info from submittals
- **Mounting**: Floor-mounted, wall-hung, countertop, undermount, drop-in, pedestal
- **Connection sizes**: Hot supply, cold supply, waste
- **Faucet type**: Manual lever, sensor (battery/hardwired), metering, foot pedal
- **ADA compliance**: Yes/no (must be explicitly noted)
- **Flow rate**: GPM for faucets/showers, GPF for flush fixtures
- **Flush valve type**: Manual, sensor, dual-flush
- **Quantity**: Total count across project

**[RENDERING DATA] - Visual Appearance**:
- **Fixture color**: "White", "Bone", "Biscuit", "Stainless", "Black", etc.
- **Faucet finish**: "Polished chrome", "Brushed nickel", "Oil-rubbed bronze", "Matte black"
- **Sink style**: Undermount, drop-in, vessel, wall-hung, pedestal
- **Accessory finishes**: Towel bars, grab bars, soap dispensers — finish and material

**Example**:
```json
{
  "tag": "WC-1", "type": "water_closet",
  "manufacturer": "American Standard", "model": "Afwall 3351.101",
  "mounting": "wall-hung", "flush_type": "sensor", "flush_gpf": 1.28,
  "connections": {"cold": "1\"", "waste": "4\"", "vent": "2\""},
  "ada": true, "quantity": 12,
  "rendering_data": {
    "fixture_color": "White vitreous china",
    "flush_valve_finish": "Polished chrome"
  }
}
```

### Water Heater / Boiler Schedule

Per unit:
- **Tag**: WH-1, BLR-1, etc.
- **Type**: Storage tank, tankless, heat pump, indirect, boiler
- **Capacity**: Gallons (storage), GPH recovery, BTU/hr input
- **Efficiency**: UEF, thermal efficiency %
- **Fuel**: Gas, electric, heat pump, solar-assist
- **Electrical**: Voltage, phase, KW (if electric)
- **Vent type**: Direct vent, power vent, atmospherically vented
- **Location**: Room, grid reference
- **Served areas**: Domestic hot water zones, heating loops

### Pipe Sizing and Routing

From plans and riser diagrams:
- **System**: DCW (domestic cold), DHW (domestic hot), sanitary, vent, storm, gas, medical gas, compressed air
- **Size**: Nominal pipe diameter
- **Material**: Copper, CPVC, PEX, PVC, cast iron, HDPE, black steel, stainless steel
- **Main runs**: From source through building, noting size transitions
- **Insulation**: Fiberglass, elastomeric, heat trace (where noted)

### Fire Protection

- **System type**: Wet, dry, pre-action, deluge, combined standpipe
- **Design standard**: NFPA 13, 13R, or 13D
- **Hazard classification**: Light, Ordinary Group 1/2, Extra Group 1/2
- **Riser**: Location (room/grid), size (pipe diameter)
- **FDC**: Location (face of building), type (Siamese/Storz), size
- **Head schedule**:
  - Type: Pendant, upright, sidewall, concealed, ESFR
  - Temperature rating: 155°F (ordinary), 200°F (intermediate), 286°F (high)
  - K-factor: 5.6, 8.0, 11.2, 14.0, 25.2
  - Coverage: SF per head
  - Finish: White, chrome, brass, custom color
- **Fire pump** (if present): GPM, PSI, HP, driver (electric/diesel), jockey pump
- **Standpipe**: Type (I, II, III), location, hose connections

---

## CIVIL DRAWINGS (C-series)

### Site Layout
- **North arrow** orientation
- **Access points**: from which streets
- **Laydown areas**: coordinates or grid references, size
- **Trailer locations**: coordinates, count
- **Crane pad locations** or pick zones
- **Dumpster locations**
- **Parking**: construction vs. permanent, space counts

### Grading & Elevations

**EXTRACT SPOT ELEVATIONS**:
- **FFE (Finished Floor Elevation)**: Building floor elevation
- **Building corners**: Existing and proposed grades
- **Entrances, loading docks, ramps**
- **Parking lot high/low points**
- **Slopes**: Parking (1-5%), sidewalks (max 2%), ramps (ADA 8.33% max)

**Example**:
```
FFE = 856.50'
NW corner = 855.00' (proposed grade)
SE corner = 854.20' (proposed grade)
Parking slope = 2% toward storm drains
```

### Storm Drainage

**EXTRACT PIPE DATA**:
For each pipe run:
- Material (RCP, HDPE, PVC)
- Diameter (12", 18", 24")
- Slope (%)
- Invert elevations IN and OUT
- Rim elevation of structures

**Example**:
```
SD-1 to SD-2: 12" RCP, 50' long, 1.0% slope
  At SD-1: Inv OUT = 844.50', Rim = 856.20'
  At SD-2: Inv IN = 844.00', Rim = 855.80'
```

---

## Output Structure

Structure extracted data for project-data storage:

```json
{
  "grid_lines": {...},
  "floor_levels": [...],
  "room_schedule": [...],
  "finish_schedule": [...],
  "door_schedule": [...],
  "window_schedule": [...],
  "casework_schedule": [...],
  "mep_equipment": {
    "hvac": [...],
    "electrical_panels": [...],
    "lighting": [...],
    "plumbing_fixtures": [...],
    "fire_protection": {...}
  },
  "structural_specs": {
    "concrete": [...],
    "rebar": {...},
    "steel": {...},
    "anchor_bolts": {...}
  },
  "site_layout": {...},
  "grading": {...},
  "utilities": {
    "storm": [...],
    "sanitary": [...],
    "water": [...]
  },
  "visual_rendering_data": {
    "exterior_appearances": [
      {
        "elevation": "South",
        "cladding": {...},
        "roof": {...},
        "trim": {...},
        "accents": {...}
      }
    ],
    "interior_finishes": {
      "paint_colors": [...],
      "flooring_products": [...],
      "tile_details": [...],
      "ceiling_products": [...]
    },
    "door_and_frame_finishes": [...],
    "window_frame_colors": [...],
    "lighting_appearance": [...],
    "fixture_colors": [...]
  }
}
```

---

## Extraction Efficiency Tips

1. **Use sheet index first**: Identify which sheets exist before reading
2. **Read schedules systematically**: Go row by row, extract all data
3. **Extract general notes carefully**: These contain the specific values (PSI, tolerances, etc.)
4. **Visual data on elevations**: Study elevation sheets for cladding color, trim details, and accent materials
5. **Cross-reference**: Link room numbers to finishes to spec sections
6. **Flag missing data**: Note if schedule exists but is incomplete
7. **Track confidence**: Flag inferred vs. explicit data
8. **Rendering data priority**: Mark visual data (colors, materials, finishes) as HIGH priority for rendering systems

---

## Integration with Daily Reports

Extracted plan data enables:

- **Location references**: "Formed footings at Grids C-D, 3-4"
- **Room tracking**: "Completed drywall in Rooms 101-105 (5 of 47 total)"
- **Finish tracking**: "Installed VCT per finish schedule in Nurse Station"
- **Equipment tracking**: "RTU-3 set on roof, connected to ductwork"
- **Spec verification**: "Placed 4,000 PSI concrete per structural notes"
- **Coordination**: "Electrical panel LP-1 installed in Room 112 per plans"

---

## Visual Rendering Integration

Extracted visual/aesthetic data enables:

- **3D model texturing**: Wall cladding colors, roof material appearance, trim finishes
- **Interior visualization**: Paint colors, flooring products, ceiling tiles, door finishes
- **Fixture rendering**: Lighting fixture styles, plumbing fixture colors, hardware finishes
- **Design documentation**: Presentation renderings showing actual specified materials
- **Color scheme verification**: Confirm paint codes, tile colors, and hardware finishes match design intent
- **Material procurement tracking**: Cross-reference rendered colors with actual product submissions

---

## Reflected Ceiling Plan (RCP) Extraction Rules

RCPs are a critical sheet type that completes the three-dimensional spatial model. Without RCP extraction, the overhead plane data (ceiling heights, fixture placement, HVAC devices, sprinkler coverage, material zones) is missing from the project intelligence.

### Sheet Identification Patterns

**Primary identifiers** (match any):
- Sheet number prefix: `RCP`, `A-5xx` (A-501, A-502, A-510, etc.)
- Sheet number suffix: `-RCP` (e.g., A-101-RCP, A-201-RCP)
- Title block text: "Reflected Ceiling Plan", "RCP", "Ceiling Plan"
- Sheet index classification: Sheets listed under "Reflected Ceiling Plans" or "Ceiling Plans"

**Secondary signals** (confirm classification):
- Dashed grid lines (RCPs show structural grid as dashed reference lines)
- Ceiling height callouts in rooms (e.g., "9'-0\" AFF", "CLG @ 10'-0\"")
- Fixture symbols without floor-level furniture/equipment
- Ceiling material boundary hatching or tagging
- Note stating "This is a reflected view -- mirror image of actual ceiling"

**Scale**: RCPs typically match the floor plan scale (1/8" = 1'-0" for full-building, 1/4" = 1'-0" for enlarged areas). Confirm scale from title block or scale bar.

### Symbol Identification Library

#### Light Fixtures
| Symbol Description | Fixture Type | Typical Mark |
|-------------------|-------------|-------------|
| Rectangle 2'x4' (solid outline, X inside or parallel lines) | 2x4 Recessed LED Troffer | Type A |
| Rectangle 2'x2' (solid outline, X inside) | 2x2 Recessed LED Troffer | Type B |
| Small circle (3-4" diameter) with dot center | Recessed Downlight (can light) | Type C |
| Circle with arrow pointing to wall | Wall Sconce / Wall Washer | Type D |
| Rectangle with "EXIT" text or triangle-person symbol | Exit Sign (with or without emergency) | Type EX |
| Circle with "EM" or battery symbol | Emergency Light (battery unit) | Type EM |
| Rectangle with single line through center | Linear LED Strip / Pendant | Type E |
| Elongated rectangle (6'-8' long, narrow) | 4-foot or 8-foot Linear LED | Type F |
| Circle with radiating lines | Surface-mount round fixture | Type G |
| Triangle or diamond shape | Specialty / Decorative fixture | Varies |

#### HVAC Ceiling Devices
| Symbol Description | Device Type | Extraction Data |
|-------------------|------------|-----------------|
| Square with X pattern (typically 24"x24") | Supply Air Diffuser (square) | Size, CFM if noted |
| Circle with concentric rings | Round Supply Diffuser | Diameter, CFM if noted |
| Rectangle with parallel bars | Return Air Grille (bar type) | Size (WxH) |
| Square with grid/egg-crate pattern | Return Air Grille (egg crate) | Size (WxH) |
| Long narrow rectangle with hash marks | Linear Slot Diffuser | Length, slot count |
| Square with "EX" or arrow-out symbol | Exhaust Grille | Size, CFM |
| Rectangle with "RA" text | Return Air Transfer | Size |
| Small square with "FD" | Fire Damper (at rated wall/floor) | Rating (1-hr, 2-hr) |

#### Fire Protection
| Symbol Description | Device Type | Extraction Data |
|-------------------|------------|-----------------|
| Circle with "S" or sprinkler symbol (pendant shape) | Pendant Sprinkler Head | Coverage area, type |
| Circle with "SC" | Concealed Sprinkler Head | Coverage area, concealed plate finish |
| Circle with "SW" | Sidewall Sprinkler Head | Coverage area, throw direction |
| Circle with "U" | Upright Sprinkler Head | Coverage area (above ceiling) |

### Ceiling Material Zone Extraction

**Material zone identification**:
- Look for boundary lines (usually dashed or dot-dash) separating ceiling material areas
- Each zone should be labeled with a material tag or ceiling type designator
- Cross-reference zone labels to the finish schedule and/or ceiling legend on the RCP sheet

**Standard ceiling material types**:
| Tag / Abbreviation | Material | Typical Specification |
|-------------------|----------|----------------------|
| ACT, ACT-1, CT-1 | Acoustical Ceiling Tile Type 1 | Standard office/corridor -- e.g., Armstrong Sahara 2x2 |
| ACT-2, CT-2 | Acoustical Ceiling Tile Type 2 | Moisture-resistant -- restrooms, kitchens -- e.g., Armstrong Ceramaguard |
| ACT-3, CT-3 | Acoustical Ceiling Tile Type 3 | High-NRC -- conference rooms, therapy rooms |
| GWB, GYP, DW | Gypsum Wallboard Ceiling | Painted drywall -- lobbies, feature areas |
| EXP, EXPOSED | Exposed Structure | Painted exposed deck/joists -- industrial/modern aesthetic |
| WD, WOOD | Wood Ceiling | Wood slat, panel, or plank ceiling -- specialty areas |
| MTL, METAL | Metal Ceiling | Linear metal, metal panel -- lobbies, canopies |
| CLOUD, RAFT | Acoustic Cloud/Raft | Suspended panels -- open office, collaborative spaces |
| CLR, OPEN | Open to Structure (no ceiling) | Mechanical rooms, storage, unfinished spaces |

### Height Transition Extraction

**Soffit/bulkhead detection**:
- Soffits appear as dashed rectangles within a room, labeled with a lower height (e.g., room ceiling at 9'-0" but soffit at 7'-6")
- Bulkheads at corridor-to-room transitions create ceiling drops -- look for height change at door headers
- Step-ups (e.g., "Ceiling steps from 9'-0\" to 12'-0\" at grid line C") shown with a transition line and heights on each side

**Extraction output**:
```json
{
  "rcp_height_transitions": [
    {
      "room": "103",
      "transition_type": "soffit",
      "main_ceiling_height": "9'-0\"",
      "soffit_height": "7'-6\"",
      "soffit_dimensions": "2'-0\" wide x 8'-0\" long",
      "soffit_location": "Over door frames along corridor wall",
      "purpose": "Conceal ductwork run"
    },
    {
      "room": "120",
      "transition_type": "step_up",
      "low_ceiling": "9'-0\"",
      "high_ceiling": "12'-0\"",
      "transition_at": "Grid line C",
      "purpose": "Lobby volume increase"
    }
  ]
}
```

### RCP Cross-Reference Rules

After extracting RCP data, validate against other extracted data:

| RCP Data | Cross-Reference Against | Validation Rule |
|----------|------------------------|-----------------|
| Room numbers on RCP | Floor plan room_schedule | Every RCP room must exist in floor plan room list |
| Ceiling heights on RCP | Finish schedule ceiling column | Heights must match; flag discrepancies |
| Grid lines on RCP | Structural grid from S-series | Grid labels and spacing must align |
| Fixture type marks | Lighting fixture schedule | Every mark on RCP must appear in fixture schedule |
| Fixture counts per room | Lighting fixture schedule totals | Sum of all rooms should approximate schedule total |
| Sprinkler coverage | Fire protection drawings (FP-series) | RCP sprinkler layout is reference only -- FP governs |
| Ceiling material tags | Finish schedule ceiling type | Material designations must match |
| Supply/return counts | Mechanical equipment schedule (CFM per room) | Diffuser count should support required CFM |

**Discrepancy handling**: When RCP data conflicts with another source, flag the conflict using the Specification Conflict Detection workflow (see SKILL.md). Typical RCP conflicts include ceiling height on RCP not matching the finish schedule, fixture counts on RCP not matching the fixture schedule total, and ceiling material tags on RCP using different designators than the finish schedule.

---

## Window Schedule Extraction -- Enhanced Depth

The existing window schedule extraction captures basic data (mark, size, type, glazing, U-value, frame material, rendering data). This section adds depth comparable to the door schedule extraction, which is significantly more detailed.

### Enhanced Window Schedule Fields

For EVERY window in the schedule, extract:

**Identification and Sizing**:
- **Window mark**: W-101, W-102, etc. (or A, B, C designators)
- **Size (nominal)**: Width x Height (e.g., "3'-0\" x 4'-6\"")
- **Rough opening (RO)**: Width x Height (typically 1/2" to 1" larger than nominal each direction)
- **Quantity**: How many of this type across the project
- **Location(s)**: Which rooms or elevations use this window type

**Performance Specifications**:
- **Glazing configuration**: Single, double (insulated), triple
- **Glass type**: Clear, low-E, tinted (bronze, gray, green), laminated, tempered, wired
- **U-value**: Overall window U-value (lower = better insulation)
- **SHGC (Solar Heat Gain Coefficient)**: Typically 0.25-0.40 for commercial
- **VT (Visible Transmittance)**: Light transmission percentage
- **STC (Sound Transmission Class)**: If acoustically rated
- **Impact rating**: If in hurricane/wind zone (ASCE 7 missile impact)

**Frame and Hardware**:
- **Frame material**: Aluminum, vinyl, fiberglass, wood, clad wood, steel
- **Frame finish**: Anodized (clear, dark bronze, black), painted, powder coat, factory finish
- **Frame thermal break**: Yes/no, type (pour and debridge, thermal strut)
- **Operation type**: Fixed, single-hung, double-hung, casement, awning, hopper, sliding, pivot
- **Hardware**: Lock type, operator (crank, push-out, lever), limit stops, screens
- **Screen type**: Full, half, removable, fixed, no screen

**Fire Rating** (where applicable):
- **Fire-rated glazing**: Wired glass, ceramic glass (Firelite, SuperLite), glass block
- **Fire rating**: 20-min, 45-min, 60-min, 90-min
- **Frame fire rating**: Matching frame assembly rating
- **Location trigger**: Rated corridors, stairwells, exterior openings near property line

**Accessibility and Code**:
- **Operable sill height**: ADA requires operable portion within reach range
- **Emergency egress**: If window serves as emergency egress, minimum clear opening dimensions (5.7 SF, 20" width, 24" height per IRC)
- **Guard/fall protection**: Windows below 36" sill may require guarding or tempered glazing

### Window Schedule Table Extraction Rules

When parsing window schedules from plan sheets:
1. Read the complete table header row to identify all columns
2. Extract every row, including rows that say "same as above" or use ditto marks
3. For grouped entries (e.g., "W-101 through W-108"), expand to individual entries with shared properties
4. Cross-reference window marks to elevation drawings for visual confirmation
5. Cross-reference to spec Division 08 51 00 for performance values not on the schedule

**Output format**:
```json
{
  "window_schedule_enhanced": [
    {
      "mark": "W-101",
      "size": "3'-0\" x 4'-6\"",
      "rough_opening": "3'-0.5\" x 4'-6.5\"",
      "qty": 12,
      "locations": ["Rooms 201-208 (north wall)", "Rooms 210-213 (east wall)"],
      "operation": "Fixed",
      "frame_material": "Aluminum",
      "frame_finish": "Dark bronze anodized",
      "thermal_break": true,
      "glazing": "1\" insulated, clear/clear, low-E on surface 2",
      "u_value": 0.28,
      "shgc": 0.32,
      "vt": 0.52,
      "fire_rated": false,
      "hardware": "N/A (fixed)",
      "screen": "None",
      "rendering_data": {
        "frame_color": "Dark bronze anodized",
        "glass_appearance": "Clear with slight green/blue tint from low-E",
        "mullion_pattern": "Single lite, no divisions",
        "sill_detail": "Aluminum sill, sloped, bronze to match frame",
        "head_trim": "Aluminum head flashing, bronze anodized"
      }
    },
    {
      "mark": "W-201",
      "size": "3'-0\" x 5'-0\"",
      "rough_opening": "3'-0.5\" x 5'-0.5\"",
      "qty": 4,
      "locations": ["Stairwell 1 (east)", "Stairwell 2 (west)"],
      "operation": "Fixed",
      "frame_material": "Steel",
      "frame_finish": "Painted white",
      "thermal_break": false,
      "glazing": "1/4\" wired glass, single pane",
      "u_value": null,
      "shgc": null,
      "vt": null,
      "fire_rated": true,
      "fire_rating": "90-min",
      "hardware": "N/A (fixed)",
      "screen": "None",
      "rendering_data": {
        "frame_color": "White painted steel",
        "glass_appearance": "Wired glass, visible diamond wire pattern",
        "mullion_pattern": "Single lite",
        "sill_detail": "Steel sill, painted white",
        "head_trim": "Steel frame head, painted white"
      }
    }
  ]
}
```

---

## EXTERIOR ELEVATION MATERIALS (A-200 series — Data Source: Pass 12 / Pass 4H)

Extract cladding and finish material zones from exterior elevation sheets, organized per building face.

### Per-Face Material Zone Data

**ALWAYS EXTRACT per face (NORTH/SOUTH/EAST/WEST)**:
- **Material type**: Metal panel, masonry, EIFS, stucco, lap siding, stone veneer, curtain wall, storefront, CMU
- **Color/finish**: Color name, paint code (e.g., SW7036), Kynar/PVDF finish designation
- **Manufacturer code**: Nucor panel profile, brick type code, EIFS system name
- **Coverage area**: Approximate percentage or SF of face
- **Grade line elevation**: Finished grade at each face from F.G. or GRADE callouts
- **Window/door positions**: Mark numbers (W-xxx, D-xxx, SF-xxx) with rough opening sizes, sill heights, head heights

### Height Data from Elevation Dimensioning
- Grade-to-eave height
- Grade-to-ridge height (if applicable)
- Grade-to-parapet height (if applicable)
- Floor-to-floor at exterior walls
- Foundation exposure (grade to top of foundation)

### Cross-Checks
- Material zones should cover ~100% of each face (gap = missing zone)
- Grade-to-eave from elevation must match building section heights (±6")
- Window/door marks must match door/window schedule entries
- Metal panel colors should match specification section 074213

### Downstream Consumers
| Consumer | Data Used |
|----------|-----------|
| Rendering Generator | Material zones, colors, manufacturer codes for photorealistic renders |
| Estimating | Material areas per face for quantity takeoffs |
| Submittal Intelligence | Manufacturer codes for submittal compliance checking |
| Quality Management | Color/finish specs for field verification |

---

## ACCESSIBILITY DATA (A-100 code plans, A-500 details — Data Source: Pass 12 / Pass 4H)

Extract ADA/accessibility compliance data from life-safety plans, code plans, and detail sheets.

### Accessible Routes
- **Corridor widths**: Minimum clear width (36" min typical, 44" in healthcare)
- **Door clearances**: Maneuvering clearance at each accessible door (pull side/push side dimensions)
- **Turning radius**: 60" diameter turning space locations
- **Route continuity**: Verify connected path from accessible entrance to all required spaces
- **Level changes**: Thresholds (max 1/2"), ramps, elevators along route

### ADA Restroom Compliance
- **Grab bar positions**: Side wall (42" long, 12" from rear wall), rear wall (36" long, centered)
- **Toilet clearance**: 60" min clear floor space, centerline 16-18" from side wall
- **Lavatory clearance**: 30" wide × 48" deep clear floor, knee clearance 27" AFF min
- **Turning radius**: 60" turning circle or T-shaped turning space
- **Fixture mounting heights**: Toilet 17-19" AFF, lavatory rim 34" max, mirror 40" max to bottom

### Ramps
- **Slope ratio**: Max 1:12 (8.33%), cross slope max 1:48 (2%)
- **Landing dimensions**: 60" min at top/bottom, 60"×60" at direction changes
- **Handrail details**: 34-38" height, 12" extension at top, extension at bottom = ramp run or 12" min
- **Rise per run**: Max 30" rise per run segment

### Signage
- **Room sign types**: Tactile/braille at permanent rooms, visual at non-permanent
- **Mounting height**: Tactile signs 48-60" AFF to baseline of lowest tactile character
- **Locations**: Latch side of door, 18" min clearance if door has closer

### Accessible Parking
- **Van-accessible spaces**: Count, 11' wide + 5' access aisle (or 8' + 8' universal)
- **Standard accessible spaces**: Count, 8' wide + 5' access aisle
- **Signage**: ISA sign at 60" min AFF, van spaces marked "Van Accessible"
- **Route to entrance**: Max slope 1:48 cross, 1:20 running, marked path

### Counters
- **ADA counter segments**: Location, length (36" min), height (28-34" AFF)
- **Knee clearance**: 27" high × 30" wide × 19" deep min
- **Approach type**: Forward or parallel

### Cross-Checks
- Every accessible restroom must have grab bars, clearances, and proper fixture heights
- Accessible route widths ≥ code minimum (36" standard, 44" healthcare E occupancy)
- Ramp slopes ≤ 1:12 with landings at every 30" of rise
- Parking counts per IBC Table 1106.1 (MOSC: 133 occupants → check required count)
- Counter heights match ADA 902 requirements (28-34" work surface)

### Downstream Consumers
| Consumer | Data Used |
|----------|-----------|
| Quality Management | Clearance dimensions for field verification checklists |
| Inspection Tracker | ADA compliance items for final inspection checklist |
| Punch List | Non-compliant items flagged during walkthrough |
| Estimating | Grab bars, signage, ramp materials for procurement |

---

## HATCH PATTERN REFINEMENT AND KEYNOTES (All A/S-series — Data Source: Pass 13 / Pass 4I)

This is a refinement pass that operates across all plan sheet types. It improves existing material zone data (Pass 5) and extracts keynote/general note intelligence that links drawing annotations to specifications.

### Hatch Pattern Refinement

**Purpose:** Pass 5 uses generic texture analysis (Gabor filters + LBP entropy) which frequently misclassifies similar patterns. This refinement uses Hough line analysis within each zone to measure actual line angles and spacing, then maps those to AIA/ANSI standard patterns.

**Standard Construction Hatch Patterns:**

| Pattern | Angles | Density (LPI) | Material | ANSI Code |
|---------|--------|---------------|----------|-----------|
| Single diagonal | 45° | 4-8 | Steel (section cut) | ANSI31 |
| Cross-hatch | 45° + 135° | 4-8 | Concrete | AR-CONC |
| Dense diagonal | 45° | >10 | Sand/gravel | AR-SAND |
| Horizontal only | 0° | 2-4 | Wood (with-grain) | ANSI37 |
| Grid | 0° + 90° | 2-4 | Wood (end-grain) | — |
| Random dots/stipple | Multiple | 1-3 | Earth fill | EARTH |
| Wavy lines | Variable | 2-4 | Insulation | INSUL |
| Running bond | 0° + 90° staggered | — | Masonry/brick | BRICK |

**Refinement Rules:**
1. If the sheet contains a material legend, legend labels override angle-based classification
2. If a leader line or adjacent text label identifies the material, the label overrides angle-based classification
3. Section-cut context (A-300/S-300 sheets) implies cut-through material; plan-view context implies surface material
4. Hatch density disambiguates similar angle patterns (concrete vs. sand, both 45° but different LPI)

### Keynote Extraction

**Keynote Types:**
- **Bubble keynotes**: Small circles, diamonds, or hexagons (6-25px radius) containing 1-2 digit numbers, connected by leader lines to drawing elements
- **Inline keynotes**: Numbered text callouts without enclosing shapes (less common, harder to detect)
- **Keynote schedules**: Two-column tables (Number | Description) in the notes zone of a sheet, or on a dedicated keynote sheet (typically A-001 or the first architectural sheet)

**What to extract per keynote:**
1. Keynote number
2. Position on the drawing (bubble center x,y)
3. Leader line endpoint (what the keynote points to)
4. Element it references (wall type, door, material, etc.)
5. Description from the keynote schedule
6. Spec section reference embedded in the description

### General Notes

**ALWAYS EXTRACT** from general notes blocks:
- Note number (1, 2, 3... or A, B, C...)
- Full text of each note
- Category classification:
  - **dimensions**: Notes about measurement conventions ("all dimensions to face of stud")
  - **materials**: Notes specifying materials or products
  - **installation**: Notes about installation methods
  - **code**: Notes referencing building code, ADA, fire rating requirements
  - **coordination**: Notes requiring field verification or trade coordination
  - **general**: Everything else
- CSI spec section references within the note text

### Cross-Checks
- Every keynote bubble on the drawing should have a matching schedule entry (orphan bubbles = incomplete keynote schedule)
- Hatch zones with legend matches should have `confidence: "high"`
- General note spec references should exist in the spec reference index from Pass 8
- Material consistency: Same material should use the same hatch pattern across all sheets (flag conflicts)

### Downstream Consumers
| Consumer | Data Used |
|----------|-----------|
| Estimating | Refined material zones for accurate quantity takeoffs |
| Quality Management | Keynote descriptions for inspection checklist generation |
| Submittal Intelligence | Spec section refs from keynotes for submittal compliance |
| Rendering Generator | Accurate material types for photorealistic rendering |
| Field Reference | General notes categorized for quick field lookup |
| Drawing Control | Keynote completeness for drawing QA/QC |
