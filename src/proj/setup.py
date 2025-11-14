# src/proj/setup.py
from project_paths import PROJECT_ROOT, ensure_src_on_sys_path

def setup_notebook():
    """Standard setup block for all notebooks."""
    # Ensure /src is importable
    ensure_src_on_sys_path()

    # Auto-reload extensions (for Jupyter)
    try:
        get_ipython().run_line_magic("load_ext", "autoreload")
        get_ipython().run_line_magic("autoreload", "2")
    except Exception:
        pass # safely ignored if outside Jupyter

    print("✅ Notebook setup complete.")
    print("Project root:", PROJECT_ROOT)