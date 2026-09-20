"""
Desktop application styling, themes (Light and Dark), and plotting color palettes.
"""

LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f8fafc;
}

QWidget#CentralWidget {
    background-color: #f8fafc;
}

/* Top Navigation Bar */
QWidget#TopBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
}

QLabel#AppTitle {
    color: #0f172a;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

QLabel#AppSubtitle {
    color: #64748b;
    font-size: 12px;
}

QLabel#AppHelp {
    color: #94a3b8;
    font-size: 11px;
}

/* Hamburger / Sandwich Toggle Button */
QPushButton#SandwichToggleBtn {
    background-color: #f1f5f9;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    padding: 6px 12px;
}

QPushButton#SandwichToggleBtn:hover {
    background-color: #e2e8f0;
    border-color: #94a3b8;
}

/* Theme Switcher Button in Top Bar */
QPushButton#ThemeToggleBtn {
    background-color: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
}

QPushButton#ThemeToggleBtn:hover {
    background-color: #e2e8f0;
    color: #0f172a;
}

/* Sandwich / Drawer Menu Styling */
QFrame#SandwichDrawer {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

QLabel#DrawerTitle {
    color: #0f172a;
    font-size: 14px;
    font-weight: 700;
    padding: 12px 16px;
    border-bottom: 1px solid #e2e8f0;
}

QLabel#DrawerCategory {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 14px 16px 6px 16px;
}

QPushButton#DrawerCloseBtn {
    background-color: transparent;
    color: #64748b;
    border: none;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#DrawerCloseBtn:hover {
    color: #0f172a;
    background-color: #f1f5f9;
    border-radius: 4px;
}

QPushButton.ModelNavButton {
    background-color: transparent;
    color: #334155;
    text-align: left;
    padding: 9px 16px;
    font-size: 12px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
}

QPushButton.ModelNavButton:hover {
    background-color: #f1f5f9;
    color: #0f172a;
}

QPushButton.ModelNavButton[selected="true"] {
    background-color: #eff6ff;
    color: #2563eb;
    border-left: 3px solid #2563eb;
    font-weight: 700;
}

/* Parameter Panel Styling */
QScrollArea#ParamScrollArea {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

QWidget#ParamScrollContent {
    background-color: #ffffff;
}

/* Universal and GroupBox Label Styling */
QLabel {
    color: #0f172a;
}

QGroupBox QLabel {
    color: #0f172a;
}

QScrollArea#ParamScrollArea QLabel {
    color: #0f172a;
}

QWidget#ParamScrollContent QLabel {
    color: #0f172a;
}

QLabel#CanvasInfoLabel {
    color: #334155;
    font-size: 12px;
}

QLabel#PresetDescLabel {
    color: #475569;
    font-size: 11px;
    font-style: italic;
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 12px;
    font-weight: 700;
    color: #0f172a;
    padding-top: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #0f172a;
}

QLabel#ModelTitle {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
}

QLabel#ModelBadge {
    background-color: #e0f2fe;
    color: #0369a1;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 4px;
}

QLabel#RelationshipBadge {
    background-color: #fef3c7;
    color: #92400e;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    border: 1px solid #fde68a;
}

/* Inputs & SpinBoxes */
QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px 8px;
    font-size: 12px;
    color: #0f172a;
    min-height: 22px;
}

QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #2563eb;
}

/* Action Buttons */
QPushButton#SimulateButton {
    background-color: #2563eb;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    border-radius: 6px;
    padding: 10px 16px;
    border: none;
}

QPushButton#SimulateButton:hover {
    background-color: #1d4ed8;
}

QPushButton#SimulateButton:pressed {
    background-color: #1e40af;
}

QPushButton#SaveJpegButton {
    background-color: #059669;
    color: #ffffff;
    font-size: 12px;
    font-weight: 700;
    border-radius: 6px;
    padding: 8px 14px;
    border: none;
}

QPushButton#SaveJpegButton:hover {
    background-color: #047857;
}

QPushButton#PresetButton {
    background-color: #f1f5f9;
    color: #334155;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton#PresetButton:hover {
    background-color: #e2e8f0;
}

/* Status Bar & Menu Bar */
QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e2e8f0;
    color: #475569;
    font-size: 12px;
}

QMenuBar {
    background-color: #ffffff;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
}

QMenuBar::item:selected {
    background-color: #f1f5f9;
}

QMenu {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #e2e8f0;
}

