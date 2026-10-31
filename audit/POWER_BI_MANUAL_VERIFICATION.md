# Power BI Manual UI Verification & Build Protocol
**CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights**  
**Audit Date:** October 31, 2026 | **Desktop Engine:** Microsoft Power BI Desktop

---

## 1. Context & Verification Boundary Notice

Power BI Desktop is a Windows desktop application that requires manual UI interaction. Because automated headless compilation of `.pbix` binaries is constrained in headless environments without Power BI Desktop CLI bindings, this protocol provides:
1. **Step-by-step UI build and verification procedures** (~25 minutes).
2. **Exact canonical reference KPI values** for 5 distinct filter combinations to verify model correctness.
3. **Screenshot and visual inspection checklists**.

---

## 2. Step-by-Step UI Setup & Relationship Configuration

### Step 1: Ingest Data
1. Open **Power BI Desktop**.
2. Select **Get Data → Text/CSV**.
3. Ingest files from `d:\Hackton\quickbite-analytics\data\powerbi\` in the following sequence:
   - `riders_cleaned.csv` → Name table: `Riders`
   - `customers_cleaned.csv` → Name table: `Customers`
   - `restaurants_cleaned.csv` → Name table: `Restaurants`
   - `orders_cleaned.csv` → Name table: `Orders`
   - `deliveries_cleaned.csv` → Name table: `Deliveries`
   - `feedback_cleaned.csv` → Name table: `Feedback`
   *(Alternative Quick Option: Ingest `pbi_orders_master.csv` as a single flat analytical fact table).*

### Step 2: Establish Model Relationships (Star Schema)
Switch to **Model View** and configure relationships:

| From Table | Column | To Table | Column | Cardinality | Cross Filter Direction |
|---|---|---|---|---|---|
| `Orders` | `customer_id` | `Customers` | `customer_id` | Many-to-One (*:1) | Single |
| `Orders` | `restaurant_id` | `Restaurants` | `restaurant_id` | Many-to-One (*:1) | Single |
| `Orders` | `rider_id` | `Riders` | `rider_id` | Many-to-One (*:1) | Single |
| `Deliveries` | `order_id` | `Orders` | `order_id` | One-to-One (1:1) | **Both (Bidirectional)** ⚠️ |
| `Feedback` | `order_id` | `Orders` | `order_id` | One-to-One (1:1) | **Both (Bidirectional)** ⚠️ |

> ⚠️ **CRITICAL AUDIT STEP:** Ensure `Deliveries` and `Feedback` have **Cross filter direction = Both**. If set to Single, slicers on City, Cuisine, and Date will NOT filter delivery durations or customer ratings.

### Step 3: Create Measures Table
1. Click **Home → Enter Data** → Name table: `_Measures` → Click **Load**.
2. Add the 7 Core KPI measures from `powerbi/02_dax_measures.md`.

---

## 3. Canonical Slicer Test Reference Values

When validating the Power BI dashboard in the desktop UI, apply the slicers below and verify that the 7 KPI cards display these **exact mathematical values**:

### Test Scenario 1: Baseline Global (No Slicers Applied)
- **Filters:** All dates, all cities, all cuisines, all hours.
- [ ] **Total Orders:** `100,000`
- [ ] **Gross Order Value (GOV):** `₹32.88M` (₹32,878,778.81 fulfilled / ₹30.27M Net Sales)
- [ ] **Average Delivery Time:** `46.4 minutes` (or 46.40 min)
- [ ] **On-Time Delivery %:** `82.8%` (82.78%)
- [ ] **Cancellation Rate %:** `12.2%` (12.18%)
- [ ] **Average Customer Rating:** `3.71 / 5.0`
- [ ] **Repeat Order Rate %:** `79.6%` (Registered: 79.59%, Active: 85.52%)

---

### Test Scenario 2: City Slicer = "Hyderabad"
- **Filters:** Slicer `Restaurants[city]` = **Hyderabad**
- [ ] **Total Orders:** `55,032`
- [ ] **Completed Orders:** `48,359`
- [ ] **Net Sales:** `₹16,673,577.85` (₹16.67M)
- [ ] **Average Delivery Time:** `46.4 minutes`
- [ ] **On-Time Delivery %:** `82.8%`
- [ ] **Cancellation Rate %:** `12.13%`
- [ ] **Average Customer Rating:** `3.71 / 5.0`
- [ ] **Repeat Order Rate %:** `85.67%` (of active ordering users in Hyderabad)

---

### Test Scenario 3: City Slicer = "Visakhapatnam"
- **Filters:** Slicer `Restaurants[city]` = **Visakhapatnam**
- [ ] **Total Orders:** `25,311`
- [ ] **Completed Orders:** `22,228`
- [ ] **Net Sales:** `₹7,659,847.29` (₹7.66M)
- [ ] **Average Delivery Time:** `46.4 minutes`
- [ ] **On-Time Delivery %:** `82.9%`
- [ ] **Cancellation Rate %:** `12.18%`
- [ ] **Average Customer Rating:** `3.71 / 5.0`
- [ ] **Repeat Order Rate %:** `85.91%` (of active ordering users in Vizag)

---

### Test Scenario 4: City Slicer = "Vijayawada"
- **Filters:** Slicer `Restaurants[city]` = **Vijayawada**
- [ ] **Total Orders:** `19,657`
- [ ] **Completed Orders:** `17,235`
- [ ] **Net Sales:** `₹5,935,214.04` (₹5.94M)
- [ ] **Average Delivery Time:** `46.4 minutes`
- [ ] **On-Time Delivery %:** `82.7%`
- [ ] **Cancellation Rate %:** `12.32%`
- [ ] **Average Customer Rating:** `3.70 / 5.0`
- [ ] **Repeat Order Rate %:** `84.63%` (of active ordering users in Vijayawada)

---

### Test Scenario 5: Cuisine Slicer = "Biryani"
- **Filters:** Slicer `Restaurants[cuisine]` = **Biryani**
- [ ] **Total Orders:** `7,725`
- [ ] **Completed Orders:** `6,786`
- [ ] **Net Sales:** `₹2,341,209.15` (₹2.34M)
- [ ] **Average Delivery Time:** `52.8 minutes` ⚠️ *(Validates that kitchen prep time of Biryani correctly inflates delivery duration)*
- [ ] **On-Time Delivery %:** `78.4%` ⚠️ *(Lower on-time rate reflects longer prep)*
- [ ] **Cancellation Rate %:** `12.16%`
- [ ] **Average Customer Rating:** `3.65 / 5.0`

---

## 4. Visual Layout & Slicer Verification Checklist

### Five Required Slicers Check
- [ ] **Date Slicer:** Range slider bound to `DateTable[Date]` (Jan 1, 2024 – Dec 31, 2024). Interacting with the slider filters all 7 KPI cards.
- [ ] **City Slicer:** Tile or dropdown bound to `Restaurants[city]` (Hyderabad, Visakhapatnam, Vijayawada).
- [ ] **Area Slicer:** Dropdown bound to `Restaurants[area]`, cascading appropriately under selected city.
- [ ] **Cuisine Slicer:** Multi-select dropdown bound to `Restaurants[cuisine]`.
- [ ] **Hour Slicer:** Range or list slicer bound to `Orders[order_hour]` (0 to 23).

### Required Visuals Inspection
- [ ] **Page 1 (Executive Summary):** 7 KPI cards in header ribbon, Monthly Revenue line chart, City volume bar chart, Top 10 Restaurants table.
- [ ] **Page 2 (City & Geography):** Clustered bar chart of orders/revenue by city, Area performance matrix with conditional formatting.
- [ ] **Page 3 (Restaurant & Cuisine):** Scatter plot of Prep Time vs. Customer Rating, Top/Bottom 10 restaurants by rating and cancellation rate.
- [ ] **Page 4 (Delivery Operations):** Hourly order volume vs. cancellation rate line/column chart, Delay category distribution column chart.
- [ ] **Page 5 (Customer & Retention):** Rating distribution histogram (1 to 5 stars), Complaint type bar chart, Customer segment revenue breakdown.

---

## 5. Screenshot & Export Checklist
1. Apply **Scenario 1** → Take screenshot → Save as `powerbi_page1_exec_summary.png`.
2. Apply **Scenario 2 (Hyderabad)** → Take screenshot → Save as `powerbi_page2_hyderabad_filtered.png`.
3. Apply **Scenario 5 (Biryani)** → Take screenshot → Save as `powerbi_page3_biryani_filtered.png`.
4. Export full report via **File → Export → Export to PDF** → Save as `QuickBite_Dashboard_Export.pdf`.
