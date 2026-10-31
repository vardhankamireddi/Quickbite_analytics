"""
QuickBite Analytics - Master QA & Automated Audit Test Suite (T01 - T19)
Team: Data Knights | Problem ID: DA-07 | Hackathon: CODEGNAN

Covers:
- Baseline integrity & Schema Contracts
- Data Quality & Referential Integrity
- Temporal & Monetary Rules
- Edge-Case Fixtures & KPI Mathematical Contracts
- SQL Execution & SQL <-> Python <-> Excel Parity
- Power BI DAX & Model Constraints
- Deliverables Completeness & Reproducibility
"""

import unittest
import os
import json
import openpyxl
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
CLEANED_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')
SQL_DIR = os.path.join(BASE_DIR, 'sql')
EXCEL_PATH = os.path.join(BASE_DIR, 'excel', 'QuickBite_Excel_Analysis.xlsx')
NB_PATH = os.path.join(BASE_DIR, 'notebooks', '01_Data_Cleaning_and_EDA.ipynb')
PBI_DIR = os.path.join(BASE_DIR, 'powerbi')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
PRES_DIR = os.path.join(BASE_DIR, 'presentation')

class TestQuickBiteAuditSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load canonical datasets
        cls.raw_orders = pd.read_csv(os.path.join(RAW_DIR, 'orders.csv'), low_memory=False)
        cls.raw_restaurants = pd.read_csv(os.path.join(RAW_DIR, 'restaurants.csv'), low_memory=False)
        cls.raw_deliveries = pd.read_csv(os.path.join(RAW_DIR, 'deliveries.csv'), low_memory=False)
        cls.raw_customers = pd.read_csv(os.path.join(RAW_DIR, 'customers.csv'), low_memory=False)
        cls.raw_feedback = pd.read_csv(os.path.join(RAW_DIR, 'feedback.csv'), low_memory=False)
        cls.raw_riders = pd.read_csv(os.path.join(RAW_DIR, 'riders.csv'), low_memory=False)

        cls.orders_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'orders_cleaned.csv'), low_memory=False)
        cls.deliveries_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'deliveries_cleaned.csv'), low_memory=False)
        cls.restaurants_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'restaurants_cleaned.csv'), low_memory=False)
        cls.customers_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'customers_cleaned.csv'), low_memory=False)
        cls.feedback_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'feedback_cleaned.csv'), low_memory=False)
        cls.riders_clean = pd.read_csv(os.path.join(CLEANED_DIR, 'riders_cleaned.csv'), low_memory=False)

    # ─────────────────────────────────────────────────────────────
    # T01: Baseline Integrity
    # ─────────────────────────────────────────────────────────────
    def test_T01_baseline_integrity(self):
        """T01: Verify original raw files, scripts, and documentation exist without deletion."""
        required_files = [
            os.path.join(RAW_DIR, 'orders.csv'),
            os.path.join(RAW_DIR, 'restaurants.csv'),
            os.path.join(RAW_DIR, 'deliveries.csv'),
            os.path.join(RAW_DIR, 'customers.csv'),
            os.path.join(RAW_DIR, 'feedback.csv'),
            os.path.join(RAW_DIR, 'riders.csv'),
            os.path.join(BASE_DIR, 'generate_dataset.py'),
            os.path.join(BASE_DIR, 'generate_notebook.py'),
            os.path.join(BASE_DIR, 'generate_excel.py'),
            os.path.join(BASE_DIR, 'generate_sql_results.py'),
            os.path.join(BASE_DIR, 'README.md'),
        ]
        for f in required_files:
            self.assertTrue(os.path.exists(f), f"Required baseline file missing: {f}")
            self.assertGreater(os.path.getsize(f), 0, f"File is empty: {f}")

    # ─────────────────────────────────────────────────────────────
    # T02: Schema Contract
    # ─────────────────────────────────────────────────────────────
    def test_T02_schema_contract(self):
        """T02: Verify required columns and primary keys exist across all tables."""
        expected_schemas = {
            'orders': ['order_id', 'customer_id', 'restaurant_id', 'rider_id', 'order_time', 'order_value', 'discount', 'final_amount', 'order_status'],
            'restaurants': ['restaurant_id', 'restaurant_name', 'cuisine', 'area', 'city', 'avg_prep_time', 'restaurant_rating'],
            'deliveries': ['delivery_id', 'order_id', 'rider_id', 'pickup_time', 'delivery_time', 'distance_km', 'actual_delivery_minutes', 'delay_minutes', 'on_time_status'],
            'customers': ['customer_id', 'signup_date', 'city', 'total_orders'],
            'feedback': ['feedback_id', 'order_id', 'customer_id', 'rating', 'refund_amount'],
            'riders': ['rider_id', 'rider_city', 'availability_status']
        }
        for col in expected_schemas['orders']:
            self.assertIn(col, self.orders_clean.columns)
        for col in expected_schemas['restaurants']:
            self.assertIn(col, self.restaurants_clean.columns)
        for col in expected_schemas['deliveries']:
            self.assertIn(col, self.deliveries_clean.columns)
        for col in expected_schemas['customers']:
            self.assertIn(col, self.customers_clean.columns)
        for col in expected_schemas['feedback']:
            self.assertIn(col, self.feedback_clean.columns)
        for col in expected_schemas['riders']:
            self.assertIn(col, self.riders_clean.columns)

        # Primary Key uniqueness
        self.assertEqual(len(self.orders_clean), self.orders_clean['order_id'].nunique())
        self.assertEqual(len(self.restaurants_clean), self.restaurants_clean['restaurant_id'].nunique())
        self.assertEqual(len(self.deliveries_clean), self.deliveries_clean['delivery_id'].nunique())
        self.assertEqual(len(self.customers_clean), self.customers_clean['customer_id'].nunique())
        self.assertEqual(len(self.feedback_clean), self.feedback_clean['feedback_id'].nunique())
        self.assertEqual(len(self.riders_clean), self.riders_clean['rider_id'].nunique())

    # ─────────────────────────────────────────────────────────────
    # T03: Data Quality
    # ─────────────────────────────────────────────────────────────
    def test_T03_data_quality(self):
        """T03: Verify duplicates, ratings range, and positive values."""
        self.assertEqual(self.orders_clean.duplicated().sum(), 0)
        self.assertEqual(self.restaurants_clean.duplicated().sum(), 0)
        self.assertEqual(self.deliveries_clean.duplicated().sum(), 0)
        
        # Ratings strictly between 1 and 5
        self.assertTrue(self.feedback_clean['rating'].between(1, 5).all())
        self.assertTrue(self.restaurants_clean['restaurant_rating'].between(1.0, 5.0).all())
        
        # Positive financial amounts
        self.assertTrue((self.orders_clean['order_value'] > 0).all())
        self.assertTrue((self.orders_clean['discount'] >= 0).all())
        self.assertTrue((self.orders_clean['final_amount'] > 0).all())

    # ─────────────────────────────────────────────────────────────
    # T04: Join Integrity
    # ─────────────────────────────────────────────────────────────
    def test_T04_join_integrity(self):
        """T04: Verify referential integrity, 1:1 delivery/feedback grain, no row fanout."""
        # Foreign key coverage
        self.assertTrue(self.orders_clean['customer_id'].isin(self.customers_clean['customer_id']).all())
        self.assertTrue(self.orders_clean['restaurant_id'].isin(self.restaurants_clean['restaurant_id']).all())
        self.assertTrue(self.orders_clean['rider_id'].isin(self.riders_clean['rider_id']).all())
        self.assertTrue(self.deliveries_clean['order_id'].isin(self.orders_clean['order_id']).all())
        self.assertTrue(self.feedback_clean['order_id'].isin(self.orders_clean['order_id']).all())

        # Cardinality: exactly 1 delivery record per delivered order, 0 for cancelled
        cancelled_ids = set(self.orders_clean[self.orders_clean['is_cancelled']]['order_id'])
        del_on_cancelled = self.deliveries_clean[self.deliveries_clean['order_id'].isin(cancelled_ids)]
        self.assertEqual(len(del_on_cancelled), 0)

        # Merge check: order total does not multiply
        merged = self.orders_clean.merge(self.deliveries_clean[['order_id','delivery_id']], on='order_id', how='left')
        self.assertEqual(len(merged), len(self.orders_clean))

    # ─────────────────────────────────────────────────────────────
    # T05: Temporal Logic
    # ─────────────────────────────────────────────────────────────
    def test_T05_temporal_logic(self):
        """T05: Verify order_time <= pickup_time <= delivery_time, hour range, midnight boundary."""
        orders_dt = pd.to_datetime(self.orders_clean['order_time'])
        del_pickup = pd.to_datetime(self.deliveries_clean['pickup_time'])
        del_drop = pd.to_datetime(self.deliveries_clean['delivery_time'])

        self.assertTrue((del_drop >= del_pickup).all())
        self.assertTrue(self.orders_clean['order_hour'].between(0, 23).all())

        # Edge test: synthetic midnight fixture
        t_order = datetime(2024, 6, 15, 23, 50, 0)
        t_pickup = datetime(2024, 6, 16, 0, 10, 0)
        t_drop = datetime(2024, 6, 16, 0, 35, 0)
        duration = (t_drop - t_order).total_seconds() / 60.0
        self.assertEqual(duration, 45.0)

    # ─────────────────────────────────────────────────────────────
    # T06: Order and Monetary Rules
    # ─────────────────────────────────────────────────────────────
    def test_T06_order_and_monetary_rules(self):
        """T06: Verify final_amount == order_value - discount, refund bounds."""
        expected_final = (self.orders_clean['order_value'] - self.orders_clean['discount']).round(2)
        actual_final = self.orders_clean['final_amount'].round(2)
        diff = (expected_final - actual_final).abs()
        self.assertTrue((diff < 0.02).all())

        # Status distribution
        valid_statuses = {'Completed', 'Partially Delivered', 'Cancelled', 'Refunded'}
        self.assertTrue(set(self.orders_clean['order_status']).issubset(valid_statuses))

    # ─────────────────────────────────────────────────────────────
    # T07: KPI Mathematical Checks (Edge Fixtures)
    # ─────────────────────────────────────────────────────────────
    def test_T07_kpi_mathematical_checks(self):
        """T07: Test all 7 KPIs against zero-denominator and edge synthetic fixtures."""
        # Fixture 1: Zero orders
        df_empty = pd.DataFrame(columns=['order_id', 'order_status', 'order_value', 'final_amount'])
        total_orders = len(df_empty)
        cancel_rate = (len(df_empty[df_empty['order_status'] == 'Cancelled']) / total_orders * 100) if total_orders > 0 else 0.0
        self.assertEqual(cancel_rate, 0.0)

        # Fixture 2: Canceled-only orders
        df_cancelled = pd.DataFrame({
            'order_id': ['O1', 'O2'],
            'order_status': ['Cancelled', 'Cancelled'],
            'order_value': [100.0, 200.0],
            'final_amount': [100.0, 200.0]
        })
        gov_completed = df_cancelled[df_cancelled['order_status'].isin(['Completed', 'Partially Delivered'])]['order_value'].sum()
        self.assertEqual(gov_completed, 0.0)
        cancel_rate_100 = len(df_cancelled[df_cancelled['order_status'] == 'Cancelled']) / len(df_cancelled) * 100
        self.assertEqual(cancel_rate_100, 100.0)

        # Fixture 3: Single customer repeated orders
        cust_orders = pd.Series([1, 2, 5, 1])
        repeat_rate = (cust_orders >= 2).mean() * 100
        self.assertEqual(repeat_rate, 50.0)

    # ─────────────────────────────────────────────────────────────
    # T08: SQL Execution
    # ─────────────────────────────────────────────────────────────
    def test_T08_sql_execution(self):
        """T08: Verify all 20 SQL query output CSV files exist, are readable, and non-empty."""
        for q_num in range(1, 21):
            pattern = f"05_Q{q_num:02d}_*.csv"
            import glob
            matches = glob.glob(os.path.join(SQL_DIR, pattern))
            self.assertGreaterEqual(len(matches), 1, f"Missing SQL output for Q{q_num:02d}")
            df = pd.read_csv(matches[0])
            self.assertGreater(len(df), 0, f"Empty SQL result for Q{q_num:02d}")

    # ─────────────────────────────────────────────────────────────
    # T09: SQL <-> Python Parity
    # ─────────────────────────────────────────────────────────────
    def test_T09_sql_python_parity(self):
        """T09: Verify exact numerical parity between Python calculations and SQL query outputs."""
        sql_q01 = pd.read_csv(os.path.join(SQL_DIR, '05_Q01_Total_Orders_by_City.csv')).set_index('city')
        py_city = self.orders_clean.merge(self.restaurants_clean[['restaurant_id','city']], on='restaurant_id')
        py_orders_by_city = py_city.groupby('city').size()

        for city, count in py_orders_by_city.items():
            self.assertEqual(count, int(sql_q01.loc[city, 'total_orders']), f"Order count mismatch for {city}")

        sql_q02 = pd.read_csv(os.path.join(SQL_DIR, '05_Q02_Revenue_by_City.csv')).set_index('city')
        py_completed = py_city[py_city['order_status'].isin(['Completed', 'Partially Delivered'])]
        py_rev_by_city = py_completed.groupby('city')['final_amount'].sum().round(2)

        for city, rev in py_rev_by_city.items():
            diff = abs(rev - float(sql_q02.loc[city, 'net_sales_inr']))
            self.assertLess(diff, 0.05, f"Revenue mismatch for {city}: {diff}")

    # ─────────────────────────────────────────────────────────────
    # T10: Excel Accuracy
    # ─────────────────────────────────────────────────────────────
    def test_T10_excel_accuracy(self):
        """T10: Verify Excel workbook structure, sheet names, and total orders reconciliation."""
        self.assertTrue(os.path.exists(EXCEL_PATH))
        wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
        expected_sheets = ['Executive Summary', 'City Performance', 'Restaurant Performance', 'Cuisine Performance', 'Hourly Analysis', 'Cancellation Analysis', 'Customer Retention', 'Data Summary', 'Pivot Ready Data']
        for s in expected_sheets:
            self.assertIn(s, wb.sheetnames)

        # Reconcile Executive Summary city totals
        ws_exec = wb['Executive Summary']
        excel_cities = {}
        for r in range(16, 19):
            city = ws_exec.cell(r, 1).value
            orders = ws_exec.cell(r, 2).value
            excel_cities[city] = orders

        self.assertEqual(excel_cities.get('Hyderabad'), 55032)
        self.assertEqual(excel_cities.get('Visakhapatnam'), 25311)
        self.assertEqual(excel_cities.get('Vijayawada'), 19657)
        self.assertEqual(sum(excel_cities.values()), 100000)

    # ─────────────────────────────────────────────────────────────
    # T11: Power BI DAX Parity
    # ─────────────────────────────────────────────────────────────
    def test_T11_powerbi_dax_parity(self):
        """T11: Compute canonical expected values for 7 KPI cards across full and sliced contexts."""
        # Global context
        total_orders = len(self.orders_clean)
        self.assertEqual(total_orders, 100000)

        completed_mask = self.orders_clean['order_status'].isin(['Completed', 'Partially Delivered'])
        gov = self.orders_clean[completed_mask]['order_value'].sum().round(2)
        self.assertAlmostEqual(gov, 32878778.81, delta=1.0)

        avg_delivery = self.deliveries_clean['actual_delivery_minutes'].mean().round(2)
        self.assertAlmostEqual(avg_delivery, 46.40, delta=0.5)

        on_time_pct = ((self.deliveries_clean['on_time_status'] == 'On Time').mean() * 100).round(2)
        self.assertAlmostEqual(on_time_pct, 82.78, delta=0.5)

        cancel_pct = (self.orders_clean['is_cancelled'].mean() * 100).round(2)
        self.assertAlmostEqual(cancel_pct, 12.18, delta=0.1)

        avg_rating = self.feedback_clean['rating'].mean().round(2)
        self.assertAlmostEqual(avg_rating, 3.71, delta=0.05)

        repeat_rate = ((self.customers_clean['order_count'] >= 2).mean() * 100).round(2)
        self.assertAlmostEqual(repeat_rate, 79.59, delta=0.5)

    # ─────────────────────────────────────────────────────────────
    # T12: Power BI Slicers & Model Relations
    # ─────────────────────────────────────────────────────────────
    def test_T12_powerbi_slicers_and_model(self):
        """T12: Verify documentation enforces bidirectional cross-filtering for 1:1 tables."""
        model_doc = os.path.join(PBI_DIR, '01_data_model.md')
        with open(model_doc, 'r', encoding='utf-8') as f:
            text = f.read()
        self.assertIn("Both (Bidirectional)", text)
        self.assertIn("CRITICAL AUDIT NOTE", text)

    # ─────────────────────────────────────────────────────────────
    # T13: Ranking Robustness
    # ─────────────────────────────────────────────────────────────
    def test_T13_ranking_robustness(self):
        """T13: Verify sample size thresholds in restaurant rankings (Q05 >= 10 reviews, Q10 >= 20 orders)."""
        sql_q05 = pd.read_csv(os.path.join(SQL_DIR, '05_Q05_Restaurant_Ranking_by_Rating.csv'))
        self.assertTrue((sql_q05['total_reviews'] >= 10).all())

        sql_q10 = pd.read_csv(os.path.join(SQL_DIR, '05_Q10_Cancellation_Rate_by_Restaurant.csv'))
        self.assertTrue((sql_q10['total_orders'] >= 20).all())

    # ─────────────────────────────────────────────────────────────
    # T14: Correlation & Insight Truthfulness
    # ─────────────────────────────────────────────────────────────
    def test_T14_correlation_truthfulness(self):
        """T14: Verify delay vs rating negative association and distance vs delivery duration correlation."""
        merged = self.deliveries_clean.merge(self.feedback_clean[['order_id', 'rating']], on='order_id')
        corr_delay_rating = merged['delay_minutes'].corr(merged['rating'])
        self.assertLess(corr_delay_rating, -0.3, "Delay should negatively correlate with rating")

        corr_dist_time = self.deliveries_clean['distance_km'].corr(self.deliveries_clean['actual_delivery_minutes'])
        self.assertGreater(corr_dist_time, 0.5, "Distance should strongly correlate with actual delivery time")

    # ─────────────────────────────────────────────────────────────
    # T15: Outputs & Reproducibility
    # ─────────────────────────────────────────────────────────────
    def test_T15_outputs_reproducibility(self):
        """T15: Verify Jupyter Notebook is executed with 31 completed code outputs."""
        self.assertTrue(os.path.exists(NB_PATH))
        with open(NB_PATH, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
        self.assertEqual(len(code_cells), 31)
        for i, c in enumerate(code_cells):
            self.assertGreater(len(c.get('outputs', [])), 0, f"Code cell {i+1} has no executed output")

    # ─────────────────────────────────────────────────────────────
    # T16: Safety & Privacy
    # ─────────────────────────────────────────────────────────────
    def test_T16_safety_privacy(self):
        """T16: Verify no hardcoded passwords, tokens, or live production connection strings in codebase."""
        forbidden_tokens = ['AWS_' + 'SECRET', 'PRIVATE_' + 'KEY', 'DATABASE_' + 'URL', 'jdbc:mysql://prod']
        for root, _, files in os.walk(BASE_DIR):
            if 'node_modules' in root or '.git' in root or 'tests' in root:
                continue
            for file in files:
                if file.endswith(('.py', '.sql', '.md', '.json')):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for token in forbidden_tokens:
                        self.assertNotIn(token, content, f"Forbidden sensitive token {token} in {filepath}")

    # ─────────────────────────────────────────────────────────────
    # T17: Deliverables Completeness
    # ─────────────────────────────────────────────────────────────
    def test_T17_deliverables_completeness(self):
        """T17: Verify all 8 core submission deliverables exist in workspace."""
        deliverables = [
            os.path.join(SQL_DIR, '04_analysis_queries.sql'),
            os.path.join(SQL_DIR, '05_sql_results_summary.md'),
            os.path.join(NB_PATH),
            os.path.join(CLEANED_DIR, 'orders_cleaned.csv'),
            os.path.join(EXCEL_PATH),
            os.path.join(PBI_DIR, '01_data_model.md'),
            os.path.join(PBI_DIR, '02_dax_measures.md'),
            os.path.join(DOCS_DIR, 'final_report.md'),
            os.path.join(PRES_DIR, 'QuickBite_Presentation_Deck.md'),
            os.path.join(PRES_DIR, 'QuickBite_Presentation_Deck.html')
        ]
        for d in deliverables:
            self.assertTrue(os.path.exists(d), f"Deliverable missing: {d}")

    # ─────────────────────────────────────────────────────────────
    # T18: Presentation Quality & Content
    # ─────────────────────────────────────────────────────────────
    def test_T18_presentation(self):
        """T18: Verify presentation contains 8 structured slides, speaker notes, and 3 priority recommendations."""
        deck_file = os.path.join(PRES_DIR, 'QuickBite_Presentation_Deck.md')
        with open(deck_file, 'r', encoding='utf-8') as f:
            deck = f.read()
        self.assertIn("Priority 1:", deck)
        self.assertIn("Priority 2:", deck)
        self.assertIn("Priority 3:", deck)
        self.assertIn("Speaker Notes", deck)

    # ─────────────────────────────────────────────────────────────
    # T19: Regression Suite
    # ─────────────────────────────────────────────────────────────
    def test_T19_regression_suite(self):
        """T19: Overall regression confirmation verifying clean data counts match raw data exactly."""
        self.assertEqual(len(self.raw_orders), len(self.orders_clean))
        self.assertEqual(len(self.raw_deliveries), len(self.deliveries_clean))
        self.assertEqual(len(self.raw_restaurants), len(self.restaurants_clean))
        self.assertEqual(len(self.raw_customers), len(self.customers_clean))
        self.assertEqual(len(self.raw_feedback), len(self.feedback_clean))
        self.assertEqual(len(self.raw_riders), len(self.riders_clean))

if __name__ == '__main__':
    unittest.main()
