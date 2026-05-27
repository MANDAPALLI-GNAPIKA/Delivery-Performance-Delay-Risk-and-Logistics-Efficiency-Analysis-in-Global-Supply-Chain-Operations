# Delivery Performance, Delay Risk, and Logistics Efficiency Analysis in Global Supply Chain Operations
## APL Logistics (KWE Group) — Supply Chain Analytics
### Research Paper — Unified Mentor Data Analyst Internship

---

## Executive Summary

This research paper provides a comprehensive diagnostic analysis of APL Logistics' global delivery performance using 180,519 order records. The dataset spans 40 operational fields covering customer demographics, order details, shipping logistics, and delivery outcomes across five global markets — LATAM, Europe, Pacific Asia, USCA, and Africa.

**Key findings at a glance:**
- **54.8% of all orders carry late delivery risk** — a majority of shipments are delayed, indicating a systemic issue, not an isolated one
- **First Class shipping has the highest late delivery rate at 95.3%**, counterintuitively outperforming Standard Class only in average delay days but failing dramatically in risk incidence
- **Standard Class, despite being the slowest mode, has the lowest late risk at 38.1%** — likely because scheduled expectations are set conservatively
- **Market-level late risk is nearly uniform (~54–55%)** across all regions, suggesting the delay problem is operational and systemic rather than regionally concentrated
- **Central Africa (58.0%) and Central Asia (55.3%)** are the highest-risk regions by order proportion
- **Customer segments show negligible difference** in delay exposure, meaning no premium or enterprise segment receives preferential treatment

---

## 1. Introduction

### 1.1 Background

APL Logistics (part of the KWE Group) operates a high-volume, multi-region global supply chain handling orders across diverse product categories — from footwear and apparel to electronics and outdoor equipment. The organization ships to customers across LATAM, Europe, Pacific Asia, USCA (US/Canada), and Africa through four shipping modes: Standard Class, Second Class, First Class, and Same Day.

Despite collecting rich transactional data, the organization lacks structured process efficiency metrics that answer:
- Are deliveries meeting scheduled timelines?
- Which shipping modes are underperforming relative to their promises?
- Which regions and markets carry concentrated delay risk?
- Are high-value customer segments receiving disproportionate delay exposure?

### 1.2 Problem Statement

The core problem is **reactive logistics management**. Without structured delivery performance metrics, logistics teams identify bottlenecks only after SLA violations occur rather than predicting and preventing them. Key gaps include:

- No measurement of on-time vs delayed delivery rates
- No understanding of systemic vs regional delay drivers
- No visibility into which shipping modes are statistically unreliable
- No customer-segment-level SLA risk assessment

### 1.3 Objectives

**Primary:**
- Calculate on-time delivery rate and late delivery risk distribution
- Compute delivery delay gap (actual vs scheduled shipping days)
- Identify high-risk shipping modes, regions, and market segments

**Secondary:**
- Evaluate financial impact of delays on order profitability
- Quantify SLA risk by customer segment
- Provide actionable recommendations for operational improvement

---

## 2. Dataset Description

| Field | Description |
|---|---|
| Days for shipping (real) | Actual days taken (range: 0–6) |
| Days for shipment (scheduled) | Planned days (range: 0–4) |
| Late_delivery_risk | Binary indicator: 1 = late, 0 = on-time |
| Delivery Status | Categorical: Late delivery, Shipping on time, Advance shipping, Shipping canceled |
| Shipping Mode | Standard Class, Second Class, First Class, Same Day |
| Market | LATAM, Europe, Pacific Asia, USCA, Africa |
| Order Region | 23 sub-regional classifications |
| Customer Segment | Consumer, Corporate, Home Office |

**Dataset size:** 180,519 orders across 40 fields
**Data quality:** Minimal nulls — only 8 missing last names and 3 missing zip codes. No records dropped.

**Derived field:**
```
Delay Gap = Days for shipping (real) − Days for shipment (scheduled)
```
- Negative = Early delivery
- Zero = On-time
- Positive = Delayed

---

## 3. Analytical Methodology

### 3.1 Data Cleaning & Validation
- Encoding: File uses Latin-1 (ISO-8859-1) encoding due to accented characters in customer names and city fields (e.g., "EE. UU.")
- No duplicate records or invalid shipping durations found
- Delivery Status and Late_delivery_risk are perfectly aligned (98,977 records each for Late delivery / Late_delivery_risk=1)

### 3.2 Delivery Gap Classification
Orders are classified into three categories based on Delay Gap:

| Class | Condition | Count | % |
|---|---|---|---|
| Early | Delay Gap < 0 | 43,366 | 24.0% |
| On-Time | Delay Gap = 0 | 33,753 | 18.7% |
| Delayed | Delay Gap > 0 | 103,400 | 57.3% |

### 3.3 KPI Framework

