# paths.py
from pathlib import Path

def _find_project_root() -> Path:
    """Locate the project root (one level above /notebooks)."""
    cwd = Path.cwd().resolve()
    if "notebooks" in cwd.parts:
        return Path(*cwd.parts[:cwd.parts.index("notebooks")])
    return cwd

PROJECT_ROOT = _find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create only top-level folders if missing
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def data_path(*parts: str) -> Path:
    """Always point to top-level data folder."""
    return (DATA_DIR / Path(*parts)).resolve()

def report_path(*parts: str) -> Path:
    """Always point to top-level reports folder."""
    return (REPORTS_DIR / Path(*parts)).resolve()

def print_layout():
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DATA_DIR    : {DATA_DIR}")
    print(f"REPORTS_DIR : {REPORTS_DIR}")