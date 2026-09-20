"""
Sandwich / Hamburger Drawer Menu for Model Selection.
Allows toggling and selecting between competition and consumer-resource models.
"""

from typing import List, Tuple
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
)

from bio_models.models import BiologicalModel, AVAILABLE_MODELS


class SandwichDrawer(QFrame):
    """
    Collapsible side drawer navigation menu ('Sandwich menu').
    """

    model_selected = pyqtSignal(BiologicalModel, str)  # (model, mode: 'continuous' or 'discrete')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SandwichDrawer")
        self.setFixedWidth(270)
        self._is_collapsed = False
        self._buttons: List[Tuple[QPushButton, BiologicalModel, str]] = []
        self._active_button: QPushButton = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with branding and close button
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 14, 12, 14)

        title = QLabel("Models Menu")
        title.setObjectName("DrawerTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setToolTip("Close menu")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: #334155;
                border-radius: 4px;
            }
        """)
        close_btn.clicked.connect(self.toggle_collapse)
        header_layout.addWidget(close_btn)

        layout.addWidget(header_widget)

        # Scrollable list of models
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(0, 8, 0, 16)
        content_layout.setSpacing(2)

        # Categorize models
        models_by_cat = {}
        for m in AVAILABLE_MODELS:
            models_by_cat.setdefault(m.category, []).append(m)

        for category, models in models_by_cat.items():
            cat_label = QLabel(category)
            cat_label.setObjectName("DrawerCategory")
            content_layout.addWidget(cat_label)

            for model in models:
                # Add continuous button
                btn = QPushButton(f"  • {model.name}")
                btn.setProperty("class", "ModelNavButton")
                btn.clicked.connect(lambda checked, m=model: self._handle_selection(m, "continuous"))
                content_layout.addWidget(btn)
                self._buttons.append((btn, model, "continuous"))

                # For Lotka-Volterra competition, add discrete recursion mode
                if "Competition" in model.name:
                    disc_btn = QPushButton("  ↳ Discrete Recursion (Eq 3.14)")
                    disc_btn.setProperty("class", "ModelNavButton")
                    disc_btn.clicked.connect(lambda checked, m=model: self._handle_selection(m, "discrete"))
                    content_layout.addWidget(disc_btn)
                    self._buttons.append((disc_btn, model, "discrete"))

        content_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Initial selection
        if self._buttons:
            first_btn, first_model, first_mode = self._buttons[0]
            self._set_active_button(first_btn)

    def _handle_selection(self, model: BiologicalModel, mode: str):
        # Update styling on buttons
        for btn, m, md in self._buttons:
            if m.name == model.name and md == mode:
                self._set_active_button(btn)
                break
        self.model_selected.emit(model, mode)

    def _set_active_button(self, btn: QPushButton):
        if self._active_button:
            self._active_button.setProperty("selected", "false")
            self._active_button.style().unpolish(self._active_button)
            self._active_button.style().polish(self._active_button)

        self._active_button = btn
        btn.setProperty("selected", "true")
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def toggle_collapse(self):
        """Toggle side drawer width between 0 and 270."""
        self._is_collapsed = not self._is_collapsed
        target_width = 0 if self._is_collapsed else 270

        self.anim = QPropertyAnimation(self, b"maximumWidth")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.width())
        self.anim.setEndValue(target_width)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

        self.anim_min = QPropertyAnimation(self, b"minimumWidth")
        self.anim_min.setDuration(200)
        self.anim_min.setStartValue(self.width())
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim_min.start()

    @property
    def is_collapsed(self) -> bool:
        return self._is_collapsed
