# Data Quality and Lineage Report
**CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights**  
**Audit Date:** October 31, 2026

---

## 1. Source Data Provenance & Schemas

The QuickBite analytics ecosystem is built upon six normalized relational entities generated deterministically with Python `numpy` and `pandas` using **Random Seed 42** to guarantee 100% auditability and reproducibility.

### Summary Table of Datasets

| Entity Name | Raw File Path | Cleaned File Path | Raw Rows | Cleaned Rows | Columns | Primary Key | Key Foreign Keys |
|---|---|---|---|---|---|---|---|
| **Orders** | `data/raw/orders.csv` | `data/cleaned/orders_cleaned.csv` | 100,000 | 100,000 | 10 (Raw) / 16 (Clean) | `order_id` | `customer_id`, `restaurant_id`, `rider_id` |
| **Restaurants** | `data/raw/restaurants.csv` | `data/cleaned/restaurants_cleaned.csv` | 4,000 | 4,000 | 7 | `restaurant_id` | None (Dimension) |
| **Deliveries** | `data/raw/deliveries.csv` | `data/cleaned/deliveries_cleaned.csv` | 87,822 | 87,822 | 10 (Raw) / 11 (Clean) | `delivery_id` | `order_id`, `rider_id` |
| **Customers** | `data/raw/customers.csv` | `data/cleaned/customers_cleaned.csv` | 20,000 | 20,000 | 4 (Raw) / 6 (Clean) | `customer_id` | None (Dimension) |
| **Feedback** | `data/raw/feedback.csv` | `data/cleaned/feedback_cleaned.csv` | 70,302 | 70,302 | 7 | `feedback_id` | `order_id`, `customer_id` |
| **Riders** | `data/raw/riders.csv` | `data/cleaned/riders_cleaned.csv` | 2,000 | 2,000 | 3 | `rider_id` | None (Dimension) |
| **Master Analytical Mart** | N/A | `data/powerbi/pbi_orders_master.csv` | N/A | 100,000 | 23 | `order_id` | Flat denormalized analytical table |

---

## 2. Relational Joins & Cardinality Audit

### Match Rates & Foreign Key Integrity

| Join Relationship | Parent Table | Child Table | Foreign Key | Match Rate | Cardinality | Join Validation Verdict |
|---|---|---|---|---|---|---|
| Orders → Customers | `customers` (20,000) | `orders` (100,000) | `customer_id` | **100.0%** (0 orphans) | 1 : Many (Avg 5.0 orders/cust) | ✅ Perfect Referential Integrity |
| Orders → Restaurants | `restaurants` (4,000) | `orders` (100,000) | `restaurant_id` | **100.0%** (0 orphans) | 1 : Many (Avg 25.0 orders/rest) | ✅ Perfect Referential Integrity |
| Orders → Riders | `riders` (2,000) | `orders` (100,000) | `rider_id` | **100.0%** (0 orphans) | 1 : Many (Avg 50.0 orders/rider) | ✅ Perfect Referential Integrity |
| Deliveries → Orders | `orders` (100,000) | `deliveries` (87,822) | `order_id` | **100.0%** (87,822 matches) | 1 : 1 (Non-cancelled orders) | ✅ Exactly 1 delivery per delivered order; 0 for cancelled |
| Feedback → Orders | `orders` (100,000) | `feedback` (70,302) | `order_id` | **100.0%** (70,302 matches) | 1 : 1 (Delivered orders with feedback) | ✅ 80.05% review capture rate; 0 reviews for cancelled |
| Feedback → Customers | `customers` (20,000) | `feedback` (70,302) | `customer_id` | **100.0%** (0 orphans) | 1 : Many | ✅ Verified customer linkage |

> **Fanout Audit:** We verified that joining `orders` to `deliveries` or `feedback` using `LEFT JOIN` on `order_id` produces exactly **100,000 rows**. There is zero fanout, zero duplicated order values, and zero row multiplication.

---

## 3. Data Cleaning Transformations & Idempotency

### Cleaning Pipeline Steps

```
[Raw CSVs] 
    │
    ▼
1. Type Casting: order_time, pickup_time, delivery_time to datetime64[ns]
    │
    ▼
2. Temporal Consistency: Assert order_time <= pickup_time <= delivery_time
    │
    ▼
3. Financial Consistency: Assert order_value > 0, discount >= 0, final_amount == order_value - discount
    │
    ▼
4. Structural Null Handling:
   - cancellation_reason: NULL/empty for 87,822 completed orders (by design)
   - complaint_type: NULL/empty for 44,263 non-complaint feedbacks (by design)
   - refund_amount: 0.00 for non-refunded orders
    │
    ▼
5. Feature Engineering:
   - Orders: order_date, order_hour, order_month, order_day_name, time_segment, is_cancelled
   - Deliveries: delay_category (Early, On Time, Slight, Moderate, Significant, Severe)
   - Customers: order_count, customer_segment (One-time, Regular, Loyal)
    │
    ▼
6. Idempotent Export: Saved to data/cleaned/, data/powerbi/, powerbi/powerbi_ready_data/
```

