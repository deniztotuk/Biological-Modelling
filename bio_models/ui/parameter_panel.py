"""
Dynamic Parameter Panel.
Generates input fields, preset selectors, and simulation controls.
"""

from typing import Any, Dict, Optional
from PyQt6.QtCore import QPoint, QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from bio_models.model_info import get_model_info_html
from bio_models.models import (
    BiologicalModel,
    ConsumerResourceModel,
    LotkaVolterraCompetitionModel,
)
from bio_models.presets import PRESETS
from bio_models.ui.styles import get_info_icon, get_play_icon


class ModelInfoButton(QPushButton):
    """Small circular info badge displaying model equations and scenarios."""

    def __init__(self, theme: str = "dark", parent=None):
        super().__init__(parent)
        self.setObjectName("ModelInfoButton")
        self.theme = theme
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(18, 18)
        self._info_html = ""
        self.update_icon()
        self.clicked.connect(self._show_info)

    def update_icon(self):
        self.setIcon(get_info_icon(self.theme))
        self.setIconSize(QSize(16, 16))

    def set_theme(self, theme: str):
        self.theme = theme
        self.update_icon()

    def set_info_html(self, html: str):
        self._info_html = html
        self.setToolTip(html)

    def _show_info(self):
        if self._info_html:
            p = self.mapToGlobal(QPoint(self.width() + 6, -10))
            QToolTip.showText(p, self._info_html, self)

    def enterEvent(self, event):
        super().enterEvent(event)
        self._show_info()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        QToolTip.hideText()


