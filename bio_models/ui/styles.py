"""Desktop application styling, themes (Light and Dark), and plotting
color palettes.
"""

import os
from PyQt6.QtGui import QColor, QIcon, QPalette

_ICONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "icons"
).replace("\\", "/")

_UP_LIGHT = f"{_ICONS_DIR}/chevron_up_light.svg"
_DOWN_LIGHT = f"{_ICONS_DIR}/chevron_down_light.svg"
_UP_DARK = f"{_ICONS_DIR}/chevron_up_dark.svg"
_DOWN_DARK = f"{_ICONS_DIR}/chevron_down_dark.svg"
_PLAY_LIGHT = f"{_ICONS_DIR}/play_light.svg"
_PLAY_DARK = f"{_ICONS_DIR}/play_dark.svg"
_SAVE_LIGHT = f"{_ICONS_DIR}/save_light.svg"
_SAVE_DARK = f"{_ICONS_DIR}/save_dark.svg"


def _ensure_icons():
    """Ensure modern vector icon files exist."""
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
        _PLAY_LIGHT: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
            'viewBox="0 0 16 16"><path d="M4.5 3.3c0-.6.7-1 1.2-.6l8 4.7'
            'c.5.3.5 1 0 1.3l-8 4.7c-.5.3-1.2-.1-1.2-.6V3.3z" '
            'fill="#ffffff"/></svg>'
        ),
        _PLAY_DARK: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
            'viewBox="0 0 16 16"><path d="M4.5 3.3c0-.6.7-1 1.2-.6l8 4.7'
            'c.5.3.5 1 0 1.3l-8 4.7c-.5.3-1.2-.1-1.2-.6V3.3z" '
            'fill="#f4f4f5"/></svg>'
        ),
        _SAVE_LIGHT: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
            'viewBox="0 0 16 16"><path d="M2.5 5.5A1.5 1.5 0 0 1 4 4h1.3a1 '
            '1 0 0 0 .8-.4l.5-.7A1 1 0 0 1 7.4 2.2h1.2a1 1 0 0 1 .8.7l.5.7'
            'a1 1 0 0 0 .8.4H12a1.5 1.5 0 0 1 1.5 1.5v6.5a1.5 1.5 0 0 1-1.5 '
            '1.5H4a1.5 1.5 0 0 1-1.5-1.5V5.5z" fill="none" stroke="#334155" '
            'stroke-width="1.4" stroke-linejoin="round"/><circle cx="8" '
            'cy="8.2" r="2.2" fill="none" stroke="#334155" '
            'stroke-width="1.4"/></svg>'
        ),
        _SAVE_DARK: (
            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
            'viewBox="0 0 16 16"><path d="M2.5 5.5A1.5 1.5 0 0 1 4 4h1.3a1 '
            '1 0 0 0 .8-.4l.5-.7A1 1 0 0 1 7.4 2.2h1.2a1 1 0 0 1 .8.7l.5.7'
            'a1 1 0 0 0 .8.4H12a1.5 1.5 0 0 1 1.5 1.5v6.5a1.5 1.5 0 0 1-1.5 '
            '1.5H4a1.5 1.5 0 0 1-1.5-1.5V5.5z" fill="none" stroke="#e4e4e7" '
            'stroke-width="1.4" stroke-linejoin="round"/><circle cx="8" '
            'cy="8.2" r="2.2" fill="none" stroke="#e4e4e7" '
            'stroke-width="1.4"/></svg>'
        ),
    }
    for path, content in icons.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


def get_play_icon(theme: str = "dark") -> QIcon:
    """Return modern vector play icon for the active theme."""
    _ensure_icons()
    path = _PLAY_LIGHT if theme == "light" else _PLAY_DARK
    return QIcon(path)


def get_save_icon(theme: str = "dark") -> QIcon:
    """Return modern vector save/camera icon for the active theme."""
    _ensure_icons()
    path = _SAVE_LIGHT if theme == "light" else _SAVE_DARK
    return QIcon(path)


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
    font-weight: 600;
    border-radius: 6px;
    padding: 9px 16px;
    border: 1px solid #1d4ed8;
}

