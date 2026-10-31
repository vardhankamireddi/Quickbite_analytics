import os, glob
import pandas as pd
import numpy as np

RAW_DIR = "quickbite-analytics/data/raw"
DIRTY_DIR = "quickbite-analytics/data/dirty"

print("--- AUDITING RAW DATA ---")
raw_files = ["customers.csv", "deliveries.csv", "feedback.csv", "orders.csv", "restaurants.csv", "riders.csv"]
raw_dfs = {}
for rf in raw_files:
    path = os.path.join(RAW_DIR, rf)
    df = pd.read_csv(path, low_memory=False)
    raw_dfs[rf] = df
    print(f"\nFile: {rf}")
    print(f"  Rows: {len(df):,}, Cols: {len(df.columns)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Null counts:\n{df.isnull().sum()[df.isnull().sum() > 0].to_dict()}")
    print(f"  Duplicates: {df.duplicated().sum()}")
    id_col = [c for c in df.columns if c.endswith('_id')][0]
    print(f"  Primary Key '{id_col}' unique: {df[id_col].is_unique} ({df[id_col].nunique():,} unique)")

# Join audits
print("\n--- AUDITING REFERENTIAL INTEGRITY & JOINS ---")
orders = raw_dfs["orders.csv"]
customers = raw_dfs["customers.csv"]
restaurants = raw_dfs["restaurants.csv"]
deliveries = raw_dfs["deliveries.csv"]
feedback = raw_dfs["feedback.csv"]
riders = raw_dfs["riders.csv"]

print("Orders -> Customers FK valid:", orders["customer_id"].isin(customers["customer_id"]).all())
print("Orders -> Restaurants FK valid:", orders["restaurant_id"].isin(restaurants["restaurant_id"]).all())
print("Orders -> Riders FK valid:", orders["rider_id"].isin(riders["rider_id"]).all())
print("Deliveries -> Orders FK valid:", deliveries["order_id"].isin(orders["order_id"]).all())
print("Deliveries -> Riders FK valid:", deliveries["rider_id"].isin(riders["rider_id"]).all())
print("Feedback -> Orders FK valid:", feedback["order_id"].isin(orders["order_id"]).all())
print("Feedback -> Customers FK valid:", feedback["customer_id"].isin(customers["customer_id"]).all())

print("\n--- CARDINALITY CHECKS ---")
print("Deliveries per order_id max:", deliveries.groupby("order_id").size().max())
print("Feedback per order_id max:", feedback.groupby("order_id").size().max())
print("Orders count:", len(orders))
print("Cancelled/Refunded orders:", orders["order_status"].isin(["Cancelled", "Refunded"]).sum())
print("Completed/Partially Delivered orders:", orders["order_status"].isin(["Completed", "Partially Delivered"]).sum())
print("Deliveries count:", len(deliveries))
print("Feedback count:", len(feedback))

# Check cancellation delivery overlap
cancelled_ids = set(orders[orders["order_status"].isin(["Cancelled", "Refunded"])]["order_id"])
del_on_cancelled = deliveries[deliveries["order_id"].isin(cancelled_ids)]
print("Deliveries for cancelled orders:", len(del_on_cancelled))
fb_on_cancelled = feedback[feedback["order_id"].isin(cancelled_ids)]
print("Feedback for cancelled orders:", len(fb_on_cancelled))

# Check numeric values
print("\n--- VALUE RANGE CHECKS ---")
print("Order value min/max:", orders["order_value"].min(), orders["order_value"].max())
print("Discount min/max:", orders["discount"].min(), orders["discount"].max())
print("Final amount min/max:", orders["final_amount"].min(), orders["final_amount"].max())
print("Final amount mismatch with (order_value - discount):", ((orders["order_value"] - orders["discount"]).round(2) != orders["final_amount"]).sum())
print("Delivery actual_delivery_minutes min/max:", deliveries["actual_delivery_minutes"].min(), deliveries["actual_delivery_minutes"].max())
print("Delivery delay_minutes min/max:", deliveries["delay_minutes"].min(), deliveries["delay_minutes"].max())
print("Feedback rating min/max:", feedback["rating"].min(), feedback["rating"].max())
print("Restaurant prep time min/max:", restaurants["avg_prep_time"].min(), restaurants["avg_prep_time"].max())
print("Restaurant rating min/max:", restaurants["restaurant_rating"].min(), restaurants["restaurant_rating"].max())
