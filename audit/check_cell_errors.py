import json

with open("quickbite-analytics/notebooks/01_Data_Cleaning_and_EDA.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for idx in [36, 42]:
    cell = nb['cells'][idx]
    print(f"\n--- CELL {idx} SOURCE ---")
    print("".join(cell['source']))
    print(f"--- CELL {idx} ERROR OUTPUT ---")
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'error':
            print("\n".join(out.get('traceback', [])))
