"""
Standalone test runner using standard library unittest and Python assertions.
"""

import os
import sys
import tempfile
import unittest
import numpy as np

# Set environment
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_cache"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bio_models.models import (
    LotkaVolterraCompetitionModel,
    ChemostatModel,
    LotkaVolterraPredatorPreyModel,
    RosenzweigMacArthurModel,
    TypeIIIPredatorPreyModel,
    ConsumerResourceModel,
    AVAILABLE_MODELS,
)
from bio_models.engine import simulate_model
from bio_models.presets import PRESETS


class TestBioModels(unittest.TestCase):

    def test_competition_continuous_simulation(self):
        model = LotkaVolterraCompetitionModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(20.0, 15.0), t_span=(0.0, 30.0), num_points=100, params=params)

        self.assertTrue(res.success)
        self.assertEqual(len(res.t), 100)
        self.assertEqual(len(res.n1), 100)
        self.assertEqual(len(res.n2), 100)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))
        self.assertGreater(res.n1[-1], 0)
        self.assertGreater(res.n2[-1], 0)

    def test_arbitrary_initial_and_end_time(self):
        """Verify models can start at arbitrary t_start != 0 and terminate at t_end."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params

        # 1. Positive non-zero start time
        res = simulate_model(model, initial_state=(20.0, 15.0), t_span=(15.0, 75.0), num_points=100, params=params)
        self.assertTrue(res.success)
        self.assertAlmostEqual(res.t[0], 15.0, places=5)
        self.assertAlmostEqual(res.t[-1], 75.0, places=5)
        self.assertEqual(len(res.t), 100)

        # 2. Negative start time
        res_neg = simulate_model(model, initial_state=(20.0, 15.0), t_span=(-10.0, 30.0), num_points=100, params=params)
        self.assertTrue(res_neg.success)
        self.assertAlmostEqual(res_neg.t[0], -10.0, places=5)
        self.assertAlmostEqual(res_neg.t[-1], 30.0, places=5)

        # 3. Discrete recurrence with arbitrary time span
        res_disc = simulate_model(model, initial_state=(20.0, 15.0), t_span=(10.0, 50.0), num_points=40, params=params, mode="discrete")
        self.assertTrue(res_disc.success)
        self.assertAlmostEqual(res_disc.t[0], 10.0, places=5)
        self.assertAlmostEqual(res_disc.t[-1], 50.0, places=5)

        # 4. Inverted/invalid time span fallback (t_end <= t_start)
        res_fallback = simulate_model(model, initial_state=(20.0, 15.0), t_span=(50.0, 20.0), num_points=50, params=params)
        self.assertTrue(res_fallback.success)
        self.assertAlmostEqual(res_fallback.t[0], 50.0, places=5)
        self.assertGreater(res_fallback.t[-1], res_fallback.t[0])

    def test_positive_integer_initial_conditions(self):
        """Verify engine enforces positive integers (>= 1) for initial species individuals."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params

        # Floating numbers and negative inputs coerced to positive integers >= 1
        res = simulate_model(model, initial_state=(25.7, -4.0), t_span=(0.0, 20.0), num_points=50, params=params)
        self.assertTrue(res.success)
        self.assertEqual(res.n1[0], 26.0)
        self.assertEqual(res.n2[0], 1.0)

        # Zero coerced to positive integer >= 1
        res_zero = simulate_model(model, initial_state=(0.0, 0.0), t_span=(0.0, 20.0), num_points=50, params=params)
        self.assertTrue(res_zero.success)
        self.assertEqual(res_zero.n1[0], 1.0)
        self.assertEqual(res_zero.n2[0], 1.0)

    def test_competition_discrete_recursion(self):
        model = LotkaVolterraCompetitionModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(20.0, 15.0), num_points=50, params=params, mode="discrete")

        self.assertTrue(res.success)
        self.assertEqual(len(res.t), 50)
        self.assertEqual(res.metadata["mode"], "discrete")
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))

    def test_competition_relationship_classification(self):
        model = LotkaVolterraCompetitionModel()
        self.assertIn("Mutualistic", model.classify_relationship(-0.5, -0.4))
        self.assertIn("Competitive", model.classify_relationship(0.5, 0.4))
        self.assertIn("Parasitic", model.classify_relationship(0.5, -0.4))
        self.assertIn("Parasitic", model.classify_relationship(-0.5, 0.4))
        self.assertIn("Commensal", model.classify_relationship(-0.5, 0.0))
        self.assertIn("Amensal", model.classify_relationship(0.5, 0.0))

    def test_classic_predator_prey_oscillations(self):
        model = LotkaVolterraPredatorPreyModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(30.0, 10.0), t_span=(0.0, 40.0), num_points=200, params=params)

        self.assertTrue(res.success)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))
        self.assertGreater(float(np.std(res.n1)), 2.0)
        self.assertGreater(float(np.std(res.n2)), 2.0)

    def test_chemostat_model_eq_317(self):
        model = ChemostatModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(20.0, 5.0), t_span=(0.0, 50.0), num_points=100, params=params)

        self.assertTrue(res.success)
        self.assertGreater(res.n1[-1], 0)
        self.assertGreater(res.n2[-1], 0)

    def test_rosenzweig_macarthur_limit_cycle(self):
        model = RosenzweigMacArthurModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(40.0, 15.0), t_span=(0.0, 80.0), num_points=250, params=params)

        self.assertTrue(res.success)
        self.assertGreater(float(np.max(res.n1)), float(np.min(res.n1)) * 1.5)

    def test_type_iii_model(self):
        model = TypeIIIPredatorPreyModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(30.0, 10.0), t_span=(0.0, 50.0), num_points=100, params=params)

        self.assertTrue(res.success)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))

    def test_modular_consumer_resource_combinations(self):
        f_types = ["constant_inflow", "constant_outflow", "exponential", "logistic", "exponential_decline"]
        g_types = ["type_1_linear", "type_2_saturating", "type_3_generalized"]

        for f in f_types:
            for g in g_types:
                model = ConsumerResourceModel(f_type=f, g_type=g, h_type="linear_death")
                params = model.default_params
                res = simulate_model(model, initial_state=(25.0, 10.0), t_span=(0.0, 15.0), num_points=50, params=params)
                self.assertTrue(res.success, f"Failed for f={f}, g={g}")

    def test_nullclines_generation(self):
        model = LotkaVolterraCompetitionModel()
        nullclines = model.get_nullclines(model.default_params, (0, 150), (0, 150))
        self.assertGreater(len(nullclines), 0)

    def test_jpeg_export(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        model = LotkaVolterraPredatorPreyModel()
        res = simulate_model(model, initial_state=(25.0, 10.0), t_span=(0.0, 20.0), num_points=100)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        ax1.plot(res.t, res.n1)
        ax2.plot(res.n1, res.n2)

        with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            fig.savefig(tmp_path, format="jpeg", dpi=200)
            plt.close(fig)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 1000)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestGUIComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_main_window_and_drawer(self):
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        self.assertIsNotNone(window)
        self.assertTrue(window.windowTitle().startswith("BioModel Studio"))

        # Test sandwich drawer
        self.assertGreater(len(window.drawer._buttons), 0)
        self.assertFalse(window.drawer.is_collapsed)
        window.drawer.toggle_collapse()
        self.assertTrue(window.drawer.is_collapsed)

        # Test parameter extraction and simulation
        window.run_simulation()
        res = window.canvas_widget._current_result
        self.assertIsNotNone(res)
        self.assertTrue(res.success)

        # Test JPEG export from the canvas widget
        temp_jpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_gui_export.jpeg")
        try:
            exported = window.canvas_widget.save_graph_as_jpeg(temp_jpeg)
            self.assertEqual(exported, temp_jpeg)
            self.assertTrue(os.path.exists(temp_jpeg))
            self.assertGreater(os.path.getsize(temp_jpeg), 1000)
        finally:
            if os.path.exists(temp_jpeg):
                os.remove(temp_jpeg)

        window.close()

    def test_theme_switching(self):
        from bio_models.ui.main_window import MainWindow

        window = MainWindow(default_theme="light")
        self.assertEqual(window.current_theme, "light")
        self.assertTrue(window.light_theme_action.isChecked())
        self.assertFalse(window.dark_theme_action.isChecked())
        self.assertEqual(window.canvas_widget.theme, "light")

        # Switch to dark theme
        window.apply_theme("dark")
        self.assertEqual(window.current_theme, "dark")
        self.assertTrue(window.dark_theme_action.isChecked())
        self.assertFalse(window.light_theme_action.isChecked())
        self.assertEqual(window.canvas_widget.theme, "dark")

        # Toggle back to light theme via quick button
        window._toggle_quick_theme()
        self.assertEqual(window.current_theme, "light")
        self.assertTrue(window.light_theme_action.isChecked())
        self.assertEqual(window.canvas_widget.theme, "light")

        window.close()

    def test_gui_time_span_controls(self):
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        # Set custom start time and end time
        window.param_panel.t_start_spin.setValue(12.5)
        window.param_panel.t_end_spin.setValue(82.5)

        inputs = window.param_panel.get_simulation_inputs()
        self.assertEqual(inputs["t_span"], (12.5, 82.5))

        # Run simulation and check result t bounds
        window.run_simulation()
        res = window.canvas_widget._current_result
        self.assertIsNotNone(res)
        self.assertTrue(res.success)
        self.assertAlmostEqual(res.t[0], 12.5, places=5)
        self.assertAlmostEqual(res.t[-1], 82.5, places=5)

        # Test automatic adjustment when t_start exceeds t_end
        window.param_panel.t_start_spin.setValue(100.0)
        self.assertGreater(window.param_panel.t_end_spin.value(), 100.0)

        window.close()

    def test_gui_positive_integer_population_spins(self):
        from PyQt6.QtWidgets import QSpinBox
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        # Check that n1 and n2 inputs are QSpinBox (integer only)
        self.assertIsInstance(window.param_panel.n1_init_spin, QSpinBox)
        self.assertIsInstance(window.param_panel.n2_init_spin, QSpinBox)

        # Check positive integer constraints: minimum is 1 (no negatives, no zero)
        self.assertEqual(window.param_panel.n1_init_spin.minimum(), 1)
        self.assertEqual(window.param_panel.n2_init_spin.minimum(), 1)

        # Set custom positive integer values
        window.param_panel.n1_init_spin.setValue(45)
        window.param_panel.n2_init_spin.setValue(30)

        inputs = window.param_panel.get_simulation_inputs()
        init_state = inputs["initial_state"]
        self.assertEqual(init_state, (45, 30))
        self.assertIsInstance(init_state[0], int)
        self.assertIsInstance(init_state[1], int)

        # Check integer carrying capacities K1 and K2 in competition model
        k1_spin = window.param_panel._param_inputs["K1"]
        self.assertIsInstance(k1_spin, QSpinBox)
        self.assertGreaterEqual(k1_spin.minimum(), 1)

        window.run_simulation()
        res = window.canvas_widget._current_result
        self.assertEqual(res.n1[0], 45.0)
        self.assertEqual(res.n2[0], 30.0)

        window.close()

    def test_no_overlapping_model_headers_on_model_switch(self):
        """Verify that switching models cleanly deletes old headers and prevents overlapping text."""
        from PyQt6.QtWidgets import QApplication, QLabel
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        # Iterate through multiple models
        for model in AVAILABLE_MODELS[:4]:
            window._on_model_selected(model, "continuous")
            QApplication.processEvents()

            # Find all title labels in param_panel
            title_labels = [
                lbl for lbl in window.param_panel.findChildren(QLabel)
                if lbl.objectName() == "ModelTitle"
            ]
            # Must be exactly 1 title label, never duplicate/overlapping!
            self.assertEqual(len(title_labels), 1, f"Expected 1 title label for {model.name}, got {len(title_labels)}")
            self.assertEqual(title_labels[0].text(), model.name)

            # Find all mode badges
            mode_badges = [
                lbl for lbl in window.param_panel.findChildren(QLabel)
                if lbl.objectName() == "ModelBadge"
            ]
            self.assertEqual(len(mode_badges), 1, f"Expected 1 mode badge for {model.name}, got {len(mode_badges)}")

        window.close()

    def test_combobox_view_and_theme_palette(self):
        """Verify combobox view is a QListView and palette colors match light and dark themes."""
        from PyQt6.QtGui import QPalette
        from PyQt6.QtWidgets import QListView
        from bio_models.ui.main_window import MainWindow

        window = MainWindow(default_theme="light")
        preset_combo = window.param_panel.preset_combo

        # Verify QListView is used (bypasses Cocoa native popup)
        self.assertIsInstance(preset_combo.view(), QListView)

        # Light theme combobox view palette checks
        base_color = preset_combo.view().palette().color(QPalette.ColorRole.Base).name().lower()
        text_color = preset_combo.view().palette().color(QPalette.ColorRole.Text).name().lower()
        self.assertEqual(base_color, "#ffffff")
        self.assertEqual(text_color, "#0f172a")

        # Switch to dark theme
        window.apply_theme("dark")
        base_color_dark = preset_combo.view().palette().color(QPalette.ColorRole.Base).name().lower()
        text_color_dark = preset_combo.view().palette().color(QPalette.ColorRole.Text).name().lower()
        self.assertEqual(base_color_dark, "#1e293b")
        self.assertEqual(text_color_dark, "#f8fafc")

        window.close()

    def test_drawer_responsive_width_and_scrollbar(self):
        """
        Verify that in default (1340px) and fullscreen (1920px) resolutions the drawer
        dynamically sizes to fit full model names and the horizontal scrollbar disappears;
        whereas in small window resolutions (950px), the drawer compresses and the
        horizontal scrollbar appears so the user can scroll across the menu.
        """
        from PyQt6.QtWidgets import QApplication
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        window.resize(1340, 820)
        window.show()
        QApplication.processEvents()

        # 1. Default resolution (1340x820)
        self.assertGreaterEqual(window.drawer.width(), 350)
        self.assertEqual(window.drawer.width(), window.drawer.optimal_expanded_width)
        hbar = window.drawer.scroll_area.horizontalScrollBar()
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        # 2. Fullscreen / wide resolution (1920x1080)
        window.resize(1920, 1080)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(), window.drawer.optimal_expanded_width)
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        # 3. Small / compressed resolution (950x600)
        window.resize(950, 600)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(), window.drawer.min_expanded_width)
        self.assertTrue(hbar.isVisible())
        self.assertGreater(hbar.maximum(), 0)

        # 4. Resize back to default (1340x820)
        window.resize(1340, 820)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(), window.drawer.optimal_expanded_width)
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        window.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)


