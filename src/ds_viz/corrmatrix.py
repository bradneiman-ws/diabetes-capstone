import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import colors as mcolors
from matplotlib import cm

# --- helper: covariance ellipse ---
def confidence_ellipse(x, y, ax, n_std=2.0, **kwargs):
    x = np.asarray(x); y = np.asarray(y)
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return
    cov = np.atleast_2d(np.cov(x, y))
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * n_std * np.sqrt(vals)
    ellip = Ellipse((np.mean(x), np.mean(y)), width, height,
                    angle=theta, fill=False, **kwargs)
    ax.add_patch(ellip)

# --- main function ---
def scatter_matrix_with_corr(
    df,
    columns=None,
    bins=20,
    s=12,
    alpha=0.6,
    max_vars=None,
    select_strategy="variance",   # "variance" | "first" | "target"
    target=None,
    cell_size_in=2.6,
    # correlation method
    method="pearson",             # "pearson" | "spearman" | "kendall"
    # r-text styling
    cmap_name="RdBu_r",
    color_by_r=True,
    scale_text_by_abs_r=True,
    base_fontsize=12,
    max_fontsize=22,
    show_colorbar=True,
    # diagonals
    diag_hist_sharey=True,
    diag_hist_density=False,
    # standardization
    standardize=False,
    # saving + display
    save_table=None,
    save_fig=None,
    dpi=300,
    show=True,
    # NaN filtering
    min_nonmissing=0.8
):
    """
    Create a JMP-style scatterplot matrix with correlations.

    Features:
      - Pearson, Spearman, or Kendall correlations
      - Automatic numeric column selection
      - NaN filtering (min_nonmissing threshold)
      - Column selection by variance, order, or target correlation
      - Standardization option for comparable scales
      - Colored & scaled correlation coefficients
      - Shared Y-axis on diagonal histograms
      - Saves correlation table (CSV) + figure (PNG/PDF)
    """
    # validate method
    method = method.lower()
    if method not in {"pearson", "spearman", "kendall"}:
        raise ValueError("method must be 'pearson', 'spearman', or 'kendall'")

    # auto-pick numeric columns
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns.tolist()

    # drop columns with too many NaNs
    valid_frac = df[columns].notna().mean()
    columns = [c for c in columns if valid_frac[c] >= min_nonmissing]
    if not columns:
        raise ValueError("No numeric columns meet the non-missing threshold.")

    # selection logic
    if max_vars is not None and len(columns) > max_vars:
        if select_strategy == "variance":
            variances = df[columns].var(numeric_only=True).sort_values(ascending=False)
            columns = variances.head(max_vars).index.tolist()
        elif select_strategy == "first":
            columns = columns[:max_vars]
        elif select_strategy == "target":
            if target is None or target not in df.columns:
                raise ValueError("Must provide a valid target column when using select_strategy='target'")
            corrs = df[columns].corrwith(df[target], method=method).abs().sort_values(ascending=False)
            columns = [target] + [c for c in corrs.index if c != target][:max_vars-1]
        else:
            raise ValueError('select_strategy must be "variance", "first", or "target"')

    n = len(columns)
    if n == 0:
        raise ValueError("No numeric columns found to plot.")

    # prepare data
    data = df[columns].copy()
    if standardize:
        data = (data - data.mean()) / data.std(ddof=0)

    # compute correlation matrix
    corr = data.corr(method=method)
    print(f"{method.capitalize()} correlation matrix:\n", corr.round(3))

    # optional save
    if save_table:
        corr.to_csv(save_table, float_format="%.6f")

    # visuals
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    cmap = plt.colormaps.get_cmap(cmap_name)
    fig, axes = plt.subplots(n, n, figsize=(cell_size_in * n, cell_size_in * n))

    diag_heights, diag_axes = [], []

    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            xi = data[columns[j]]
            yi = data[columns[i]]

            if i == j:
                counts, _, _ = ax.hist(xi.dropna(), bins=bins, density=diag_hist_density)
                diag_heights.append(counts.max() if counts.size else 0)
                diag_axes.append(ax)
                ax.set_ylabel(columns[i] if j == 0 else "")
                ax.set_xlabel(columns[j] if i == n - 1 else "")

            elif i > j:
                ax.scatter(xi, yi, s=s, alpha=alpha)
                confidence_ellipse(xi, yi, ax, n_std=2.0, linewidth=1.5, color='red')
                ax.set_ylabel(columns[i] if j == 0 else "")
                ax.set_xlabel(columns[j] if i == n - 1 else "")

            else:
                r = corr.iloc[i, j]
                color = cmap(norm(r)) if color_by_r else "black"
                fs = base_fontsize + (max_fontsize - base_fontsize) * abs(r) if scale_text_by_abs_r else base_fontsize
                ax.text(0.5, 0.5, f"{r:.2f}", ha='center', va='center', fontsize=fs, color=color)
                ax.set_xticks([]); ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_visible(False)

            if i < n - 1 and not (i == j):
                ax.set_xticklabels([])
            if j > 0 and not (i == j):
                ax.set_yticklabels([])

    # unify diagonal histogram y-scales
    if diag_hist_sharey and diag_heights:
        ymax = max(diag_heights)
        if np.isfinite(ymax) and ymax > 0:
            pad = 0.05 * ymax
            for ax in diag_axes:
                ax.set_ylim(0, ymax + pad)
            ylabel = "Density" if diag_hist_density else "Count"
            axes[0,0].set_ylabel(f"{columns[0]}\n({ylabel}, shared scale)")

    fig.suptitle(f"Scatterplot Matrix with {method.capitalize()} Correlations", y=1.02, fontsize=14)
    plt.tight_layout()

    if show_colorbar and color_by_r:
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=axes.ravel().tolist(),
                            orientation="horizontal", fraction=0.02, pad=0.05)
        cbar.set_label(f"{method.capitalize()} correlation coefficient (r)")

    if save_fig:
        fig.savefig(save_fig, dpi=dpi, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return corr, fig

# --- quick wrapper ---
def quick_corr_plot(
    filepath,
    target=None,
    max_vars=10,
    method="pearson",     # "pearson" | "spearman" | "kendall"
    select_strategy="variance",
    standardize=True,
    min_nonmissing=0.8,
    bins=20,
    show=True
):
    """
    Quick one-liner wrapper around scatter_matrix_with_corr.
    Saves outputs in the SAME directory as the input file.
    Filenames include method and target for easy tracking.
    """
    import os
    import pandas as pd

    # --- Load data ---
    if filepath.lower().endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.lower().endswith((".xls", ".xlsx")):
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Only CSV or Excel supported for now.")

    # --- Build output paths in the input's directory ---
    in_dir  = os.path.dirname(os.path.abspath(filepath)) or "."
    base    = os.path.splitext(os.path.basename(filepath))[0]
    method_suffix = method.lower()
    target_suffix = "" if target is None else "_" + str(target).replace(" ", "").replace("/", "_")

    save_table = os.path.join(in_dir, f"{base}_corr_{method_suffix}{target_suffix}.csv")
    save_fig   = os.path.join(in_dir, f"{base}_scatter_matrix_{method_suffix}{target_suffix}.png")

    # --- Run the full plotter ---
    corr, fig = scatter_matrix_with_corr(
        df,
        target=target,
        max_vars=max_vars,
        select_strategy=select_strategy,
        method=method,
        standardize=standardize,
        min_nonmissing=min_nonmissing,
        bins=bins,
        save_table=save_table,
        save_fig=save_fig,
        show=show
    )

    print(f"✅ Saved correlation matrix to {save_table}")
    print(f"✅ Saved scatterplot matrix to {save_fig}")
    return corr, fig

