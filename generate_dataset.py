"""
QuickBite Synthetic Dataset Generator
======================================
Team: Data Knights | Problem: DA-07 | Hackathon: CODEGNAN
Generates realistic synthetic data for food delivery analytics.

NOTE: All data is explicitly SYNTHETIC and generated for demonstration purposes only.
      It does not represent actual QuickBite business records.

Random Seed: 42 (for full reproducibility)
"""

import numpy as np
import pandas as pd
import random
import os
from datetime import datetime, timedelta

# ── Configuration ────────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

N_ORDERS       = 100_000
N_RESTAURANTS  = 4_000
N_CUSTOMERS    = 20_000
N_RIDERS       = 2_000

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
RAW_DIR    = os.path.join(BASE_DIR, "data", "raw")
DIRTY_DIR  = os.path.join(BASE_DIR, "data", "dirty")

START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

CITIES = ["Hyderabad", "Visakhapatnam", "Vijayawada"]
CITY_WEIGHTS = [0.55, 0.25, 0.20]   # Population-proportional weights

# Areas per city
CITY_AREAS = {
    "Hyderabad": [
        "Banjara Hills", "Jubilee Hills", "Gachibowli", "Madhapur",
        "Hitech City", "Kukatpally", "Kondapur", "Begumpet",
        "Secunderabad", "Ameerpet", "Dilsukhnagar", "LB Nagar",
        "Miyapur", "Chandanagar", "Uppal",
    ],
    "Visakhapatnam": [
        "Dwaraka Nagar", "MVP Colony", "Gajuwaka", "Rushikonda",
        "Maddilapalem", "Seethammadhara", "Asilmetta", "Jagadamba",
        "Bheemunipatnam", "Kommadi",
    ],
    "Vijayawada": [
        "Benz Circle", "Governorpet", "MG Road", "Patamata",
        "Gunadala", "Machavaram", "Moghalrajpuram", "Auto Nagar",
        "Kanuru", "Ramavarappadu",
    ],
}

CUISINES = [
    "Biryani", "South Indian", "North Indian", "Chinese",
    "Pizza", "Burger", "Fast Food", "Desserts", "Healthy",
    "Continental", "Rolls & Wraps", "Seafood", "Thali",
]

CANCEL_REASONS = [
    "Customer cancelled", "Restaurant not accepting",
    "Item unavailable", "Payment failed", "Long wait time",
    "Duplicate order", "Address issue", "No rider available",
]

COMPLAINT_TYPES = [
    "Late Delivery", "Wrong Item", "Cold Food",
    "Missing Item", "Poor Packaging", "Rude Rider",
    "Quality Issue", "Overcharge",
]

REVIEW_TEMPLATES = {
    5: ["Excellent! Loved it.", "Perfect delivery and great food!", "Will order again definitely.",
        "Hot and fresh, arrived on time.", "Outstanding experience."],
    4: ["Good experience overall.", "Food was nice, slightly delayed.",
        "Pretty good, would recommend.", "Satisfied with the order."],
    3: ["Average experience.", "Food was okay, took some time.",
        "Neither good nor bad.", "Delivery was acceptable."],
    2: ["Disappointed with the food quality.", "Delivery was quite late.",
        "Not what I expected.", "Food arrived cold."],
    1: ["Very bad experience. Will not order again.", "Wrong items delivered!",
        "Extremely late delivery.", "Terrible food quality.", "Refund requested!"],
}

print("=" * 60)
print("  QuickBite Synthetic Dataset Generator")
print("  Team: Data Knights | CODEGNAN DA-07")
print("=" * 60)

# ── 1. RESTAURANTS ───────────────────────────────────────────────────────────
print("\n[1/6] Generating restaurants...")

