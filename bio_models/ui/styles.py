"""
Desktop application styling and theme definitions.
"""

APP_STYLESHEET = """
QMainWindow {
    background-color: #f8fafc;
}

QWidget#CentralWidget {
    background-color: #f8fafc;
}

/* Sandwich / Drawer Menu Styling */
QFrame#SandwichDrawer {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

QLabel#DrawerTitle {
    color: #f8fafc;
    font-size: 15px;
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

QPushButton.ModelNavButton {
    background-color: transparent;
    color: #cbd5e1;
    text-align: left;
    padding: 10px 16px;
    font-size: 13px;
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
    font-weight: 600;
}

/* Hamburger / Sandwich Toggle Button */
QPushButton#SandwichToggleBtn {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    padding: 6px 12px;
}

QPushButton#SandwichToggleBtn:hover {
    background-color: #1e293b;
    border-color: #475569;
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

QLabel#SectionHeader {
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
    padding-top: 8px;
    padding-bottom: 4px;
    border-bottom: 2px solid #e2e8f0;
}

QLabel#ModelTitle {
    font-size: 17px;
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
    padding: 5px 10px;
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
    font-size: 14px;
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
    font-size: 13px;
    font-weight: 700;
    border-radius: 6px;
    padding: 8px 16px;
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

QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e2e8f0;
    color: #475569;
    font-size: 12px;
}
"""

PLOT_COLORS = {
    "n1": "#0284c7",       # Ocean Blue for Prey / Resource / Species 1
    "n2": "#ea580c",       # Sunset Orange for Predator / Consumer / Species 2
    "n1_fill": "#e0f2fe",
    "n2_fill": "#ffedd5",
    "trajectory": "#4338ca",  # Indigo for phase space trajectory
    "start": "#16a34a",       # Green for start marker
    "end": "#dc2626",         # Red for end marker
    "isocline1": "#0ea5e9",   # Cyan dashed
    "isocline2": "#f97316",   # Orange dashed
    "grid": "#f1f5f9",
}
