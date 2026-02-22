# Compliance - Deep Extraction Guide

Extract specific requirements from geotechnical reports, SWPPP documents, environmental compliance records, permits, safety plans, and inspection documents. Compliance documents define the legal and engineering constraints that govern every activity on the project — missing a single requirement can trigger stop-work orders, fines, or structural failure.

---

## Extraction Priority Matrix

| Priority | Document Type | Why It Matters | Completeness Target |
|----------|--------------|----------------|---------------------|
| **CRITICAL** | Geotechnical report — bearing capacity and foundation recommendations | Foundation design depends on these values; wrong numbers = structural failure | 100% of all recommendations |
| **CRITICAL** | SWPPP — BMP schedule and inspection triggers | Regulatory violation = project shutdown, fines up to $50K/day | 100% of all BMPs and triggers |
| **CRITICAL** | Building permit conditions — special inspections (IBC Ch. 17) | Work without required inspection = tear-out or legal liability | 100% of all conditions |
| **CRITICAL** | Asbestos/lead survey results | Worker safety; OSHA violations for uncontrolled exposure | 100% of all positive results |
| **HIGH** | Geotechnical report — earthwork and compaction requirements | Subgrade failure delays schedule by weeks; rework is expensive | 100% of all requirements |
| **HIGH** | Environmental permits — wetland delineation, ESA findings | Violating boundary = federal enforcement action | 100% of all restrictions |
| **HIGH** | Grading permit conditions | Exceeding permitted cut/fill or operating outside hours = stop-work | 100% of all conditions |
| **HIGH** | Fire department conditions | Failed fire inspection blocks occupancy | 100% of all conditions |
| **MEDIUM** | Geotechnical report — laboratory test results | Supports engineering decisions; not needed daily | 100% if provided |
| **MEDIUM** | SWPPP — NOI/NOT tracking | Administrative but required for permit closure | 100% |
| **MEDIUM** | Noise/vibration limits | Affects scheduling of certain operations | 100% if applicable |
| **LOW** | Phase I ESA (no RECs found) | File for record; no action required | Summary only |
| **LOW** | Endangered species — no species present | File for record | Summary only |

---

## GEOTECHNICAL REPORT DEEP EXTRACTION

Geotechnical reports are the foundation (literally) of every structural and sitework decision. A thorough extraction prevents the most expensive category of construction errors: foundation failures and earthwork rework.

### Boring Log Data

For **EVERY boring** in the report, extract a complete record. Most geotech reports contain 5-20 borings; extract all of them.

**Per-Boring Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Boring ID** | Unique identifier assigned by geotechnical engineer | B-1, B-2, BH-101 |
| **Location** | Coordinates (lat/long), grid reference, or station+offset | N 38.2544, W 85.7638 or Grid A-3 |
| **Surface elevation** | Ground surface elevation at boring location (ft above datum) | 842.5 ft MSL |
| **Groundwater depth** | Depth where water first encountered during drilling | 12.0 ft BGS |
| **Stabilized water level** | Water level after 24-hour equilibrium (more accurate than initial encounter) | 14.5 ft BGS |
| **Boring depth** | Total depth drilled | 35.0 ft BGS |
| **Date drilled** | Date boring was performed | January 5, 2026 |
| **Drilling method** | Technique used (hollow stem auger, rotary wash, etc.) | Hollow stem auger, 4.25" ID |
| **Termination reason** | Why drilling stopped (refusal, design depth reached, etc.) | Auger refusal on limestone at 35 ft |

**EXAMPLE BORING LOG EXTRACT**:
```
Boring B-1:
  Location: Grid A-3 (N 38.2544, W 85.7638)
  Surface elevation: 842.5 ft MSL
  Date drilled: January 5, 2026
  Drilling method: Hollow stem auger, 4.25" ID
  Total depth: 35.0 ft BGS
  Groundwater:
    First encountered: 12.0 ft BGS
    Stabilized (24 hr): 14.5 ft BGS
  Termination: Auger refusal on limestone at 35 ft
```

### Soil Profile Per Boring

For each boring, extract the complete soil stratigraphy. This data drives foundation design, excavation planning, and dewatering decisions.

**Per-Layer Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Depth interval** | Top and bottom of layer (ft BGS) | 0.0 - 3.5 ft |
| **USCS classification** | Unified Soil Classification System code | CL (lean clay) |
| **Description** | Color, texture, inclusions | Brown, stiff, moist lean clay with trace gravel |
| **Moisture** | Moisture condition (dry, moist, wet, saturated) | Moist |
| **Density/Consistency** | For granular: loose/medium/dense; for cohesive: soft/medium/stiff/hard | Stiff |
| **SPT N-values** | Standard Penetration Test blow counts per 6-inch increment | 8/10/12 (N=22) |
| **Sample type** | Split-spoon (SS), Shelby tube (ST), grab, rock core | SS at 5.0 ft |

**EXAMPLE SOIL PROFILE EXTRACT**:
```
Boring B-1 Soil Profile:

Depth (ft)   USCS   Description                           SPT N    Sample
0.0 - 3.5    CL     Brown, stiff, moist lean clay          12      SS @ 2.0'
                     with trace gravel, root traces
3.5 - 8.0    SM     Gray-brown, medium dense, moist        18      SS @ 5.0'
                     silty sand, fine-grained
8.0 - 14.0   CL     Gray, stiff to very stiff,             25      SS @ 10.0'
                     moist lean clay
14.0 - 22.0  SP-SM  Brown, dense, saturated                35      SS @ 15.0', 20.0'
                     poorly-graded sand with silt
22.0 - 35.0  ---    Limestone bedrock                      50/2"   Rock core @ 25.0'
                     (auger refusal)
```

### Groundwater Data

Groundwater is one of the most schedule-impacting discoveries on a construction project. Extract every detail.

**Groundwater Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Depth encountered** | First water during drilling (may not be true static level) | 12.0 ft BGS in B-1 |
| **Stabilized level** | Water level after 24 hours or piezometer reading | 14.5 ft BGS |
| **Seasonal variation** | High/low range noted by engineer | May rise to 10 ft BGS in spring |
| **Perched water** | Isolated water above main water table | Perched at 6 ft in B-3 (clay layer) |
| **Artesian conditions** | Water rising above encountered depth | None noted |
| **Dewatering requirements** | Engineer's recommendation for construction dewatering | Sump pumps adequate for footings; wellpoints for basement |
| **Chemical characteristics** | pH, sulfate content, chloride content (if tested) | Sulfate = 450 ppm (moderate exposure) |

**EXAMPLE GROUNDWATER EXTRACT**:
```
Groundwater Summary:
  Borings with water: B-1, B-2, B-4, B-5 (4 of 6 borings)
  Borings dry: B-3, B-6

  Depth encountered (during drilling):
    B-1: 12.0 ft    B-2: 11.5 ft    B-4: 13.0 ft    B-5: 10.5 ft

  Stabilized levels (24-hour readings):
    B-1: 14.5 ft    B-2: 13.0 ft    B-4: 14.0 ft    B-5: 12.0 ft

  Seasonal variation: Engineer notes water table may rise 3-4 ft
    during spring (March-May) due to rainfall and snowmelt.
    Design groundwater elevation: 10.0 ft BGS (conservative)

  Perched water: B-3 encountered perched water at 6 ft above clay
    layer. Not connected to main water table.

  Dewatering recommendation:
    - Footings (4 ft depth): No dewatering needed
    - Basement (10 ft depth): Wellpoint system required
    - Utility trenches (6-8 ft): Sump pumps adequate

  Chemical: Sulfate at 450 ppm → Type II cement required for
    concrete in contact with soil (moderate sulfate exposure)
```

### Bearing Capacity Recommendations

These are the numbers the structural engineer uses for foundation design. Extract every recommendation exactly as stated.

**Bearing Capacity Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Foundation type** | Spread footings, continuous footings, mat, piers, etc. | Spread footings |
| **Allowable bearing pressure** | PSF (pounds per square foot) at recommended depth | 3,000 PSF |
| **Minimum embedment depth** | How deep below grade the footing must be | 4.0 ft below finished grade |
| **Bearing stratum** | Which soil layer provides the bearing capacity | Stiff lean clay (CL) below 3.5 ft |
| **Settlement estimate** | Total and differential settlement expected | 0.75" total, 0.5" differential |
| **Settlement timeframe** | How long for settlement to occur | 90% within 6 months |
| **Factor of safety** | Safety factor applied to ultimate capacity | FS = 3.0 |
| **Lateral earth pressure** | Active, passive, at-rest coefficients for retaining walls | Ka = 0.33, Kp = 3.0, Ko = 0.50 |
| **Modulus of subgrade reaction** | For slab-on-grade design (PCI per inch) | 150 PCI |
| **Uplift resistance** | If applicable (for anchor bolts, tiedowns) | 1,500 PLF for continuous footings |

