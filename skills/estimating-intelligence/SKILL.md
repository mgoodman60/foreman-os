---
name: estimating-intelligence
description: >
  Construction estimating knowledge for field superintendents — unit cost structure, assembly-based estimating, CSI MasterFormat cost coding, quantity takeoff methods, productivity rate validation, T&M pricing verification, bid review and leveling, and value engineering analysis. Provides cost awareness for daily decisions, change order pricing review, pay application verification, and budget-to-field reconciliation. Triggers: "estimate", "estimating", "cost", "unit cost", "unit price", "bid", "bid leveling", "takeoff", "quantity", "productivity", "labor rate", "equipment rate", "markup", "overhead", "profit", "CSI", "MasterFormat", "assembly", "waste factor", "T&M", "time and materials", "change order pricing", "value engineering", "VE".
version: 1.0.0
---

# Estimating Intelligence Skill

## Overview

The **estimating-intelligence** skill provides deep estimating knowledge for the field superintendent. This skill does not aim to replace a professional estimator -- it equips the superintendent with a working understanding of cost structure, quantity verification methods, productivity assumptions, and pricing validation so they can make informed daily decisions that protect the project budget.

Construction superintendents operate at the intersection of field execution and project financials. Every decision a superintendent makes -- crew sizing, equipment selection, work sequencing, material ordering, overtime authorization, change order acceptance -- has a direct cost impact. A superintendent who understands how estimates are built can:

- **Verify quantities** on pay applications and change orders rather than accepting them at face value
- **Validate productivity assumptions** against actual field conditions before committing to pricing
- **Identify scope gaps** between the estimate and the work being performed
- **Challenge unreasonable T&M charges** from subcontractors with data-backed pushback
- **Support value engineering** with practical alternatives that maintain quality while reducing cost
- **Code daily reports accurately** so cost tracking reflects reality
- **Anticipate cost overruns** by recognizing when field conditions deviate from estimate assumptions

This skill provides:
- Complete unit cost structure breakdown (labor, material, equipment, overhead, profit, contingency)
- Assembly-based estimating concepts with trade-specific component breakdowns
- CSI MasterFormat division structure with field-relevant cost coding guidance
- Quantity takeoff methods for every measurement type (area, linear, volume, count, weight)
- Comprehensive productivity rate tables by trade with crew compositions
- T&M pricing verification procedures and documentation requirements
- Bid review and leveling methodology for subcontractor selection
- Value engineering framework with common VE items by trade
- Waste factor tables by material category
- Productivity adjustment factors for field conditions

**Key Principle**: The superintendent's role in estimating is not to create estimates -- it is to validate them against field reality. The best estimates are built on assumptions. The superintendent is the person who knows whether those assumptions are correct.

---

## Unit Cost Structure

### The Total Cost Formula

Every line item in a construction estimate follows the same fundamental structure:

```
Total Cost = (Material + Labor Hours x Burdened Rate + Equipment) x (1 + OH%) x (1 + Profit%) + Contingency
```

Understanding each component allows the superintendent to dissect any price and determine whether it is reasonable.

### Labor Burden Breakdown

The "burdened" labor rate is the true cost of an hour of labor -- far more than the base wage. Subcontractors and self-perform crews carry these costs whether or not they appear on the bid breakdown.

**Labor Burden Components:**

| Component | Typical Rate/Percentage | Notes |
|-----------|------------------------|-------|
| Base Wage | Varies by trade/region | Journeyman rate, check prevailing wage if applicable |
| FICA (Social Security + Medicare) | 7.65% of base | Employer's matching portion |
| FUTA (Federal Unemployment) | 0.6% of first $7,000 | Effectively negligible on annualized basis |
| SUTA (State Unemployment) | 2-6% of first $7,000-$40,000 | Varies significantly by state and employer history |
| Workers' Compensation | 3-30% of base | Varies dramatically by trade classification |
| General Liability Insurance | 1-5% of labor cost | Trade-dependent, higher for roofing/structural |
| Health Insurance | $400-$1,200/month per employee | Union plans typically higher |
| Pension/401k | 3-8% of base | Union pension contributions often higher |
| Training/Apprenticeship | 0.5-2% of base | Required in many union agreements |
| Vacation/Holiday Pay | 3-6% of base | Paid time off, union holiday schedules |
| Small Tools/Consumables | 1-3% of base | Hand tools, blades, PPE replacement |

