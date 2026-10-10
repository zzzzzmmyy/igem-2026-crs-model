"""Figure 3-3: the well-mixed biodiversity-law parameter scan.

Preserve the original 22 x 18 scan, 40 passages and extinction metric.
Only presentation, English labels and output management are revised.
"""

import argparse
import csv
from pathlib import Path

import mplconfig
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator

from model import DEFAULT_PARAMS, simulate_serial_dilution


N_CYCLES = 40
RC_VALUES = np.linspace(0.01, 0.5, 22)
POTENCY_VALUES = np.linspace(0.5, 10, 18)
OUTPUT_STEM = "figure3-3_biodiversity_law"
BACKGROUND = "#000000"
FOREGROUND = "#E8ECF1"
MUTED = "#ABB4C0"
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
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "mathtext.fontset": "dejavusans",
    "svg.fonttype": "none",
}


def compute_results():
    """Run the unchanged original parameter scan and persistence calculation."""
    Z = np.zeros((len(POTENCY_VALUES), len(RC_VALUES)))
    for i, pot in enumerate(POTENCY_VALUES):
        params = dict(DEFAULT_PARAMS)
        params["kappa"] = pot
        params["kill"] = pot
        for j, rC in enumerate(RC_VALUES):
            rR = rS = (1 - rC) / 2
            _, ext = simulate_serial_dilution((rC, rR, rS), n_cycles=N_CYCLES,
                                             params=params)
            cycles = {k: (v if v is not None else N_CYCLES + 1) for k, v in ext.items()}
            pers = min(cycles.values()) - 1
            Z[i, j] = min(pers, N_CYCLES)
        print(f"Simulated {(i + 1) * len(RC_VALUES)}/{Z.size} parameter combinations",
              flush=True)
    return Z


def create_figure(Z):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(9.5, 7.3))
        fig.subplots_adjust(left=0.115, right=0.795, bottom=0.175, top=0.805)
        cmap = ListedColormap(plt.get_cmap("viridis")(np.linspace(0.18, 1, 256)))
        # Keep the original automatic normalization and unsmoothed sample cells.
        heatmap = ax.pcolormesh(RC_VALUES, POTENCY_VALUES, Z, shading="auto",
                               cmap=cmap, rasterized=False)
        colorbar_ax = fig.add_axes((0.83, 0.175, 0.024, 0.63))
        colorbar = fig.colorbar(heatmap, cax=colorbar_ax)
        colorbar.set_label("Three-strain coexistence (passages)", labelpad=13, fontsize=11)
        colorbar.locator = MaxNLocator(nbins=6, integer=True)
        colorbar.update_ticks()
        colorbar.outline.set_visible(False)
        colorbar.ax.tick_params(length=3, labelsize=10)

        contours = ax.contour(RC_VALUES, POTENCY_VALUES, Z, levels=[5, 15],
                              colors=FOREGROUND, linewidths=1.15)
        contour_labels = ax.clabel(contours, fmt=lambda value: f"{value:g} passages",
                                   fontsize=9, inline=True, inline_spacing=7)
        for label in contour_labels:
            label.set_path_effects([path_effects.withStroke(linewidth=2.5,
                                                           foreground="#18212B")])
        ax.set_xlabel(r"Initial producer fraction, $r_C$", labelpad=11)
        ax.set_ylabel(r"Toxin potency, $p$ (a.u.)", labelpad=12)
        ax.set_xticks(np.arange(0, 0.51, 0.1))
        ax.set_yticks(np.arange(2, 11, 2))
        ax.tick_params(length=3, width=0.8, pad=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.suptitle("Biodiversity law", y=0.96, fontsize=17)
        fig.text(0.5, 0.905, "Well-mixed serial dilution | 40 passages",
                 ha="center", fontsize=11, color=MUTED)
        # The scan sets both parameters to p; its vertical coordinate is not their product.
        fig.text(0.455, 0.055, r"$r_R = r_S = (1-r_C)/2$    |    $\kappa = k_{\mathrm{kill}} = p$",
                 ha="center", fontsize=10, color=MUTED)
    return fig


def main(output_dir=None):
    output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    Z = compute_results()
    with (output_dir / f"{OUTPUT_STEM}.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("r_C", "r_R", "r_S", "potency_p", "kappa", "kill", "coexistence_passages"))
        for i, pot in enumerate(POTENCY_VALUES):
            for j, rC in enumerate(RC_VALUES):
                writer.writerow((rC, (1-rC)/2, (1-rC)/2, pot, pot, pot, int(Z[i, j])))
    fig = create_figure(Z)
    try:
        with plt.rc_context(STYLE):
            for extension in ("png", "svg"):
                output = output_dir / f"{OUTPUT_STEM}.{extension}"
                fig.savefig(output, dpi=300, facecolor=BACKGROUND, transparent=False)
                print(f"Saved {output}", flush=True)
    finally:
        plt.close(fig)
    print(f"Coexistence range: {Z.min():g}-{Z.max():g} passages across {Z.size} conditions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Override the output directory.")
    main(parser.parse_args().output_dir)