QPushButton#SimulateButton:hover {
    background-color: #1d4ed8;
    border: 1px solid #1e40af;
}

QPushButton#SimulateButton:pressed {
    background-color: #1e40af;
}

QPushButton#SaveGraphButton,
QPushButton#SaveJpegButton {
    background-color: #ffffff;
    color: #334155;
    font-size: 12px;
    font-weight: 600;
    border-radius: 6px;
    padding: 7px 14px;
    border: 1px solid #cbd5e1;
}

QPushButton#SaveGraphButton:hover,
QPushButton#SaveJpegButton:hover {
    background-color: #f8fafc;
    border: 1px solid #94a3b8;
    color: #0f172a;
}

QPushButton#SaveGraphButton:pressed,
QPushButton#SaveJpegButton:pressed {
    background-color: #e2e8f0;
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

QSplitter::handle {
    background-color: #cbd5e1;
}

QSplitter::handle:hover {
    background-color: #94a3b8;
}
"""

LIGHT_STYLESHEET = _RAW_LIGHT_STYLESHEET.replace(
    "__UP_LIGHT__", _UP_LIGHT
).replace(
    "__DOWN_LIGHT__", _DOWN_LIGHT
)

_RAW_DARK_STYLESHEET = """
QMainWindow {
    background-color: #121212;
}

QWidget#CentralWidget {
    background-color: #121212;
}

/* Top Navigation Bar */
QWidget#TopBar {
    background-color: #161616;
    border-bottom: 1px solid #262626;
}

QLabel#AppTitle {
    color: #f4f4f5;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

QLabel#AppSubtitle {
    color: #a1a1aa;
    font-size: 12px;
}

QLabel#AppHelp {
    color: #71717a;
    font-size: 11px;
}

/* Hamburger / Sandwich Toggle Button */
QPushButton#SandwichToggleBtn {
    background-color: #1e1e1e;
    color: #e4e4e7;
    border: 1px solid #2e2e2e;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    padding: 6px 12px;
}

QPushButton#SandwichToggleBtn:hover {
    background-color: #282828;
    border-color: #3f3f46;
}

/* Theme Switcher Button in Top Bar */
QPushButton#ThemeToggleBtn {
    background-color: #1e1e1e;
    color: #d4d4d8;
    border: 1px solid #2e2e2e;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
}

QPushButton#ThemeToggleBtn:hover {
    background-color: #282828;
    color: #ffffff;
    border-color: #3f3f46;
}

/* Sandwich / Drawer Menu Styling */
QFrame#SandwichDrawer {
    background-color: #141414;
    border-right: 1px solid #262626;
}

QLabel#DrawerTitle {
    color: #f4f4f5;
    font-size: 14px;
    font-weight: 700;
    padding: 12px 16px;
    border-bottom: 1px solid #262626;
}

QLabel#DrawerCategory {
    color: #71717a;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 14px 16px 6px 16px;
}

QPushButton#DrawerCloseBtn {
    background-color: transparent;
    color: #71717a;
    border: none;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#DrawerCloseBtn:hover {
    color: #ffffff;
    background-color: #262626;
    border-radius: 4px;
}

QPushButton.ModelNavButton {
    background-color: transparent;
    color: #a1a1aa;
    text-align: left;
    padding: 9px 16px;
    font-size: 12px;
    border: none;
    border-bottom: 1px solid #202020;
    border-left: 3px solid transparent;
    border-radius: 0px;
}

QPushButton.ModelNavButton:hover {
    background-color: #222222;
    color: #ffffff;
    border-bottom: 1px solid #202020;
}

QPushButton.ModelNavButton[selected="true"] {
    background-color: #262626;
    color: #f4f4f5;
    border-left: 3px solid #a1a1aa;
    border-bottom: 1px solid #202020;
    font-weight: 700;
}

/* Parameter Panel Styling */
QScrollArea#ParamScrollArea {
    background-color: #181818;
    border: 1px solid #262626;
    border-radius: 8px;
}