**Workers' Compensation Rates by Trade (Typical Ranges):**

| Trade | WC Rate Range | Classification Code |
|-------|---------------|-------------------|
| General Laborers | 8-15% | 5213 |
| Carpenters | 10-20% | 5403 |
| Ironworkers (structural) | 15-30% | 5040 |
| Electricians | 4-8% | 5190 |
| Plumbers | 5-10% | 5183 |
| Sheet Metal Workers | 6-12% | 5538 |
| Painters | 8-15% | 5474 |
| Roofers | 20-35% | 5551 |
| Equipment Operators | 6-12% | 3724 |
| Concrete Finishers | 10-18% | 5213 |

**Total Burden Multiplier by Trade (Typical):**

| Trade | Base Wage Example | Burden Multiplier | Fully Burdened Rate |
|-------|-------------------|-------------------|---------------------|
| Electrician | $45/hr | 1.40-1.50 | $63-$68/hr |
| Plumber | $48/hr | 1.40-1.50 | $67-$72/hr |
| Carpenter | $40/hr | 1.45-1.55 | $58-$62/hr |
| Laborer | $32/hr | 1.35-1.45 | $43-$46/hr |
| Ironworker | $50/hr | 1.55-1.65 | $78-$83/hr |
| Operator | $48/hr | 1.40-1.50 | $67-$72/hr |
| Sheet Metal | $46/hr | 1.42-1.52 | $65-$70/hr |
| Roofer | $38/hr | 1.55-1.65 | $59-$63/hr |
| Painter | $35/hr | 1.40-1.50 | $49-$53/hr |

**Field Application**: When a subcontractor submits T&M tickets at $95/hr for a journeyman electrician, you can check whether that rate is reasonable. If the base wage in your area is $45/hr and the burden multiplier is 1.45, the burdened rate is ~$65/hr. Add 10% overhead and 10% profit and you get ~$79/hr. The $95/hr rate may include a premium -- or may be inflated.

### Equipment Cost Components

Equipment costs consist of two major categories: ownership costs and operating costs.

**Ownership Costs (Fixed):**
- Depreciation: straight-line or hours-based over useful life
- Interest/cost of capital: financing cost of the asset
- Insurance: comprehensive, liability, physical damage
- Property tax: varies by jurisdiction
- Storage: when not deployed

**Operating Costs (Variable):**
- Fuel: consumption rate x fuel price x hours
- Maintenance and repair: planned PM + unplanned repairs
- Tires/tracks: replacement cost amortized over life
- Operator wages: if operated (included in some rates, not others)

**Ownership vs. Rental Decision Factors:**
- Utilization threshold: if equipment will be used >60-70% of available time, ownership is usually cheaper
- Duration: short-term (<3 months) favors rental; long-term (>6 months) favors ownership
- Maintenance capability: does the contractor have mechanics/shop capability?
- Mobilization: rental companies often include delivery; owned equipment requires transport
- Technology: rapidly changing technology (GPS grade control) may favor rental to avoid obsolescence

**Fuel Consumption by Equipment Class (Approximate):**

| Equipment | Fuel Consumption (gal/hr) | Notes |
|-----------|--------------------------|-------|
| Skid Steer Loader | 2-4 | Light duty |
| Backhoe Loader | 3-5 | Medium duty |
| Excavator (20-ton) | 4-7 | Varies with digging conditions |
| Excavator (35-ton) | 6-10 | Heavy excavation |
| Dozer (D5-D6) | 4-8 | Grade work |
| Dozer (D8-D9) | 8-15 | Heavy pushing |
| Wheel Loader (2-3 CY) | 4-7 | Loading trucks |
| Motor Grader | 4-7 | Fine grading |
| Vibratory Roller | 3-5 | Compaction |
| Concrete Pump (truck-mounted) | 5-8 | During pumping operations |
| Crane (50-100 ton) | 4-8 | Varies with load/swing |
| Crane (200+ ton) | 8-15 | Heavy lifts |
| Aerial Lift (60-80 ft) | 1-3 | Boom/scissor lift |

