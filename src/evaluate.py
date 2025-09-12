import argparse, json
import pandas as pd
import pyarrow.parquet as pq
from .metrics import classification_metrics
from .utils import save_json
from .threshold import find_best_threshold
from .subgroup import subgroup_metrics

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--pred_path", type=str, required=True)
    p.add_argument("--ytrue_path", type=str, required=True)
    p.add_argument("--report_path", type=str, required=True)
    return p.parse_args()

def main():
    args = parse_args()
    preds = pq.read_table(args.pred_path).to_pandas()
    ytrue = pq.read_table(args.ytrue_path).to_pandas()["y_true"].values
    y_pred = preds["y_pred"].values
    y_prob = preds["y_prob"].values if "y_prob" in preds.columns else None

    metrics = classification_metrics(ytrue, y_pred, y_prob)

    # Threshold tuning (binary only)
    if y_prob is not None and len(set(ytrue))==2:
        thr, score = find_best_threshold(ytrue, y_prob, metric="f1")
        metrics["best_thr_f1"] = thr
        metrics["best_f1"] = score

    # Optionally add subgroup metrics if meta cols present (e.g., gender)
    subgroup_results = {}
    if "gender" in preds.columns:
        subgroup_results["gender"] = subgroup_metrics(preds, ytrue, y_pred, "gender")

    out = {"metrics": metrics, "subgroups": subgroup_results}
    save_json(out, args.report_path)

if __name__ == "__main__":
    main()
