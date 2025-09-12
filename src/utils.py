import json
from pathlib import Path

def save_json(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        json.dump(obj, f, indent=2)

def _parse_args_quick():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--metrics_path", type=str, required=True)
    p.add_argument("--out_path", type=str, required=True)
    return p.parse_args()

def _plot_metrics(metrics, out_path):
    import matplotlib.pyplot as plt
    keys = list(metrics.keys())
    vals = [metrics[k] for k in keys]
    plt.figure()
    plt.bar(keys, vals)
    plt.title("Baseline Metrics")
    plt.ylabel("Score")
    plt.xticks(rotation=45, ha="right")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)

def quick_plot():
    import json
    args = _parse_args_quick()
    with open(args.metrics_path) as f:
        metrics = json.load(f)
    _plot_metrics(metrics, args.out_path)

if __name__ == "__main__":
    quick_plot()
