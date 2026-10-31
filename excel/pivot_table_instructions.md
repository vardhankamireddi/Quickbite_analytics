# Excel Pivot Table Instructions
## QuickBite Analytics | Team: Data Knights | CODEGNAN DA-07

Use the **"Pivot Ready Data"** sheet in `QuickBite_Excel_Analysis.xlsx` to create the following pivot tables.

---

## How to Create a Pivot Table in Excel

1. Click any cell in the **"Pivot Ready Data"** sheet
2. **Insert tab → PivotTable → From Table/Range**
3. Check "New Worksheet", click OK
4. Drag fields to Rows, Columns, Values, and Filters areas

---

## Pivot Table 1: Orders by City

**Step 1:** Insert PivotTable from Pivot Ready Data  
**Step 2:** Drag fields:
- **Rows:** `city`
- **Values:** `order_id` → Count (rename to "Total Orders")
- **Values:** `final_amount` → Sum (rename to "Net Revenue")

**Expected Result:**

| City | Total Orders | Net Revenue |
|---|---|---|
| Hyderabad | ~55,000 | ₹ highest |
| Visakhapatnam | ~25,000 | ₹ medium |
| Vijayawada | ~20,000 | ₹ lowest |

**Add Chart:** Right-click PivotTable → PivotChart → Clustered Bar

---

## Pivot Table 2: Revenue by City (with discount breakdown)

**Rows:** `city`  
**Values:**
- `order_value` → Sum (Gross Revenue)
- `discount` → Sum (Total Discounts)
- `final_amount` → Sum (Net Revenue)

---

## Pivot Table 3: Orders by Area

**Rows:** `city`, then `area` (nested)  
**Values:** Count of `order_id`  
**Sort:** Largest to Smallest

---

## Pivot Table 4: Orders by Hour of Day

**Rows:** `order_hour`  
**Values:**
- Count of `order_id` (Total Orders)
- Sum of `is_cancelled` (Cancellations)

**Add a Calculated Field:**  
- Name: `Cancel Rate`
- Formula: `=is_cancelled/order_id`

**Add Chart:** Line Chart showing order volume trend by hour

---

## Pivot Table 5: Average Rating by Cuisine

**Rows:** `cuisine`  
**Values:**
- `rating` → Average (rename to "Avg Rating")
- `order_id` → Count (rename to "Total Orders")

**Sort:** By Avg Rating, Largest to Smallest  
**Add Chart:** Horizontal Bar Chart

---

## Pivot Table 6: Cancellation Rate by Restaurant

**Rows:** `restaurant_name`  
**Values:** Count of `order_id` (Total), Count of `is_cancelled` (Cancelled)  
**Calculated Field:** `=is_cancelled/order_id`  
**Filter:** Top 20 by cancellation rate  
**Add Chart:** Bar Chart

---

## Pivot Table 7: Delivery Performance by Area

**Rows:** `city`, `area`  
**Values:**
- `actual_delivery_minutes` → Average
- `on_time_status` → Count

---

## Pivot Table 8: Revenue by Month

**Rows:** `order_month`  
**Values:** `final_amount` → Sum  
**Add Chart:** Line Chart for trend

---

## Adding Slicers to Connect Multiple Pivot Tables

1. Click a pivot table → **PivotTable Analyze → Insert Slicer**
2. Select: `city`, `cuisine`, `order_hour`
3. **Right-click slicer → Report Connections** → Select all pivot tables to link them

This creates an interactive dashboard where all pivot tables filter together.

---

## Tips

- **Refresh data:** Right-click any pivot table → **Refresh** after updating source data
- **Number formatting:** Right-click value → Value Field Settings → Number Format
- **Conditional formatting:** Select value column → Home → Conditional Formatting → Color Scales
