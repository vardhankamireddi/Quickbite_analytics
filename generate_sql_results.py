"""
QuickBite Analytics – SQL Results Summary Generator (Comprehensive: All 20 Queries)
Generates: sql/05_sql_results_summary.md
           sql/05_Q*.csv (Q01 to Q20 results)
           data/powerbi/*.csv (Power BI-optimized exports)
"""
import pandas as pd
import numpy as np
import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')
RAW_DIR     = os.path.join(BASE_DIR, 'data', 'raw')
PBI_DIR     = os.path.join(BASE_DIR, 'data', 'powerbi')
PBI_READY   = os.path.join(BASE_DIR, 'powerbi', 'powerbi_ready_data')
SQL_DIR     = os.path.join(BASE_DIR, 'sql')

def load(fname):
    for d in [CLEANED_DIR, RAW_DIR]:
        p = os.path.join(d, fname)
        pp = os.path.join(d, fname.replace('_cleaned',''))
        for path in [p, pp]:
            if os.path.exists(path):
                return pd.read_csv(path, low_memory=False)
    raise FileNotFoundError(fname)

print("Loading data for all 20 SQL analytical queries...")
orders      = load('orders_cleaned.csv')
restaurants = load('restaurants_cleaned.csv')
deliveries  = load('deliveries_cleaned.csv')
customers   = load('customers_cleaned.csv')
feedback    = load('feedback_cleaned.csv')
riders      = load('riders_cleaned.csv')

orders['order_time']   = pd.to_datetime(orders['order_time'])
deliveries['pickup_time']   = pd.to_datetime(deliveries['pickup_time'])
deliveries['delivery_time'] = pd.to_datetime(deliveries['delivery_time'])
orders['order_hour']   = orders['order_time'].dt.hour
orders['order_month']  = orders['order_time'].dt.month
orders['order_date']   = orders['order_time'].dt.date
orders['is_cancelled'] = orders['order_status'].isin(['Cancelled','Refunded'])
completed = orders[orders['order_status'].isin(['Completed','Partially Delivered'])]

results = {}

# ── Q01: Total Orders by City ────────────────────────────────────────────────
q01 = (orders
    .merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')
    .agg(
        total_orders=('order_id','count'),
        completed_orders=('is_cancelled', lambda x: (~x).sum()),
        cancelled_orders=('is_cancelled','sum'),
    )
    .assign(cancellation_rate_pct=lambda df: (df['cancelled_orders']/df['total_orders']*100).round(2))
    .assign(pct_of_total=lambda df: (df['total_orders']/df['total_orders'].sum()*100).round(2))
    .reset_index()
    .sort_values('total_orders', ascending=False)
)
results['Q01_Total_Orders_by_City'] = q01

# ── Q02: Revenue by City ─────────────────────────────────────────────────────
q02 = (completed
    .merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')
    .agg(
        total_orders=('order_id','count'),
        gross_order_value_inr=('order_value','sum'),
        total_discounts_inr=('discount','sum'),
        net_sales_inr=('final_amount','sum'),
        avg_order_value_inr=('order_value','mean')
    )
    .assign(discount_rate_pct=lambda df: (df['total_discounts_inr']/df['gross_order_value_inr']*100).round(2))
    .reset_index()
    .sort_values('net_sales_inr', ascending=False)
)
for c in ['gross_order_value_inr','total_discounts_inr','net_sales_inr','avg_order_value_inr']:
    q02[c] = q02[c].round(2)
results['Q02_Revenue_by_City'] = q02

# ── Q03: Top 20 Restaurants by Orders ────────────────────────────────────────
q03 = (completed
    .merge(restaurants, on='restaurant_id')
    .groupby(['restaurant_id','restaurant_name','cuisine','city','area'])
    .agg(completed_orders=('order_id','count'))
    .reset_index()
    .sort_values('completed_orders', ascending=False)
    .head(20)
    .assign(rank=lambda df: range(1, len(df)+1))
    [['rank','restaurant_id','restaurant_name','cuisine','city','area','completed_orders']]
)
results['Q03_Top_Restaurants_by_Orders'] = q03

