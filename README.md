[![Run tests](https://github.com/bradneiman-ws/diabetes-capstone/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/bradneiman-ws/diabetes-capstone/actions/workflows/tests.yml?query=branch%3Amain)

[![CI](https://github.com/bradneiman-ws/diabetes-capstone/actions/workflows/ci.yml/badge.svg)](#)

![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

- - -

# Diabetes Capstone (Healthcare Focus)

A production-minded capstone demonstrating **end-to-end ML** on a diabetes dataset (e.g., UCI "Diabetes 130-US hospitals" or Pima Indians). 
It balances **engineering rigor** (tests, repo structure, CI-ready entry points) with **storytelling** (polished Kaggle notebook).

## Quickstart

```bash
conda env create -f environment.yml
conda activate diabetes-capstone

# Put your raw CSV in ./data/raw/diabetes.csv  (or pass --csv_path)
make reproduce
```


## Datasets supported
- **UCI Diabetes 130-US hospitals** (default): predicts 30-day readmission (`target`).
- **Pima Indians Diabetes**: predicts diabetes presence (`target`).

## Subgroup analysis ideas
- Age (use `age_mid` if present), gender, number of inpatient/outpatient visits, medication changes.
- Report metrics across cohorts to surface disparities.


The training step also writes a **leakage report** to `output/leakage_report.json` before fitting.


### Config-driven leakage handling
- `config.yaml` lets you control auto-drop of leakage columns.
- **auto_drop:** if true, any suspected leakage columns are dropped.
- **allowlist:** columns you want to keep even if flagged.
- **denylist:** columns you want to drop regardless.


## Config-driven training
Edit `config.yaml` to control dataset kind and leakage handling:

```yaml
dataset:
  kind: uci_hospitals   # or: pima
leakage:
  auto_drop: true       # auto-drop suspected leaks
  id_threshold: 0.90
  corr_threshold: 0.95
columns:
  drop: ["encounter_id"]  # always drop
  allowlist: ["age"]      # never drop even if flagged
```

CLI overrides config:
```bash
python -m src.train --csv_path data/raw/diabetes.csv --kind pima
```
Outputs include `output/leakage_report.json` and `output/column_drop_report.json`.

## License
This project is licensed under the Apache 2.0 License – see the [LICENSE](LICENSE) file for details.