| KPI | Formula | Value |
|---|---|---|
| On-Time Delivery Rate | On-time orders ÷ Total | 45.2% |
| Late Delivery Risk Ratio | Late risk orders ÷ Total | 54.8% |
| Average Delivery Delay | Mean(Delay Gap) | +0.57 days |
| Avg Real Shipping Days | Mean(Days for shipping real) | 3.50 days |
| Avg Scheduled Days | Mean(Days for shipment scheduled) | 2.93 days |

---

## 4. Exploratory Data Analysis

### 4.1 Overall Delivery Performance

Out of 180,519 orders:
- **98,977 (54.8%) carry Late Delivery Risk**
- **81,542 (45.2%) are on-time or early**

The Delivery Status breakdown:
| Status | Count | % |
|---|---|---|
| Late delivery | 98,977 | 54.8% |
| Advance shipping | 41,592 | 23.0% |
| Shipping on time | 32,196 | 17.8% |
| Shipping canceled | 7,754 | 4.3% |

Notably, advance shipping (early) accounts for 23% — meaning the system does have capacity for ahead-of-schedule delivery, but it is unevenly distributed.

### 4.2 Delay Gap Distribution

| Gap (Days) | Orders | % |
|---|---|---|
| -2 (2 days early) | 21,666 | 12.0% |
| -1 (1 day early) | 21,700 | 12.0% |
| 0 (on-time) | 33,753 | 18.7% |
| +1 (1 day late) | 60,647 | 33.6% |
| +2 (2 days late) | 28,718 | 15.9% |
| +3 (3 days late) | 7,052 | 3.9% |
| +4 (4 days late) | 6,983 | 3.9% |

The most common outcome is a **1-day delay**, affecting 33.6% of all orders — suggesting a systemic underestimation of transit time in scheduling, not a catastrophic logistics failure.

### 4.3 Shipping Mode Efficiency Analysis

| Shipping Mode | Orders | Late Risk | Late % | Avg Delay Gap | Avg Real Days | Avg Scheduled Days |
|---|---|---|---|---|---|---|
| First Class | 27,814 | 26,513 | **95.3%** | +1.00 | 2.00 | 1.00 |
| Second Class | 35,216 | 26,987 | **76.6%** | +1.99 | 3.99 | 2.00 |
| Same Day | 9,737 | 4,454 | **45.7%** | +0.48 | 0.48 | 0.00 |
| Standard Class | 107,752 | 41,023 | **38.1%** | −0.004 | 3.996 | 4.00 |

**Critical finding:** First Class is by far the worst performer with a 95.3% late risk rate. This is a paradox — a premium shipping mode is the most unreliable. The cause is likely **overpromising**: First Class promises 1-day delivery, but real transit consistently takes 2 days, meaning virtually every First Class shipment is technically "late."

Standard Class, scheduled at 4 days and consistently delivering in ~4 days, has only a 38.1% late risk — the best of any mode.

**Implication:** The issue is not delivery speed but **schedule accuracy**. First Class and Second Class have systematically optimistic scheduled times that real operations cannot meet.

### 4.4 Regional & Market Analysis

**By Market:**
| Market | Orders | Late Risk % | Avg Delay |
|---|---|---|---|
| Europe | 50,252 | 55.2% | +0.57 |
| Pacific Asia | 41,260 | 55.0% | +0.57 |
| USCA | 25,799 | 54.8% | +0.57 |
| Africa | 11,614 | 54.6% | +0.56 |
| LATAM | 51,594 | 54.4% | +0.56 |

Market-level delay rates are remarkably uniform (54.4%–55.2%), with less than 1 percentage point separating best from worst. This strongly implies the delay driver is **not regional infrastructure** but rather a **global scheduling policy flaw** — the same overpromised schedule times are applied uniformly across all markets.

**By Region (Top 5 Highest Risk):**
| Region | Late Risk % | Avg Delay |
|---|---|---|
| Central Africa | 58.0% | +0.64 |
| South Asia | 56.3% | +0.60 |
| East Africa | 55.9% | +0.57 |
| South of USA | 55.8% | +0.58 |
| Western Europe | 55.8% | +0.60 |

Central Africa and South Asia show slightly elevated delay, possibly reflecting genuine infrastructure challenges on top of the global scheduling issue.

### 4.5 Customer Segment Impact

| Segment | Orders | Late Risk % | Avg Delay |
|---|---|---|---|
| Consumer | 93,504 | 54.8% | +0.56 |
| Corporate | 54,789 | 54.7% | +0.56 |
| Home Office | 32,226 | 55.1% | +0.58 |

No segment receives meaningful preferential treatment. Corporate clients — who typically negotiate SLA guarantees — face the same 54.7% late risk as consumer customers. This represents a significant SLA exposure for enterprise relationships.

### 4.6 Category & Department Analysis

**Highest delay risk categories:**
| Category | Late Risk % |
|---|---|
| Golf Bags & Carts | 68.9% |
| Lacrosse | 60.1% |
| Pet Supplies | 58.9% |
| Cameras | 58.1% |
| Fitness Accessories | 57.0% |

Specialized/niche categories show above-average delay rates, possibly due to less predictable sourcing or fulfillment routing.

### 4.7 Financial Impact of Delays

