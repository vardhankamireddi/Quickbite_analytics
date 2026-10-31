# Master QA & Audit Test Report (T01 – T19)
**CODEGNAN Hackathon — Problem ID: DA-07 | Team: Data Knights**  
**Audit Date:** October 31, 2026 | **Test Harness:** Python 3.14 `unittest` + Custom Analytical Assertions  
**Execution Command:** `python -m unittest quickbite-analytics/tests/test_audit_suite.py`

---

## 1. Executive Test Execution Summary

- **Total Test Cases Executed:** **19**
- **Passed:** **19 (100%)**
- **Failed:** **0 (0%)**
- **Skipped:** **0 (0%)**
- **Execution Elapsed Time:** **6.938 seconds**
- **Final Verdict:** **ALL TESTS PASS (Zero Regressions)**

---

## 2. Master Test Matrix (T01 – T19)

| Test ID | Test Category & Focus | Execution Method & Command | Expected Assertion | Observed Result | Evidence Path / Artifact | Final Status |
|---|---|---|---|---|---|---|
| **T01** | **Baseline Integrity** | Python `test_T01_baseline_integrity` | All 6 raw CSVs, 4 generation scripts, and docs exist and are non-empty. | 11/11 files exist with positive size. Zero raw files deleted or overwritten. | `quickbite-analytics/data/raw/` | **PASS** |
| **T02** | **Schema Contract** | Python `test_T02_schema_contract` | All primary keys unique; required columns and valid types present. | All PKs unique (Orders: 100k, Restaurants: 4k, Deliveries: 87.8k, Customers: 20k). | `data/cleaned/*_cleaned.csv` | **PASS** |
| **T03** | **Data Quality** | Python `test_T03_data_quality` | 0 unexpected duplicates, feedback rating in [1, 5], order amounts > 0. | 0 duplicate rows; ratings bounded [1, 5]; all monetary fields positive. | `audit/DATA_QUALITY_AND_LINEAGE.md` | **PASS** |
| **T04** | **Join Integrity** | Python `test_T04_join_integrity` | 100% FK match rate; 0 deliveries for cancelled orders; zero fanout. | 100% FK coverage; 0 deliveries on cancelled; merge preserves 100,000 grain. | `audit/evidence/join_audit.log` | **PASS** |
| **T05** | **Temporal Logic** | Python `test_T05_temporal_logic` | `order_time <= pickup_time <= delivery_time`; hour in [0, 23]; midnight boundary. | 100% chronologically consistent; midnight boundary test duration = 45.0 min. | `data/cleaned/deliveries_cleaned.csv` | **PASS** |
| **T06** | **Monetary & Order Rules** | Python `test_T06_order_and_monetary_rules` | `final_amount == order_value - discount`; valid order status set. | Absolute variance < 0.02 across all 100k orders; valid 4-status distribution. | `data/cleaned/orders_cleaned.csv` | **PASS** |
| **T07** | **KPI Mathematical Edge Fixtures** | Python `test_T07_kpi_mathematical_checks` | Zero denominator, canceled-only orders, single customer repeat orders handled safely. | Zero denominator returns 0.0%; canceled-only GOV returns 0.0; repeat fixture = 50%. | `tests/test_audit_suite.py` | **PASS** |
| **T08** | **SQL Execution** | Python `test_T08_sql_execution` | All 20 SQL query CSV outputs exist, are readable, and contain valid rows. | 20 of 20 query CSV files verified (`05_Q01_*.csv` to `05_Q20_*.csv`). | `quickbite-analytics/sql/05_Q*.csv` | **FIXED & RETESTED** |
| **T09** | **SQL ↔ Python Parity** | Python `test_T09_sql_python_parity` | Exact order counts and net sales per city between Python and SQL queries Q01, Q02. | Exact zero variance across Hyderabad, Visakhapatnam, and Vijayawada. | `audit/KPI_DEFINITIONS_AND_RECONCILIATION.md` | **PASS** |
| **T10** | **Excel Accuracy** | Python `test_T10_excel_accuracy` | Workbook loads; sheet names match; Executive Summary city orders equal 100,000. | All 9 sheets present; city orders (55032, 25311, 19657) sum to 100,000. | `excel/QuickBite_Excel_Analysis.xlsx` | **PASS** |
| **T11** | **Power BI DAX Parity** | Python `test_T11_powerbi_dax_parity` | All 7 KPI expressions evaluated on canonical data match baseline targets. | Orders: 100k, GOV: ₹32.88M, Avg Del: 46.4m, On-Time: 82.8%, Cancel: 12.18%, Rating: 3.71, Repeat: 79.59%. | `powerbi/02_dax_measures.md` | **FIXED & RETESTED** |
| **T12** | **Power BI Slicers & Model** | Python `test_T12_powerbi_slicers_and_model` | Data model documentation specifies bidirectional cross-filtering for 1:1 tables. | Verified `Both (Bidirectional)` in `01_data_model.md` and build guide. | `powerbi/01_data_model.md` | **FIXED & RETESTED** |
| **T13** | **Ranking Robustness** | Python `test_T13_ranking_robustness` | Minimum sample size thresholds (Q05 >= 10 reviews, Q10 >= 20 orders) enforced. | 100% of ranked restaurants meet minimum sample size; no 1-order anomalies. | `sql/05_Q05_*.csv`, `05_Q10_*.csv` | **PASS** |
| **T14** | **Insight Truthfulness** | Python `test_T14_correlation_truthfulness` | Delay negatively correlates with rating ($r < -0.3$); distance correlates with time ($r > 0.5$). | Delay-rating $r = -0.42$; distance-duration $r = 0.62$. No unsupported causal claims. | `docs/final_report.md` | **FIXED & RETESTED** |
| **T15** | **Outputs & Reproducibility** | Python `test_T15_outputs_reproducibility` | Jupyter notebook fully executed with 31 completed code outputs; all CSVs load. | 31/31 code cells have executed outputs; notebook size 1.48 MB; charts embedded. | `notebooks/01_Data_Cleaning_and_EDA.ipynb` | **FIXED & RETESTED** |
| **T16** | **Safety & Privacy** | Python `test_T16_safety_privacy` | No hardcoded credentials, secret keys, or live production connection strings. | Scanned all `.py`, `.sql`, `.md`, `.json` files. Zero sensitive tokens detected. | Full workspace scan | **FIXED & RETESTED** |
| **T17** | **Deliverables Completeness** | Python `test_T17_deliverables_completeness` | All required core submission deliverables exist and are accessible. | Verified `.sql`, outputs, `.ipynb`, cleaned data, Excel workbook, report, slides. | `audit/SUBMISSION_CHECKLIST.md` | **PASS** |
| **T18** | **Presentation Quality** | Python `test_T18_presentation` | Presentation contains 8 slides, speaker notes, and 3 priority recommendations. | 8 structured slides; speaker notes on all slides; 3 actionable recommendations. | `presentation/QuickBite_Presentation_Deck.md` | **PASS** |
| **T19** | **Full Regression Suite** | Python `test_T19_regression_suite` | Clean data row counts match raw data exactly; full test suite passes. | Cleaned row counts match raw 100%; 19/19 tests PASS in 6.9s. | `tests/test_audit_suite.py` | **PASS** |

---

## 3. Disclosed Manual & Blocked Boundary Items

- **Power BI Desktop Native UI Refresh:** Power BI Desktop is a Windows GUI desktop application without a headless command-line interface. Direct visual rendering, interactive button clicks, and `.pbix` saving cannot be executed headlessly.
- **Verification Strategy:** We conducted a deep static audit of all DAX measures, M queries, and model relationships, and computed canonical expected values for 5 slicer combinations. A step-by-step manual test checklist is provided in `audit/POWER_BI_MANUAL_VERIFICATION.md`.
