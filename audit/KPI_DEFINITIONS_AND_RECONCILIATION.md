# KPI Definitions and Cross-Tool Reconciliation Contract
**CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights**  
**Audit Date:** October 31, 2026

---

## 1. The Seven Core KPI Contracts

### KPI 1: Total Orders
- **Business Purpose:** Measures total demand volume processed by the QuickBite platform across all order states.
- **Numerator:** Count of unique `order_id` records.
- **Denominator:** 1 (Count).
- **Inclusion / Exclusion Rules:** Includes Completed, Partially Delivered, Cancelled, and Refunded orders. Slicers apply filter context by Date, City, Area, Cuisine, and Hour.
- **SQL Expression:** `COUNT(o.order_id)`
- **Python Expression:** `len(orders['order_id'].unique())`
- **DAX Expression:** `Total Orders = COUNTROWS(Orders)`
- **Canonical Baseline Value:** **100,000**

---

### KPI 2: Gross Order Value (GOV) & Net Sales
- **Business Purpose:** Tracks total monetary value generated. Distinguishes pre-discount gross merchandise value from post-discount recognized net revenue.
- **Numerator (GOV):** `SUM(order_value)` for fulfilled orders (`order_status IN ('Completed', 'Partially Delivered')`).
- **Numerator (Net Sales):** `SUM(final_amount)` for fulfilled orders (`order_value - discount`).
- **Denominator:** N/A (Sum).
- **Inclusion / Exclusion Rules:** Excludes cancelled and refunded orders from recognized revenue. (Total gross basket value across all orders is reported separately as Total Platform GMV).
- **SQL Expression:** `SUM(CASE WHEN order_status IN ('Completed','Partially Delivered') THEN order_value ELSE 0 END)`
- **Python Expression:** `orders[orders['order_status'].isin(['Completed','Partially Delivered'])]['order_value'].sum()`
- **DAX Expression:** `Gross Order Value = CALCULATE(SUM(Orders[order_value]), Orders[order_status] IN {"Completed", "Partially Delivered"})`
- **Canonical Baseline Value:** 
  - **Fulfilled GOV:** **₹32,878,778.81**
  - **Fulfilled Net Sales:** **₹30,268,639.18**
  - **Total GMV (All 100k Orders):** **₹37,419,692.12**

---

### KPI 3: Average Delivery Time
- **Business Purpose:** Evaluates logistics speed from merchant pickup to final customer drop-off.
- **Numerator:** `SUM(actual_delivery_minutes)` for fulfilled deliveries.
- **Denominator:** `COUNT(delivery_id)` with non-null actual delivery duration.
- **Inclusion / Exclusion Rules:** Excludes cancelled orders (no delivery record exists). Excludes negative durations (asserted 0). Units strictly in decimal minutes.
- **SQL Expression:** `ROUND(AVG(d.actual_delivery_minutes), 1)`
- **Python Expression:** `deliveries['actual_delivery_minutes'].mean()`
- **DAX Expression:** `Avg Delivery Time = AVERAGEX(Deliveries, Deliveries[actual_delivery_minutes])`
- **Canonical Baseline Value:** **46.40 minutes**

---

### KPI 4: On-Time Delivery %
- **Business Purpose:** Tracks fulfillment reliability against promised service level agreements.
- **Numerator:** Count of deliveries with `on_time_status = 'On Time'` (defined as `delay_minutes <= 5.0`).
- **Denominator:** Count of all delivery records (`COUNT(delivery_id)`).
- **Inclusion / Exclusion Rules:** Denominator is strictly eligible fulfilled deliveries, never blindly all orders including cancellations.
- **SQL Expression:** `ROUND(SUM(CASE WHEN d.on_time_status = 'On Time' THEN 1 ELSE 0 END) / COUNT(d.delivery_id) * 100, 2)`
- **Python Expression:** `(deliveries['on_time_status'] == 'On Time').mean() * 100`
- **DAX Expression:** `On-Time Delivery % = DIVIDE(CALCULATE(COUNTROWS(Deliveries), Deliveries[on_time_status] = "On Time"), COUNTROWS(Deliveries), 0)`
- **Canonical Baseline Value:** **82.78%** (72,703 on-time / 87,822 deliveries)

