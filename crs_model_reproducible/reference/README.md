# Regression reference data

These CSVs were verified against the supplied pre-cleanup scripts.
They contain deterministic simulation results, not biological measurements.

- `reference_figure3-2.csv`: 435 rows of x/y coordinates, three-strain persistence
  and first-loss labels, in the original simplex-grid order.
- `reference_figure3-3.csv`: 18 potency rows x 22 initial-C columns of persistence.

Run `python run_all.py`, then `python tests/check_regression.py`. The check compares
fresh CSV results in `output/` to these files. Do not replace reference results
merely to make a failing comparison pass.
