import openpyxl
import pandas as pd

wb = openpyxl.load_workbook('quickbite-analytics/excel/QuickBite_Excel_Analysis.xlsx', data_only=True)

print("--- EXCEL EXECUTIVE SUMMARY VALUES ---")
ws_exec = wb['Executive Summary']
for r in range(1, 15):
    row_vals = [ws_exec.cell(r, c).value for c in range(1, 6)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")

print("\n--- EXCEL CITY PERFORMANCE VALUES ---")
ws_city = wb['City Performance']
for r in range(1, 10):
    row_vals = [ws_city.cell(r, c).value for c in range(1, 8)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")

print("\n--- EXCEL HOURLY ANALYSIS VALUES (First 6 hours) ---")
ws_hour = wb['Hourly Analysis']
for r in range(1, 10):
    row_vals = [ws_hour.cell(r, c).value for c in range(1, 8)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")
