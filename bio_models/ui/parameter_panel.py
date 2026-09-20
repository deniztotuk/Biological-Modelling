"""
Dynamic Parameter Panel.
Generates input fields, preset selectors, and simulation controls.
"""

from typing import Dict, Any, Optional
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QScrollArea,
    QFrame,
    QGroupBox,
)

from bio_models.models import BiologicalModel, LotkaVolterraCompetitionModel, ConsumerResourceModel
from bio_models.presets import PRESETS


class ParameterPanel(QWidget):
    """
    Panel providing inputs for initial states, parameters, and presets.
    """

    simulate_requested = pyqtSignal()
    relationship_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model: Optional[BiologicalModel] = None
        self.mode: str = "continuous"
        self._param_inputs: Dict[str, QDoubleSpinBox] = {}

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

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ParamScrollContent")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(12)

        scroll.setWidget(self.scroll_content)
        main_layout.addWidget(scroll)

        # Persistent Action Button at bottom
        self.run_btn = QPushButton("▶ Run Simulation & Update Plot")
        self.run_btn.setObjectName("SimulateButton")
        self.run_btn.setToolTip("Run simulation (Shortcut: Enter)")
        self.run_btn.clicked.connect(self.simulate_requested.emit)
        main_layout.addWidget(self.run_btn)

    def set_model(self, model: BiologicalModel, mode: str = "continuous"):
        self.model = model
        self.mode = mode
        self._build_panel_content()

    def _build_panel_content(self):
        # Clear existing layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._param_inputs.clear()

        if not self.model:
            return

        # 1. Header with Model Name and Mode Badge
        header_box = QVBoxLayout()
        header_box.setSpacing(4)

        title_lbl = QLabel(self.model.name)
        title_lbl.setObjectName("ModelTitle")
        title_lbl.setWordWrap(True)
        header_box.addWidget(title_lbl)

        badge_layout = QHBoxLayout()
        mode_text = "Continuous ODE (Runge-Kutta RK45)" if self.mode == "continuous" else "Discrete Recursion (Eq 3.14)"
        mode_badge = QLabel(mode_text)
        mode_badge.setObjectName("ModelBadge")
        badge_layout.addWidget(mode_badge)

        # Relationship badge for competition
        if isinstance(self.model, LotkaVolterraCompetitionModel):
            self.rel_badge = QLabel("Competitive (+ / +)")
            self.rel_badge.setObjectName("RelationshipBadge")
            badge_layout.addWidget(self.rel_badge)
        else:
            self.rel_badge = None

        badge_layout.addStretch()
        header_box.addLayout(badge_layout)
        self.content_layout.addLayout(header_box)

        # 2. Presets Selector
        model_presets = PRESETS.get(self.model.name, [])
        if model_presets:
            preset_group = QGroupBox("Biological Scenarios && Presets")
            preset_layout = QVBoxLayout(preset_group)
            preset_layout.setSpacing(6)

            self.preset_combo = QComboBox()
            for p in model_presets:
                self.preset_combo.addItem(p["name"], p)

            self.preset_desc = QLabel(model_presets[0]["description"])
            self.preset_desc.setObjectName("PresetDescLabel")
            self.preset_desc.setWordWrap(True)

            self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)

            load_btn = QPushButton("Apply Selected Scenario")
            load_btn.setObjectName("PresetButton")
            load_btn.clicked.connect(self._apply_current_preset)

            preset_layout.addWidget(self.preset_combo)
            preset_layout.addWidget(self.preset_desc)
            preset_layout.addWidget(load_btn)
            self.content_layout.addWidget(preset_group)

        # 3. Modular Function Selector (Only for Modular Consumer-Resource)
        if "Modular" in self.model.name and isinstance(self.model, ConsumerResourceModel):
            mod_group = QGroupBox("Modular Function Selection (Table 3.3)")
            mod_layout = QGridLayout(mod_group)
            mod_layout.setSpacing(8)

            mod_layout.addWidget(QLabel("Resource Renewal f(n₁):"), 0, 0)
            self.f_combo = QComboBox()
            self.f_combo.addItems([
                "logistic (r·n₁·(1 - n₁/K))",
                "constant_inflow (θ)",
                "constant_outflow (-ψ)",
                "exponential (r·n₁)",
                "exponential_decline (r·n₁·e^(-a·n₁))",
            ])
            mod_layout.addWidget(self.f_combo, 0, 1)

            mod_layout.addWidget(QLabel("Consumption Rate g(n₁, n₂):"), 1, 0)
            self.g_combo = QComboBox()
            self.g_combo.addItems([
                "type_2_saturating (Holling II: ac·n₁/(b+n₁)·n₂)",
                "type_1_linear (Type I: ac·n₁·n₂)",
                "type_3_generalized (Holling III: ac·n₁^k/(b+n₁^k)·n₂)",
            ])
            mod_layout.addWidget(self.g_combo, 1, 1)

            mod_layout.addWidget(QLabel("Consumer Mortality h(n₂):"), 2, 0)
            self.h_combo = QComboBox()
            self.h_combo.addItems([
                "density_dependent_death ((δ + γ·n₂)·n₂)",
                "linear_death (δ·n₂)",
            ])
            mod_layout.addWidget(self.h_combo, 2, 1)

            self.f_combo.currentIndexChanged.connect(self._on_modular_changed)
            self.g_combo.currentIndexChanged.connect(self._on_modular_changed)
            self.h_combo.currentIndexChanged.connect(self._on_modular_changed)

            self.content_layout.addWidget(mod_group)

        # 4. Initial Conditions & Simulation Settings
        sim_group = QGroupBox("Initial Conditions && Time Span")
        sim_layout = QGridLayout(sim_group)
        sim_layout.setSpacing(8)

        # Initial n1 (Positive integers only: 1, 2, 3...)
        sim_layout.addWidget(QLabel(f"Initial {self.model.n1_label}:"), 0, 0)
        self.n1_init_spin = QSpinBox()
        self.n1_init_spin.setRange(1, 1000000)
        self.n1_init_spin.setValue(25)
        self.n1_init_spin.setSingleStep(1)
        self.n1_init_spin.setToolTip("Initial population count (must be a positive integer ≥ 1)")
        sim_layout.addWidget(self.n1_init_spin, 0, 1)

        # Initial n2 (Positive integers only: 1, 2, 3...)
        sim_layout.addWidget(QLabel(f"Initial {self.model.n2_label}:"), 1, 0)
        self.n2_init_spin = QSpinBox()
        self.n2_init_spin.setRange(1, 1000000)
        self.n2_init_spin.setValue(15)
        self.n2_init_spin.setSingleStep(1)
        self.n2_init_spin.setToolTip("Initial population count (must be a positive integer ≥ 1)")
        sim_layout.addWidget(self.n2_init_spin, 1, 1)

        # Initial Time (t_start / t0)
        start_label = "Start Time (t₀ / t_start):" if self.mode == "continuous" else "Start Step (t₀):"
        sim_layout.addWidget(QLabel(start_label), 2, 0)
        self.t_start_spin = QDoubleSpinBox()
        self.t_start_spin.setRange(-10000.0, 100000.0)
        self.t_start_spin.setValue(0.0)
        self.t_start_spin.setSingleStep(1.0)
        self.t_start_spin.setToolTip("Initial simulation time point (can start at 0 or any arbitrary value)")
        self.t_start_spin.valueChanged.connect(self._on_t_start_changed)
        sim_layout.addWidget(self.t_start_spin, 2, 1)

        # End Time (t_end / t_max)
        end_label = "End Time (t_end):" if self.mode == "continuous" else "End Step (t_end):"
        sim_layout.addWidget(QLabel(end_label), 3, 0)
        self.t_end_spin = QDoubleSpinBox()
        self.t_end_spin.setRange(-10000.0, 100000.0)
        self.t_end_spin.setValue(50.0)
        self.t_end_spin.setSingleStep(5.0)
        self.t_end_spin.setToolTip("Final simulation time point (must be greater than start time)")
        sim_layout.addWidget(self.t_end_spin, 3, 1)

        # Sampling points
        sim_layout.addWidget(QLabel("Output Resolution Points:"), 4, 0)
        self.points_spin = QSpinBox()
        self.points_spin.setRange(50, 5000)
        self.points_spin.setValue(500)
        self.points_spin.setSingleStep(50)
        sim_layout.addWidget(self.points_spin, 4, 1)

        self.content_layout.addWidget(sim_group)

        # 5. Model Parameters
        param_group = QGroupBox("Model Parameters")
        param_layout = QGridLayout(param_group)
        param_layout.setSpacing(8)

        defaults = self.model.default_params
        meta = self.model.param_meta

        row = 0
        for p_key, p_val in defaults.items():
            info = meta.get(p_key, {"label": p_key, "min": -100.0, "max": 1000.0, "step": 0.05, "description": ""})
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
            if isinstance(self.model, LotkaVolterraCompetitionModel) and p_key in ("alpha12", "alpha21"):
                spin.valueChanged.connect(self._update_relationship_badge)

            param_layout.addWidget(spin, row, 1)
            self._param_inputs[p_key] = spin
            row += 1

        self.content_layout.addWidget(param_group)
        self.content_layout.addStretch()

        if isinstance(self.model, LotkaVolterraCompetitionModel):
            self._update_relationship_badge()

    def _on_preset_changed(self, idx: int):
        data = self.preset_combo.currentData()
        if data:
            self.preset_desc.setText(data.get("description", ""))

    def _on_t_start_changed(self, val: float):
        if hasattr(self, "t_end_spin") and self.t_end_spin.value() <= val:
            self.t_end_spin.setValue(val + 10.0)

    def _apply_current_preset(self):
        data = self.preset_combo.currentData()
        if not data:
            return

        if "initial" in data:
            self.n1_init_spin.setValue(int(round(data["initial"][0])))
            self.n2_init_spin.setValue(int(round(data["initial"][1])))

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
        if not isinstance(self.model, LotkaVolterraCompetitionModel) or not self.rel_badge:
            return
        a12 = self._param_inputs.get("alpha12", None)
        a21 = self._param_inputs.get("alpha21", None)
        if a12 is not None and a21 is not None:
            rel = self.model.classify_relationship(a12.value(), a21.value())
            self.rel_badge.setText(rel)
            self.relationship_changed.emit(rel)

    def get_simulation_inputs(self) -> Dict[str, Any]:
        """Extract all current user inputs from the UI."""
        params = {k: spin.value() for k, spin in self._param_inputs.items()}
        return {
            "model": self.model,
            "mode": self.mode,
            "initial_state": (int(self.n1_init_spin.value()), int(self.n2_init_spin.value())),
            "t_span": (self.t_start_spin.value(), self.t_end_spin.value()),
            "num_points": self.points_spin.value(),
            "params": params,
        }
