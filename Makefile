.PHONY: train evaluate reproduce test

PY := python

train:
	$(PY) -m src.train --csv_path data/raw/diabetes.csv --kind uci_hospitals --output_dir output

evaluate:
	$(PY) -m src.evaluate --pred_path output/preds.parquet --ytrue_path output/y_true.parquet --report_path output/metrics.json

reproduce: train evaluate
	$(PY) -m src.utils.quick_plot --metrics_path output/metrics.json --out_path reports/figures/baseline_metrics.png

test:
	pytest -q