### Overhead Types

**Job Overhead (General Conditions) -- Typically 8-15% of Direct Cost:**

| Item | Typical Monthly Cost | Notes |
|------|---------------------|-------|
| Superintendent salary | $8,000-$15,000 | Fully burdened |
| Project manager (allocated) | $4,000-$8,000 | Partial allocation typical |
| Field office/trailer | $800-$2,500 | Lease + setup/teardown |
| Temporary utilities | $500-$2,000 | Power, water, phone, internet |
| Temporary facilities | $1,000-$3,000 | Toilets, dumpsters, fencing |
| Project insurance | Varies | Builder's risk, OCIP/CCIP |
| Bonds (P&P) | 1-3% of contract | Performance and payment |
| Small tools | $500-$2,000 | Consumables, replacement |
| Safety equipment | $500-$1,500 | Signs, barricades, PPE supply |
| Clean-up labor | $2,000-$5,000 | Daily/weekly clean-up crew |
| Testing and inspection | $1,000-$4,000 | Third-party testing coordination |
| Surveying and layout | $1,000-$3,000 | Survey crew or subcontractor |
| Winter protection | $2,000-$10,000 | Heating, hoarding (seasonal) |
| Temporary protection | $500-$2,000 | Floor/finish protection |

**Home Office Overhead -- Typically 5-10% of Revenue:**
- Executive salaries and benefits
- Estimating department
- Accounting and payroll
- Human resources
- Office rent and utilities
- Legal and professional services
- Marketing and business development
- IT and software
- Vehicle fleet (non-project)
- Corporate insurance

### Profit and Markup

**Typical Profit Ranges by Project Type:**

| Project Type | Typical Profit Range | Notes |
|-------------|---------------------|-------|
| Competitive hard bid (public) | 3-6% | Low margin, high volume strategy |
| Competitive hard bid (private) | 5-8% | Slightly higher than public |
| Negotiated (CM at-risk) | 8-12% | Pre-construction services add value |
| Design-build | 8-15% | Higher risk = higher reward |
| Specialty/niche work | 10-20% | Limited competition |
| Emergency/fast-track | 15-25% | Premium for acceleration |
| T&M work | 10-15% on labor, 10-15% on material | Per contract terms |

**Market Conditions Impact:**
- Hot market (high demand, low supply of subs): profit margins decrease due to higher sub pricing
- Slow market (low demand, high competition): profit margins decrease due to aggressive bidding
- Ideal conditions: moderate workload with selective bidding allows healthy margins
- Relationship work: repeat clients may accept higher margins for reliability and quality

### Contingency

**Design Contingency by Project Phase:**

| Design Phase | Contingency Range | Rationale |
|-------------|-------------------|-----------|
| Conceptual/programming | 15-25% | High uncertainty, scope undefined |
| Schematic design (30%) | 10-20% | Major systems defined, details unknown |
| Design development (60%) | 7-15% | Details emerging, some coordination gaps |
| Construction documents (90%) | 5-10% | Most details resolved, minor gaps |
| Bid documents (100%) | 3-5% | Final documents, known scope |

**Construction Contingency -- Typically 3-5%:**
- Covers unforeseen field conditions not identified in plans/specs
- NOT a slush fund for scope changes (those are change orders)
- Drawn down through formal approval process
- Common uses: unexpected rock, contaminated soil, hidden conditions in renovation
- Track remaining contingency monthly as percentage of original budget

**Owner Contingency -- Typically 5-10%:**
- Covers owner-initiated changes, market fluctuations, permitting changes
- Managed by owner, not contractor
- Should be separate from contractor contingency
- Reduces as design progresses and scope firms up

---

## Assembly-Based Estimating

### What Assemblies Are

An assembly is a pre-configured bundle that combines all materials, labor, equipment, and incidental items needed to complete one unit of a defined work element. Instead of pricing individual components (one stud, one screw, one piece of track), the estimator prices the entire assembly as a unit (one linear foot of interior partition wall).

Assemblies encode **productivity assumptions** -- the labor hours per unit reflect expected field conditions, crew composition, and work complexity. This is where the estimate meets the field: if the assembly assumes 0.08 labor hours per square foot of drywall hanging, and the field is achieving 0.12 hours (50% slower), the project will overrun labor.

