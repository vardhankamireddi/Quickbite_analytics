import os, shutil, sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')
PBI_DIR = os.path.join(BASE_DIR, 'data', 'powerbi')
PBI_READY_DIR = os.path.join(BASE_DIR, 'powerbi', 'powerbi_ready_data')

os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(PBI_DIR, exist_ok=True)
os.makedirs(PBI_READY_DIR, exist_ok=True)

print("Loading raw datasets from:", RAW_DIR)
orders = pd.read_csv(os.path.join(RAW_DIR, 'orders.csv'), low_memory=False)
restaurants = pd.read_csv(os.path.join(RAW_DIR, 'restaurants.csv'), low_memory=False)
deliveries = pd.read_csv(os.path.join(RAW_DIR, 'deliveries.csv'), low_memory=False)
customers = pd.read_csv(os.path.join(RAW_DIR, 'customers.csv'), low_memory=False)
feedback = pd.read_csv(os.path.join(RAW_DIR, 'feedback.csv'), low_memory=False)
riders = pd.read_csv(os.path.join(RAW_DIR, 'riders.csv'), low_memory=False)

print(f"Raw orders: {len(orders):,}")
print(f"Raw deliveries: {len(deliveries):,}")
print(f"Raw restaurants: {len(restaurants):,}")
print(f"Raw customers: {len(customers):,}")
print(f"Raw feedback: {len(feedback):,}")
print(f"Raw riders: {len(riders):,}")

# Datetime conversion
orders['order_time'] = pd.to_datetime(orders['order_time'])
deliveries['pickup_time'] = pd.to_datetime(deliveries['pickup_time'])
deliveries['delivery_time'] = pd.to_datetime(deliveries['delivery_time'])
customers['signup_date'] = pd.to_datetime(customers['signup_date'])

# Feature engineering - Orders
orders['order_date'] = orders['order_time'].dt.strftime('%Y-%m-%d')
orders['order_hour'] = orders['order_time'].dt.hour
orders['order_month'] = orders['order_time'].dt.month
orders['order_day_name'] = orders['order_time'].dt.day_name()
orders['time_segment'] = pd.cut(
    orders['order_hour'],
    bins=[-1, 5, 11, 14, 17, 22, 23],
    labels=['Late Night', 'Morning', 'Lunch Peak', 'Afternoon', 'Dinner Peak', 'Night']
)
orders['is_cancelled'] = orders['order_status'].isin(['Cancelled', 'Refunded'])

# Feature engineering - Deliveries
deliveries['delay_category'] = pd.cut(
    deliveries['delay_minutes'],
    bins=[-np.inf, 0, 5, 15, 30, 60, np.inf],
    labels=['Early', 'On Time', 'Slight Delay', 'Moderate Delay', 'Significant Delay', 'Severe Delay']
)

# Feature engineering - Customers
cust_order_counts = orders.groupby('customer_id').size().reset_index(name='order_count')
customers = customers.drop(columns=['order_count'], errors='ignore').merge(cust_order_counts, on='customer_id', how='left')
customers['order_count'] = customers['order_count'].fillna(0).astype(int)
customers['customer_segment'] = pd.cut(
    customers['order_count'],
    bins=[-1, 0, 1, 3, 9, np.inf],
    labels=['No Orders', 'One-Time', '2-3 Orders', '4-9 Orders (Regular)', '10+ Orders (Loyal)']
)

# Format timestamps for saving
orders_save = orders.copy()
orders_save['order_time'] = orders_save['order_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

deliveries_save = deliveries.copy()
deliveries_save['pickup_time'] = deliveries_save['pickup_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
deliveries_save['delivery_time'] = deliveries_save['delivery_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

customers_save = customers.copy()
customers_save['signup_date'] = customers_save['signup_date'].dt.strftime('%Y-%m-%d')

cleaned_dfs = {
    'orders_cleaned.csv': orders_save,
    'deliveries_cleaned.csv': deliveries_save,
    'restaurants_cleaned.csv': restaurants,
    'customers_cleaned.csv': customers_save,
    'feedback_cleaned.csv': feedback,
    'riders_cleaned.csv': riders,
}

print("\n--- SAVING CLEANED DATASETS ---")
for fname, df in cleaned_dfs.items():
    p1 = os.path.join(CLEANED_DIR, fname)
    df.to_csv(p1, index=False)
    p2 = os.path.join(PBI_DIR, fname)
    df.to_csv(p2, index=False)
    p3 = os.path.join(PBI_READY_DIR, fname)
    df.to_csv(p3, index=False)
    print(f"Saved {fname:25s} -> {len(df):>7,} rows | {os.path.getsize(p1)/1024:>7.1f} KB")

# Also regenerate pbi_orders_master.csv to make sure it includes clean features
print("\n--- GENERATING PBI ORDERS MASTER TABLE ---")
pbi_orders = (orders
    .merge(restaurants[['restaurant_id','restaurant_name','cuisine','area','city']], on='restaurant_id')
    .merge(deliveries[['order_id','actual_delivery_minutes','on_time_status',
                        'delay_minutes','delay_category','distance_km','estimated_delivery_time']],
           on='order_id', how='left')
    .merge(feedback[['order_id','rating','complaint_type','refund_amount']],
           on='order_id', how='left')
)
pbi_orders['order_time'] = pbi_orders['order_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
pbi_master_path = os.path.join(PBI_DIR, 'pbi_orders_master.csv')
pbi_orders.to_csv(pbi_master_path, index=False)
shutil.copy(pbi_master_path, os.path.join(PBI_READY_DIR, 'pbi_orders_master.csv'))
print(f"Saved pbi_orders_master.csv: {len(pbi_orders):,} rows | {os.path.getsize(pbi_master_path)/(1024*1024):.1f} MB")
