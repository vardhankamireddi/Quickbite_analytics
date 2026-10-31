import re

with open('quickbite-analytics/sql/04_analysis_queries.sql', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern matching -- QUERY (\d+): (.*)
matches = list(re.finditer(r'-- QUERY (\d+):\s*([^\n]+)', text))
print(f"Total query matches: {len(matches)}")

queries = []
for i, m in enumerate(matches):
    q_num = int(m.group(1))
    title = m.group(2).strip()
    start_pos = m.end()
    end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
    block = text[start_pos:end_pos]
    
    # Strip comments at the top (like Business Question, etc.)
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
    queries.append({'num': q_num, 'title': title, 'sql': sql_text})

for q in queries:
    print(f"Q{q['num']:02d}: {q['title']:45s} | SQL starts: {q['sql'][:30]}...")

