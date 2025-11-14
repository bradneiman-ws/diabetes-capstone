# tests/test_env.py
from project_paths import PROJECT_ROOT, SRC, ensure_src_on_sys_path

def test_layout():
    assert (PROJECT_ROOT / "src").exists(), "src/ missing at project root"
    assert (PROJECT_ROOT / "notebooks").exists(), "notebooks/ missing at project root"

def test_imports():
    ensure_src_on_sys_path()
    import ds_viz # noqa: F401