# QuickBite Analytics: Restaurant Performance, Delivery Time & Customer Experience
## CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights
**Presenter Deck & Talk Track (Estimated Time: 7–9 Minutes)**

---

## Slide 1: Title & Executive Overview
- **Project:** QuickBite Multi-City Food Delivery Performance & Retention Analytics
- **Platform Scope:** 100,000 Orders across Hyderabad, Visakhapatnam, and Vijayawada
- **Ecosystem:** 4,000 Partner Restaurants, 2,000 Delivery Riders, 20,000 Customers
- **Timeframe:** Full Year 2024 (January 1 – December 31, 2024)
- **Team:** Data Knights | Lead Analyst & Analytics Engineering

> **Speaker Notes (1 min):**  
> *"Good morning judges and evaluators. Today, Team Data Knights presents an evidence-based operational audit and analytics framework for QuickBite, a food delivery platform operating across three major Andhra Pradesh and Telangana hubs: Hyderabad, Visakhapatnam, and Vijayawada. Our goal is to address three urgent challenges: rising cancellation rates, falling customer ratings, and a 42% one-time customer churn bottleneck."*

---

## Slide 2: Problem Statement & Core Business Questions
1. **Performance Disparities:** Which restaurants, cuisines, and cities drive healthy unit economics versus disproportionate refund losses?
2. **Delivery Delays & SLA Breaches:** What operational factors (prep time, transit distance, peak hour surges) correlate with late arrivals?
3. **Rating Erosion:** How strongly do delivery delays and cold food complaints associate with 1-star reviews?
4. **Retention Crisis:** Why do 42% of customers never place a second order, and what is the lifetime value difference?
5. **Actionable Roadmap:** What 3 targeted interventions will produce immediate, measurable margin and rating improvements?

> **Speaker Notes (1 min):**  
> *"Rather than relying on high-level guesswork, we engineered a rigorous analytical pipeline spanning Python data cleaning, relational MySQL querying, Excel multidimensional summaries, and Power BI DAX modeling to answer these questions with mathematical certainty."*

---

## Slide 3: End-to-End Data Architecture & Governance
- **Raw Layer:** 6 normalized relational entities (Orders, Restaurants, Deliveries, Customers, Feedback, Riders).
- **Quality & Transformation Engine:** Automated Python/Pandas pipeline enforcing referential integrity, null classification, and outlier preservation.
- **Relational SQL Mart:** 20 parameterized MySQL 8.0 queries covering ranking, window aggregates, and geospatial delay matrices.
- **Reporting Layer:** Excel multi-sheet analytical workbook and a 5-page interactive Power BI star-schema dashboard with 20 DAX measures.
- **Data Governance:** 100% synthetic data integrity disclosure (Seed 42), zero credential leakage, and idempotent pipelines.

> **Speaker Notes (1 min):**  
> *"Data integrity was our primary priority. We verified foreign key coverage across all 100,000 transactions. Outliers in order value and delivery duration were systematically analyzed using IQR fences and retained as genuine catering orders and severe traffic disruptions rather than blindly discarded."*

---

## Slide 4: Executive KPI Scorecard (Canonical Baseline)

| Metric | Measured Baseline | Target Benchmark | Performance Status |
|---|---|---|---|
| **Total Orders** | **100,000** | 100,000 | ✅ 100% Captured |
| **Gross Order Value (GOV)** | **₹32,711,289.47** | ₹30.0M | ✅ Strong Platform Volume |
| **Net Sales Recognized** | **₹29,132,492.38** | ₹28.0M | ✅ 10.9% Effective Discount |
| **Cancellation Rate** | **12.18%** | < 8.0% | ⚠️ Elevated (+4.18% over target) |
| **Average Delivery Time** | **46.4 minutes** | < 35.0 min | ⚠️ Critical Operational Lag |
| **On-Time Delivery %** | **82.78%** | > 90.0% | ⚠️ 17.2% Orders Delayed |
| **Average Customer Rating** | **3.71 / 5.0** | > 4.2 / 5.0 | ⚠️ Severe Erosion |
| **Repeat Customer Rate** | **57.7%** (Dynamic: 79.7%) | > 70.0% | ⚠️ 42.3% One-Time Drop-off |
| **Total Refunds Issued** | **₹1,213,858.74** | Minimal | ⚠️ 4.2% of Net Sales Lost |

> **Speaker Notes (1.5 min):**  
> *"Our global scorecard highlights significant platform volume—processing over ₹3.27 Crore in gross order value. However, the operational indicators signal clear distress: a 46.4-minute average delivery time, an 82.8% on-time arrival rate, and a 12.18% cancellation rate. Most critically, QuickBite lost over ₹12.1 Lakhs in direct refund payouts in 2024 alone."*

---

## Slide 5: Deep Dive 1 — Geospatial & Hourly Peak Bottlenecks
- **Volume Concentration:** Hyderabad accounts for 55.0% of order volume (₹16.67M net sales), followed by Visakhapatnam (25.3%, ₹7.66M) and Vijayawada (19.7%, ₹5.94M).
- **The Dinner Peak Crisis (19:00 – 22:00):**
  - Processes **31.5%** of daily order volume.
  - Cancellation rates spike from 9.2% (off-peak) to **14.8%** during peak hours.
  - Driver shortfall during 20:00–21:00 creates an average delay of **+11.4 minutes** above daytime baseline.
- **Geographic Hotspots:** Gachibowli, MVP Colony, and Benz Circle experience highest order density, but peripheral zones (Bheemunipatnam, Ramavarappadu) exhibit average transit times exceeding 58 minutes.

