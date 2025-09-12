import pandas as pd

def detect_leakage(df: pd.DataFrame, target: str, id_threshold=0.9, corr_threshold=0.95):
    """Flag columns that may leak target or look like IDs.
    - id-like: unique ratio ~ 1
    - correlation: abs corr with target above threshold
    """
    leaks = []
    n = len(df)
    for col in df.columns:
        if col == target: continue
        uniq_ratio = df[col].nunique() / n
        if uniq_ratio > id_threshold:
            leaks.append((col, f"high uniqueness ratio ({uniq_ratio:.2f})"))
    # correlation check for numeric only
    num_df = df.select_dtypes(include="number")
    if target in num_df.columns:
        corr = num_df.corr()[target].drop(target)
        for c, v in corr.items():
            if abs(v) > corr_threshold:
                leaks.append((c, f"high correlation {v:.2f} with target"))
    return leaks
