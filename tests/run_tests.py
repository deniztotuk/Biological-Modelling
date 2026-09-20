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


if __name__ == "__main__":
    unittest.main(verbosity=2)