rest_ids      = [f"R{str(i).zfill(4)}" for i in range(1, N_RESTAURANTS + 1)]
rest_cities   = np.random.choice(CITIES, size=N_RESTAURANTS, p=CITY_WEIGHTS)
rest_areas    = [
    np.random.choice(CITY_AREAS[city]) for city in rest_cities
]
rest_cuisines = np.random.choice(CUISINES, size=N_RESTAURANTS)

# Restaurant names
adj = ["Spicy", "Royal", "Golden", "Fresh", "Quick", "Tasty", "Classic",
       "Authentic", "Premium", "Star", "Grand", "Local", "Urban", "Home"]
noun = ["Kitchen", "Bites", "House", "Point", "Corner", "Hub", "Eatery",
        "Diner", "Place", "Express", "Station", "Stop", "Cafe", "Delight"]
rest_names = [
    f"{random.choice(adj)} {c} {random.choice(noun)}" for c in rest_cuisines
]

# Preparation times (minutes) – varies by cuisine
cuisine_prep = {
    "Biryani": (25, 8), "South Indian": (15, 5), "North Indian": (20, 6),
    "Chinese": (18, 5), "Pizza": (20, 6), "Burger": (12, 4),
    "Fast Food": (10, 3), "Desserts": (10, 4), "Healthy": (15, 4),
    "Continental": (22, 6), "Rolls & Wraps": (12, 3), "Seafood": (25, 7),
    "Thali": (20, 5),
}
avg_prep = np.array([
    max(5, np.random.normal(cuisine_prep[c][0], cuisine_prep[c][1]))
    for c in rest_cuisines
]).round(1)

# Restaurant ratings – slightly right-skewed (most are 3.5–4.5)
rest_ratings = np.clip(np.random.normal(3.9, 0.5, N_RESTAURANTS), 1.0, 5.0).round(1)

restaurants_df = pd.DataFrame({
    "restaurant_id":    rest_ids,
    "restaurant_name":  rest_names,
    "cuisine":          rest_cuisines,
    "area":             rest_areas,
    "city":             rest_cities,
    "avg_prep_time":    avg_prep,
    "restaurant_rating": rest_ratings,
})
print(f"   ✓ {len(restaurants_df):,} restaurants generated")

# ── 2. CUSTOMERS ─────────────────────────────────────────────────────────────
print("[2/6] Generating customers...")

