# Power BI Dashboard Design Specification
## QuickBite – Restaurant and Delivery Performance Analytics
### Team: Data Knights | CODEGNAN DA-07

---

## Global Design Settings

| Setting | Value |
|---|---|
| Theme | Custom dark/corporate theme |
| Canvas Size | 1280 × 720 px (16:9) |
| Background | #F1F3F4 (light grey) or #FFFFFF |
| Primary Colour | #1A73E8 (Google Blue) |
| Accent Colours | #34A853 (Green), #FBBC04 (Yellow), #EA4335 (Red) |
| Font | Segoe UI (Power BI default) |
| Page Navigation | Buttons at top right of each page |

---

## PAGE 1: Executive Overview

**Purpose:** C-suite summary of overall business health.

### Layout (Grid)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [Logo/Title: QuickBite Analytics]        [Date Slicer] [City Slicer]   │
├──────┬──────┬──────┬──────┬──────┬──────┬──────────────────────────────┤
│ KPI1 │ KPI2 │ KPI3 │ KPI4 │ KPI5 │ KPI6 │ KPI7                         │
│Total │Gross │Avg   │On-   │Cancel│Avg   │Repeat                        │
│Orders│Rev   │Del   │Time  │Rate  │Rating│Rate                          │
│      │      │Time  │      │      │      │                              │
├──────────────────────────┬───────────────────────────────────────────────┤
│   Line Chart:            │   Bar Chart:                                 │
│   Monthly Order &        │   City Comparison                            │
│   Revenue Trends         │   (Orders + Revenue + Avg Rating)            │
│                          │                                              │
├──────────────────────────┴───────────────────────────────────────────────┤
│   Donut Chart:       │   Gauge: On-Time   │   KPI Card: Total Refunds   │
│   Order Status       │   Delivery Rate    │   with Trend Indicator      │
│   Distribution       │                    │                             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Visuals Detail

**KPI Cards (Row 1 — 7 cards):**

| # | Title | Measure | Icon | Target/Goal |
|---|---|---|---|---|
| 1 | Total Orders | `Total Orders` | 📦 | 100,000 |
| 2 | Gross Revenue | `Gross Order Value` | 💰 | ₹2Cr+ |
| 3 | Avg Delivery Time | `Avg Delivery Time` | 🕐 | < 45 min |
| 4 | On-Time Delivery | `On-Time Delivery %` | ✅ | > 85% |
| 5 | Cancellation Rate | `Cancellation Rate %` | ❌ | < 10% |
| 6 | Avg Rating | `Avg Customer Rating` | ⭐ | > 4.0 |
| 7 | Repeat Rate | `Repeat Order Rate %` | 🔄 | > 60% |

**Line Chart — Monthly Trends:**
- X-Axis: `DateTable[Month Name]`
- Y-Axis (Primary): `Total Orders`
- Y-Axis (Secondary): `Net Sales`
- Title: "Monthly Order Volume and Revenue (2024)"

**Clustered Bar — City Comparison:**
- X-Axis: `Restaurants[city]`
- Values: `Total Orders`, `Net Sales`, `Avg Customer Rating`
- Title: "Performance by City"

**Donut Chart — Order Status:**
- Legend: `Orders[order_status]`
- Values: `Total Orders`
- Colours: Green=Completed, Red=Cancelled, Orange=Refunded

**Gauge — On-Time Delivery:**
- Value: `On-Time Delivery %`
- Min: 0%, Target: 85%, Max: 100%

---

## PAGE 2: Restaurant Performance

**Purpose:** Identify top/bottom performers; track cuisine and complaint trends.

### Visuals

**Slicers (top bar):** City, Cuisine, Area, Date Range

**Stacked Bar Chart — Top 20 Restaurants by Revenue:**
- Y-Axis: Restaurant Name
- X-Axis: Net Sales
- Legend: City
- Drill-through: Click → Restaurant Detail Page
- Title: "Top 20 Restaurants by Net Revenue"

**Table — Restaurant Scorecard:**
Columns: Restaurant Name | City | Cuisine | Total Orders | Revenue | Avg Rating | Cancel Rate | On-Time % | Complaint Rate | Performance Tier
- Conditional formatting: Rating (Red→Green), Cancel Rate (Green→Red)
- Sort by: Total Orders DESC

**Bar Chart — Orders by Cuisine:**
- X-Axis: Cuisine
- Y-Axis: `Total Orders`
- Colour: by City (clustered)

**Scatter Chart — Rating vs Cancellation Rate:**
- X-Axis: `Cancellation Rate %`
- Y-Axis: `Avg Customer Rating`
- Size: `Total Orders`
- Colour: City
- Title: "Restaurant Risk Map (Low Rating + High Cancellation = High Risk)"

**Clustered Column — Complaint Types:**
- X-Axis: Complaint Type
- Y-Axis: Count
- Filter: Complaint not blank

---

## PAGE 3: Delivery Analysis

**Purpose:** Analyse delivery operations, peak hours, and geographic performance.

