"""Unit tests for engine, models, and export functionality."""

import os
import tempfile
import numpy as np
try:
    import pytest
except ImportError:
    pytest = None

from bio_models.engine import simulate_model
from bio_models.models import (
    ChemostatModel,
    ConsumerResourceModel,
    DiploidSelectionModel,
    HaploidSelectionModel,
    LotkaVolterraCompetitionModel,
    LotkaVolterraPredatorPreyModel,
    RosenzweigMacArthurModel,
    TypeIIIPredatorPreyModel,
)


def test_competition_continuous_simulation():
    """Verify continuous ODE simulation for competition model."""
    model = LotkaVolterraCompetitionModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(20.0, 15.0),
        t_span=(0.0, 30.0),
        num_points=100,
        params=params,
    )

    assert res.success is True
    assert len(res.t) == 100
    assert len(res.n1) == 100
    assert len(res.n2) == 100
    assert np.all(res.n1 >= 0)
    assert np.all(res.n2 >= 0)
    # Check that both populations reach coexistence
    assert res.n1[-1] > 0
    assert res.n2[-1] > 0


def test_arbitrary_initial_and_end_time():
    """Verify models start at arbitrary t_start != 0 and reach t_end."""
    model = LotkaVolterraCompetitionModel()
    params = model.default_params

    # Positive non-zero start time
    res = simulate_model(
        model,
        initial_state=(20.0, 15.0),
        t_span=(15.0, 75.0),
        num_points=100,
        params=params,
    )
    assert res.success is True
    assert np.isclose(res.t[0], 15.0)
    assert np.isclose(res.t[-1], 75.0)
    assert len(res.t) == 100

    # Negative start time
    res_neg = simulate_model(
        model,
        initial_state=(20.0, 15.0),
        t_span=(-10.0, 30.0),
        num_points=100,
        params=params,
    )
    assert res_neg.success is True
    assert np.isclose(res_neg.t[0], -10.0)
    assert np.isclose(res_neg.t[-1], 30.0)

    # Discrete recurrence
    res_disc = simulate_model(
        model,
        initial_state=(20.0, 15.0),
        t_span=(10.0, 50.0),
        num_points=40,
        params=params,
        mode="discrete",
    )
    assert res_disc.success is True
    assert np.isclose(res_disc.t[0], 10.0)
    assert np.isclose(res_disc.t[-1], 50.0)


def test_positive_integer_initial_conditions():
    """Verify engine enforces positive integers (>= 1) for counts."""
    model = LotkaVolterraCompetitionModel()
    params = model.default_params

    res = simulate_model(
        model,
        initial_state=(25.7, -4.0),
        t_span=(0.0, 20.0),
        num_points=50,
        params=params,
    )
    assert res.success is True
    assert res.n1[0] == 26.0
    assert res.n2[0] == 1.0


def test_competition_discrete_recursion():
    """Verify discrete recursion step for competition model."""
    model = LotkaVolterraCompetitionModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(20.0, 15.0),
        num_points=50,
        params=params,
        mode="discrete",
    )

    assert res.success is True
    assert len(res.t) == 50
    assert res.metadata["mode"] == "discrete"
    assert np.all(res.n1 >= 0)
    assert np.all(res.n2 >= 0)


def test_competition_relationship_classification():
    """Verify ecological relationship classification logic."""
    model = LotkaVolterraCompetitionModel()
    assert "Mutualistic" in model.classify_relationship(-0.5, -0.4)
    assert "Competitive" in model.classify_relationship(0.5, 0.4)
    assert "Parasitic" in model.classify_relationship(0.5, -0.4)
    assert "Parasitic" in model.classify_relationship(-0.5, 0.4)
    assert "Commensal" in model.classify_relationship(-0.5, 0.0)
    assert "Amensal" in model.classify_relationship(0.5, 0.0)


def test_classic_predator_prey_oscillations():
    """Verify limit cycle oscillations in Lotka-Volterra."""
    model = LotkaVolterraPredatorPreyModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(30.0, 10.0),
        t_span=(0.0, 40.0),
        num_points=200,
        params=params,
    )

    assert res.success is True
    assert np.all(res.n1 >= 0)
    assert np.all(res.n2 >= 0)
    # Predator-prey cycles should oscillate (std > 0)
    assert np.std(res.n1) > 2.0
    assert np.std(res.n2) > 2.0