# ── Q04: Top 20 Restaurants by Revenue ───────────────────────────────────────
q04 = (completed
    .merge(restaurants[['restaurant_id','restaurant_name','cuisine','city']], on='restaurant_id')
    .groupby(['restaurant_id','restaurant_name','cuisine','city'])
    .agg(
        total_orders=('order_id','count'),
        total_revenue_inr=('final_amount','sum'),
        avg_order_value_inr=('final_amount','mean')
    )
    .reset_index()
    .sort_values('total_revenue_inr', ascending=False)
    .head(20)
    .assign(revenue_rank=lambda df: range(1, len(df)+1))
)
q04['total_revenue_inr']   = q04['total_revenue_inr'].round(2)
q04['avg_order_value_inr'] = q04['avg_order_value_inr'].round(2)
results['Q04_Top_Restaurants_by_Revenue'] = q04[['revenue_rank','restaurant_id','restaurant_name','cuisine','city','total_orders','total_revenue_inr','avg_order_value_inr']]

# ── Q05: Restaurant Ranking by Customer Rating ───────────────────────────────
q05_base = (completed
    .merge(restaurants, on='restaurant_id')
    .merge(feedback[['order_id','rating']], on='order_id', how='left')
    .groupby(['restaurant_id','restaurant_name','cuisine','city','restaurant_rating'])
    .agg(
        total_reviews=('rating','count'),
        avg_customer_rating=('rating','mean'),
        five_star_count=('rating', lambda x: (x == 5).sum()),
        low_rating_count=('rating', lambda x: (x <= 2).sum())
    )
    .reset_index()
    .query('total_reviews >= 10')
    .assign(
        pct_5_star=lambda df: (df['five_star_count'] / df['total_reviews'] * 100).round(1),
        pct_low_rating=lambda df: (df['low_rating_count'] / df['total_reviews'] * 100).round(1)
    )
    .sort_values('avg_customer_rating', ascending=False)
    .head(20)
    .assign(rating_rank=lambda df: range(1, len(df)+1))
    .rename(columns={'restaurant_rating': 'platform_rating'})
)
q05_base['avg_customer_rating'] = q05_base['avg_customer_rating'].round(2)
results['Q05_Restaurant_Ranking_by_Rating'] = q05_base[['rating_rank','restaurant_id','restaurant_name','cuisine','city','platform_rating','total_reviews','avg_customer_rating','pct_5_star','pct_low_rating']]

# ── Q06: Complaint Rate by Restaurant ────────────────────────────────────────
q06_base = (completed
    .merge(restaurants, on='restaurant_id')
    .merge(feedback[['order_id','feedback_id','complaint_type']], on='order_id', how='left')
    .groupby(['restaurant_id','restaurant_name','city','cuisine'])
    .agg(
        total_feedback=('feedback_id','count'),
        total_complaints=('complaint_type', lambda x: x.notna().sum()),
        top_complaints=('complaint_type', lambda x: ", ".join(x.dropna().value_counts().head(3).index))
    )
    .reset_index()
    .query('total_complaints > 0')
    .assign(complaint_rate_pct=lambda df: (df['total_complaints'] / df['total_feedback'] * 100).round(2))
    .sort_values('complaint_rate_pct', ascending=False)
    .head(20)
)
results['Q06_Complaint_Rate_by_Restaurant'] = q06_base[['restaurant_id','restaurant_name','city','cuisine','total_feedback','total_complaints','complaint_rate_pct','top_complaints']]

