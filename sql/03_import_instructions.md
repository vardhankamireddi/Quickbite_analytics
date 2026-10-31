# QuickBite Analytics – SQL Import Instructions
## Team: Data Knights | CODEGNAN DA-07

## Prerequisites
- MySQL 8.0 or higher
- MySQL Workbench (recommended) or MySQL Command Line Client
- CSV files in `data/raw/` directory

---

## Step 1: Create the Database

Run `01_create_database.sql` to create the `quickbite_analytics` database:

```sql
source /path/to/01_create_database.sql;
```

Or in MySQL Workbench: **File → Open SQL Script → 01_create_database.sql → Execute**

---

## Step 2: Create All Tables

Run `02_create_tables.sql` to create all 6 tables with constraints and indexes:

```sql
source /path/to/02_create_tables.sql;
```

---

## Step 3: Configure MySQL for CSV Import

Enable local file loading (run as MySQL root):

```sql
SET GLOBAL local_infile = 1;
```

If using MySQL Workbench, ensure the connection has `OPT_LOCAL_INFILE=1` in advanced options.

---

## Step 4: Import Data in the Correct Order

> **IMPORTANT:** Import in this exact order to satisfy foreign key constraints.

### 4.1 Import Riders (no foreign keys)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/riders.csv'
INTO TABLE riders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(rider_id, rider_city, availability_status);
```

### 4.2 Import Customers (no foreign keys)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, signup_date, city, total_orders);
```

### 4.3 Import Restaurants (no foreign keys)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/restaurants.csv'
INTO TABLE restaurants
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(restaurant_id, restaurant_name, cuisine, area, city, avg_prep_time, restaurant_rating);
```

### 4.4 Import Orders (depends on customers, restaurants, riders)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, restaurant_id, rider_id, order_time, order_value,
 discount, final_amount, order_status, @cancel_reason)
SET cancellation_reason = NULLIF(@cancel_reason, '');
```

### 4.5 Import Deliveries (depends on orders, riders)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/deliveries.csv'
INTO TABLE deliveries
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(delivery_id, order_id, rider_id, pickup_time, delivery_time, distance_km,
 estimated_delivery_time, actual_delivery_minutes, delay_minutes, on_time_status);
```

### 4.6 Import Feedback (depends on orders, customers)

```sql
LOAD DATA LOCAL INFILE '/full/path/to/data/raw/feedback.csv'
INTO TABLE feedback
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(feedback_id, order_id, customer_id, rating, review_text, @complaint_type, refund_amount)
SET complaint_type = NULLIF(@complaint_type, '');
```

---

## Step 5: Verify Import

Run these verification queries:

```sql
USE quickbite_analytics;

SELECT 'riders'      AS tbl, COUNT(*) AS rows FROM riders
UNION ALL
SELECT 'customers',   COUNT(*) FROM customers
UNION ALL
SELECT 'restaurants', COUNT(*) FROM restaurants
UNION ALL
SELECT 'orders',      COUNT(*) FROM orders
UNION ALL
SELECT 'deliveries',  COUNT(*) FROM deliveries
UNION ALL
SELECT 'feedback',    COUNT(*) FROM feedback;
```

**Expected approximate counts:**

| Table | Expected Rows |
|---|---|
| riders | 2,000 |
| customers | 20,000 |
| restaurants | 4,000 |
| orders | 100,000 |
| deliveries | ~87,000 |
| feedback | ~70,000 |

---

## Troubleshooting

| Error | Solution |
|---|---|
| `ERROR 1290: --secure-file-priv` | Use `LOCAL` keyword in LOAD DATA, or copy files to MySQL data dir |
| `ERROR 1406: Data too long` | Check VARCHAR column sizes in 02_create_tables.sql |
| `ERROR 1452: Foreign key violation` | Import in the order specified above (Step 4) |
| `ERROR 1366: Incorrect integer value` | Ensure blank strings are converted to NULL for optional columns |

---

## Alternative: Python Import Script

If LOAD DATA is not available, use Python:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://username:password@localhost/quickbite_analytics'
)

tables = ['riders', 'customers', 'restaurants', 'orders', 'deliveries', 'feedback']
for table in tables:
    df = pd.read_csv(f'data/raw/{table}.csv')
    df.to_sql(table, engine, if_exists='append', index=False, chunksize=5000)
    print(f'Imported {len(df):,} rows into {table}')
```

Install dependencies: `pip install pymysql sqlalchemy`