**EXAMPLE BEARING CAPACITY EXTRACT**:
```
Foundation Recommendations:

Spread footings:
  Allowable bearing pressure: 3,000 PSF
  Minimum embedment: 4.0 ft below finished grade (below frost + unsuitable fill)
  Bearing stratum: Stiff lean clay (CL), encountered at 3.5 ft in all borings
  Settlement: 0.75" total, 0.50" differential (90% within 6 months)
  Factor of safety: 3.0 applied to ultimate bearing capacity of 9,000 PSF
  Minimum footing width: 24 inches (per structural engineer)

Continuous wall footings:
  Allowable bearing pressure: 2,500 PSF
  Same embedment and bearing stratum as spread footings

Slab-on-grade:
  Modulus of subgrade reaction: 150 PCI (on prepared subgrade)
  Minimum subgrade prep: Remove top 2 ft, replace with compacted structural fill
  Vapor barrier: Required (10-mil minimum, per ACI 302)

Retaining walls (basement walls):
  Active earth pressure coefficient (Ka): 0.33
  Passive earth pressure coefficient (Kp): 3.0
  At-rest coefficient (Ko): 0.50
  Equivalent fluid pressure (active): 40 PCF
  Surcharge: Include 250 PSF for adjacent traffic/equipment
```

### Earthwork Recommendations

Earthwork specs from the geotech report govern excavation, fill, and compaction — the first major activity on most projects.

**Earthwork Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Suitable fill materials** | USCS classifications acceptable for structural fill | CL, SC, SM, SP (no organic, no topsoil) |
| **Unsuitable materials** | Materials that must be removed | OL, OH, PT (organic soils), topsoil, debris |
| **Removal depth** | Depth of unsuitable material to remove | Top 2.0 ft across site |
| **Compaction standard** | Modified or standard Proctor (ASTM D698 or D1557) | 95% of modified Proctor (ASTM D1557) |
| **Lift thickness** | Maximum loose lift before compaction | 8 inches loose (6 inches compacted) |
| **Moisture range** | Acceptable moisture content for compaction | Optimum moisture +/- 2% |
| **Testing frequency** | How often density tests are required | 1 test per 2,500 SF per lift, minimum 1 per day |
| **Subgrade preparation** | Steps before placing structural fill or slabs | Proof-roll with loaded dump truck, scarify 6 inches, recompact |
| **Slope stability** | Maximum cut/fill slopes without shoring | 2H:1V for temporary cuts in clay, 1.5H:1V for sand |
| **Shoring requirements** | When shoring is required vs. open-cut | Excavations > 5 ft in clay require shoring or sloping per OSHA |

**EXAMPLE EARTHWORK EXTRACT**:
```
Earthwork Recommendations:

Unsuitable material removal:
  - Remove top 2.0 ft of existing fill/topsoil across entire building footprint
  - Remove all organic material, debris, frozen soil
  - Proof-roll exposed subgrade with loaded dump truck (min 20 tons)
  - Geotechnical engineer to observe and approve subgrade before fill placement

Structural fill specification:
  Suitable materials: CL, SC, SM, SP, GP (no organics, no topsoil, no frozen material)
  Maximum particle size: 4 inches
  Compaction: 95% of modified Proctor (ASTM D1557)
  Lift thickness: 8 inches loose maximum (compacts to ~6 inches)
  Moisture content: Within +/- 2% of optimum (test each source)
  Testing: 1 nuclear density test per 2,500 SF per lift, minimum 1 per day
  Inspector: Geotechnical firm on-site for all fill placement

Trench backfill:
  Pipe zone: Granular bedding (#57 stone or ODOT #304)
  Backfill above pipe zone: Same as structural fill, 95% modified Proctor
  Testing: 1 test per 200 LF per lift (more restrictive than area fill)

Temporary excavation slopes (OSHA compliant):
  Clay soils: 1H:1V for depths up to 12 ft (Type B soil)
  Sand/silt: 1.5H:1V (Type C soil)
  Shoring required for vertical cuts > 5 ft
  Trench box acceptable for utility trenches
```

### Special Conditions

These are the "watch out" items that can derail a project if missed during extraction.

**Special Condition Fields**:

| Condition | What to Extract | Impact |
|-----------|-----------------|--------|
| **Expansive soils** | Swell potential (%), expansion index, recommended mitigation | Foundation heave, slab cracking, structural damage |
| **Organic layers** | Depth, thickness, extent, removal requirements | Cannot support structures; must be removed |
| **Rock depth** | Depth to rock, rock type, excavation method needed | Blasting or rock hammer required = cost and schedule |
| **Contamination indicators** | Staining, odors, buried debris, historical use | Phase II ESA required; may trigger remediation |
| **Frost depth** | Design frost depth for the region | Footings must be below frost line |
| **Karst/sinkholes** | Presence of voids, solution channels in limestone | May require deep foundations or ground improvement |
| **Fill of unknown origin** | Uncontrolled fill from previous construction/dumping | Must be removed or tested for suitability |
| **High water table** | Groundwater within construction zone | Dewatering, waterproofing, buoyancy considerations |
| **Seismic site class** | ASCE 7 site classification (A through F) | Affects structural design loads |

**EXAMPLE SPECIAL CONDITIONS EXTRACT**:
```
Special Conditions Identified:

1. EXPANSIVE CLAY (CRITICAL)
   Location: B-2 and B-5, depth 4-10 ft
   Swell potential: 3.5% (moderate)
   Expansion index: 62 (moderate-high per ASTM D4829)
   Mitigation: Moisture-condition fill to optimum +2%;
   install void boxes under grade beams; do NOT place slabs
   directly on expansive clay without 12" granular cushion

2. ROCK AT SHALLOW DEPTH
   Location: B-6 (southeast corner of site)
   Rock depth: 8 ft BGS (limestone)
   Impact: Foundation excavation in this area will require
   rock hammer or hoe-ram. No blasting permitted (adjacent structures).
   Budget impact: Add $15,000-$25,000 for rock excavation

3. FILL OF UNKNOWN ORIGIN
   Location: B-3, depth 0-5 ft
   Description: Dark brown fill with brick fragments, glass, concrete rubble
   Recommendation: Remove entirely within building footprint.
   Environmental: No odors or staining observed; Phase II not recommended
   unless contamination suspected during excavation.

4. SEISMIC SITE CLASS
   Classification: Site Class D (stiff soil)
   Per ASCE 7-22 Table 20.3-1
   Based on average SPT N-value in upper 100 ft: N = 24

5. FROST DEPTH
   Design frost depth: 36 inches (per local building code)
   All exterior footings must bear at minimum 36 inches below
   final exterior grade.
```

### Laboratory Test Results

Laboratory tests provide the engineering properties that support the report's recommendations. Extract the summary table.

**Common Lab Tests**:

| Test | Standard | What It Measures | Key Values |
|------|----------|------------------|------------|
| **Atterberg limits** | ASTM D4318 | Liquid limit (LL), plastic limit (PL), plasticity index (PI) | LL, PL, PI values |
| **Grain size distribution** | ASTM D6913 / D422 | Percent gravel, sand, silt, clay; D10, D30, D60 | Gradation curve percentages |
| **Moisture content** | ASTM D2216 | Natural water content (%) | Current moisture vs. optimum |
| **Proctor (compaction)** | ASTM D698 (standard) / D1557 (modified) | Maximum dry density, optimum moisture | MDD (PCF) and OMC (%) |
| **Unconfined compression** | ASTM D2166 | Unconfined compressive strength of cohesive soil | qu in PSF or TSF |
| **Consolidation** | ASTM D2435 | Settlement parameters (Cc, Cr, preconsolidation pressure) | Compression index, time rate |
| **Direct shear** | ASTM D3080 | Shear strength parameters (cohesion, friction angle) | c (PSF), phi (degrees) |
| **California Bearing Ratio** | ASTM D1883 | Subgrade support for pavements | CBR (%) |
| **Swell/expansion** | ASTM D4546 / D4829 | Expansion potential of clay soils | Swell %, expansion index |
| **Chemical (sulfate, pH)** | Various | Soil aggressiveness to concrete and steel | Sulfate (ppm), pH |

**EXAMPLE LAB RESULTS EXTRACT**:
```
Laboratory Test Summary:

Sample B-1 @ 5.0 ft (CL - lean clay):
  Atterberg limits: LL = 38, PL = 18, PI = 20
  Natural moisture: 22.4%
  Grain size: 12% sand, 52% silt, 36% clay
  Unconfined compression: 3,200 PSF (qu)
  Proctor (modified): MDD = 112.5 PCF, OMC = 16.8%

Sample B-2 @ 8.0 ft (CL - lean clay, expansive):
  Atterberg limits: LL = 52, PL = 22, PI = 30 (HIGH plasticity)
  Natural moisture: 28.1%
  Swell potential: 3.5% (ASTM D4546)
  Expansion index: 62 (ASTM D4829)

Sample B-4 @ 15.0 ft (SP-SM - sand with silt):
  Grain size: 78% sand, 18% silt, 4% clay
  Direct shear: c = 0 PSF, phi = 32 degrees

Sulfate testing (composite sample):
  Sulfate content: 450 ppm → Moderate exposure (ACI 318 Table 19.3.1.1)
  Recommendation: Type II cement for all concrete in contact with soil
  pH: 6.8 (neutral, no special protection needed for steel)
```

### Foundation Recommendations

Extract the engineer's final recommendation for foundation type and any special requirements.

**EXAMPLE FOUNDATION RECOMMENDATION EXTRACT**:
```
Foundation Recommendation:

Recommended type: Conventional spread footings on stiff clay (CL)
  - Bearing at 4.0 ft minimum below finished grade
  - Bearing on stiff lean clay (CL) with N > 15

Alternative considered: Drilled piers (caissons) to rock
  - Not required based on bearing capacity analysis
  - Would be needed if settlement exceeds 1.0 inch (not expected)

Special requirements:
  - SE corner (near B-6): Rock excavation required at 8 ft; footings
    may bear directly on rock (higher capacity = 10,000 PSF)
  - Near B-2 and B-5: Void boxes under grade beams due to expansive clay
  - Basement area: Waterproofing membrane required (groundwater within 5 ft
    of basement floor); underslab drainage system recommended

Ground improvement: NOT required for this project

Deep foundations: NOT required for this project

Geotechnical engineer to be on-site for:
  1. Subgrade observation before fill placement
  2. Bearing verification at each footing excavation
  3. Compaction testing during all fill operations
  4. Rock surface verification if encountered
```

