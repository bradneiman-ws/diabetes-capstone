"""
Audit notebook and Python files for hardcoded 'Path("reports")' or 'Path("data")' calls.
Run with: python -m utils.audit_paths
"""
import re, os
from pathlib import Path

def find_hardcoded_paths(root="."):
    bad = []
    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith(".ipynb", ".py"):
                p = Path(root) / f
                s = p.read_text(errors="ignore")
                if re.search(r'Path\(\s*["\']reports', s) or re.search(r'Path\(\s*["\']data', s):
                    bad.append(str(p))
    return bad

if __name__ == "__main__":
    bad = find_hardcoded_paths(".")
    if bad:
        print("⚠️ Found hardcoded paths in:")
        for b in bad:
            print(" ", b)
    else:
        print("✅ No hardcoded 'Path(\"reports\")' or 'Path(\"data\")' found.")