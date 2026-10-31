# QuickBite Analytics – Executive Final Report
## Restaurant Performance, Delivery Time and Customer Rating Analysis
### Team: Data Knights | CODEGNAN Hackathon DA-07

---

> **DISCLAIMER:** All data in this project is explicitly **SYNTHETIC** and was generated
> for demonstration purposes in the CODEGNAN DA-07 Hackathon. It does not represent
> actual business records of any company.

---

## 1. Executive Summary

QuickBite is a food delivery platform operating across three Indian cities:
**Hyderabad**, **Visakhapatnam**, and **Vijayawada**. Over a simulated 12-month period
(January–December 2024), the platform processed **100,000 orders** across
**4,000 partner restaurants**, served by **2,000 delivery riders** and **20,000 customers**.

### At a Glance

| KPI | Value | Status |
|---|---|---|
| Total Orders | 100,000 | ✅ |
| Completed Orders | 87,822 (87.8%) | ✅ |
| Gross Revenue | ₹3.27 Crore+ | ✅ |
| Cancellation Rate | **12.2%** | ⚠️ Above target |
| Avg Delivery Time | **46.4 minutes** | ⚠️ Improvement needed |
| On-Time Delivery | 82.8% | ⚠️ Below 85% target |
| Avg Customer Rating | **3.71 / 5.0** | ⚠️ Declining trend |
| Repeat Order Rate | **79.6%** (85.5% active) | ✅ Solid retention base |
| Total Refunds Issued | ₹1.2L+ | ⚠️ High cost exposure |

---

## 2. City Performance Analysis

### 2.1 Order Volume and Revenue

| City | Orders | % Share | Net Revenue | Avg Order Value |
|---|---|---|---|---|
| Hyderabad | ~55,000 | 55% | ₹ Highest | ₹332 |
| Visakhapatnam | ~25,000 | 25% | ₹ Medium | ₹338 |
| Vijayawada | ~20,000 | 20% | ₹ Lowest | ₹330 |

**Key Finding:** Hyderabad dominates all metrics due to its larger population and
higher restaurant density. However, Visakhapatnam shows a slightly higher average
order value, suggesting a more premium customer base.

**Action:** Focus growth marketing on Visakhapatnam and Vijayawada while protecting
market position in Hyderabad.

### 2.2 Delivery Performance by City

All three cities show comparable delivery times (~46 min average). The key differentiator
is the **distribution of delays** — certain areas within each city drive outsized delays.

---

## 3. Restaurant Performance Analysis

### 3.1 Top Performers

The top-performing restaurants (by revenue and rating) share these characteristics:
- Located in high-density urban areas (Banjara Hills, MVP Colony, Benz Circle)
- Biryani and North Indian cuisine (highest order volumes)
- Avg prep time within the 15–20 minute window
- Cancellation rates below 8%

### 3.2 Poor Performers — Intervention Required

Restaurants with **rating < 3.0 AND cancellation rate > 20%** are classified as
**NEEDS ATTENTION** (performance tier). Key findings:
- Repeated complaints concentrated in: Late Delivery, Cold Food, Wrong Item
- Restaurants with very high prep times (>30 min) consistently produce lower ratings
- These restaurants generate significant refund costs

**Action Items:**
1. Mandatory quality review for all restaurants with > 20% cancellation rate
2. Remove restaurants with persistent < 2.5 rating despite review
3. Incentivise faster-prep restaurants during peak demand hours

### 3.3 Cuisine Performance

| Cuisine | Performance | Action |
|---|---|---|
| Biryani | 🏆 Highest volume | Expand partnership roster |
| South Indian | ✅ Strong ratings | Good baseline |
| Fast Food / Burger | ⚡ Fastest prep | Good for peak hours |
| Seafood | ⏱️ Long prep, lower ratings | Set realistic ETAs |
| Continental | 🏷️ High value, medium volume | Premium segment opportunity |

---

## 4. Delivery Operations Analysis

### 4.1 Peak Hour Crisis

The **dinner peak (19:00–22:00)** is the most critical window:
- Highest order volume: ~35% of all daily orders
- Highest cancellation rate: 14%+ (vs 8% overall)
- Highest delivery delays: Average delay 8–12 minutes above baseline

**Root Cause:** Insufficient rider availability relative to demand surge.

**Action:** Implement **surge-based rider allocation** — incentivise 40% more riders
to be active during 19:00–22:00.

### 4.2 Distance and Delay Correlation

Strong positive correlation (r ≈ 0.62) between delivery distance and actual delivery time.
Orders over 10 km consistently exceed 60-minute delivery times.

**Action:** 
- Cap delivery radius at 12 km for standard orders
- Implement separate "long-distance" SLA communicated to customers at checkout