---

## SWPPP (STORMWATER POLLUTION PREVENTION PLAN) EXTRACTION

The SWPPP is a legally binding document under the Clean Water Act. Non-compliance triggers regulatory enforcement, project shutdowns, and significant fines. Extract every actionable requirement.

### BMP (Best Management Practice) Schedule

**Per-BMP Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **BMP type** | Name/category of the practice | Silt fence |
| **Specification** | Product or construction standard | ASTM-backed geotextile, 36" height, 6" key-in |
| **Installation location** | Where on site (reference site plan) | Site perimeter — south and east property lines |
| **Quantity** | Linear feet, each, square yards | 1,200 LF |
| **Installation timing** | Before grading, during construction, at stabilization | Before any land disturbance |
| **Responsible party** | Who installs and maintains | GC (earthwork subcontractor) |
| **Maintenance frequency** | How often to inspect and maintain | Weekly + after each rain event > 0.5 inches |
| **Removal timing** | When BMP can be removed | After permanent stabilization of upslope area (70% cover) |

**EXAMPLE BMP SCHEDULE EXTRACT**:
```
BMP Schedule:

BMP #1: Silt Fence
  Type: ASTM-backed geotextile silt fence, 36" height, 6" key-in trench
  Location: South and east property lines (downslope)
  Quantity: 1,200 LF
  Install: BEFORE any land disturbance or grading
  Responsible: ABC Earthwork (earthwork sub)
  Maintenance: Inspect weekly and after each 0.5" rain event.
    Replace/repair when sediment reaches 1/3 height.
  Remove: After permanent stabilization of upslope areas (70% vegetation cover)

BMP #2: Inlet Protection
  Type: Filter fabric wrap with gravel ring (per state DOT standard)
  Location: All 6 storm drain inlets within project limits
  Quantity: 6 EA
  Install: BEFORE any land disturbance
  Responsible: ABC Earthwork
  Maintenance: Clean sediment after each storm event. Replace fabric if
    clogged or damaged. Must not cause street flooding.
  Remove: After all contributing drainage area is permanently stabilized

BMP #3: Stabilized Construction Entrance
  Type: #57 limestone, 6" thick, 50 ft long x 20 ft wide, geotextile underliner
  Location: Main site entrance (north access road)
  Quantity: 1 EA
  Install: BEFORE any construction traffic enters site
  Responsible: GC
  Maintenance: Add stone as needed; sweep adjacent roadway daily.
    Tire wash station required if tracking persists.
  Remove: When permanent entrance is constructed

BMP #4: Temporary Seeding
  Type: Annual ryegrass, 120 lbs/acre, with straw mulch at 2 tons/acre
  Location: All disturbed areas inactive for > 14 days
  Quantity: As needed (approx 2.5 acres)
  Install: Within 14 days of last disturbance in each area
  Responsible: GC
  Maintenance: Re-seed bare spots; re-mulch if washout occurs
  Remove: Replaced by permanent stabilization

BMP #5: Concrete Washout
  Type: Lined pit (10-mil poly), 10 ft x 10 ft x 3 ft deep
  Location: Northwest corner of site (away from storm drains)
  Quantity: 1 EA (expand as needed)
  Install: Before first concrete delivery
  Responsible: GC (concrete sub must use designated washout only)
  Maintenance: Pump and dispose of washwater when pit is 75% full
  Remove: After final concrete placement; dispose of hardened material to landfill
```

### Inspection Triggers and Schedule

**Inspection Trigger Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Rainfall threshold** | Rain amount that triggers a post-storm inspection | 0.5 inches in 24 hours |
| **Routine frequency** | How often inspections occur regardless of rain | Weekly (every 7 calendar days) |
| **Post-storm deadline** | When post-storm inspection must be completed | Within 24 hours of qualifying rain event |
| **Inspector qualifications** | Required training or certification | State-certified SWPPP inspector or QCI (Qualified Compliance Inspector) |
| **Inspection form** | Required documentation format | State environmental agency form or SWPPP inspection checklist |
| **Corrective action timeline** | How fast problems must be fixed | Immediate for BMP failures; 7 days for maintenance items |
| **Record retention** | How long inspection records must be kept | 3 years after NOT filing |

**EXAMPLE INSPECTION TRIGGER EXTRACT**:
```
Inspection Requirements:

Routine: Every 7 calendar days (rain or shine)
Post-storm: Within 24 hours of any rain event >= 0.5 inches in 24 hours
  (measured at on-site rain gauge or nearest NOAA station)

Inspector: Must be QCI-certified (40-hour training) or state-licensed
  SWPPP inspector. Name: Mike Johnson, QCI #12345

Inspection checklist items:
  - All BMPs in place and functional? (silt fence, inlet protection, entrance)
  - Sediment accumulation at BMPs? (clean if > 1/3 silt fence height)
  - Evidence of erosion or sediment leaving site?
  - Concrete washout pit capacity adequate?
  - All inactive areas stabilized (seeded/mulched) within 14-day deadline?
  - Outfall discharge points clear of sediment?
  - Construction entrance clean? Adjacent road tracked?

Corrective action:
  - BMP failure (down silt fence, overtopped inlet protection): FIX IMMEDIATELY
    (same day, before end of next business day at latest)
  - Maintenance items (sediment removal, stone addition): Within 7 calendar days
  - Stabilization deficiency (bare area > 14 days): Seed within 48 hours

Record keeping:
  - Maintain all inspection reports on-site in SWPPP binder
  - Retain for 3 years after Notice of Termination (NOT) is filed
  - Available for review by regulatory agency at any time
```

### Stabilization Requirements

**Stabilization Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Temporary stabilization deadline** | Days of inactivity before stabilization required | 14 days (varies by state: 7 in some, 14 in most) |
| **Temporary methods** | Approved temporary stabilization measures | Annual ryegrass, straw mulch, erosion control blankets |
| **Permanent stabilization methods** | Final ground cover requirements | Permanent seed mix, sod, pavement, building coverage |
| **Seed mix specification** | Species, rate, season | Tall fescue at 200 lbs/acre (fall); annual rye at 120 lbs/acre (spring) |
| **Mulch specification** | Type, rate | Straw at 2 tons/acre (no hay — contains weed seeds) |
| **Erosion control blankets** | When required (slopes, channels) | Slopes > 3H:1V, all constructed channels |
| **Soil amendment** | If required (lime, fertilizer, compost) | 10-10-10 fertilizer at 400 lbs/acre; lime per soil test |

**EXAMPLE STABILIZATION EXTRACT**:
```
Stabilization Requirements:

Temporary:
  Deadline: 14 calendar days of inactivity in any disturbed area
  Method (Spring/Summer - Mar to Aug): Annual ryegrass, 120 lbs/acre
    + straw mulch at 2 tons/acre. Anchor mulch if windy.
  Method (Fall/Winter - Sep to Feb): Winter wheat, 150 lbs/acre
    + straw mulch at 2 tons/acre
  Slopes > 3H:1V: Erosion control blanket (straw/coconut fiber,
    single-net, stapled per manufacturer's specs)

Permanent:
  Seed mix: State highway mix (tall fescue 60%, KY bluegrass 20%,
    perennial rye 20%) at 200 lbs/acre
  Fertilizer: 10-10-10 at 400 lbs/acre, lime as recommended by soil test
  Method: Drill seed or hydroseed (broadcast acceptable with mulch cover)
  Target: 70% perennial vegetative cover within 1 year

Channels/swales:
  Permanent: Rip-rap or turf reinforcement mat (per engineering design)
  Temporary: Erosion control blanket (double-net, staked)
```

### Discharge Monitoring

**Discharge Monitoring Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Outfall locations** | Where stormwater leaves the site | Outfall 001 (SE corner to Mill Creek), Outfall 002 (NW to city storm) |
| **Sampling requirements** | When and what to sample | Grab sample within first 30 minutes of discharge from qualifying event |
| **Benchmark values** | Numeric limits for discharge quality | Turbidity: 280 NTU max; pH: 6.0 - 9.0 |
| **Reporting frequency** | How often monitoring reports are due | Quarterly DMR (Discharge Monitoring Report) to state EPA |
| **Exceedance response** | What to do if benchmarks are exceeded | Install additional BMPs, re-sample within 30 days, submit corrective action report |

**EXAMPLE DISCHARGE MONITORING EXTRACT**:
```
Discharge Monitoring:

Outfall 001:
  Location: SE corner of site, discharge to Mill Creek (waters of the US)
  Receiving water: Mill Creek (classified Cold Water Habitat)
  Monitoring: Grab sample within first 30 minutes of discharge
    from any storm event >= 0.5 inches in 24 hours

Outfall 002:
  Location: NW corner, discharge to city municipal storm system
  Monitoring: Same as Outfall 001

Benchmark parameters:
  Turbidity: 280 NTU maximum (state benchmark)
  pH: 6.0 to 9.0 (federal benchmark)
  Total suspended solids: Not required unless state mandates

Reporting:
  Quarterly DMR to state environmental agency (due 28th of month
  following quarter end: Apr 28, Jul 28, Oct 28, Jan 28)
  Annual report due February 28

Exceedance response:
  If turbidity > 280 NTU or pH outside 6.0-9.0:
    1. Install additional BMPs within 7 days
    2. Re-sample within 30 days of corrective action
    3. Submit corrective action report to state EPA
    4. Document in SWPPP amendment log
```