# ── Q07: Average Delivery Time by City ───────────────────────────────────────
q07 = (deliveries
    .merge(orders[['order_id','restaurant_id']], on='order_id')
    .merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')
    .agg(
        total_deliveries=('delivery_id','count'),
        avg_delivery_time_min=('actual_delivery_minutes','mean'),
        min_delivery_time_min=('actual_delivery_minutes','min'),
        max_delivery_time_min=('actual_delivery_minutes','max'),
        avg_delay_min=('delay_minutes','mean'),
        avg_distance_km=('distance_km','mean'),
        on_time_deliveries=('on_time_status', lambda x: (x=='On Time').sum())
    )
    .assign(on_time_pct=lambda df: (df['on_time_deliveries']/df['total_deliveries']*100).round(2))
    .reset_index()
    .sort_values('avg_delivery_time_min')
)
for c in ['avg_delivery_time_min','min_delivery_time_min','max_delivery_time_min','avg_delay_min','avg_distance_km']:
    q07[c] = q07[c].round(2)
results['Q07_Avg_Delivery_by_City'] = q07

# ── Q08: Average Delivery Time by Area and Hour ──────────────────────────────
q08 = (deliveries
    .merge(orders[['order_id','restaurant_id','order_time']], on='order_id')
    .merge(restaurants[['restaurant_id','city','area']], on='restaurant_id')
    .assign(order_hour=lambda df: df['order_time'].dt.hour)
    .groupby(['city','area','order_hour'])
    .agg(
        total_deliveries=('delivery_id','count'),
        avg_delivery_time_min=('actual_delivery_minutes','mean'),
        avg_delay_min=('delay_minutes','mean'),
        delay_rate_pct=('on_time_status', lambda x: (x == 'Delayed').mean() * 100)
    )
    .reset_index()
    .query('total_deliveries >= 5')
    .sort_values('avg_delay_min', ascending=False)
    .head(50)
)
q08['avg_delivery_time_min'] = q08['avg_delivery_time_min'].round(1)
q08['avg_delay_min'] = q08['avg_delay_min'].round(1)
q08['delay_rate_pct'] = q08['delay_rate_pct'].round(1)
results['Q08_Delivery_by_Area_and_Hour'] = q08

# ── Q09: Identify Slow-Performing Delivery Areas ─────────────────────────────
q09_base = (deliveries
    .merge(orders[['order_id','restaurant_id']], on='order_id')
    .merge(restaurants[['restaurant_id','city','area']], on='restaurant_id')
    .groupby(['city','area'])
    .agg(
        total_deliveries=('delivery_id','count'),
        avg_delivery_time=('actual_delivery_minutes','mean'),
        avg_delay=('delay_minutes','mean'),
        delay_rate_pct=('on_time_status', lambda x: (x == 'Delayed').mean() * 100)
    )
    .reset_index()
    .query('total_deliveries >= 50')
)
city_avg = q09_base.groupby('city')['avg_delivery_time'].transform('mean')
q09_base['time_above_city_avg'] = (q09_base['avg_delivery_time'] - city_avg).round(1)
q09_base['area_delay_rank'] = q09_base.groupby('city')['delay_rate_pct'].rank(ascending=False, method='min').astype(int)
q09_base['avg_delivery_time'] = q09_base['avg_delivery_time'].round(1)
q09_base['avg_delay'] = q09_base['avg_delay'].round(1)
q09_base['delay_rate_pct'] = q09_base['delay_rate_pct'].round(2)
results['Q09_Slow_Delivery_Areas'] = q09_base.sort_values(['city','area_delay_rank'])

# ── Q10: Cancellation Rate by Restaurant ─────────────────────────────────────
q10 = (orders
    .merge(restaurants[['restaurant_id','restaurant_name','city','cuisine']], on='restaurant_id')
    .groupby(['restaurant_id','restaurant_name','city','cuisine'])
    .agg(
        total_orders=('order_id','count'),
        cancelled_orders=('is_cancelled','sum'),
        cancellation_rate_pct=('is_cancelled', lambda x: x.mean() * 100)
    )
    .reset_index()
    .query('total_orders >= 20')
    .sort_values('cancellation_rate_pct', ascending=False)
    .head(20)
    .assign(rank=lambda df: range(1, len(df)+1))
)
q10['cancellation_rate_pct'] = q10['cancellation_rate_pct'].round(2)
results['Q10_Cancellation_Rate_by_Restaurant'] = q10[['rank','restaurant_id','restaurant_name','city','cuisine','total_orders','cancelled_orders','cancellation_rate_pct']]