cust_ids     = [f"C{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)]
cust_cities  = np.random.choice(CITIES, size=N_CUSTOMERS, p=CITY_WEIGHTS)

# Signup dates spread across 2023-2024
signup_days  = np.random.randint(0, 730, size=N_CUSTOMERS)
signup_dates = [
    (datetime(2023, 1, 1) + timedelta(days=int(d))).strftime("%Y-%m-%d")
    for d in signup_days
]

# total_orders will be filled after order generation
customers_df = pd.DataFrame({
    "customer_id":  cust_ids,
    "signup_date":  signup_dates,
    "city":         cust_cities,
    "total_orders": 0,      # placeholder
})
print(f"   ✓ {len(customers_df):,} customers generated")

# ── 3. RIDERS ────────────────────────────────────────────────────────────────
print("[3/6] Generating riders...")

rider_ids     = [f"RD{str(i).zfill(4)}" for i in range(1, N_RIDERS + 1)]
rider_cities  = np.random.choice(CITIES, size=N_RIDERS, p=CITY_WEIGHTS)
avail_status  = np.random.choice(
    ["Active", "Inactive", "On Leave"],
    size=N_RIDERS, p=[0.80, 0.12, 0.08]
)

riders_df = pd.DataFrame({
    "rider_id":           rider_ids,
    "rider_city":         rider_cities,
    "availability_status": avail_status,
})
print(f"   ✓ {len(riders_df):,} riders generated")

# ── 4. ORDERS ────────────────────────────────────────────────────────────────
print("[4/6] Generating orders (this may take a moment)...")

# Hour-of-day weights — realistic peak patterns
# Peak: 12–14 (lunch), 19–22 (dinner); low: 4–7 (night)
hour_weights_raw = [
    0.5, 0.3, 0.2, 0.2, 0.3, 0.5,    # 0–5
    0.8, 1.5, 2.0, 2.5, 3.0, 4.5,    # 6–11
    7.0, 7.5, 5.0, 3.5, 3.0, 4.5,    # 12–17
    6.5, 8.5, 9.0, 8.0, 6.0, 3.0,    # 18–23
]
hw_sum = sum(hour_weights_raw)
hour_weights = [w / hw_sum for w in hour_weights_raw]

# Customer order frequency: many one-timers, some repeats, few heavy users
# Use negative binomial for realistic distribution
cust_order_counts = 1 + np.random.negative_binomial(1, 0.35, N_CUSTOMERS)
cust_order_counts = np.clip(cust_order_counts, 1, 80)
total_implied = cust_order_counts.sum()

# Sample N_ORDERS customer IDs proportional to their order counts
cust_probs    = cust_order_counts / cust_order_counts.sum()
order_cust    = np.random.choice(cust_ids, size=N_ORDERS, p=cust_probs)

# Match customer city to nearby restaurant
cust_city_map = dict(zip(customers_df.customer_id, customers_df.city))
order_cities  = [cust_city_map[c] for c in order_cust]

# Pick restaurant from same city
city_rest_map = {
    city: restaurants_df[restaurants_df.city == city].restaurant_id.tolist()
    for city in CITIES
}
order_rest = np.array([
    random.choice(city_rest_map[city]) for city in order_cities
])

# Pick rider from same city (or nearby)
city_rider_map = {
    city: riders_df[riders_df.rider_city == city].rider_id.tolist()
    for city in CITIES
}
# Fallback for very small city rider pools
all_riders = riders_df.rider_id.tolist()
order_riders = np.array([
    random.choice(city_rider_map.get(city, all_riders))
    for city in order_cities
])

# Order timestamps
order_days   = np.random.randint(0, 365, size=N_ORDERS)
order_hours  = np.random.choice(range(24), size=N_ORDERS, p=hour_weights)
order_mins   = np.random.randint(0, 60, size=N_ORDERS)
order_times  = [
    START_DATE + timedelta(days=int(d), hours=int(h), minutes=int(m))
    for d, h, m in zip(order_days, order_hours, order_mins)
]

# Order values (INR)
order_values = np.random.lognormal(mean=5.8, sigma=0.5, size=N_ORDERS).round(2)
order_values = np.clip(order_values, 80, 3000)

# Discounts (0–30% of order value, often 0)
has_discount  = np.random.choice([True, False], size=N_ORDERS, p=[0.45, 0.55])
disc_pct      = np.where(has_discount, np.random.uniform(0.05, 0.30, N_ORDERS), 0.0)
discounts     = (order_values * disc_pct).round(2)
final_amounts = (order_values - discounts).round(2)

# Order status
# Cancellation higher during peak hours (dinner)
cancel_prob_by_hour = {h: 0.08 + 0.06 * (1 if h in [19, 20, 21, 22] else 0) for h in range(24)}
status_list = []
for h in order_hours:
    cp = cancel_prob_by_hour[h]
    status_list.append(np.random.choice(
        ["Completed", "Cancelled", "Refunded", "Partially Delivered"],
        p=[1 - cp - 0.02 - 0.01, cp, 0.02, 0.01]
    ))
order_status = np.array(status_list)

# Cancellation reasons (only for cancelled/refunded orders)
cancel_mask = np.isin(order_status, ["Cancelled", "Refunded"])
cancel_reasons = np.where(
    cancel_mask,
    np.random.choice(CANCEL_REASONS, size=N_ORDERS),
    ""
)

order_ids = [f"ORD{str(i).zfill(6)}" for i in range(1, N_ORDERS + 1)]

orders_df = pd.DataFrame({
    "order_id":          order_ids,
    "customer_id":       order_cust,
    "restaurant_id":     order_rest,
    "rider_id":          order_riders,
    "order_time":        order_times,
    "order_value":       order_values,
    "discount":          discounts,
    "final_amount":      final_amounts,
    "order_status":      order_status,
    "cancellation_reason": cancel_reasons,
})
print(f"   ✓ {len(orders_df):,} orders generated")
print(f"     Status distribution:\n{orders_df.order_status.value_counts().to_string()}")

# Update customer total_orders
order_counts_actual = orders_df.groupby("customer_id").size().reset_index(name="total_orders")
customers_df = customers_df.merge(order_counts_actual, on="customer_id", how="left")
customers_df["total_orders"] = customers_df["total_orders_y"].fillna(0).astype(int)
customers_df.drop(columns=["total_orders_x", "total_orders_y"], errors="ignore", inplace=True)
# Handle merge suffix if total_orders_x/y not present
if "total_orders" not in customers_df.columns:
    customers_df["total_orders"] = 0

# ── 5. DELIVERIES ────────────────────────────────────────────────────────────
print("[5/6] Generating delivery records...")

# Only non-cancelled orders get deliveries
completed_orders = orders_df[~cancel_mask].copy()
n_del = len(completed_orders)

del_ids = [f"DEL{str(i).zfill(6)}" for i in range(1, n_del + 1)]

# Distance 0.5–20 km; most 2–10 km
dist_km = np.clip(np.random.lognormal(1.8, 0.5, n_del), 0.5, 22).round(2)

# Estimated delivery time based on distance + prep time
rest_prep_map = dict(zip(restaurants_df.restaurant_id, restaurants_df.avg_prep_time))
prep_times = np.array([rest_prep_map[r] for r in completed_orders.restaurant_id])

# Avg rider speed 15–20 km/h in city traffic
avg_speed_kmh = np.random.uniform(14, 20, n_del)
transit_time  = (dist_km / avg_speed_kmh * 60)  # minutes
estimated_del = (prep_times + transit_time).round(1)

# Actual delivery time — add noise; 25% chance of delay
delay_prob  = np.random.random(n_del)
# Peak hours: higher delay probability
order_hour_arr = np.array([t.hour for t in completed_orders.order_time])
peak_mask   = np.isin(order_hour_arr, [12, 13, 14, 19, 20, 21, 22])
delay_prob  = np.where(peak_mask, delay_prob * 0.6, delay_prob)  # reduce threshold for peak

# Delay categories
delay_minutes = np.where(
    delay_prob < 0.60,  # on-time or early
    np.random.uniform(-5, 5, n_del),
    np.where(
        delay_prob < 0.85,  # mild delay
        np.random.uniform(5, 25, n_del),
        # Severe delay
        np.random.uniform(25, 70, n_del),
    )
).round(1)

actual_del = np.maximum((estimated_del + delay_minutes), estimated_del * 0.6).round(1)
on_time_status = np.where(delay_minutes <= 5, "On Time", "Delayed")

# Pickup time = order_time + prep_time (+ small restaurant wait)
pickup_offsets = prep_times + np.random.uniform(0, 8, n_del)
pickup_times   = [
    t + timedelta(minutes=float(p))
    for t, p in zip(completed_orders.order_time, pickup_offsets)
]
delivery_times = [
    pt + timedelta(minutes=float(a))
    for pt, a in zip(pickup_times, actual_del)
]

deliveries_df = pd.DataFrame({
    "delivery_id":              del_ids,
    "order_id":                 completed_orders.order_id.values,
    "rider_id":                 completed_orders.rider_id.values,
    "pickup_time":              pickup_times,
    "delivery_time":            delivery_times,
    "distance_km":              dist_km,
    "estimated_delivery_time":  estimated_del,
    "actual_delivery_minutes":  actual_del,
    "delay_minutes":            delay_minutes,
    "on_time_status":           on_time_status,
})
print(f"   ✓ {len(deliveries_df):,} delivery records generated")
print(f"     On-time rate: {(deliveries_df.on_time_status=='On Time').mean()*100:.1f}%")

# ── 6. FEEDBACK ──────────────────────────────────────────────────────────────
print("[6/6] Generating customer feedback...")

# ~80% of completed orders get feedback
feedback_mask = (np.random.random(n_del) < 0.80)
fb_orders     = completed_orders[feedback_mask].copy()
n_fb          = len(fb_orders)

fb_ids = [f"FB{str(i).zfill(6)}" for i in range(1, n_fb + 1)]

# Rating correlates negatively with delay
fb_delay = delay_minutes[feedback_mask]
# Base rating from restaurant rating
fb_rest_rating = np.array([rest_ratings[rest_ids.index(r)] for r in fb_orders.restaurant_id])

# Rating model: start from restaurant rating, penalize for delays
rating_noise  = np.random.normal(0, 0.4, n_fb)
raw_rating    = fb_rest_rating + rating_noise - (np.clip(fb_delay, 0, 60) / 30)
ratings       = np.clip(np.round(raw_rating).astype(int), 1, 5)

# Review text
reviews = [random.choice(REVIEW_TEMPLATES[r]) for r in ratings]

# Complaint types — more likely for low ratings or delayed orders
has_complaint = (ratings <= 3) | (fb_delay > 20)
complaint_types = np.where(
    has_complaint,
    np.random.choice(COMPLAINT_TYPES, size=n_fb),
    ""
)

# Refund amount — mostly for 1-star, partial for 2-star
refund_amounts = np.where(
    ratings == 1,
    (fb_orders.final_amount.values * np.random.uniform(0.5, 1.0, n_fb)).round(2),
    np.where(
        ratings == 2,
        (fb_orders.final_amount.values * np.random.uniform(0.0, 0.3, n_fb)).round(2),
        0.0
    )
)

feedback_df = pd.DataFrame({
    "feedback_id":    fb_ids,
    "order_id":       fb_orders.order_id.values,
    "customer_id":    fb_orders.customer_id.values,
    "rating":         ratings,
    "review_text":    reviews,
    "complaint_type": complaint_types,
    "refund_amount":  refund_amounts,
})
print(f"   ✓ {len(feedback_df):,} feedback records generated")
print(f"     Avg rating: {feedback_df.rating.mean():.2f}")

# ── SAVE RAW DATASETS ────────────────────────────────────────────────────────
print("\nSaving raw datasets...")

# Format timestamps for CSV
orders_df_save     = orders_df.copy()
deliveries_df_save = deliveries_df.copy()
orders_df_save["order_time"] = orders_df_save["order_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
deliveries_df_save["pickup_time"]   = deliveries_df_save["pickup_time"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if hasattr(x, 'strftime') else x)
deliveries_df_save["delivery_time"] = deliveries_df_save["delivery_time"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if hasattr(x, 'strftime') else x)

datasets = {
    "orders.csv":       orders_df_save,
    "restaurants.csv":  restaurants_df,
    "deliveries.csv":   deliveries_df_save,
    "customers.csv":    customers_df,
    "feedback.csv":     feedback_df,
    "riders.csv":       riders_df,
}

for fname, df in datasets.items():
    path = os.path.join(RAW_DIR, fname)
    df.to_csv(path, index=False)
    size_kb = os.path.getsize(path) / 1024
    print(f"   ✓ {fname:25s} → {len(df):>7,} rows | {size_kb:>7.1f} KB")

# ── DIRTY DATASET COPY ────────────────────────────────────────────────────────
print("\nGenerating dirty dataset copies for data cleaning demo...")

def make_dirty(df, name):
    """Introduce realistic data quality issues into a dataframe."""
    dirty = df.copy()
    n = len(dirty)
    rng = np.random.RandomState(42)

    # 1. Missing values (~3–5%)
    num_cols = dirty.select_dtypes(include=[np.number]).columns.tolist()
    str_cols = dirty.select_dtypes(include=[object]).columns.tolist()
    miss_cols = num_cols[:2] + str_cols[:2] if len(str_cols) >= 2 else num_cols[:2]
    for col in miss_cols:
        miss_idx = rng.choice(n, size=int(n * 0.03), replace=False)
        dirty.iloc[miss_idx, dirty.columns.get_loc(col)] = np.nan

    # 2. Duplicates (~1%)
    dup_rows = dirty.sample(frac=0.01, random_state=42)
    dirty = pd.concat([dirty, dup_rows], ignore_index=True)

    # 3. Invalid values in numeric columns
    if num_cols:
        neg_idx = rng.choice(n, size=int(n * 0.005), replace=False)
        dirty.iloc[neg_idx, dirty.columns.get_loc(num_cols[0])] = -abs(
            dirty.iloc[neg_idx, dirty.columns.get_loc(num_cols[0])].fillna(0)
        )

    # 4. Date format inconsistencies (for orders)
    if "order_time" in dirty.columns:
        alt_fmt_idx = rng.choice(n, size=int(n * 0.02), replace=False)
        dirty.loc[alt_fmt_idx[:len(alt_fmt_idx)//2], "order_time"] = \
            dirty.loc[alt_fmt_idx[:len(alt_fmt_idx)//2], "order_time"].apply(
                lambda x: str(x)[:10] if isinstance(x, str) else x
            )

    # 5. Inconsistent case in text columns
    if str_cols:
        case_col = str_cols[0]
        case_idx = rng.choice(n, size=int(n * 0.03), replace=False)
        dirty.iloc[case_idx, dirty.columns.get_loc(case_col)] = \
            dirty.iloc[case_idx, dirty.columns.get_loc(case_col)].apply(
                lambda x: str(x).upper() if isinstance(x, str) else x
            )

    # 6. Out-of-range ratings (for feedback)
    if "rating" in dirty.columns:
        oor_idx = rng.choice(n, size=int(n * 0.005), replace=False)
        dirty.loc[oor_idx, "rating"] = rng.choice([0, 6, 7, -1], size=len(oor_idx))

    return dirty

for fname, df in datasets.items():
    dirty = make_dirty(df, fname)
    path  = os.path.join(DIRTY_DIR, fname.replace(".csv", "_dirty.csv"))
    dirty.to_csv(path, index=False)
    print(f"   ✓ {fname.replace('.csv','_dirty.csv'):35s} → {len(dirty):>7,} rows")

print("\n" + "=" * 60)
print("  Dataset generation COMPLETE!")
print(f"  Raw data  → {RAW_DIR}")
print(f"  Dirty data→ {DIRTY_DIR}")
print("=" * 60)

# Summary statistics
print("\nQUICK SUMMARY")
print("-" * 40)
print(f"Total orders      : {len(orders_df):>10,}")
print(f"Completed orders  : {(~cancel_mask).sum():>10,}")
print(f"Cancelled orders  : {cancel_mask.sum():>10,}")
print(f"Total restaurants : {len(restaurants_df):>10,}")
print(f"Total customers   : {len(customers_df):>10,}")
print(f"Total riders      : {len(riders_df):>10,}")
print(f"Total deliveries  : {len(deliveries_df):>10,}")
print(f"Total feedback    : {len(feedback_df):>10,}")
print(f"Avg rating        : {feedback_df.rating.mean():>10.2f}")
print(f"Avg delivery time : {deliveries_df.actual_delivery_minutes.mean():>10.1f} min")
print(f"On-time delivery  : {(deliveries_df.on_time_status=='On Time').mean()*100:>9.1f}%")
print(f"Cancellation rate : {cancel_mask.mean()*100:>9.1f}%")
