"""Reproduce the C:R:S application module and its three final figures."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", choices=("all", "3-1", "3-2", "3-3"), default="all")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.setdefault("MPLCONFIGDIR", str(output / ".mplconfig"))
    environment.setdefault("PYTHONIOENCODING", "utf-8")
    scripts = {"3-1": "fig1_trajectories.py", "3-2": "fig2_deterministic_ternary.py",
               "3-3": "fig3_biodiversity_law.py"}
    stems = {"3-1": "figure3-1_trajectories", "3-2": "figure3-2_deterministic_ternary",
             "3-3": "figure3-3_biodiversity_law"}
    start = time.perf_counter()
    (ROOT / "figures").mkdir(exist_ok=True)
    for number, filename in scripts.items():
        if args.figure in ("all", number):
            subprocess.run([sys.executable, str(ROOT / "src" / filename),
                            "--output-dir", str(output)], cwd=ROOT, env=environment, check=True)
            for extension in ("png", "svg"):
                source = output / f"{stems[number]}.{extension}"
                destination = ROOT / "figures" / source.name
                if source.resolve() != destination.resolve():
                    shutil.copy2(source, destination)
    print(f"Reproduction complete in {time.perf_counter()-start:.1f} seconds. "
          f"Figures: {ROOT / 'figures'}; analysis outputs: {output}.", flush=True)


if __name__ == "__main__":
    main()
