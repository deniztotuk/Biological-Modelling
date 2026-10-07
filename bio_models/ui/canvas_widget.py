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

from bio_models.engine import export_simulation_to_csv
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
    """Dual-view visualization widget for simulation dynamics.

    Provides time-series and phase portrait visualizations, dynamic
    theme switching, and unified export to CSV data and plot images.
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

        self.export_btn = QPushButton("Save")
        self.export_btn.setObjectName("SaveGraphButton")
        self.export_btn.setIcon(get_save_icon(self.theme))
        self.export_btn.setIconSize(QSize(13, 13))
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setToolTip(
            "Save simulation data (CSV) or plot image (Ctrl+S)"
        )
        self.export_btn.clicked.connect(lambda: self.save())
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
        """Update plot colors and redraw active plots with new theme."""
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

        if getattr(model, "is_epidemic_model", False):
            self._update_plot_epidemic_model(result, model, colors)
        elif getattr(model, "is_frequency_model", False):
            self._update_plot_frequency_model(result, model, colors)
        elif model.is_single_variable:
            self._update_plot_single_variable(result, model, colors)
        else:
            self._update_plot_two_variable(result, model, colors)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.figure.tight_layout(
                pad=1.8, w_pad=3.2, rect=(0.02, 0.02, 0.98, 0.98)
            )
            self.canvas.draw()

        if getattr(model, "is_epidemic_model", False):
            self._update_epidemic_info_label(result, model)
        elif getattr(model, "is_frequency_model", False):
            p_end = result.n1[-1]
            q_end = result.n2[-1]
            dp = p_end - result.n1[0]
            self.info_lbl.setText(
                f"{result.message} | Final: p={p_end:.3f}, q={q_end:.3f} "
                f"(Δp = {dp:+.3f})"
            )
        elif model.is_single_variable:
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

    def _update_epidemic_info_label(
        self, result: SimulationResult, model: BiologicalModel
    ) -> None:
        # Format informative status summary for epidemic dynamics.
        beta = result.parameters.get("beta", 0.0002)
        gamma = result.parameters.get("gamma", 0.10)
        s0 = result.n1[0]
        s_end = result.n1[-1]

        if "SIS" in model.name:
            n_tot = result.n1[0] + result.n2[0]
            r0 = (beta * n_tot) / gamma if gamma > 0 else 0.0
            if r0 > 1.0:
                i_star = n_tot * (1.0 - 1.0 / r0)
                s_star = n_tot / r0
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} | "
                    f"Endemic Equilibrium: I* = {int(round(i_star))}, "
                    f"S* = {int(round(s_star))} | "
                    f"Final: I = {int(round(result.n2[-1]))}"
                )
            else:
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} (R₀ ≤ 1: Pathogen "
                    f"Eradicated, S* = {int(round(n_tot))})"
                )
        elif "SEIR" in model.name:
            r0 = (beta * s0) / gamma if gamma > 0 else 0.0
            sigma = result.parameters.get("sigma", 0.20)
            latency_days = (1.0 / sigma) if sigma > 0 else 0.0
            e_max = float(np.max(result.n2))
            i_max = (
                float(np.max(result.n3))
                if result.n3 is not None
                else 0.0
            )
            t_i = (
                result.t[int(np.argmax(result.n3))]
                if result.n3 is not None
                else 0.0
            )
            if r0 > 1.0:
                hit = (1.0 - 1.0 / r0) * 100.0
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} (HIT: {hit:.1f}%) | "
                    f"Latency 1/σ = {latency_days:.1f}d | "
                    f"Peak: I = {int(round(i_max))} (t = {t_i:.1f}), "
                    f"E = {int(round(e_max))} | "
                    f"Uninfected: {int(round(s_end))}"
                )
            else:
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} (Sub-Threshold: "
                    f"Clearance) | Uninfected: {int(round(s_end))}"
                )
        else:
            # Classic SIR model.
            r0 = (beta * s0) / gamma if gamma > 0 else 0.0
            i_max = float(np.max(result.n2))
            t_peak = result.t[int(np.argmax(result.n2))]
            if r0 > 1.0:
                hit = (1.0 - 1.0 / r0) * 100.0
                s_c = gamma / beta if beta > 0 else 0.0
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} (HIT: {hit:.1f}%, "
                    f"S_c = {int(round(s_c))}) | "
                    f"Peak: I = {int(round(i_max))} (t = {t_peak:.1f}) | "
                    f"Uninfected: {int(round(s_end))}"
                )
            else:
                msg = (
                    f"{result.message} | R₀ = {r0:.2f} (Sub-Threshold: "
                    f"No Outbreak Wave) | "
                    f"Uninfected: {int(round(s_end))}"
                )
        self.info_lbl.setText(msg)

    def _update_plot_epidemic_model(
        self,
        result: SimulationResult,
        model: BiologicalModel,
        colors: dict,
    ) -> None:
        # Render epidemic time series curves and phase portrait.
        t = result.t
        s_arr = result.n1
        is_disc = result.metadata.get("mode") == "discrete"
        params = result.parameters
        beta = params.get("beta", 0.0002)
        gamma = params.get("gamma", 0.10)

        is_dark = self.theme.lower() == "dark"
        c_s = "#38bdf8" if is_dark else "#0284c7"
        c_e = "#fbbf24" if is_dark else "#d97706"
        c_i = "#f87171" if is_dark else "#dc2626"
        c_r = "#34d399" if is_dark else "#059669"
        c_thresh = "#94a3b8" if is_dark else "#64748b"

        # -------------------------------------------------------------
        # 1. Left Subplot: Epidemic Waves Over Time
        # -------------------------------------------------------------
        if "SEIR" in model.name:
            e_arr = result.n2
            i_arr = (
                result.n3 if result.n3 is not None else np.zeros_like(t)
            )
            r_arr = (
                result.n4 if result.n4 is not None else np.zeros_like(t)
            )

            if is_disc:
                self.ax_time.step(
                    t, s_arr, where="post", color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.step(
                    t, e_arr, where="post", color=c_e, linewidth=2.0,
                    label=result.n2_label,
                )
                self.ax_time.step(
                    t, i_arr, where="post", color=c_i, linewidth=2.2,
                    label=result.n3_label or "Infectious (I)",
                )
                self.ax_time.step(
                    t, r_arr, where="post", color=c_r, linewidth=2.0,
                    label=result.n4_label or "Recovered (R)",
                )
                self.ax_time.fill_between(
                    t, i_arr, step="post", color=c_i, alpha=0.15
                )
                self.ax_time.plot(
                    t, i_arr, "o", color=c_i, markersize=3.0, alpha=0.85
                )
                self.ax_time.xaxis.set_major_locator(
                    MaxNLocator(integer=True)
                )
            else:
                self.ax_time.plot(
                    t, s_arr, color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.plot(
                    t, e_arr, color=c_e, linewidth=2.0,
                    label=result.n2_label,
                )
                self.ax_time.plot(
                    t, i_arr, color=c_i, linewidth=2.2,
                    label=result.n3_label or "Infectious (I)",
                )
                self.ax_time.plot(
                    t, r_arr, color=c_r, linewidth=2.0,
                    label=result.n4_label or "Recovered (R)",
                )
                self.ax_time.fill_between(
                    t, i_arr, color=c_i, alpha=0.15
                )
                self.ax_time.fill_between(
                    t, e_arr, color=c_e, alpha=0.08
                )

            s0 = s_arr[0]
            if beta > 0 and gamma > 0:
                s_c = gamma / beta
                if s_c < s0:
                    self.ax_time.axhline(
                        s_c, color=c_thresh, linestyle="--", alpha=0.6,
                        label=f"Threshold (S_c = {int(round(s_c))})",
                    )
            self.ax_time.set_title(
                "SEIR Dynamics",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )

        elif "SIS" in model.name:
            i_arr = result.n2
            if is_disc:
                self.ax_time.step(
                    t, s_arr, where="post", color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.step(
                    t, i_arr, where="post", color=c_i, linewidth=2.2,
                    label=result.n2_label,
                )
                self.ax_time.fill_between(
                    t, i_arr, step="post", color=c_i, alpha=0.15
                )
                self.ax_time.plot(
                    t, i_arr, "o", color=c_i, markersize=3.0, alpha=0.85
                )
                self.ax_time.xaxis.set_major_locator(
                    MaxNLocator(integer=True)
                )
            else:
                self.ax_time.plot(
                    t, s_arr, color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.plot(
                    t, i_arr, color=c_i, linewidth=2.2,
                    label=result.n2_label,
                )
                self.ax_time.fill_between(
                    t, i_arr, color=c_i, alpha=0.15
                )

            n_tot = s_arr[0] + i_arr[0]
            r0 = (beta * n_tot) / gamma if gamma > 0 else 0.0
            if r0 > 1.0:
                i_star = n_tot * (1.0 - 1.0 / r0)
                self.ax_time.axhline(
                    i_star, color=c_i, linestyle=":", alpha=0.7,
                    label=f"Endemic I* = {int(round(i_star))}",
                )
            self.ax_time.set_title(
                "SIS Dynamics",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )

        else:
            # Classic SIR model.
            i_arr = result.n2
            r_arr = (
                result.n3 if result.n3 is not None else np.zeros_like(t)
            )

            if is_disc:
                self.ax_time.step(
                    t, s_arr, where="post", color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.step(
                    t, i_arr, where="post", color=c_i, linewidth=2.2,
                    label=result.n2_label,
                )
                self.ax_time.step(
                    t, r_arr, where="post", color=c_r, linewidth=2.0,
                    label=result.n3_label or "Recovered (R)",
                )
                self.ax_time.fill_between(
                    t, i_arr, step="post", color=c_i, alpha=0.15
                )
                self.ax_time.plot(
                    t, i_arr, "o", color=c_i, markersize=3.0, alpha=0.85
                )
                self.ax_time.xaxis.set_major_locator(
                    MaxNLocator(integer=True)
                )
            else:
                self.ax_time.plot(
                    t, s_arr, color=c_s, linewidth=2.0,
                    label=result.n1_label,
                )
                self.ax_time.plot(
                    t, i_arr, color=c_i, linewidth=2.2,
                    label=result.n2_label,
                )
                self.ax_time.plot(
                    t, r_arr, color=c_r, linewidth=2.0,
                    label=result.n3_label or "Recovered (R)",
                )
                self.ax_time.fill_between(
                    t, i_arr, color=c_i, alpha=0.15
                )

            s0 = s_arr[0]
            if beta > 0 and gamma > 0:
                s_c = gamma / beta
                if s_c < s0:
                    self.ax_time.axhline(
                        s_c, color=c_thresh, linestyle="--", alpha=0.6,
                        label=f"Threshold (S_c = {int(round(s_c))})",
                    )
            self.ax_time.set_title(
                "SIR Dynamics",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )

        x_lbl = "Generations / Steps (t)" if is_disc else "Time (t)"
        self.ax_time.set_xlabel(
            x_lbl, fontsize=10, color=colors["subtext_color"]
        )
        self.ax_time.set_ylabel(
            "Population Count", fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_time.legend(
            loc="best", framealpha=0.85,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"], fontsize=8.5,
        )
        self.ax_time.grid(
            True, linestyle="--", alpha=0.35, color=colors["grid"]
        )

        # -------------------------------------------------------------
        # 2. Right Subplot: Phase Portrait & Vector Trajectory
        # -------------------------------------------------------------
        if "SIS" in model.name:
            # Trajectory in (S, I) plane with conservation line.
            i_phase = result.n2
            n_tot = s_arr[0] + i_phase[0]
            self.ax_phase.plot(
                [0, n_tot], [n_tot, 0], "--", color=c_thresh, alpha=0.5,
                label=f"Constraint (S+I = {int(round(n_tot))})",
            )
            self.ax_phase.plot(
                s_arr, i_phase, color=colors["trajectory"],
                linewidth=2.2, label="Infection Path",
            )
            self.ax_phase.plot(
                s_arr[0], i_phase[0], "o", color=colors["start"],
                markersize=8, markeredgecolor="black",
                markeredgewidth=1.2,
                label=(
                    f"Start (S={int(round(s_arr[0]))}, "
                    f"I={int(round(i_phase[0]))})"
                ),
            )
            self.ax_phase.plot(
                s_arr[-1], i_phase[-1], "X", color=colors["end"],
                markersize=9, markeredgecolor="black",
                markeredgewidth=1.2,
                label=(
                    f"Final (S={int(round(s_arr[-1]))}, "
                    f"I={int(round(i_phase[-1]))})"
                ),
            )

            r0 = (beta * n_tot) / gamma if gamma > 0 else 0.0
            if r0 > 1.0:
                i_star = n_tot * (1.0 - 1.0 / r0)
                s_star = n_tot / r0
                self.ax_phase.plot(
                    s_star, i_star, "*", color="#fbbf24",
                    markersize=12, markeredgecolor="black",
                    markeredgewidth=1.0,
                    label=f"Endemic (I* = {int(round(i_star))})",
                )

            # Vector field in (S, I).
            s_max = max(1.0, float(np.max(s_arr))) * 1.05
            i_max = max(1.0, float(np.max(i_phase))) * 1.15
            s_grid = np.linspace(0.0, s_max, 15)
            i_grid = np.linspace(0.0, i_max, 15)
            sg, ig = np.meshgrid(s_grid, i_grid)
            ds = -beta * sg * ig + gamma * ig
            di = beta * sg * ig - gamma * ig
            mag = np.hypot(ds, di)
            mag[mag == 0] = 1.0
            self.ax_phase.quiver(
                sg, ig, ds / mag, di / mag,
                color=colors["subtext_color"],
                alpha=0.25, angles="xy",
            )
            self.ax_phase.set_title(
                "Phase Portrait (S, I)",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )
        else:
            # SIR and SEIR: Infectious (I) vs Susceptible (S).
            i_phase = (
                result.n3
                if "SEIR" in model.name and result.n3 is not None
                else result.n2
            )
            self.ax_phase.plot(
                s_arr, i_phase, color=colors["trajectory"],
                linewidth=2.2, label="Epidemic Path (S, I)",
            )
            self.ax_phase.plot(
                s_arr[0], i_phase[0], "o", color=colors["start"],
                markersize=8, markeredgecolor="black",
                markeredgewidth=1.2,
                label=(
                    f"Start (S={int(round(s_arr[0]))}, "
                    f"I={int(round(i_phase[0]))})"
                ),
            )
            peak_idx = int(np.argmax(i_phase))
            self.ax_phase.plot(
                s_arr[peak_idx], i_phase[peak_idx], "D",
                color="#fbbf24", markersize=8,
                markeredgecolor="black", markeredgewidth=1.2,
                label=f"Peak (I = {int(round(i_phase[peak_idx]))})",
            )
            self.ax_phase.plot(
                s_arr[-1], i_phase[-1], "X", color=colors["end"],
                markersize=9, markeredgecolor="black",
                markeredgewidth=1.2,
                label=(
                    f"Final (S={int(round(s_arr[-1]))}, "
                    f"I={int(round(i_phase[-1]))})"
                ),
            )

            # Threshold S_c = gamma / beta.
            if beta > 0 and gamma > 0:
                s_c = gamma / beta
                s_max = max(1.0, float(np.max(s_arr)))
                if s_c <= s_max * 1.2:
                    self.ax_phase.axvline(
                        s_c, color=c_thresh, linestyle="--",
                        alpha=0.75,
                        label=f"Threshold (S_c = {int(round(s_c))})",
                    )

            # Vector field in (S, I).
            s_max = max(1.0, float(np.max(s_arr))) * 1.05
            i_max = max(1.0, float(np.max(i_phase))) * 1.15
            s_grid = np.linspace(0.0, s_max, 15)
            i_grid = np.linspace(0.0, i_max, 15)
            sg, ig = np.meshgrid(s_grid, i_grid)
            ds = -beta * sg * ig
            di = beta * sg * ig - gamma * ig
            mag = np.hypot(ds, di)
            mag[mag == 0] = 1.0
            self.ax_phase.quiver(
                sg, ig, ds / mag, di / mag,
                color=colors["subtext_color"],
                alpha=0.25, angles="xy",
            )
            self.ax_phase.set_title(
                "Phase Portrait (S, I)",
                fontsize=10.5,
                fontweight="bold",
                color=colors["text_color"],
                pad=10,
            )

        self.ax_phase.set_xlabel(
            "Susceptible Population (S)", fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_phase.set_ylabel(
            "Infectious Population (I)", fontsize=10,
            color=colors["subtext_color"],
        )
        self.ax_phase.legend(
            loc="best", framealpha=0.85,
            facecolor=colors["legend_face"],
            edgecolor=colors["legend_edge"], fontsize=8.5,
        )
        self.ax_phase.grid(
            True, linestyle="--", alpha=0.35, color=colors["grid"]
        )

    def _update_plot_single_variable(
        self,
        result: SimulationResult,
        model: BiologicalModel,
        colors: dict,
    ) -> None:
        """Render single-species dynamics:
        time-series trajectory and 1D phase space.
        """
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

    def _update_plot_frequency_model(
        self,
        result: SimulationResult,
        model: BiologicalModel,
        colors: dict,
    ) -> None:
        # Render allele frequency dynamics and selection phase.
        t = result.t
        p_arr = result.n1
        q_arr = result.n2
        c1 = colors["n1"]
        c2 = colors["n2"]
        params = result.parameters
        is_disc = result.metadata.get("mode") == "discrete"

        # -------------------------------------------------------------
        # 1. Left Subplot: Allele Frequency Dynamics Over Time
        # -------------------------------------------------------------
        if is_disc:
            self.ax_time.step(
                t,
                p_arr,
                where="post",
                color=c1,
                linewidth=2.2,
                label=result.n1_label,
            )
            self.ax_time.step(
                t,
                q_arr,
                where="post",
                color=c2,
                linewidth=2.2,
                label=result.n2_label,
            )
            self.ax_time.fill_between(
                t, p_arr, step="post", color=c1, alpha=0.12
            )
            self.ax_time.fill_between(
                t, q_arr, step="post", color=c2, alpha=0.12
            )
            self.ax_time.plot(
                t, p_arr, "o", color=c1, markersize=3.5, alpha=0.9
            )
            self.ax_time.plot(
                t, q_arr, "o", color=c2, markersize=3.5, alpha=0.9
            )
            self.ax_time.xaxis.set_major_locator(
                MaxNLocator(integer=True)
            )
        else:
            self.ax_time.plot(
                t, p_arr, color=c1, linewidth=2.2, label=result.n1_label
            )
            self.ax_time.plot(
                t, q_arr, color=c2, linewidth=2.2, label=result.n2_label
            )
            self.ax_time.fill_between(t, p_arr, color=c1, alpha=0.12)
            self.ax_time.fill_between(t, q_arr, color=c2, alpha=0.12)

        self.ax_time.set_title(
            "Allele Frequencies (p, q)",
            fontsize=10.0,
            fontweight="bold",
            color=colors["text_color"],
            pad=8,
        )
        time_unit = "Generations (t)" if is_disc else "Time (t)"
        self.ax_time.set_xlabel(
            time_unit,
            fontsize=9.5,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_ylabel(
            "Frequency",
            fontsize=9.5,
            fontweight="bold",
            color=colors["subtext_color"],
        )
        self.ax_time.set_xlim(left=t[0], right=t[-1])
        self.ax_time.set_ylim(bottom=-0.02, top=1.05)
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
        # 2. Right Subplot: Selection Gradient / Discrete Return Map
        # -------------------------------------------------------------
        p_grid = np.linspace(0.0, 1.0, 200)

        if is_disc:
            # Discrete Return Map: p(t+1) vs p(t)
            next_grid = np.array([
                model.discrete_step(
                    np.array([val, 1.0 - val]), params
                )[0]
                for val in p_grid
            ])
            self.ax_phase.plot(
                p_grid,
                p_grid,
                linestyle="--",
                color=colors["grid"],
                linewidth=1.3,
                label="1:1 Line (p(t+1) = p(t))",
            )
            self.ax_phase.plot(
                p_grid,
                next_grid,
                color=c1,
                linewidth=2.2,
                label="Return Map p(t+1)",
            )

            # Markers for start and end points
            start_p = p_arr[0]
            end_p = p_arr[-1]
            next_start = model.discrete_step(
                np.array([start_p, 1.0 - start_p]), params
            )[0]
            next_end = model.discrete_step(
                np.array([end_p, 1.0 - end_p]), params
            )[0]
            self.ax_phase.scatter(
                [start_p],
                [next_start],
                color=colors["start"],
                s=80,
                zorder=6,
                edgecolors="black",
                linewidths=1.2,
                label=f"Start (p₀={start_p:.2f})",
            )
            self.ax_phase.scatter(
                [end_p],
                [next_end],
                color=colors["end"],
                s=70,
                zorder=6,
                marker="X",
                edgecolors="black",
                linewidths=1.2,
                label=f"End (p={end_p:.2f})",
            )

            self.ax_phase.set_title(
                "Return Map: p(t+1)",
                fontsize=10.0,
                fontweight="bold",
                color=colors["text_color"],
                pad=8,
            )
            self.ax_phase.set_xlabel(
                "Current Frequency p(t)",
                fontsize=9.5,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_ylabel(
                "Next Frequency p(t+1)",
                fontsize=9.5,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_xlim(left=0.0, right=1.0)
            self.ax_phase.set_ylim(bottom=-0.02, top=1.05)

        else:
            # Continuous Selection Gradient: dp/dt vs p (Figure 3.6)
            rate_grid = np.array([
                model.rhs(0.0, np.array([val, 1.0 - val]), params)[0]
                for val in p_grid
            ])
            self.ax_phase.axhline(
                0.0,
                linestyle="--",
                color=colors["grid"],
                linewidth=1.3,
                label="Neutral (dp/dt = 0)",
            )
            self.ax_phase.plot(
                p_grid,
                rate_grid,
                color=c1,
                linewidth=2.2,
                label="Selection Rate dp/dt",
            )

            # Check for polymorphic equilibrium p* in diploid model
            if (
                "W_AA" in params
                and "W_Aa" in params
                and "W_aa" in params
            ):
                w11 = params["W_AA"]
                w12 = params["W_Aa"]
                w22 = params["W_aa"]
                denom = w11 - 2.0 * w12 + w22
                if abs(denom) > 1e-6:
                    p_star = (w22 - w12) / denom
                    if 0.001 < p_star < 0.999:
                        self.ax_phase.scatter(
                            [p_star],
                            [0.0],
                            color=colors["isocline1"],
                            s=75,
                            zorder=6,
                            edgecolors="black",
                            linewidths=1.2,
                            label=f"Polymorphic p* ({p_star:.2f})",
                        )

            # Trajectory on rate curve
            start_p = p_arr[0]
            end_p = p_arr[-1]
            r_start = model.rhs(
                0.0, np.array([start_p, 1.0 - start_p]), params
            )[0]
            r_end = model.rhs(
                0.0, np.array([end_p, 1.0 - end_p]), params
            )[0]
            self.ax_phase.scatter(
                [start_p],
                [r_start],
                color=colors["start"],
                s=80,
                zorder=6,
                edgecolors="black",
                linewidths=1.2,
                label=f"Start (p₀={start_p:.2f})",
            )
            self.ax_phase.scatter(
                [end_p],
                [r_end],
                color=colors["end"],
                s=70,
                zorder=6,
                marker="X",
                edgecolors="black",
                linewidths=1.2,
                label=f"End (p={end_p:.2f})",
            )

            self.ax_phase.set_title(
                "Selection Rate: dp/dt",
                fontsize=10.0,
                fontweight="bold",
                color=colors["text_color"],
                pad=8,
            )
            self.ax_phase.set_xlabel(
                "Allele A Frequency (p)",
                fontsize=9.5,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_ylabel(
                "Rate of Change (dp/dt)",
                fontsize=9.5,
                fontweight="bold",
                color=colors["subtext_color"],
            )
            self.ax_phase.set_xlim(left=0.0, right=1.0)
            y_min = min(0.0, float(np.min(rate_grid)))
            y_max = max(0.0, float(np.max(rate_grid)))
            pad_val = max(0.01, (y_max - y_min) * 0.15)
            self.ax_phase.set_ylim(
                bottom=y_min - pad_val, top=y_max + pad_val
            )

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
        """Render two-species dynamics:
        time-series trajectory and phase portrait.
        """
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

    def export_csv(
        self, custom_path: Optional[str] = None
    ) -> Optional[str]:
        """Export current simulation numerical data to a CSV file.

        If custom_path is not provided, opens a native Save File Dialog.
        """
        return self.save(custom_path=custom_path, format_filter="CSV")

    def save_graph_as_jpeg(
        self, custom_path: Optional[str] = None
    ) -> Optional[str]:
        """Export the current figure as a 300 DPI JPEG image.

        If custom_path is not provided, opens a native Save File Dialog.
        """
        return self.save(custom_path=custom_path, format_filter="JPEG")

    def save(
        self,
        custom_path: Optional[str] = None,
        format_filter: Optional[str] = None,
    ) -> Optional[str]:
        """Save simulation as CSV data or image via native file dialog.

        Allows format selection (CSV, JPEG, PNG) through the file dialog
        format dropdown filter.
        """
        if self._current_result is None:
            QMessageBox.warning(
                self,
                "No Data",
                "Please run a simulation first before exporting.",
            )
            return None

        is_interactive = custom_path is None
        if custom_path:
            target_path = custom_path
            chosen_filter = format_filter or ""
        else:
            base_model_name = (
                self._current_result.model_name.replace(" ", "_").lower()
            )
            # Default to CSV or requested filter format.
            if format_filter and "JPEG" in format_filter:
                default_name = f"{base_model_name}_simulation.jpeg"
            elif format_filter and "PNG" in format_filter:
                default_name = f"{base_model_name}_simulation.png"
            else:
                default_name = f"{base_model_name}_simulation.csv"

            filter_str = (
                "CSV Data (*.csv);;"
                "JPEG Image (*.jpeg *.jpg);;"
                "PNG Image (*.png);;"
                "All Files (*)"
            )
            target_path, chosen_filter = QFileDialog.getSaveFileName(
                self,
                "Save Simulation Data or Graph",
                default_name,
                filter_str,
            )

        if not target_path:
            return None

        # Determine format from file extension or selected filter.
        ext = os.path.splitext(target_path)[1].lower()
        if ext == ".csv":
            export_type = "csv"
        elif ext in (".jpeg", ".jpg"):
            export_type = "jpeg"
        elif ext == ".png":
            export_type = "png"
        else:
            if "PNG" in chosen_filter:
                export_type = "png"
                target_path += ".png"
            elif "JPEG" in chosen_filter:
                export_type = "jpeg"
                target_path += ".jpeg"
            else:
                export_type = "csv"
                target_path += ".csv"

        os.makedirs(
            os.path.dirname(os.path.abspath(target_path)), exist_ok=True
        )

        if export_type == "csv":
            try:
                export_simulation_to_csv(
                    self._current_result, target_path
                )
                self.export_completed.emit(target_path)
                if is_interactive:
                    QMessageBox.information(
                        self,
                        "Data Exported",
                        f"Successfully saved simulation data to:\n"
                        f"{target_path}",
                    )
                return target_path
            except Exception as e:
                if is_interactive:
                    QMessageBox.critical(
                        self,
                        "Export Error",
                        f"Failed to export CSV data:\n{e}",
                    )
                return None

        colors = get_plot_colors(self.theme)
        is_png = export_type == "png"
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
            if is_interactive:
                fmt_name = "PNG" if is_png else "JPEG"
                QMessageBox.information(
                    self,
                    "Graph Exported",
                    f"Successfully saved {fmt_name} image to:\n"
                    f"{target_path}",
                )
            return target_path
        except Exception as e:
            if is_interactive:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to save image:\n{e}",
                )
            return None

    def resizeEvent(self, event):
        """Debounce layout recalculation during window/drawer resize."""
        super().resizeEvent(event)
        if self._current_result is not None:
            self._resize_timer.start()

    def _on_resize_debounced(self):
        # Execute tight layout once after resize or drawer slide ends.
        if self._current_result is not None:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    self.figure.tight_layout(
                        pad=1.8, w_pad=3.2, rect=(0.02, 0.02, 0.98, 0.98)
                    )
                    self.canvas.draw_idle()
            except Exception:
                pass
