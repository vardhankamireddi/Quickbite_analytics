import os, sys
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8')

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'QuickBite Analytics - Master Engineering Audit & Final Report', 0, 1, 'R')
        self.line(10, 18, 200, 18)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDFReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Helvetica', '', 10)

with open('quickbite-analytics/audit/FINAL_PROJECT_EXPLANATION.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace KaTeX / unicode characters that fpdf latin-1 doesn't support
replacements = {
    '₹': 'INR ',
    '—': ' - ',
    '–': ' - ',
    '’': "'",
    '‘': "'",
    '“': '"',
    '”': '"',
    '⭐': '*',
    '✅': '[OK]',
    '⚠️': '[WARN]',
    '🏆': '[TOP]',
    '⏱️': '[TIME]',
    '⚡': '[FAST]',
    '🏷️': '[TAG]',
    'le': '<=',
    'ge': '>=',
}
for k, v in replacements.items():
    text = text.replace(k, v)

lines = text.split('\n')
for line in lines:
    line_clean = line.encode('latin-1', 'replace').decode('latin-1')
    if line_clean.startswith('# '):
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(26, 115, 232)
        pdf.cell(0, 10, line_clean[2:], 0, 1)
        pdf.set_text_color(0, 0, 0)
    elif line_clean.startswith('## '):
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(40, 50, 70)
        pdf.cell(0, 8, line_clean[3:], 0, 1)
        pdf.set_text_color(0, 0, 0)
    elif line_clean.startswith('### '):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 6, line_clean[4:], 0, 1)
        pdf.set_text_color(0, 0, 0)
    elif line_clean.startswith('- '):
        pdf.set_font('Helvetica', '', 9.5)
        pdf.multi_cell(0, 5, '  * ' + line_clean[2:])
    elif line_clean.startswith('|'):
        # Table rows in monospace
        pdf.set_font('Courier', '', 8)
        pdf.cell(0, 4.5, line_clean[:110], 0, 1)
    elif line_clean.strip() == '':
        pdf.ln(2)
    else:
        pdf.set_font('Helvetica', '', 9.5)
        pdf.multi_cell(0, 5, line_clean)

out_pdf = 'quickbite-analytics/audit/FINAL_PROJECT_EXPLANATION.pdf'
pdf.output(out_pdf)
print(f"Generated PDF successfully: {out_pdf} ({os.path.getsize(out_pdf):,} bytes)")
