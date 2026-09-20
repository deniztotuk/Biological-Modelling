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


def run_gui():
    from PyQt6.QtWidgets import QApplication
    from bio_models.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("BioModel Studio")
    app.setOrganizationName("Ecology & Evolution Labs")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


def export_sample():
    """Headless simulation and export of sample JPEG images for verification."""
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

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)

    samples = [
        ("competition_coexistence.jpeg", LotkaVolterraCompetitionModel(), (25.0, 20.0), {"r1": 0.8, "r2": 0.7, "K1": 100.0, "K2": 100.0, "alpha12": 0.45, "alpha21": 0.40}),
        ("predator_prey_cycles.jpeg", LotkaVolterraPredatorPreyModel(), (30.0, 10.0), {"r": 0.9, "a": 0.05, "c": 0.4, "epsilon": 0.5, "delta": 0.25}),
        ("rosenzweig_macarthur_limit_cycle.jpeg", RosenzweigMacArthurModel(), (40.0, 15.0), {"r": 1.2, "K": 140.0, "a": 0.8, "c": 0.9, "b": 25.0, "epsilon": 0.45, "delta": 0.22}),
    ]

    print(f"Generating {len(samples)} sample JPEG plots in {output_dir}...")

    for filename, model, init_state, params in samples:
        res = simulate_model(model, initial_state=init_state, t_span=(0.0, 60.0), params=params)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=300)
        # Left: Time series
        ax1.plot(res.t, res.n1, color="#0284c7", lw=2, label=res.n1_label)
        ax1.plot(res.t, res.n2, color="#ea580c", lw=2, label=res.n2_label)
        ax1.fill_between(res.t, res.n1, color="#0284c7", alpha=0.1)
        ax1.fill_between(res.t, res.n2, color="#ea580c", alpha=0.1)
        ax1.set_title(f"Time Dynamics: {model.name}", fontsize=10, fontweight="bold")
        ax1.set_xlabel("Time (t)")
        ax1.set_ylabel("Population / Level")
        ax1.grid(True, linestyle="--", alpha=0.5)
        ax1.legend(loc="upper right")

        # Right: Phase space
        ax2.plot(res.n1, res.n2, color="#4338ca", lw=2, label="Trajectory")
        ax2.scatter([res.n1[0]], [res.n2[0]], color="#16a34a", s=60, label=f"Start ({res.n1[0]:.1f}, {res.n2[0]:.1f})")
        ax2.scatter([res.n1[-1]], [res.n2[-1]], color="#dc2626", marker="X", s=70, label=f"End ({res.n1[-1]:.1f}, {res.n2[-1]:.1f})")
        ax2.set_title("Phase Space (Respective to Each Other)", fontsize=10, fontweight="bold")
        ax2.set_xlabel(res.n1_label)
        ax2.set_ylabel(res.n2_label)
        ax2.grid(True, linestyle="--", alpha=0.5)
        ax2.legend(loc="upper right")

        fig.tight_layout()
        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, format="jpeg", dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved: {filepath} ({os.path.getsize(filepath) // 1024} KB)")

    print("Sample JPEG exports completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Biological Modelling Desktop Application")
    parser.add_argument("--export-sample", action="store_true", help="Generate sample JPEG graphs without launching GUI")
    args = parser.parse_args()

    if args.export_sample:
        export_sample()
    else:
        run_gui()


if __name__ == "__main__":
    main()
