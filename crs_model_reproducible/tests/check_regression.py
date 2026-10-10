"""Check freshly generated CSVs against the original, independently recorded scan results.
Run `python run_all.py` before this check.
"""
import csv
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "output/figure3-2_deterministic_ternary.csv").open(encoding="utf-8", newline="") as stream:
    actual = list(csv.DictReader(stream))
with (ROOT / "reference/reference_figure3-2.csv").open(encoding="utf-8", newline="") as stream:
    reference = list(csv.DictReader(stream))
assert len(actual) == len(reference) == 435
for a, b in zip(actual, reference):
    for key in ("x", "y", "coexistence_passages"):
        assert float(a[key]) == float(b[key]), (key, a, b)
    assert a["first_lost"] == b["first_lost"]
with (ROOT / "output/figure3-3_biodiversity_law.csv").open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
actual_Z = np.array([int(row["coexistence_passages"]) for row in rows]).reshape(18,22)
np.testing.assert_array_equal(actual_Z, np.loadtxt(ROOT / "reference/reference_figure3-3.csv", delimiter=","))
assert len(rows) == 396
print("PASS: all 435 initial-composition results and all 396 potency-scan results match the pre-cleanup code.")