### 4.3 Area-Specific Bottlenecks

Several areas consistently produce above-average delays:
- High-traffic areas during rush hours
- Areas with insufficient local restaurant density forcing longer pickup routes

**Action:** Deploy area-specific **micro-warehouses or cloud kitchens** in
high-delay, high-demand zones.

---

## 5. Customer Experience Analysis

### 5.1 Rating–Delay Relationship

This is the clearest actionable finding in the dataset:

| Delay Category | Avg Rating |
|---|---|
| Early (arrived before estimate) | 4.2+ ⭐ |
| On Time (0–5 min) | 3.9 ⭐ |
| Slight Delay (6–15 min) | 3.6 ⭐ |
| Moderate Delay (16–30 min) | 3.3 ⭐ |
| Significant Delay (31–60 min) | 3.0 ⭐ |
| Severe Delay (>60 min) | 2.5 ⭐ |

**Conclusion:** Every 15-minute increase in delay corresponds to approximately
0.3–0.4 star drop in customer rating.

### 5.2 Customer Retention Dynamics

- **13.5% (2,694)** of registered customers placed only **1 order** (one-timers), with an additional **6.9% (1,388)** zero-order signups.
- Across active ordering customers, the repeat rate is **85.5%** (15,918 customers placed 2+ orders).
- One-time customers generate only **3.5%** of total platform revenue (₹1.06M).
- Highly loyal customers (10+ orders: 2,759 customers) generate over **₹10.3M** (34.1% of revenue)—exhibiting an **8.5x lifetime value multiplier** over one-timers.
- 64% of one-time customers who never placed a second order experienced a delivery delay exceeding 20 minutes or filed a cold food complaint on their first order.

**Action:** Launch a structured **first-order win-back programme**:
- 2nd order discount (15% off + Free Delivery) automatically triggered 48 hours after order 1.
- Apologetic ₹50 wallet credit if order 1 suffered a delay > 15 minutes.
- Milestone incentives at order 5 and order 10 to lock in loyal cohorts.

### 5.3 Complaint Analysis

Top complaint categories:
1. **Late Delivery** (32%): Operationally fixable via better routing
2. **Cold Food** (18%): Packaging upgrade (thermal bags) required
3. **Wrong Item** (15%): Restaurant order accuracy training
4. **Missing Item** (12%): QC check at pickup required

**Total refund exposure:** ₹1.2L+ (primarily from 1-star, repeated-complaint restaurants)

---

## 6. Business Recommendations

### Priority 1 (Immediate — 0–30 days)

| Action | Problem Addressed | Expected Impact |
|---|---|---|
| Rider surge incentive (19–22h) | Peak-hour cancellations | -3% cancellation rate |
| Remove < 2.5★ restaurants (>50 reviews) | Poor experience | +0.2 avg rating |
| Thermal bag mandate for all riders | Cold food complaints | -30% cold food complaints |

### Priority 2 (Short-term — 1–3 months)

| Action | Problem Addressed | Expected Impact |
|---|---|---|
| 2nd-order retention voucher | 40% one-time customers | +10% repeat rate |
| Zone-based delivery SLAs | Unrealistic ETAs | -25% "late delivery" complaints |
| Restaurant prep time audit | Long-prep delays | -5 min avg delivery time |

### Priority 3 (Strategic — 3–6 months)

| Action | Problem Addressed | Expected Impact |
|---|---|---|
| Cloud kitchens in high-delay areas | Geographic bottlenecks | -8 min avg delivery time |
| AI route optimisation | Transit time | +5% on-time rate |
| Customer loyalty subscription | Retention | +20% LTV per customer |

---

## 7. Methodology Notes

- **Analysis tool:** Python (Pandas, Matplotlib, Seaborn)
- **Validation:** SQL (MySQL 8.0 compatible)
- **Visualisation:** Power BI (5-page interactive dashboard)
- **Data type:** Synthetic — generated using seed 42 for reproducibility
- **Analysis period:** January 2024 – December 2024

---

## 8. Appendix

- `data/raw/` — Original synthetic datasets
- `data/cleaned/` — Post-cleaning datasets
- `notebooks/01_Data_Cleaning_and_EDA.ipynb` — Full EDA with 15+ visualisations
- `sql/04_analysis_queries.sql` — All 20 SQL queries
- `excel/QuickBite_Excel_Analysis.xlsx` — Multi-sheet Excel analysis
- `powerbi/` — Full Power BI build package (data model, DAX, design spec)
- `docs/data_dictionary.md` — Field documentation
- `docs/synthetic_data_assumptions.md` — Generation assumptions

---

*Report prepared by Team Data Knights | CODEGNAN Hackathon DA-07*  
*Analysis Date: October 2024*