def test_chemostat_model():
    """Verify chemostat nutrient-consumer dynamics."""
    model = ChemostatModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(20.0, 5.0),
        t_span=(0.0, 50.0),
        num_points=100,
        params=params,
    )

    assert res.success is True
    assert res.n1[-1] > 0
    assert res.n2[-1] > 0


def test_rosenzweig_macarthur_limit_cycle():
    """Verify limit cycles in Rosenzweig-MacArthur model."""
    model = RosenzweigMacArthurModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(40.0, 15.0),
        t_span=(0.0, 80.0),
        num_points=250,
        params=params,
    )

    assert res.success is True
    # Verify limit cycle oscillations occur
    assert np.max(res.n1) > np.min(res.n1) * 1.5


def test_type_iii_model():
    """Verify Type III sigmoidal predator-prey dynamics."""
    model = TypeIIIPredatorPreyModel()
    params = model.default_params
    res = simulate_model(
        model,
        initial_state=(30.0, 10.0),
        t_span=(0.0, 50.0),
        num_points=100,
        params=params,
    )

    assert res.success is True
    assert np.all(res.n1 >= 0)
    assert np.all(res.n2 >= 0)


def test_modular_consumer_resource_combinations():
    """Verify all combinations of modular consumer-resource."""
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
    h_types = ["linear_death", "density_dependent_death"]

    # Test representative combinations across all functional forms
    for f in f_types:
        for g in g_types:
            for h in h_types:
                model = ConsumerResourceModel(
                    f_type=f, g_type=g, h_type=h
                )
                params = model.default_params
                res = simulate_model(
                    model,
                    initial_state=(25.0, 10.0),
                    t_span=(0.0, 15.0),
                    num_points=50,
                    params=params,
                )
                assert res.success is True, f"Failed for f={f}, g={g}, h={h}"


def test_nullclines_generation():
    """Verify nullcline generation for phase plane."""
    model = LotkaVolterraCompetitionModel()
    nullclines = model.get_nullclines(
        model.default_params, (0.0, 150.0), (0.0, 150.0)
    )
    assert len(nullclines) > 0


def test_jpeg_export():
    """Verify headless JPEG plot image export."""
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
        assert os.path.exists(tmp_path)
        assert os.path.getsize(tmp_path) > 1000  # Non-trivial JPEG file
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_haploid_selection_model():
    """Verify Haploid Selection dynamics in continuous and discrete."""
    model = HaploidSelectionModel()
    assert model.topic == "Evolution Models"
    assert model.category == "Natural Selection Models"
    assert model.is_frequency_model is True

    # Continuous directional selection
    res_cont = simulate_model(
        model=model,
        initial_state=(0.05, 0.95),
        t_span=(0.0, 30.0),
        num_points=150,
        params={"W_A": 1.25, "W_a": 1.00},
        mode="continuous",
    )
    assert res_cont.success is True
    assert res_cont.n1[-1] > res_cont.n1[0]
    assert np.allclose(res_cont.n1 + res_cont.n2, 1.0)

    # Discrete recursion
    res_disc = simulate_model(
        model=model,
        initial_state=(0.20, 0.80),
        t_span=(0.0, 5.0),
        params={"W_A": 1.50, "W_a": 1.00},
        mode="discrete",
    )
    assert res_disc.success is True
    expected_p1 = (1.50 * 0.20) / (1.50 * 0.20 + 1.00 * 0.80)
    assert np.isclose(res_disc.n1[1], expected_p1, atol=1e-4)


def test_diploid_selection_model():
    """Verify Diploid Selection dynamics and overdominance."""
    model = DiploidSelectionModel()
    assert model.topic == "Evolution Models"
    assert model.category == "Natural Selection Models"
    assert model.is_frequency_model is True

    # Overdominance (heterozygote advantage) polymorphism: p* = 2/3
    res_poly = simulate_model(
        model=model,
        initial_state=(0.10, 0.90),
        t_span=(0.0, 50.0),
        num_points=200,
        params={"W_AA": 0.90, "W_Aa": 1.20, "W_aa": 0.60},
        mode="continuous",
    )
    assert res_poly.success is True
    assert np.isclose(res_poly.n1[-1], 2.0 / 3.0, atol=0.03)


if __name__ == "__main__":
    if pytest is not None:
        pytest.main(["-v", __file__])
    else:
        # Run test functions directly if pytest is unavailable
        for test_name, test_func in list(globals().items()):
            if test_name.startswith("test_") and callable(test_func):
                test_func()
                print(f"{test_name}: ok")
