# Power BI DAX Measures – QuickBite Analytics
## Team: Data Knights | CODEGNAN DA-07

Create these measures in a dedicated **"_Measures"** table in Power BI for organisation.

---

## How to Create a Measures Table

1. In Power BI Desktop → Home → Enter Data
2. Name it `_Measures`, enter one blank column, click Load
3. Right-click `_Measures` in the Fields pane → New Measure

---

## Core KPI Measures

### 1. Total Orders
```dax
Total Orders =
COUNTROWS(Orders)
```
> **Definition:** Count of all order rows regardless of status.

---

### 2. Completed Orders
```dax
Completed Orders =
CALCULATE(
    COUNTROWS(Orders),
    Orders[order_status] IN {"Completed", "Partially Delivered"}
)
```

---

### 3. Gross Order Value (INR)
```dax
Gross Order Value =
CALCULATE(
    SUM(Orders[order_value]),
    Orders[order_status] IN {"Completed", "Partially Delivered"}
)
```
> **Denominator:** Completed and Partially Delivered orders only.

---

### 4. Net Sales (INR)
```dax
Net Sales =
CALCULATE(
    SUM(Orders[final_amount]),
    Orders[order_status] IN {"Completed", "Partially Delivered"}
)
```
> **Definition:** Gross order value minus all discounts applied.

---

### 5. Average Delivery Time (minutes)
```dax
Avg Delivery Time =
AVERAGEX(
    Deliveries,
    Deliveries[actual_delivery_minutes]
)
```
> **Note:** Only rows in the Deliveries table (non-cancelled orders) are included.

---

### 6. On-Time Delivery %
```dax
On-Time Delivery % =
DIVIDE(
    CALCULATE(COUNTROWS(Deliveries), Deliveries[on_time_status] = "On Time"),
    COUNTROWS(Deliveries),
    0
)
```
> **Display Format:** Percentage (0.00%)  
> **Denominator:** All delivery records (non-cancelled orders).

---

### 7. Cancellation Rate %
```dax
Cancellation Rate % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Orders),
        Orders[order_status] IN {"Cancelled", "Refunded"}
    ),
    COUNTROWS(Orders),
    0
)
```
> **Display Format:** Percentage (0.00%)  
> **Denominator:** All orders including cancelled.

---

### 8. Average Customer Rating
```dax
Avg Customer Rating =
AVERAGEX(
    Feedback,
    Feedback[rating]
)
```
> **Display Format:** Decimal (0.00)  
> **Note:** Only orders with feedback are included. Use AVERAGEX to handle filter context correctly.

---

### 9. Repeat Order Rate %
```dax
-- Dynamic Period/Slicer-Responsive Measure (Recommended):
Repeat Order Rate % =
VAR ActiveCustomers = VALUES(Orders[customer_id])
VAR TotalCust = COUNTROWS(ActiveCustomers)
VAR RepeatCust =
    COUNTROWS(
        FILTER(
            ActiveCustomers,
            CALCULATE(COUNTROWS(Orders)) >= 2
        )
    )
RETURN
DIVIDE(RepeatCust, TotalCust, 0)
```
> **Display Format:** Percentage (0.00%)  
> **Definition:** % of active customers in the selected filter context (Date, City, Cuisine) who placed 2 or more orders.
> *(Alternative Lifetime version: `DIVIDE(CALCULATE(COUNTROWS(Customers), Customers[total_orders] >= 2), COUNTROWS(Customers), 0)` computes platform-wide lifetime repeat rate across all 20,000 customers).*

---

### 10. Complaint Rate %
```dax
Complaint Rate % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Feedback),
        NOT ISBLANK(Feedback[complaint_type]),
        Feedback[complaint_type] <> ""
    ),
    COUNTROWS(Feedback),
    0
)
```

---

### 11. Total Refund Amount (INR)
```dax
Total Refund Amount =
SUM(Feedback[refund_amount])
```

---

### 12. Average Delay (minutes)
```dax
Avg Delay Minutes =
AVERAGEX(
    Deliveries,
    Deliveries[delay_minutes]
)
```

---

## Advanced Measures

### 13. Revenue per Completed Order
```dax
Avg Revenue per Order =
DIVIDE([Net Sales], [Completed Orders], 0)
```

---

### 14. % Orders with Delay > 30 min
```dax
Pct Severe Delay =
DIVIDE(
    CALCULATE(COUNTROWS(Deliveries), Deliveries[delay_minutes] > 30),
    COUNTROWS(Deliveries),
    0
)
```

---

### 15. Revenue Trend (MoM Change %)
```dax
Net Sales MoM % =
VAR CurrentSales = [Net Sales]
VAR PrevMonthSales =
    CALCULATE(
        [Net Sales],
        DATEADD(DateTable[Date], -1, MONTH)
    )
RETURN
DIVIDE(CurrentSales - PrevMonthSales, PrevMonthSales, BLANK())
```

---

### 16. Rolling 7-Day Orders
```dax
Orders Last 7 Days =
CALCULATE(
    [Total Orders],
    DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -7, DAY)
)
```

---

### 17. Customer Lifetime Value (Average)
```dax
Avg Customer LTV =
AVERAGEX(
    Customers,
    CALCULATE(SUM(Orders[final_amount]),
              RELATEDTABLE(Orders),
              Orders[order_status] IN {"Completed", "Partially Delivered"})
)
```

---

### 18. Rating Trend vs Previous Month
```dax
Rating MoM Change =
VAR CurrentRating = [Avg Customer Rating]
VAR PrevRating =
    CALCULATE(
        [Avg Customer Rating],
        DATEADD(DateTable[Date], -1, MONTH)
    )
RETURN CurrentRating - PrevRating
```

---

### 19. % of Revenue from Loyal Customers (10+ orders)
```dax
Loyal Customer Revenue % =
DIVIDE(
    CALCULATE(
        [Net Sales],
        FILTER(Customers, Customers[total_orders] >= 10)
    ),
    [Net Sales],
    0
)
```

---

### 20. Restaurant Performance Score (Composite)
```dax
Restaurant Score =
VAR NormRating      = DIVIDE([Avg Customer Rating] - 1, 4, 0)      -- 0 to 1
VAR NormOnTime      = [On-Time Delivery %]                          -- 0 to 1
VAR NormLowCancel   = 1 - [Cancellation Rate %]                    -- 0 to 1
VAR NormLowComplaint= 1 - [Complaint Rate %]                       -- 0 to 1
RETURN
(NormRating * 0.35) + (NormOnTime * 0.30) + (NormLowCancel * 0.20) + (NormLowComplaint * 0.15)
```
> **Scale:** 0 to 1 (multiply by 100 for display as %).  
> **Weights:** Rating (35%), On-time (30%), Low cancellation (20%), Low complaints (15%).

---

## Measure Formatting Guide

| Measure | Format String | Example |
|---|---|---|
| Total Orders | `#,##0` | 87,822 |
| Gross/Net Revenue | `₹#,##0` | ₹2,34,56,789 |
| Avg Delivery Time | `0.0 "min"` | 46.4 min |
| On-Time Delivery % | `0.00%` | 82.80% |
| Cancellation Rate % | `0.00%` | 12.18% |
| Avg Customer Rating | `0.00` | 3.71 |
| Repeat Order Rate % | `0.00%` | 58.30% |
| Complaint Rate % | `0.00%` | 24.50% |
| Total Refunds | `₹#,##0` | ₹1,23,456 |
| Restaurant Score | `0%` | 72% |
