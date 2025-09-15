# Capstone Thread Hub – Implementation Tracker

> Single source of truth for planning, tracking, and closing the loops across all ChatGPT threads + your repo.

---

## 0) Project Snapshot (auto‑update weekly)
- **Objective:** Build, evaluate, and present predictive models on the UCI Diabetes dataset (capstone project).
- **Current focus / sprint goal (1–2 weeks):** Establish reproducible repo + core EDA (correlation matrices & pairplots).
- **Dataset(s):** UCI Diabetes Dataset
- **Primary notebook(s):** `eda_correlation.ipynb`, `eda_pairplot.ipynb`
- **Repo URL:** [diabetes-capstone](https://github.com/bradneiman-ws/diabetes-capstone)
- **Owner:** Brad J. Neiman  
- **Dates:** Week of 9/13/25 → ____

---

## 1) Thread Index (permalink each thread)
| ID | Thread Title | Link | Why it exists (1 line) | Status |
|---|---|---|---|---|
| T‑01 | [Correlation like JMP in Python]([url](https://github.com/bradneiman-ws/diabetes-capstone/issues/2)) | [thread link] | Reproduce JMP scatterplot/correlation matrix in Python | In progress |
| T‑02 | [Pairplots in Python]([url](https://github.com/bradneiman-ws/diabetes-capstone/issues/3)) | [thread link] | Learn seaborn pairplot and compare to JMP matrix | In progress |
| T‑03 | Git SSH / repo setup | [thread link] | Set up GitHub repo and SSH key for commits | Open |
| T‑04 | F1 score explanation | [thread link] | Understand F1 for model evaluation | Done |

---

## 2) Decisions Log
| Date | Decision | Options considered | Reasoning | Impact |
|---|---|---|---|---|
| 2025‑09‑14 | Use matplotlib over seaborn for correlation matrix | matplotlib vs seaborn | Cleaner control, matches JMP style | Ensures reproducibility + clarity |
| 2025‑09‑14 | Keep pairplot for comparison | Keep vs drop | Useful visual vs JMP | Adds depth to EDA |

---

## 3) Actionable Backlog (from all threads)
- [ ] **T‑01** · H · code · Brad · DoD: `eda_correlation.ipynb` runs end‑to‑end, outputs correlation scatterplot matrix · Target: 2025‑09‑20
- [ ] **T‑02** · M · code · Brad · DoD: pairplot notebook runs with UCI dataset, documented differences vs JMP · Target: 2025‑09‑20
- [ ] **T‑03** · H · infra · Brad · DoD: repo initialized with README, SSH key working, first commit pushed · Target: 2025‑09‑18
- [ ] **T‑04** · L · doc · Brad · DoD: summary of F1 use in capstone doc · Target: 2025‑09‑22

---

## 4) Sprint Plan (this week)
- [ ] T‑01 → implement correlation scatterplot matrix notebook
- [ ] T‑02 → implement pairplot notebook
- [ ] T‑03 → finalize repo + SSH setup

---

## 5) Routing Table (thread → repo work)
| T‑ID | GitHub Issue | Branch | PR | Merged |
|---|---|---|---|---|
| T‑01 | #1 | `t01-correlation` | #2 | ☐ |
| T‑02 | #3 | `t02-pairplot` | #4 | ☐ |
| T‑03 | #5 | `t03-repo-setup` | #6 | ☐ |

---

## 6) Experiments & Results
| Exp ID | Hypothesis | Dataset/Split | Method | Metric (baseline → result) | Notes |
|---|---|---|---|---|---|
| E‑01 | Baseline logistic regression | UCI train/test 80/20 | LogisticRegression | F1: __ → __ | Baseline to compare future models |

---

## 7) Risks & Blocks
- Risk: Repo setup blocked by SSH error · **Trigger:** Permission denied error persists · **Mitigation:** Generate new SSH key + add to GitHub · **Owner:** Brad

---

## 8) Parking Lot
- Idea: Try alternative viz (heatmap correlation) → Revisit by Week 3
- Idea: Automate correlation + pairplot wrapper → Revisit after baseline EDA

---

## 9) Done / Release Notes
- 2025‑09‑12: Closed T‑04 (no code, doc only). Summary: F1 explanation integrated into project notes.

---

## 10) Copy‑Paste Snippets (for speed)
*(unchanged)*

---

## 11) Weekly Review
- What shipped? → correlation + pairplot notebooks
- What moved the metric? → baseline F1
- What to drop/keep next week? → drop duplicate plots, keep heatmap idea parked
- Bottleneck? → GitHub SSH setup

---

### How to use this hub
*(unchanged)*
