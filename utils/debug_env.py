# src/utilities/debug_env.py
"""
Environment diagnostics and repair helpers for Jupyter notebooks.

Usage (from any notebook):
    from utilities.debug_env import diagnose_environment
    diagnose_environment()

This prints out:
  • Active Python interpreter path
  • sys.path summary (whether /src is included)
  • Installed editable packages
  • Discovery results for specific modules (proj, project_paths, etc.)
"""

import sys
import pathlib
import pkgutil
import inspect
import subprocess
import shlex

def diagnose_environment(targets=("proj", "project_paths")):
    print("🐍 Python executable:", sys.executable)
    print("Python version:", sys.version)
    print()

    # Check sys.path
    src_entries = [p for p in sys.path if "src" in p]
    print("📁 sys.path entries containing 'src':")
    for p in src_entries:
        print("   ", p)
    if not src_entries:
        print("   (no src/ in sys.path!)")
    print()

    # Confirm pyproject location
    here = pathlib.Path.cwd().resolve()
    root = here
    while not (root / "pyproject.toml").exists() and root != root.parent:
        root = root.parent
    if (root / "pyproject.toml").exists():
        print("🧭 pyproject.toml found at:", root)
    else:
        print("⚠️ pyproject.toml not found above", here)
    print()

    # List installed editable packages
    print("📦 Installed packages matching editable installs:")
    subprocess.call(shlex.split(f'"{sys.executable}" -m pip list --editable'))
    subprocess.call(shlex.split(f'"{sys.executable}" -m pip list --editable'))
    print()

    # Try importing target modules
    for name in targets:
        print(f"🔍 Checking import for '{name}':")
        try:
            mod = __import__(name)
            print(f"   ✅ Found → {inspect.getfile(mod)}")
        except Exception as e:
            print(f"   ❌ Import failed: {e!r}")
    print()

    print("✅ Diagnostic complete.")


def reinstall_editable(root=None):
    """Force a clean editable reinstall using the current interpreter."""
    import subprocess, shlex
    if root is None:
        root = pathlib.Path.cwd().resolve()
        while not (root / "pyproject.toml").exists() and root != root.parent:
            root = root.parent
    if not (root / "pyproject.toml").exists():
        raise FileNotFoundError("No pyproject.toml found above", pathlib.Path.cwd())
    print("🛠  Reinstalling editable from:", root)
    subprocess.check_call(shlex.split(f'"{sys.executable}" -m pip install -e "{root}"'))
    print("✅ Reinstall complete. Restart kernel.")