| Metric | Late Orders | On-Time Orders | Difference |
|---|---|---|---|
| Avg Benefit per Order | $21.62 | $22.40 | −$0.78 |
| Avg Profit Ratio | 0.1197 | 0.1218 | −0.0021 |

Late deliveries generate slightly lower average profit, though the difference is small in absolute terms. Across 98,977 late orders, the aggregate benefit gap is approximately **$77,000** — a meaningful but not catastrophic financial signal. Reputational and SLA penalty costs are likely more significant.

### 4.8 Order Status Distribution

| Status | Count |
|---|---|
| COMPLETE | 59,491 (32.9%) |
| PENDING_PAYMENT | 39,832 (22.1%) |
| PROCESSING | 21,902 (12.1%) |
| PENDING | 20,227 (11.2%) |
| CLOSED | 19,616 (10.9%) |
| CANCELED | 3,692 (2.0%) |

3,692 canceled orders (2.0%) represent lost revenue and potential delay-driven churn.

---

## 5. Key Findings

### Finding 1: Majority of Orders Are Late — This Is Systemic, Not Exceptional
A 54.8% late delivery risk rate is not a spike or an anomaly — it is the baseline operating condition. The uniformity across markets (all within 1%) confirms this is driven by global policy (scheduling), not regional execution.

### Finding 2: First Class Shipping Is Statistically Broken
A 95.3% late risk rate for First Class means it almost never delivers on its promise. The scheduled time of 1 day vs actual transit of 2 days is the direct cause. This mode is **actively misleading customers** about expected delivery.

### Finding 3: Standard Class Is the Most Reliable Mode
Standard Class's 38.1% late rate — the lowest of any mode — is achieved not by being fast but by being honest. Its 4-day schedule matches its actual ~4-day delivery. **Reliability comes from schedule accuracy, not speed.**

### Finding 4: Corporate Customers Have No SLA Advantage
Corporate clients face the same ~54.7% late risk as consumers. If corporate contracts include SLA guarantees, APL Logistics is systematically in breach of those agreements for over half of corporate orders.

### Finding 5: The Primary Fix Is Scheduling, Not Logistics Infrastructure
Since delay rates are uniform across all 5 markets and 23 regions, and the average delay is only +0.57 days, the solution is not to build faster logistics — it is to **extend scheduled delivery estimates by 1 day** for First Class and Second Class modes.

---

## 6. Recommendations

### Immediate Actions (0–30 days)
1. **Recalibrate First Class scheduled delivery from 1 day to 2 days.** This single change would reduce First Class late risk from 95.3% to near 0% without any operational change.
2. **Recalibrate Second Class from 2 days to 4 days.** Second Class actual delivery is consistently ~4 days; the 2-day promise is chronically unmet.
3. **Implement threshold alerts** in the dashboard when any shipping mode's late risk exceeds 50% in a rolling 7-day window.

### Short-Term Actions (30–90 days)
4. **Audit Corporate SLA contracts** against actual delivery performance. With 54.7% late rate, legal and financial exposure from SLA penalties is significant.
5. **Investigate niche category delays** (Golf Bags, Lacrosse, Pet Supplies) — these may have fulfillment routing issues not shared by high-volume categories.
6. **Separate Same Day scheduling by region** — Same Day's 45.7% late rate may vary significantly by geography due to last-mile infrastructure differences.

### Strategic Actions (90+ days)
7. **Build a predictive delay model** using Shipping Mode, Region, Category, and Delay Gap as features to flag high-risk orders before dispatch.
8. **Introduce tiered customer prioritization** — ensure Corporate and enterprise SLA orders are routed through the most reliable mode (Standard Class) unless urgency justifies the tradeoff.
9. **Track cancellation rate as a delay-outcome KPI** — the 2% cancellation rate may be partially delay-driven; correlation analysis would confirm this.

---

## 7. Conclusion

This analysis establishes a clear diagnostic picture: APL Logistics' delivery delay problem is systemic and is primarily caused by **chronically optimistic scheduling** for First Class and Second Class shipping modes. The data consistently shows that actual delivery times exceed scheduled times by a predictable margin — meaning this is a solvable problem through administrative correction, not capital investment.

The KPI framework developed here — On-Time Delivery Rate, Average Delay Gap, Late Delivery Risk Ratio, Shipping Mode Efficiency Index, and Regional Delay Index — provides a reusable monitoring layer for ongoing operational accountability.

---

## 8. Appendix: Data Cleaning Notes

1. File encoded as Latin-1 (ISO-8859-1) — loaded with `encoding='latin1'`
2. Derived column: `Delay_Gap = Days for shipping (real) − Days for shipment (scheduled)`
3. Delivery classification: Early (gap < 0), On-Time (gap = 0), Delayed (gap > 0)
4. 8 null last names and 3 null zip codes retained — not used in analysis
5. 7,754 "Shipping canceled" records included in Late_delivery_risk computation (per original dataset labeling)

---

*Dataset: APL_Logistics.csv — 180,519 orders, 40 fields*
*Author: Unified Mentor Data Analyst Internship Project*
