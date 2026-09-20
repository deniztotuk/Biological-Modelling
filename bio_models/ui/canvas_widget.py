"""
Matplotlib Canvas and Plotting Widget.
Displays dual subplots:
1. Time series: n1(t) and n2(t) over time
2. Phase portrait: n2 vs n1 (populations respective to each other)
Provides direct export to JPEG / PNG.
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
from bio_models.ui.styles import PLOT_COLORS


class BioPlotCanvas(QWidget):
    """
    Dual-view visualization widget displaying both time-series dynamics
    and phase-space trajectory, with JPEG export capabilities.
    """

    export_completed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_result: Optional[SimulationResult] = None
        self._current_model: Optional[BiologicalModel] = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Matplotlib Figure with 2 subplots side-by-side
        self.figure = Figure(figsize=(10, 5.2), dpi=100, facecolor="#ffffff")
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
        self.info_lbl.setStyleSheet("color: #475569; font-size: 12px;")
        bar_layout.addWidget(self.info_lbl)
        bar_layout.addStretch()

        self.save_btn = QPushButton("📷 Save Graph (JPEG)...")
        self.save_btn.setObjectName("SaveJpegButton")
        self.save_btn.setToolTip("Export the current graph as a high-resolution JPEG file")
        self.save_btn.clicked.connect(self.save_graph_as_jpeg)
        bar_layout.addWidget(self.save_btn)

        layout.addLayout(bar_layout)

        # Draw empty placeholder
        self._draw_placeholder()

    def _draw_placeholder(self):
        self.ax_time.clear()
        self.ax_phase.clear()

        self.ax_time.set_title("Time Dynamics: n₁(t) and n₂(t)", fontsize=11, fontweight="bold", color="#1e293b")
        self.ax_time.set_xlabel("Time (t)", fontsize=10, color="#475569")
        self.ax_time.set_ylabel("Population / Abundance", fontsize=10, color="#475569")
        self.ax_time.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")
        self.ax_time.text(0.5, 0.5, "Click 'Run Simulation' to display", ha="center", va="center", color="#94a3b8", transform=self.ax_time.transAxes)

        self.ax_phase.set_title("Phase Portrait: n₂ vs n₁", fontsize=11, fontweight="bold", color="#1e293b")
        self.ax_phase.set_xlabel("n₁ (Resource / Species 1)", fontsize=10, color="#475569")
        self.ax_phase.set_ylabel("n₂ (Consumer / Species 2)", fontsize=10, color="#475569")
        self.ax_phase.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")
        self.ax_phase.text(0.5, 0.5, "State-space trajectory", ha="center", va="center", color="#94a3b8", transform=self.ax_phase.transAxes)

        self.canvas.draw()

    def update_plot(self, result: SimulationResult, model: BiologicalModel):
        """Update both subplots with simulation data."""
        self._current_result = result
        self._current_model = model

        self.ax_time.clear()
        self.ax_phase.clear()

        if not result.success:
            self.ax_time.text(0.5, 0.5, f"Simulation Failed:\n{result.message}", ha="center", va="center", color="red", transform=self.ax_time.transAxes)
            self.canvas.draw()
            return

        t = result.t
        n1 = result.n1
        n2 = result.n2

        c1 = PLOT_COLORS["n1"]
        c2 = PLOT_COLORS["n2"]

        # -------------------------------------------------------------
        # 1. Left Subplot: Population Dynamics Over Time
        # -------------------------------------------------------------
        self.ax_time.plot(t, n1, color=c1, linewidth=2.2, label=result.n1_label)
        self.ax_time.plot(t, n2, color=c2, linewidth=2.2, label=result.n2_label)
        self.ax_time.fill_between(t, n1, color=c1, alpha=0.08)
        self.ax_time.fill_between(t, n2, color=c2, alpha=0.08)

        self.ax_time.set_title(f"Population Over Time\n({result.model_name})", fontsize=11, fontweight="bold", color="#0f172a", pad=8)
        time_unit = "Time Steps (discrete)" if result.metadata.get("mode") == "discrete" else "Time (t)"
        self.ax_time.set_xlabel(time_unit, fontsize=10, fontweight="600", color="#334155")
        self.ax_time.set_ylabel("Population Density / Abundance", fontsize=10, fontweight="600", color="#334155")
        self.ax_time.set_xlim(left=0, right=t[-1])
        self.ax_time.set_ylim(bottom=0, top=max(1.0, max(np.max(n1), np.max(n2)) * 1.15))
        self.ax_time.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")
        self.ax_time.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=9, loc="upper right")

        # -------------------------------------------------------------
        # 2. Right Subplot: Phase Portrait (n2 vs n1)
        # -------------------------------------------------------------
        traj_color = PLOT_COLORS["trajectory"]
        self.ax_phase.plot(n1, n2, color=traj_color, linewidth=2.0, label="Trajectory", alpha=0.85)

        # Start and End Markers
        self.ax_phase.scatter([n1[0]], [n2[0]], color=PLOT_COLORS["start"], s=80, zorder=5, label=f"Start ({n1[0]:.1f}, {n2[0]:.1f})", edgecolors="black", linewidth=1.2)
        self.ax_phase.scatter([n1[-1]], [n2[-1]], color=PLOT_COLORS["end"], marker="X", s=90, zorder=5, label=f"End ({n1[-1]:.1f}, {n2[-1]:.1f})", edgecolors="black", linewidth=1.2)

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
                self.ax_phase.plot(iso_x, iso_y, linestyle="--", color=c1, alpha=0.75, linewidth=1.4, label=name)
            else:
                self.ax_phase.plot(iso_x, iso_y, linestyle="--", color=c2, alpha=0.75, linewidth=1.4, label=name)

        self.ax_phase.set_title("Phase Space: Consumer/Predator vs Resource/Prey", fontsize=11, fontweight="bold", color="#0f172a", pad=8)
        self.ax_phase.set_xlabel(result.n1_label, fontsize=10, fontweight="600", color="#334155")
        self.ax_phase.set_ylabel(result.n2_label, fontsize=10, fontweight="600", color="#334155")
        self.ax_phase.set_xlim(left=0, right=max_n1)
        self.ax_phase.set_ylim(bottom=0, top=max_n2)
        self.ax_phase.grid(True, linestyle="--", alpha=0.5, color="#cbd5e1")
        self.ax_phase.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=8, loc="upper right")

        self.figure.tight_layout(pad=2.8)
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

        try:
            self.figure.savefig(
                target_path,
                format="jpeg" if not target_path.lower().endswith(".png") else "png",
                dpi=300,
                bbox_inches="tight",
                facecolor="#ffffff",
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