# ── Q11: Cancellation Reasons ────────────────────────────────────────────────
q11 = (orders[orders['is_cancelled'] & orders['cancellation_reason'].notna() & (orders['cancellation_reason']!='')]
    .groupby('cancellation_reason')
    .agg(
        total_cancellations=('order_id','count'),
        avg_order_value_inr=('order_value','mean')
    )
    .assign(pct_of_total=lambda df: (df['total_cancellations']/df['total_cancellations'].sum()*100).round(2))
    .reset_index()
    .sort_values('total_cancellations', ascending=False)
)
q11['avg_order_value_inr'] = q11['avg_order_value_inr'].round(2)
results['Q11_Cancellation_Reasons'] = q11[['cancellation_reason','total_cancellations','pct_of_total','avg_order_value_inr']]

# ── Q12: Repeat Customer Rate by City ────────────────────────────────────────
cust_orders = (orders
    .groupby('customer_id')
    .agg(order_count=('order_id','count'))
    .reset_index()
    .merge(customers[['customer_id','city']], on='customer_id')
)
q12 = (cust_orders
    .groupby('city')
    .agg(
        total_customers=('customer_id','count'),
        one_time_customers=('order_count', lambda x: (x==1).sum()),
        repeat_customers=('order_count', lambda x: (x>=2).sum()),
        loyal_customers_5plus=('order_count', lambda x: (x>=5).sum()),
        vip_customers_10plus=('order_count', lambda x: (x>=10).sum()),
        avg_orders_per_customer=('order_count','mean')
    )
    .assign(repeat_rate_pct=lambda df: (df['repeat_customers']/df['total_customers']*100).round(2))
    .reset_index()
    .sort_values('repeat_rate_pct', ascending=False)
)
q12['avg_orders_per_customer'] = q12['avg_orders_per_customer'].round(2)
results['Q12_Repeat_Customer_Rate'] = q12

# ── Q13: Repeat vs One-Time Customer Revenue Comparison ──────────────────────
cust_spend = (completed
    .groupby('customer_id')
    .agg(
        order_count=('order_id','count'),
        total_spend=('final_amount','sum'),
        avg_order_value=('final_amount','mean')
    )
    .reset_index()
)
cust_spend['customer_segment'] = np.where(
    cust_spend['order_count'] == 1, '1 - One-time Customer',
    np.where(cust_spend['order_count'] <= 3, '2-3 Orders',
    np.where(cust_spend['order_count'] <= 9, '4-9 Orders (Regular)',
    '10+ Orders (Loyal/VIP)'))
)
q13 = (cust_spend
    .groupby('customer_segment')
    .agg(
        customer_count=('customer_id','count'),
        segment_revenue_inr=('total_spend','sum'),
        avg_lifetime_value_inr=('total_spend','mean'),
        avg_order_value_inr=('avg_order_value','mean')
    )
    .reset_index()
    .assign(pct_of_total_revenue=lambda df: (df['segment_revenue_inr'] / df['segment_revenue_inr'].sum() * 100).round(2))
    .sort_values('customer_segment')
)
for c in ['segment_revenue_inr','avg_lifetime_value_inr','avg_order_value_inr']:
    q13[c] = q13[c].round(2)
results['Q13_Customer_Segment_Revenue'] = q13

