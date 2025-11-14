# src/project_paths.py
from pathlib import Path
import sys

# project root is parent of src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC          = PROJECT_ROOT / "src"
DATA_DIR     = PROJECT_ROOT / "data"
REPORTS_DIR  = PROJECT_ROOT / "reports"
FIGURES_DIR  = REPORTS_DIR / "figures"
TABLES_DIR   = REPORTS_DIR / "tables"

def ensure_src_on_sys_path() -> None:
    """Put src/ at the front of sys.path for local development."""
    s = str(SRC)
    if s not in sys.path:
        sys.path.insert(0, s)  # ahead of site-packages for local dev