### Idempotency Verification
Rerunning `run_data_cleaning.py` or the Jupyter notebook produces byte-identical output files without generating duplicate records, multiplying keys, or modifying raw data.

---

## 4. Field Semantics & Verified Business Definitions

| Field Name | Table | Data Type | Physical Meaning | Business Constraints & Boundaries |
|---|---|---|---|---|
| `order_value` | Orders | Decimal(10,2) | **Gross Order Value (GOV)** | Pre-discount food item total (₹80.00 to ₹2,838.20). |
| `discount` | Orders | Decimal(10,2) | **Promotional Discount** | Deducted from order value (₹0.00 to ₹647.72). |
| `final_amount` | Orders | Decimal(10,2) | **Net Sales / Recognized Revenue** | Customer payable amount: `order_value - discount`. |
| `order_status` | Orders | String | Transaction fulfillment state | 87,822 Completed/Partially Delivered (87.82%), 12,178 Cancelled/Refunded (12.18%). |
| `cancellation_reason` | Orders | String | Reason logged for cancellation | Populated only for 12,178 cancelled orders. 8 distinct categories. |
| `actual_delivery_minutes` | Deliveries | Float | Total elapsed delivery duration | Measured from kitchen pickup to customer drop-off (5.7 to 179.9 min, mean: 46.4 min). |
| `delay_minutes` | Deliveries | Float | Variance from estimated arrival time | `actual_delivery_minutes - estimated_delivery_time` (-5.0 to 70.0 min). |
| `on_time_status` | Deliveries | String | SLA fulfillment indicator | "On Time" if `delay_minutes <= 5.0` (82.78%), else "Delayed" (17.22%). |
| `avg_prep_time` | Restaurants | Float | Kitchen preparation benchmark | Varies by cuisine (5.0 to 48.1 min, mean: 18.5 min). Fast food ~10 min, Biryani ~25 min. |
| `restaurant_rating` | Restaurants | Float | Platform baseline rating aggregate | 1.9 to 5.0 scale (mean: 3.90). Stored at restaurant level. |
| `rating` | Feedback | Integer | Per-order customer satisfaction score | 1 to 5 integer rating submitted by customer after completed delivery (mean: 3.71). |

---

## 5. Outlier Detection & Retention Policy

We applied Tukey’s Interquartile Range (IQR) method: $[Q1 - 1.5 \times IQR, Q3 + 1.5 \times IQR]$ across all continuous variables:

| Column | Q1 | Q3 | IQR | Lower Fence | Upper Fence | Detected Outliers | Analytical Decision & Rationale |
|---|---|---|---|---|---|---|---|
| `orders.order_value` | ₹234.50 | ₹492.10 | ₹257.60 | -₹151.90 | ₹878.50 | 4,218 rows (> ₹878) | **RETAINED:** Legitimate group meals, family feasts, and corporate party orders. Not erroneous data. |
| `deliveries.actual_delivery_minutes` | 32.4 min | 58.6 min | 26.2 min | -6.9 min | 97.9 min | 1,412 rows (> 98 min) | **RETAINED:** Legitimate severe weather disruptions, transit breakdowns, and long-distance deliveries. |
| `deliveries.delay_minutes` | -2.1 min | 12.4 min | 14.5 min | -23.8 min | 34.1 min | 5,302 rows (> 34 min) | **RETAINED:** Critical data points representing severe peak-hour delays that drive customer dissatisfaction. |
| `deliveries.distance_km` | 4.1 km | 9.8 km | 5.7 km | -4.4 km | 18.4 km | 842 rows (> 18.4 km) | **RETAINED:** Long-distance deliveries to peripheral suburbs. |
| `restaurants.avg_prep_time` | 13.8 min | 22.4 min | 8.6 min | 0.9 min | 35.3 min | 94 rows (> 35 min) | **RETAINED:** Slow-prep artisan cuisines (Dum Biryani, Seafood platters). |

---

## 6. Data Assumptions & Limitations

1. **Synthetic Nature:** All 100,000 records are generated with NumPy seed 42. Findings illustrate realistic food delivery platform dynamics but do not reflect confidential records of any commercial entity.
2. **Pre-Order Promised SLA:** The dataset records `estimated_delivery_time` derived from `avg_prep_time + transit_time`. Customer-facing dynamic promise times during checkout are inferred from this estimate.
3. **Driver Availability:** While active rider pool size is modeled (2,000 riders), individual rider GPS trajectories and concurrent multi-order stacking are abstracted into order-level pickup and delivery timestamps.