QWidget#ParamScrollContent {
    background-color: #181818;
}

/* Universal and GroupBox Label Styling */
QLabel {
    color: #e4e4e7;
}

QGroupBox QLabel {
    color: #e4e4e7;
}

QScrollArea#ParamScrollArea QLabel {
    color: #e4e4e7;
}

QWidget#ParamScrollContent QLabel {
    color: #e4e4e7;
}

QLabel#CanvasInfoLabel {
    color: #a1a1aa;
    font-size: 12px;
}

QLabel#PresetDescLabel {
    color: #a1a1aa;
    font-size: 11px;
    font-style: italic;
}

QGroupBox {
    background-color: #1e1e1e;
    border: 1px solid #2c2c2c;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 12px;
    font-weight: 700;
    color: #f4f4f5;
    padding-top: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #f4f4f5;
}

QLabel#ModelTitle {
    font-size: 16px;
    font-weight: 800;
    color: #f4f4f5;
}

QLabel#ModelBadge,
QPushButton#ModelBadge {
    background-color: #27272a;
    color: #e4e4e7;
    border: 1px solid #3f3f46;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    text-align: center;
}

QPushButton#ModelBadge[mode="continuous"] {
    background-color: #27272a;
    color: #e4e4e7;
    border: 1px solid #3f3f46;
}

QPushButton#ModelBadge[mode="continuous"]:hover {
    background-color: #3f3f46;
    color: #ffffff;
}

QPushButton#ModelBadge[mode="discrete"] {
    background-color: #3f1d1d;
    color: #fca5a5;
    border: 1px solid #7f1d1d;
}

QPushButton#ModelBadge[mode="discrete"]:hover {
    background-color: #502323;
    color: #fecaca;
}

QLabel#RelationshipBadge {
    background-color: #27272a;
    color: #fbbf24;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 5px;
    border: 1px solid #52525b;
}

/* Inputs & SpinBoxes */
QDoubleSpinBox, QSpinBox {
    background-color: #141414;
    border: 1px solid #2c2c2c;
    border-radius: 6px;
    padding: 5px 24px 5px 8px;
    font-size: 12px;
    color: #f4f4f5;
    min-height: 24px;
}

QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1.5px solid #71717a;
    background-color: #141414;
}

QDoubleSpinBox::up-button, QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #2c2c2c;
    border-bottom: 0.5px solid #2c2c2c;
    border-top-right-radius: 5px;
    background-color: #1e1e1e;
}

QDoubleSpinBox::up-button:hover, QSpinBox::up-button:hover {
    background-color: #2c2c2c;
}

QDoubleSpinBox::up-button:pressed, QSpinBox::up-button:pressed {
    background-color: #383838;
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
    border-left: 1px solid #2c2c2c;
    border-top: 0.5px solid #2c2c2c;
    border-bottom-right-radius: 5px;
    background-color: #1e1e1e;
}

QDoubleSpinBox::down-button:hover, QSpinBox::down-button:hover {
    background-color: #2c2c2c;
}

QDoubleSpinBox::down-button:pressed, QSpinBox::down-button:pressed {
    background-color: #383838;
}

QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {
    image: url("__DOWN_DARK__");
    width: 8px;
    height: 5px;
}

/* QComboBox & Dropdown Popup (Dark Theme) */
QComboBox {
    background-color: #141414;
    border: 1px solid #2c2c2c;
    border-radius: 6px;
    padding: 6px 28px 6px 12px;
    font-size: 12px;
    color: #f4f4f5;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #3f3f46;
    background-color: #1a1a1a;
}

QComboBox:focus {
    border: 1.5px solid #71717a;
    background-color: #141414;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #2c2c2c;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #1e1e1e;
}

QComboBox::drop-down:hover {
    background-color: #2c2c2c;
}

QComboBox::down-arrow {
    image: url("__DOWN_DARK__");
    width: 9px;
    height: 6px;
}

