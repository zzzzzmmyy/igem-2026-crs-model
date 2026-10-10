"""Figure 3-1: single-batch trajectories with a dark, English-only layout.

The model, initial densities and 30-hour simulation are unchanged.
Run this script directly; outputs default to the output directory.
"""

import argparse
import csv
from pathlib import Path

import mplconfig
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from model import DEFAULT_PARAMS, simulate_batch


OUTPUT_STEM = "figure3-1_trajectories"
BACKGROUND = "#000000"
FOREGROUND = "#E8ECF1"
MUTED = "#ABB4C0"

# Initial densities are listed in C:R:S order; the solver expects C:S:R.
RATIOS = (
    ("Equal inoculum", "1:1:1", (0.01 / 3, 0.01 / 3, 0.01 / 3)),
    ("High producer", "5:1:1", (0.01 * 5 / 7, 0.01 / 7, 0.01 / 7)),
    ("Low producer", "0.1:1:1", (0.01 * 0.1 / 2.1, 0.01 / 2.1, 0.01 / 2.1)),
    ("Very low producer", "0.02:1:1", (0.01 * 0.02 / 2.02, 0.01 / 2.02, 0.01 / 2.02)),
)

# Bright colors and distinct line styles remain legible on a black wiki.
STRAINS = (
    ("C (colicin producer)", "#F3AC69", "-"),
    ("R (colicin resistant)", "#76B7F2", "--"),
    ("S (colicin sensitive)", "#79D3AF", "-."),
)

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
    "axes.linewidth": 0.8,
    "axes.titleweight": "normal",
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.color": "#56606E",
    "grid.linewidth": 0.6,
    "svg.fonttype": "none",
}


def create_figure():
    """Plot the original four scenarios without changing model calculations."""
    with plt.rc_context(STYLE):
        fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey=True)
        fig.subplots_adjust(left=0.095, right=0.98, bottom=0.09, top=0.79,
                            hspace=0.34, wspace=0.13)

        for panel, ax, (label, ratio, (c0, r0, s0)) in zip("ABCD", axes.flat, RATIOS):
            sol = simulate_batch((c0, s0, r0), t_max=30, params=DEFAULT_PARAMS)
            C, S, R, T = sol.y
            total = C + S + R
            for values, (legend, color, linestyle) in zip((C, R, S), STRAINS):
                ax.plot(sol.t, values / total, color=color, linestyle=linestyle,
                        label=legend, linewidth=2.2)

            ax.set_title(f"{label}  |  C:R:S = {ratio}", loc="left", fontsize=11, pad=11)
            ax.text(-0.065, 1.045, panel, transform=ax.transAxes,
                    fontsize=12, fontweight="bold", ha="right", va="bottom")
            ax.set_xlim(0, 30)
            ax.set_ylim(-0.02, 1.02)
            ax.xaxis.set_major_locator(MultipleLocator(5))
            ax.yaxis.set_major_locator(MultipleLocator(0.2))
            ax.set_axisbelow(True)
            ax.grid(axis="y", alpha=0.28)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.tick_params(length=3, width=0.8, pad=5)

        for ax in axes[1]:
            ax.set_xlabel("Time (h)", labelpad=9)
        for ax in axes[:, 0]:
            ax.set_ylabel("Relative abundance", labelpad=10)

        fig.suptitle("Single-batch dynamics in well-mixed culture", y=0.965, fontsize=17)
        fig.text(0.5, 0.915, "Effect of initial C:R:S composition",
                 ha="center", color=MUTED, fontsize=11)
        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.884),
                   ncol=3, frameon=False, handlelength=3.2, columnspacing=2.4, fontsize=10)
    return fig


def main(output_dir=None):
    """Save CSV data, a 300 dpi PNG and an editable vector SVG."""
    output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / f"{OUTPUT_STEM}.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("initial_ratio_C_R_S", "time_model_units", "C_fraction", "R_fraction", "S_fraction"))
        for _, ratio, (c0, r0, s0) in RATIOS:
            sol = simulate_batch((c0, s0, r0), t_max=30, params=DEFAULT_PARAMS)
            C, S, R, T = sol.y
            total = C + S + R
            writer.writerows(zip([ratio] * len(sol.t), sol.t, C / total, R / total, S / total))
    fig = create_figure()
    try:
        with plt.rc_context(STYLE):
            for extension in ("png", "svg"):
                output = output_dir / f"{OUTPUT_STEM}.{extension}"
                fig.savefig(output, dpi=300, facecolor=BACKGROUND, transparent=False)
                print(f"Saved {output}")
    finally:
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Override the output directory.")
    main(parser.parse_args().output_dir)
