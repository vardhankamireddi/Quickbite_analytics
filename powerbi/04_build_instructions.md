# Power BI Step-by-Step Build Instructions
## QuickBite Analytics | Team: Data Knights | CODEGNAN DA-07

Estimated build time: **25–35 minutes** with this guide.

---

## Prerequisites

- [ ] Power BI Desktop installed (free from microsoft.com/power-bi)
- [ ] CSV files ready in `data/cleaned/` or `data/powerbi/`
- [ ] `02_dax_measures.md` open for reference

---

## STEP 1: Import Data (5 min)

1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Import files in this order:
   - `riders_cleaned.csv`
   - `customers_cleaned.csv`
   - `restaurants_cleaned.csv`
   - `orders_cleaned.csv`
   - `deliveries_cleaned.csv`
   - `feedback_cleaned.csv`
3. For each file: click **Transform Data** to open Power Query Editor
4. Verify column types (especially datetime columns):
   - `orders[order_time]` → Date/Time
   - `deliveries[pickup_time]`, `deliveries[delivery_time]` → Date/Time

---

## STEP 2: Create Date Table (2 min)

1. **Modeling tab → New Table**
2. Paste the DAX from `01_data_model.md` (Option B: DAX Calculated Table)
3. Name it `DateTable`

---

## STEP 3: Set Up Relationships (3 min)

1. Switch to **Model View** (diagram icon on left sidebar)
2. Create relationships by dragging:

| From | → | To |
|---|---|---|
| `Orders[customer_id]` | → | `Customers[customer_id]` |
| `Orders[restaurant_id]` | → | `Restaurants[restaurant_id]` |
| `Orders[rider_id]` | → | `Riders[rider_id]` |
| `Deliveries[order_id]` | → | `Orders[order_id]` |
| `Feedback[order_id]` | → | `Orders[order_id]` |
| `Orders[order_date]` | → | `DateTable[Date]` |

3. For Deliveries ↔ Orders: set **Cross filter direction = Both** (enables slicers on Date/City/Cuisine to filter Deliveries)
4. For Feedback ↔ Orders: set **Cross filter direction = Both** (enables slicers on Date/City/Cuisine to filter Feedback)

---

## STEP 4: Create Calculated Columns (3 min)

1. Click `Orders` table → **Table tools → New Column**
2. Add these columns (from `01_data_model.md`):
   - `order_date = DATE(...)` — or it may already exist
   - `order_hour = HOUR(Orders[order_time])`
   - `Time Segment = SWITCH(TRUE(), ...)` — copy from data_model.md

3. Click `Deliveries` table → New Column:
   - `Delay Category = SWITCH(TRUE(), ...)` — copy from data_model.md

4. Click `Customers` table → New Column:
   - `Customer Segment = SWITCH(TRUE(), ...)` — copy from data_model.md

---

## STEP 5: Create Measures Table and All Measures (5 min)

1. **Home → Enter Data** → Name: `_Measures` → Load
2. **Right-click `_Measures` → New Measure** for each measure in `02_dax_measures.md`

Create them in order:
1. `Total Orders`
2. `Completed Orders`
3. `Gross Order Value`
4. `Net Sales`
5. `Avg Delivery Time`
6. `On-Time Delivery %`
7. `Cancellation Rate %`
8. `Avg Customer Rating`
9. `Repeat Order Rate %`
10. `Complaint Rate %`
11. `Total Refund Amount`
12. `Avg Delay Minutes`
13. `Avg Revenue per Order`
14. `Pct Severe Delay`

> Apply formatting to each measure as per `02_dax_measures.md`.

---

## STEP 6: Build Page 1 – Executive Overview (5 min)

1. **Right-click page tab → Rename → "Executive Overview"**
2. **Insert → Text Box** → Title: "QuickBite – Restaurant & Delivery Performance Analytics"

**Add KPI Cards (7 cards in a row):**
- Select **Card Visual** from the Visualizations pane
- Drag measure → Fields well
- Repeat for all 7 KPI measures
- Arrange in a row at the top

**Add Slicers:**
- Insert **Slicer** → Field: `DateTable[Date]` → Slicer style: Between
- Insert **Slicer** → Field: `Restaurants[city]` → Slicer style: Dropdown

**Add Monthly Trend Line Chart:**
- Select **Line and Clustered Column Chart**
- X-Axis: `DateTable[Month Name]`
- Column Values: `Total Orders`
- Line Values: `Net Sales`

