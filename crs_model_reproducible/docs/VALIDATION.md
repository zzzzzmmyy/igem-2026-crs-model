# Validation scope

Numerical/mechanistic verification, not biological validation.

Environment: Python 3.10.20 on Windows; NumPy 2.2.5, SciPy 1.15.3,
Matplotlib 3.10.9. Date: 2026-10-10, Asia/Shanghai.

Pre-cleanup figure revisions were compared with the supplied original scripts:
12 single-batch curves matched exactly; the 435-point ternary persistence/first-loss
map and 396-condition potency surface also matched exactly. Reference scan data
were retained in `reference/` with their original ordering.

Cleanup verification:

- AST comparison confirmed all three model function bodies are unchanged,
  excluding docstrings. Parameters and original numerical behavior are retained.
- Five unit checks passed: no producer/no toxin; toxin affects S only; finite
  nonnegative batch output; serial fractions/detection; simplex count/coordinates.
- Full post-cleanup figure/CSV reproduction and regression outcome is recorded
  in `REPRODUCTION_RESULT.json` after the run completes.
- Figure presentation was visually checked; English labels and black backgrounds
  were preserved. Any elapsed time recorded is local, not a benchmark against
  other software or biological experiments.

No wet-lab comparison, calibrated parameter inference, stability theorem or
uncertainty quantification was added. Best Software requires the team's broader
evidence in addition to these implementation checks.
