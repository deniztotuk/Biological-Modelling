"""
Matplotlib Canvas and Plotting Widget.
Displays dual subplots:
1. Time series: n1(t) and n2(t) over time
2. Phase portrait: n2 vs n1 (populations respective to each other)
Provides dynamic theme switching (Light / Dark) and direct export to JPEG / PNG.
"""

import os
from typing import Optional
import numpy as np

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
    QFrame,
)

from bio_models.models import SimulationResult, BiologicalModel
from bio_models.ui.styles import get_plot_colors


class BioPlotCanvas(QWidget):
    """
    Dual-view visualization widget displaying both time-series dynamics
    and phase-space trajectory, with Light/Dark themes and JPEG export.
    """

    export_completed = pyqtSignal(str)

    def __init__(self, theme: str = "light", parent=None):
        super().__init__(parent)
        self.theme = theme
        self._current_result: Optional[SimulationResult] = None
        self._current_model: Optional[BiologicalModel] = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        colors = get_plot_colors(self.theme)

        # Matplotlib Figure with 2 subplots side-by-side
        self.figure = Figure(figsize=(10, 5.2), dpi=100, facecolor=colors["figure_facecolor"])
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(380)

        # Plot subplots
        self.ax_time = self.figure.add_subplot(121)
        self.ax_phase = self.figure.add_subplot(122)
        self.figure.tight_layout(pad=3.0)

        layout.addWidget(self.canvas, stretch=1)

        # Controls Bar at bottom
        bar_layout = QHBoxLayout()
        bar_layout.setContentsMargins(4, 4, 4, 4)

        self.info_lbl = QLabel("Ready to simulate. Adjust parameters or select a model.")
        self.info_lbl.setObjectName("CanvasInfoLabel")
        bar_layout.addWidget(self.info_lbl)
        bar_layout.addStretch()

        self.save_btn = QPushButton("📷 Save Graph (JPEG)...")
        self.save_btn.setObjectName("SaveJpegButton")
        self.save_btn.setToolTip("Export the current graph as a high-resolution JPEG file")
        self.save_btn.clicked.connect(self.save_graph_as_jpeg)
        bar_layout.addWidget(self.save_btn)

        layout.addLayout(bar_layout)

        # Draw initial placeholder
        self._draw_placeholder()

    def set_theme(self, theme_name: str):
        """Switch plotting theme between 'light' and 'dark' and re-render."""
        self.theme = theme_name
        colors = get_plot_colors(self.theme)
        self.figure.set_facecolor(colors["figure_facecolor"])

        if self._current_result and self._current_model:
            self.update_plot(self._current_result, self._current_model)
        else:
            self._draw_placeholder()

    def _draw_placeholder(self):
        colors = get_plot_colors(self.theme)
        self.figure.set_facecolor(colors["figure_facecolor"])

        self.ax_time.clear()
        self.ax_phase.clear()

        self.ax_time.set_facecolor(colors["axes_facecolor"])
        self.ax_phase.set_facecolor(colors["axes_facecolor"])

        # Spines & Ticks
        for ax in (self.ax_time, self.ax_phase):
            for spine in ax.spines.values():
                spine.set_color(colors["grid"])
            ax.tick_params(colors=colors["subtext_color"])

        self.ax_time.set_title("Time Dynamics: n₁(t) and n₂(t)", fontsize=11, fontweight="bold", color=colors["text_color"])
        self.ax_time.set_xlabel("Time (t)", fontsize=10, color=colors["subtext_color"])
        self.ax_time.set_ylabel("Population / Abundance", fontsize=10, color=colors["subtext_color"])
        self.ax_time.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])
        self.ax_time.text(0.5, 0.5, "Click 'Run Simulation' to display", ha="center", va="center", color=colors["subtext_color"], transform=self.ax_time.transAxes)

        self.ax_phase.set_title("Phase Portrait: n₂ vs n₁", fontsize=11, fontweight="bold", color=colors["text_color"])
        self.ax_phase.set_xlabel("n₁ (Resource / Species 1)", fontsize=10, color=colors["subtext_color"])
        self.ax_phase.set_ylabel("n₂ (Consumer / Species 2)", fontsize=10, color=colors["subtext_color"])
        self.ax_phase.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])
        self.ax_phase.text(0.5, 0.5, "State-space trajectory", ha="center", va="center", color=colors["subtext_color"], transform=self.ax_phase.transAxes)

        self.canvas.draw()

    def update_plot(self, result: SimulationResult, model: BiologicalModel):
        """Update both subplots with simulation data."""
        self._current_result = result
        self._current_model = model

        colors = get_plot_colors(self.theme)
        self.figure.set_facecolor(colors["figure_facecolor"])

        self.ax_time.clear()
        self.ax_phase.clear()

        self.ax_time.set_facecolor(colors["axes_facecolor"])
        self.ax_phase.set_facecolor(colors["axes_facecolor"])

        # Spines and Ticks styling
        for ax in (self.ax_time, self.ax_phase):
            for spine in ax.spines.values():
                spine.set_color(colors["grid"])
            ax.tick_params(colors=colors["subtext_color"])

        if not result.success:
            self.ax_time.text(0.5, 0.5, f"Simulation Failed:\n{result.message}", ha="center", va="center", color="red", transform=self.ax_time.transAxes)
            self.canvas.draw()
            return

        t = result.t
        n1 = result.n1
        n2 = result.n2

        c1 = colors["n1"]
        c2 = colors["n2"]

        # -------------------------------------------------------------
        # 1. Left Subplot: Population Dynamics Over Time
        # -------------------------------------------------------------
        self.ax_time.plot(t, n1, color=c1, linewidth=2.2, label=result.n1_label)
        self.ax_time.plot(t, n2, color=c2, linewidth=2.2, label=result.n2_label)
        self.ax_time.fill_between(t, n1, color=c1, alpha=0.10)
        self.ax_time.fill_between(t, n2, color=c2, alpha=0.10)

        self.ax_time.set_title("Population Dynamics (Time Series)", fontsize=11, fontweight="bold", color=colors["text_color"], pad=10)
        time_unit = "Time Steps (discrete)" if result.metadata.get("mode") == "discrete" else "Time (t)"
        self.ax_time.set_xlabel(time_unit, fontsize=10, fontweight="600", color=colors["subtext_color"])
        self.ax_time.set_ylabel("Population Density / Abundance", fontsize=10, fontweight="600", color=colors["subtext_color"])
        self.ax_time.set_xlim(left=t[0], right=t[-1])
        self.ax_time.set_ylim(bottom=0, top=max(1.0, max(np.max(n1), np.max(n2)) * 1.15))
        self.ax_time.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])

        leg_time = self.ax_time.legend(
            frameon=True,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"],
            fontsize=9,
            loc="upper right",
        )
        for text in leg_time.get_texts():
            text.set_color(colors["text_color"])

        # -------------------------------------------------------------
        # 2. Right Subplot: Phase Portrait (n2 vs n1)
        # -------------------------------------------------------------
        traj_color = colors["trajectory"]
        self.ax_phase.plot(n1, n2, color=traj_color, linewidth=2.0, label="Trajectory", alpha=0.9)

        # Start and End Markers
        self.ax_phase.scatter(
            [n1[0]], [n2[0]],
            color=colors["start"],
            s=80,
            zorder=5,
            label=f"Start ({n1[0]:.1f}, {n2[0]:.1f})",
            edgecolors=colors["figure_facecolor"],
            linewidth=1.2,
        )
        self.ax_phase.scatter(
            [n1[-1]], [n2[-1]],
            color=colors["end"],
            marker="X",
            s=90,
            zorder=5,
            label=f"End ({n1[-1]:.1f}, {n2[-1]:.1f})",
            edgecolors=colors["figure_facecolor"],
            linewidth=1.2,
        )

        # Directional arrows on trajectory
        if len(t) > 30:
            step_arrow = max(len(t) // 6, 8)
            for idx in range(step_arrow // 2, len(t) - 2, step_arrow):
                dx = n1[idx + 1] - n1[idx]
                dy = n2[idx + 1] - n2[idx]
                dist = np.hypot(dx, dy)
                if dist > 1e-4:
                    self.ax_phase.annotate(
                        "",
                        xy=(n1[idx + 1], n2[idx + 1]),
                        xytext=(n1[idx], n2[idx]),
                        arrowprops=dict(arrowstyle="->", color=traj_color, lw=1.5),
                    )

        # Plot Nullclines (Zero-growth isoclines) if available
        max_n1 = max(10.0, np.max(n1) * 1.25)
        max_n2 = max(10.0, np.max(n2) * 1.25)
        nullclines = model.get_nullclines(result.parameters, (0, max_n1), (0, max_n2))

        for name, (iso_x, iso_y) in nullclines.items():
            if "dn₁" in name:
                self.ax_phase.plot(iso_x, iso_y, linestyle="--", color=colors["isocline1"], alpha=0.8, linewidth=1.4, label=name)
            else:
                self.ax_phase.plot(iso_x, iso_y, linestyle="--", color=colors["isocline2"], alpha=0.8, linewidth=1.4, label=name)

        self.ax_phase.set_title("Phase Portrait (State Space)", fontsize=11, fontweight="bold", color=colors["text_color"], pad=10)
        self.ax_phase.set_xlabel(result.n1_label, fontsize=10, fontweight="600", color=colors["subtext_color"])
        self.ax_phase.set_ylabel(result.n2_label, fontsize=10, fontweight="600", color=colors["subtext_color"])
        self.ax_phase.set_xlim(left=0, right=max_n1)
        self.ax_phase.set_ylim(bottom=0, top=max_n2)
        self.ax_phase.grid(True, linestyle="--", alpha=0.5, color=colors["grid"])

        leg_phase = self.ax_phase.legend(
            frameon=True,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"],
            fontsize=8,
            loc="upper right",
        )
        for text in leg_phase.get_texts():
            text.set_color(colors["text_color"])

        self.figure.tight_layout(pad=2.8, w_pad=3.5)
        self.canvas.draw()

        self.info_lbl.setText(f"{result.message} | Final: n₁={n1[-1]:.2f}, n₂={n2[-1]:.2f}")

    def save_graph_as_jpeg(self, custom_path: Optional[str] = None) -> Optional[str]:
        """
        Export the current figure as a 300 DPI JPEG image.
        If custom_path is not provided, open a native Save File Dialog.
        """
        if self._current_result is None:
            QMessageBox.warning(self, "No Data", "Please run a simulation first before exporting.")
            return None

        if custom_path:
            target_path = custom_path
        else:
            default_name = f"{self._current_result.model_name.replace(' ', '_').lower()}_simulation.jpeg"
            target_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Simulation Graph as JPEG",
                default_name,
                "JPEG Image (*.jpeg *.jpg);;PNG Image (*.png);;All Files (*)",
            )

        if not target_path:
            return None

        # Ensure correct extension
        if not (target_path.lower().endswith(".jpeg") or target_path.lower().endswith(".jpg") or target_path.lower().endswith(".png")):
            target_path += ".jpeg"

        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

        colors = get_plot_colors(self.theme)
        try:
            self.figure.savefig(
                target_path,
                format="jpeg" if not target_path.lower().endswith(".png") else "png",
                dpi=300,
                bbox_inches="tight",
                facecolor=colors["figure_facecolor"],
                edgecolor="none",
            )
            self.export_completed.emit(target_path)
            if not custom_path:
                QMessageBox.information(self, "Graph Exported", f"Successfully saved graph to:\n{target_path}")
            return target_path
        except Exception as e:
            if not custom_path:
                QMessageBox.critical(self, "Export Error", f"Failed to save image:\n{e}")
            return None
