# src/io_utils.py
from pathlib import Path
from project_paths import PROJECT_ROOT, DATA_DIR, REPORTS_DIR, FIGURES_DIR, TABLES_DIR

def _safe_mkdir(path: Path) -> Path:
    path = path.resolve()
    if not (PROJECT_ROOT == path or PROJECT_ROOT in path.parents):
        raise AssertionError("Refusing to write outside of project.")
    path.mkdir(parents=True, exist_ok=True)
    return path

def ensure_output_dirs() -> Path:
    _safe_mkdir(REPORTS_DIR)
    _safe_mkdir(FIGURES_DIR)
    _safe_mkdir(TABLES_DIR)

def data_path(*parts: str) -> Path:
    return (DATA_DIR / Path(*parts)).resolve()

def report_path(*parts: str) -> Path:
    return (REPORTS_DIR / Path(*parts)).resolve()

def save_table(df, name: str):
    ensure_output_dirs()
    out = TABLES_DIR / f"{name}.csv"
    df.to_csv(out, index=False)
    return out

def save_fig(fig, name: str):
    ensure_output_dirs()
    out = FIGURES_DIR / f"{name}.png"
    fig.savefig(out, bbox_inches="tight", dpi=150)
    return out