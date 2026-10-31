"""
QuickBite Analytics – Excel Workbook Generator
===============================================
Team: Data Knights | CODEGNAN DA-07
Generates: excel/QuickBite_Excel_Analysis.xlsx

Uses openpyxl to create a fully formatted Excel workbook with:
- Summary dashboard
- City, restaurant, cuisine, hourly, cancellation, retention analysis
- Pivot-ready tables and charts
"""

import pandas as pd
import numpy as np
import os
from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')
RAW_DIR     = os.path.join(BASE_DIR, 'data', 'raw')
EXCEL_DIR   = os.path.join(BASE_DIR, 'excel')
OUT_PATH    = os.path.join(EXCEL_DIR, 'QuickBite_Excel_Analysis.xlsx')

# Load the cleaned (or raw) data
def load(fname, folder=None):
    folder = folder or CLEANED_DIR
    path = os.path.join(folder, fname)
    if not os.path.exists(path):
        path = os.path.join(RAW_DIR, fname.replace('_cleaned',''))
    return pd.read_csv(path, low_memory=False)

print("Loading datasets...")
orders      = load('orders_cleaned.csv')
restaurants = load('restaurants_cleaned.csv')
deliveries  = load('deliveries_cleaned.csv')
customers   = load('customers_cleaned.csv')
feedback    = load('feedback_cleaned.csv')
riders      = load('riders_cleaned.csv')

orders['order_time']      = pd.to_datetime(orders['order_time'])
deliveries['pickup_time'] = pd.to_datetime(deliveries['pickup_time'])
orders['order_hour']      = orders['order_time'].dt.hour
orders['order_month']     = orders['order_time'].dt.month
orders['order_date']      = orders['order_time'].dt.date
orders['is_cancelled']    = orders['order_status'].isin(['Cancelled','Refunded'])
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ── Colour palette ────────────────────────────────────────────────────────────
GOOGLE_BLUE   = "1A73E8"
GOOGLE_GREEN  = "34A853"
GOOGLE_YELLOW = "FBBC04"
GOOGLE_RED    = "EA4335"
DARK_GREY     = "3C4043"
LIGHT_GREY    = "F1F3F4"
WHITE         = "FFFFFF"
HEADER_FILL   = PatternFill("solid", fgColor=GOOGLE_BLUE)
SUBHEADER_FILL= PatternFill("solid", fgColor=DARK_GREY)
HIGHLIGHT_FILL= PatternFill("solid", fgColor=GOOGLE_YELLOW)
ALT_FILL      = PatternFill("solid", fgColor=LIGHT_GREY)
GREEN_FILL    = PatternFill("solid", fgColor="E6F4EA")
RED_FILL      = PatternFill("solid", fgColor="FCE8E6")

HEADER_FONT   = Font(name='Calibri', bold=True, color=WHITE, size=11)
SUBHEADER_FONT= Font(name='Calibri', bold=True, color=WHITE, size=10)
TITLE_FONT    = Font(name='Calibri', bold=True, color=DARK_GREY, size=14)
DATA_FONT     = Font(name='Calibri', size=10)
BOLD_FONT     = Font(name='Calibri', bold=True, size=10)

THIN_BORDER   = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

def style_header(ws, row, cols, fill=None, font=None, height=22):
    fill = fill or HEADER_FILL
    font = font or HEADER_FONT
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[row].height = height

def write_df(ws, df, start_row=1, start_col=1, header=True,
             header_fill=None, alt_rows=True, formats=None):
    """Write a DataFrame to a worksheet with formatting."""
    formats = formats or {}
    header_fill = header_fill or HEADER_FILL
    r = start_row
    if header:
        for j, col_name in enumerate(df.columns, start=start_col):
            cell = ws.cell(row=r, column=j, value=str(col_name).replace('_',' ').title())
            cell.fill = header_fill
            cell.font = HEADER_FONT
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = THIN_BORDER
        r += 1

    for i, (_, row) in enumerate(df.iterrows()):
        fill = ALT_FILL if (alt_rows and i % 2 == 1) else PatternFill()
        for j, (col, val) in enumerate(row.items(), start=start_col):
            cell = ws.cell(row=r, column=j, value=val)
            cell.font = DATA_FONT
            cell.fill = fill
            cell.border = THIN_BORDER
            cell.alignment = Alignment(horizontal='center', vertical='center')
            if col in formats:
                cell.number_format = formats[col]
        r += 1
    return r

