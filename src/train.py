import argparse
from pathlib import Path
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import pyarrow as pa, pyarrow.parquet as pq

from .presets import load_dataset
from .data import train_valid_test_split
from .features import basic_preprocess
from .utils import save_json
from .leakage import detect_leakage

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--csv_path", type=str, required=True, help="Path to input CSV.")
    p.add_argument("--kind", type=str, default=None, choices=["uci_hospitals","pima"], help="Dataset kind (overrides config).")
    p.add_argument("--output_dir", type=str, default="output", help="Where to write predictions and artifacts.")
    p.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config.")
    return p.parse_args()

def load_config(path: str):
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("r") as f:
        return yaml.safe_load(f) or {}

def main():
    args = parse_args()
    cfg = load_config(args.config)

    # Resolve dataset kind: CLI arg wins, else config, else default
    kind = args.kind or cfg.get("dataset", {}).get("kind", "uci_hospitals")

    df = load_dataset(args.csv_path, kind=kind)
    target = "target"
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found after loading. Columns include: {list(df.columns)[:10]} ...")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- Leakage detection BEFORE splitting ----
    id_thr = cfg.get("leakage", {}).get("id_threshold", 0.90)
    corr_thr = cfg.get("leakage", {}).get("corr_threshold", 0.95)
    leaks = detect_leakage(df.copy(), target=target, id_threshold=id_thr, corr_threshold=corr_thr)
    leak_report = [{"column": c, "reason": r} for (c, r) in leaks]
    save_json({"suspected_leaks": leak_report}, outdir/"leakage_report.json")

    # Determine columns to drop based on config
    config_drops = set(cfg.get("columns", {}).get("drop", []) or [])
    allowlist = set(cfg.get("columns", {}).get("allowlist", []) or [])
    auto_drop = bool(cfg.get("leakage", {}).get("auto_drop", False))

    detected_cols = set([x["column"] for x in leak_report])
    drops = set(config_drops)
    if auto_drop:
        drops.update(detected_cols - allowlist)

    # Apply drops (but never drop target)
    drops.discard(target)
    applied_drops = [c for c in df.columns if c in drops]
    if applied_drops:
        df = df.drop(columns=applied_drops, errors="ignore")

    save_json({
        "applied_drops": applied_drops,
        "config_drops": list(config_drops),
        "auto_drop": auto_drop,
        "allowlist": list(allowlist)
    }, outdir/"column_drop_report.json")

    # ---- Split and fit ----
    (X_train, y_train), (X_valid, y_valid), (X_test, y_test) = train_valid_test_split(df, target=target)
    full = pd.concat([X_train, X_valid, X_test], axis=0)
    pipeline = Pipeline([
        ("pre", basic_preprocess(full)),
        ("clf", LogisticRegression(max_iter=200))
    ])

    # CV sanity
    try:
        cv = cross_val_score(pipeline, X_train, y_train, cv=3, scoring="roc_auc")
        cv_scores = {"cv_roc_auc_mean": float(cv.mean()), "cv_roc_auc_std": float(cv.std())}
    except Exception:
        cv_scores = {}

    pipeline.fit(X_train, y_train)

    # Predict
    y_pred = pipeline.predict(X_test)
    try:
        y_prob = pipeline.predict_proba(X_test)[:, 1]
    except Exception:
        y_prob = None

    # Save outputs
    pq.write_table(pa.Table.from_pandas(pd.DataFrame({"y_true": y_test})), outdir/"y_true.parquet")
    dfp = {"y_pred": y_pred}
    if y_prob is not None:
        dfp["y_prob"] = y_prob
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(dfp)), outdir/"preds.parquet")
    save_json(cv_scores, outdir/"cv_scores.json")

if __name__ == "__main__":
    main()
