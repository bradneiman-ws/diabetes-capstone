from pathlib import Path
import pandas as pd

def load_csv(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at {csv_path}. Put your data at ./data/raw/diabetes.csv or pass --csv_path.")
    return pd.read_csv(path)

def train_valid_test_split(df, target, seed=42, valid_size=0.2, test_size=0.2):
    from sklearn.model_selection import train_test_split
    y = df[target]
    X = df.drop(columns=[target])
    strat = y if y.nunique()<=20 else None
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=seed, stratify=strat)
    rel_valid = valid_size / (1 - test_size)
    strat_temp = y_temp if y_temp.nunique()<=20 else None
    X_train, X_valid, y_train, y_valid = train_test_split(X_temp, y_temp, test_size=rel_valid, random_state=seed, stratify=strat_temp)
    return (X_train, y_train), (X_valid, y_valid), (X_test, y_test)