# ── Q14: Delivery Time vs Customer Ratings ───────────────────────────────────
del_fb = (deliveries
    .merge(feedback[['order_id','rating']], on='order_id')
)
del_fb['delay_bucket'] = np.where(
    del_fb['delay_minutes'] <= 0, 'Early (<=0 min)',
    np.where(del_fb['delay_minutes'] <= 5, 'On Time (1-5 min)',
    np.where(del_fb['delay_minutes'] <= 15, 'Slight Delay (6-15 min)',
    np.where(del_fb['delay_minutes'] <= 30, 'Moderate Delay (16-30 min)',
    np.where(del_fb['delay_minutes'] <= 60, 'Significant Delay (31-60 min)',
    'Severe Delay (>60 min)'))))
)
q14 = (del_fb
    .groupby('delay_bucket')
    .agg(
        feedback_count=('rating','count'),
        avg_rating=('rating','mean'),
        avg_delay_min=('delay_minutes','mean'),
        high_ratings=('rating', lambda x: (x >= 4).sum()),
        low_ratings=('rating', lambda x: (x <= 2).sum())
    )
    .reset_index()
    .assign(
        pct_high_rating=lambda df: (df['high_ratings'] / df['feedback_count'] * 100).round(1),
        pct_low_rating=lambda df: (df['low_ratings'] / df['feedback_count'] * 100).round(1)
    )
    .sort_values('avg_delay_min')
)
q14['avg_rating'] = q14['avg_rating'].round(2)
q14['avg_delay_min'] = q14['avg_delay_min'].round(1)
results['Q14_Delivery_Time_vs_Ratings'] = q14

# ── Q15: Distance vs Delivery Delays ─────────────────────────────────────────
del_copy = deliveries.copy()
del_copy['distance_bucket'] = np.where(
    del_copy['distance_km'] <= 2, '0-2 km (Very Close)',
    np.where(del_copy['distance_km'] <= 5, '2-5 km (Close)',
    np.where(del_copy['distance_km'] <= 8, '5-8 km (Medium)',
    np.where(del_copy['distance_km'] <= 12, '8-12 km (Far)',
    '12+ km (Very Far)'))))
q15 = (del_copy
    .groupby('distance_bucket')
    .agg(
        total_deliveries=('delivery_id','count'),
        avg_delivery_time_min=('actual_delivery_minutes','mean'),
        avg_delay_min=('delay_minutes','mean'),
        delay_rate_pct=('on_time_status', lambda x: (x == 'Delayed').mean() * 100),
        avg_distance_km=('distance_km','mean')
    )
    .reset_index()
    .sort_values('avg_distance_km')
)
q15['avg_delivery_time_min'] = q15['avg_delivery_time_min'].round(1)
q15['avg_delay_min'] = q15['avg_delay_min'].round(1)
q15['delay_rate_pct'] = q15['delay_rate_pct'].round(2)
q15['avg_distance_km'] = q15['avg_distance_km'].round(2)
results['Q15_Distance_vs_Delays'] = q15

# ── Q16: Peak Ordering Hours Analysis ────────────────────────────────────────
q16 = (orders
    .groupby('order_hour')
    .agg(
        total_orders=('order_id','count'),
        cancelled_orders=('is_cancelled','sum'),
        avg_order_value_inr=('final_amount','mean'),
    )
    .assign(cancellation_rate_pct=lambda df: (df['cancelled_orders']/df['total_orders']*100).round(2))
    .assign(pct_of_daily_orders=lambda df: (df['total_orders']/df['total_orders'].sum()*100).round(2))
    .reset_index()
    .rename(columns={'order_hour':'hour_of_day'})
    .assign(time_segment=lambda df: df['hour_of_day'].apply(
        lambda h: 'Morning (6-11)' if 6<=h<=11 else
                 ('Lunch Peak (12-14)' if 12<=h<=14 else
                 ('Afternoon (15-17)' if 15<=h<=17 else
                 ('Dinner Peak (18-22)' if 18<=h<=22 else 'Late Night / Early Morning')))
    ))
    [['hour_of_day','time_segment','total_orders','cancelled_orders','cancellation_rate_pct','avg_order_value_inr','pct_of_daily_orders']]
)
q16['avg_order_value_inr'] = q16['avg_order_value_inr'].round(2)
results['Q16_Peak_Hours'] = q16

