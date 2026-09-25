"""Matplotlib Canvas and Plotting Widget.

Displays dual subplots:
1. Time series: n1(t) and n2(t) over time
2. Phase portrait: n2 vs n1 (populations respective to each other)
Provides dynamic theme switching (Light / Dark) and direct export to
JPEG / PNG.
"""

import os
from typing import Optional
import warnings

import matplotlib
from matplotlib.ticker import MaxNLocator
import numpy as np
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from matplotlib.figure import Figure
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bio_models.models import BiologicalModel, SimulationResult
from bio_models.ui.styles import get_plot_colors, get_save_icon

matplotlib.use("QtAgg")


def _format_density(val: float) -> str:
    """Format population count gracefully for display in status bar."""
    if not np.isfinite(val):
        return "N/A"
    if abs(val) >= 1e6 or (0 < abs(val) < 1e-2):
        return f"{val:.2e}"
    return f"{val:.2f}"


class BioPlotCanvas(QWidget):
    """Dual-view visualization widget displaying both time-series dynamics
    and phase-space trajectory, with Light/Dark themes and JPEG export.
    """

    export_completed = pyqtSignal(str)

    def __init__(self, theme: str = "light", parent=None):
        super().__init__(parent)
        self.theme = theme
        self._current_result: Optional[SimulationResult] = None
        self._current_model: Optional[BiologicalModel] = None

        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(70)
        self._resize_timer.timeout.connect(self._on_resize_debounced)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 14)
        layout.setSpacing(10)

        # Header bar with simulation status and export action
        canvas_header = QWidget()
        ch_layout = QHBoxLayout(canvas_header)
        ch_layout.setContentsMargins(0, 0, 0, 0)

        self.info_lbl = QLabel(
            "Ready — select a model from sandwich menu and run simulation."
        )
        self.info_lbl.setObjectName("CanvasInfoLabel")
        ch_layout.addWidget(self.info_lbl)
        ch_layout.addStretch()

        self.export_btn = QPushButton("Save Graph")
        self.export_btn.setObjectName("SaveGraphButton")
        self.export_btn.setIcon(get_save_icon(self.theme))
        self.export_btn.setIconSize(QSize(13, 13))
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setToolTip(
            "Save high-resolution 300 DPI plot image (Ctrl+S)"
        )
        self.export_btn.clicked.connect(lambda: self.save_graph_as_jpeg())
        ch_layout.addWidget(self.export_btn)

        layout.addWidget(canvas_header)

        # Matplotlib Figure and Canvas
        colors = get_plot_colors(self.theme)
        self.figure = Figure(
            figsize=(10, 5),
            dpi=100,
            facecolor=colors["figure_facecolor"],
        )
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setObjectName("PlotCanvas")
        layout.addWidget(self.canvas, stretch=1)

        # Setup side-by-side subplots (Time series + Phase portrait)
        self.ax_time = self.figure.add_subplot(121)
        self.ax_phase = self.figure.add_subplot(122)

        self._apply_initial_styling()

    def set_theme(self, theme: str):
        """Update plotting colors and redraw active plots with new theme."""
        self.theme = theme
        if hasattr(self, "export_btn"):
            self.export_btn.setIcon(get_save_icon(self.theme))
        if self._current_result and self._current_model:
            self.update_plot(self._current_result, self._current_model)
        else:
            self._apply_initial_styling()

    def _apply_initial_styling(self):
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

        self.ax_time.set_title(
            "Time Dynamics: n₁(t) and n₂(t)",
            fontsize=11,
            fontweight="bold",
            color=colors["text_color"],
        )
        self.ax_time.set_xlabel(
            "Time (t)", fontsize=10, color=colors["subtext_color"]
        )
        self.ax_time.set_ylabel(
            "Population / Abundance",
            fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_time.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )
        self.ax_time.text(
            0.5,
            0.5,
            "Click 'Run Simulation' to display",
            ha="center",
            va="center",
            color=colors["subtext_color"],
            transform=self.ax_time.transAxes,
        )

        self.ax_phase.set_title(
            "Phase Portrait: n₂ vs n₁",
            fontsize=11,
            fontweight="bold",
            color=colors["text_color"],
        )
        self.ax_phase.set_xlabel(
            "n₁ (Resource / Species 1)",
            fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_phase.set_ylabel(
            "n₂ (Consumer / Species 2)",
            fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_phase.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )
        self.ax_phase.text(
            0.5,
            0.5,
            "State-space trajectory",
            ha="center",
            va="center",
            color=colors["subtext_color"],
            transform=self.ax_phase.transAxes,
        )

        self.canvas.draw()

    def update_plot(
        self, result: SimulationResult, model: BiologicalModel
    ) -> None:
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
            self.ax_time.text(
                0.5,
                0.5,
                f"Simulation Failed:\n{result.message}",
                ha="center",
                va="center",
                color="red",
                transform=self.ax_time.transAxes,
            )
            self.canvas.draw()
            return

        if model.is_single_variable:
            self._update_plot_single_variable(result, model, colors)
        else:
            self._update_plot_two_variable(result, model, colors)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.figure.tight_layout(
                pad=2.2, w_pad=4.5, rect=(0.02, 0.0, 1.0, 1.0)
            )
            self.canvas.draw()

        if model.is_single_variable:
            n_str = _format_density(result.n1[-1])
            if "K" in result.parameters:
                k_int = int(round(result.parameters["K"]))
                self.info_lbl.setText(
                    f"{result.message} | Final: n={n_str} (K={k_int})"
                )
            else:
                self.info_lbl.setText(f"{result.message} | Final: n={n_str}")
        else:
            n1_str = _format_density(result.n1[-1])
            n2_str = _format_density(result.n2[-1])
            self.info_lbl.setText(
                f"{result.message} | Final: n₁={n1_str}, n₂={n2_str}"
            )

    def _update_plot_single_variable(
        self,
        result: SimulationResult,
        model: BiologicalModel,
        colors: dict,
    ) -> None:
        """Render single-species dynamics: time-series and 1D phase space."""
        t = result.t
        n1 = result.n1
        c1 = colors["n1"]
        traj_color = colors["trajectory"]
        params = result.parameters
        is_disc = result.metadata.get("mode") == "discrete"

        # -------------------------------------------------------------
        # 1. Left Subplot: Population Dynamics Over Time
        # -------------------------------------------------------------
        if is_disc:
            self.ax_time.step(
                t,
                n1,
                where="post",
                color=c1,
                linewidth=2.2,
                label=result.n1_label,
            )
            self.ax_time.fill_between(
                t, n1, step="post", color=c1, alpha=0.12
            )
            self.ax_time.plot(
                t, n1, "o", color=c1, markersize=4.0, alpha=0.9
            )
            self.ax_time.xaxis.set_major_locator(
                MaxNLocator(integer=True)
            )
        else:
            self.ax_time.plot(
                t, n1, color=c1, linewidth=2.2, label=result.n1_label
            )
            self.ax_time.fill_between(t, n1, color=c1, alpha=0.12)

        # Plot carrying capacity line if available
        if "K" in params:
            k_val = params["K"]
            self.ax_time.axhline(
                k_val,
                color=colors["isocline1"],
                linestyle=":",
                linewidth=1.6,
                alpha=0.85,
                label=f"Carrying Cap. (K={int(round(k_val))})",
            )
            y_max = max(1.0, max(np.max(n1), k_val) * 1.15)
        else:
            y_max = max(1.0, np.max(n1) * 1.15)

        self.ax_time.set_title(
            "Population Dynamics",
            fontsize=10.5,
            fontweight="bold",
            color=colors["text_color"],
            pad=10,
        )
        time_unit = "Time Steps (discrete)" if is_disc else "Time (t)"
        self.ax_time.set_xlabel(
            time_unit,
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_ylabel(
            "Population Density (n)",
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_xlim(left=t[0], right=t[-1])
        self.ax_time.set_ylim(bottom=0, top=y_max)
        self.ax_time.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )

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
        # 2. Right Subplot: 1D Phase Dynamics / Return Map
        # -------------------------------------------------------------
        grid_max = max(10.0, float(np.max(n1)) * 1.25)
        if "K" in params:
            grid_max = max(grid_max, float(params["K"]) * 1.25)
        n_grid = np.linspace(0.0, grid_max, 250)

        if is_disc:
            # Discrete Return Map: n(t+1) vs n(t)
            next_grid = np.array([
                model.discrete_step(np.array([val]), params)[0]
                for val in n_grid
            ])
            self.ax_phase.plot(
                n_grid,
                n_grid,
                linestyle="--",
                color=colors["grid"],
                linewidth=1.3,
                label="1:1 Line (n(t+1) = n(t))",
            )
            self.ax_phase.plot(
                n_grid,
                next_grid,
                color=c1,
                linewidth=2.0,
                label="Return Map n(t+1)",
            )

            # Observed trajectory steps
            if len(n1) > 1:
                self.ax_phase.plot(
                    n1[:-1],
                    n1[1:],
                    "o-",
                    color=traj_color,
                    linewidth=1.4,
                    markersize=3.5,
                    alpha=0.7,
                    label="Iteration Trajectory",
                )
                self.ax_phase.scatter(
                    [n1[0]],
                    [n1[1]],
                    color=colors["start"],
                    s=80,
                    zorder=6,
                    edgecolors="black",
                    linewidths=1.2,
                    label=f"Start (n₀={int(round(n1[0]))})",
                )
                self.ax_phase.scatter(
                    [n1[-2]],
                    [n1[-1]],
                    color=colors["end"],
                    s=70,
                    zorder=6,
                    marker="X",
                    edgecolors="black",
                    linewidths=1.2,
                    label=f"End (n={n1[-1]:.1f})",
                )

            self.ax_phase.set_title(
                "Return Map: n(t+1) vs n(t)",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )
            self.ax_phase.set_xlabel(
                "Current Generation n(t)",
                fontsize=10,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_ylabel(
                "Next Generation n(t+1)",
                fontsize=10,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            y_ceil = max(grid_max, float(np.max(next_grid)) * 1.1)
            self.ax_phase.set_xlim(left=0, right=grid_max)
            self.ax_phase.set_ylim(bottom=0, top=y_ceil)

        else:
            # Continuous Phase Space: dn/dt vs n
            rate_grid = np.array([
                model.rhs(0.0, np.array([val]), params)[0]
                for val in n_grid
            ])
            self.ax_phase.axhline(
                0.0,
                linestyle="--",
                color=colors["grid"],
                linewidth=1.3,
                label="Zero Growth (dn/dt = 0)",
            )
            self.ax_phase.plot(
                n_grid,
                rate_grid,
                color=c1,
                linewidth=2.0,
                label="Growth Rate dn/dt",
            )

            # Mark equilibrium at K if available
            if "K" in params:
                k_val = params["K"]
                self.ax_phase.scatter(
                    [k_val],
                    [0.0],
                    color=colors["isocline1"],
                    s=75,
                    zorder=6,
                    edgecolors="black",
                    linewidths=1.2,
                    label=f"Equilibrium (K={int(round(k_val))})",
                )

            # Trajectory on rate curve
            traj_rates = np.array([
                model.rhs(0.0, np.array([val]), params)[0]
                for val in n1
            ])
            self.ax_phase.scatter(
                [n1[0]],
                [traj_rates[0]],
                color=colors["start"],
                s=80,
                zorder=6,
                edgecolors="black",
                linewidths=1.2,
                label=f"Start (n₀={int(round(n1[0]))})",
            )
            self.ax_phase.scatter(
                [n1[-1]],
                [traj_rates[-1]],
                color=colors["end"],
                s=70,
                zorder=6,
                marker="X",
                edgecolors="black",
                linewidths=1.2,
                label=f"End (n={n1[-1]:.1f})",
            )

            self.ax_phase.set_title(
                "Growth Rate Curve (dn/dt)",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )
            self.ax_phase.set_xlabel(
                "Population Density (n)",
                fontsize=10,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_ylabel(
                "Net Rate of Change (dn/dt)",
                fontsize=10,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_xlim(left=0, right=grid_max)

        self.ax_phase.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )
        leg_phase = self.ax_phase.legend(
            frameon=True,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"],
            fontsize=8,
            loc="upper right",
        )
        for text in leg_phase.get_texts():
            text.set_color(colors["text_color"])

    def _update_plot_two_variable(
        self,
        result: SimulationResult,
        model: BiologicalModel,
        colors: dict,
    ) -> None:
        """Render two-species dynamics: time-series and phase portrait."""
        t = result.t
        n1 = result.n1
        n2 = result.n2

        c1 = colors["n1"]
        c2 = colors["n2"]

        is_disc = result.metadata.get("mode") == "discrete"

        # -------------------------------------------------------------
        # 1. Left Subplot: Population Dynamics Over Time
        # -------------------------------------------------------------
        if is_disc:
            self.ax_time.step(
                t,
                n1,
                where="post",
                color=c1,
                linewidth=2.2,
                label=result.n1_label,
            )
            self.ax_time.step(
                t,
                n2,
                where="post",
                color=c2,
                linewidth=2.2,
                label=result.n2_label,
            )
            self.ax_time.fill_between(
                t, n1, step="post", color=c1, alpha=0.10
            )
            self.ax_time.fill_between(
                t, n2, step="post", color=c2, alpha=0.10
            )
            self.ax_time.plot(
                t, n1, "o", color=c1, markersize=3.5, alpha=0.85
            )
            self.ax_time.plot(
                t, n2, "o", color=c2, markersize=3.5, alpha=0.85
            )
            self.ax_time.xaxis.set_major_locator(
                MaxNLocator(integer=True)
            )
        else:
            self.ax_time.plot(
                t, n1, color=c1, linewidth=2.2, label=result.n1_label
            )
            self.ax_time.plot(
                t, n2, color=c2, linewidth=2.2, label=result.n2_label
            )
            self.ax_time.fill_between(t, n1, color=c1, alpha=0.10)
            self.ax_time.fill_between(t, n2, color=c2, alpha=0.10)

        self.ax_time.set_title(
            "Population Dynamics (Time Series)",
            fontsize=10.5,
            fontweight="bold",
            color=colors["text_color"],
            pad=10,
        )
        time_unit = "Time Steps (discrete)" if is_disc else "Time (t)"
        self.ax_time.set_xlabel(
            time_unit,
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_ylabel(
            "Population Density / Abundance",
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_xlim(left=t[0], right=t[-1])
        finite_n1 = n1[np.isfinite(n1)]
        finite_n2 = n2[np.isfinite(n2)]
        max_1 = float(np.max(finite_n1)) if len(finite_n1) > 0 else 1.0
        max_2 = float(np.max(finite_n2)) if len(finite_n2) > 0 else 1.0
        self.ax_time.set_ylim(
            bottom=0,
            top=max(1.0, max(max_1, max_2) * 1.15),
        )
        self.ax_time.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )

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
        # 2. Right Subplot: Phase Portrait (State Space)
        # -------------------------------------------------------------
        traj_color = colors["trajectory"]
        if is_disc:
            self.ax_phase.plot(
                n1,
                n2,
                "o--",
                color=traj_color,
                linewidth=1.4,
                markersize=3.5,
                alpha=0.8,
                label="Discrete Trajectory (n₁, n₂)",
            )
        else:
            self.ax_phase.plot(
                n1,
                n2,
                color=traj_color,
                linewidth=2.0,
                label="Trajectory (n₁, n₂)",
            )

        # Markers for start and end points
        init_n1 = int(round(n1[0]))
        init_n2 = int(round(n2[0]))
        self.ax_phase.scatter(
            [n1[0]],
            [n2[0]],
            color=colors["start"],
            s=80,
            zorder=6,
            edgecolors="black",
            linewidths=1.2,
            label=f"Start ({init_n1}, {init_n2})",
        )
        self.ax_phase.scatter(
            [n1[-1]],
            [n2[-1]],
            color=colors["end"],
            s=70,
            zorder=6,
            marker="X",
            edgecolors="black",
            linewidths=1.2,
            label=f"End ({n1[-1]:.1f}, {n2[-1]:.1f})",
        )

        # Direction arrows along trajectory
        if len(n1) > 20:
            step = max(5, len(n1) // 6)
            for idx in range(step // 2, len(n1) - step // 2, step):
                dx = n1[idx + 1] - n1[idx]
                dy = n2[idx + 1] - n2[idx]
                dist = np.hypot(dx, dy)
                if dist > 1e-4:
                    self.ax_phase.annotate(
                        "",
                        xy=(n1[idx] + dx * 0.6, n2[idx] + dy * 0.6),
                        xytext=(n1[idx], n2[idx]),
                        arrowprops=dict(
                            arrowstyle="->",
                            color=traj_color,
                            lw=1.5,
                        ),
                    )

        # Plot Nullclines (Zero-growth isoclines) if available
        max_n1 = max(10.0, np.max(n1) * 1.25)
        max_n2 = max(10.0, np.max(n2) * 1.25)
        nullclines = model.get_nullclines(
            result.parameters, (0, max_n1), (0, max_n2)
        )

        for name, (iso_x, iso_y) in nullclines.items():
            if "dn₁" in name:
                self.ax_phase.plot(
                    iso_x,
                    iso_y,
                    linestyle="--",
                    color=colors["isocline1"],
                    alpha=0.8,
                    linewidth=1.4,
                    label=name,
                )
            else:
                self.ax_phase.plot(
                    iso_x,
                    iso_y,
                    linestyle="--",
                    color=colors["isocline2"],
                    alpha=0.8,
                    linewidth=1.4,
                    label=name,
                )

        self.ax_phase.set_title(
            "Phase Portrait (State Space)",
            fontsize=10.5,
            fontweight="bold",
            color=colors["text_color"],
            pad=10,
        )
        self.ax_phase.set_xlabel(
            result.n1_label,
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_phase.set_ylabel(
            result.n2_label,
            fontsize=10,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_phase.set_xlim(left=0, right=max_n1)
        self.ax_phase.set_ylim(bottom=0, top=max_n2)
        self.ax_phase.grid(
            True, linestyle="--", alpha=0.5, color=colors["grid"]
        )

        leg_phase = self.ax_phase.legend(
            frameon=True,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"],
            fontsize=8,
            loc="upper right",
        )
        for text in leg_phase.get_texts():
            text.set_color(colors["text_color"])

    def save_graph_as_jpeg(
        self, custom_path: Optional[str] = None
    ) -> Optional[str]:
        """Export the current figure as a 300 DPI JPEG image.
        If custom_path is not provided, open a native Save File Dialog.
        """
        if self._current_result is None:
            QMessageBox.warning(
                self,
                "No Data",
                "Please run a simulation first before exporting.",
            )
            return None

        if custom_path:
            target_path = custom_path
        else:
            base_model_name = (
                self._current_result.model_name.replace(" ", "_").lower()
            )
            default_name = f"{base_model_name}_simulation.jpeg"
            target_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Simulation Graph",
                default_name,
                "JPEG Image (*.jpeg *.jpg);;PNG Image (*.png);;All Files (*)",
            )

        if not target_path:
            return None

        # Ensure correct extension
        ext = target_path.lower()
        if not (
            ext.endswith(".jpeg")
            or ext.endswith(".jpg")
            or ext.endswith(".png")
        ):
            target_path += ".jpeg"

        os.makedirs(
            os.path.dirname(os.path.abspath(target_path)), exist_ok=True
        )

        colors = get_plot_colors(self.theme)
        is_png = target_path.lower().endswith(".png")
        try:
            self.figure.savefig(
                target_path,
                format="png" if is_png else "jpeg",
                dpi=300,
                bbox_inches="tight",
                facecolor=colors["figure_facecolor"],
                edgecolor="none",
            )
            self.export_completed.emit(target_path)
            if not custom_path:
                QMessageBox.information(
                    self,
                    "Graph Exported",
                    f"Successfully saved graph to:\n{target_path}",
                )
            return target_path
        except Exception as e:
            if not custom_path:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to save image:\n{e}",
                )
            return None

    def resizeEvent(self, event):
        """Debounce layout recalculation during window and drawer resize."""
        super().resizeEvent(event)
        if self._current_result is not None:
            self._resize_timer.start()

    def _on_resize_debounced(self):
        """Execute tight layout once after resize or drawer animation ends."""
        if self._current_result is not None:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    self.figure.tight_layout(
                        pad=2.2, w_pad=4.5, rect=(0.02, 0.0, 1.0, 1.0)
                    )
                    self.canvas.draw_idle()
            except Exception:
                pass
