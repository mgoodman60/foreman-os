# CPM and Last Planner System Integration Reference

## Overview
The Critical Path Method (CPM) and the Last Planner System (LPS) are complementary, not competing, scheduling methodologies. CPM provides the strategic master schedule (milestones, critical path, float analysis). LPS provides the tactical execution plan (reliable weekly promises, constraint removal, continuous improvement). Together they form a hybrid scheduling model that is becoming the industry standard.

## The Hybrid Model

### CPM Layer (Strategic — Top Down)
- **Master Schedule**: Overall project timeline, contractual milestones
- **Critical Path**: Identifies the longest path and activities with zero float
- **Float Analysis**: Shows where schedule flexibility exists
- **What-If Scenarios**: Models the impact of delays, acceleration, resequencing
- **Baseline Management**: Contractual benchmark for progress measurement

### LPS Layer (Tactical — Bottom Up)
- **Phase Scheduling**: Collaborative planning for each construction phase
- **Lookahead Planning**: 6-week rolling window of upcoming work
- **Constraint Analysis**: Systematic identification and removal of work blockers
- **Weekly Work Plans**: Reliable commitments from trade foremen
- **PPC Tracking**: Percent Plan Complete measurement and trending
- **Variance Analysis**: Root cause investigation when commitments fail

### How They Connect
```
CPM Master Schedule
  ↓ (decompose into)
Phase Schedules (collaborative planning sessions)
  ↓ (decompose into)
6-Week Lookahead (constraint identification)
  ↓ (make-ready process: remove constraints)
Weekly Work Plan (LPS commitments)
  ↓ (execute and measure)
PPC Results
  ↓ (feedback loop)
CPM Schedule Update (actuals fed back into master schedule)
```

## PPC Benchmarks and Actions

| PPC Range | Assessment | Actions |
|-----------|-----------|---------|
| >85% | Healthy — team is reliable | Continue current planning rhythm. Focus on maintaining discipline. |
| 70-85% | Caution — reliability needs work | Increase constraint analysis frequency. Review variance categories weekly. Identify top 3 root causes. |
| 60-70% | Alert — significant reliability gap | Trigger recovery schedule analysis. Escalate to PM. Review resource allocation. Conduct focused improvement workshop. |
| <60% | Critical — system breakdown | Emergency planning session. Re-baseline weekly plan process. One-on-one meetings with underperforming trade foremen. Consider crew changes. |

### Industry Benchmarks
- **CPM-only projects** (no LPS): Typical PPC equivalent of 15-45%
- **LPS implementation** (first 8 weeks): PPC typically 55-70% and improving
- **Mature LPS practice** (3+ months): PPC typically 80-90%
- **LPS + Takt Time planning**: PPC approaching 95-100%

## Variance Category Analysis

When tasks fail, categorize why. The nine variance categories track root causes:

| Category | Description | Typical % of Total |
|----------|-----------|-------------------|
| Prerequisites | Prior work not complete/accepted | 25-35% |
| Material | Material not on site or not approved | 15-25% |
| Labor | Crew not available or insufficient | 10-15% |
| Equipment | Equipment not available or down | 5-10% |
| Design | Drawings not current, RFIs unanswered | 5-15% |
| Weather | Weather prevented work | 5-15% |
| Space/Access | Work area not clear | 5-10% |
| Rework | Work had to be redone | 3-8% |
| Overcommitment | Too much committed for capacity | 5-10% |

Track these weekly. Pareto analysis every 4 weeks reveals the top blockers.

## Schedule Recovery Protocol

When PPC trends downward for 3+ consecutive weeks:

### Step 1: Diagnose
- Run Pareto analysis on variance categories
- Identify if the problem is systemic (multiple categories) or concentrated (1-2 categories)
- Review constraint log for patterns

### Step 2: Targeted Intervention
Based on top variance categories:
- **Prerequisites dominant**: Improve handoff protocols, add inspection buffer time
- **Material dominant**: Increase procurement monitoring, earlier constraint screening
- **Labor dominant**: Verify crew commitments earlier, develop backup crew plan
- **Design dominant**: Escalate RFI/submittal turnaround to owner/architect
- **Weather dominant**: Build weather buffers, identify indoor backup work

### Step 3: CPM Recovery Analysis
- Identify critical path activities affected by PPC decline
- Determine if float has been consumed
- Model recovery options: fast-tracking, crashing, resequencing
- Present options to PM with cost/risk analysis

### Step 4: Adjust LPS Process
- Increase constraint screening lead time (from 4 weeks to 6 weeks)
- Add mid-week check-in on critical commitments
- Consider daily PPC tracking for critical path activities
- Reduce commitment scope (smaller, more achievable promises)

### Step 5: Monitor Recovery
- Track PPC weekly against recovery target
- Verify CPM schedule is being updated with actuals
- Report progress to PM and owner as appropriate

## Constraint Analysis Timing

The make-ready process operates on a rolling timeline:

| Timeframe | Activity | Purpose |
|-----------|----------|---------|
| 6 weeks out | Identify constraints | Flag potential blockers early |
| 4 weeks out | Assign constraint owners | Accountability for resolution |
| 3 weeks out | Active make-ready | Work to remove constraints |
| 2 weeks out | Verify clearance | Confirm constraints resolved |
| 1 week out | Final check | Last opportunity before commitment |
| This week | Execute | Constraint-free commitments only |

## Integration with Foreman OS Skills

### Feeding PPC Back to CPM
When PPC results are captured via the last-planner skill:
1. Completed commitments → update CPM activity status (% complete or actual finish)
2. Incomplete commitments → flag CPM activities at risk
3. Constraint log items → map to CPM predecessors that need attention

### PPC Correlation with Schedule Metrics
Track these pairs over time:
- **PPC trend + SPI**: Rising PPC → SPI should stabilize or improve
- **PPC trend + BEI**: PPC measures reliability; BEI measures progress against baseline
- **High PPC + Low BEI**: Team is reliable but working on non-critical activities — redirect focus
- **Low PPC + High BEI**: Unusual — few commitments made, most completed
- **Low PPC + Low BEI**: Systemic problem — both reliability and progress failing