**Add City Bar Chart:**
- Select **Clustered Bar Chart**
- Y-Axis: `Restaurants[city]`
- X-Axis: `Total Orders`

**Add Order Status Donut:**
- Select **Donut Chart**
- Legend: `Orders[order_status]`
- Values: `Total Orders`

---

## STEP 7: Build Page 2 – Restaurant Performance (5 min)

1. **Right-click page tab → Rename → "Restaurant Performance"**

**Add Slicers:** City, Cuisine, Date Range

**Add Revenue Bar Chart (Top 20):**
- Select **Horizontal Bar Chart**
- Y-Axis: `Restaurants[restaurant_name]`
- X-Axis: `Net Sales`
- Apply Top N Filter: Top 20 by Net Sales

**Add Restaurant Table:**
- Select **Table Visual**
- Columns: restaurant_name, city, cuisine, Total Orders, Net Sales,
  Avg Customer Rating, Cancellation Rate %, On-Time Delivery %
- Enable conditional formatting on Rating and Cancellation Rate columns

**Add Cuisine Bar Chart:**
- X-Axis: `Restaurants[cuisine]`
- Y-Axis: `Total Orders`

**Add Scatter Chart (Risk Map):**
- X-Axis: `Cancellation Rate %`
- Y-Axis: `Avg Customer Rating`
- Size: `Total Orders`

---

## STEP 8: Build Page 3 – Delivery Analysis (4 min)

1. Rename page → "Delivery Analysis"

**Add KPI Cards:** Avg Delivery Time, On-Time %, Avg Delay, Pct Severe Delay

**Add Hourly Delivery Line Chart:**
- X-Axis: `Orders[order_hour]`
- Y-Axis: `Avg Delivery Time`
- Add a reference line at 45 min

**Add Area Bar Chart:**
- Y-Axis: `Restaurants[area]`
- X-Axis: `Avg Delivery Time`
- Filter: Minimum 50 deliveries

**Add Heatmap Matrix:**
- Rows: `Restaurants[area]`
- Columns: `Orders[order_hour]`
- Values: `Avg Delay Minutes`
- Conditional formatting on values: Green (low) → Red (high)

**Add Distance Scatter:**
- X-Axis: `Deliveries[distance_km]`
- Y-Axis: `Avg Delivery Time`

---

## STEP 9: Build Page 4 – Customer Experience (4 min)

1. Rename page → "Customer Experience"

**Add KPI Cards:** Avg Rating, Complaint Rate %, Total Refunds, Repeat Order Rate %

**Add Rating Bar Chart:**
- X-Axis: `Feedback[rating]`
- Y-Axis: Count of Feedback
- Custom colours: 1=Red, 2=Orange, 3=Yellow, 4=LightGreen, 5=Green

**Add Rating Trend Line:**
- X-Axis: `DateTable[Month Name]`
- Y-Axis: `Avg Customer Rating`
- Reference line at 4.0

**Add Delay vs Rating Bar:**
- X-Axis: `Deliveries[Delay Category]`
- Y-Axis: `Avg Customer Rating`

**Add Customer Segment Donut:**
- Legend: `Customers[Customer Segment]`
- Values: Count of Customers

---

## STEP 10: Build Page 5 – Business Recommendations (2 min)

1. Rename page → "Business Recommendations"
2. Use **Text Boxes** and **Tables** as per `03_dashboard_design.md`
3. Add Team Name, Hackathon Name, and disclaimer

---

## STEP 11: Add Navigation and Final Polish (2 min)

1. **Insert → Buttons → Blank** for each page
2. Set action: **Page Navigation** → target page
3. Copy buttons to all pages for consistent navigation
4. Adjust colours, fonts, background fill as needed
5. **File → Save As → QuickBite_Dashboard.pbix**

---

## STEP 12: Publish (Optional)

1. **Home → Publish → Select workspace**
2. Or export: **File → Export → PDF** for sharing

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Measures return BLANK | Check relationship direction; ensure FK-PK match |
| Double-counting orders | Verify Feedback and Deliveries use Single cross-filter direction |
| Wrong date filtering | Ensure `Orders[order_date]` is a Date type, not DateTime |
| Slicer not filtering chart | Check if relationship exists between slicer table and visual table |
| Heatmap too slow | Reduce row/column count; use Top N filter |
