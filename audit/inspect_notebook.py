import json

nb = json.load(open('quickbite-analytics/notebooks/01_Data_Cleaning_and_EDA.ipynb', encoding='utf-8'))
for i, c in enumerate(nb.get('cells', [])):
    src = c.get('source', [''])
    first_line = src[0].strip() if src else ''
    print(f"Cell {i:2d} ({c.get('cell_type'):8s}): {first_line[:75]}")