### SWPPP Amendment Triggers

**When the SWPPP Must Be Updated**:

| Trigger | Action Required | Timeline |
|---------|-----------------|----------|
| Change in construction sequence affecting drainage patterns | Update site plan, revise BMP locations | Before construction change begins |
| New BMP installed (not in original plan) | Add to BMP schedule with location and maintenance plan | Within 7 days of installation |
| BMP failure requiring permanent replacement | Document failure, update with replacement BMP | Within 7 days |
| New discharge point or change in discharge location | Update outfall map, revise monitoring plan | Before new discharge occurs |
| Change in operator/contractor responsible for BMPs | Update responsible personnel page | Within 7 days |
| Area of disturbance increases beyond original permit | May require new NOI or permit modification | BEFORE expanding disturbance |
| Response to regulatory inspection findings | Address all cited deficiencies in amendment | Per inspector's timeline (typically 30 days) |

### NOI/NOT Tracking

**NOI/NOT Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **NOI filing date** | When Notice of Intent was submitted | December 15, 2025 |
| **Permit number** | State NPDES or CGP permit number | KYR100456 |
| **Permit effective date** | When coverage begins | January 2, 2026 |
| **Permit expiration** | When the general permit expires (must renew) | December 31, 2030 (5-year CGP) |
| **NOT requirements** | What must be achieved before filing termination | 70% permanent vegetative cover on all disturbed areas |
| **NOT filing target** | Estimated date for project final stabilization | September 2027 (based on schedule) |
| **Annual fee** | Permit fee amount and due date | $500 annual fee, due with NOI and each anniversary |

**EXAMPLE NOI/NOT EXTRACT**:
```
Permit Tracking:

NOI filed: December 15, 2025
Permit number: KYR100456 (Kentucky CGP)
Effective date: January 2, 2026
General permit expiration: December 31, 2030
Annual fee: $500 (paid with NOI)

NOT requirements:
  - All disturbed areas must have 70% permanent vegetative cover
  - All temporary BMPs removed (silt fence, inlet protection)
  - All construction debris and waste materials removed from site
  - Final SWPPP inspection conducted and documented
  - NOT form submitted to state EPA within 30 days of achieving
    final stabilization

NOT target date: September 2027 (based on project schedule + 1 growing season)

CRITICAL: Do NOT file NOT prematurely. Premature termination = regulatory
violation. Verify 70% cover with photo documentation.
```

### Responsible Personnel

**SWPPP Personnel Fields**:

| Role | Name | Certification | Contact |
|------|------|---------------|---------|
| **SWPPP Administrator** | Person responsible for plan maintenance and amendments | QCI or state-licensed | Name, phone, email |
| **Qualified Inspector** | Person who conducts routine and post-storm inspections | QCI certification # | Name, phone, cert # |
| **Site Superintendent** | Day-to-day BMP oversight and corrective action | N/A (experience-based) | Name, phone |
| **Erosion Control Subcontractor** | Installs and maintains BMPs | State licensing if required | Company, contact |

**EXAMPLE PERSONNEL EXTRACT**:
```
SWPPP Responsible Personnel:

SWPPP Administrator: Sarah Williams, PE
  Company: GC Environmental Compliance
  Phone: (555) 234-5678
  Email: swilliams@gcenv.com
  Certification: State QCI #12345, expires 12/2027

Qualified Inspector: Mike Johnson
  Company: GC Environmental Compliance
  Phone: (555) 234-5679
  Certification: QCI #12346, 40-hour training, expires 12/2027

Site Superintendent: Tom Jackson
  Company: General Contractor, Inc.
  Phone: (555) 345-6789
  Responsible for: Daily BMP observation, corrective action initiation

Erosion Control Sub: Green Earth Environmental
  Contact: Dave Miller
  Phone: (555) 456-7890
  Responsible for: BMP installation, repair, and removal
  State License: ENV-2026-001
```

---

## ENVIRONMENTAL COMPLIANCE EXTRACTION

Environmental documents establish legal constraints that can be far more consequential than building code violations. A wetland encroachment or endangered species disturbance can trigger federal enforcement.

### Phase I / Phase II ESA Findings

**Phase I ESA Extraction** (ASTM E1527):

| Field | Description | Example |
|-------|-------------|---------|
| **RECs** | Recognized Environmental Conditions (evidence of contamination or likely contamination) | Former gas station on adjacent parcel; underground storage tank (UST) records |
| **HRECs** | Historical RECs (past contamination that has been remediated) | Fuel spill in 1998, cleaned up under state oversight, NFA letter issued 2002 |
| **CRECs** | Controlled RECs (contamination exists but is managed under institutional/engineering controls) | Deed restriction limiting site use; vapor mitigation system required |
| **De Minimis** | Minor conditions not rising to REC level | Small quantities of household chemicals in garage |
| **Recommended further action** | What the assessor recommends | Phase II ESA recommended to investigate RECs |
| **Data gaps** | Information the assessor could not obtain | Historical aerial photos 1950-1965 not available |

**Phase II ESA Extraction** (ASTM E1903):

| Field | Description | Example |
|-------|-------------|---------|
| **Sampling locations** | Where soil/groundwater samples were collected | MW-1, MW-2 (monitoring wells); SB-1 through SB-6 (soil borings) |
| **Contaminants detected** | What was found above screening levels | Benzene in groundwater at MW-2: 12 ppb (MCL = 5 ppb) |
| **Screening levels** | Regulatory comparison values | EPA RSLs, state action levels, MCLs |
| **Exceedances** | Which results exceed regulatory thresholds | Benzene at MW-2 exceeds MCL; lead in soil at SB-4 exceeds residential RSL |
| **Risk assessment** | Assessor's risk characterization | Low risk to construction workers with standard PPE; vapor intrusion assessment recommended for occupied building |
| **Remediation required** | What cleanup is needed | Soil excavation of 200 CY from SB-4 area; groundwater monitoring quarterly for 2 years |
| **Regulatory oversight** | Which agency has jurisdiction | State Department of Environmental Protection, case file #ENV-2025-789 |

**EXAMPLE ESA EXTRACT**:
```
Environmental Site Assessment Summary:

Phase I (completed November 2025):
  RECs identified: 1
    - Adjacent parcel (south): Former dry cleaning operation (1975-2005).
      Potential chlorinated solvent contamination (PCE/TCE) migrating
      onto project site via groundwater flow direction (south to north).
  HRECs: 0
  CRECs: 0
  Recommendation: Phase II ESA to investigate chlorinated solvents
    in groundwater at southern property boundary.

Phase II (completed January 2026):
  Sampling: 3 monitoring wells (MW-1, MW-2, MW-3), 6 soil borings
  Results:
    MW-1 (south boundary): PCE = 2.3 ppb (MCL = 5 ppb) → BELOW threshold
    MW-2 (center of site): PCE = 0.5 ppb → BELOW threshold
    MW-3 (north boundary): PCE = non-detect
    All soil samples: Below residential RSLs for VOCs and metals

  Conclusion: No exceedances of regulatory thresholds.
  Contamination from adjacent dry cleaner has NOT migrated onto site
  at actionable concentrations. No remediation required.
  Recommendation: Install sub-slab vapor barrier as precautionary measure
    (cost: ~$2/SF, approximately $10,000 for building footprint).
```

### Asbestos / Lead Surveys

**Survey Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Survey type** | Pre-demolition, pre-renovation, or limited | Pre-demolition survey (full building) |
| **Surveyor** | Licensed inspector name and license number | John Doe, AHERA Inspector #IL-12345 |
| **Materials sampled** | Types and locations of samples | Floor tile, mastic, pipe insulation, transite siding, window glazing |
| **Positive results** | Materials containing asbestos or lead | Floor tile (9x9, beige): Chrysotile asbestos, 5% |
| **Quantities** | Amount of ACM (asbestos-containing material) or LBP (lead-based paint) | 2,400 SF floor tile, 350 LF pipe insulation |
| **Condition** | Friable (easily crumbled) or non-friable; intact or damaged | Non-friable, intact (floor tile); friable, damaged (pipe insulation) |
| **Abatement requirement** | Required removal method and regulatory framework | NESHAP notification 10 working days before demolition; licensed abatement contractor |
| **Estimated cost** | Abatement cost estimate | $45,000 for pipe insulation removal; $15,000 for floor tile removal |