# ── Q17: Restaurants with Consistently Poor Performance ──────────────────────
rest_perf = (orders
    .merge(restaurants[['restaurant_id','restaurant_name','city','cuisine','avg_prep_time']], on='restaurant_id')
    .merge(feedback[['order_id','rating','complaint_type','refund_amount']], on='order_id', how='left')
    .merge(deliveries[['order_id','actual_delivery_minutes']], on='order_id', how='left')
    .groupby(['restaurant_id','restaurant_name','city','cuisine','avg_prep_time'])
    .agg(
        total_orders=('order_id','count'),
        avg_rating=('rating','mean'),
        cancel_rate_pct=('is_cancelled', lambda x: x.mean() * 100),
        complaint_rate_pct=('complaint_type', lambda x: x.notna().mean() * 100),
        avg_delivery_min=('actual_delivery_minutes','mean'),
        total_refunds_inr=('refund_amount','sum')
    )
    .reset_index()
    .query('total_orders >= 20')
)
rest_perf['poor_perf_flags'] = (
    (rest_perf['avg_rating'] < 3.0).astype(int) +
    (rest_perf['cancel_rate_pct'] > 15).astype(int) +
    (rest_perf['complaint_rate_pct'] > 20).astype(int)
)
q17 = (rest_perf[rest_perf['poor_perf_flags'] >= 1]
    .sort_values(['poor_perf_flags','avg_rating'], ascending=[False, True])
    .head(30)
    .assign(performance_status=lambda df: df['poor_perf_flags'].map({
        3: 'CRITICAL - All 3 flags',
        2: 'HIGH - 2 flags',
        1: 'MODERATE - 1 flag'
    }))
)
for c in ['avg_rating','cancel_rate_pct','complaint_rate_pct','avg_delivery_min','total_refunds_inr']:
    q17[c] = q17[c].round(2)
results['Q17_Poor_Performing_Restaurants'] = q17[['restaurant_id','restaurant_name','city','cuisine','total_orders','avg_rating','cancel_rate_pct','complaint_rate_pct','avg_delivery_min','total_refunds_inr','poor_perf_flags','performance_status']]

# ── Q18: Cuisine Performance ─────────────────────────────────────────────────
q18 = (orders
    .merge(restaurants[['restaurant_id','cuisine','avg_prep_time']], on='restaurant_id')
    .merge(feedback[['order_id','rating']], on='order_id', how='left')
    .groupby('cuisine')
    .agg(
        restaurant_count=('restaurant_id','nunique'),
        total_orders=('order_id','count'),
        completed_orders=('is_cancelled', lambda x: (~x).sum()),
        total_revenue_inr=('final_amount', lambda x: x[~orders.loc[x.index,'is_cancelled']].sum()),
        avg_order_value_inr=('final_amount', lambda x: x[~orders.loc[x.index,'is_cancelled']].mean()),
        avg_customer_rating=('rating','mean'),
        avg_prep_time_min=('avg_prep_time','mean'),
        cancellation_rate_pct=('is_cancelled', lambda x: x.mean()*100)
    )
    .reset_index()
    .sort_values('total_revenue_inr', ascending=False)
)
for c in ['total_revenue_inr','avg_order_value_inr','avg_customer_rating','avg_prep_time_min','cancellation_rate_pct']:
    q18[c] = q18[c].round(2)
results['Q18_Cuisine_Performance'] = q18

# ── Q19: Refund Analysis by City ─────────────────────────────────────────────
q19 = (feedback
    .merge(orders[['order_id','restaurant_id']], on='order_id')
    .merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')
    .agg(
        feedback_count=('feedback_id','count'),
        refund_issued_count=('refund_amount', lambda x: (x > 0).sum()),
        total_refund_inr=('refund_amount','sum'),
        avg_refund_when_issued_inr=('refund_amount', lambda x: x[x > 0].mean() if (x > 0).sum() > 0 else 0)
    )
    .assign(refund_rate_pct=lambda df: (df['refund_issued_count'] / df['feedback_count'] * 100).round(2))
    .reset_index()
    .sort_values('total_refund_inr', ascending=False)
)
for c in ['total_refund_inr','avg_refund_when_issued_inr']:
    q19[c] = q19[c].round(2)
