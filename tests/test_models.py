"""
Unit tests for Biological Modelling engine, models, and export functionality.
"""

import os
import tempfile
import numpy as np
import pytest

from bio_models.engine import simulate_model
from bio_models.models import (
    ChemostatModel,
    ConsumerResourceModel,
    LotkaVolterraCompetitionModel,
    LotkaVolterraPredatorPreyModel,
    RosenzweigMacArthurModel,
    TypeIIIPredatorPreyModel,
)


def test_competition_continuous_simulation():
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
    """Verify models can start at arbitrary t_start != 0 and reach t_end."""
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
    """Verify engine enforces positive integers (>= 1) for individuals."""
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
    model = LotkaVolterraCompetitionModel()
    assert "Mutualistic" in model.classify_relationship(-0.5, -0.4)
    assert "Competitive" in model.classify_relationship(0.5, 0.4)
    assert "Parasitic" in model.classify_relationship(0.5, -0.4)
    assert "Parasitic" in model.classify_relationship(-0.5, 0.4)
    assert "Commensal" in model.classify_relationship(-0.5, 0.0)
    assert "Amensal" in model.classify_relationship(0.5, 0.0)


def test_classic_predator_prey_oscillations():
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


def test_chemostat_model_eq_317():
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
    model = LotkaVolterraCompetitionModel()
    nullclines = model.get_nullclines(
        model.default_params, (0.0, 150.0), (0.0, 150.0)
    )
    assert len(nullclines) > 0


def test_jpeg_export():
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


if __name__ == "__main__":
    pytest.main(["-v", __file__])