def set_col_widths(ws, widths_dict):
    for col_letter, width in widths_dict.items():
        ws.column_dimensions[col_letter].width = width

def add_section_title(ws, row, text, col_span=10, fill_color=DARK_GREY):
    ws.merge_cells(start_row=row, start_column=1,
                   end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = PatternFill("solid", fgColor=fill_color)
    cell.font = Font(name='Calibri', bold=True, color=WHITE, size=12)
    cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws.row_dimensions[row].height = 20

wb = Workbook()

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 1: Executive Summary...")
ws = wb.active
ws.title = "Executive Summary"

# Title
ws.merge_cells("A1:J1")
ws["A1"] = "QuickBite – Restaurant & Delivery Performance Analytics"
ws["A1"].font = Font(name='Calibri', bold=True, size=18, color=GOOGLE_BLUE)
ws["A1"].alignment = Alignment(horizontal='center', vertical='center')
ws.row_dimensions[1].height = 35

ws.merge_cells("A2:J2")
ws["A2"] = "CODEGNAN Hackathon DA-07 | Team: Data Knights | Synthetic Data – For Demonstration Only"
ws["A2"].font = Font(name='Calibri', italic=True, size=10, color="5F6368")
ws["A2"].alignment = Alignment(horizontal='center')

# KPI Section
completed_mask = orders['order_status'].isin(['Completed', 'Partially Delivered'])
completed_orders = orders[completed_mask]

kpi_data = [
    ("Total Orders",             len(orders),                                "#"),
    ("Completed Orders",         completed_mask.sum(),                        "#"),
    ("Gross Revenue (INR)",      completed_orders['order_value'].sum(),       "INR"),
    ("Net Revenue (INR)",        completed_orders['final_amount'].sum(),      "INR"),
    ("Cancellation Rate",        orders['is_cancelled'].mean() * 100,        "%"),
    ("Avg Delivery Time",        deliveries['actual_delivery_minutes'].mean(), "min"),
    ("On-Time Delivery Rate",    (deliveries['on_time_status']=='On Time').mean()*100, "%"),
    ("Avg Customer Rating",      feedback['rating'].mean(),                   "/ 5.0"),
    ("Repeat Customer Rate",     (customers['total_orders'] >= 2).mean()*100, "%"),
    ("Total Refunds (INR)",      feedback['refund_amount'].sum(),             "INR"),
]

ws["A4"] = "KEY PERFORMANCE INDICATORS"
ws["A4"].font = Font(name='Calibri', bold=True, size=12, color=DARK_GREY)
ws.row_dimensions[4].height = 20

kpi_fills = [
    PatternFill("solid", fgColor="E8F0FE"),  # light blue
    PatternFill("solid", fgColor="E6F4EA"),  # light green
    PatternFill("solid", fgColor="FEF7E0"),  # light yellow
    PatternFill("solid", fgColor="E6F4EA"),
    PatternFill("solid", fgColor="FCE8E6"),  # light red
    PatternFill("solid", fgColor="E8F0FE"),
    PatternFill("solid", fgColor="E6F4EA"),
    PatternFill("solid", fgColor="FEF7E0"),
    PatternFill("solid", fgColor="E6F4EA"),
    PatternFill("solid", fgColor="FCE8E6"),
]

r = 5
for i, ((label, value, unit), fill) in enumerate(zip(kpi_data, kpi_fills)):
    col = (i % 5) * 2 + 1
    if i == 5: r += 4

    label_cell = ws.cell(row=r, column=col, value=label)
    label_cell.font = Font(name='Calibri', bold=True, size=9, color="5F6368")
    label_cell.fill = fill
    label_cell.alignment = Alignment(horizontal='center', vertical='center')
    label_cell.border = THIN_BORDER
    ws.merge_cells(start_row=r, start_column=col, end_row=r, end_column=col+1)
    ws.row_dimensions[r].height = 16

    # Format value
    if unit == "INR":
        disp = f"₹{value:,.0f}"
    elif unit == "%":
        disp = f"{value:.2f}%"
    elif unit == "min":
        disp = f"{value:.1f} min"
    elif unit == "/ 5.0":
        disp = f"{value:.2f} ⭐"
    else:
        disp = f"{value:,}"

    val_cell = ws.cell(row=r+1, column=col, value=disp)
    val_cell.font = Font(name='Calibri', bold=True, size=14, color=GOOGLE_BLUE)
    val_cell.fill = fill
    val_cell.alignment = Alignment(horizontal='center', vertical='center')
    val_cell.border = THIN_BORDER
    ws.merge_cells(start_row=r+1, start_column=col, end_row=r+1, end_column=col+1)
    ws.row_dimensions[r+1].height = 24

# City Summary Table
city_summary = (orders.merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')
    .agg(total_orders=('order_id','count'),
         completed=('is_cancelled', lambda x: (~x).sum()),
         cancelled=('is_cancelled','sum'))
    .reset_index()
)
city_summary['cancel_rate_%'] = (city_summary['cancelled'] / city_summary['total_orders'] * 100).round(2)

# Net revenue per city
city_rev = (completed_orders.merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby('city')['final_amount'].sum().reset_index())
city_rev.columns = ['city', 'net_revenue_inr']
city_summary = city_summary.merge(city_rev, on='city')
city_summary = city_summary.sort_values('total_orders', ascending=False)

add_section_title(ws, 14, "CITY PERFORMANCE SUMMARY", col_span=8)
write_df(ws, city_summary, start_row=15, formats={
    'net_revenue_inr': '#,##0.00', 'cancel_rate_%': '0.00"%"'
})
set_col_widths(ws, {'A':22,'B':16,'C':16,'D':14,'E':16,'F':18,'G':14,'H':14,'I':14,'J':14})

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2: CITY PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 2: City Performance...")
ws2 = wb.create_sheet("City Performance")

ws2.merge_cells("A1:H1")
ws2["A1"] = "City-wise Performance Analysis"
ws2["A1"].font = TITLE_FONT
ws2["A1"].alignment = Alignment(horizontal='center')
ws2.row_dimensions[1].height = 28

# Hourly by city
hourly_city = (orders.merge(restaurants[['restaurant_id','city']], on='restaurant_id')
    .groupby(['city','order_hour'])
    .agg(orders=('order_id','count'), cancellations=('is_cancelled','sum'))
    .reset_index()
)
hourly_city['cancel_rate_%'] = (hourly_city['cancellations'] / hourly_city['orders'] * 100).round(2)

add_section_title(ws2, 3, "HOURLY ORDER DISTRIBUTION BY CITY", col_span=8)
write_df(ws2, hourly_city, start_row=4)
set_col_widths(ws2, {get_column_letter(i): 18 for i in range(1,9)})

# Area performance
area_perf = (orders.merge(restaurants[['restaurant_id','area','city']], on='restaurant_id')
    .merge(deliveries[['order_id','actual_delivery_minutes','on_time_status']], on='order_id', how='left')
    .groupby(['city','area'])
    .agg(orders=('order_id','count'),
         avg_delivery_min=('actual_delivery_minutes','mean'),
         on_time_pct=('on_time_status', lambda x: (x=='On Time').mean()*100))
    .reset_index()
    .sort_values(['city','orders'], ascending=[True,False])
)
area_perf['avg_delivery_min'] = area_perf['avg_delivery_min'].round(1)
area_perf['on_time_pct'] = area_perf['on_time_pct'].round(2)

row_after_hourly = 4 + len(hourly_city) + 3
add_section_title(ws2, row_after_hourly, "AREA-WISE PERFORMANCE", col_span=8)
write_df(ws2, area_perf, start_row=row_after_hourly+1)

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 3: RESTAURANT PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 3: Restaurant Performance...")
ws3 = wb.create_sheet("Restaurant Performance")

ws3.merge_cells("A1:J1")
ws3["A1"] = "Restaurant Performance Report"
ws3["A1"].font = TITLE_FONT
ws3["A1"].alignment = Alignment(horizontal='center')
ws3.row_dimensions[1].height = 28

rest_perf = (orders
    .merge(restaurants, on='restaurant_id')
    .merge(deliveries[['order_id','actual_delivery_minutes','on_time_status']],
           on='order_id', how='left')
    .merge(feedback[['order_id','rating','refund_amount','complaint_type']],
           on='order_id', how='left')
    .groupby(['restaurant_id','restaurant_name','cuisine','city','area'])
    .agg(
        total_orders=('order_id','count'),
        completed=('is_cancelled', lambda x: (~x).sum()),
        cancel_rate_pct=('is_cancelled', lambda x: x.mean()*100),
        net_revenue=('final_amount',lambda x: x[~x.isna()].sum()),
        avg_del_min=('actual_delivery_minutes','mean'),
        on_time_pct=('on_time_status', lambda x: (x=='On Time').mean()*100),
        avg_rating=('rating','mean'),
        total_refund=('refund_amount','sum')
    )
    .reset_index()
    .query('total_orders >= 10')
    .sort_values('net_revenue', ascending=False)
    .head(50)
)
for col in ['cancel_rate_pct','avg_del_min','on_time_pct','avg_rating']:
    rest_perf[col] = rest_perf[col].round(2)
rest_perf['net_revenue'] = rest_perf['net_revenue'].round(2)

add_section_title(ws3, 3, "TOP 50 RESTAURANTS BY REVENUE", col_span=10)
last_row = write_df(ws3, rest_perf, start_row=4, formats={
    'net_revenue': '#,##0.00',
    'cancel_rate_pct': '0.00',
    'avg_rating': '0.00',
    'on_time_pct': '0.00',
})

# Conditional formatting: rating column
rating_col_idx = list(rest_perf.columns).index('avg_rating') + 1
rating_col     = get_column_letter(rating_col_idx)
ws3.conditional_formatting.add(
    f"{rating_col}5:{rating_col}{last_row-1}",
    ColorScaleRule(
        start_type='min', start_color='FCE8E6',
        mid_type='percentile', mid_value=50, mid_color='FEF7E0',
        end_type='max', end_color='E6F4EA'
    )
)
for i in range(1, 11):
    ws3.column_dimensions[get_column_letter(i)].width = 18

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 4: CUISINE PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 4: Cuisine Performance...")
ws4 = wb.create_sheet("Cuisine Performance")

cuisine_perf = (orders
    .merge(restaurants[['restaurant_id','cuisine']], on='restaurant_id')
    .merge(feedback[['order_id','rating']], on='order_id', how='left')
    .groupby('cuisine')
    .agg(
        total_orders=('order_id','count'),
        completed=('is_cancelled', lambda x: (~x).sum()),
        cancel_rate_pct=('is_cancelled', lambda x: x.mean()*100),
        gross_revenue=('order_value', lambda x: x[~orders.loc[x.index,'is_cancelled']].sum() if len(x) else 0),
        avg_order_value=('final_amount','mean'),
        avg_rating=('rating','mean')
    )
    .reset_index()
    .sort_values('total_orders', ascending=False)
)
cuisine_perf = cuisine_perf.round(2)

ws4.merge_cells("A1:G1")
ws4["A1"] = "Cuisine Performance Analysis"
ws4["A1"].font = TITLE_FONT
ws4["A1"].alignment = Alignment(horizontal='center')
ws4.row_dimensions[1].height = 28

add_section_title(ws4, 3, "CUISINE-WISE METRICS", col_span=7)
write_df(ws4, cuisine_perf, start_row=4)
for i in range(1, 8):
    ws4.column_dimensions[get_column_letter(i)].width = 20

# Add chart
chart = BarChart()
chart.type = "col"
chart.title = "Orders by Cuisine"
chart.y_axis.title = "Total Orders"
chart.x_axis.title = "Cuisine"
data_ref = Reference(ws4, min_col=2, min_row=4, max_row=4+len(cuisine_perf))
cats_ref  = Reference(ws4, min_col=1, min_row=5, max_row=4+len(cuisine_perf))
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
chart.width = 22; chart.height = 14
ws4.add_chart(chart, "I3")

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 5: HOURLY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 5: Hourly Analysis...")
ws5 = wb.create_sheet("Hourly Analysis")

hourly = (orders
    .merge(deliveries[['order_id','actual_delivery_minutes','delay_minutes']], on='order_id', how='left')
    .groupby('order_hour')
    .agg(
        total_orders=('order_id','count'),
        cancellations=('is_cancelled','sum'),
        cancel_rate_pct=('is_cancelled', lambda x: x.mean()*100),
        avg_del_min=('actual_delivery_minutes','mean'),
        avg_delay_min=('delay_minutes','mean'),
        avg_order_value=('final_amount','mean')
    )
    .reset_index()
    .rename(columns={'order_hour':'hour_of_day'})
)
hourly = hourly.round(2)

ws5.merge_cells("A1:G1")
ws5["A1"] = "Hourly Order Analysis"
ws5["A1"].font = TITLE_FONT
ws5["A1"].alignment = Alignment(horizontal='center')
ws5.row_dimensions[1].height = 28

add_section_title(ws5, 3, "ORDERS AND DELIVERY PERFORMANCE BY HOUR (24H)", col_span=7)
write_df(ws5, hourly, start_row=4)

# Highlight peak hours
for row_idx in range(5, 5 + len(hourly)):
    hour_val = ws5.cell(row=row_idx, column=1).value
    if hour_val in [12, 13, 14, 19, 20, 21, 22]:
        for col in range(1, 8):
            ws5.cell(row=row_idx, column=col).fill = PatternFill("solid", fgColor="FEF7E0")

# Line chart
chart2 = LineChart()
chart2.title = "Order Volume by Hour"
chart2.y_axis.title = "Total Orders"
chart2.x_axis.title = "Hour of Day"
data_ref2 = Reference(ws5, min_col=2, min_row=4, max_row=4+len(hourly))
chart2.add_data(data_ref2, titles_from_data=True)
chart2.width = 22; chart2.height = 12
ws5.add_chart(chart2, "I3")
for i in range(1, 8):
    ws5.column_dimensions[get_column_letter(i)].width = 20

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 6: CANCELLATION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 6: Cancellation Analysis...")
ws6 = wb.create_sheet("Cancellation Analysis")

ws6.merge_cells("A1:H1")
ws6["A1"] = "Cancellation Analysis"
ws6["A1"].font = TITLE_FONT
ws6["A1"].alignment = Alignment(horizontal='center')
ws6.row_dimensions[1].height = 28

# Cancellation reasons
cancel_reasons = (orders[orders['is_cancelled'] & orders['cancellation_reason'].notna()
                          & (orders['cancellation_reason'] != '')]
    .groupby('cancellation_reason')
    .agg(count=('order_id','count'))
    .reset_index()
    .sort_values('count', ascending=False)
)
cancel_reasons['pct_of_cancellations'] = (cancel_reasons['count'] / cancel_reasons['count'].sum() * 100).round(2)

add_section_title(ws6, 3, "CANCELLATION REASONS", col_span=4)
write_df(ws6, cancel_reasons, start_row=4)

# Top cancelled restaurants
top_cancel_rest = (orders
    .merge(restaurants[['restaurant_id','restaurant_name','city','cuisine']], on='restaurant_id')
    .groupby(['restaurant_id','restaurant_name','city','cuisine'])
    .agg(total=('order_id','count'), cancelled=('is_cancelled','sum'))
    .reset_index()
    .query('total >= 20')
    .assign(cancel_rate_pct=lambda df: (df['cancelled']/df['total']*100).round(2))
    .sort_values('cancel_rate_pct', ascending=False)
    .head(20)
)
next_row = 4 + len(cancel_reasons) + 3
add_section_title(ws6, next_row, "TOP 20 RESTAURANTS BY CANCELLATION RATE", col_span=8)
write_df(ws6, top_cancel_rest, start_row=next_row+1)
for i in range(1, 9):
    ws6.column_dimensions[get_column_letter(i)].width = 22

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 7: CUSTOMER RETENTION
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 7: Customer Retention Analysis...")
ws7 = wb.create_sheet("Customer Retention")

ws7.merge_cells("A1:G1")
ws7["A1"] = "Customer Retention & Segmentation Analysis"
ws7["A1"].font = TITLE_FONT
ws7["A1"].alignment = Alignment(horizontal='center')
ws7.row_dimensions[1].height = 28

cust_segments = (customers
    .assign(segment=pd.cut(
        customers['total_orders'],
        bins=[-1, 0, 1, 3, 9, 999],
        labels=['No Orders','One-Time','2-3 Orders','4-9 Orders','10+ Orders (Loyal)']
    ))
    .groupby('segment')
    .agg(customer_count=('customer_id','count'))
    .reset_index()
)
cust_segments['pct_of_customers'] = (cust_segments['customer_count'] / len(customers) * 100).round(2)

add_section_title(ws7, 3, "CUSTOMER SEGMENTATION", col_span=4)
write_df(ws7, cust_segments, start_row=4)

# City retention
city_retention = (customers
    .assign(is_repeat=customers['total_orders'] >= 2)
    .groupby('city')
    .agg(total_customers=('customer_id','count'),
         repeat_customers=('is_repeat','sum'),
         avg_orders=('total_orders','mean'))
    .reset_index()
    .assign(repeat_rate_pct=lambda df: (df['repeat_customers']/df['total_customers']*100).round(2))
)
city_retention['avg_orders'] = city_retention['avg_orders'].round(2)

next_row2 = 4 + len(cust_segments) + 3
add_section_title(ws7, next_row2, "RETENTION BY CITY", col_span=6)
write_df(ws7, city_retention, start_row=next_row2+1)
for i in range(1, 8):
    ws7.column_dimensions[get_column_letter(i)].width = 22

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 8: DATA SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 8: Data Summary...")
ws8 = wb.create_sheet("Data Summary")

ws8.merge_cells("A1:D1")
ws8["A1"] = "Dataset Summary and Data Quality Report"
ws8["A1"].font = TITLE_FONT
ws8["A1"].alignment = Alignment(horizontal='center')
ws8.row_dimensions[1].height = 28

summary_data = [
    ("Dataset",        "Total Rows", "Key Fields",  "Notes"),
    ("orders.csv",     f"{len(orders):,}", "order_id, customer_id, restaurant_id", "100K orders, 2024"),
    ("restaurants.csv",f"{len(restaurants):,}", "restaurant_id, cuisine, city",    "4K restaurants"),
    ("deliveries.csv", f"{len(deliveries):,}", "delivery_id, order_id, rider_id",  "Non-cancelled only"),
    ("customers.csv",  f"{len(customers):,}", "customer_id, city, total_orders",   "20K customers"),
    ("feedback.csv",   f"{len(feedback):,}", "feedback_id, rating, complaint_type","~80% of completed"),
    ("riders.csv",     f"{len(riders):,}", "rider_id, rider_city, status",         "2K riders"),
]
for row_data in summary_data:
    ws8.append(row_data)
style_header(ws8, 3, 4)
for i in range(1, 5):
    ws8.column_dimensions[get_column_letter(i)].width = 28

# Data quality metrics
dq_data = [
    ("Metric",                 "Value"),
    ("Missing values in orders",     str(orders.isnull().sum().sum())),
    ("Duplicate order IDs",          str(orders.duplicated(subset=['order_id']).sum())),
    ("Invalid ratings (not 1-5)",    str((~feedback['rating'].between(1,5)).sum())),
    ("Negative order values",         str((orders['order_value'] < 0).sum())),
    ("Referential integrity issues", "0 (all keys valid)"),
    ("Analysis period",              "Jan 2024 – Dec 2024"),
    ("Data type",                    "SYNTHETIC (demo only)"),
]
next_row3 = len(summary_data) + 5
add_section_title(ws8, next_row3, "DATA QUALITY METRICS", col_span=4)
for i, row_data in enumerate(dq_data):
    ws8.append(row_data)
    if i == 0:
        style_header(ws8, next_row3 + 1, 2)
    else:
        r = ws8.max_row
        fill = ALT_FILL if i % 2 == 0 else PatternFill()
        for col in [1, 2]:
            ws8.cell(row=r, column=col).fill = fill
            ws8.cell(row=r, column=col).border = THIN_BORDER

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 9: PIVOT READY DATA
# ══════════════════════════════════════════════════════════════════════════════
print("Creating Sheet 9: Pivot Ready Data...")
ws9 = wb.create_sheet("Pivot Ready Data")

# Flat analytical table for pivot creation
pivot_data = (orders
    .merge(restaurants[['restaurant_id','restaurant_name','cuisine','area','city']], on='restaurant_id')
    .merge(deliveries[['order_id','actual_delivery_minutes','on_time_status','delay_minutes']],
           on='order_id', how='left')
    .merge(feedback[['order_id','rating','complaint_type','refund_amount']],
           on='order_id', how='left')
    [['order_id','order_time','order_hour','order_month','city','area',
      'restaurant_name','cuisine','order_value','discount','final_amount',
      'order_status','is_cancelled','actual_delivery_minutes','on_time_status',
      'delay_minutes','rating','complaint_type','refund_amount']]
    .head(10000)   # sample for Excel manageability
)

ws9.merge_cells("A1:S1")
ws9["A1"] = "Pivot-Ready Data Table (Sample: 10,000 orders) — Use Insert → PivotTable in Excel"
ws9["A1"].font = Font(name='Calibri', bold=True, size=11, color=DARK_GREY)
ws9["A1"].fill = PatternFill("solid", fgColor=LIGHT_GREY)
ws9["A1"].alignment = Alignment(horizontal='center')
ws9.row_dimensions[1].height = 20

write_df(ws9, pivot_data, start_row=2, header_fill=HEADER_FILL)
for i in range(1, len(pivot_data.columns)+2):
    ws9.column_dimensions[get_column_letter(i)].width = 18

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
os.makedirs(EXCEL_DIR, exist_ok=True)
wb.save(OUT_PATH)
size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
print(f"\nExcel workbook saved: {OUT_PATH}")
print(f"File size: {size_mb:.2f} MB")
print("\nSheets created:")
for sheet in wb.sheetnames:
    print(f"  - {sheet}")
