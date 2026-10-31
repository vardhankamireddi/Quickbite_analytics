# Data Dictionary – QuickBite Analytics Dataset
## Team: Data Knights | CODEGNAN DA-07 | Version 1.0

> **IMPORTANT:** All data in this project is **SYNTHETIC** and generated for demonstration
> purposes only. It does not represent actual QuickBite business records.

---

## Table: `orders.csv`
Primary Key: `order_id`

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| order_id | STRING | Unique identifier for each order | ORD000001 | Format: ORD + 6-digit number |
| customer_id | STRING | Foreign key to customers table | C00001 | Format: C + 5-digit number |
| restaurant_id | STRING | Foreign key to restaurants table | R0001 | Format: R + 4-digit number |
| rider_id | STRING | Foreign key to riders table | RD0001 | Format: RD + 4-digit number |
| order_time | DATETIME | Timestamp when the order was placed | 2024-03-15 19:32:00 | Format: YYYY-MM-DD HH:MM:SS |
| order_value | FLOAT | Gross order value before discount (INR) | 350.50 | Range: 80–3000 INR |
| discount | FLOAT | Discount applied on the order (INR) | 52.58 | Range: 0–900 INR; 0 if no discount |
| final_amount | FLOAT | Net amount paid after discount (INR) | 297.92 | = order_value − discount |
| order_status | STRING | Final status of the order | Completed | Completed / Cancelled / Refunded / Partially Delivered |
| cancellation_reason | STRING | Reason for cancellation (if applicable) | Long wait time | Empty string if status is Completed |

---

## Table: `restaurants.csv`
Primary Key: `restaurant_id`

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| restaurant_id | STRING | Unique identifier for each restaurant | R0001 | Format: R + 4-digit number |
| restaurant_name | STRING | Name of the restaurant | Spicy Biryani Kitchen | Generated from cuisine-themed templates |
| cuisine | STRING | Primary cuisine category | Biryani | See cuisine list below |
| area | STRING | Neighbourhood/area of the restaurant | Banjara Hills | Specific to the city |
| city | STRING | City where restaurant operates | Hyderabad | Hyderabad / Visakhapatnam / Vijayawada |
| avg_prep_time | FLOAT | Average food preparation time (minutes) | 22.5 | Range: 5–40 min; cuisine-dependent |
| restaurant_rating | FLOAT | Aggregate restaurant rating | 4.1 | Range: 1.0–5.0; 1 decimal |

**Cuisine List:** Biryani, South Indian, North Indian, Chinese, Pizza, Burger, Fast Food, Desserts, Healthy, Continental, Rolls & Wraps, Seafood, Thali

---

## Table: `deliveries.csv`
Primary Key: `delivery_id`  
Foreign Keys: `order_id` → orders, `rider_id` → riders

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| delivery_id | STRING | Unique identifier for each delivery | DEL000001 | Format: DEL + 6-digit number |
| order_id | STRING | Foreign key to orders table | ORD000001 | Only non-cancelled orders have delivery records |
| rider_id | STRING | Foreign key to riders table | RD0001 | Rider assigned to this delivery |
| pickup_time | DATETIME | When rider picked up the order | 2024-03-15 19:55:00 | = order_time + prep_time + wait buffer |
| delivery_time | DATETIME | When order was delivered to customer | 2024-03-15 20:18:00 | = pickup_time + transit_time |
| distance_km | FLOAT | Road distance from restaurant to customer (km) | 4.8 | Range: 0.5–22 km |
| estimated_delivery_time | FLOAT | Estimated total delivery time (minutes) | 35.2 | = prep_time + estimated transit |
| actual_delivery_minutes | FLOAT | Actual total delivery time (minutes) | 43.1 | Includes real delays |
| delay_minutes | FLOAT | Actual delay relative to estimate (minutes) | 7.9 | Negative = early, Positive = delayed |
| on_time_status | STRING | Whether delivery was on time | Delayed | On Time (delay ≤ 5 min) / Delayed |

---

## Table: `customers.csv`
Primary Key: `customer_id`

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| customer_id | STRING | Unique identifier for each customer | C00001 | Format: C + 5-digit number |
| signup_date | DATE | Date customer registered on QuickBite | 2023-04-20 | Format: YYYY-MM-DD; range 2023-01-01 to 2024-12-31 |
| city | STRING | City the customer is located in | Hyderabad | Hyderabad / Visakhapatnam / Vijayawada |
| total_orders | INTEGER | Total number of orders placed by customer | 12 | Reflects actual order count in orders.csv |

**Note:** No personal identifiers (name, phone, email, address) are stored.

---

## Table: `feedback.csv`
Primary Key: `feedback_id`  
Foreign Keys: `order_id` → orders, `customer_id` → customers

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| feedback_id | STRING | Unique identifier for each feedback record | FB000001 | Format: FB + 6-digit number |
| order_id | STRING | Foreign key to orders table | ORD000001 | Only completed orders have feedback |
| customer_id | STRING | Foreign key to customers table | C00001 | Must match the customer from the order |
| rating | INTEGER | Customer rating for the delivery experience | 4 | Range: 1–5 (integer stars) |
| review_text | STRING | Short review comment | "Great food, quick delivery!" | Templated text; ~80% of completed orders have feedback |
| complaint_type | STRING | Category of complaint (if any) | Late Delivery | Empty string if no complaint |
| refund_amount | FLOAT | Refund issued (INR) | 0.0 | 0 if no refund; non-zero mainly for 1–2 star ratings |

**Complaint Types:** Late Delivery, Wrong Item, Cold Food, Missing Item, Poor Packaging, Rude Rider, Quality Issue, Overcharge

---

## Table: `riders.csv`
Primary Key: `rider_id`

| Field | Data Type | Description | Example | Valid Values / Notes |
|---|---|---|---|---|
| rider_id | STRING | Unique identifier for each rider | RD0001 | Format: RD + 4-digit number |
| rider_city | STRING | City where the rider operates | Hyderabad | Hyderabad / Visakhapatnam / Vijayawada |
| availability_status | STRING | Current availability of the rider | Active | Active / Inactive / On Leave |

**Availability Distribution:** ~80% Active, ~12% Inactive, ~8% On Leave

---

## Key Relationships

```
customers (customer_id)
    └── orders (customer_id → customer_id)
            └── deliveries (order_id → order_id)
            └── feedback   (order_id → order_id)

restaurants (restaurant_id)
    └── orders (restaurant_id → restaurant_id)

riders (rider_id)
    └── orders (rider_id → rider_id)
    └── deliveries (rider_id → rider_id)
```

---

## Cancellation Logic

| order_status | Has delivery record? | Has feedback record? | Has cancellation_reason? |
|---|---|---|---|
| Completed | ✓ Yes | ✓ Yes (~80%) | ✗ No |
| Cancelled | ✗ No | ✗ No | ✓ Yes |
| Refunded | ✗ No | ✗ No | ✓ Yes |
| Partially Delivered | ✓ Yes | ✓ Yes (~80%) | ✗ No |
