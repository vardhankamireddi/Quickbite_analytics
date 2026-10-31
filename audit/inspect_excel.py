import openpyxl

wb = openpyxl.load_workbook('quickbite-analytics/excel/QuickBite_Excel_Analysis.xlsx', data_only=False)

print("Worksheet details:")
for name in wb.sheetnames:
    ws = wb[name]
    max_r = ws.max_row
    max_c = ws.max_column
    
    # Check formulas
    formulas = []
    for row in ws.iter_rows(values_only=False):
        for cell in row:
            if cell.value and str(cell.value).startswith('='):
                formulas.append(f"{cell.coordinate}: {cell.value}")
                
    print(f"\nSheet: '{name}'")
    print(f"  Dimensions: {max_r} rows x {max_c} cols")
    print(f"  Charts: {len(ws._charts)}")
    print(f"  Tables: {len(ws.tables)}")
    print(f"  PivotTables: {len(ws._pivots)}")
    print(f"  Formulas count: {len(formulas)}")
    if formulas:
        print(f"  Sample formulas: {formulas[:5]}")
