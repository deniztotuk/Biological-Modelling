"""
Main Application Window.
Integrates Sandwich Drawer, Parameter Panel, Canvas Widget,
Native Menu Bar with Settings (Theme selection: Light / Dark), and shortcuts.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from bio_models.models import BiologicalModel, AVAILABLE_MODELS
from bio_models.engine import simulate_model
from bio_models.ui.sandwich_menu import SandwichDrawer
from bio_models.ui.parameter_panel import ParameterPanel
from bio_models.ui.canvas_widget import BioPlotCanvas
from bio_models.ui.styles import get_stylesheet, get_theme_palette


class MainWindow(QMainWindow):
    """
    Main desktop application window for biological interaction modeling.
    Features dynamic Light and Dark theme switching, native menu bar,
    sandwich navigation drawer, parameter controls, and dual-view plotting.
    """

    def __init__(self, default_theme: str = "light"):
        super().__init__()
        self.setWindowTitle(
            "BioModel Studio — Ecology & Evolutionary Dynamics"
        )
        self.resize(1340, 820)
        self.setMinimumSize(950, 600)

        self.current_theme = default_theme

        self._init_menu_bar()
        self._init_ui()
        self._setup_shortcuts()

        # Apply initial theme
        self.apply_theme(self.current_theme)

        # Load initial model (Lotka-Volterra Competition)
        initial_model = AVAILABLE_MODELS[0]
        self.drawer._handle_selection(initial_model, "continuous")

    def _init_menu_bar(self):
        """Create native application menu bar with Settings and Theme
        selection.
        """
        menu_bar = self.menuBar()

        # 1. File Menu
        file_menu = menu_bar.addMenu("&File")

        run_action = QAction("&Run Simulation", self)
        run_action.setShortcut(QKeySequence("Ctrl+R"))
        run_action.setStatusTip("Run simulation and update graph")
        run_action.triggered.connect(self.run_simulation)
        file_menu.addAction(run_action)

        save_action = QAction("&Save Graph as JPEG...", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.setStatusTip(
            "Export current graph as a high-resolution JPEG")
        save_action.triggered.connect(
            lambda: self.canvas_widget.save_graph_as_jpeg())
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # 2. View Menu
        view_menu = menu_bar.addMenu("&View")

        toggle_menu_action = QAction("Toggle &Models Menu", self)
        toggle_menu_action.setShortcut(QKeySequence("Ctrl+M"))
        toggle_menu_action.triggered.connect(self._toggle_menu)
        view_menu.addAction(toggle_menu_action)

        # 3. Settings Menu (Theme Selection)
        settings_menu = menu_bar.addMenu("&Settings")
        theme_menu = settings_menu.addMenu("&Theme")

        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        self.light_theme_action = QAction("&Light Theme", self, checkable=True)
        self.light_theme_action.setChecked(self.current_theme == "light")
        self.light_theme_action.triggered.connect(
            lambda: self.apply_theme("light"))
        theme_group.addAction(self.light_theme_action)
        theme_menu.addAction(self.light_theme_action)

        self.dark_theme_action = QAction("&Dark Theme", self, checkable=True)
        self.dark_theme_action.setChecked(self.current_theme == "dark")
        self.dark_theme_action.triggered.connect(
            lambda: self.apply_theme("dark"))
        theme_group.addAction(self.dark_theme_action)
        theme_menu.addAction(self.dark_theme_action)

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
        self.top_bar = QWidget()
        self.top_bar.setObjectName("TopBar")
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(14, 8, 16, 8)
        top_layout.setSpacing(12)

        # Hamburger / Sandwich Menu Toggle Button
        self.menu_toggle_btn = QPushButton("☰  Models Menu")
        self.menu_toggle_btn.setObjectName("SandwichToggleBtn")
        self.menu_toggle_btn.setToolTip(
            "Toggle Models Navigation Drawer (Shortcut: Ctrl+M / Cmd+M)")
        self.menu_toggle_btn.clicked.connect(self._toggle_menu)
        top_layout.addWidget(self.menu_toggle_btn)

        app_title = QLabel("BioModel Studio")
        app_title.setObjectName("AppTitle")
        top_layout.addWidget(app_title)

        subtitle = QLabel(
            "• Predator-Prey, Competition & Consumer-Resource Dynamics")
        subtitle.setObjectName("AppSubtitle")
        top_layout.addWidget(subtitle)

        top_layout.addStretch()

        help_text = QLabel("[Enter] Run | [Ctrl+S] Save JPEG")
        help_text.setObjectName("AppHelp")
        top_layout.addWidget(help_text)

        # Quick Theme Switcher Button on the bar (reflects current theme)
        self.theme_btn = QPushButton("☀️ Light Mode")
        self.theme_btn.setObjectName("ThemeToggleBtn")
        self.theme_btn.setToolTip(
            "Click to toggle between Light and Dark themes")
        self.theme_btn.clicked.connect(self._toggle_quick_theme)
        top_layout.addWidget(self.theme_btn)

        root_layout.addWidget(self.top_bar)

        # -------------------------------------------------------------
        # 2. Main Body Splitter Layout (Drawer + Parameters + Plot)
        # -------------------------------------------------------------
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Sandwich Navigation Drawer (Collapsible & Responsive)
        self.drawer = SandwichDrawer()
        self.drawer.model_selected.connect(self._on_model_selected)
        self.drawer.adapt_to_window_width(self.width())
        body_layout.addWidget(self.drawer)

        # Splitter between Parameter Panel and Canvas
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setHandleWidth(4)

        # Parameter Input Panel
        self.param_panel = ParameterPanel()
        self.param_panel.setMinimumWidth(370)
        self.param_panel.setMaximumWidth(480)
        self.param_panel.simulate_requested.connect(self.run_simulation)
        content_splitter.addWidget(self.param_panel)

        # Visualization Canvas
        self.canvas_widget = BioPlotCanvas(theme=self.current_theme)
        self.canvas_widget.export_completed.connect(self._on_export_completed)
        content_splitter.addWidget(self.canvas_widget)

        # Proportions: 35% params, 65% plot
        content_splitter.setSizes([380, 720])
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)

        body_layout.addWidget(content_splitter, stretch=1)
        root_layout.addLayout(body_layout, stretch=1)

        # -------------------------------------------------------------
        # 3. Status Bar
        # -------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(
            "Ready. Select a model or scenario to begin.")

    def _setup_shortcuts(self):
        # Enter / Return runs simulation
        run_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        run_shortcut.activated.connect(self.run_simulation)

        run_shortcut_enter = QShortcut(QKeySequence(Qt.Key.Key_Enter), self)
        run_shortcut_enter.activated.connect(self.run_simulation)

        # Ctrl+M / Cmd+M toggles sandwich menu
        menu_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        menu_shortcut.activated.connect(self._toggle_menu)

        # Ctrl+S / Cmd+S exports JPEG
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(
            lambda: self.canvas_widget.save_graph_as_jpeg())

    def apply_theme(self, theme_name: str):
        """Apply theme ('light' or 'dark') across the entire application
        and plot canvas.
        """
        self.current_theme = theme_name.lower()
        stylesheet = get_stylesheet(self.current_theme)
        palette = get_theme_palette(self.current_theme)

        app = QApplication.instance()
        if app:
            app.setPalette(palette)
            app.setStyleSheet(stylesheet)

        self.setPalette(palette)
        self.setStyleSheet(stylesheet)

        # Update canvas theme
        if hasattr(self, "canvas_widget"):
            self.canvas_widget.set_theme(self.current_theme)

        # Update top bar button label to match active theme
        if hasattr(self, "theme_btn"):
            if self.current_theme == "light":
                self.theme_btn.setText("☀️ Light Mode")
                self.theme_btn.setToolTip(
                    "Currently in Light Mode. Click to switch to Dark Mode.")
            else:
                self.theme_btn.setText("🌙 Dark Mode")
                self.theme_btn.setToolTip(
                    "Currently in Dark Mode. Click to switch to Light Mode.")

        # Sync menu check states
        if (
            hasattr(self, "light_theme_action")
            and hasattr(self, "dark_theme_action")
        ):
            self.light_theme_action.setChecked(self.current_theme == "light")
            self.dark_theme_action.setChecked(self.current_theme == "dark")

        if hasattr(self, "status_bar"):
            self.status_bar.showMessage(
                f"Applied {self.current_theme.capitalize()} Theme", 3000)

    def _toggle_quick_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)

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
        self.status_bar.showMessage(
            f"Graph successfully exported to JPEG: {path}", 6000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "drawer") and not self.drawer.is_collapsed:
            self.drawer.adapt_to_window_width(self.width())