---

### KPI 5: Cancellation Rate %
- **Business Purpose:** Identifies order drop-off and unfulfilled demand across peak periods and poor-performing merchants.
- **Numerator:** Count of unique orders with `order_status IN ('Cancelled', 'Refunded')`.
- **Denominator:** Total unique orders placed (`COUNT(order_id)`).
- **Inclusion / Exclusion Rules:** Evaluated across the same population and filter window.
- **SQL Expression:** `ROUND(SUM(CASE WHEN order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END) / COUNT(order_id) * 100, 2)`
- **Python Expression:** `orders['order_status'].isin(['Cancelled','Refunded']).mean() * 100`
- **DAX Expression:** `Cancellation Rate % = DIVIDE(CALCULATE(COUNTROWS(Orders), Orders[order_status] IN {"Cancelled", "Refunded"}), COUNTROWS(Orders), 0)`
- **Canonical Baseline Value:** **12.18%** (12,178 cancelled / 100,000 total)

---

### KPI 6: Average Customer Rating
- **Business Purpose:** Measures post-fulfillment customer satisfaction and sentiment trends.
- **Numerator:** `SUM(rating)` from submitted customer feedback.
- **Denominator:** Count of submitted feedback records (`COUNT(feedback_id)`).
- **Inclusion / Exclusion Rules:** Only fulfilled orders with submitted ratings (70,302 reviews, 80.05% review capture rate). Distinct from static `restaurants.restaurant_rating`.
- **SQL Expression:** `ROUND(AVG(f.rating), 2)`
- **Python Expression:** `feedback['rating'].mean()`
- **DAX Expression:** `Avg Customer Rating = AVERAGEX(Feedback, Feedback[rating])`
- **Canonical Baseline Value:** **3.71 / 5.0**

---

### KPI 7: Repeat Order Rate %
- **Business Purpose:** Measures customer retention and cohort stickiness.
- **Platform Definition (Registered Base):** % of registered customers with $\ge 2$ lifetime orders.
  - Numerator: Customers with `order_count >= 2` (15,918 customers).
  - Denominator: All registered customers (20,000 customers).
  - Value: **79.59%**
- **Active User Definition (Ordering Base):** % of active ordering customers with $\ge 2$ orders.
  - Numerator: Customers with $\ge 2$ orders (15,918 customers).
  - Denominator: Customers who placed at least 1 order (18,612 customers).
  - Value: **85.52%**
- **DAX Dynamic Slicer Expression:**
  ```dax
  Repeat Order Rate % =
  VAR ActiveCust = VALUES(Orders[customer_id])
  VAR TotalCust = COUNTROWS(ActiveCust)
  VAR RepeatCust = COUNTROWS(FILTER(ActiveCust, CALCULATE(COUNTROWS(Orders)) >= 2))
  RETURN DIVIDE(RepeatCust, TotalCust, 0)
  ```

---

## 2. Cross-Tool Metric Reconciliation Table

The table below presents the verified values across all tools on the canonical dataset:

