"""Desktop application styling, themes (Light and Dark), and plotting
color palettes.
"""

import os
from PyQt6.QtGui import QColor, QPalette

_ICONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "icons"
).replace("\\", "/")

_UP_LIGHT = f"{_ICONS_DIR}/chevron_up_light.svg"
_DOWN_LIGHT = f"{_ICONS_DIR}/chevron_down_light.svg"
_UP_DARK = f"{_ICONS_DIR}/chevron_up_dark.svg"
_DOWN_DARK = f"{_ICONS_DIR}/chevron_down_dark.svg"


def _ensure_icons():
    """Ensure modern vector chevron icon files exist."""
    os.makedirs(_ICONS_DIR, exist_ok=True)
    icons = {
        _UP_LIGHT: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" '
            'viewBox="0 0 12 8"><path d="M2 6L6 2L10 6" stroke="#475569" '
            'stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" fill="none"/></svg>'
        ),
        _DOWN_LIGHT: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" '
            'viewBox="0 0 12 8"><path d="M2 2L6 6L10 2" stroke="#475569" '
            'stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" fill="none"/></svg>'
        ),
        _UP_DARK: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" '
            'viewBox="0 0 12 8"><path d="M2 6L6 2L10 6" stroke="#94a3b8" '
            'stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" fill="none"/></svg>'
        ),
        _DOWN_DARK: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" '
            'viewBox="0 0 12 8"><path d="M2 2L6 6L10 2" stroke="#94a3b8" '
            'stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" fill="none"/></svg>'
        ),
    }
    for path, content in icons.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


_ensure_icons()

_RAW_LIGHT_STYLESHEET = """
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
    border-bottom: 1px solid #e2e8f0;
    border-left: 3px solid transparent;
    border-radius: 0px;
}

QPushButton.ModelNavButton:hover {
    background-color: #f1f5f9;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
}

QPushButton.ModelNavButton[selected="true"] {
    background-color: #eff6ff;
    color: #2563eb;
    border-left: 3px solid #2563eb;
    border-bottom: 1px solid #e2e8f0;
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

QLabel#ModelBadge,
QPushButton#ModelBadge {
    background-color: #dbeafe;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    text-align: center;
}

QPushButton#ModelBadge[mode="continuous"] {
    background-color: #dbeafe;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}

QPushButton#ModelBadge[mode="continuous"]:hover {
    background-color: #bfdbfe;
    color: #1e40af;
}

QPushButton#ModelBadge[mode="discrete"] {
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
}

QPushButton#ModelBadge[mode="discrete"]:hover {
    background-color: #fecaca;
    color: #991b1b;
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
QDoubleSpinBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 24px 5px 8px;
    font-size: 12px;
    color: #0f172a;
    min-height: 24px;
}

QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1.5px solid #2563eb;
    background-color: #ffffff;
}

QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    border-bottom: 0.5px solid #cbd5e1;
    border-top-right-radius: 5px;
    background-color: #f8fafc;
}

QDoubleSpinBox::up-button:hover, QSpinBox::up-button:hover {
    background-color: #e2e8f0;
}

QDoubleSpinBox::up-button:pressed, QSpinBox::up-button:pressed {
    background-color: #cbd5e1;
}

QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {
    image: url("__UP_LIGHT__");
    width: 8px;
    height: 5px;
}

QDoubleSpinBox::down-button, QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    border-top: 0.5px solid #cbd5e1;
    border-bottom-right-radius: 5px;
    background-color: #f8fafc;
}

QDoubleSpinBox::down-button:hover, QSpinBox::down-button:hover {
    background-color: #e2e8f0;
}

QDoubleSpinBox::down-button:pressed, QSpinBox::down-button:pressed {
    background-color: #cbd5e1;
}

QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    image: url("__DOWN_LIGHT__");
    width: 8px;
    height: 5px;
}

/* QComboBox & Dropdown Popup (Light Theme) */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 28px 6px 12px;
    font-size: 12px;
    color: #0f172a;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #94a3b8;
    background-color: #f8fafc;
}

QComboBox:focus {
    border: 1.5px solid #2563eb;
    background-color: #ffffff;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #cbd5e1;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #f8fafc;
}

QComboBox::drop-down:hover {
    background-color: #e2e8f0;
}

QComboBox::down-arrow {
    image: url("__DOWN_LIGHT__");
    width: 9px;
    height: 6px;
}

QComboBox QAbstractItemView, QComboBox QListView {
    background-color: #ffffff;
    color: #0f172a;
    selection-background-color: #e0f2fe;
    selection-color: #0369a1;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px;
    outline: none;
}

QComboBox QAbstractItemView::item, QComboBox QListView::item {
    background-color: #ffffff;
    color: #0f172a;
    padding: 8px 12px;
    min-height: 26px;
    border-radius: 4px;
}

QComboBox QAbstractItemView::item:hover, QComboBox QListView::item:hover {
    background-color: #f1f5f9;
    color: #0f172a;
}

QComboBox QAbstractItemView::item:selected,
QComboBox QListView::item:selected {
    background-color: #e0f2fe;
    color: #0369a1;
    font-weight: 700;
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

/* Modern ScrollBars (Horizontal & Vertical) */
QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #cbd5e1;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    height: 0px;
    border: none;
    background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    width: 0px;
    height: 0px;
    border: none;
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""

LIGHT_STYLESHEET = _RAW_LIGHT_STYLESHEET.replace(
    "__UP_LIGHT__", _UP_LIGHT
).replace(
    "__DOWN_LIGHT__", _DOWN_LIGHT
)

_RAW_DARK_STYLESHEET = """
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
    border-bottom: 1px solid #1e293b;
    border-left: 3px solid transparent;
    border-radius: 0px;
}

