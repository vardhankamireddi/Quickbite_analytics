import sqlite3
import pandas as pd
import os
import re

# Connect to in-memory SQLite
conn = sqlite3.connect(":memory:")

# Register MySQL-compatible helper functions
def sql_hour(val):
    if not val: return None
    try:
        # Expected format: 'YYYY-MM-DD HH:MM:SS'
        return int(str(val)[11:13])
    except:
        return None

def sql_date(val):
    if not val: return None
    try:
        return str(val)[:10]
    except:
        return None

def sql_concat(*args):
    return "".join(str(a) if a is not None else "" for a in args)

conn.create_function("HOUR", 1, sql_hour)
conn.create_function("DATE", 1, sql_date)
conn.create_function("CONCAT", -1, sql_concat)

RAW_DIR = "quickbite-analytics/data/raw"
tables = ["customers", "deliveries", "feedback", "orders", "restaurants", "riders"]
for t in tables:
    df = pd.read_csv(os.path.join(RAW_DIR, f"{t}.csv"), low_memory=False)
    df.to_sql(t, conn, index=False, if_exists="replace")
    print(f"Loaded {t}: {len(df):,} rows")

print("\n--- RUNNING ALL 20 SQL QUERIES AGAINST SQLITE ---")

with open('quickbite-analytics/sql/04_analysis_queries.sql', 'r', encoding='utf-8') as f:
    text = f.read()

matches = list(re.finditer(r'-- QUERY (\d+):\s*([^\n]+)', text))

results = {}
failures = {}

for i, m in enumerate(matches):
    q_num = int(m.group(1))
    title = m.group(2).strip()
    start_pos = m.end()
    end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
    block = text[start_pos:end_pos]
    
    lines = block.split('\n')
    sql_lines = []
    in_sql = False
    for line in lines:
        stripped = line.strip()
        if not in_sql:
            if stripped.startswith('SELECT') or stripped.startswith('WITH'):
                in_sql = True
                sql_lines.append(line)
        else:
            sql_lines.append(line)
            
    sql_text = '\n'.join(sql_lines).strip()
    if sql_text.endswith(';'):
        sql_text = sql_text[:-1].strip()
        
    try:
        res_df = pd.read_sql_query(sql_text, conn)
        results[q_num] = {'title': title, 'df': res_df}
        print(f"PASS Q{q_num:02d}: {title:45s} -> {len(res_df):>6,} rows returned")
    except Exception as e:
        failures[q_num] = {'title': title, 'sql': sql_text, 'error': str(e)}
        print(f"FAIL Q{q_num:02d}: {title:45s} -> ERROR: {e}")

print(f"\nSummary: {len(results)} PASS, {len(failures)} FAIL out of {len(matches)}")
