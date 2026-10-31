# QuickBite Analytics — Submission Deliverables Checklist
**CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights**  
**Audit & Verification Date:** October 31, 2026

---

## 1. Master Submission Deliverables Matrix

| Required Deliverable Category | Expected File / Artifact Name | Actual Verified Path | File Size | Execution / Verification Status | Evaluator / Audit Notes |
|---|---|---|---|---|---|
| **1. SQL Queries** | `.sql` source script containing all analytical queries | `sql/04_analysis_queries.sql` | 34.5 KB | **VERIFIED** | 20 MySQL 8.0+ queries with CTEs, window functions, and business filters. |
| **2. SQL Outputs** | Exported query result tables / CSVs & summary doc | `sql/05_Q01_*.csv` to `05_Q20_*.csv`<br>`sql/05_sql_results_summary.md` | 20 CSV files<br>(47.2 KB doc) | **FIXED & VERIFIED** | All 20 query results exported and documented. Reconciles with Python. |
| **3. Python Notebook** | `.ipynb` cleaning and exploratory data analysis | `notebooks/01_Data_Cleaning_and_EDA.ipynb` | 1.48 MB | **FIXED & VERIFIED** | 57 total cells; 31/31 code cells executed with tables and 15+ inline PNG figures. |
| **4. Cleaned Dataset** | Cleaned, processed CSV files | `data/cleaned/orders_cleaned.csv`<br>`data/cleaned/deliveries_cleaned.csv`<br>`data/cleaned/restaurants_cleaned.csv`<br>`data/cleaned/customers_cleaned.csv`<br>`data/cleaned/feedback_cleaned.csv`<br>`data/cleaned/riders_cleaned.csv` | 26.8 MB total | **FIXED & VERIFIED** | 6 verified clean datasets with feature engineering. Populated in `data/powerbi/`. |
| **5. Excel Workbook** | Excel analysis with pivot summaries | `excel/QuickBite_Excel_Analysis.xlsx`<br>`excel/pivot_table_instructions.md` | 1.06 MB | **VERIFIED** | 9 formatted sheets; 10,001 pivot-ready transaction rows. Reconciles with Python & SQL. |
| **6. Power BI Model & DAX** | Power BI star schema, DAX measures, design spec | `powerbi/01_data_model.md`<br>`powerbi/02_dax_measures.md`<br>`powerbi/03_dashboard_design.md`<br>`powerbi/04_build_instructions.md` | 30.2 KB docs | **FIXED & VERIFIED** | Corrected bidirectional cross-filter relationships; 20 audited DAX measures. |
| **7. Power BI Binary (.pbix)**| Compiled Power BI Desktop binary file | `powerbi/*.pbix` | 0 KB | **MISSING (Desktop GUI)** | Power BI Desktop GUI required to compile `.pbix`. Complete manual guide in `audit/POWER_BI_MANUAL_VERIFICATION.md`. |
| **8. Written Report** | Executive analytical report | `docs/final_report.md`<br>`audit/FINAL_PROJECT_EXPLANATION.md`<br>`audit/FINAL_PROJECT_EXPLANATION.pdf` | 8.2 KB<br>18.5 KB<br>14.4 KB | **FIXED & VERIFIED** | Corrected retention metrics; comprehensive report exported to Markdown and PDF. |
| **9. Presentation Deck** | 5–10 minute presentation deck & talk track | `presentation/QuickBite_Presentation_Deck.md`<br>`presentation/QuickBite_Presentation_Deck.html` | 8.5 KB<br>15.2 KB | **FIXED & VERIFIED** | 8 structured slides with timing and speaker notes. Standalone HTML presentation included. |
| **10. QA Audit Suite** | Automated test suite (T01–T19) | `tests/test_audit_suite.py`<br>`audit/TEST_REPORT.md` | 17.5 KB<br>8.2 KB | **FIXED & VERIFIED** | 19 automated tests covering T01–T19. 100% PASS (19/19 in 6.9s). |

---

## 2. Deliverables Readiness Summary

- **Deliverables Ready for Direct Submission:** 9 of 10 items (90% native submission readiness).
- **Desktop Boundary Item:** `.pbix` compilation is documented with full data mart (`pbi_orders_master.csv`), DAX measures, relationship diagrams, and exact expected values across 5 test scenarios.
