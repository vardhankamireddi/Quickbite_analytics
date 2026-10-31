import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('quickbite-analytics/excel/QuickBite_Excel_Analysis.xlsx', data_only=True)

for name in wb.sheetnames:
    ws = wb[name]
    found = []
    for r in range(1, min(ws.max_row+1, 50)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 10))]
        for c, v in enumerate(row_vals):
            if v == 'Hyderabad':
                found.append((r, row_vals))
                break
    if found:
        print(f"\nSheet '{name}' has Hyderabad in rows:")
        for r, vals in found[:3]:
            print(f"  Row {r:2d}: {vals}")
