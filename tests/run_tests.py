"""Standalone test runner using standard library unittest and assertions."""

import os
import sys
import tempfile
import unittest

import numpy as np

# Set offscreen environment for Qt and Matplotlib before GUI modules.
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_cache"),
)
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from bio_models.engine import (  # noqa: E402
    export_simulation_to_csv,
    simulate_model,
)
from bio_models.models import (  # noqa: E402
    AVAILABLE_MODELS,
    ChemostatModel,
    ConsumerResourceModel,
    ExponentialGrowthModel,
    LogisticGrowthModel,
    LotkaVolterraCompetitionModel,
    LotkaVolterraPredatorPreyModel,
    RosenzweigMacArthurModel,
    TypeIIIPredatorPreyModel,
)


class TestBioModels(unittest.TestCase):
    """Unit test suite for biological models and simulation engine."""

    def test_competition_continuous_simulation(self):
        """Verify continuous simulation for competition model."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params
        res = simulate_model(
            model,
            initial_state=(20.0, 15.0),
            t_span=(0.0, 30.0),
            num_points=100,
            params=params,
        )

        self.assertTrue(res.success)
        self.assertEqual(len(res.t), 100)
        self.assertEqual(len(res.n1), 100)
        self.assertEqual(len(res.n2), 100)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))
        self.assertGreater(res.n1[-1], 0)
        self.assertGreater(res.n2[-1], 0)

    def test_arbitrary_initial_and_end_time(self):
        """Verify models start at arbitrary t_start and reach t_end."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params

        # 1. Positive non-zero start time
        res = simulate_model(
            model,
            initial_state=(20.0, 15.0),
            t_span=(15.0, 75.0),
            num_points=100,
            params=params,
        )
        self.assertTrue(res.success)
        self.assertAlmostEqual(res.t[0], 15.0, places=5)
        self.assertAlmostEqual(res.t[-1], 75.0, places=5)
        self.assertEqual(len(res.t), 100)

        # 2. Negative start time
        res_neg = simulate_model(
            model,
            initial_state=(20.0, 15.0),
            t_span=(-10.0, 30.0),
            num_points=100,
            params=params,
        )
        self.assertTrue(res_neg.success)
        self.assertAlmostEqual(res_neg.t[0], -10.0, places=5)
        self.assertAlmostEqual(res_neg.t[-1], 30.0, places=5)

        # 3. Discrete recurrence with arbitrary time span
        res_disc = simulate_model(
            model,
            initial_state=(20.0, 15.0),
            t_span=(10.0, 50.0),
            num_points=40,
            params=params,
            mode="discrete",
        )
        self.assertTrue(res_disc.success)
        self.assertAlmostEqual(res_disc.t[0], 10.0, places=5)
        self.assertAlmostEqual(res_disc.t[-1], 50.0, places=5)

        # 4. Inverted/invalid time span fallback (t_end <= t_start)
        res_fallback = simulate_model(
            model,
            initial_state=(20.0, 15.0),
            t_span=(50.0, 20.0),
            num_points=50,
            params=params,
        )
        self.assertTrue(res_fallback.success)
        self.assertAlmostEqual(res_fallback.t[0], 50.0, places=5)
        self.assertGreater(res_fallback.t[-1], res_fallback.t[0])

    def test_positive_integer_initial_conditions(self):
        """Verify engine enforces positive integers (>= 1) for counts."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params

        # Floating numbers and negative inputs coerced to positive
        # integers >= 1
        res = simulate_model(
            model,
            initial_state=(25.7, -4.0),
            t_span=(0.0, 20.0),
            num_points=50,
            params=params,
        )
        self.assertTrue(res.success)
        self.assertEqual(res.n1[0], 26.0)
        self.assertEqual(res.n2[0], 1.0)

        # Zero coerced to positive integer >= 1
        res_zero = simulate_model(model, initial_state=(
            0.0, 0.0), t_span=(0.0, 20.0), num_points=50, params=params)
        self.assertTrue(res_zero.success)
        self.assertEqual(res_zero.n1[0], 1.0)
        self.assertEqual(res_zero.n2[0], 1.0)

    def test_competition_discrete_recursion(self):
        """Verify discrete recursion for competition model."""
        model = LotkaVolterraCompetitionModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(
            20.0, 15.0), num_points=50, params=params, mode="discrete")

        self.assertTrue(res.success)
        self.assertEqual(len(res.t), 50)
        self.assertEqual(res.metadata["mode"], "discrete")
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))

    def test_competition_relationship_classification(self):
        """Verify relationship classification based on alphas."""
        model = LotkaVolterraCompetitionModel()
        self.assertIn("Mutualistic", model.classify_relationship(-0.5, -0.4))
        self.assertIn("Competitive", model.classify_relationship(0.5, 0.4))
        self.assertIn("Parasitic", model.classify_relationship(0.5, -0.4))
        self.assertIn("Parasitic", model.classify_relationship(-0.5, 0.4))
        self.assertIn("Commensal", model.classify_relationship(-0.5, 0.0))
        self.assertIn("Amensal", model.classify_relationship(0.5, 0.0))

    def test_classic_predator_prey_oscillations(self):
        """Verify oscillatory dynamics in Lotka-Volterra."""
        model = LotkaVolterraPredatorPreyModel()
        params = model.default_params
        res = simulate_model(model, initial_state=(30.0, 10.0), t_span=(
            0.0, 40.0), num_points=200, params=params)

        self.assertTrue(res.success)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))
        self.assertGreater(float(np.std(res.n1)), 2.0)
        self.assertGreater(float(np.std(res.n2)), 2.0)

    def test_chemostat_model(self):
        """Verify nutrient inflow and consumer dynamics."""
        model = ChemostatModel()
        params = model.default_params
        res = simulate_model(
            model,
            initial_state=(20.0, 5.0),
            t_span=(0.0, 50.0),
            num_points=100,
            params=params,
        )

        self.assertTrue(res.success)
        self.assertGreater(res.n1[-1], 0)
        self.assertGreater(res.n2[-1], 0)

    def test_rosenzweig_macarthur_limit_cycle(self):
        """Verify limit cycle generation in Type II system."""
        model = RosenzweigMacArthurModel()
        params = model.default_params
        res = simulate_model(
            model,
            initial_state=(40.0, 15.0),
            t_span=(0.0, 80.0),
            num_points=250,
            params=params,
        )

        self.assertTrue(res.success)
        self.assertGreater(float(np.max(res.n1)), float(np.min(res.n1)) * 1.5)

    def test_type_iii_model(self):
        """Verify sigmoid functional response dynamics."""
        model = TypeIIIPredatorPreyModel()
        params = model.default_params
        res = simulate_model(
            model,
            initial_state=(30.0, 10.0),
            t_span=(0.0, 50.0),
            num_points=100,
            params=params,
        )

        self.assertTrue(res.success)
        self.assertTrue(np.all(res.n1 >= 0))
        self.assertTrue(np.all(res.n2 >= 0))

    def test_modular_consumer_resource_combinations(self):
        """Verify modular consumer-resource combinations."""
        f_types = [
            "constant_inflow",
            "constant_outflow",
            "exponential",
            "logistic",
            "exponential_decline",
        ]
        g_types = [
            "type_1_linear",
            "type_2_saturating",
            "type_3_generalized",
        ]

        for f in f_types:
            for g in g_types:
                model = ConsumerResourceModel(
                    f_type=f, g_type=g, h_type="linear_death"
                )
                params = model.default_params
                res = simulate_model(
                    model,
                    initial_state=(25.0, 10.0),
                    t_span=(0.0, 15.0),
                    num_points=50,
                    params=params,
                )
                self.assertTrue(res.success, f"Failed for f={f}, g={g}")

    def test_nullclines_generation(self):
        """Verify nullcline coordinate computation."""
        model = LotkaVolterraCompetitionModel()
        nullclines = model.get_nullclines(
            model.default_params, (0.0, 150.0), (0.0, 150.0)
        )
        self.assertGreater(len(nullclines), 0)

    def test_jpeg_export(self):
        """Verify high-resolution JPEG graph export."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        model = LotkaVolterraPredatorPreyModel()
        res = simulate_model(
            model,
            initial_state=(25.0, 10.0),
            t_span=(0.0, 20.0),
            num_points=100,
        )

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

    def test_csv_export(self):
        """Verify simulation time-series CSV data export."""
        model = LogisticGrowthModel()
        res = simulate_model(
            model,
            initial_state=(15.0,),
            t_span=(0.0, 25.0),
            num_points=50,
        )

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            exported_path = export_simulation_to_csv(res, tmp_path)
            self.assertEqual(exported_path, tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 50)

            with open(tmp_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]

            # Validate header comments and columns.
            self.assertTrue(lines[0].startswith("# BioModel Studio"))
            self.assertIn("Logistic Growth", lines[1])
            self.assertIn("continuous", lines[2])
            self.assertEqual(lines[5], "time,n")
            # Total of 5 comment lines, 1 header, and 50 data rows.
            self.assertEqual(len(lines), 56)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Test frequency model CSV export.
        from bio_models.models import HaploidSelectionModel

        freq_model = HaploidSelectionModel()
        freq_res = simulate_model(
            freq_model,
            initial_state=(0.2, 0.8),
            t_span=(0.0, 20.0),
            num_points=30,
        )
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            freq_tmp = tmp.name

        try:
            export_simulation_to_csv(freq_res, freq_tmp)
            with open(freq_tmp, "r", encoding="utf-8") as f:
                freq_lines = [row.strip() for row in f.readlines()]
            self.assertEqual(freq_lines[6], "time,p,q")
            self.assertEqual(len(freq_lines), 37)
        finally:
            if os.path.exists(freq_tmp):
                os.remove(freq_tmp)

    def test_exponential_growth_model_analytical_and_discrete(self):
        """Verify Exponential Growth matches analytical solution."""
        model = ExponentialGrowthModel()
        self.assertEqual(model.num_variables, 1)
        self.assertTrue(model.is_single_variable)

        # 1. Analytical test: dn/dt = r * n => n(t) = n0 * exp(r * t)
        n0 = 8.0
        r = 1.10
        res = simulate_model(
            model=model,
            initial_state=(n0, 0.0),
            t_span=(0.0, 3.0),
            num_points=100,
            params={"r": r},
            mode="continuous",
        )
        self.assertTrue(res.success)
        expected_final = n0 * np.exp(r * 3.0)
        self.assertAlmostEqual(res.n1[-1], expected_final, delta=0.5)

        # 2. Discrete test: n(t+1) = (1 + r) * n(t) = R * n(t)
        # Protection Island Pheasant benchmark (Lack 1954).
        # R = 3.0 => r = 2.0. Generations: 8 -> 24 -> 72 -> 216
        curr = np.array([8.0])
        gen1 = model.discrete_step(curr, {"r": 2.0})[0]
        self.assertAlmostEqual(gen1, 24.0)
        gen2 = model.discrete_step(np.array([gen1]), {"r": 2.0})[0]
        self.assertAlmostEqual(gen2, 72.0)
        gen3 = model.discrete_step(np.array([gen2]), {"r": 2.0})[0]
        self.assertAlmostEqual(gen3, 216.0)

        # 3. Extinction decay test: r = -0.2 < 0
        res_decay = simulate_model(
            model=model,
            initial_state=(100.0, 0.0),
            t_span=(0.0, 20.0),
            num_points=50,
            params={"r": -0.2},
            mode="continuous",
        )
        self.assertTrue(res_decay.n1[-1] < res_decay.n1[0])

    def test_logistic_growth_model_saturation_and_discrete(self):
        """Verify Logistic Growth saturation at K and recursion."""
        model = LogisticGrowthModel()
        self.assertEqual(model.num_variables, 1)
        self.assertTrue(model.is_single_variable)

        # 1. Continuous saturation at carrying capacity K = 100
        res = simulate_model(
            model=model,
            initial_state=(5.0, 0.0),
            t_span=(0.0, 40.0),
            num_points=200,
            params={"r": 0.6, "K": 100.0},
            mode="continuous",
        )
        self.assertTrue(res.success)
        self.assertAlmostEqual(res.n1[-1], 100.0, delta=0.5)

        # 2. Overcapacity decline: n0 = 180 > K = 100
        res_over = simulate_model(
            model=model,
            initial_state=(180.0, 0.0),
            t_span=(0.0, 30.0),
            num_points=150,
            params={"r": 0.5, "K": 100.0},
            mode="continuous",
        )
        self.assertTrue(res_over.success)
        self.assertTrue(res_over.n1[0] > 100.0)
        self.assertAlmostEqual(res_over.n1[-1], 100.0, delta=0.5)

        # 3. Discrete recursion
        curr = np.array([10.0])
        for _ in range(30):
            curr = model.discrete_step(curr, {"r": 0.55, "K": 370.0})
        self.assertAlmostEqual(curr[0], 370.0, delta=1.0)

    def test_logistic_growth_presets_and_names(self):
        """Verify yeast presets and (May 1976) removed from names."""
        from bio_models.presets import PRESETS
        from bio_models.model_info import MODEL_DETAILS

        presets = PRESETS.get("Logistic Growth Model", [])
        preset_names = [p["name"] for p in presets]

        # 1. Verify yeast culture presets removed from logistic model.
        for name in preset_names:
            self.assertNotIn("Yeast", name)
            self.assertNotIn("Haploid", name)
            self.assertNotIn("Diploid", name)

        # 2. Verify remaining presets
        self.assertIn("Sigmoidal Carrying Capacity Approach", preset_names)
        self.assertIn("Overcapacity Crash & Damping", preset_names)
        self.assertIn("Discrete Chaos & Limit Cycles", preset_names)

        # 3. Verify (May 1976) reference removed from chaotic name.
        self.assertNotIn(
            "Discrete Chaos & Limit Cycles (May 1976)", preset_names
        )
        for name in preset_names:
            self.assertNotIn("May 1976", name)

        # 4. Verify info scenarios heading does not contain (May 1976).
        scenarios = MODEL_DETAILS["Logistic Growth Model"]["scenarios"]
        self.assertIn("<b>Discrete Overshoot & Chaos</b>", scenarios)
        self.assertNotIn("Discrete Overshoot & Chaos (May 1976)", scenarios)

    def test_discrete_ladder_step_counts_and_exponential_benchmark(self):
        """Verify discrete simulation produces exact step counts."""
        model = ExponentialGrowthModel()
        # Initial: 16, r: 2.0, t: [0, 15] => 15 steps, 16 points.
        res = simulate_model(
            model=model,
            initial_state=(16.0, 0.0),
            t_span=(0.0, 15.0),
            params={"r": 2.0},
            mode="discrete",
        )
        self.assertTrue(res.success)
        self.assertEqual(len(res.t), 16)
        self.assertEqual(res.metadata["steps"], 15)
        self.assertTrue(np.allclose(res.t, np.arange(0, 16, dtype=float)))
        self.assertAlmostEqual(res.n1[0], 16.0)
        self.assertAlmostEqual(res.n1[1], 48.0)
        self.assertAlmostEqual(res.n1[2], 144.0)
        expected_final = 16.0 * (3.0 ** 15)
        self.assertAlmostEqual(res.n1[-1], expected_final, delta=1.0)
        self.assertIn("15 steps", res.message)

        # Explicit num_points backward compatibility check
        res_custom = simulate_model(
            model=model,
            initial_state=(10.0, 0.0),
            t_span=(0.0, 10.0),
            num_points=50,
            params={"r": 0.5},
            mode="discrete",
        )
        self.assertEqual(len(res_custom.t), 50)
        self.assertEqual(res_custom.metadata["steps"], 49)

    def test_all_models_discrete_simulation_and_ladder_properties(self):
        """Verify discrete simulation across all available models."""
        for model in AVAILABLE_MODELS:
            init = (
                (20.0, 10.0)
                if not model.is_single_variable
                else (20.0, 0.0)
            )
            res = simulate_model(
                model=model,
                initial_state=init,
                t_span=(0.0, 15.0),
                params=model.default_params,
                mode="discrete",
            )
            self.assertTrue(
                res.success, f"Discrete run failed: {model.name}"
            )
            self.assertEqual(len(res.t), 16)
            self.assertEqual(res.metadata["steps"], 15)
            self.assertTrue(np.all(np.isfinite(res.n1)))
            self.assertTrue(np.all(res.n1 >= 0.0))
            if not model.is_single_variable:
                self.assertTrue(np.all(np.isfinite(res.n2)))
                self.assertTrue(np.all(res.n2 >= 0.0))

    def test_haploid_selection_model(self):
        """Verify Haploid Selection dynamics in continuous and discrete."""
        from bio_models.models import HaploidSelectionModel

        model = HaploidSelectionModel()
        self.assertEqual(model.topic, "Evolution Models")
        self.assertEqual(model.category, "Natural Selection Models")
        self.assertTrue(model.is_frequency_model)

        # 1. Continuous directional selection: W_A > W_a => p increases
        res_cont = simulate_model(
            model=model,
            initial_state=(0.05, 0.95),
            t_span=(0.0, 30.0),
            num_points=150,
            params={"W_A": 1.25, "W_a": 1.00},
            mode="continuous",
        )
        self.assertTrue(res_cont.success)
        self.assertAlmostEqual(res_cont.n1[0], 0.05, places=3)
        self.assertAlmostEqual(res_cont.n2[0], 0.95, places=3)
        self.assertGreater(res_cont.n1[-1], res_cont.n1[0])
        self.assertTrue(np.allclose(res_cont.n1 + res_cont.n2, 1.0))

        # 2. Discrete recursion matching analytical formula
        # p(1) = W_A * p0 / (W_A * p0 + W_a * (1 - p0))
        res_disc = simulate_model(
            model=model,
            initial_state=(0.20, 0.80),
            t_span=(0.0, 5.0),
            params={"W_A": 1.50, "W_a": 1.00},
            mode="discrete",
        )
        self.assertTrue(res_disc.success)
        expected_p1 = (1.50 * 0.20) / (1.50 * 0.20 + 1.00 * 0.80)
        self.assertAlmostEqual(res_disc.n1[1], expected_p1, places=4)
        self.assertAlmostEqual(res_disc.n2[1], 1.0 - expected_p1, places=4)

        # 3. Neutral evolution: W_A == W_a => p remains constant
        res_neutral = simulate_model(
            model=model,
            initial_state=(0.40, 0.60),
            t_span=(0.0, 10.0),
            params={"W_A": 1.00, "W_a": 1.00},
            mode="discrete",
        )
        self.assertTrue(res_neutral.success)
        self.assertAlmostEqual(res_neutral.n1[-1], 0.40, places=4)

    def test_diploid_selection_model(self):
        """Verify Diploid Selection dynamics and overdominance."""
        from bio_models.models import DiploidSelectionModel

        model = DiploidSelectionModel()
        self.assertEqual(model.topic, "Evolution Models")
        self.assertEqual(model.category, "Natural Selection Models")
        self.assertTrue(model.is_frequency_model)

        # 1. Overdominance (heterozygote advantage) stable polymorphism
        # W_AA = 0.9, W_Aa = 1.2, W_aa = 0.6
        # Expected p* = (W_aa - W_Aa) / (W_AA - 2*W_Aa + W_aa)
        # = (0.6 - 1.2) / (0.9 - 2.4 + 0.6) = -0.6 / -0.9 = 2/3 ≈ 0.6667
        res_poly = simulate_model(
            model=model,
            initial_state=(0.10, 0.90),
            t_span=(0.0, 50.0),
            num_points=200,
            params={"W_AA": 0.90, "W_Aa": 1.20, "W_aa": 0.60},
            mode="continuous",
        )
        self.assertTrue(res_poly.success)
        self.assertAlmostEqual(res_poly.n1[-1], 2.0 / 3.0, delta=0.02)
        self.assertAlmostEqual(res_poly.n2[-1], 1.0 / 3.0, delta=0.02)

        # 2. Discrete recursion formula check:
        # W_bar = p0^2 * W_AA + 2*p0*q0 * W_Aa + q0^2 * W_aa
        # p1 = (p0^2 * W_AA + p0*q0 * W_Aa) / W_bar
        p0 = 0.30
        q0 = 0.70
        w_aa, w_ab, w_bb = 1.30, 1.15, 1.00
        w_bar = (p0 ** 2) * w_aa + 2.0 * p0 * q0 * w_ab + (q0 ** 2) * w_bb
        expected_p1 = ((p0 ** 2) * w_aa + p0 * q0 * w_ab) / w_bar

        res_disc = simulate_model(
            model=model,
            initial_state=(p0, q0),
            t_span=(0.0, 5.0),
            params={"W_AA": w_aa, "W_Aa": w_ab, "W_aa": w_bb},
            mode="discrete",
        )
        self.assertTrue(res_disc.success)
        self.assertAlmostEqual(res_disc.n1[1], expected_p1, places=4)
        self.assertAlmostEqual(res_disc.n2[1], 1.0 - expected_p1, places=4)

    def test_mutation_selection_model(self):
        """Verify Mutation-Selection dynamics and neutral drift."""
        from bio_models.models import MutationSelectionModel
        from bio_models.presets import PRESETS

        model = MutationSelectionModel()
        self.assertEqual(model.topic, "Evolution Models")
        self.assertEqual(model.category, "Natural Selection Models")
        self.assertTrue(model.is_frequency_model)

        # 1. Null hypothesis stasis with equal fitness and zero mutation.
        res_null = simulate_model(
            model=model,
            initial_state=(0.35, 0.65),
            t_span=(0.0, 20.0),
            params={"W_A": 1.0, "W_a": 1.0, "mu": 0.0, "nu": 0.0},
            mode="continuous",
        )
        self.assertTrue(res_null.success)
        self.assertAlmostEqual(res_null.n1[0], 0.35, places=4)
        self.assertAlmostEqual(res_null.n1[-1], 0.35, places=4)
        self.assertTrue(np.allclose(res_null.n1 + res_null.n2, 1.0))

        # 2. Mutational equilibrium without selection: p̂ = ν / (μ + ν).
        mu, nu = 0.03, 0.01
        expected_p_eq = nu / (mu + nu)
        res_mut = simulate_model(
            model=model,
            initial_state=(0.80, 0.20),
            t_span=(0.0, 150.0),
            num_points=300,
            params={"W_A": 1.0, "W_a": 1.0, "mu": mu, "nu": nu},
            mode="continuous",
        )
        self.assertTrue(res_mut.success)
        self.assertAlmostEqual(res_mut.n1[-1], expected_p_eq, places=2)

        # 3. Discrete recursion matching analytical formula.
        # Formula: p* = W_A * p0 / (W_A * p0 + W_a * (1 - p0)).
        # Then: p1 = p* * (1 - mu) + (1 - p*) * nu.
        p0 = 0.40
        w_a, w_b, mu_d, nu_d = 1.20, 1.00, 0.02, 0.005
        p_sel = (w_a * p0) / (w_a * p0 + w_b * (1.0 - p0))
        expected_p1 = p_sel * (1.0 - mu_d) + (1.0 - p_sel) * nu_d

        res_disc = simulate_model(
            model=model,
            initial_state=(p0, 1.0 - p0),
            t_span=(0.0, 5.0),
            params={"W_A": w_a, "W_a": w_b, "mu": mu_d, "nu": nu_d},
            mode="discrete",
        )
        self.assertTrue(res_disc.success)
        self.assertAlmostEqual(res_disc.n1[1], expected_p1, places=4)
        self.assertAlmostEqual(res_disc.n2[1], 1.0 - expected_p1, places=4)

        # 4. Verify all presets for this model run successfully.
        presets = PRESETS[model.name]
        has_null_preset = any("Neutral Drift" in p["name"] for p in presets)
        self.assertTrue(has_null_preset)
        for preset in presets:
            res_p = simulate_model(
                model=model,
                initial_state=preset["initial"],
                t_span=preset["t_span"],
                params=preset["params"],
                mode="continuous",
            )
            self.assertTrue(res_p.success)

    def test_migration_selection_model(self):
        """Verify Migration-Selection dynamics and neutral drift."""
        from bio_models.models import MigrationSelectionModel
        from bio_models.presets import PRESETS

        model = MigrationSelectionModel()
        self.assertEqual(model.topic, "Evolution Models")
        self.assertEqual(model.category, "Natural Selection Models")
        self.assertTrue(model.is_frequency_model)

        # 1. Null hypothesis stasis with equal fitness and zero gene flow.
        res_null = simulate_model(
            model=model,
            initial_state=(0.42, 0.58),
            t_span=(0.0, 20.0),
            params={"W_A": 1.0, "W_a": 1.0, "m": 0.0, "p_m": 0.5},
            mode="continuous",
        )
        self.assertTrue(res_null.success)
        self.assertAlmostEqual(res_null.n1[0], 0.42, places=4)
        self.assertAlmostEqual(res_null.n1[-1], 0.42, places=4)
        self.assertTrue(np.allclose(res_null.n1 + res_null.n2, 1.0))

        # 2. Neutral gene flow: island frequency equilibrates to p_m.
        p_m = 0.70
        res_flow = simulate_model(
            model=model,
            initial_state=(0.10, 0.90),
            t_span=(0.0, 60.0),
            num_points=200,
            params={"W_A": 1.0, "W_a": 1.0, "m": 0.15, "p_m": p_m},
            mode="continuous",
        )
        self.assertTrue(res_flow.success)
        self.assertAlmostEqual(res_flow.n1[-1], p_m, places=2)

        # 3. Discrete recursion matching analytical formula.
        # Formula: p* = W_A * p0 / (W_A * p0 + W_a * (1 - p0)).
        # Then: p1 = (1 - m) * p* + m * p_m.
        p0 = 0.30
        w_a, w_b, m_rate, p_mainland = 1.30, 1.00, 0.08, 0.10
        p_sel = (w_a * p0) / (w_a * p0 + w_b * (1.0 - p0))
        expected_p1 = (1.0 - m_rate) * p_sel + m_rate * p_mainland

        res_disc = simulate_model(
            model=model,
            initial_state=(p0, 1.0 - p0),
            t_span=(0.0, 5.0),
            params={
                "W_A": w_a,
                "W_a": w_b,
                "m": m_rate,
                "p_m": p_mainland,
            },
            mode="discrete",
        )
        self.assertTrue(res_disc.success)
        self.assertAlmostEqual(res_disc.n1[1], expected_p1, places=4)
        self.assertAlmostEqual(res_disc.n2[1], 1.0 - expected_p1, places=4)

        # 4. Verify all presets for this model run successfully.
        presets = PRESETS[model.name]
        has_null_preset = any("Neutral Drift" in p["name"] for p in presets)
        self.assertTrue(has_null_preset)
        for preset in presets:
            res_p = simulate_model(
                model=model,
                initial_state=preset["initial"],
                t_span=preset["t_span"],
                params=preset["params"],
                mode="continuous",
            )
            self.assertTrue(res_p.success)