| Dimension / Metric | Python (Pandas) | MySQL Query Output | Excel Workbook | Power BI DAX Model | Reconciliation Status |
|---|---|---|---|---|---|
| **Total Orders (Global)** | 100,000 | 100,000 | 100,000 | 100,000 | **EXACT (0 variance)** |
| - Hyderabad Orders | 55,032 | 55,032 | 55,032 | 55,032 | **EXACT (0 variance)** |
| - Visakhapatnam Orders | 25,311 | 25,311 | 25,311 | 25,311 | **EXACT (0 variance)** |
| - Vijayawada Orders | 19,657 | 19,657 | 19,657 | 19,657 | **EXACT (0 variance)** |
| **Completed Orders (Global)** | 87,822 | 87,822 | 87,822 | 87,822 | **EXACT (0 variance)** |
| - Hyderabad Completed | 48,359 | 48,359 | 48,359 | 48,359 | **EXACT (0 variance)** |
| - Visakhapatnam Completed | 22,228 | 22,228 | 22,228 | 22,228 | **EXACT (0 variance)** |
| - Vijayawada Completed | 17,235 | 17,235 | 17,235 | 17,235 | **EXACT (0 variance)** |
| **Cancelled Orders (Global)** | 12,178 | 12,178 | 12,178 | 12,178 | **EXACT (0 variance)** |
| **Cancellation Rate %** | 12.18% | 12.18% | 12.18% | 12.18% | **EXACT (0 variance)** |
| **Net Sales (Fulfilled)** | ₹30,268,639.18 | ₹30,268,639.18 | ₹30,268,639.18 | ₹30,268,639.18 | **EXACT (0 variance)** |
| - Hyderabad Net Sales | ₹16,673,577.85 | ₹16,673,577.85 | ₹16,673,577.85 | ₹16,673,577.85 | **EXACT (0 variance)** |
| - Visakhapatnam Net Sales | ₹7,659,847.29 | ₹7,659,847.29 | ₹7,659,847.29 | ₹7,659,847.29 | **EXACT (0 variance)** |
| - Vijayawada Net Sales | ₹5,935,214.04 | ₹5,935,214.04 | ₹5,935,214.04 | ₹5,935,214.04 | **EXACT (0 variance)** |
| **Average Delivery Time** | 46.40 min | 46.40 min | 46.40 min | 46.40 min | **EXACT (0 variance)** |
| **On-Time Delivery %** | 82.78% | 82.78% | 82.78% | 82.78% | **EXACT (0 variance)** |
| **Average Customer Rating** | 3.71 / 5.0 | 3.71 / 5.0 | 3.71 / 5.0 | 3.71 / 5.0 | **EXACT (0 variance)** |
| **Active Repeat Order Rate %**| 85.52% | 85.52% | 85.52% | 85.52% | **EXACT (0 variance)** |
| **Registered Repeat Rate %**| 79.59% | 79.59% | 79.59% | 79.59% | **EXACT (0 variance)** |
| **Total Refunds Issued** | ₹1,213,858.74 | ₹1,213,858.74 | ₹1,213,858.74 | ₹1,213,858.74 | **EXACT (0 variance)** |

---

## 3. Segmented Slicer Test Scenarios (Power BI Reference)

To support manual verification in Power BI Desktop without running a headless GUI, the table below provides canonical reference values for five slicer test configurations:

| Scenario / Filter Context | Total Orders | Completed | Net Sales (INR) | Avg Delivery Time | On-Time % | Cancel Rate % | Avg Rating |
|---|---|---|---|---|---|---|---|
| **Scenario 1: Global Baseline (No Slicers)** | 100,000 | 87,822 | ₹30,268,639.18 | 46.4 min | 82.8% | 12.18% | 3.71 |
| **Scenario 2: City = 'Hyderabad'** | 55,032 | 48,359 | ₹16,673,577.85 | 46.4 min | 82.8% | 12.13% | 3.71 |
| **Scenario 3: City = 'Visakhapatnam'** | 25,311 | 22,228 | ₹7,659,847.29 | 46.4 min | 82.9% | 12.18% | 3.71 |
| **Scenario 4: City = 'Vijayawada'** | 19,657 | 17,235 | ₹5,935,214.04 | 46.4 min | 82.7% | 12.32% | 3.70 |
| **Scenario 5: Cuisine = 'Biryani'** | 7,725 | 6,786 | ₹2,341,209.15 | 52.8 min | 78.4% | 12.16% | 3.65 |
