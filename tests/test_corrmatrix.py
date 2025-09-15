import pandas as pd
from ds_viz import scatter_matrix_with_corr, quick_corr_plot

def test_scatter_matrix_runs(tmp_path):
    # Small dummy dataset
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [2, 4, 6, 8, 10],   # perfectly correlated with A
        "C": [5, 4, 3, 2, 1]     # perfectly negatively correlated with A
    })

    # Call function (don’t show plot)
    corr, fig = scatter_matrix_with_corr(df, show=False)

    # Check correlation shape and values
    assert corr.shape == (3, 3)
    assert abs(corr.loc["A", "B"] - 1.0) < 1e-9
    assert abs(corr.loc["A", "C"] + 1.0) < 1e-9

    # Save outputs to tmp dir
    table_path = tmp_path / "corr.csv"
    fig_path = tmp_path / "matrix.png"

    corr, fig = scatter_matrix_with_corr(
        df, show=False,
        save_table=str(table_path),
        save_fig=str(fig_path)
    )

    assert table_path.exists()
    assert fig_path.exists()

def test_quick_corr_plot(tmp_path):
    # Create a temp CSV
    df = pd.DataFrame({
        "X": [10, 20, 30],
        "Y": [1, 2, 3],
        "Z": [3, 2, 1]
    })
    csv_path = tmp_path / "tiny.csv"
    df.to_csv(csv_path, index=False)

    # Run quick_corr_plot
    corr, fig = quick_corr_plot(str(csv_path), show=False)

    # Expected output files
    assert (tmp_path / "tiny_corr_pearson.csv").exists()
    assert (tmp_path / "tiny_scatter_matrix_pearson.png").exists()
