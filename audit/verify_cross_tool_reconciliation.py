import os, sys
import pandas as pd
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

print("=== CROSS-TOOL RECONCILIATION: PYTHON vs SQL vs EXCEL ===")

# 1. Load Canonical Clean Data
orders = pd.read_csv("quickbite-analytics/data/cleaned/orders_cleaned.csv")
restaurants = pd.read_csv("quickbite-analytics/data/cleaned/restaurants_cleaned.csv")
deliveries = pd.read_csv("quickbite-analytics/data/cleaned/deliveries_cleaned.csv")

# Python calculations
py_city_orders = orders.merge(restaurants[['restaurant_id','city']], on='restaurant_id').groupby('city').size().to_dict()
py_city_completed = orders[orders['order_status'].isin(['Completed','Partially Delivered'])].merge(restaurants[['restaurant_id','city']], on='restaurant_id').groupby('city').size().to_dict()
py_city_revenue = orders[orders['order_status'].isin(['Completed','Partially Delivered'])].merge(restaurants[['restaurant_id','city']], on='restaurant_id').groupby('city')['final_amount'].sum().round(2).to_dict()

# SQL outputs
sql_q01 = pd.read_csv("quickbite-analytics/sql/05_Q01_Total_Orders_by_City.csv").set_index('city')
sql_q02 = pd.read_csv("quickbite-analytics/sql/05_Q02_Revenue_by_City.csv").set_index('city')

# Excel outputs
wb = openpyxl.load_workbook("quickbite-analytics/excel/QuickBite_Excel_Analysis.xlsx", data_only=True)
ws_city = wb['City Performance']

# In City Performance sheet:
# Let's inspect where city totals are stored
excel_city_data = {}
for r in range(4, 10):
    city_name = ws_city.cell(r, 1).value
    if city_name in ['Hyderabad', 'Visakhapatnam', 'Vijayawada']:
        excel_city_data[city_name] = {
            'orders': ws_city.cell(r, 2).value,
            'completed': ws_city.cell(r, 3).value,
            'revenue': ws_city.cell(r, 5).value,
        }

print("\n--- 1. CITY ORDER VOLUME RECONCILIATION ---")
print(f"{'City':15s} | {'Python Orders':14s} | {'SQL Orders':12s} | {'Excel Orders':12s} | {'Status':8s}")
print("-" * 70)
for city in sorted(py_city_orders.keys()):
    po = py_city_orders[city]
    so = int(sql_q01.loc[city, 'total_orders'])
    eo = int(excel_city_data[city]['orders']) if city in excel_city_data else None
    status = "EXACT" if (po == so == eo) else "MISMATCH"
    print(f"{city:15s} | {po:14,d} | {so:12,d} | {eo:12,d} | {status:8s}")

print("\n--- 2. CITY COMPLETED ORDERS RECONCILIATION ---")
print(f"{'City':15s} | {'Python Completed':16s} | {'SQL Completed':14s} | {'Excel Completed':15s} | {'Status':8s}")
print("-" * 75)
for city in sorted(py_city_completed.keys()):
    pc = py_city_completed[city]
    sc = int(sql_q01.loc[city, 'completed_orders'])
    ec = int(excel_city_data[city]['completed']) if city in excel_city_data else None
    status = "EXACT" if (pc == sc == ec) else "MISMATCH"
    print(f"{city:15s} | {pc:16,d} | {sc:14,d} | {ec:15,d} | {status:8s}")

print("\n--- 3. CITY NET REVENUE RECONCILIATION (INR) ---")
print(f"{'City':15s} | {'Python Revenue':14s} | {'SQL Revenue':12s} | {'Excel Revenue':14s} | {'Status':8s}")
print("-" * 70)
for city in sorted(py_city_revenue.keys()):
    pr = py_city_revenue[city]
    sr = float(sql_q02.loc[city, 'net_sales_inr'])
    er = float(excel_city_data[city]['revenue']) if city in excel_city_data else None
    diff = abs(pr - sr)
    status = "EXACT" if (diff < 0.05 and abs(pr - er) < 0.05) else "MISMATCH"
    print(f"{city:15s} | ₹{pr:13,.2f} | ₹{sr:11,.2f} | ₹{er:13,.2f} | {status:8s}")

# 4. Hourly Reconciliation
print("\n--- 4. HOURLY ORDERS RECONCILIATION ---")
sql_q16 = pd.read_csv("quickbite-analytics/sql/05_Q16_Peak_Hours.csv").set_index('hour_of_day')
py_hour_orders = orders.groupby('order_hour').size().to_dict()
ws_hour = wb['Hourly Analysis']
excel_hour_orders = {}
for r in range(4, 28):
    h = ws_hour.cell(r, 1).value
    if h is not None and isinstance(h, int):
        excel_hour_orders[h] = ws_hour.cell(r, 2).value

hourly_match = all(py_hour_orders[h] == int(sql_q16.loc[h, 'total_orders']) == int(excel_hour_orders[h]) for h in range(24))
print(f"All 24 hours reconcile across Python, SQL, and Excel: {hourly_match}")

# 5. Core 7 KPIs Reconciled
print("\n--- 5. CORE 7 KPI CONTRACT VALUES (GLOBAL) ---")
kpi_total_orders = len(orders)
kpi_gov = orders[orders['order_status'].isin(['Completed','Partially Delivered'])]['order_value'].sum()
kpi_net_sales = orders[orders['order_status'].isin(['Completed','Partially Delivered'])]['final_amount'].sum()
kpi_avg_del_time = deliveries['actual_delivery_minutes'].mean()
kpi_on_time_pct = (deliveries['on_time_status'] == 'On Time').mean() * 100
kpi_cancel_pct = orders['order_status'].isin(['Cancelled','Refunded']).mean() * 100
feedback = pd.read_csv("quickbite-analytics/data/cleaned/feedback_cleaned.csv")
kpi_avg_rating = feedback['rating'].mean()
customers = pd.read_csv("quickbite-analytics/data/cleaned/customers_cleaned.csv")
kpi_repeat_rate = (customers['order_count'] >= 2).mean() * 100

print(f"1. Total Orders         : {kpi_total_orders:,}")
print(f"2. Gross Order Value    : ₹{kpi_gov:,.2f} (Net Sales: ₹{kpi_net_sales:,.2f})")
print(f"3. Avg Delivery Time    : {kpi_avg_del_time:.2f} minutes")
print(f"4. On-Time Delivery %   : {kpi_on_time_pct:.2f}%")
print(f"5. Cancellation Rate %  : {kpi_cancel_pct:.2f}%")
print(f"6. Avg Customer Rating  : {kpi_avg_rating:.2f} / 5.0")
print(f"7. Repeat Order Rate %  : {kpi_repeat_rate:.2f}%")