class TestGUIComponents(unittest.TestCase):
    """Test GUI components and user interaction workflows."""

    @classmethod
    def setUpClass(cls):
        """Initialize QApplication instance for GUI testing."""
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_main_window_and_drawer(self):
        """Verify main window initialization and sandwich drawer toggling."""
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
        temp_jpeg = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_gui_export.jpeg"
        )
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
        """Verify dynamic switching between light and dark visual themes."""
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
        """Verify time span input spinboxes and simulation integration."""
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
        """Verify integer spinbox constraints on initial population values."""
        from PyQt6.QtWidgets import QSpinBox
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        # Check that n1 and n2 inputs are QSpinBox (integer only)
        self.assertIsInstance(window.param_panel.n1_init_spin, QSpinBox)
        self.assertIsInstance(window.param_panel.n2_init_spin, QSpinBox)

        # Check positive integer constraints: minimum is 1 (>= 1)
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

        # Check integer carrying capacities K1 and K2 in competition
        k1_spin = window.param_panel._param_inputs["K1"]
        self.assertIsInstance(k1_spin, QSpinBox)
        self.assertGreaterEqual(k1_spin.minimum(), 1)

        window.run_simulation()
        res = window.canvas_widget._current_result
        self.assertEqual(res.n1[0], 45.0)
        self.assertEqual(res.n2[0], 30.0)

        window.close()

    def test_no_overlapping_model_headers_on_model_switch(self):
        """Verify that switching models cleanly deletes old headers."""
        from PyQt6.QtWidgets import QApplication, QLabel, QPushButton
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
            # Exactly 1 title label required; never duplicate.
            msg = f"Expected 1 title label for {model.name}"
            self.assertEqual(len(title_labels), 1, msg)
            self.assertEqual(title_labels[0].text(), model.name)

            # Find all mode badges
            mode_badges = [
                btn for btn in window.param_panel.findChildren(QPushButton)
                if btn.objectName() == "ModelBadge"
            ]
            badge_msg = f"Expected 1 mode badge for {model.name}"
            self.assertEqual(len(mode_badges), 1, badge_msg)

        window.close()

    def test_combobox_view_and_theme_palette(self):
        """Verify combobox view is QListView and palette matches themes."""
        from PyQt6.QtGui import QPalette
        from PyQt6.QtWidgets import QListView
        from bio_models.ui.main_window import MainWindow

        window = MainWindow(default_theme="light")
        preset_combo = window.param_panel.preset_combo

        # Verify QListView is used (bypasses Cocoa native popup)
        self.assertIsInstance(preset_combo.view(), QListView)

        # Light theme combobox view palette checks
        base_color = preset_combo.view().palette().color(
            QPalette.ColorRole.Base).name().lower()
        text_color = preset_combo.view().palette().color(
            QPalette.ColorRole.Text).name().lower()
        self.assertEqual(base_color, "#ffffff")
        self.assertEqual(text_color, "#0f172a")

        # Switch to dark theme
        window.apply_theme("dark")
        base_color_dark = preset_combo.view().palette().color(
            QPalette.ColorRole.Base).name().lower()
        text_color_dark = preset_combo.view().palette().color(
            QPalette.ColorRole.Text).name().lower()
        self.assertEqual(base_color_dark, "#1a1a1a")
        self.assertEqual(text_color_dark, "#f4f4f5")

        window.close()

    def test_drawer_responsive_width_and_scrollbar(self):
        """Verify drawer responsive width and scrollbar behavior.

        In default and fullscreen resolutions, the drawer dynamically
        sizes to fit full model names and horizontal scrollbar hides.
        In small resolutions, drawer compresses and scrollbar appears.
        """
        from PyQt6.QtWidgets import QApplication
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        window.resize(1340, 820)
        window.show()
        window.drawer.expand_topic("Ecology Models")
        QApplication.processEvents()

        # 1. Default resolution (1340x820)
        self.assertGreaterEqual(window.drawer.width(), 340)
        self.assertEqual(window.drawer.width(),
                         window.drawer.optimal_expanded_width)
        hbar = window.drawer.scroll_area.horizontalScrollBar()
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        # 2. Fullscreen / wide resolution (1920x1080)
        window.resize(1920, 1080)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(),
                         window.drawer.optimal_expanded_width)
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        # 3. Small / compressed resolution (950x600)
        window.resize(950, 600)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(),
                         window.drawer.min_expanded_width)
        self.assertTrue(hbar.isVisible())
        self.assertGreater(hbar.maximum(), 0)

        # 4. Resize back to default (1340x820)
        window.resize(1340, 820)
        QApplication.processEvents()
        self.assertEqual(window.drawer.width(),
                         window.drawer.optimal_expanded_width)
        self.assertFalse(hbar.isVisible())
        self.assertEqual(hbar.maximum(), 0)

        window.close()

    def test_drawer_category_order(self):
        """Verify Single-Species Population Growth is at the top of menu."""
        from PyQt6.QtWidgets import QLabel
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        drawer = window.drawer

        cat_labels = [
            lbl.text()
            for lbl in drawer.findChildren(QLabel)
            if lbl.objectName() == "DrawerCategory"
        ]

        self.assertGreaterEqual(len(cat_labels), 3)
        # First category must be Single-Species Population Growth
        self.assertEqual(cat_labels[0], "Single-Species Population Growth")
        self.assertEqual(cat_labels[1], "Competition & Interactions")
        self.assertEqual(cat_labels[2], "Consumer-Resource Models")

        # First model buttons under top category must be Exponential &
        # Logistic.
        first_model_names = [m.name for _, m, _ in drawer._buttons[:2]]
        self.assertEqual(
            first_model_names,
            ["Exponential Growth Model", "Logistic Growth Model"],
        )

        window.close()

    def test_drawer_topic_umbrella_expand_collapse(self):
        """Verify Ecology Models topic umbrella collapses & expands."""
        from PyQt6.QtWidgets import QPushButton
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        window.show()
        drawer = window.drawer

        # Verify both topic headers exist
        topic_btns = [
            btn for btn in drawer.findChildren(QPushButton)
            if btn.objectName() == "DrawerTopic"
        ]
        self.assertEqual(len(topic_btns), 2)
        eco_btn = topic_btns[0]
        self.assertIn("Ecology Models", eco_btn.text())
        evo_btn = topic_btns[1]
        self.assertIn("Evolution Models", evo_btn.text())

        # Initially, topic umbrellas are collapsed
        self.assertFalse(drawer.is_topic_expanded("Ecology Models"))
        container = drawer._topic_containers["Ecology Models"]
        self.assertFalse(container.isVisible())
        self.assertIn("▸", eco_btn.text())

        # Click on Ecology Models to expand and make models appear
        eco_btn.click()
        self.assertTrue(drawer.is_topic_expanded("Ecology Models"))
        self.assertTrue(container.isVisible())
        self.assertIn("▾", eco_btn.text())

        # Click Ecology Models again to collapse
        eco_btn.click()
        self.assertFalse(drawer.is_topic_expanded("Ecology Models"))
        self.assertFalse(container.isVisible())
        self.assertIn("▸", eco_btn.text())

        # Click on Evolution Models to expand
        self.assertFalse(drawer.is_topic_expanded("Evolution Models"))
        evo_container = drawer._topic_containers["Evolution Models"]
        self.assertFalse(evo_container.isVisible())
        self.assertIn("▸", evo_btn.text())

        evo_btn.click()
        self.assertTrue(drawer.is_topic_expanded("Evolution Models"))
        self.assertTrue(evo_container.isVisible())
        self.assertIn("▾", evo_btn.text())

        # Click Evolution Models again to collapse
        evo_btn.click()
        self.assertFalse(drawer.is_topic_expanded("Evolution Models"))
        self.assertFalse(evo_container.isVisible())
        self.assertIn("▸", evo_btn.text())

        window.close()

    def test_auto_load_scenario_preset_and_no_button(self):
        """Verify Load button is removed and combo auto-loads preset."""
        from PyQt6.QtWidgets import QPushButton
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        # 1. Verify "Load Selected Scenario" button does not exist
        load_buttons = [
            btn for btn in window.param_panel.findChildren(QPushButton)
            if "Load" in btn.text()
        ]
        self.assertEqual(len(load_buttons), 0)

        # 2. Select scenario at index 1 ("Competitive Exclusion")
        window.param_panel.preset_combo.setCurrentIndex(1)

        # Verify initial states and parameters updated automatically
        inputs = window.param_panel.get_simulation_inputs()
        self.assertEqual(inputs["initial_state"], (20, 25))
        self.assertEqual(inputs["params"]["r1"], 0.9)
        self.assertEqual(inputs["params"]["alpha21"], 1.2)

        # Verify simulation was triggered automatically
        res = window.canvas_widget._current_result
        self.assertIsNotNone(res)
        self.assertEqual(res.n1[0], 20.0)
        self.assertEqual(res.n2[0], 25.0)

        window.close()

    def test_mode_badge_toggle_interaction(self):
        """Verify clicking mode badge toggles continuous/discrete mode."""
        from PyQt6.QtWidgets import QPushButton
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        # 1. Verify drawer menu has no separate discrete button
        drawer_buttons = [
            btn.text() for btn, _, _ in window.drawer._buttons
        ]
        self.assertEqual(len(drawer_buttons), len(AVAILABLE_MODELS))
        for text in drawer_buttons:
            self.assertNotIn("Discrete Recursion", text)

        # 2. Check initial continuous mode badge
        badge = window.param_panel.mode_badge
        self.assertIsInstance(badge, QPushButton)
        self.assertEqual(badge.text(), "Continuous ODE")
        self.assertEqual(badge.property("mode"), "continuous")
        self.assertEqual(window.param_panel.mode, "continuous")
        self.assertEqual(
            window.param_panel.start_time_lbl.text(),
            "Start Time (t<sub>start</sub>):",
        )

        # 3. Click mode badge to toggle to discrete mode
        badge.click()
        self.assertEqual(window.param_panel.mode, "discrete")
        self.assertEqual(badge.text(), "Discrete Recursion")
        self.assertEqual(badge.property("mode"), "discrete")
        self.assertEqual(
            window.param_panel.start_time_lbl.text(),
            "Start Step (t<sub>start</sub>):",
        )
        self.assertEqual(
            window.param_panel.end_time_lbl.text(),
            "End Step (t<sub>end</sub>):",
        )

        # Verify simulation executed in discrete mode
        res_disc = window.canvas_widget._current_result
        self.assertIsNotNone(res_disc)
        self.assertEqual(res_disc.metadata.get("mode"), "discrete")

        # 4. Click mode badge again to toggle back to continuous mode
        badge.click()
        self.assertEqual(window.param_panel.mode, "continuous")
        self.assertEqual(badge.text(), "Continuous ODE")
        self.assertEqual(badge.property("mode"), "continuous")
        self.assertEqual(
            window.param_panel.start_time_lbl.text(),
            "Start Time (t<sub>start</sub>):",
        )
        self.assertEqual(
            window.param_panel.end_time_lbl.text(),
            "End Time (t<sub>end</sub>):",
        )

        res_cont = window.canvas_widget._current_result
        self.assertIsNotNone(res_cont)
        self.assertEqual(res_cont.metadata.get("mode"), "continuous")

        window.close()

    def test_all_models_support_discrete_step_and_toggle(self):
        """Verify that every biological model supports discrete recursion."""
        from PyQt6.QtWidgets import QApplication
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        for model in AVAILABLE_MODELS:
            # 1. Test model.discrete_step directly
            init_state = np.array([20.0, 15.0])
            params = model.default_params
            next_state = model.discrete_step(init_state, params)
            self.assertIsInstance(next_state, np.ndarray)
            self.assertEqual(len(next_state), 2)
            self.assertTrue(np.all(next_state >= 0))

            # 2. Test simulation in discrete mode
            res = simulate_model(
                model=model,
                initial_state=(20.0, 15.0),
                t_span=(0.0, 25.0),
                num_points=50,
                params=params,
                mode="discrete",
            )
            self.assertTrue(res.success)
            self.assertEqual(res.metadata.get("mode"), "discrete")
            self.assertEqual(len(res.t), 50)
            self.assertTrue(np.all(res.n1 >= 0))
            self.assertTrue(np.all(res.n2 >= 0))

            # 3. Test GUI toggle interaction for this model
            window._on_model_selected(model, "continuous")
            QApplication.processEvents()

            self.assertEqual(window.param_panel.mode, "continuous")
            self.assertEqual(
                window.param_panel.mode_badge.text(), "Continuous ODE"
            )

            # Click badge to toggle into discrete mode
            window.param_panel.mode_badge.click()
            QApplication.processEvents()

            self.assertEqual(window.param_panel.mode, "discrete")
            self.assertEqual(
                window.param_panel.mode_badge.text(), "Discrete Recursion"
            )
            gui_res = window.canvas_widget._current_result
            self.assertIsNotNone(gui_res)
            self.assertEqual(gui_res.metadata.get("mode"), "discrete")

        window.close()

    def test_modern_spinbox_and_combobox_styling(self):
        """Verify that spinboxes use modernized stepper buttons and icons."""
        from bio_models.ui.styles import (
            LIGHT_STYLESHEET,
            DARK_STYLESHEET,
            _UP_LIGHT,
            _DOWN_LIGHT,
            _UP_DARK,
            _DOWN_DARK,
        )

        # 1. Verify SVG icon files exist on disk
        for path in (_UP_LIGHT, _DOWN_LIGHT, _UP_DARK, _DOWN_DARK):
            self.assertTrue(os.path.isfile(path), f"Missing icon: {path}")
            self.assertGreater(os.path.getsize(path), 50)

        # 2. Verify stylesheets contain stepper subcontrol selectors
        for ss in (LIGHT_STYLESHEET, DARK_STYLESHEET):
            self.assertIn("QSpinBox::up-button", ss)
            self.assertIn("QSpinBox::down-button", ss)
            self.assertIn("QSpinBox::up-arrow", ss)
            self.assertIn("QSpinBox::down-arrow", ss)
            self.assertIn("QDoubleSpinBox::up-button", ss)
            self.assertIn("QDoubleSpinBox::down-button", ss)
            self.assertIn("QDoubleSpinBox::up-arrow", ss)
            self.assertIn("QDoubleSpinBox::down-arrow", ss)
            self.assertIn("QComboBox::down-arrow", ss)

        # 3. Test functional stepping on UI spinboxes
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        spin = window.param_panel.n1_init_spin
        initial_val = spin.value()
        spin.stepUp()
        self.assertEqual(spin.value(), initial_val + spin.singleStep())
        spin.stepDown()
        self.assertEqual(spin.value(), initial_val)
        window.close()

    def test_modern_action_buttons(self):
        """Verify Run Simulation and Save buttons have modern styling."""
        from PyQt6.QtCore import Qt
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        run_btn = window.param_panel.run_btn
        self.assertEqual(run_btn.text(), "Run Simulation")
        self.assertFalse(run_btn.icon().isNull())
        self.assertEqual(
            run_btn.cursor().shape(),
            Qt.CursorShape.PointingHandCursor,
        )

        export_btn = window.canvas_widget.export_btn
        self.assertEqual(export_btn.text(), "Save")
        self.assertNotIn("JPEG", export_btn.text())
        self.assertFalse(export_btn.icon().isNull())
        self.assertEqual(
            export_btn.cursor().shape(),
            Qt.CursorShape.PointingHandCursor,
        )

        # Test theme changes update icons
        window.apply_theme("light")
        self.assertFalse(run_btn.icon().isNull())
        self.assertFalse(export_btn.icon().isNull())

        window.apply_theme("dark")
        self.assertFalse(run_btn.icon().isNull())
        self.assertFalse(export_btn.icon().isNull())
        window.close()

    def test_gui_unified_save(self):
        """Verify unified GUI Save method for CSV and image exports."""
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        window.run_simulation()
        canvas = window.canvas_widget
        self.assertIsNotNone(canvas._current_result)

        # 1. Save to CSV directly via save(custom_path).
        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False
        ) as tmp:
            csv_path = tmp.name
        try:
            exported = canvas.save(custom_path=csv_path)
            self.assertEqual(exported, csv_path)
            self.assertTrue(os.path.exists(csv_path))
            self.assertGreater(os.path.getsize(csv_path), 50)
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

        # 2. Save to PNG via save(custom_path).
        with tempfile.NamedTemporaryFile(
            suffix=".png", delete=False
        ) as tmp:
            png_path = tmp.name
        try:
            exported = canvas.save(custom_path=png_path)
            self.assertEqual(exported, png_path)
            self.assertTrue(os.path.exists(png_path))
            self.assertGreater(os.path.getsize(png_path), 500)
        finally:
            if os.path.exists(png_path):
                os.remove(png_path)

        # 3. Save without extension using format_filter dispatch.
        base_tmp = os.path.join(
            tempfile.gettempdir(), "test_export_dispatch"
        )
        try:
            csv_disp = canvas.save(
                custom_path=base_tmp, format_filter="CSV Data (*.csv)"
            )
            self.assertTrue(csv_disp.endswith(".csv"))
            self.assertTrue(os.path.exists(csv_disp))
            if os.path.exists(csv_disp):
                os.remove(csv_disp)

            png_disp = canvas.save(
                custom_path=base_tmp, format_filter="PNG Image (*.png)"
            )
            self.assertTrue(png_disp.endswith(".png"))
            self.assertTrue(os.path.exists(png_disp))
            if os.path.exists(png_disp):
                os.remove(png_disp)
        finally:
            for ext in (".csv", ".png", ".jpeg"):
                p = base_tmp + ext
                if os.path.exists(p):
                    os.remove(p)

        window.close()

    def test_model_info_button(self):
        """Verify model info circle button displays equations & scenarios."""
        from bio_models.models import LotkaVolterraPredatorPreyModel
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        param_panel = window.param_panel
        info_btn = param_panel.info_btn

        self.assertIsNotNone(info_btn)
        self.assertFalse(info_btn.icon().isNull())

        # Continuous mode: must mention differential equations
        tooltip_cont = info_btn._info_html
        self.assertIn("Differential Equations", tooltip_cont)
        self.assertIn("dn₁/dt", tooltip_cont)
        self.assertIn("Biological Scenarios", tooltip_cont)

        # Toggle to discrete mode: must update to difference equations
        param_panel._toggle_mode()
        tooltip_disc = info_btn._info_html
        self.assertIn("Difference Equations", tooltip_disc)
        self.assertIn("n₁(t+1)", tooltip_disc)
        self.assertIn("Biological Scenarios", tooltip_disc)

        # Switch model: check updated info
        pred_model = LotkaVolterraPredatorPreyModel()
        param_panel.set_model(pred_model, mode="continuous")
        tooltip_pred = param_panel.info_btn._info_html
        self.assertIn("Classic Lotka-Volterra Predator-Prey", tooltip_pred)
        self.assertIn("Differential Equations", tooltip_pred)

        window.close()

    def test_single_variable_gui_controls_and_canvas(self):
        """Verify single-variable models in GUI: inputs, canvas, tooltips."""
        from PyQt6.QtWidgets import QApplication
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()

        for model_cls in (ExponentialGrowthModel, LogisticGrowthModel):
            model = model_cls()
            window._on_model_selected(model, "continuous")
            QApplication.processEvents()

            panel = window.param_panel
            self.assertIsNotNone(panel.n1_init_spin)
            # n2 spin must be None for single-species models
            self.assertIsNone(panel.n2_init_spin)

            # Continuous simulation check
            res_cont = window.canvas_widget._current_result
            self.assertIsNotNone(res_cont)
            self.assertTrue(res_cont.success)
            self.assertTrue(res_cont.metadata.get("is_single_variable"))

            # Toggle to discrete mode
            panel.mode_badge.click()
            QApplication.processEvents()
            self.assertEqual(panel.mode, "discrete")

            res_disc = window.canvas_widget._current_result
            self.assertIsNotNone(res_disc)
            self.assertTrue(res_disc.success)
            self.assertEqual(res_disc.metadata.get("mode"), "discrete")

            # Check model info tooltip contents
            info_html = panel.info_btn._info_html
            self.assertIn("Discrete Difference", info_html)
            self.assertIn("Biological Scenarios", info_html)

        window.close()

    def test_discrete_mode_controls_and_ladder_plot(self):
        """Verify discrete mode UI controls visibility and canvas steps."""
        from PyQt6.QtWidgets import QApplication
        from bio_models.ui.main_window import MainWindow

        window = MainWindow()
        window.show()
        QApplication.processEvents()
        panel = window.param_panel

        # Default model is Lotka-Volterra competition (continuous)
        self.assertEqual(panel.mode, "continuous")
        self.assertFalse(panel.points_lbl.isHidden())
        self.assertFalse(panel.points_spin.isHidden())
        self.assertEqual(panel.t_start_spin.decimals(), 2)
        self.assertEqual(panel.t_end_spin.decimals(), 2)

        # Toggle to discrete
        panel._toggle_mode()
        QApplication.processEvents()
        self.assertEqual(panel.mode, "discrete")
        self.assertTrue(panel.points_lbl.isHidden())
        self.assertTrue(panel.points_spin.isHidden())
        self.assertEqual(panel.t_start_spin.decimals(), 0)
        self.assertEqual(panel.t_end_spin.decimals(), 0)
        self.assertEqual(panel.t_start_spin.singleStep(), 1.0)
        self.assertEqual(panel.t_end_spin.singleStep(), 1.0)

        # Run simulation in discrete mode
        panel.t_start_spin.setValue(0.0)
        panel.t_end_spin.setValue(15.0)
        inputs = panel.get_simulation_inputs()
        self.assertEqual(inputs["num_points"], 16)

        window.run_simulation()
        res = window.canvas_widget._current_result
        self.assertEqual(len(res.t), 16)
        self.assertEqual(res.metadata["steps"], 15)

        # Switch to single variable exponential in discrete mode
        exp_model = ExponentialGrowthModel()
        window._on_model_selected(exp_model, "discrete")
        QApplication.processEvents()
        self.assertTrue(panel.points_lbl.isHidden())
        self.assertTrue(panel.points_spin.isHidden())

        panel.t_start_spin.setValue(0.0)
        panel.t_end_spin.setValue(15.0)
        panel.n1_init_spin.setValue(16)
        panel._param_inputs["r"].setValue(2.0)

        window.run_simulation()
        res_exp = window.canvas_widget._current_result
        self.assertEqual(len(res_exp.t), 16)
        self.assertAlmostEqual(res_exp.n1[0], 16.0)
        expected_final = 16.0 * (3.0 ** 15)
        self.assertAlmostEqual(res_exp.n1[-1], expected_final, delta=1.0)

        # Toggle back to continuous
        panel._toggle_mode()
        QApplication.processEvents()
        self.assertEqual(panel.mode, "continuous")
        self.assertFalse(panel.points_lbl.isHidden())
        self.assertFalse(panel.points_spin.isHidden())
        self.assertEqual(panel.t_start_spin.decimals(), 2)
        self.assertEqual(panel.t_end_spin.decimals(), 2)
        self.assertEqual(panel.t_end_spin.singleStep(), 5.0)

        window.close()

    def test_pep8_compliance(self):
        """Verify that all codebase files strictly adhere to PEP 8."""
        import subprocess

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        flake8_bin = os.path.join(root_dir, ".venv", "bin", "flake8")
        if not os.path.exists(flake8_bin):
            flake8_bin = "flake8"

        result = subprocess.run(
            [flake8_bin, "bio_models", "run_app.py", "tests"],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"PEP 8 violations found:\n{result.stdout}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
