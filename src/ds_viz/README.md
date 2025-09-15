ds_viz

Reusable visualization helpers for Data Sci – Learning.
Main feature: a JMP-style scatterplot matrix with correlations.

✨ Features

Correlation methods: Pearson, Spearman, Kendall

Selection strategies: first N, highest variance, or top correlated with a target variable

Handles missing data (drops NaN-heavy columns automatically)

Standardization option for comparable axes (z-scores)

Diagonal histograms (counts or density, shared Y-axis scale)

Correlation coefficients in upper triangle:

colored by sign (blue ↔ red)

scaled by strength (font size grows with |r|)

Covariance ellipses in scatterplots

Exports both:

CSV correlation table

PNG/PDF scatterplot matrix figure

📦 Installation (development mode)

From repo root:

python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows

pip install -e .

🚀 Usage
Quick one-liner
from ds_viz import quick_corr_plot

# CSV or Excel file → saves outputs automatically
quick_corr_plot("data/diabetes.csv", target="Outcome", max_vars=8, method="spearman")


Produces:

diabetes_corr_spearman_Outcome.csv

diabetes_scatter_matrix_spearman_Outcome.png

Full control
import pandas as pd
from ds_viz import scatter_matrix_with_corr

df = pd.read_csv("data/diabetes.csv")

corr, fig = scatter_matrix_with_corr(
    df,
    method="spearman",
    select_strategy="target",
    target="Outcome",
    max_vars=8,
    standardize=True,
    diag_hist_density=True,
    save_table="pima_corr.csv",
    save_fig="pima_scatter_matrix.png"
)

Other examples
# Pearson, first 6 numeric columns
quick_corr_plot("mydata.csv", max_vars=6, select_strategy="first", method="pearson")

# Kendall, stricter NaN filter, silent batch run
quick_corr_plot("mydata.xlsx", method="kendall", min_nonmissing=0.95, show=False)

# Variance-based selection (default), save as PDF
import pandas as pd
df = pd.read_csv("mydata.csv")
scatter_matrix_with_corr(df, max_vars=8, select_strategy="variance",
                         method="pearson", save_fig="custom_matrix.pdf")

🛠 Troubleshooting

Module not found
Ensure you ran pip install -e . inside the right environment.
Check your notebook kernel matches that environment.

Dependencies missing
Re-run:

pip install -e .


No numeric columns left
Your dataset may have too many NaNs. Relax min_nonmissing (default = 0.8).

Need to reload changes
In notebooks, enable auto-reload:

%load_ext autoreload
%autoreload 2

📖 License

MIT — use freely, attribute if you share.
