"""
Main Application Window.
Integrates Sandwich Drawer, Parameter Panel, and Canvas Widget.
"""

from PyQt6.QtCore import Qt, QKeyCombination
from PyQt6.QtGui import QKeySequence, QShortcut, QAction
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStatusBar,
    QSplitter,
    QToolBar,
)

from bio_models.models import BiologicalModel, AVAILABLE_MODELS
from bio_models.engine import simulate_model
from bio_models.ui.sandwich_menu import SandwichDrawer
from bio_models.ui.parameter_panel import ParameterPanel
from bio_models.ui.canvas_widget import BioPlotCanvas
from bio_models.ui.styles import APP_STYLESHEET


class MainWindow(QMainWindow):
    """
    Main desktop application window for biological interaction modeling.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BioModel Studio — Ecology & Evolutionary Dynamics (Otto & Day)")
        self.resize(1340, 820)
        self.setMinimumSize(950, 600)

        self.setStyleSheet(APP_STYLESHEET)

        self._init_ui()
        self._setup_shortcuts()

        # Load initial model (Lotka-Volterra Competition)
        initial_model = AVAILABLE_MODELS[0]
        self.drawer._handle_selection(initial_model, "continuous")

    def _init_ui(self):
        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -------------------------------------------------------------
        # 1. Top Application Bar
        # -------------------------------------------------------------
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #0f172a; border-bottom: 1px solid #1e293b;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(14, 10, 16, 10)
        top_layout.setSpacing(12)

        # Hamburger / Sandwich Menu Toggle Button
        self.menu_toggle_btn = QPushButton("☰  Models Menu")
        self.menu_toggle_btn.setObjectName("SandwichToggleBtn")
        self.menu_toggle_btn.setToolTip("Toggle Models Navigation Menu (Shortcut: Ctrl+M / Cmd+M)")
        self.menu_toggle_btn.clicked.connect(self._toggle_menu)
        top_layout.addWidget(self.menu_toggle_btn)

        app_title = QLabel("BioModel Studio")
        app_title.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;")
        top_layout.addWidget(app_title)

        subtitle = QLabel("• Predator-Prey, Competition & Consumer-Resource Dynamics")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 12px;")
        top_layout.addWidget(subtitle)

        top_layout.addStretch()

        help_text = QLabel("Press [Enter] to Run | [Ctrl+S] Save JPEG")
        help_text.setStyleSheet("color: #64748b; font-size: 11px;")
        top_layout.addWidget(help_text)

        root_layout.addWidget(top_bar)

        # -------------------------------------------------------------
        # 2. Main Body Splitter Layout (Drawer + Parameters + Plot)
        # -------------------------------------------------------------
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Sandwich Navigation Drawer (Collapsible)
        self.drawer = SandwichDrawer()
        self.drawer.model_selected.connect(self._on_model_selected)
        body_layout.addWidget(self.drawer)

        # Splitter between Parameter Panel and Canvas
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setHandleWidth(4)
        content_splitter.setStyleSheet("QSplitter::handle { background-color: #e2e8f0; }")

        # Parameter Input Panel
        self.param_panel = ParameterPanel()
        self.param_panel.setMinimumWidth(320)
        self.param_panel.setMaximumWidth(460)
        self.param_panel.simulate_requested.connect(self.run_simulation)
        content_splitter.addWidget(self.param_panel)

        # Visualization Canvas
        self.canvas_widget = BioPlotCanvas()
        self.canvas_widget.export_completed.connect(self._on_export_completed)
        content_splitter.addWidget(self.canvas_widget)

        # Set initial splitter proportions (35% params, 65% plot)
        content_splitter.setSizes([380, 720])

        body_layout.addWidget(content_splitter, stretch=1)
        root_layout.addLayout(body_layout, stretch=1)

        # -------------------------------------------------------------
        # 3. Status Bar
        # -------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. Select a model or scenario to begin.")

    def _setup_shortcuts(self):
        # Shortcut: Enter or Return runs simulation
        run_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        run_shortcut.activated.connect(self.run_simulation)

        run_shortcut_enter = QShortcut(QKeySequence(Qt.Key.Key_Enter), self)
        run_shortcut_enter.activated.connect(self.run_simulation)

        # Shortcut: Ctrl+M / Cmd+M toggles sandwich menu
        menu_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        menu_shortcut.activated.connect(self._toggle_menu)

        # Shortcut: Ctrl+S / Cmd+S exports JPEG
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(lambda: self.canvas_widget.save_graph_as_jpeg())

    def _toggle_menu(self):
        self.drawer.toggle_collapse()
        if self.drawer.is_collapsed:
            self.menu_toggle_btn.setText("☰  Models Menu")
        else:
            self.menu_toggle_btn.setText("✕  Hide Menu")

    def _on_model_selected(self, model: BiologicalModel, mode: str):
        self.param_panel.set_model(model, mode)
        self.status_bar.showMessage(f"Selected: {model.name} [{mode}]")
        self.run_simulation()

    def run_simulation(self):
        inputs = self.param_panel.get_simulation_inputs()
        model = inputs["model"]
        if not model:
            return

        self.status_bar.showMessage(f"Simulating {model.name}...")
        result = simulate_model(
            model=model,
            initial_state=inputs["initial_state"],
            t_span=inputs["t_span"],
            num_points=inputs["num_points"],
            params=inputs["params"],
            mode=inputs["mode"],
        )

        self.canvas_widget.update_plot(result, model)
        self.status_bar.showMessage(result.message)

    def _on_export_completed(self, path: str):
        self.status_bar.showMessage(f"Graph successfully exported to JPEG: {path}", 6000)
