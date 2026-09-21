"""Unit test for PyQt6 GUI components in offscreen mode."""

import os
import sys

import pytest
from PyQt6.QtWidgets import QApplication

from bio_models.ui.main_window import MainWindow

# Use offscreen platform for headless test execution
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_cache"),
)


@pytest.fixture(scope="session")
def qapp():
    """Ensure QApplication instance is available."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_main_window_creation(qapp):
    """Verify MainWindow creation, drawer toggle, simulation, and export."""
    window = MainWindow()
    assert window is not None
    assert window.windowTitle().startswith("BioModel Studio")

    # Check drawer exists and has buttons
    assert window.drawer is not None
    assert len(window.drawer._buttons) > 0

    # Toggle sandwich drawer
    initial_collapsed = window.drawer.is_collapsed
    window.drawer.toggle_collapse()
    assert window.drawer.is_collapsed != initial_collapsed

    # Check parameter panel and canvas
    assert window.param_panel is not None
    assert window.canvas_widget is not None

    # Simulate model
    window.run_simulation()
    assert window.canvas_widget._current_result is not None
    assert window.canvas_widget._current_result.success is True

    # Test JPEG export to temporary file
    temp_jpeg = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_export.jpeg"
    )
    try:
        exported = window.canvas_widget.save_graph_as_jpeg(temp_jpeg)
        assert exported == temp_jpeg
        assert os.path.exists(temp_jpeg)
        assert os.path.getsize(temp_jpeg) > 1000
    finally:
        if os.path.exists(temp_jpeg):
            os.remove(temp_jpeg)
