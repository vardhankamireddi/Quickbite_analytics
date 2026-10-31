# QuickBite Analytics – CODEGNAN Hackathon DA-07

## Team: Data Knights
**Hackathon:** CODEGNAN  
**Problem ID:** DA-07  
**Industry:** Food Delivery  
**Project Title:** Restaurant Performance, Delivery Time and Customer Rating Analysis

> ⚠️ **All data in this project is explicitly SYNTHETIC and generated for demonstration
> purposes only. It does not represent actual business records.**

---

## Project Structure

```
quickbite-analytics/
│
├── generate_dataset.py          ← Run first: generates all raw CSV data
├── generate_notebook.py         ← Run second: creates Jupyter notebook
├── generate_excel.py            ← Run third: creates Excel workbook  
├── generate_sql_results.py      ← Run fourth: generates SQL results + Power BI CSVs
│
├── data/
│   ├── raw/                     ← 6 original synthetic CSVs
│   │   ├── orders.csv           (100,000 rows)
│   │   ├── restaurants.csv      (4,000 rows)
│   │   ├── deliveries.csv       (87,822 rows)
│   │   ├── customers.csv        (20,000 rows)
│   │   ├── feedback.csv         (70,302 rows)
│   │   └── riders.csv           (2,000 rows)
│   ├── dirty/                   ← Intentionally dirty copies for cleaning demo
│   ├── cleaned/                 ← Post-cleaning output (from notebook)
│   └── powerbi/                 ← Power BI-ready imports
│       ├── pbi_orders_master.csv  (flat analytical table)
│       └── *_cleaned.csv copies
│
├── notebooks/
│   └── 01_Data_Cleaning_and_EDA.ipynb   ← Main Jupyter notebook (57 cells)
│
├── sql/
│   ├── 01_create_database.sql    ← Create quickbite_analytics DB
│   ├── 02_create_tables.sql      ← Create all 6 tables with PKs, FKs, indexes
│   ├── 03_import_instructions.md ← Step-by-step MySQL import guide
│   ├── 04_analysis_queries.sql   ← All 20 SQL analysis queries
│   ├── 05_sql_results_summary.md ← Query results in markdown
│   └── 05_Q*.csv                 ← Individual query result CSVs
│
├── excel/
│   ├── QuickBite_Excel_Analysis.xlsx    ← 9-sheet Excel workbook (1.06 MB)
│   └── pivot_table_instructions.md     ← Guide to create pivot tables
│
├── powerbi/
│   ├── 01_data_model.md          ← Star schema, relationships, Power Query code
│   ├── 02_dax_measures.md        ← All 20 DAX measures with definitions
│   ├── 03_dashboard_design.md    ← Page-by-page visual specifications
│   ├── 04_build_instructions.md  ← Step-by-step dashboard build guide (~30 min)
│   └── powerbi_ready_data/       ← Optimised CSVs for Power BI import
│
└── docs/
    ├── data_dictionary.md         ← Field-by-field documentation
    ├── synthetic_data_assumptions.md  ← All modeling assumptions
    └── final_report.md            ← Executive analysis report
```

---

## Quick Start

### Step 1: Generate Datasets
```bash
python generate_dataset.py
```
Produces all 6 raw CSVs + dirty copies. Takes ~30 seconds.

### Step 2: Open Jupyter Notebook
```bash
jupyter notebook notebooks/01_Data_Cleaning_and_EDA.ipynb
```
Install dependencies: `pip install pandas numpy matplotlib seaborn jupyter`  
Run all cells (Kernel → Restart & Run All)

### Step 3: Run SQL Analysis
1. Open MySQL Workbench
2. Run `sql/01_create_database.sql`
3. Run `sql/02_create_tables.sql`
4. Follow `sql/03_import_instructions.md` to load CSVs
5. Run `sql/04_analysis_queries.sql`

### Step 4: Open Excel Workbook
Open `excel/QuickBite_Excel_Analysis.xlsx` directly.  
Follow `excel/pivot_table_instructions.md` to add pivot tables.

### Step 5: Build Power BI Dashboard
1. Open Power BI Desktop
2. Import CSVs from `data/powerbi/`
3. Follow `powerbi/04_build_instructions.md` (25–35 min)

---

## Key Findings Summary

| Finding | Impact | Recommended Action |
|---|---|---|
| 12.2% cancellation rate | ₹X lost revenue | Rider surge incentives (19–22h) |
| Peak-hour delays (dinner) | Rating drops to 3.0★ | Route optimisation AI |
| 40% one-time customers | Low LTV | Retention programme + 2nd-order discount |
| Late delivery = #1 complaint | 32% of complaints | Zone-based delivery SLAs |
| Severe delay → 2.5★ avg | Customer churn | Proactive delay alerts |

---

## Technical Stack

| Component | Technology |
|---|---|
| Data Generation | Python 3.10+, NumPy, Pandas |
| Data Cleaning & EDA | Jupyter Notebook, Pandas, Matplotlib, Seaborn |
| Database | MySQL 8.0, SQL (CTEs, Window Functions, Joins) |
| Excel Analysis | openpyxl, Excel 2016+ |
| Business Intelligence | Power BI Desktop |

---

## Team Information

- **Team Name:** Data Knights
- **Hackathon:** CODEGNAN
- **Problem:** DA-07 – Food Delivery Analytics
- **Random Seed:** 42 (for full reproducibility)
