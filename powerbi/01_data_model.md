# Power BI Data Model – QuickBite Analytics
## Team: Data Knights | CODEGNAN DA-07

---

## Data Sources (Import from `data/powerbi/` or `data/cleaned/`)

Import these cleaned CSV files into Power BI Desktop:

| File | Table Name in Power BI | Rows |
|---|---|---|
| `orders_cleaned.csv` | `Orders` | ~100,000 |
| `restaurants_cleaned.csv` | `Restaurants` | 4,000 |
| `deliveries_cleaned.csv` | `Deliveries` | ~87,822 |
| `customers_cleaned.csv` | `Customers` | 20,000 |
| `feedback_cleaned.csv` | `Feedback` | ~70,302 |
| `riders_cleaned.csv` | `Riders` | 2,000 |

---

## Relationships (Star Schema)

```
                    ┌──────────────┐
                    │   Customers  │
                    │  (customer_id)│
                    └──────┬───────┘
                           │ 1:N
                    ┌──────▼───────┐        ┌──────────────┐
        ┌──────────►│    Orders    │◄───────►│  Restaurants │
        │           │  (order_id)  │         │(restaurant_id)│
        │           └──────┬───────┘         └──────────────┘
        │                  │ 1:1/1:N
        │           ┌──────▼───────┐
        │           │  Deliveries  │
        │           │ (delivery_id)│
        │           └──────────────┘
        │
        │           ┌──────────────┐
        └──────────►│   Feedback   │
                    │ (feedback_id)│
                    └──────────────┘

                    ┌──────────────┐
                    │    Riders    │◄── Orders.rider_id
                    │  (rider_id)  │◄── Deliveries.rider_id
                    └──────────────┘

                    ┌──────────────┐
                    │  DateTable   │◄── Orders.order_time (date)
                    │  (Date)      │
                    └──────────────┘
```

### Relationship Configuration

| From Table | From Column | To Table | To Column | Cardinality | Direction |
|---|---|---|---|---|---|
| Orders | customer_id | Customers | customer_id | Many-to-One | Single (Orders → Customers) |
| Orders | restaurant_id | Restaurants | restaurant_id | Many-to-One | Single (Orders → Restaurants) |
| Orders | rider_id | Riders | rider_id | Many-to-One | Single (Orders → Riders) |
| Deliveries | order_id | Orders | order_id | One-to-One | **Both (Bidirectional)** |
| Feedback | order_id | Orders | order_id | One-to-One | **Both (Bidirectional)** |
| Orders | order_date | DateTable | Date | Many-to-One | Single (Orders → DateTable) |

> **CRITICAL AUDIT NOTE (FIX APPLIED):** 
> In original documentation, Deliveries → Orders and Feedback → Orders were set to "Single (→ Orders)". 
> Under that setting, filtering Orders via Slicers (Date, City, Cuisine, Area) did NOT propagate to 
> the Deliveries or Feedback tables, causing `[Avg Delivery Time]`, `[On-Time Delivery %]`, and `[Avg Customer Rating]` 
> to ignore slicer selections and remain fixed at nationwide totals!
> **Resolution:** Set cross-filter direction to **Both (Bidirectional)** for Deliveries ↔ Orders and Feedback ↔ Orders.
> Alternatively, use the flat analytical model `pbi_orders_master.csv` (Option C) where all attributes reside in one table.

---

## Date Dimension Table (Create in Power Query or DAX)

### Option A: Create in Power Query (M Language)

