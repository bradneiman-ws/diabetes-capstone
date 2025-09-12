from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

UCI_DROP_COLS = [
    # high-cardinality IDs / leakage-like
    "encounter_id","patient_nbr",
    # redundant / free text often missing
    "weight","payer_code","medical_specialty",
]

def _clean_uci(df: pd.DataFrame) -> pd.DataFrame:
    # Replace '?' with NaN (UCI uses '?' for missing)
    df = df.replace("?", np.nan)
    # Drop columns that are mostly missing or IDs
    drop_cols = [c for c in UCI_DROP_COLS if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)
    # Normalize readmitted to binary (within 30 days)
    if "readmitted" in df.columns:
        df["target"] = (df["readmitted"] == "<30").astype(int)
    # Convert 'gender' to simple categories if present
    if "gender" in df.columns:
        df["gender"] = df["gender"].replace({"Unknown/Invalid": np.nan})
    # Map age ranges to midpoints (e.g., [60-70) -> 65)
    if "age" in df.columns and df["age"].astype(str).str.startswith("[").any():
        def to_mid(s):
            try:
                s = s.strip("[]()")
                lo, hi = s.split("-")
                return (int(lo)+int(hi))/2
            except Exception:
                return np.nan
        df["age_mid"] = df["age"].astype(str).map(to_mid)
    # Convert 'A1Cresult'/'max_glu_serum' to ordered categories
    for col in ["A1Cresult","max_glu_serum"]:
        if col in df.columns:
            order = {"None":0, "Norm":1, ">7":2, ">8":3, ">200":2, ">300":3}
            df[col] = df[col].map(order).astype("float")
    # Collapse diagnosis codes to prefixes (e.g., 250.xx -> 250)
    for col in ["diag_1","diag_2","diag_3"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.extract(r"^(\d{3})", expand=False)
    return df

def _clean_pima(df: pd.DataFrame) -> pd.DataFrame:
    # Expect classic Pima schema with 'Outcome' as target
    # Replace zero-as-missing for some columns
    zero_na_cols = ["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]
    for c in zero_na_cols:
        if c in df.columns:
            df[c] = df[c].replace({0: np.nan})
    if "Outcome" in df.columns:
        df["target"] = df["Outcome"].astype(int)
    return df

def load_dataset(csv_path: str, kind: str = "uci_hospitals") -> pd.DataFrame:
    """Load and lightly clean a diabetes dataset.
    - kind='uci_hospitals' for UCI 130-US hospitals (readmission task)
    - kind='pima' for Pima Indians Diabetes
    Returns a DataFrame with a unified 'target' column for modeling.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at {csv_path}. Put your data at ./data/raw/diabetes.csv or pass --csv_path.")
    df = pd.read_csv(path)
    if kind == "uci_hospitals":
        df = _clean_uci(df)
        if "target" not in df.columns:
            raise ValueError("Could not derive 'target' from UCI dataset. Expect a 'readmitted' column.")
    elif kind == "pima":
        df = _clean_pima(df)
        if "target" not in df.columns:
            raise ValueError("Pima dataset missing 'Outcome' to derive 'target'.")
    else:
        raise ValueError("Unknown kind. Use 'uci_hospitals' or 'pima'.")
    return df
