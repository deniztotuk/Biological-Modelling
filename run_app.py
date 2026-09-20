#!/usr/bin/env python3
"""
Launcher for the Biological Modelling Desktop Application.
Usage:
    python run_app.py                  # Launch desktop GUI
    python run_app.py --export-sample  # Headless sample JPEG export for testing
"""

import sys
import os
import argparse

# Ensure writable matplotlib cache dir
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_cache"))


def run_gui(default_theme: str = "light"):
    from PyQt6.QtWidgets import QApplication
    from bio_models.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("BioModel Studio")
    app.setOrganizationName("Ecology & Evolution Labs")

    window = MainWindow(default_theme=default_theme)
    window.show()

    sys.exit(app.exec())


def export_sample():
    """Headless simulation and export of sample JPEG images in both Light and Dark themes."""
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive headless backend
    import matplotlib.pyplot as plt
    import numpy as np

    from bio_models.models import (
        LotkaVolterraCompetitionModel,
        LotkaVolterraPredatorPreyModel,
        RosenzweigMacArthurModel,
    )
    from bio_models.engine import simulate_model
    from bio_models.ui.styles import get_plot_colors

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)

    samples = [
        ("competition_coexistence_light.jpeg", LotkaVolterraCompetitionModel(), (25, 20), {"r1": 0.8, "r2": 0.7, "K1": 100, "K2": 100, "alpha12": 0.45, "alpha21": 0.40}, "light"),
        ("predator_prey_cycles_light.jpeg", LotkaVolterraPredatorPreyModel(), (30, 10), {"r": 0.9, "a": 0.05, "c": 0.4, "epsilon": 0.5, "delta": 0.25}, "light"),
        ("rosenzweig_macarthur_dark.jpeg", RosenzweigMacArthurModel(), (40, 15), {"r": 1.2, "K": 140, "a": 0.8, "c": 0.9, "b": 25.0, "epsilon": 0.45, "delta": 0.22}, "dark"),
    ]

    print(f"Generating {len(samples)} sample JPEG plots in {output_dir}...")

    for filename, model, init_state, params, theme in samples:
        colors = get_plot_colors(theme)
        res = simulate_model(model, initial_state=init_state, t_span=(0.0, 60.0), params=params)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=300, facecolor=colors["figure_facecolor"])
        for ax in (ax1, ax2):
            ax.set_facecolor(colors["axes_facecolor"])
            for spine in ax.spines.values():
                spine.set_color(colors["grid"])
            ax.tick_params(colors=colors["subtext_color"])

        # Left: Time series
        ax1.plot(res.t, res.n1, color=colors["n1"], lw=2.2, label=res.n1_label)
        ax1.plot(res.t, res.n2, color=colors["n2"], lw=2.2, label=res.n2_label)
        ax1.fill_between(res.t, res.n1, color=colors["n1"], alpha=0.10)
        ax1.fill_between(res.t, res.n2, color=colors["n2"], alpha=0.10)
        ax1.set_title(f"Time Dynamics: {model.name}\n({theme.capitalize()} Theme)", fontsize=10, fontweight="bold", color=colors["text_color"])
        ax1.set_xlabel("Time (t)", color=colors["subtext_color"])
        ax1.set_ylabel("Population / Level", color=colors["subtext_color"])
        ax1.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])
        leg1 = ax1.legend(loc="upper right", facecolor=colors["legend_face"], edgecolor=colors["legend_edge"])
        for t in leg1.get_texts():
            t.set_color(colors["text_color"])

        # Right: Phase space
        ax2.plot(res.n1, res.n2, color=colors["trajectory"], lw=2.0, label="Trajectory")
        ax2.scatter([res.n1[0]], [res.n2[0]], color=colors["start"], s=70, label=f"Start ({res.n1[0]:.1f}, {res.n2[0]:.1f})")
        ax2.scatter([res.n1[-1]], [res.n2[-1]], color=colors["end"], marker="X", s=80, label=f"End ({res.n1[-1]:.1f}, {res.n2[-1]:.1f})")
        ax2.set_title(f"Phase Space (Respective to Each Other)\n({theme.capitalize()} Theme)", fontsize=10, fontweight="bold", color=colors["text_color"])
        ax2.set_xlabel(res.n1_label, color=colors["subtext_color"])
        ax2.set_ylabel(res.n2_label, color=colors["subtext_color"])
        ax2.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])
        leg2 = ax2.legend(loc="upper right", facecolor=colors["legend_face"], edgecolor=colors["legend_edge"])
        for t in leg2.get_texts():
            t.set_color(colors["text_color"])

        fig.tight_layout()
        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, format="jpeg", dpi=300, bbox_inches="tight", facecolor=colors["figure_facecolor"])
        plt.close(fig)
        print(f"Saved: {filepath} ({os.path.getsize(filepath) // 1024} KB)")

    print("Sample JPEG exports completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Biological Modelling Desktop Application")
    parser.add_argument("--theme", choices=["light", "dark"], default="light", help="Initial theme (default: light)")
    parser.add_argument("--export-sample", action="store_true", help="Generate sample JPEG graphs without launching GUI")
    args = parser.parse_args()

    if args.export_sample:
        export_sample()
    else:
        run_gui(default_theme=args.theme)


if __name__ == "__main__":
    main()