**EXAMPLE ASBESTOS/LEAD EXTRACT**:
```
Asbestos Survey Results (Pre-Demolition):

Surveyor: John Doe, AHERA Inspector #IL-12345
Survey date: December 1, 2025
Building: Existing warehouse (1962 construction)

POSITIVE RESULTS:

Material #1: 9x9 Beige Floor Tile + Black Mastic
  Asbestos type: Chrysotile, 5% (tile); Chrysotile, 8% (mastic)
  Location: First floor, all rooms (2,400 SF)
  Condition: Non-friable, intact
  Abatement: Wet removal by licensed contractor, NESHAP notification required
  Estimated cost: $15,000

Material #2: Pipe Insulation (Mechanical Room)
  Asbestos type: Amosite, 25%
  Location: Mechanical room, 350 LF of 4" pipe
  Condition: FRIABLE, damaged in several locations (CRITICAL)
  Abatement: Full containment, negative air, licensed contractor
  NESHAP notification: 10 working days minimum before disturbance
  Estimated cost: $45,000

Material #3: Transite Cement Siding (exterior)
  Asbestos type: Chrysotile, 12%
  Location: All exterior walls (4,800 SF)
  Condition: Non-friable, intact
  Abatement: Wet methods, careful removal to avoid breakage
  Estimated cost: $22,000

NEGATIVE RESULTS (no asbestos):
  Drywall/joint compound, roofing materials, window caulk

Lead Paint Survey:
  XRF testing: 45 locations tested
  Positive (>1.0 mg/cm2): Interior window sills (24 locations), door frames (12 locations)
  Abatement: Encapsulation acceptable for renovation; full removal if demolition
  Estimated cost: $8,000 (encapsulation) or $18,000 (full removal)

TOTAL ABATEMENT ESTIMATE: $82,000 - $100,000
SCHEDULE IMPACT: 3-4 weeks for abatement before demolition can begin
```

### Wetland Delineation

**Wetland Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Wetland boundaries** | Delineated limits (reference survey/map) | 0.85 acres in NW corner of site, flagged with pink flagging tape |
| **Wetland type** | Palustrine emergent, forested, scrub-shrub, etc. | Palustrine emergent (PEM) — cattails, sedges |
| **Jurisdictional determination** | USACE or state determination (wetlands vs. non-jurisdictional) | Jurisdictional under CWA Section 404 (connected to navigable waters) |
| **Buffer requirements** | Required setback from wetland boundary | 50 ft undisturbed buffer (per local ordinance) |
| **Permitted impacts** | Any approved fill or disturbance within wetlands | 0.12 acres temporary impact for utility crossing (NWP 12) |
| **Mitigation requirements** | Required compensation for wetland impacts | 2:1 mitigation ratio = 0.24 acres of wetland creation or mitigation bank credits |
| **Permit type** | Section 404 permit (individual or nationwide) | Nationwide Permit 12 (Utility Line Activities) |
| **Permit conditions** | Specific conditions of the 404 permit | Restore temporary impact area within 30 days of utility installation |

**EXAMPLE WETLAND EXTRACT**:
```
Wetland Delineation Summary:

Delineation date: October 15, 2025
Delineator: Environmental Consultants, Inc. (Jane Smith, PWS)

Wetland A:
  Location: NW corner of site
  Area: 0.85 acres
  Type: Palustrine emergent (PEM) — cattails, sedges, hydric soils
  Jurisdiction: USACE jurisdictional (adjacent to Mill Creek)
  Buffer: 50 ft undisturbed buffer per county ordinance
  Construction limits: Silt fence installed at buffer boundary.
    NO equipment, material storage, or grading within buffer.

Permitted impacts:
  Utility crossing (sanitary sewer): 0.12 acres temporary impact
  Permit: Nationwide Permit 12 (pre-construction notification filed)
  Conditions:
    - Bore under wetland if feasible (preferred); open-cut only if boring fails
    - Restore disturbed area within 30 days: replace topsoil, re-seed with
      native wetland seed mix (state-approved), install erosion control blanket
    - No permanent fill in wetland
  Mitigation: 2:1 ratio = 0.24 acres of mitigation bank credits purchased
    from XYZ Mitigation Bank (credit purchase receipt on file)

CRITICAL: Any unauthorized impact to wetland beyond permitted 0.12 acres
triggers federal enforcement (USACE + EPA). Fine up to $25,000/day.
Mark buffer with high-visibility fencing. Brief all subs on limits.
```

### Endangered Species

**Species Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Species identified** | Name, federal/state status | Indiana bat (Myotis sodalis), federally endangered |
| **Habitat areas** | Where on or near the site | Mature tree stand along eastern property line (potential roost trees) |
| **Survey results** | Presence/absence survey findings | Acoustic survey: No Indiana bat calls detected (survey July 2025) |
| **Seasonal restrictions** | Time-of-year restrictions on activities | No tree clearing April 1 - September 30 (bat active season) |
| **Buffer/setback** | Required distance from habitat | 100 ft buffer from tree drip line during nesting season |
| **Agency consultation** | USFWS or state agency involvement | USFWS Section 7 consultation completed; Biological Opinion issued |
| **Mitigation** | Required conservation measures | Install 10 bat boxes on retained trees; monitoring for 3 years |

**EXAMPLE ENDANGERED SPECIES EXTRACT**:
```
Endangered Species Assessment:

Species: Indiana bat (Myotis sodalis) — Federally Endangered
Habitat: 12 mature trees (DBH > 11 inches) along eastern property line
  identified as potential summer roost habitat.

Survey: Acoustic monitoring conducted July 15-25, 2025
  Result: No Indiana bat calls detected at any of 4 monitoring stations
  Conclusion: No documented presence, but suitable habitat exists

USFWS consultation: Section 7 informal consultation completed (Nov 2025)
  Determination: "Not likely to adversely affect"
  Conditions:
    1. Tree clearing restricted to October 1 - March 31 ONLY
       (outside bat active season April 1 - September 30)
    2. If tree clearing cannot occur in this window, formal consultation
       required (adds 90+ days to schedule)
    3. Install 10 bat boxes on retained trees along property line
    4. Report any bat observations to USFWS within 24 hours

Schedule impact: Tree clearing must be completed by March 31 or project
  is delayed until October 1. Currently scheduled for February 2026 — OK.

Cost: Bat boxes = $2,500 installed. No other mitigation costs.
```

### Noise / Vibration Limits

**Noise/Vibration Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Permitted noise levels** | Decibel limits by time of day | Daytime (7am-7pm): 85 dBA at property line; Nighttime: 70 dBA |
| **Measurement locations** | Where monitoring occurs | Nearest residential property line (east, 150 ft from site) |
| **Vibration limits** | Peak particle velocity (PPV) limits | 0.5 in/sec PPV at nearest structure (per local ordinance) |
| **Restricted hours** | When certain operations are prohibited | No pile driving before 8:00 AM or after 5:00 PM weekdays; none on weekends |
| **Monitoring requirements** | When continuous monitoring is required | During all pile driving and rock hammer operations |
| **Mitigation measures** | Required noise/vibration reduction methods | Sound barriers (8 ft plywood fence), vibration-dampened equipment |
| **Pre-construction survey** | Existing conditions documentation | Photo survey of adjacent structures within 200 ft (document pre-existing cracks) |

**EXAMPLE NOISE/VIBRATION EXTRACT**:
```
Noise and Vibration Requirements:

Noise limits (per City Ordinance 2025-123):
  Daytime (7:00 AM - 7:00 PM, Mon-Sat): 85 dBA at property line
  Evening (7:00 PM - 10:00 PM): 70 dBA at property line
  Nighttime (10:00 PM - 7:00 AM): 55 dBA at property line
  Sunday/Holidays: 70 dBA at property line (all hours)
  Measurement: A-weighted, slow response, at nearest residential lot line

Vibration limits:
  0.5 in/sec PPV at nearest structure (residential standard)
  0.2 in/sec PPV at historic structures (if any within 500 ft — none identified)
  Monitoring required during: Pile driving, vibratory compaction, rock hammer

Work hour restrictions:
  Standard construction: 7:00 AM - 7:00 PM, Mon-Sat
  Pile driving: 8:00 AM - 5:00 PM, Mon-Fri only
  Concrete placement: May extend to 9:00 PM with city permit ($250 fee)
  No work Sundays or federal holidays without special variance

Pre-construction survey:
  Photo/video survey of all structures within 200 ft of site perimeter
  Completed: January 10, 2026 (report on file)
  Purpose: Document pre-existing cracks and conditions to defend against
    future damage claims from adjacent property owners

Mitigation:
  8 ft plywood sound barrier along east property line (nearest residences)
  Vibration-dampened compaction equipment for work within 50 ft of property line
  Noise monitoring (handheld meter) twice daily during heavy equipment operations
```

---

## PERMIT COMPLIANCE EXTRACTION

Permits contain conditions that are legally binding. Missing a permit condition is equivalent to building without a permit.

### Building Permit Conditions

**Building Permit Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Permit number** | Building permit ID | BP-2026-001234 |
| **Issue date** | When permit was issued | January 15, 2026 |
| **Expiration** | When permit expires if work has not commenced | January 15, 2027 (12 months) |
| **Approved plans** | Which plan set was approved (date and revision) | Plans dated December 1, 2025, Revision 2 |
| **Special inspections required** | IBC Chapter 17 inspections (structural steel, concrete, etc.) | See special inspections table below |
| **Conditions of approval** | Any non-standard conditions added by plan reviewer | See conditions list below |
| **Variance conditions** | If a variance or deviation was granted | Reduced side yard setback approved (10 ft vs 15 ft code minimum) |
| **Approved deferred submittals** | Items not reviewed at permit — must be submitted later | Truss engineering, curtain wall shop drawings, fire suppression design |

**Special Inspections Required (IBC Chapter 17)**:

