# C:R:S Application Model

Team: ShanghaiTech-China, iGEM 2026. This package supports the well-mixed
C:R:S competition analysis described in the **Model** section.

## Files

- `data/`: A record of illustrative simulation parameters; there are no raw
  experimental measurements in this module. The JSON records the constants in
  `src/`, rather than acting as a runtime configuration file.
- `src/`: Original ODE/serial-passage solver, simplex utilities and three plotting scripts.
- `reference/`: Original numerical scan results used to check reproducibility.
- `figures/`: PNG and SVG files for the three final figures, included in the repository.
- `run_all.py`: Runs the three analyses in sequence and copies final images to `figures/`.
- `requirements.txt`: Python dependency versions used for verification.
- `tests/`: Mechanistic checks and complete-grid regression verification.
- `docs/` and `LICENSE`: Model assumptions, provenance, validation, Wiki draft and licenses.


## Reproduction Steps (Windows)

Verification uses Python 3.10.20. Install Python 3.10, open a terminal in the
directory containing this file, and run:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_all.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/check_regression.py
```

Activation is unnecessary. If `py` is unavailable, replace `py -3.10` in the first
line with the path to your Python 3.10 executable. On macOS/Linux use
`python3.10 -m venv .venv` and `.venv/bin/python` for the remaining commands.
Initial dependency installation needs the internet; simulations and checks then
run locally. Full reproduction takes several minutes on the verified machine.

## Outputs

Images and CSV results are generated in `output/`. Final images are also copied to
`figures/`:

```text
figure3-1_trajectories.png / .svg
figure3-2_deterministic_ternary.png / .svg
figure3-3_biodiversity_law.png / .svg
```

The three corresponding CSVs contain time trajectories, the ternary persistence
map, and the potency scan, respectively. `output/` and environment/cache files are
excluded from Git; the final PNG/SVG files are retained, matching the reference repository.

For one figure, run `python run_all.py --figure 3-1` (or `3-2`, `3-3`). The scripts
resolve their source paths independently of the terminal's working directory.
CSV results and Python model functions can be used by other analysis workflows.

The regression script should print `PASS`. It checks all **435** initial
compositions and **396** potency conditions against the unchanged reference
results. Persistence counts and loss labels must match; the implementation uses
the same default SciPy solver settings as the original code. Image byte equality
is not required across different environments.