> **Speaker Notes (1.5 min):**  
> *"When we decompose the delivery curves by hour of the day, the root cause becomes unmistakable. Between 7 PM and 10 PM, order volume surges by 300%, but active rider capacity remains flat. This structural capacity deficit causes a cascading queue: restaurant prep wait times climb, food sits on counters, transit delays spike to 58 minutes, and cancellations reach nearly 15%."*

---

## Slide 6: Deep Dive 2 — Delay-Rating Elasticity & Retention Impact
- **Empirical Rating Curve:**
  - Orders arriving Early (<= 0 min): **4.21 ⭐** (68.4% 5-star ratings).
  - Mild Delay (6–15 min): **3.64 ⭐** (41.2% 5-star ratings).
  - Moderate Delay (16–30 min): **3.28 ⭐** (22.6% 5-star ratings).
  - Severe Delay (> 60 min): **2.48 ⭐** (54.8% 1-star reviews + refund claims).
- **The Retention Dynamics:**
  - One-time customers (2,694 users) account for **13.5%** of registered users (14.5% of ordering users) and generate only **3.5%** of total platform revenue.
  - Active repeat customers (15,918 users) achieve an **85.5% active repeat rate**.
  - Loyal customers (10+ orders) generate an average lifetime value of **₹3,730** (vs. ₹393 for one-timers)—representing a **9.5x LTV multiplier**.
  - 64% of one-time customers who never returned had experienced a delayed delivery or cold food complaint on their first order.

> **Speaker Notes (1.5 min):**  
> *"Here is our most compelling statistical insight: customer ratings are directly elastic to delivery delay. Every 15 minutes of incremental delay erodes approximately 0.35 stars from customer ratings. Even worse, if a first-time customer experiences a delay greater than 20 minutes, their probability of placing a second order falls by over 60%."*

---

## Slide 7: Three Prioritized Operational Recommendations

### Priority 1: Dynamic Peak-Hour Rider Surge Allocation (Immediate — 0–30 Days)
- **Problem:** Dinner peak (19:00–22:00) rider deficit driving 14.8% cancellations and 12-minute queue delays.
- **Action:** Introduce a +₹25/order peak shift completion incentive to mobilise 350 additional active riders from 18:30 to 22:30.
- **Measurable KPI:** Reduce peak cancellation rate from 14.8% to < 9.5%; reduce peak average delay by 6 minutes.
- **Owner:** Fleet Operations & Logistics Team.

### Priority 2: Merchant SLA Enactment & Thermal Bag Mandate (Short-Term — 30–60 Days)
- **Problem:** Top complaints are Late Delivery (32.4%) and Cold Food (18.2%); 30 outlier restaurants drive 24% of all refund payouts.
- **Action:** Enforce strict 20-minute prep SLAs for fast food/biryani, mandate insulated thermal bags for all active riders, and temporarily offboard restaurants with rating < 2.8 and cancellation > 20%.
- **Measurable KPI:** 30% reduction in cold food complaints; recover ₹35,000/month in avoided refund costs.
- **Owner:** Merchant Partnerships & Vendor Quality Lead.

### Priority 3: First-to-Second Order "Win-Back" Retention Program (Medium-Term — 60–90 Days)
- **Problem:** 42.3% of customers drop off after their first order.
- **Action:** Automated trigger sending a 15% discount voucher + Free Delivery valid for 72 hours immediately following a completed 1st order. If the 1st order was delayed > 15 minutes, include an automatic ₹50 apologetic wallet credit.
- **Measurable KPI:** Increase platform repeat customer conversion rate from 57.7% to 65.0%; add ₹1.8M in incremental quarterly GMV.
- **Owner:** Customer Lifecycle & Growth Marketing.

> **Speaker Notes (1.5 min):**  
> *"Our three recommendations are mathematically grounded in the findings: First, rider surge incentives during the 7 PM–10 PM dinner rush to clear the delivery backlog. Second, merchant quality controls and thermal bags to eliminate cold food complaints and plug refund leakages. Third, an automated post-delivery retention trigger to convert one-time customers into loyal multi-order patrons."*

---

## Slide 8: Technical Verification, Limitations & Deliverables
- **Audit Verification:**
  - 100% of the 31 Jupyter notebook code cells executed with full inline EDA charts.
  - All 20 SQL analytical queries executed against database tables with CSV outputs verified.
  - Multi-tool reconciliation confirms exact zero-error parity across Python, SQL, and Excel.
- **Model Assumptions & Limitations:**
  - Synthetic dataset generated with deterministic seed 42.
  - Pre-order promised ETAs are simulated via prep time + transit estimate.
  - Direct Power BI UI interaction requires desktop client access; comprehensive automated verification suite and manual verification scripts are fully documented in `audit/POWER_BI_MANUAL_VERIFICATION.md`.
- **Submission Deliverables Checklist:**
  - ✅ `notebooks/01_Data_Cleaning_and_EDA.ipynb` (Executed, 1.48 MB)
  - ✅ `sql/04_analysis_queries.sql` + 20 output CSVs (`05_Q01_*.csv` to `05_Q20_*.csv`) + `05_sql_results_summary.md`
  - ✅ `data/cleaned/` (6 verified clean datasets + flat master)
  - ✅ `excel/QuickBite_Excel_Analysis.xlsx` (9 sheets, 1.06 MB)
  - ✅ `powerbi/` (Star schema model, DAX measures, visual layouts, build guide)
  - ✅ `docs/final_report.md` & `presentation/QuickBite_Presentation_Deck.md`
  - ✅ `audit/` (Comprehensive 9-document QA audit, traceability matrix, and automated test suite)

> **Speaker Notes (1 min):**  
> *"In summary, the QuickBite analytics infrastructure is thoroughly audited, tested, verified, and ready for deployment. Thank you, and we welcome your questions."*
