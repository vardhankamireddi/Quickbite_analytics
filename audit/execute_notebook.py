import json, os, sys, io, base64, traceback
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

# Set MPLCONFIGDIR to temp folder to avoid permissions issue
temp_dir = tempfile.gettempdir()
os.environ['MPLCONFIGDIR'] = os.path.join(temp_dir, 'matplotlib_qb')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

NB_PATH = "quickbite-analytics/notebooks/01_Data_Cleaning_and_EDA.ipynb"
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Global execution namespace
# The notebook expects os.getcwd() to be notebooks/, so BASE_DIR is '..'
# Let's run from quickbite-analytics/notebooks or set BASE_DIR properly
notebook_dir = os.path.abspath("quickbite-analytics/notebooks")
orig_cwd = os.getcwd()
os.chdir(notebook_dir)

exec_globals = {}
code_cell_idx = 0
executed_count = 0

print(f"Executing notebook: {NB_PATH} (total cells: {len(nb['cells'])})")

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    code_cell_idx += 1
    src = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    
    # Capture stdout
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    
    outputs = []
    cell_error = None
    
    try:
        # Clear any existing plots before running cell
        plt.close('all')
        
        exec(src, exec_globals)
        
        # Check if any plot was generated
        fig_nums = plt.get_fignums()
        for fignum in fig_nums:
            fig = plt.figure(fignum)
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode('utf-8')
            outputs.append({
                "output_type": "display_data",
                "data": {
                    "image/png": img_b64,
                    "text/plain": [f"<Figure size {fig.get_size_inches()[0]*100}x{fig.get_size_inches()[1]*100} with {len(fig.axes)} Axes>"]
                },
                "metadata": {}
            })
            plt.close(fig)
            
    except Exception as e:
        cell_error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        
    captured_text = redirected_output.getvalue()
    if captured_text:
        outputs.insert(0, {
            "output_type": "stream",
            "name": "stdout",
            "text": captured_text.splitlines(keepends=True)
        })
        
    if cell_error:
        print(f"Error in cell {i} (code cell {code_cell_idx}): {cell_error[:150]}")
        outputs.append({
            "output_type": "error",
            "ename": "ExecutionError",
            "evalue": str(cell_error.splitlines()[-1]),
            "traceback": cell_error.splitlines()
        })
    else:
        executed_count += 1
        print(f"Cell {i:2d} (code {code_cell_idx:2d}) executed OK ({len(outputs)} outputs)")
        
    cell['execution_count'] = code_cell_idx
    cell['outputs'] = outputs

os.chdir(orig_cwd)

# Save executed notebook
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"\nExecution complete: {executed_count} of {code_cell_idx} code cells executed successfully.")