| Inspection Category | What Is Inspected | Frequency | Inspector Qualification |
|---------------------|-------------------|-----------|------------------------|
| **Concrete placement** | Concrete strength, slump, air content, reinforcement | Each placement (hold point for rebar, witness for pour) | ACI certified |
| **Structural steel — welding** | CJP and PJP welds, fillet welds | Continuous for CJP; periodic for others | AWS CWI |
| **Structural steel — bolting** | High-strength bolts (pretensioned and slip-critical) | Per connection type | ICC Special Inspector |
| **Structural masonry** | Grout placement, reinforcement, mortar joints | Each grout lift (hold point) | ICC Special Inspector |
| **Soils/earthwork** | Compaction, bearing verification, fill placement | Per geotech report frequency | Geotechnical engineer or technician |
| **Spray fireproofing** | Thickness, density, bond strength | Each floor/area | ICC Special Inspector |
| **Structural wood** | Metal plate connectors, hold-downs, shear walls | As installed (before concealment) | ICC Special Inspector |
| **Deep foundations** | Pile driving records, drilled shaft installation | Each pile/shaft (hold point) | Geotechnical engineer |

**EXAMPLE BUILDING PERMIT EXTRACT**:
```
Building Permit:

Permit number: BP-2026-001234
Issued: January 15, 2026
Expires: January 15, 2027 (if work not commenced)
Approved plans: ABC Building, dated December 1, 2025, Revision 2
  Structural: S-100 through S-512 (Smith Engineering)
  Architectural: A-100 through A-801 (Jones Architects)
  MEP: M-100 through P-402 (Green Mechanical)

Special inspections required:
  1. Concrete: Rebar placement (HOLD POINT — do not pour until inspected)
     Concrete placement (WITNESS — inspector should be present)
     Testing: 1 set cylinders per 50 CY, slump every truck
  2. Structural steel: All CJP welds (continuous inspection by AWS CWI)
     High-strength bolts (periodic inspection)
  3. Soils: Per geotech report — bearing verification at each footing,
     compaction testing per 2,500 SF per lift
  4. Spray fireproofing: Thickness verification per floor

Conditions of approval:
  C-1: Deferred submittal for pre-engineered metal building design
       (must be submitted and approved before PEMB erection)
  C-2: Fire sprinkler shop drawings deferred — must be approved by
       Fire Marshal before concealment of sprinkler piping
  C-3: Stormwater management plan approved by county separate from
       building permit — see SWPPP requirements
  C-4: Tree preservation plan: Protect 3 oak trees along north
       property line with 6 ft chain-link fence at drip line

Variance:
  Side yard setback reduced from 15 ft to 10 ft (east side)
  Condition: 2-hour fire-rated wall required on east elevation
    (in lieu of standard 1-hour for reduced setback)
```

### Grading Permit

**Grading Permit Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Permit number** | Grading permit ID | GP-2026-000567 |
| **Permitted cut quantity** | Maximum cubic yards of excavation | 12,000 CY cut |
| **Permitted fill quantity** | Maximum cubic yards of fill | 8,500 CY fill |
| **Export/import** | Net export or import of material | 3,500 CY net export to approved disposal site |
| **Haul route** | Approved truck route for material transport | Main Street to Highway 60 (NO residential streets) |
| **Hours of operation** | When grading/hauling is permitted | 7:00 AM - 5:00 PM, Mon-Fri; 8:00 AM - 12:00 PM Sat |
| **Dust control** | Required dust mitigation measures | Water trucks on active grading areas; apply tackifier on stockpiles |
| **Tracking control** | Measures to prevent mud tracking on roads | Stabilized construction entrance; wheel wash if tracking persists |
| **Erosion control** | Required erosion and sediment control measures | Per SWPPP (separate document — cross-reference) |
| **As-built survey** | Required upon completion | Certified as-built grading survey within 30 days of completion |

**EXAMPLE GRADING PERMIT EXTRACT**:
```
Grading Permit:

Permit number: GP-2026-000567
Issued: January 10, 2026
Expires: July 10, 2026 (6 months)

Permitted quantities:
  Cut: 12,000 CY maximum
  Fill: 8,500 CY maximum (on-site)
  Export: 3,500 CY to approved disposal site (XYZ Landfill, permit on file)
  Import: None permitted without amendment

Haul route:
  Site → North access road → Main Street → Highway 60 → Disposal site
  PROHIBITED: Oak Street, Elm Avenue (residential areas)
  Flaggers required at Main Street intersection during haul hours

Hours of operation:
  Grading: 7:00 AM - 5:00 PM, Monday through Friday
  Saturday: 8:00 AM - 12:00 PM (no hauling on Saturday)
  Sunday/Holidays: NO WORK

Dust control:
  Water truck on-site during all active grading (minimum 2,000-gallon capacity)
  Apply tackifier to inactive stockpiles within 48 hours
  Wind speed > 25 mph: CEASE grading operations
  Compliance: Visible emissions (opacity) must not exceed 20%

As-built requirement:
  Certified as-built grading survey by licensed surveyor within 30 days
  of grading completion. Must show final contours, retaining wall locations,
  drainage swale inverts, and detention basin bottom elevations.
```

### Utility Permits

**Utility Permit Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **ROW permit** | Right-of-way work permit for work in public ROW | ROW-2026-0089 (City Public Works) |
| **Encroachment permit** | For work near or over public infrastructure | ENC-2026-0045 (State DOT) |
| **Utility connection permits** | Water, sewer, gas, electric, telecom | Water tap: WT-2026-012; Sewer: SW-2026-034 |
| **Inspection requirements** | Utility-specific inspections before backfill | City water inspector must witness tap and pressure test |
| **Restoration requirements** | How to restore ROW after utility work | Full-depth pavement patch, 2 ft beyond trench each side, compaction test |
| **Traffic control plan** | Required TCP for work in or near roadway | Approved TCP on file; flaggers required during lane closures |
| **Bond/deposit** | Financial guarantee for ROW restoration | $15,000 ROW bond (refundable after 1-year maintenance period) |

**EXAMPLE UTILITY PERMIT EXTRACT**:
```
Utility Permits:

1. Water Tap — Permit WT-2026-012
   Provider: City Water Department
   Tap size: 6-inch ductile iron (for domestic + fire)
   Location: Main Street, station 2+45 (east side)
   Inspector: City water inspector must be on-site for:
     - Tap connection (HOLD POINT)
     - Pressure test at 200 PSI for 2 hours (HOLD POINT)
     - Bacteriological test (sample before connection to building)
   Restoration: Full-depth pavement, 3 ft beyond trench, 95% compaction

2. Sanitary Sewer — Permit SW-2026-034
   Provider: County Sewer District
   Tap size: 8-inch PVC lateral to 15-inch main
   Location: Elm Avenue, station 4+80
   Inspector: County sewer inspector must be on-site for:
     - Lateral connection to main (HOLD POINT)
     - Mandrel test (deflection test on PVC pipe)
     - TV inspection of completed lateral
   Restoration: Same as water tap

3. Gas Service — No separate permit (utility company handles)
   Provider: Gas Company, Inc.
   Meter location: NW corner of building
   Coordination: 48-hour notice before excavation near gas main (call 811)

4. ROW Permit — ROW-2026-0089
   Issuer: City Public Works Department
   Scope: Utility trenching in Main Street and Elm Avenue ROW
   Duration: February 15 - April 15, 2026 (60 days maximum)
   Traffic control: Approved TCP on file; flaggers during lane closures
   Bond: $15,000 (refundable 12 months after final restoration acceptance)
```

### Fire Department Conditions

**Fire Department Fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **FDC location** | Fire department connection location and type | FDC on north elevation, Siamese connection, 50 ft from hydrant |
| **Hydrant spacing** | Required fire hydrant spacing and locations | Every 300 ft along fire apparatus access; 2 hydrants on-site |
| **Fire lane requirements** | Width, turning radius, marking | 20 ft wide, 26 ft inside turning radius, marked "NO PARKING — FIRE LANE" |
| **Access requirements** | Fire apparatus access road specs | All-weather surface, 80,000 lb load capacity, within 150 ft of all building points |
| **Knox box** | Key box for fire department access | Knox box at main entrance, keyed to local FD |
| **Alarm system** | Fire alarm type and monitoring | Addressable fire alarm, monitored by UL-listed central station |
| **Sprinkler requirements** | Suppression system type | NFPA 13 wet-pipe throughout; NFPA 13R in residential areas |
| **Standpipe** | Standpipe requirements (if multi-story) | Class I standpipe in all stairwells (building > 3 stories) |
| **Fire watch** | When fire watch is required during construction | During all hot work (welding, cutting) and whenever fire alarm is impaired |

**EXAMPLE FIRE DEPARTMENT EXTRACT**:
```
Fire Department Conditions (Fire Marshal Plan Review):

FDC (Fire Department Connection):
  Location: North elevation, within 50 ft of nearest fire hydrant
  Type: 2.5" Siamese connection with clappers and caps
  Signage: "FDC" sign, reflective, 12" letters minimum
  Install BEFORE building is enclosed

Fire hydrants:
  Existing: 1 hydrant at Main Street / North access road intersection
  New: 2 additional hydrants required:
    - 1 on-site at NE corner of building (within 100 ft of FDC)
    - 1 on-site at SW corner of parking lot
  Spacing: Maximum 300 ft between hydrants measured along access road
  Flow test: 1,500 GPM at 20 PSI residual required (flow test on file)

Fire lane / apparatus access:
  Width: Minimum 20 ft clear (26 ft at curves)
  Turning radius: 26 ft inside, 46 ft outside
  Surface: All-weather, capable of supporting 80,000 lbs (fire apparatus)
  Marking: Red curb or "NO PARKING — FIRE LANE" signs every 100 ft
  Dead-end: Turnaround (hammerhead or cul-de-sac) at any dead-end > 150 ft
  Access: Must be within 150 ft of all points on exterior building walls

Knox Box:
  Location: Right side of main entrance door, 5 ft above grade
  Contains: Building master key, alarm panel key, elevator key, FDC key
  Order from: Knox Company (Fire Department provides authorization)

Fire alarm:
  Type: Addressable fire alarm per NFPA 72
  Monitoring: UL-listed central station (contract before occupancy)
  Annunciator: At main entrance, visible to responding firefighters

Sprinkler:
  Type: NFPA 13 wet-pipe system throughout
  Design: Ordinary hazard Group 1 (office); Ordinary Hazard Group 2 (warehouse)
  Shop drawings: Deferred submittal — must be approved by Fire Marshal
    BEFORE sprinkler rough-in begins

Fire watch during construction:
  Required during: All hot work (welding, cutting, brazing)
  Duration: 30 minutes after hot work completion
  Required when: Fire alarm or sprinkler system impaired (24-hour fire watch)
  Personnel: Dedicated fire watch with extinguisher and communication device
```