```m
let
    StartDate = #date(2024, 1, 1),
    EndDate   = #date(2024, 12, 31),
    NrDays    = Duration.Days(EndDate - StartDate) + 1,
    DateList  = List.Dates(StartDate, NrDays, #duration(1, 0, 0, 0)),
    Table     = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    TypedDate = Table.TransformColumnTypes(Table, {{"Date", type date}}),
    Year      = Table.AddColumn(TypedDate,  "Year",        each Date.Year([Date]),   Int64.Type),
    Month     = Table.AddColumn(Year,       "Month",       each Date.Month([Date]),  Int64.Type),
    MonthName = Table.AddColumn(Month,      "Month Name",  each Date.ToText([Date], "MMM"), type text),
    Quarter   = Table.AddColumn(MonthName,  "Quarter",     each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    DayName   = Table.AddColumn(Quarter,    "Day Name",    each Date.DayOfWeekName([Date]), type text),
    WeekNum   = Table.AddColumn(DayName,    "Week Number", each Date.WeekOfYear([Date]), Int64.Type),
    IsWeekend = Table.AddColumn(WeekNum,    "Is Weekend",  each Date.DayOfWeek([Date]) >= 5, type logical)
in
    IsWeekend
```

### Option B: DAX Calculated Table

```dax
DateTable =
VAR StartDate = DATE(2024, 1, 1)
VAR EndDate   = DATE(2024, 12, 31)
RETURN
ADDCOLUMNS(
    CALENDAR(StartDate, EndDate),
    "Year",        YEAR([Date]),
    "Month",       MONTH([Date]),
    "Month Name",  FORMAT([Date], "MMM"),
    "Month Year",  FORMAT([Date], "MMM YYYY"),
    "Quarter",     "Q" & FORMAT(QUARTER([Date]), "0"),
    "Day Name",    FORMAT([Date], "ddd"),
    "Week Number", WEEKNUM([Date]),
    "Is Weekend",  WEEKDAY([Date], 2) >= 6
)
```

---

## Power Query: Required Column Transformations

### Orders Table
```m
// Convert order_time to datetime
Table.TransformColumnTypes(Source, {
    {"order_time", type datetime},
    {"order_value", type number},
    {"discount", type number},
    {"final_amount", type number}
})

// Add calculated columns
order_date  = Date.From([order_time])
order_hour  = Time.Hour(DateTime.Time([order_time]))
order_month = Date.Month(Date.From([order_time]))
is_completed = [order_status] = "Completed" or [order_status] = "Partially Delivered"
is_cancelled = [order_status] = "Cancelled" or [order_status] = "Refunded"
```

### Deliveries Table
```m
Table.TransformColumnTypes(Source, {
    {"pickup_time",  type datetime},
    {"delivery_time", type datetime},
    {"actual_delivery_minutes", type number},
    {"delay_minutes", type number},
    {"distance_km", type number}
})
```

### Feedback Table
```m
// Replace empty strings with null for complaint_type
Table.ReplaceValue(Source, "", null, Replacer.ReplaceValue, {"complaint_type"})
```

---

## Calculated Columns (DAX)

```dax
// Orders table: time segmentation
Time Segment =
SWITCH(
    TRUE(),
    Orders[order_hour] >= 6  && Orders[order_hour] <= 11, "Morning",
    Orders[order_hour] >= 12 && Orders[order_hour] <= 14, "Lunch Peak",
    Orders[order_hour] >= 15 && Orders[order_hour] <= 17, "Afternoon",
    Orders[order_hour] >= 18 && Orders[order_hour] <= 22, "Dinner Peak",
    "Late Night"
)

// Deliveries: delay category
Delay Category =
SWITCH(
    TRUE(),
    Deliveries[delay_minutes] <= 0,  "Early",
    Deliveries[delay_minutes] <= 5,  "On Time",
    Deliveries[delay_minutes] <= 15, "Slight Delay",
    Deliveries[delay_minutes] <= 30, "Moderate Delay",
    Deliveries[delay_minutes] <= 60, "Significant Delay",
    "Severe Delay"
)

// Customers: segment
Customer Segment =
SWITCH(
    TRUE(),
    Customers[total_orders] = 0,  "No Orders",
    Customers[total_orders] = 1,  "One-Time",
    Customers[total_orders] <= 3, "2-3 Orders",
    Customers[total_orders] <= 9, "Regular (4-9)",
    "Loyal (10+)"
)
```