### Assembly Examples by Trade

**Concrete Footing Assembly (per LF of continuous footing, 24" wide x 12" deep):**

| Component | Quantity per LF | Unit | Unit Cost | Extended |
|-----------|----------------|------|-----------|----------|
| Formwork (2x material, ties, oil) | 4 SF | SF | $2.50 | $10.00 |
| Form labor (set and strip) | 0.15 | MH | $58.00 | $8.70 |
| Rebar (#5 @ 12" OC each way) | 3.5 LB | LB | $0.85 | $2.98 |
| Rebar labor (place and tie) | 0.04 | MH | $62.00 | $2.48 |
| Concrete (4000 PSI) | 0.074 | CY | $165.00 | $12.21 |
| Concrete placing labor | 0.03 | MH | $55.00 | $1.65 |
| Pump (amortized) | 0.074 | CY | $15.00 | $1.11 |
| Vibrating/finishing | 0.02 | MH | $55.00 | $1.10 |
| Curing compound | 1.0 | SF | $0.15 | $0.15 |
| **Total Direct Cost per LF** | | | | **$40.38** |

**Metal Stud Interior Partition Assembly (per SF, 3-5/8" studs @ 16" OC, one side GWB, Level 4 finish, painted):**

| Component | Quantity per SF | Unit | Unit Cost | Extended |
|-----------|----------------|------|-----------|----------|
| Floor/ceiling track | 0.25 | LF | $0.65 | $0.16 |
| Metal studs 3-5/8" 25ga | 0.75 | LF | $0.80 | $0.60 |
| Stud labor (layout, cut, install) | 0.018 | MH | $55.00 | $0.99 |
| 5/8" Type X GWB (one side) | 1.05 | SF | $0.55 | $0.58 |
| GWB screws | 0.05 | LB | $2.00 | $0.10 |
| Hanging labor | 0.008 | MH | $52.00 | $0.42 |
| Joint compound | 0.015 | GAL | $12.00 | $0.18 |
| Paper tape | 0.12 | LF | $0.02 | $0.00 |
| Taping labor (Level 4) | 0.012 | MH | $55.00 | $0.66 |
| Primer | 0.012 | GAL | $25.00 | $0.30 |
| Finish paint (2 coats) | 0.016 | GAL | $35.00 | $0.56 |
| Paint labor | 0.010 | MH | $48.00 | $0.48 |
| **Total Direct Cost per SF** | | | | **$5.03** |

**Plumbing Rough-In Assembly (per fixture, lavatory sink):**

| Component | Quantity | Unit | Unit Cost | Extended |
|-----------|----------|------|-----------|----------|
| 1/2" copper supply (H&C) | 12 | LF | $3.50 | $42.00 |
| Supply fittings (elbows, tees) | 6 | EA | $4.50 | $27.00 |
| 1-1/2" DWV pipe | 8 | LF | $5.00 | $40.00 |
| DWV fittings (P-trap, wye, vent) | 4 | EA | $8.00 | $32.00 |
| Hangers and supports | 6 | EA | $3.00 | $18.00 |
| Supply valves (angle stops) | 2 | EA | $12.00 | $24.00 |
| Pipe insulation | 12 | LF | $1.50 | $18.00 |
| Plumber labor (rough-in) | 6.0 | MH | $72.00 | $432.00 |
| Testing (pressure/DWV) | 0.5 | MH | $72.00 | $36.00 |
| **Total Direct Cost per Fixture** | | | | **$669.00** |

**Electrical Circuit Assembly (per 20A branch circuit, 120V, typical office):**

| Component | Quantity | Unit | Unit Cost | Extended |
|-----------|----------|------|-----------|----------|
| 12/2 MC cable | 75 | LF | $1.20 | $90.00 |
| 3/4" EMT conduit (exposed areas) | 15 | LF | $1.80 | $27.00 |
| EMT fittings (connectors, couplings) | 8 | EA | $1.50 | $12.00 |
| 4" square boxes | 4 | EA | $3.50 | $14.00 |
| Device rings/covers | 4 | EA | $1.25 | $5.00 |
| Receptacles (duplex, 20A) | 4 | EA | $4.50 | $18.00 |
| Wire nuts/connectors | 12 | EA | $0.30 | $3.60 |
| Circuit breaker (20A, 1-pole) | 1 | EA | $8.00 | $8.00 |
| Supports/hangers | 8 | EA | $2.00 | $16.00 |
| Electrician labor | 5.0 | MH | $68.00 | $340.00 |
| **Total Direct Cost per Circuit** | | | | **$533.60** |

**Roofing Assembly (per square = 100 SF, 60-mil TPO fully adhered):**

| Component | Quantity | Unit | Unit Cost | Extended |
|-----------|----------|------|-----------|----------|
| TPO membrane (60 mil) | 105 | SF | $1.10 | $115.50 |
| Polyiso insulation (2 layers, R-30) | 105 | SF | $1.80 | $189.00 |
| Cover board (1/2" HD polyiso) | 105 | SF | $0.65 | $68.25 |
| Insulation adhesive | 1 | unit | $35.00 | $35.00 |
| Membrane bonding adhesive | 2 | GAL | $28.00 | $56.00 |
| Termination bar and sealant | 4 | LF | $2.50 | $10.00 |
| Flashing (pre-formed corners, pipe boots) | Allow | | | $25.00 |
| Roofing labor (install) | 3.5 | MH | $58.00 | $203.00 |
| **Total Direct Cost per Square** | | | | **$701.75** |

### How Assemblies Encode Productivity

Every assembly contains embedded productivity assumptions:
- **Labor hours per unit**: the core assumption connecting estimate to field performance
- **Crew composition**: assumed skill mix (journeyman vs. apprentice ratio)
- **Work conditions**: assumed height, access, weather, congestion
- **Sequence**: assumed installation order and method
- **Equipment**: assumed equipment availability (crane, pump, lift)

**When field conditions differ from assembly assumptions, the estimate is wrong.** The superintendent's job is to recognize when actual conditions deviate and flag the impact early.

### Assembly-to-WBS Mapping

Assemblies in the estimate map to Work Breakdown Structure (WBS) elements in the schedule:
- Assembly = the cost of a work element
- WBS activity = the time to complete that work element
- The link: labor hours in the assembly / crew hours per day = activity duration

Example: 500 LF of continuous footing x 0.15 MH/LF forming labor = 75 man-hours. With a 4-person forming crew working 8 hours/day = 32 crew-hours/day. Duration = 75/32 = 2.3 days (round to 3 days with setup/cleanup).

### Assembly Adjustment Factors

| Factor | Adjustment Range | When to Apply |
|--------|-----------------|---------------|
| Location (urban premium) | +5-15% labor | Dense urban, limited staging, traffic |
| Location (rural premium) | +5-10% labor | Travel time, limited labor pool |
| Height above ground | +1-2% per 10 ft above grade | Scaffold/lift time, material handling |
| Weather (hot >95F) | +10-20% labor | Reduced productivity, hydration breaks |
| Weather (cold <32F) | +10-25% labor | Heated enclosures, material protection |
| Congestion/tight spaces | +15-30% labor | Renovation, occupied spaces |
| Overtime (>40 hr/week) | +15-25% per OT hour | Fatigue factor reduces productivity |
| Night/shift work | +10-20% labor | Lighting, coordination, fatigue |
| Learning curve (first units) | +15-25% labor | New crew, unfamiliar work |
| Repetitive work (later units) | -5-15% labor | Crew becomes efficient |

---

## Waste Factor Reference

Waste factors account for material lost during installation due to cutting, breakage, over-ordering, damage, and field conditions. Apply these factors to net (plan) quantities to arrive at order quantities.

| Material | Typical Waste % | Low (controlled) | High (complex) | Notes |
|----------|----------------|-------------------|-----------------|-------|
| Ready-mix concrete (slabs) | 5% | 3% | 8% | Pump loss, over-pour, finishing waste |
| Ready-mix concrete (footings) | 3% | 2% | 5% | Form accuracy dependent |
| Ready-mix concrete (walls) | 7% | 5% | 10% | Form blowout risk, pump waste |
| Rebar | 5% | 3% | 8% | Lap splices, cut-off waste |
| Structural steel | 3% | 2% | 5% | Shop fabrication waste |
| CMU (block) | 5% | 3% | 8% | Breakage, cutting waste |
| Brick | 8% | 5% | 12% | Breakage, cutting at openings |
| Drywall | 10% | 7% | 15% | Cutouts, damage, odd room shapes |
| Insulation (batt) | 5% | 3% | 8% | Cutting waste at framing |
| Insulation (rigid) | 7% | 5% | 10% | Cutting waste, breakage |
| Lumber (framing) | 10% | 7% | 15% | End cuts, defects, damage |
| Plywood/OSB (sheathing) | 8% | 5% | 12% | Cut-off waste, damage |
| Roofing membrane (TPO/EPDM) | 10% | 7% | 15% | Seam overlaps, flashing waste |
| Asphalt shingles | 10% | 7% | 15% | Starter, ridge, hip cuts |
| Paint | 10% | 5% | 15% | Touch-up, coverage variance, texture |
| Ceramic tile | 10% | 7% | 15% | Cuts at edges, breakage, patterns |
| Carpet | 8% | 5% | 12% | Seaming waste, room geometry |
| Pipe (all types) | 5% | 3% | 8% | Fittings allowance, cut waste |
| Conduit | 5% | 3% | 8% | Bends, cut waste |
| Wire/cable | 3% | 2% | 5% | Pull lengths, termination waste |
| Ductwork | 5% | 3% | 8% | Fittings allowance, custom pieces |

### Waste Factor Application Notes

- These are **default** waste factors. When `project-config.json` has project-specific waste factors, use those instead.
- Complex geometry, multi-story work, and tight access increase waste toward the high end of each range.
- Material stored properly on-site (covered, level, protected from traffic) reduces breakage waste toward the low end.
- Pre-fabrication (off-site) significantly reduces field waste -- shop-fabricated assemblies typically achieve the low-end waste factor or better.

---

## Assembly-to-Division Mapping

Assembly chains in `plans-spatial.json` group elements by physical construction sequence (e.g., "Footing F1" = excavation + formwork + rebar + concrete + strip). CSI division budgets in `cost-data.json` group costs by trade/material type (e.g., Division 03 = all concrete, Division 05 = all metals).

**One assembly spans multiple divisions:**

| Assembly Step | CSI Division | Cost Category |
|--------------|-------------|---------------|
| Footing F1 — Excavation | 31 (Earthwork) | Equipment + labor |
| Footing F1 — Formwork | 03 (Concrete) | Material + labor |
| Footing F1 — Rebar | 03 (Concrete) | Material + labor |
| Footing F1 — Concrete pour | 03 (Concrete) | Material + equipment + labor |
| Footing F1 — Backfill | 31 (Earthwork) | Equipment + labor |
| Footing F1 — Waterproofing | 07 (Thermal & Moisture) | Material + labor |

**Mapping workflow:**
1. For each assembly chain in `plans-spatial.json → assembly_chains[]`, identify constituent steps
2. Each step maps to a CSI division via `estimating-intelligence` division classification
3. Quantity from the assembly step × unit cost from division budget = cost allocation
4. Sum allocations per division to validate against `cost-data.json → budget_by_division[]`

**Common multi-division assemblies:**
- **Exterior wall**: 04 (masonry) + 05 (structural steel lintels) + 07 (insulation, flashing, sealants) + 08 (windows/doors) + 09 (interior finish)
- **Roof**: 05 (steel deck) + 07 (insulation, membrane, flashing) + 22 (roof drains) + 23 (RTU curbs)
- **Slab on grade**: 31 (subgrade prep) + 03 (concrete, rebar, vapor barrier) + 09 (floor finish)
- **MEP rough-in in wall**: 22 (plumbing) + 23 (HVAC) + 26 (electrical) — all hidden in same wall cavity

**Reconciliation check:** After estimates are complete, compare:
- Total assembly-based estimate (sum of all assemblies × unit costs) vs.
- Total division-based budget (sum of `budget_by_division[].original_amount`)
- Variance >5% should be investigated — likely indicates missing scope in one method

---

> **Extended reference**: Detailed examples, templates, scoring rubrics, and best practices are in `references/skill-detail.md`.