QMenu::item:selected {
    background-color: #eff6ff;
    color: #2563eb;
}
"""

DARK_STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
}

QWidget#CentralWidget {
    background-color: #0f172a;
}

/* Top Navigation Bar */
QWidget#TopBar {
    background-color: #0b1120;
    border-bottom: 1px solid #1e293b;
}

QLabel#AppTitle {
    color: #f8fafc;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

QLabel#AppSubtitle {
    color: #94a3b8;
    font-size: 12px;
}

QLabel#AppHelp {
    color: #64748b;
    font-size: 11px;
}

/* Hamburger / Sandwich Toggle Button */
QPushButton#SandwichToggleBtn {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    padding: 6px 12px;
}

QPushButton#SandwichToggleBtn:hover {
    background-color: #334155;
    border-color: #475569;
}

/* Theme Switcher Button in Top Bar */
QPushButton#ThemeToggleBtn {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
}

QPushButton#ThemeToggleBtn:hover {
    background-color: #334155;
    color: #ffffff;
}

/* Sandwich / Drawer Menu Styling */
QFrame#SandwichDrawer {
    background-color: #0b1120;
    border-right: 1px solid #1e293b;
}

QLabel#DrawerTitle {
    color: #f8fafc;
    font-size: 14px;
    font-weight: 700;
    padding: 12px 16px;
    border-bottom: 1px solid #1e293b;
}

QLabel#DrawerCategory {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 14px 16px 6px 16px;
}

QPushButton#DrawerCloseBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#DrawerCloseBtn:hover {
    color: #ffffff;
    background-color: #1e293b;
    border-radius: 4px;
}

QPushButton.ModelNavButton {
    background-color: transparent;
    color: #cbd5e1;
    text-align: left;
    padding: 9px 16px;
    font-size: 12px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
}

QPushButton.ModelNavButton:hover {
    background-color: #1e293b;
    color: #ffffff;
}

QPushButton.ModelNavButton[selected="true"] {
    background-color: #1e293b;
    color: #38bdf8;
    border-left: 3px solid #38bdf8;
    font-weight: 700;
}

/* Parameter Panel Styling */
QScrollArea#ParamScrollArea {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}

QWidget#ParamScrollContent {
    background-color: #1e293b;
}

/* Universal and GroupBox Label Styling */
QLabel {
    color: #f8fafc;
}

QGroupBox QLabel {
    color: #f8fafc;
}

QScrollArea#ParamScrollArea QLabel {
    color: #f8fafc;
}

QWidget#ParamScrollContent QLabel {
    color: #f8fafc;
}

QLabel#CanvasInfoLabel {
    color: #94a3b8;
    font-size: 12px;
}

QLabel#PresetDescLabel {
    color: #94a3b8;
    font-size: 11px;
    font-style: italic;
}

QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 12px;
    font-weight: 700;
    color: #f8fafc;
    padding-top: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #f8fafc;
}

QLabel#ModelTitle {
    font-size: 16px;
    font-weight: 800;
    color: #f8fafc;
}

QLabel#ModelBadge {
    background-color: #075985;
    color: #e0f2fe;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 4px;
}

QLabel#RelationshipBadge {
    background-color: #78350f;
    color: #fef3c7;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    border: 1px solid #b45309;
}

/* Inputs & SpinBoxes */
QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 5px;
    padding: 5px 8px;
    font-size: 12px;
    color: #f8fafc;
    min-height: 22px;
}

QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #38bdf8;
}

/* Action Buttons */
QPushButton#SimulateButton {
    background-color: #2563eb;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    border-radius: 6px;
    padding: 10px 16px;
    border: none;
}

QPushButton#SimulateButton:hover {
    background-color: #1d4ed8;
}

QPushButton#SimulateButton:pressed {
    background-color: #1e40af;
}

QPushButton#SaveJpegButton {
    background-color: #059669;
    color: #ffffff;
    font-size: 12px;
    font-weight: 700;
    border-radius: 6px;
    padding: 8px 14px;
    border: none;
}

QPushButton#SaveJpegButton:hover {
    background-color: #047857;
}

QPushButton#PresetButton {
    background-color: #334155;
    color: #f1f5f9;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #475569;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton#PresetButton:hover {
    background-color: #475569;
}

/* Status Bar & Menu Bar */
QStatusBar {
    background-color: #0b1120;
    border-top: 1px solid #1e293b;
    color: #94a3b8;
    font-size: 12px;
}

QMenuBar {
    background-color: #0b1120;
    color: #f8fafc;
    border-bottom: 1px solid #1e293b;
}

QMenuBar::item:selected {
    background-color: #1e293b;
}

QMenu {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #1e293b;
}

QMenu::item:selected {
    background-color: #1e293b;
    color: #38bdf8;
}
"""

LIGHT_PLOT_COLORS = {
    "figure_facecolor": "#ffffff",
    "axes_facecolor": "#ffffff",
    "text_color": "#0f172a",
    "subtext_color": "#475569",
    "grid": "#e2e8f0",
    "n1": "#0284c7",       # Ocean Blue
    "n2": "#ea580c",       # Sunset Orange
    "n1_fill": "#0284c7",
    "n2_fill": "#ea580c",
    "trajectory": "#4338ca",  # Indigo
    "start": "#16a34a",       # Green
    "end": "#dc2626",         # Red
    "isocline1": "#0ea5e9",
    "isocline2": "#f97316",
    "legend_face": "#ffffff",
    "legend_edge": "#cbd5e1",
}

DARK_PLOT_COLORS = {
    "figure_facecolor": "#0f172a",
    "axes_facecolor": "#1e293b",
    "text_color": "#f8fafc",
    "subtext_color": "#94a3b8",
    "grid": "#334155",
    "n1": "#38bdf8",       # Bright Sky
    "n2": "#fb923c",       # Bright Coral
    "n1_fill": "#38bdf8",
    "n2_fill": "#fb923c",
    "trajectory": "#a5b4fc",  # Light Indigo
    "start": "#4ade80",       # Neon Green
    "end": "#f87171",         # Coral Red
    "isocline1": "#38bdf8",
    "isocline2": "#fb923c",
    "legend_face": "#1e293b",
    "legend_edge": "#334155",
}

# Compatibility reference
APP_STYLESHEET = LIGHT_STYLESHEET
PLOT_COLORS = LIGHT_PLOT_COLORS


def get_stylesheet(theme: str = "light") -> str:
    """Return Qt CSS stylesheet for theme ('light' or 'dark')."""
    return DARK_STYLESHEET if theme.lower() == "dark" else LIGHT_STYLESHEET


def get_plot_colors(theme: str = "light") -> dict:
    """Return plotting color dictionary for theme ('light' or 'dark')."""
    return DARK_PLOT_COLORS if theme.lower() == "dark" else LIGHT_PLOT_COLORS