### Visuals

**Slicers:** City, Area, Hour of Day, Date

**KPI Cards (top row — 4):**
- Avg Delivery Time | On-Time % | Avg Delay | % Severe Delays (>30 min)

**Line Chart — Avg Delivery Time by Hour:**
- X-Axis: `Orders[order_hour]` (0–23)
- Y-Axis: `Avg Delivery Time`
- Reference Line: Overall average
- Title: "Delivery Time by Hour of Day"

**Clustered Bar — Area Delivery Performance:**
- Y-Axis: Area
- X-Axis: `Avg Delivery Time`
- Colour Intensity: by Delay Rate
- Title: "Average Delivery Time by Area"

**Matrix (Heatmap) — Area × Hour Delay:**
- Rows: Area
- Columns: Hour (0–23)
- Values: `Avg Delay Minutes`
- Conditional formatting: Green (low) → Red (high)
- Title: "Delivery Delay Heatmap (Area × Hour)"

**Scatter — Distance vs Delivery Time:**
- X-Axis: `Deliveries[distance_km]`
- Y-Axis: `Deliveries[actual_delivery_minutes]`
- Size/Colour: On-Time Status
- Title: "Distance vs Delivery Duration"

**Pie Chart — On-Time Status Distribution:**
- Legend: `on_time_status`
- Values: Count of deliveries

---

## PAGE 4: Customer Experience

**Purpose:** Understand customer satisfaction, retention, and refund trends.

### Visuals

**Slicers:** City, Rating (1–5), Complaint Type, Date

**KPI Cards (top row — 4):**
- Avg Rating | Complaint Rate % | Total Refunds | Repeat Order Rate %

**Bar Chart — Rating Distribution:**
- X-Axis: Rating (1–5)
- Y-Axis: Count
- Colour: 1=Red, 2=Orange, 3=Yellow, 4=LightGreen, 5=Green
- Title: "Customer Rating Distribution"

**Line Chart — Rating Trend by Month:**
- X-Axis: Month
- Y-Axis: `Avg Customer Rating`
- Reference Line: Target rating (4.0)
- Title: "Monthly Rating Trend"

**Bar Chart — Delay Bucket vs Avg Rating:**
- X-Axis: `Deliveries[Delay Category]` (Early, On Time, Slight, Moderate, Significant, Severe)
- Y-Axis: `Avg Customer Rating`
- Colour: Gradient (Green → Red)
- Title: "Delivery Delay Impact on Customer Rating"

**Donut Chart — Customer Segments:**
- Legend: Customer Segment (One-Time, 2-3, Regular, Loyal)
- Values: Customer Count
- Title: "Customer Segmentation"

**Stacked Bar — Revenue by Customer Segment:**
- X-Axis: Customer Segment
- Y-Axis: Net Revenue
- Title: "Revenue Contribution by Customer Segment"

**Table — Top Complaint Categories:**
Columns: Complaint Type | Count | % of Feedback | Avg Rating | Avg Refund

---

## PAGE 5: Business Recommendations

**Purpose:** Summary slide — findings and action points for management.

### Layout

Use **Text Boxes**, **Cards**, and **Tables** (no complex charts needed).

```
┌─────────────────────────────────────────────────────────────────────┐
│  EXECUTIVE SUMMARY & RECOMMENDATIONS                                 │
│  QuickBite Food Delivery Analytics | Data Knights                    │
├─────────────────────────────────────────────────────────────────────┤
│  🔴 KEY PROBLEMS IDENTIFIED          │  🟢 RECOMMENDED ACTIONS       │
│  ─────────────────────────────────   │  ──────────────────────────   │
│  1. Cancellation rate: 12.2%         │  → Deploy extra riders 7–10pm │
│  2. Dinner peak delays (19–22h)      │  → Zone-based SLAs for areas  │
│  3. Low ratings for delayed orders   │  → Better insulation packaging│
│  4. 40%+ are one-time customers      │  → Loyalty programme launch   │
│  5. Certain areas: >15 min avg delay │  → Rider reallocation plan    │
├─────────────────────────────────────────────────────────────────────┤
│  EVIDENCE SUMMARY TABLE                                              │
│  Problem → Data Point → Impact → Action → Expected Improvement      │
└─────────────────────────────────────────────────────────────────────┘
```

**Evidence Table Content:**

| Problem | Supporting Metric | Revenue Impact | Recommended Action |
|---|---|---|---|
| High cancellation at dinner | 14% cancel rate at 20:00–21:00 | Lost orders + refunds | Rider surge pricing 18–22h |
| Delivery delay → low ratings | Severe delay → avg 2.5★ vs 4.2★ normal | Churn risk | Route optimisation AI |
| Low repeat rate | ~40% one-time customers | LTV shortfall | 2nd-order discount voucher |
| High complaint: Late Delivery | 32% of all complaints | ₹X refunds/month | SLA guarantee + proactive alerts |
| Slow prep time cuisines | Biryani avg 25 min prep | Higher delay probability | Notify customers at order time |