results['Q19_Refunds_by_City'] = q19

# ── Q20: Restaurant Performance Report (top 100) ─────────────────────────────
q20 = (orders
    .merge(restaurants, on='restaurant_id')
    .merge(deliveries[['order_id','actual_delivery_minutes','on_time_status']], on='order_id', how='left')
    .merge(feedback[['order_id','rating','complaint_type','refund_amount']], on='order_id', how='left')
    .groupby(['restaurant_id','restaurant_name','cuisine','city','area'])
    .agg(
        total_orders=('order_id','count'),
        completed_orders=('is_cancelled', lambda x: (~x).sum()),
        cancel_rate_pct=('is_cancelled', lambda x: x.mean()*100),
        total_revenue_inr=('final_amount', lambda x: x[~orders.loc[x.index,'is_cancelled']].sum() if len(x) else 0),
        avg_del_min=('actual_delivery_minutes','mean'),
        on_time_pct=('on_time_status', lambda x: (x=='On Time').mean()*100),
        avg_rating=('rating','mean'),
        complaint_rate_pct=('complaint_type', lambda x: x.notna().mean()*100),
        total_refund_inr=('refund_amount','sum')
    )
    .reset_index()
    .query('total_orders >= 10')
    .sort_values('total_revenue_inr', ascending=False)
    .head(100)
)
for c in ['cancel_rate_pct','avg_del_min','on_time_pct','avg_rating','complaint_rate_pct']:
    q20[c] = q20[c].round(2)
q20['total_revenue_inr'] = q20['total_revenue_inr'].round(2)
q20['total_refund_inr']  = q20['total_refund_inr'].round(2)
q20['performance_tier']  = np.where(
    (q20['avg_rating'] >= 4.0) & (q20['cancel_rate_pct'] < 10) & (q20['on_time_pct'] > 80),
    'TOP PERFORMER',
    np.where(
        (q20['avg_rating'] < 3.0) | (q20['cancel_rate_pct'] > 20) | (q20['complaint_rate_pct'] > 25),
        'NEEDS ATTENTION',
        'AVERAGE'
    )
)
results['Q20_Restaurant_Performance_Report'] = q20

# ── SAVE ALL SQL RESULTS CSVs ────────────────────────────────────────────────
print("\nSaving all 20 SQL query results CSVs...")
for name, df in results.items():
    path = os.path.join(SQL_DIR, f"05_{name}.csv")
    df.to_csv(path, index=False)
    print(f"  Saved 05_{name}.csv: {len(df):>4d} rows")

# ── GENERATE COMPREHENSIVE SQL RESULTS SUMMARY MD ────────────────────────────
print("\nGenerating comprehensive SQL results summary markdown...")
md_lines = [
    "# SQL Query Results Summary (All 20 Queries)",
    "## QuickBite Analytics | Team: Data Knights | CODEGNAN DA-07",
    "",
    "> Complete empirical results for all 20 analytical queries defined in `sql/04_analysis_queries.sql`.",
    "> Executed against the full 100,000-order QuickBite canonical dataset.",
    "",
]

for name, df in results.items():
    q_num = name.split('_')[0]
    q_title = name.replace(q_num+'_','').replace('_',' ')
    md_lines.append(f"## {q_num}: {q_title}")
    md_lines.append(f"*(Result count: {len(df):,} rows)*\n")
    # For large tables, show head(25) in markdown
    display_df = df.head(25) if len(df) > 25 else df
    md_lines.append(display_df.to_markdown(index=False) if hasattr(display_df, 'to_markdown') else display_df.to_string(index=False))
    if len(df) > 25:
        md_lines.append(f"\n*... showing top 25 of {len(df):,} rows. Full data in `sql/05_{name}.csv`.*")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

with open(os.path.join(SQL_DIR, '05_sql_results_summary.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print("SQL Results Summary written successfully to sql/05_sql_results_summary.md")
