# src/_env_setup.py
from project_paths import PROJECT_ROOT, ensure_src_on_sys_path

def core_env_setup(verbose: bool = True):
    """Core environment setup shared by notebooks and scripts."""
    ensure_src_on_sys_path()
    if verbose:
        print("✅ Environment initialized.")
        print("Project root:", PROJECT_ROOT)
    return PROJECT_ROOT