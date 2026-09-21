"""
Sandwich / Hamburger Drawer Menu for Model Selection.
Allows toggling and selecting between competition and consumer-resource models.
"""

from typing import List, Tuple
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from bio_models.models import AVAILABLE_MODELS, BiologicalModel


class SandwichDrawer(QFrame):
    """Collapsible side drawer navigation menu ('Sandwich menu').

    Dynamically sizes to fit full model names in normal and fullscreen
    resolutions, while gracefully compressing and enabling horizontal
    scrolling in small window resolutions.
    """

    # (model, mode: 'continuous' or 'discrete')
    model_selected = pyqtSignal(BiologicalModel, str)

    DEFAULT_EXPANDED_WIDTH = 360
    MIN_EXPANDED_WIDTH = 260

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SandwichDrawer")
        self._is_collapsed = False
        self._buttons: List[Tuple[QPushButton, BiologicalModel, str]] = []
        self._active_button: QPushButton = None

        self._optimal_expanded_width = self.DEFAULT_EXPANDED_WIDTH
        self._min_expanded_width = self.MIN_EXPANDED_WIDTH
        self._expanded_width = self.DEFAULT_EXPANDED_WIDTH

        self._init_ui()
        self._calculate_optimal_width()
        self.setFixedWidth(self._expanded_width)

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
        close_btn.setObjectName("DrawerCloseBtn")
        close_btn.setFixedSize(28, 28)
        close_btn.setToolTip("Close menu")
        close_btn.clicked.connect(self.toggle_collapse)
        header_layout.addWidget(close_btn)

        layout.addWidget(header_widget)

        # Scrollable list of models
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("DrawerScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

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
                btn.clicked.connect(
                    lambda checked, m=model: self._handle_selection(
                        m, "continuous"
                    )
                )
                content_layout.addWidget(btn)
                self._buttons.append((btn, model, "continuous"))

                # For Lotka-Volterra competition, add discrete recursion mode
                if "Competition" in model.name:
                    disc_btn = QPushButton("  ↳ Discrete Recursion (Eq 3.14)")
                    disc_btn.setProperty("class", "ModelNavButton")
                    disc_btn.clicked.connect(
                        lambda checked, m=model: self._handle_selection(
                            m, "discrete"
                        )
                    )
                    content_layout.addWidget(disc_btn)
                    self._buttons.append((disc_btn, model, "discrete"))

        content_layout.addStretch()
        self.scroll_area.setWidget(scroll_content)
        layout.addWidget(self.scroll_area)

        # Initial selection
        if self._buttons:
            first_btn, first_model, first_mode = self._buttons[0]
            self._set_active_button(first_btn)

    def _calculate_optimal_width(self):
        """Calculate optimal width to fit all model names without any
        horizontal scrollbar.
        """
        max_btn_w = 0
        for btn, _, _ in self._buttons:
            fm = btn.fontMetrics()
            # padding (16 left + 16 right) + left indicator
            btn_w = fm.horizontalAdvance(btn.text()) + 36
            if btn_w > max_btn_w:
                max_btn_w = btn_w

        for cat_lbl in self.findChildren(QLabel):
            if cat_lbl.objectName() == "DrawerCategory":
                fm = cat_lbl.fontMetrics()
                cat_w = fm.horizontalAdvance(cat_lbl.text()) + 32
                if cat_w > max_btn_w:
                    max_btn_w = cat_w

        # Ensure clearance for vertical scrollbar (16-20px) and margins
        self._optimal_expanded_width = max(
            max_btn_w + 24, self.DEFAULT_EXPANDED_WIDTH
        )
        self._expanded_width = self._optimal_expanded_width

    def adapt_to_window_width(self, window_width: int):
        """Dynamically adapt drawer width:
        - At default (1340px) or fullscreen/high resolutions: comfortably
          sized at optimal_expanded_width so the horizontal scrollbar
          disappears.
        - At smaller window widths (<1300px down to minimum 950px):
          gracefully shrinks down to min_expanded_width, allowing the
          horizontal scrollbar to appear as needed.
        """
        if window_width >= 1300:
            target_w = self._optimal_expanded_width
        else:
            ratio = max(0.0, min(1.0, (window_width - 950) / 350.0))
            target_w = int(
                self._min_expanded_width
                + (self._optimal_expanded_width - self._min_expanded_width)
                * ratio
            )

        self._expanded_width = target_w
        if not self._is_collapsed:
            if (
                hasattr(self, "anim")
                and self.anim.state() == QPropertyAnimation.State.Running
            ):
                self.anim.stop()
            if (
                hasattr(self, "anim_min")
                and self.anim_min.state() == QPropertyAnimation.State.Running
            ):
                self.anim_min.stop()
            self.setFixedWidth(target_w)

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
        """Toggle side drawer width between 0 and active expanded width."""
        self._is_collapsed = not self._is_collapsed
        target_width = 0 if self._is_collapsed else self._expanded_width

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

    @property
    def expanded_width(self) -> int:
        return self._expanded_width

    @property
    def optimal_expanded_width(self) -> int:
        return self._optimal_expanded_width

    @property
    def min_expanded_width(self) -> int:
        return self._min_expanded_width