---

## OUTPUT MAPPING — JSON STRUCTURES

Compliance data maps to multiple project intelligence files. Below are the specific fields and structures for each target file.

### quality-data.json

Geotechnical test results, environmental reports, and material testing data map here.

```json
{
  "geotech_data": {
    "report_date": "2026-01-15",
    "firm": "ABC Geotechnical, Inc.",
    "report_number": "GEO-2026-001",
    "borings": [
      {
        "boring_id": "B-1",
        "location": "Grid A-3 (N 38.2544, W 85.7638)",
        "surface_elevation_ft": 842.5,
        "total_depth_ft": 35.0,
        "groundwater_depth_ft": 12.0,
        "groundwater_stabilized_ft": 14.5,
        "date_drilled": "2026-01-05",
        "drilling_method": "Hollow stem auger, 4.25\" ID",
        "soil_profile": [
          {
            "depth_top_ft": 0.0,
            "depth_bottom_ft": 3.5,
            "uscs": "CL",
            "description": "Brown, stiff, moist lean clay with trace gravel",
            "spt_n_value": 12,
            "sample_type": "SS",
            "sample_depth_ft": 2.0
          }
        ]
      }
    ],
    "bearing_capacity": {
      "spread_footings_psf": 3000,
      "continuous_footings_psf": 2500,
      "min_embedment_ft": 4.0,
      "bearing_stratum": "Stiff lean clay (CL)",
      "settlement_total_in": 0.75,
      "settlement_differential_in": 0.50,
      "factor_of_safety": 3.0,
      "subgrade_modulus_pci": 150
    },
    "earthwork": {
      "unsuitable_depth_ft": 2.0,
      "compaction_standard": "95% modified Proctor (ASTM D1557)",
      "lift_thickness_in": 8,
      "testing_frequency": "1 test per 2,500 SF per lift",
      "moisture_range": "Optimum +/- 2%"
    },
    "special_conditions": [
      {
        "type": "expansive_clay",
        "location": "B-2 and B-5, depth 4-10 ft",
        "severity": "moderate",
        "swell_percent": 3.5,
        "mitigation": "Moisture-condition fill; void boxes under grade beams"
      },
      {
        "type": "shallow_rock",
        "location": "B-6 (SE corner)",
        "depth_ft": 8.0,
        "mitigation": "Rock hammer required; no blasting"
      }
    ],
    "lab_results": [
      {
        "sample_id": "B-1 @ 5.0 ft",
        "uscs": "CL",
        "liquid_limit": 38,
        "plastic_limit": 18,
        "plasticity_index": 20,
        "natural_moisture_pct": 22.4,
        "proctor_mdd_pcf": 112.5,
        "proctor_omc_pct": 16.8
      }
    ],
    "groundwater_summary": {
      "design_water_table_ft": 10.0,
      "seasonal_high_note": "May rise 3-4 ft in spring (March-May)",
      "sulfate_ppm": 450,
      "sulfate_exposure": "moderate",
      "cement_recommendation": "Type II"
    }
  },
  "environmental_data": {
    "phase_i_date": "2025-11-15",
    "phase_i_firm": "Environmental Consultants, Inc.",
    "recs_count": 1,
    "recs": [
      {
        "description": "Adjacent former dry cleaner — potential PCE/TCE migration",
        "action_required": "Phase II ESA"
      }
    ],
    "phase_ii_date": "2026-01-20",
    "phase_ii_result": "No exceedances; precautionary vapor barrier recommended",
    "asbestos_survey": {
      "date": "2025-12-01",
      "positive_materials": 3,
      "abatement_required": true,
      "estimated_cost": 82000,
      "schedule_impact_weeks": 4
    },
    "lead_survey": {
      "date": "2025-12-01",
      "positive_locations": 36,
      "abatement_method": "encapsulation",
      "estimated_cost": 8000
    },
    "wetland_delineation": {
      "date": "2025-10-15",
      "wetland_area_acres": 0.85,
      "buffer_ft": 50,
      "permitted_impact_acres": 0.12,
      "permit_type": "Nationwide Permit 12",
      "mitigation_ratio": "2:1",
      "mitigation_credits": 0.24
    },
    "endangered_species": {
      "species": "Indiana bat (Myotis sodalis)",
      "status": "Federally Endangered",
      "survey_result": "No documented presence; suitable habitat exists",
      "seasonal_restriction": "No tree clearing April 1 - September 30",
      "consultation": "USFWS Section 7 informal — Not likely to adversely affect"
    }
  }
}
```

### specs-quality.json

Compliance thresholds, inspection triggers, and testing requirements map here.

```json
{
  "compliance_thresholds": {
    "swppp": {
      "permit_number": "KYR100456",
      "noi_date": "2025-12-15",
      "rainfall_trigger_in": 0.5,
      "inspection_frequency": "Weekly + within 24 hours of qualifying rain",
      "stabilization_deadline_days": 14,
      "turbidity_ntu_max": 280,
      "ph_range": "6.0 - 9.0",
      "not_requirement": "70% permanent vegetative cover",
      "corrective_action_immediate": ["BMP failure", "active erosion leaving site"],
      "corrective_action_7day": ["sediment removal", "stone replenishment", "re-seeding"]
    },
    "noise_vibration": {
      "daytime_dba": 85,
      "evening_dba": 70,
      "nighttime_dba": 55,
      "vibration_ppv_in_sec": 0.5,
      "work_hours": "7:00 AM - 7:00 PM Mon-Sat",
      "pile_driving_hours": "8:00 AM - 5:00 PM Mon-Fri"
    },
    "earthwork": {
      "compaction_pct_proctor": 95,
      "proctor_standard": "modified (ASTM D1557)",
      "lift_thickness_in": 8,
      "test_frequency": "1 per 2,500 SF per lift",
      "moisture_tolerance_pct": 2
    }
  },
  "special_inspections": [
    {
      "category": "concrete_placement",
      "hold_points": ["rebar placement before pour"],
      "witness_points": ["concrete placement"],
      "testing": "1 set cylinders per 50 CY; slump every truck",
      "inspector_qualification": "ACI certified"
    },
    {
      "category": "structural_steel_welding",
      "hold_points": ["CJP welds — continuous inspection"],
      "witness_points": ["fillet welds — periodic"],
      "inspector_qualification": "AWS CWI"
    },
    {
      "category": "soils_earthwork",
      "hold_points": ["bearing verification at each footing"],
      "witness_points": ["fill placement"],
      "testing": "Per geotech report frequency",
      "inspector_qualification": "Geotechnical engineer or technician"
    }
  ],
  "bmp_schedule": [
    {
      "bmp_id": 1,
      "type": "silt_fence",
      "location": "South and east property lines",
      "quantity": "1,200 LF",
      "install_timing": "Before land disturbance",
      "responsible_party": "Earthwork subcontractor",
      "maintenance": "Weekly + post-storm; replace at 1/3 sediment height"
    },
    {
      "bmp_id": 2,
      "type": "inlet_protection",
      "location": "All 6 storm drain inlets",
      "quantity": "6 EA",
      "install_timing": "Before land disturbance",
      "responsible_party": "Earthwork subcontractor",
      "maintenance": "Clean after each storm event"
    }
  ]
}
```

### project-config.json

Permit tracking and compliance deadlines map here.

