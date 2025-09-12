import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

def subgroup_metrics(df: pd.DataFrame, y_true, y_pred, col: str):
    """Return accuracy/F1 per subgroup value for a categorical column."""
    if col not in df.columns:
        return {}
    results = {}
    for val in sorted(df[col].dropna().unique()):
        mask = df[col] == val
        if mask.sum() < 10:
            continue
        acc = accuracy_score(y_true[mask], y_pred[mask])
        f1 = f1_score(y_true[mask], y_pred[mask], average="binary")
        results[str(val)] = {"n": int(mask.sum()), "accuracy": acc, "f1": f1}
    return results