class ParameterPanel(QWidget):
    """
    Panel providing inputs for initial states, parameters, and presets.
    """

    simulate_requested = pyqtSignal()
    relationship_changed = pyqtSignal(str)

    def __init__(self, theme: str = "dark", parent=None):
        super().__init__(parent)
        self.theme = theme
        self.model: Optional[BiologicalModel] = None
        self.mode: str = "continuous"
        self._param_inputs: Dict[str, QDoubleSpinBox] = {}
        self._just_changed_index: bool = False
        self.mode_badge: Optional[QPushButton] = None
        self.start_time_lbl: Optional[QLabel] = None
        self.end_time_lbl: Optional[QLabel] = None
        self.points_lbl: Optional[QLabel] = None
        self.points_spin: Optional[QSpinBox] = None
        self.info_btn: Optional[ModelInfoButton] = None

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Scroll area for parameters
        scroll = QScrollArea()
        scroll.setObjectName("ParamScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ParamScrollContent")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(8, 8, 14, 8)
        self.content_layout.setSpacing(12)

        scroll.setWidget(self.scroll_content)
        main_layout.addWidget(scroll)

        # Persistent Action Button at bottom
        self.run_btn = QPushButton("Run Simulation")
        self.run_btn.setObjectName("SimulateButton")
        self.run_btn.setIcon(get_play_icon(self.theme))
        self.run_btn.setIconSize(QSize(13, 13))
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.setToolTip("Run simulation (Shortcut: Enter)")
        self.run_btn.clicked.connect(self.simulate_requested.emit)
        main_layout.addWidget(self.run_btn)

    def set_theme(self, theme: str):
        """Update theme-dependent icons."""
        self.theme = theme
        if hasattr(self, "run_btn"):
            self.run_btn.setIcon(get_play_icon(self.theme))
        if self.info_btn is not None:
            self.info_btn.set_theme(self.theme)
            if self.model:
                self.info_btn.set_info_html(
                    get_model_info_html(self.model.name, self.mode, self.theme)
                )

    def set_model(self, model: BiologicalModel, mode: str = "continuous"):
        self.model = model
        self.mode = mode
        self._build_panel_content()

    def _clear_layout(self, layout):
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self._clear_layout(sub_layout)

    def _configure_combo(self, combo: QComboBox) -> None:
        """Configure combo box to avoid horizontal overflow."""
        combo.setView(QListView())
        combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        combo.setMinimumContentsLength(10)
        combo.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed
        )

    def _build_panel_content(self):
        # Clear existing layout and all children to prevent overlapping text
        self._clear_layout(self.content_layout)
        for child in self.scroll_content.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        self._param_inputs.clear()

        if not self.model:
            return

        # 1. Header with Model Name and Mode Badge
        header_widget = QWidget()
        header_widget.setObjectName("HeaderWidget")
        header_box = QVBoxLayout(header_widget)
        header_box.setContentsMargins(0, 0, 0, 0)
        header_box.setSpacing(6)

        title_lbl = QLabel(self.model.name)
        title_lbl.setObjectName("ModelTitle")
        title_lbl.setWordWrap(True)
        header_box.addWidget(title_lbl)

        badge_layout = QHBoxLayout()
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setSpacing(6)
        mode_text = (
            "Continuous ODE"
            if self.mode == "continuous"
            else "Discrete Recursion"
        )
        self.mode_badge = QPushButton(mode_text)
        self.mode_badge.setObjectName("ModelBadge")
        self.mode_badge.setProperty("mode", self.mode)
        self.mode_badge.setMinimumWidth(135)
        self.mode_badge.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_badge.setToolTip(
            "Click to switch calculation method between Continuous ODE "
            "and Discrete Recursion"
        )
        self.mode_badge.clicked.connect(self._toggle_mode)
        badge_layout.addWidget(self.mode_badge)

        # Relationship badge for competition
        if isinstance(self.model, LotkaVolterraCompetitionModel):
            self.rel_badge = QLabel("Competitive (+ / +)")
            self.rel_badge.setObjectName("RelationshipBadge")
            badge_layout.addWidget(self.rel_badge)
        else:
            self.rel_badge = None

        badge_layout.addStretch()
        header_box.addLayout(badge_layout)
        self.content_layout.addWidget(header_widget)

        # 2. Biological Presets Selector
        presets = PRESETS.get(self.model.name, [])
        if presets:
            preset_group = QGroupBox("Biological Scenarios & Presets")
            preset_layout = QVBoxLayout(preset_group)
            preset_layout.setSpacing(6)

            self.preset_combo = QComboBox()
            self._configure_combo(self.preset_combo)
            for p in presets:
                self.preset_combo.addItem(p["name"], p)
            self.preset_combo.currentIndexChanged.connect(
                self._on_preset_changed
            )
            self.preset_combo.activated.connect(
                self._on_preset_activated
            )

            desc_row = QWidget()
            desc_layout = QHBoxLayout(desc_row)
            desc_layout.setContentsMargins(0, 0, 0, 0)
            desc_layout.setSpacing(6)

            self.preset_desc = QLabel(presets[0]["description"])
            self.preset_desc.setObjectName("PresetDescription")
            self.preset_desc.setWordWrap(True)

            self.info_btn = ModelInfoButton(theme=self.theme)
            info_html = get_model_info_html(
                self.model.name, self.mode, self.theme
            )
            self.info_btn.set_info_html(info_html)

            desc_layout.addWidget(self.preset_desc, stretch=1)
            desc_layout.addWidget(
                self.info_btn,
                alignment=Qt.AlignmentFlag.AlignTop
                | Qt.AlignmentFlag.AlignRight,
            )

            preset_layout.addWidget(self.preset_combo)
            preset_layout.addWidget(desc_row)
            self.content_layout.addWidget(preset_group)

        # 3. Modular Function Selector (Only for Modular Consumer-Resource)
        if (
            "Modular" in self.model.name
            and isinstance(self.model, ConsumerResourceModel)
        ):
            mod_group = QGroupBox("Modular Function Selection")
            mod_layout = QGridLayout(mod_group)
            mod_layout.setSpacing(8)

            mod_layout.addWidget(QLabel("Resource Renewal (f(n₁)):"), 0, 0)
            self.f_combo = QComboBox()
            self._configure_combo(self.f_combo)
            self.f_combo.addItems([
                "logistic (r·n₁·(1 - n₁/K))",
                "constant_inflow (θ)",
                "constant_outflow (-ψ)",
                "exponential (r·n₁)",
                "exponential_decline (r·n₁·e^(-a·n₁))",
            ])
            mod_layout.addWidget(self.f_combo, 0, 1)

            mod_layout.addWidget(
                QLabel("Consumption Rate (g(n₁, n₂)):"), 1, 0
            )
            self.g_combo = QComboBox()
            self._configure_combo(self.g_combo)
            self.g_combo.addItems([
                "type_2_saturating (Holling II: ac·n₁/(b+n₁)·n₂)",
                "type_1_linear (Type I: ac·n₁·n₂)",
                "type_3_generalized (Holling III: ac·n₁^k/(b+n₁^k)·n₂)",
            ])
            mod_layout.addWidget(self.g_combo, 1, 1)

            mod_layout.addWidget(
                QLabel("Consumer Mortality (h(n₂)):"), 2, 0
            )
            self.h_combo = QComboBox()
            self._configure_combo(self.h_combo)
            self.h_combo.addItems([
                "density_dependent_death ((δ + γ·n₂)·n₂)",
                "linear_death (δ·n₂)",
            ])
            mod_layout.addWidget(self.h_combo, 2, 1)

            self.f_combo.currentIndexChanged.connect(self._on_modular_changed)
            self.g_combo.currentIndexChanged.connect(self._on_modular_changed)
            self.h_combo.currentIndexChanged.connect(self._on_modular_changed)

            self.content_layout.addWidget(mod_group)

        # 4. Simulation Settings & Initial Conditions
        sim_group = QGroupBox("Initial Conditions & Time Range")
        sim_layout = QGridLayout(sim_group)
        sim_layout.setSpacing(8)

        # Initial n1 (Positive integers only: 1, 2, 3...)
        sim_layout.addWidget(QLabel(f"Initial {self.model.n1_label}:"), 0, 0)
        self.n1_init_spin = QSpinBox()
        self.n1_init_spin.setRange(1, 1000000)
        if self.model.name == "Exponential Growth Model":
            default_n1 = 8
            default_tend = 5.0
        elif self.model.name == "Logistic Growth Model":
            default_n1 = 5
            default_tend = 20.0
        else:
            default_n1 = 25
            default_tend = 50.0
        self.n1_init_spin.setValue(default_n1)
        self.n1_init_spin.setSingleStep(1)
        self.n1_init_spin.setToolTip(
            "Initial population count (must be a positive integer ≥ 1)")
        sim_layout.addWidget(self.n1_init_spin, 0, 1)

        row_idx = 1
        if not self.model.is_single_variable:
            # Initial n2 (Positive integers only: 1, 2, 3...)
            sim_layout.addWidget(
                QLabel(f"Initial {self.model.n2_label}:"), row_idx, 0
            )
            self.n2_init_spin = QSpinBox()
            self.n2_init_spin.setRange(1, 1000000)
            self.n2_init_spin.setValue(15)
            self.n2_init_spin.setSingleStep(1)
            self.n2_init_spin.setToolTip(
                "Initial population count (must be a positive integer ≥ 1)")
            sim_layout.addWidget(self.n2_init_spin, row_idx, 1)
            row_idx += 1
        else:
            self.n2_init_spin = None

        # Initial Time (t_start / t0)
        start_label = (
            "Start Time (t<sub>start</sub>):"
            if self.mode == "continuous"
            else "Start Step (t<sub>start</sub>):"
        )
        self.start_time_lbl = QLabel(start_label)
        sim_layout.addWidget(self.start_time_lbl, row_idx, 0)
        self.t_start_spin = QDoubleSpinBox()
        self.t_start_spin.setRange(-10000.0, 100000.0)
        self.t_start_spin.setValue(0.0)
        self.t_start_spin.setSingleStep(1.0)
        self.t_start_spin.setToolTip(
            "Initial simulation time point (can start at 0 or any arbitrary "
            "value)"
        )
        self.t_start_spin.valueChanged.connect(self._on_t_start_changed)
        sim_layout.addWidget(self.t_start_spin, row_idx, 1)
        row_idx += 1

        # End Time (t_end / t_max)
        end_label = (
            "End Time (t<sub>end</sub>):"
            if self.mode == "continuous"
            else "End Step (t<sub>end</sub>):"
        )
        self.end_time_lbl = QLabel(end_label)
        sim_layout.addWidget(self.end_time_lbl, row_idx, 0)
        self.t_end_spin = QDoubleSpinBox()
        self.t_end_spin.setRange(-10000.0, 100000.0)
        self.t_end_spin.setValue(default_tend)
        self.t_end_spin.setSingleStep(5.0)
        self.t_end_spin.setToolTip(
            "Final simulation time point (must be greater than start time)")
        sim_layout.addWidget(self.t_end_spin, row_idx, 1)
        row_idx += 1

        # Sampling points
        self.points_lbl = QLabel("Output Resolution Points:")
        sim_layout.addWidget(self.points_lbl, row_idx, 0)
        self.points_spin = QSpinBox()
        self.points_spin.setRange(50, 5000)
        self.points_spin.setValue(500)
        self.points_spin.setSingleStep(50)
        sim_layout.addWidget(self.points_spin, row_idx, 1)

        if self.mode == "discrete":
            self.points_lbl.setVisible(False)
            self.points_spin.setVisible(False)
            self.t_start_spin.setDecimals(0)
            self.t_end_spin.setDecimals(0)
            self.t_start_spin.setSingleStep(1.0)
            self.t_end_spin.setSingleStep(1.0)

        self.content_layout.addWidget(sim_group)

        # 5. Model Parameters
        param_group = QGroupBox("Model Parameters")
        param_layout = QGridLayout(param_group)
        param_layout.setSpacing(8)

        defaults = self.model.default_params
        meta = self.model.param_meta

        row = 0
        for p_key, p_val in defaults.items():
            info = meta.get(
                p_key,
                {
                    "label": p_key,
                    "min": -100.0,
                    "max": 1000.0,
                    "step": 0.05,
                    "description": "",
                },
            )
            lbl = QLabel(info["label"])
            lbl.setToolTip(info.get("description", ""))
            param_layout.addWidget(lbl, row, 0)

            if info.get("is_int", False):
                spin = QSpinBox()
                spin.setRange(int(info["min"]), int(info["max"]))
                spin.setSingleStep(int(info.get("step", 1)))
                spin.setValue(int(round(p_val)))
            else:
                spin = QDoubleSpinBox()
                spin.setRange(float(info["min"]), float(info["max"]))
                spin.setSingleStep(float(info["step"]))
                spin.setDecimals(int(info.get("decimals", 3)))
                spin.setValue(float(p_val))
            spin.setToolTip(info.get("description", ""))

            # Connect changes to relationship classifier if competition
            if (
                isinstance(self.model, LotkaVolterraCompetitionModel)
                and p_key in ("alpha12", "alpha21")
            ):
                spin.valueChanged.connect(self._update_relationship_badge)

            param_layout.addWidget(spin, row, 1)
            self._param_inputs[p_key] = spin
            row += 1

        self.content_layout.addWidget(param_group)
        self.content_layout.addStretch()

        if isinstance(self.model, LotkaVolterraCompetitionModel):
            self._update_relationship_badge()

    def _on_preset_changed(self, idx: int):
        self._just_changed_index = True
        data = self.preset_combo.currentData()
        if data:
            self.preset_desc.setText(data.get("description", ""))
            self._apply_current_preset()

    def _on_preset_activated(self, idx: int):
        if self._just_changed_index:
            self._just_changed_index = False
            return
        self._on_preset_changed(idx)

    def _on_t_start_changed(self, val: float):
        if hasattr(self, "t_end_spin") and self.t_end_spin.value() <= val:
            self.t_end_spin.setValue(val + 10.0)

    def _apply_current_preset(self):
        data = self.preset_combo.currentData()
        if not data:
            return

        if "initial" in data:
            init_vals = data["initial"]
            self.n1_init_spin.setValue(int(round(init_vals[0])))
            if len(init_vals) > 1 and self.n2_init_spin is not None:
                self.n2_init_spin.setValue(int(round(init_vals[1])))

        if "t_span" in data:
            t_span = data["t_span"]
            self.t_start_spin.setValue(float(t_span[0]))
            self.t_end_spin.setValue(float(t_span[1]))

        params = data.get("params", {})
        for k, v in params.items():
            if k in self._param_inputs:
                spin = self._param_inputs[k]
                if isinstance(spin, QSpinBox):
                    spin.setValue(int(round(v)))
                else:
                    spin.setValue(float(v))

        if isinstance(self.model, LotkaVolterraCompetitionModel):
            self._update_relationship_badge()

        # Trigger automatic re-simulation
        self.simulate_requested.emit()

    def _on_modular_changed(self):
        if isinstance(self.model, ConsumerResourceModel):
            f_key = self.f_combo.currentText().split()[0]
            g_key = self.g_combo.currentText().split()[0]
            h_key = self.h_combo.currentText().split()[0]
            self.model.f_type = f_key
            self.model.g_type = g_key
            self.model.h_type = h_key
            self.simulate_requested.emit()

    def _update_relationship_badge(self):
        if (
            not isinstance(self.model, LotkaVolterraCompetitionModel)
            or not self.rel_badge
        ):
            return
        a12 = self._param_inputs.get("alpha12", None)
        a21 = self._param_inputs.get("alpha21", None)
        if a12 is not None and a21 is not None:
            rel = self.model.classify_relationship(a12.value(), a21.value())
            self.rel_badge.setText(rel)
            self.relationship_changed.emit(rel)

    def _toggle_mode(self):
        """Toggle calculation method between continuous and discrete mode."""
        self.mode = "discrete" if self.mode == "continuous" else "continuous"
        is_disc = self.mode == "discrete"
        if self.mode_badge is not None:
            self.mode_badge.setText(
                "Discrete Recursion" if is_disc else "Continuous ODE"
            )
            self.mode_badge.setProperty("mode", self.mode)
            self.mode_badge.style().unpolish(self.mode_badge)
            self.mode_badge.style().polish(self.mode_badge)

        if self.start_time_lbl is not None:
            self.start_time_lbl.setText(
                "Start Step (t<sub>start</sub>):"
                if is_disc
                else "Start Time (t<sub>start</sub>):"
            )
        if self.end_time_lbl is not None:
            self.end_time_lbl.setText(
                "End Step (t<sub>end</sub>):"
                if is_disc
                else "End Time (t<sub>end</sub>):"
            )

        if self.points_lbl is not None:
            self.points_lbl.setVisible(not is_disc)
        if self.points_spin is not None:
            self.points_spin.setVisible(not is_disc)

        if self.t_start_spin is not None:
            self.t_start_spin.setDecimals(0 if is_disc else 2)
            self.t_start_spin.setSingleStep(1.0)
        if self.t_end_spin is not None:
            self.t_end_spin.setDecimals(0 if is_disc else 2)
            self.t_end_spin.setSingleStep(1.0 if is_disc else 5.0)

        if self.info_btn is not None and self.model is not None:
            self.info_btn.set_info_html(
                get_model_info_html(self.model.name, self.mode, self.theme)
            )

        self.simulate_requested.emit()

    def get_simulation_inputs(self) -> Dict[str, Any]:
        """Extract all current user inputs from the UI."""
        params = {k: spin.value() for k, spin in self._param_inputs.items()}
        n2_val = (
            int(self.n2_init_spin.value())
            if self.n2_init_spin is not None
            else 0
        )
        if self.mode == "discrete":
            steps = max(
                1,
                int(
                    round(
                        self.t_end_spin.value() - self.t_start_spin.value()
                    )
                ),
            )
            num_points = steps + 1
        else:
            num_points = (
                self.points_spin.value()
                if self.points_spin is not None
                else 500
            )

        return {
            "model": self.model,
            "mode": self.mode,
            "initial_state": (
                int(self.n1_init_spin.value()),
                n2_val,
            ),
            "t_span": (self.t_start_spin.value(), self.t_end_spin.value()),
            "num_points": num_points,
            "params": params,
        }
