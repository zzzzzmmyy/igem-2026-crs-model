"""Figure 3-2: initial-ratio maps for the deterministic serial-dilution model.

The original 28-division simplex, 60 passages, extinction threshold and
first-loss classification are unchanged. Only figure presentation is revised.
"""

import argparse
import csv
from pathlib import Path

import mplconfig
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from model import DEFAULT_PARAMS, simulate_serial_dilution
from ternary_utils import SQRT3_2, bary_to_xy, simplex_grid


N_CYCLES = 60
GRID_DIVISIONS = 28
OUTPUT_STEM = "figure3-2_deterministic_ternary"
BACKGROUND = "#000000"
FOREGROUND = "#E8ECF1"
MUTED = "#ABB4C0"
COLORS = {"C": "#F3AC69", "R": "#76B7F2", "S": "#79D3AF", "none": "#C4A1ED"}
STYLE = {
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 11,
    "text.color": FOREGROUND,
    "axes.facecolor": BACKGROUND,
    "figure.facecolor": BACKGROUND,
    "savefig.facecolor": BACKGROUND,
    "axes.labelcolor": FOREGROUND,
    "axes.edgecolor": "#67717E",
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "svg.fonttype": "none",
}


def compute_results():
    """Retain the original simulation and persistence/classification logic."""
    xs, ys, persistence, first_lost = [], [], [], []
    grid = simplex_grid(GRID_DIVISIONS)
    for index, (rC, rR, rS) in enumerate(grid, start=1):
        if rC + rR + rS == 0:
            continue
        _, ext = simulate_serial_dilution((rC, rR, rS), n_cycles=N_CYCLES,
                                         params=DEFAULT_PARAMS)
        cycles = {k: (v if v is not None else N_CYCLES + 1) for k, v in ext.items()}
        first = min(cycles, key=cycles.get)
        pers = cycles[first] - 1
        x, y = bary_to_xy(rC, rR, rS)
        xs.append(x)
        ys.append(y)
        persistence.append(min(pers, N_CYCLES))
        first_lost.append(first if cycles[first] <= N_CYCLES else "none")
        if index % 50 == 0 or index == len(grid):
            print(f"Simulated {index}/{len(grid)} initial compositions", flush=True)
    return tuple(np.array(values) for values in (xs, ys, persistence, first_lost))


def draw_frame(ax):
    """Local English frame; shared ternary utilities and other figures stay intact."""
    ax.plot([0, 1, 0.5, 0], [0, 0, SQRT3_2, 0], color="#ABB4C0",
            linewidth=0.85, zorder=3)
    ax.text(0.5, SQRT3_2 + 0.045, "C (colicin producer)", ha="center", va="bottom")
    ax.text(0, -0.055, "R (resistant)", ha="center", va="top")
    ax.text(1, -0.055, "S (sensitive)", ha="center", va="top")
    ax.set_xlim(-0.14, 1.14)
    ax.set_ylim(-0.105, SQRT3_2 + 0.105)
    ax.set_aspect("equal")
    ax.axis("off")


def create_figure(results):
    xs, ys, persistence, first_lost = results
    with plt.rc_context(STYLE):
        fig = plt.figure(figsize=(12.8, 7.4))
        axes = [fig.add_axes((0.035, 0.22, 0.445, 0.575)),
                fig.add_axes((0.52, 0.22, 0.445, 0.575))]
        for ax in axes:
            draw_frame(ax)

        # Lift the low end of viridis for visibility on black; keep the 0-60 scale.
        cmap = ListedColormap(plt.get_cmap("viridis")(np.linspace(0.18, 1, 256)))
        dots = axes[0].scatter(xs, ys, c=persistence, cmap=cmap, s=32,
                               vmin=0, vmax=N_CYCLES, linewidths=0, zorder=2)
        colorbar_ax = fig.add_axes((0.105, 0.145, 0.305, 0.024))
        colorbar = fig.colorbar(dots, cax=colorbar_ax, orientation="horizontal",
                               ticks=np.arange(0, N_CYCLES + 1, 10))
        colorbar.set_label("Three-strain coexistence (passages)", labelpad=8, fontsize=10)
        colorbar.outline.set_visible(False)
        colorbar.ax.tick_params(labelsize=9, length=3)

        labels = {"C": "C lost first", "R": "R lost first", "S": "S lost first",
                  "none": f"No loss within {N_CYCLES} passages"}
        for strain in ("C", "R", "S", "none"):
            mask = first_lost == strain
            if mask.any():
                axes[1].scatter(xs[mask], ys[mask], color=COLORS[strain], s=32,
                                label=labels[strain], linewidths=0, zorder=2)
        handles, legend_labels = axes[1].get_legend_handles_labels()
        fig.legend(handles, legend_labels, loc="upper center",
                   bbox_to_anchor=(0.7425, 0.18), ncol=3 if len(handles) <= 3 else 2, frameon=False,
                   columnspacing=1.4, handletextpad=0.4, fontsize=10)

        fig.suptitle("Initial composition shapes coexistence", y=0.965, fontsize=17)
        fig.text(0.5, 0.91, "Deterministic serial dilution in well-mixed culture | 60 passages",
                 ha="center", color=MUTED, fontsize=11)
        fig.text(0.065, 0.827, "A", fontsize=13, fontweight="bold")
        fig.text(0.095, 0.827, "Coexistence duration", fontsize=12)
        fig.text(0.55, 0.827, "B", fontsize=13, fontweight="bold")
        fig.text(0.58, 0.827, "First strain lost", fontsize=12)
    return fig


def main(output_dir=None):
    output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = compute_results()
    with (output_dir / f"{OUTPUT_STEM}.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("r_C", "r_R", "r_S", "x", "y", "coexistence_passages", "first_lost"))
        for ratio, x, y, persistence, first in zip(simplex_grid(GRID_DIVISIONS), *results):
            writer.writerow((*ratio, x, y, int(persistence), first))
    fig = create_figure(results)
    try:
        with plt.rc_context(STYLE):
            for extension in ("png", "svg"):
                output = output_dir / f"{OUTPUT_STEM}.{extension}"
                fig.savefig(output, dpi=300, facecolor=BACKGROUND, transparent=False)
                print(f"Saved {output}", flush=True)
    finally:
        plt.close(fig)
    persistence = results[2]
    print("median persistence:", np.median(persistence), "max:", persistence.max())
    print("fraction with persistence >= 30 cycles:", (persistence >= 30).mean())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Override the output directory.")
    main(parser.parse_args().output_dir)