QPushButton.ModelNavButton:hover {
    background-color: #1e293b;
    color: #ffffff;
    border-bottom: 1px solid #1e293b;
}

QPushButton.ModelNavButton[selected="true"] {
    background-color: #1e293b;
    color: #38bdf8;
    border-left: 3px solid #38bdf8;
    border-bottom: 1px solid #1e293b;
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

QLabel#ModelBadge,
QPushButton#ModelBadge {
    background-color: #1e3a8a;
    color: #bfdbfe;
    border: 1px solid #3b82f6;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    text-align: center;
}

QPushButton#ModelBadge[mode="continuous"] {
    background-color: #1e3a8a;
    color: #bfdbfe;
    border: 1px solid #3b82f6;
}

QPushButton#ModelBadge[mode="continuous"]:hover {
    background-color: #2563eb;
    color: #eff6ff;
}

QPushButton#ModelBadge[mode="discrete"] {
    background-color: #7f1d1d;
    color: #fecaca;
    border: 1px solid #ef4444;
}

QPushButton#ModelBadge[mode="discrete"]:hover {
    background-color: #991b1b;
    color: #fee2e2;
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
QDoubleSpinBox, QSpinBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 24px 5px 8px;
    font-size: 12px;
    color: #f8fafc;
    min-height: 24px;
}

QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1.5px solid #38bdf8;
    background-color: #1e293b;
}

QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #334155;
    border-bottom: 0.5px solid #334155;
    border-top-right-radius: 5px;
    background-color: #1e293b;
}

QDoubleSpinBox::up-button:hover, QSpinBox::up-button:hover {
    background-color: #334155;
}

QDoubleSpinBox::up-button:pressed, QSpinBox::up-button:pressed {
    background-color: #475569;
}

QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {
    image: url("__UP_DARK__");
    width: 8px;
    height: 5px;
}

QDoubleSpinBox::down-button, QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #334155;
    border-top: 0.5px solid #334155;
    border-bottom-right-radius: 5px;
    background-color: #1e293b;
}

QDoubleSpinBox::down-button:hover, QSpinBox::down-button:hover {
    background-color: #334155;
}

QDoubleSpinBox::down-button:pressed, QSpinBox::down-button:pressed {
    background-color: #475569;
}

QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    image: url("__DOWN_DARK__");
    width: 8px;
    height: 5px;
}

/* QComboBox & Dropdown Popup (Dark Theme) */
QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 28px 6px 12px;
    font-size: 12px;
    color: #f8fafc;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #475569;
    background-color: #1e293b;
}

QComboBox:focus {
    border: 1.5px solid #38bdf8;
    background-color: #1e293b;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #334155;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #1e293b;
}

QComboBox::drop-down:hover {
    background-color: #334155;
}

QComboBox::down-arrow {
    image: url("__DOWN_DARK__");
    width: 9px;
    height: 6px;
}

QComboBox QAbstractItemView, QComboBox QListView {
    background-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #0369a1;
    selection-color: #ffffff;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px;
    outline: none;
}

QComboBox QAbstractItemView::item, QComboBox QListView::item {
    background-color: #1e293b;
    color: #f8fafc;
    padding: 8px 12px;
    min-height: 26px;
    border-radius: 4px;
}

QComboBox QAbstractItemView::item:hover, QComboBox QListView::item:hover {
    background-color: #334155;
    color: #ffffff;
}

QComboBox QAbstractItemView::item:selected,
QComboBox QListView::item:selected {
    background-color: #0284c7;
    color: #ffffff;
    font-weight: 700;
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

/* Modern ScrollBars (Horizontal & Vertical) */
QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #334155;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #475569;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    height: 0px;
    border: none;
    background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    width: 0px;
    height: 0px;
    border: none;
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""

DARK_STYLESHEET = _RAW_DARK_STYLESHEET.replace(
    "__UP_DARK__", _UP_DARK
).replace(
    "__DOWN_DARK__", _DOWN_DARK
)

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


def get_theme_palette(theme: str = "light") -> QPalette:
    """
    Return explicit QPalette matching the theme to prevent OS system dark mode
    from overriding popup menus and dropdown item views with dark backgrounds.
    """
    pal = QPalette()
    is_dark = theme.lower() == "dark"

    if is_dark:
        bg = QColor("#0f172a")
        panel_bg = QColor("#1e293b")
        fg = QColor("#f8fafc")
        sub_fg = QColor("#94a3b8")
        hl = QColor("#0284c7")
        hl_fg = QColor("#ffffff")
    else:
        bg = QColor("#f8fafc")
        panel_bg = QColor("#ffffff")
        fg = QColor("#0f172a")
        sub_fg = QColor("#475569")
        hl = QColor("#e0f2fe")
        hl_fg = QColor("#0369a1")

    pal.setColor(QPalette.ColorRole.Window, bg)
    pal.setColor(QPalette.ColorRole.WindowText, fg)
    pal.setColor(QPalette.ColorRole.Base, panel_bg)
    pal.setColor(QPalette.ColorRole.AlternateBase, bg)
    pal.setColor(QPalette.ColorRole.ToolTipBase, panel_bg)
    pal.setColor(QPalette.ColorRole.ToolTipText, fg)
    pal.setColor(QPalette.ColorRole.Text, fg)
    pal.setColor(QPalette.ColorRole.PlaceholderText, sub_fg)
    pal.setColor(QPalette.ColorRole.Button, panel_bg)
    pal.setColor(QPalette.ColorRole.ButtonText, fg)
    pal.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    pal.setColor(QPalette.ColorRole.Highlight, hl)
    pal.setColor(QPalette.ColorRole.HighlightedText, hl_fg)
    return pal