```json
{
  "permits": [
    {
      "type": "building_permit",
      "number": "BP-2026-001234",
      "issue_date": "2026-01-15",
      "expiration": "2027-01-15",
      "approved_plans_date": "2025-12-01",
      "approved_plans_revision": 2,
      "deferred_submittals": [
        "PEMB design",
        "Fire sprinkler shop drawings",
        "Truss engineering"
      ],
      "conditions": [
        "C-1: PEMB design deferred — approve before erection",
        "C-2: Sprinkler shop drawings deferred — approve before rough-in",
        "C-3: Stormwater plan per SWPPP",
        "C-4: Tree preservation — protect 3 oaks with 6 ft fence"
      ],
      "variance": "East side setback reduced 15 ft to 10 ft; 2-hr fire wall required"
    },
    {
      "type": "grading_permit",
      "number": "GP-2026-000567",
      "issue_date": "2026-01-10",
      "expiration": "2026-07-10",
      "cut_cy": 12000,
      "fill_cy": 8500,
      "export_cy": 3500,
      "haul_route": "Site → North access → Main St → Hwy 60",
      "hours": "7:00 AM - 5:00 PM Mon-Fri; 8:00 AM - 12:00 PM Sat"
    },
    {
      "type": "swppp_npdes",
      "number": "KYR100456",
      "noi_date": "2025-12-15",
      "effective_date": "2026-01-02",
      "expiration": "2030-12-31",
      "not_target": "2027-09-01"
    },
    {
      "type": "row_permit",
      "number": "ROW-2026-0089",
      "issue_date": "2026-02-01",
      "expiration": "2026-04-15",
      "bond_amount": 15000,
      "scope": "Utility trenching in Main Street and Elm Avenue ROW"
    },
    {
      "type": "water_tap",
      "number": "WT-2026-012",
      "provider": "City Water Department",
      "tap_size": "6-inch DI",
      "inspections_required": ["tap connection", "pressure test", "bacteriological test"]
    },
    {
      "type": "sewer_connection",
      "number": "SW-2026-034",
      "provider": "County Sewer District",
      "tap_size": "8-inch PVC",
      "inspections_required": ["lateral connection", "mandrel test", "TV inspection"]
    }
  ],
  "compliance_deadlines": [
    {
      "item": "Tree clearing deadline (endangered species)",
      "deadline": "2026-03-31",
      "consequence": "Delay until October 1 if missed",
      "status": "on_track"
    },
    {
      "item": "Grading permit expiration",
      "deadline": "2026-07-10",
      "consequence": "Renewal required if grading not complete",
      "status": "on_track"
    },
    {
      "item": "ROW permit expiration",
      "deadline": "2026-04-15",
      "consequence": "Extension required for continued work in ROW",
      "status": "on_track"
    },
    {
      "item": "SWPPP quarterly DMR",
      "deadline": "2026-04-28",
      "consequence": "Regulatory violation if late",
      "status": "pending"
    }
  ]
}
```

---

## CROSS-REFERENCE RULES

Compliance data connects to nearly every other project record. Use these cross-references to catch conflicts and ensure completeness.

| Compliance Data | Related Project Record | Cross-Reference Rule |
|-----------------|----------------------|---------------------|
| Geotech bearing capacity | Structural drawings (foundation schedule) | Verify structural design loads do not exceed allowable bearing pressure |
| Geotech compaction requirements | Earthwork specifications (spec section 31 23 00) | Compaction standard in geotech must match spec; geotech report governs if conflict |
| Geotech groundwater depth | Dewatering plan, excavation safety plan | If excavation depth exceeds groundwater, dewatering and OSHA excavation safety required |
| Geotech sulfate content | Concrete mix design (cement type) | Moderate sulfate (150-1,500 ppm) = Type II cement; Severe (>1,500 ppm) = Type V |
| SWPPP BMP locations | Site logistics plan (crane, laydown, access) | BMP locations must not conflict with crane swing, material laydown, or access roads |
| SWPPP inspection frequency | Project schedule (weather days) | Log rain events that trigger inspections; cross-reference with daily report weather data |
| SWPPP stabilization deadlines | Schedule (grading, building enclosure) | Areas inactive >14 days must be stabilized; schedule should flag stabilization milestones |
| Building permit special inspections | Inspection log, schedule | Hold points must be in schedule as milestones; inspector must be booked in advance |
| Building permit deferred submittals | Submittal log, procurement log | Deferred submittals must be tracked and approved BEFORE associated work begins |
| Fire department FDC / hydrant locations | Site plan, utility drawings | Verify FDC within 50 ft of hydrant; hydrants spaced per fire code; access road meets load requirements |
| Environmental seasonal restrictions | Schedule (tree clearing, earthwork) | Tree clearing window must be on critical path if species restrictions apply |
| Noise/vibration limits | Schedule (pile driving, rock hammer) | Restricted-hour activities must be scheduled within permitted windows |
| Wetland buffer | Site logistics plan, grading plan | No equipment, stockpiles, or grading within buffer zone; silt fence at buffer boundary |
| Asbestos abatement schedule | Demolition schedule | Abatement must complete BEFORE demolition begins (3-4 week lead time typical) |
| Grading permit quantities | Earthwork quantities (from takeoff) | Verify actual cut/fill does not exceed permitted quantities; amend permit if needed |
| Utility permit expiration dates | Utility installation schedule | Utility work must be completed and inspected before permit expires |

---

## SUMMARY CHECKLIST — COMPLIANCE DOCUMENT EXTRACTION

### On Receipt of Geotechnical Report

- [ ] Extract ALL boring logs (ID, location, depth, groundwater, soil profile, SPT N-values)
- [ ] Extract bearing capacity for each foundation type (PSF, embedment depth, bearing stratum)
- [ ] Extract settlement estimates (total and differential)
- [ ] Extract earthwork requirements (compaction standard, lift thickness, testing frequency)
- [ ] Extract groundwater data (depth, seasonal variation, dewatering needs, chemical properties)
- [ ] Extract special conditions (expansive soils, rock, contamination, fill, frost depth)
- [ ] Extract laboratory test results (Atterberg limits, grain size, Proctor, strength tests)
- [ ] Extract foundation recommendation (type, special requirements, ground improvement)
- [ ] Cross-reference bearing capacity with structural foundation schedule
- [ ] Cross-reference sulfate content with concrete mix cement type
- [ ] Cross-reference groundwater with excavation plan and dewatering needs
- [ ] Flag any special conditions that affect schedule or budget
- [ ] Write to `quality-data.json` → `geotech_data` section

### On Receipt of SWPPP Documents

- [ ] Extract permit number (NOI, NPDES/CGP)
- [ ] Extract complete BMP schedule (type, location, quantity, timing, responsible party, maintenance)
- [ ] Extract inspection triggers (rainfall threshold, routine frequency, post-storm deadline)
- [ ] Extract inspector qualifications and name
- [ ] Extract stabilization requirements (temporary and permanent, deadlines, methods)
- [ ] Extract discharge monitoring (outfall locations, benchmarks, reporting frequency)
- [ ] Extract SWPPP amendment triggers
- [ ] Extract NOI/NOT tracking (filing dates, permit number, termination requirements)
- [ ] Extract responsible personnel (administrator, inspector, superintendent, erosion control sub)
- [ ] Cross-reference BMP locations with site logistics plan
- [ ] Cross-reference stabilization deadlines with project schedule
- [ ] Write to `specs-quality.json` → `compliance_thresholds.swppp` and `bmp_schedule`
- [ ] Write to `project-config.json` → `permits` array (SWPPP/NPDES entry)

### On Receipt of Environmental Reports

- [ ] Extract Phase I ESA findings (RECs, HRECs, CRECs, recommended action)
- [ ] Extract Phase II ESA results (sampling locations, contaminants, exceedances, remediation)
- [ ] Extract asbestos/lead survey results (positive materials, quantities, abatement requirements, cost)
- [ ] Extract wetland delineation (boundaries, buffers, permitted impacts, mitigation)
- [ ] Extract endangered species assessment (species, restrictions, seasonal windows, consultation)
- [ ] Extract noise/vibration limits (permitted levels, hours, monitoring requirements)
- [ ] Cross-reference seasonal restrictions with project schedule critical path
- [ ] Cross-reference wetland buffers with site logistics and grading plans
- [ ] Cross-reference abatement schedule with demolition schedule
- [ ] Write to `quality-data.json` → `environmental_data` section
- [ ] Write to `project-config.json` → `compliance_deadlines` array

### On Receipt of Permits

- [ ] Extract building permit number, issue date, expiration, approved plan set
- [ ] Extract ALL special inspection requirements (IBC Ch. 17) with hold points and witness points
- [ ] Extract ALL conditions of approval (numbered list with required actions)
- [ ] Extract deferred submittals (what, when it must be approved)
- [ ] Extract any variance conditions
- [ ] Extract grading permit (quantities, haul route, hours, dust control, as-built requirement)
- [ ] Extract utility permits (type, provider, tap size, inspection requirements, bond)
- [ ] Extract fire department conditions (FDC, hydrants, fire lane, Knox box, sprinkler, fire watch)
- [ ] Cross-reference deferred submittals with submittal log and procurement schedule
- [ ] Cross-reference special inspections with project schedule (add hold point milestones)
- [ ] Cross-reference fire department conditions with site plan and MEP drawings
- [ ] Cross-reference grading quantities with earthwork takeoff
- [ ] Write to `project-config.json` → `permits` array
- [ ] Write to `specs-quality.json` → `special_inspections` array

---

## NOTES

- Compliance documents are **legally binding**. Unlike shop drawings or RFIs, a missed compliance requirement can result in fines, stop-work orders, or criminal liability. Extraction must be exhaustive.
- The geotechnical report is the most technically dense compliance document. If the AI is uncertain about a value (e.g., bearing capacity units, compaction standard type), flag for human review rather than guessing.
- SWPPP inspections are the most frequent recurring compliance obligation. Automate reminders: weekly + within 24 hours of qualifying rain.
- Environmental restrictions often create **hard schedule constraints** (seasonal windows for tree clearing, abatement before demolition). These must be on the critical path.
- Permit expiration dates are easily forgotten. Track all expiration dates in `project-config.json` → `compliance_deadlines` and surface them in the morning brief.
- When multiple compliance documents conflict (e.g., geotech says "95% standard Proctor" but specs say "95% modified Proctor"), the more stringent requirement governs unless the engineer issues a written clarification.
- Fire department conditions must be met before occupancy. Late discovery of a missing FDC, Knox box, or fire lane marking can delay the certificate of occupancy by weeks.
- Always store the original compliance document reference (report number, date, author) alongside extracted data so the field team can pull the source document if questions arise.