QComboBox QAbstractItemView, QComboBox QListView {
    background-color: #1a1a1a;
    color: #f4f4f5;
    selection-background-color: #333333;
    selection-color: #ffffff;
    border: 1px solid #2e2e2e;
    border-radius: 6px;
    padding: 4px;
    outline: none;
}

QComboBox QAbstractItemView::item, QComboBox QListView::item {
    background-color: #1a1a1a;
    color: #f4f4f5;
    padding: 8px 12px;
    min-height: 26px;
    border-radius: 4px;
}

QComboBox QAbstractItemView::item:hover, QComboBox QListView::item:hover {
    background-color: #27272a;
    color: #ffffff;
}

QComboBox QAbstractItemView::item:selected,
QComboBox QListView::item:selected {
    background-color: #3f3f46;
    color: #ffffff;
    font-weight: 700;
}

/* Action Buttons */
QPushButton#SimulateButton {
    background-color: #27272a;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
    padding: 9px 16px;
    border: 1px solid #3f3f46;
}

QPushButton#SimulateButton:hover {
    background-color: #38383e;
    border: 1px solid #52525b;
    color: #ffffff;
}

QPushButton#SimulateButton:pressed {
    background-color: #1c1c1f;
    border: 1px solid #3f3f46;
}

QPushButton#SaveGraphButton,
QPushButton#SaveJpegButton {
    background-color: #202023;
    color: #e4e4e7;
    font-size: 12px;
    font-weight: 600;
    border-radius: 6px;
    padding: 7px 14px;
    border: 1px solid #333338;
}

QPushButton#SaveGraphButton:hover,
QPushButton#SaveJpegButton:hover {
    background-color: #2c2c30;
    border: 1px solid #484852;
    color: #ffffff;
}

QPushButton#SaveGraphButton:pressed,
QPushButton#SaveJpegButton:pressed {
    background-color: #18181b;
    border: 1px solid #333338;
}

QPushButton#PresetButton {
    background-color: #222222;
    color: #e4e4e7;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #333333;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton#PresetButton:hover {
    background-color: #2c2c2c;
    border-color: #3f3f46;
}

/* Status Bar & Menu Bar */
QStatusBar {
    background-color: #141414;
    border-top: 1px solid #262626;
    color: #71717a;
    font-size: 12px;
}

QMenuBar {
    background-color: #141414;
    color: #e4e4e7;
    border-bottom: 1px solid #262626;
}

QMenuBar::item:selected {
    background-color: #262626;
}

QMenu {
    background-color: #1a1a1a;
    color: #f4f4f5;
    border: 1px solid #2e2e2e;
}

QMenu::item:selected {
    background-color: #282828;
    color: #ffffff;
}

/* Modern ScrollBars (Horizontal & Vertical) */
QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #2e2e2e;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #404040;
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
    background-color: #2e2e2e;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #404040;
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

QSplitter::handle {
    background-color: #262626;
}

QSplitter::handle:hover {
    background-color: #3f3f46;
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
    "figure_facecolor": "#141414",
    "axes_facecolor": "#1a1a1a",
    "text_color": "#f4f4f5",
    "subtext_color": "#a1a1aa",
    "grid": "#262626",
    "n1": "#38bdf8",       # Bright Sky Blue
    "n2": "#fb923c",       # Bright Coral Orange
    "n1_fill": "#38bdf8",
    "n2_fill": "#fb923c",
    "trajectory": "#c084fc",  # Lavender Violet
    "start": "#4ade80",       # Neon Green
    "end": "#f87171",         # Coral Red
    "isocline1": "#38bdf8",
    "isocline2": "#fb923c",
    "legend_face": "#1a1a1a",
    "legend_edge": "#2e2e2e",
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
    """Return explicit QPalette matching the theme to prevent OS system
    dark mode from overriding popup menus and dropdown item views with
    dark backgrounds.
    """
    pal = QPalette()
    is_dark = theme.lower() == "dark"

    if is_dark:
        bg = QColor("#121212")
        panel_bg = QColor("#181818")
        fg = QColor("#f4f4f5")
        sub_fg = QColor("#a1a1aa")
        hl = QColor("#3f3f46")
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
