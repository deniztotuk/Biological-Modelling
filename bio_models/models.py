"""
Mathematical Models for Species Interactions and Consumer-Resource Systems.
Continuous ODE systems and discrete-time recursions.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple, Optional, List
import numpy as np


@dataclass
class SimulationResult:
    """Stores the output of a biological simulation run."""
    t: np.ndarray
    n1: np.ndarray
    n2: np.ndarray
    model_name: str
    n1_label: str
    n2_label: str
    parameters: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    message: str = "Simulation completed successfully"


class BiologicalModel(ABC):
    """Abstract base class for two-variable biological interaction models."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the model."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Category for sandwich menu organization."""
        pass

    @property
    @abstractmethod
    def n1_label(self) -> str:
        """Label for species/variable 1 (e.g. Prey, Resource, Species 1)."""
        pass

    @property
    @abstractmethod
    def n2_label(self) -> str:
        """Label for species/variable 2 (e.g. Predator, Species 2)."""
        pass

    @property
    def num_variables(self) -> int:
        """Number of state variables in the system (1 or 2). Defaults to 2."""
        return 2

    @property
    def is_single_variable(self) -> bool:
        """Return True if model describes a single-species system."""
        return self.num_variables == 1

    @property
    @abstractmethod
    def default_params(self) -> Dict[str, float]:
        """Default parameter values."""
        pass

    @property
    @abstractmethod
    def param_meta(self) -> Dict[str, Dict[str, Any]]:
        """Metadata for UI generation: label, min, max, step, description."""
        pass

    @abstractmethod
    def rhs(
        self, t: float, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Right-hand side of continuous-time ODE: d[n1, n2]/dt."""
        pass

    def discrete_step(
        self, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Discrete-time recursion step: [n1(t+1), n2(t+1)]."""
        raise NotImplementedError(
            "Discrete mode not implemented for this model.")

    def get_nullclines(
        self,
        params: Dict[str, float],
        n1_range: Tuple[float, float],
        n2_range: Tuple[float, float],
    ) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """Return coordinates for nullclines (dn1/dt = 0 and dn2/dt = 0)."""
        return {}


# -------------------------------------------------------------------------
# 1. Lotka-Volterra Model of Competition & Multi-Species Interactions
# -------------------------------------------------------------------------
class LotkaVolterraCompetitionModel(BiologicalModel):
    """
    Two-species competition and multi-species interaction model.
    dn1/dt = r1 * n1 * (1 - (n1 + alpha12 * n2) / K1)
    dn2/dt = r2 * n2 * (1 - (n2 + alpha21 * n1) / K2)
    """

    @property
    def name(self) -> str:
        return "Lotka-Volterra Competition & Species Interactions"

    @property
    def category(self) -> str:
        return "Competition & Interactions"

    @property
    def n1_label(self) -> str:
        return "Species 1 (n₁)"

    @property
    def n2_label(self) -> str:
        return "Species 2 (n₂)"

    @property
    def default_params(self) -> Dict[str, float]:
        return {
            "r1": 0.8,
            "r2": 0.6,
            "K1": 100.0,
            "K2": 100.0,
            "alpha12": 0.5,
            "alpha21": 0.5,
        }

    @property
    def param_meta(self) -> Dict[str, Dict[str, Any]]:
        return {
            "r1": {
                "label": "Growth rate sp. 1 (r₁):",
                "min": -2.0,
                "max": 5.0,
                "step": 0.05,
                "description": "Intrinsic per capita growth rate of species 1",
            },
            "r2": {
                "label": "Growth rate sp. 2 (r₂):",
                "min": -2.0,
                "max": 5.0,
                "step": 0.05,
                "description": "Intrinsic per capita growth rate of species 2",
            },
            "K1": {
                "label": "Carrying cap. sp. 1 (K₁):",
                "min": 1,
                "max": 10000,
                "step": 1,
                "is_int": True,
                "description": (
                    "Carrying capacity of species 1 "
                    "(maximum sustainable individuals)"
                ),
            },
            "K2": {
                "label": "Carrying cap. sp. 2 (K₂):",
                "min": 1,
                "max": 10000,
                "step": 1,
                "is_int": True,
                "description": (
                    "Carrying capacity of species 2 "
                    "(maximum sustainable individuals)"
                ),
            },
            "alpha12": {
                "label": "Effect of sp. 2 on 1 (α₁₂):",
                "min": -2.0,
                "max": 3.0,
                "step": 0.05,
                "description": (
                    "Competition/interaction coefficient on species 1"
                ),
            },
            "alpha21": {
                "label": "Effect of sp. 1 on 2 (α₂₁):",
                "min": -2.0,
                "max": 3.0,
                "step": 0.05,
                "description": (
                    "Competition/interaction coefficient on species 2"
                ),
            },
        }

    def classify_relationship(self, a12: float, a21: float) -> str:
        """
        Classifies interaction type based on pair interaction coefficients:
        - Mutualistic: a12 < 0, a21 < 0
        - Commensal: (a12 < 0, a21 == 0) or (a12 == 0, a21 < 0)
        - Parasitic / Exploitative: (a12 > 0, a21 < 0) or (a12 < 0, a21 > 0)
        - Competitive: a12 > 0, a21 > 0
        - Neutral: a12 == 0, a21 == 0
        """
        eps = 1e-6
        if a12 < -eps and a21 < -eps:
            return "Mutualistic (- / -)"
        elif a12 > eps and a21 > eps:
            return "Competitive (+ / +)"
        elif (a12 > eps and a21 < -eps) or (a12 < -eps and a21 > eps):
            return "Parasitic / Exploitative (+ / -)"
        elif (
            (a12 < -eps and abs(a21) <= eps)
            or (abs(a12) <= eps and a21 < -eps)
        ):
            return "Commensal (+ / 0)"
        elif (
            (a12 > eps and abs(a21) <= eps)
            or (abs(a12) <= eps and a21 > eps)
        ):
            return "Amensal (- / 0)"
        else:
            return "Neutral (0 / 0)"

    def rhs(
        self, t: float, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        n1 = max(0.0, float(state[0]))
        n2 = max(0.0, float(state[1]))
        r1, r2 = params["r1"], params["r2"]
        K1, K2 = max(1e-6, params["K1"]), max(1e-6, params["K2"])
        a12, a21 = params["alpha12"], params["alpha21"]

        dn1_dt = r1 * n1 * (1.0 - (n1 + a12 * n2) / K1)
        dn2_dt = r2 * n2 * (1.0 - (n2 + a21 * n1) / K2)
        return np.array([dn1_dt, dn2_dt], dtype=float)

    def discrete_step(
        self, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Discrete recursion step for multi-species interaction."""
        n1 = max(0.0, float(state[0]))
        n2 = max(0.0, float(state[1]))
        r1, r2 = params["r1"], params["r2"]
        K1, K2 = max(1e-6, params["K1"]), max(1e-6, params["K2"])
        a12, a21 = params["alpha12"], params["alpha21"]

        n1_next = n1 + r1 * n1 * (1.0 - (n1 + a12 * n2) / K1)
        n2_next = n2 + r2 * n2 * (1.0 - (n2 + a21 * n1) / K2)
        return np.array([max(0.0, n1_next), max(0.0, n2_next)], dtype=float)

    def get_nullclines(
        self,
        params: Dict[str, float],
        n1_range: Tuple[float, float],
        n2_range: Tuple[float, float],
    ) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """Calculate n1 and n2 non-trivial zero-growth isoclines."""
        K1, K2 = params["K1"], params["K2"]
        a12, a21 = params["alpha12"], params["alpha21"]
        nullclines = {}

        # Isocline 1: n1 + a12 * n2 = K1 => n2 = (K1 - n1) / a12
        if abs(a12) > 1e-5:
            n1_pts = np.linspace(0, max(K1 * 1.5, n1_range[1]), 100)
            n2_pts = (K1 - n1_pts) / a12
            valid = (n2_pts >= 0) & (n2_pts <= max(K2 * 2.0, n2_range[1]))
            if np.any(valid):
                nullclines["dn₁/dt = 0 isocline"] = (
                    n1_pts[valid], n2_pts[valid])
        else:
            # Vertical line at n1 = K1
            nullclines["dn₁/dt = 0 isocline"] = (
                np.array([K1, K1]), np.array([0, n2_range[1]]))

        # Isocline 2: n2 + a21 * n1 = K2 => n2 = K2 - a21 * n1
        n1_pts = np.linspace(0, max(K1 * 1.5, n1_range[1]), 100)
        n2_pts = K2 - a21 * n1_pts
        valid = (n2_pts >= 0) & (n2_pts <= max(K2 * 2.0, n2_range[1]))
        if np.any(valid):
            nullclines["dn₂/dt = 0 isocline"] = (n1_pts[valid], n2_pts[valid])

        return nullclines


# -------------------------------------------------------------------------
# 2. General Consumer-Resource Model
# -------------------------------------------------------------------------
class ConsumerResourceModel(BiologicalModel):
    """
    General Consumer-Resource Model:
    dn1/dt = f(n1) - g(n1, n2)
    dn2/dt = epsilon * g(n1, n2) - h(n2)
    """

    def __init__(
        self,
        name: str = "Modular Consumer-Resource Model",
        category: str = "Consumer-Resource Models",
        f_type: str = "logistic",
        g_type: str = "type_1_linear",
        h_type: str = "linear_death",
        custom_params: Optional[Dict[str, float]] = None,
    ):
        self._name = name
        self._category = category
        self.f_type = f_type
        self.g_type = g_type
        self.h_type = h_type
        self._custom_params = custom_params or {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def n1_label(self) -> str:
        return "Resource / Prey (n₁)"

    @property
    def n2_label(self) -> str:
        return "Consumer / Predator (n₂)"

    @property
    def default_params(self) -> Dict[str, float]:
        defaults = {
            "theta": 15.0,        # Constant inflow
            "psi": 2.0,           # Constant outflow
            "r": 1.0,             # Resource growth rate
            "K": 100.0,           # Resource carrying capacity
            "a_f": 0.02,          # Exp decline parameter in f(n1)
            "a": 0.1,             # Attack/usage probability
            "c": 0.1,             # Contact rate
            "b": 20.0,            # Half-saturation constant
            "k": 2.0,             # Type III exponent
            "epsilon": 0.5,       # Conversion efficiency
            "delta": 0.2,         # Consumer death rate
            "gamma": 0.005,       # Density-dependent death rate
        }
        defaults.update(self._custom_params)
        return defaults

    @property
    def param_meta(self) -> Dict[str, Dict[str, Any]]:
        return {
            "theta": {
                "label": "Constant Inflow (θ):",
                "min": 0.0,
                "max": 100.0,
                "step": 1.0,
                "description": "Constant resource immigration/inflow rate",
            },
            "psi": {
                "label": "Constant Outflow (ψ):",
                "min": 0.0,
                "max": 50.0,
                "step": 0.5,
                "description": "Constant resource outflow rate",
            },
            "r": {
                "label": "Resource growth rate (r):",
                "min": 0.01,
                "max": 5.0,
                "step": 0.05,
                "description": "Intrinsic per capita growth rate of resource",
            },
            "K": {
                "label": "Carrying capacity (K):",
                "min": 1,
                "max": 10000,
                "step": 1,
                "is_int": True,
                "description": (
                    "Environmental carrying capacity for resource "
                    "(maximum sustainable individuals)"
                ),
            },
            "a_f": {
                "label": "Exp decay coeff (a<sub>f</sub>):",
                "min": 0.001,
                "max": 0.5,
                "step": 0.005,
                "description": "Prey exponential decline factor",
            },
            "a": {
                "label": "Attack / success prob (a):",
                "min": 0.001,
                "max": 1.0,
                "step": 0.01,
                "description": (
                    "Probability of successful consumption per contact"
                ),
            },
            "c": {
                "label": "Contact rate (c):",
                "min": 0.001,
                "max": 2.0,
                "step": 0.01,
                "description": (
                    "Rate of contact between consumers and resources"
                ),
            },
            "b": {
                "label": "Half-saturation const (b):",
                "min": 1.0,
                "max": 200.0,
                "step": 1.0,
                "description": "Resource density at half-maximum consumption",
            },
            "k": {
                "label": "Type III exponent (k):",
                "min": 1.0,
                "max": 5.0,
                "step": 0.1,
                "description": (
                    "Hill exponent for sigmoidal functional response"
                ),
            },
            "epsilon": {
                "label": "Conversion efficiency (ε):",
                "min": 0.01,
                "max": 1.0,
                "step": 0.02,
                "description": (
                    "Biomass conversion efficiency of consumed "
                    "prey into predators"
                ),
            },
            "delta": {
                "label": "Consumer death rate (δ):",
                "min": 0.01,
                "max": 2.0,
                "step": 0.01,
                "description": (
                    "Per capita mortality rate of consumer in absence "
                    "of resource"
                ),
            },
            "gamma": {
                "label": "Density dep. mortality (γ):",
                "min": 0.0,
                "max": 0.1,
                "step": 0.001,
                "description": (
                    "Intraspecific competition / density-dependent "
                    "consumer death"
                ),
            },
        }

    def calc_f(self, n1: float, params: Dict[str, float]) -> float:
        """Resource renewal function f(n1)."""
        if self.f_type == "constant_inflow":
            return float(params.get("theta", 10.0))
        elif self.f_type == "constant_outflow":
            return -float(params.get("psi", 2.0))
        elif self.f_type == "exponential":
            return float(params.get("r", 1.0) * n1)
        elif self.f_type == "logistic":
            r = params.get("r", 1.0)
            K = max(1e-6, params.get("K", 100.0))
            return float(r * n1 * (1.0 - n1 / K))
        elif self.f_type == "exponential_decline":
            r = params.get("r", 1.0)
            a_f = params.get("a_f", 0.02)
            return float(r * n1 * np.exp(-a_f * n1))
        else:
            return 0.0

    def calc_g(self, n1: float, n2: float, params: Dict[str, float]) -> float:
        """Resource consumption rate g(n1, n2)."""
        a = params.get("a", 0.1)
        c = params.get("c", 0.1)
        ac = a * c

        if self.g_type == "type_1_linear":
            return float(ac * n1 * n2)
        elif self.g_type == "type_2_saturating":
            b = max(1e-6, params.get("b", 20.0))
            return float((ac * n1 / (b + n1)) * n2)
        elif self.g_type == "type_3_generalized":
            b = max(1e-6, params.get("b", 20.0))
            k = max(1.0, params.get("k", 2.0))
            n1_k = np.power(max(0.0, n1), k)
            denom = b + n1_k
            if denom <= 1e-9:
                return 0.0
            return float((ac * n1_k / denom) * n2)
        else:
            return float(ac * n1 * n2)

    def calc_h(self, n2: float, params: Dict[str, float]) -> float:
        """Consumer loss rate h(n2)."""
        delta = params.get("delta", 0.2)
        if self.h_type == "linear_death":
            return float(delta * n2)
        elif self.h_type == "density_dependent_death":
            gamma = params.get("gamma", 0.005)
            return float((delta + gamma * n2) * n2)
        else:
            return float(delta * n2)

    def rhs(
        self, t: float, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        n1 = max(0.0, float(state[0]))
        n2 = max(0.0, float(state[1]))
        eps = params.get("epsilon", 0.5)

        fn1 = self.calc_f(n1, params)
        gn12 = self.calc_g(n1, n2, params)
        hn2 = self.calc_h(n2, params)

        dn1_dt = fn1 - gn12
        dn2_dt = eps * gn12 - hn2
        return np.array([dn1_dt, dn2_dt], dtype=float)

    def discrete_step(
        self, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Discrete recursion step for consumer-resource dynamics."""
        n1 = max(0.0, float(state[0]))
        n2 = max(0.0, float(state[1]))
        eps = params.get("epsilon", 0.5)

        fn1 = self.calc_f(n1, params)
        gn12 = self.calc_g(n1, n2, params)
        hn2 = self.calc_h(n2, params)

        n1_next = n1 + fn1 - gn12
        n2_next = n2 + eps * gn12 - hn2
        return np.array([max(0.0, n1_next), max(0.0, n2_next)], dtype=float)

    def get_nullclines(
        self,
        params: Dict[str, float],
        n1_range: Tuple[float, float],
        n2_range: Tuple[float, float],
    ) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        nullclines = {}
        eps = params.get("epsilon", 0.5)
        n1_pts = np.linspace(
            max(0.1, n1_range[0]), max(100.0, n1_range[1]), 200)

        # Consumer nullcline: dn2/dt = 0 => eps * g(n1, n2) = h(n2)
        # For linear death h(n2) = delta * n2:
        # Type I: eps * ac * n1 * n2 = delta * n2 =>
        # n1* = delta / (eps * ac) (vertical line)
        # Type II: eps * (ac * n1 / (b + n1)) * n2 = delta * n2 =>
        # n1* = (b * delta) / (eps * ac - delta)
        a = params.get("a", 0.1)
        c = params.get("c", 0.1)
        ac = a * c
        delta = params.get("delta", 0.2)

        if self.h_type == "linear_death":
            if self.g_type == "type_1_linear" and (eps * ac) > 1e-7:
                n1_star = delta / (eps * ac)
                if 0 <= n1_star <= n1_range[1] * 2:
                    nullclines["dn₂/dt = 0 isocline"] = (
                        np.array([n1_star, n1_star]),
                        np.array([0, n2_range[1] * 1.5]),
                    )
            elif self.g_type == "type_2_saturating":
                b = params.get("b", 20.0)
                denom = eps * ac - delta
                if denom > 1e-7:
                    n1_star = (b * delta) / denom
                    if 0 <= n1_star <= n1_range[1] * 2:
                        nullclines["dn₂/dt = 0 isocline"] = (
                            np.array([n1_star, n1_star]),
                            np.array([0, n2_range[1] * 1.5]),
                        )

        # Resource nullcline: dn1/dt = 0 => f(n1) = g(n1, n2) =>
        # n2 = f(n1) / (consumption_rate_per_consumer)
        n2_vals = []
        valid_n1 = []
        for val in n1_pts:
            fn = self.calc_f(val, params)
            if self.g_type == "type_1_linear":
                per_consumer_g = ac * val
            elif self.g_type == "type_2_saturating":
                b = params.get("b", 20.0)
                per_consumer_g = (ac * val) / (b + val)
            elif self.g_type == "type_3_generalized":
                b = params.get("b", 20.0)
                k = params.get("k", 2.0)
                val_k = np.power(val, k)
                per_consumer_g = (ac * val_k) / (b + val_k)
            else:
                per_consumer_g = ac * val

            if per_consumer_g > 1e-9:
                n2_val = fn / per_consumer_g
                if 0 <= n2_val <= max(200.0, n2_range[1] * 2.0):
                    valid_n1.append(val)
                    n2_vals.append(n2_val)

        if valid_n1:
            nullclines["dn₁/dt = 0 isocline"] = (
                np.array(valid_n1), np.array(n2_vals))

        return nullclines


# -------------------------------------------------------------------------
# Specialized Classic Consumer-Resource Subclasses
# -------------------------------------------------------------------------
class ChemostatModel(ConsumerResourceModel):
    """
    Nutrient Inflow / Chemostat Model.
    dn1/dt = theta - a * c * n1 * n2
    dn2/dt = epsilon * a * c * n1 * n2 - delta * n2
    """

    def __init__(self):
        super().__init__(
            name="Nutrient Inflow / Chemostat Model",
            category="Consumer-Resource Models",
            f_type="constant_inflow",
            g_type="type_1_linear",
            h_type="linear_death",
            custom_params={
                "theta": 20.0,
                "a": 0.05,
                "c": 0.1,
                "epsilon": 0.6,
                "delta": 0.25,
            },
        )

    @property
    def n1_label(self) -> str:
        return "Nutrient / Resource Level (n₁)"

    @property
    def n2_label(self) -> str:
        return "Consumer / Algae Population (n₂)"


class LotkaVolterraPredatorPreyModel(ConsumerResourceModel):
    """
    Classic Lotka-Volterra Predator-Prey Model.
    dn1/dt = r * n1 - a * c * n1 * n2
    dn2/dt = epsilon * a * c * n1 * n2 - delta * n2
    """

    def __init__(self):
        super().__init__(
            name="Classic Lotka-Volterra Predator-Prey",
            category="Consumer-Resource Models",
            f_type="exponential",
            g_type="type_1_linear",
            h_type="linear_death",
            custom_params={
                "r": 0.8,
                "a": 0.02,
                "c": 0.5,
                "epsilon": 0.5,
                "delta": 0.2,
            },
        )

    @property
    def n1_label(self) -> str:
        return "Prey Population (n₁)"

    @property
    def n2_label(self) -> str:
        return "Predator Population (n₂)"


class RosenzweigMacArthurModel(ConsumerResourceModel):
    """
    Logistic prey growth with Holling Type II saturating functional response.
    Classic demonstration of the Paradox of Enrichment and stable limit cycles.
    """

    def __init__(self):
        super().__init__(
            name="Rosenzweig-MacArthur (Type II Limit Cycles)",
            category="Consumer-Resource Models",
            f_type="logistic",
            g_type="type_2_saturating",
            h_type="linear_death",
            custom_params={
                "r": 1.0,
                "K": 120.0,
                "a": 0.8,
                "c": 1.0,
                "b": 30.0,
                "epsilon": 0.4,
                "delta": 0.2,
            },
        )

    @property
    def n1_label(self) -> str:
        return "Prey Population (n₁)"

    @property
    def n2_label(self) -> str:
        return "Predator Population (n₂)"


class TypeIIIPredatorPreyModel(ConsumerResourceModel):
    """
    Logistic prey growth with Holling Type III sigmoid functional response.
    Models prey switching and refuges at low prey densities.
    """

    def __init__(self):
        super().__init__(
            name="Generalized Type III Predator-Prey (Sigmoidal)",
            category="Consumer-Resource Models",
            f_type="logistic",
            g_type="type_3_generalized",
            h_type="linear_death",
            custom_params={
                "r": 1.0,
                "K": 100.0,
                "a": 0.5,
                "c": 1.0,
                "b": 400.0,
                "k": 2.0,
                "epsilon": 0.5,
                "delta": 0.2,
            },
        )

    @property
    def n1_label(self) -> str:
        return "Prey Population (n₁)"

    @property
    def n2_label(self) -> str:
        return "Predator Population (n₂)"


# -------------------------------------------------------------------------
# Single-Species Population Growth Models (Otto & Day 2007, Chapter 3)
# -------------------------------------------------------------------------
class ExponentialGrowthModel(BiologicalModel):
    """
    Classic exponential population growth model (Otto & Day 2007, Sec. 3.2.1).
    Continuous differential equation:
        dn/dt = r * n
    Discrete recursion equation:
        n(t+1) = (1 + r) * n(t) = R * n(t)
    """

    @property
    def name(self) -> str:
        return "Exponential Growth Model"

    @property
    def category(self) -> str:
        return "Single-Species Population Growth"

    @property
    def num_variables(self) -> int:
        return 1

    @property
    def n1_label(self) -> str:
        return "Population Density (n)"

    @property
    def n2_label(self) -> str:
        return ""

    @property
    def default_params(self) -> Dict[str, float]:
        return {"r": 0.5}

    @property
    def param_meta(self) -> Dict[str, Dict[str, Any]]:
        return {
            "r": {
                "label": "Growth rate (r):",
                "min": -2.0,
                "max": 5.0,
                "step": 0.05,
                "description": (
                    "Intrinsic per capita growth rate (r = b - d)"
                ),
            },
        }

    def rhs(
        self, t: float, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Continuous differential equation: dn/dt = r * n."""
        n = max(0.0, float(state[0]))
        r = params.get("r", 0.5)
        dn_dt = r * n
        if len(state) > 1:
            return np.array([dn_dt, 0.0], dtype=float)
        return np.array([dn_dt], dtype=float)

    def discrete_step(
        self, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Discrete recursion: n(t+1) = (1 + r) * n(t) = R * n(t)."""
        n = max(0.0, float(state[0]))
        r = params.get("r", 0.5)
        n_next = max(0.0, (1.0 + r) * n)
        if len(state) > 1:
            return np.array([n_next, 0.0], dtype=float)
        return np.array([n_next], dtype=float)


class LogisticGrowthModel(BiologicalModel):
    """
    Classic logistic population growth model (Otto & Day 2007, Sec. 3.2.2).
    Continuous differential equation:
        dn/dt = r * n * (1 - n / K)
    Discrete recursion equation:
        n(t+1) = n(t) + r * n(t) * (1 - n(t) / K)
    """

    @property
    def name(self) -> str:
        return "Logistic Growth Model"

    @property
    def category(self) -> str:
        return "Single-Species Population Growth"

    @property
    def num_variables(self) -> int:
        return 1

    @property
    def n1_label(self) -> str:
        return "Population Density (n)"

    @property
    def n2_label(self) -> str:
        return ""

    @property
    def default_params(self) -> Dict[str, float]:
        return {
            "r": 0.6,
            "K": 100.0,
        }

    @property
    def param_meta(self) -> Dict[str, Dict[str, Any]]:
        return {
            "r": {
                "label": "Growth rate (r):",
                "min": -2.0,
                "max": 5.0,
                "step": 0.05,
                "description": (
                    "Intrinsic per capita growth rate when "
                    "density is near zero"
                ),
            },
            "K": {
                "label": "Carrying cap. (K):",
                "min": 1,
                "max": 100000,
                "step": 10,
                "is_int": True,
                "description": (
                    "Maximum population size sustainable by resources"
                ),
            },
        }

    def rhs(
        self, t: float, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Continuous differential equation: dn/dt = r * n * (1 - n / K)."""
        n = max(0.0, float(state[0]))
        r = params.get("r", 0.6)
        k = max(1.0, params.get("K", 100.0))
        dn_dt = r * n * (1.0 - n / k)
        if len(state) > 1:
            return np.array([dn_dt, 0.0], dtype=float)
        return np.array([dn_dt], dtype=float)

    def discrete_step(
        self, state: np.ndarray, params: Dict[str, float]
    ) -> np.ndarray:
        """Discrete recursion: n(t+1) = n(t) + r * n(t) * (1 - n(t) / K)."""
        n = max(0.0, float(state[0]))
        r = params.get("r", 0.6)
        k = max(1.0, params.get("K", 100.0))
        n_next = max(0.0, n + r * n * (1.0 - n / k))
        if len(state) > 1:
            return np.array([n_next, 0.0], dtype=float)
        return np.array([n_next], dtype=float)


# Registry of available models for the sandwich menu
AVAILABLE_MODELS: List[BiologicalModel] = [
    LotkaVolterraCompetitionModel(),
    ExponentialGrowthModel(),
    LogisticGrowthModel(),
    LotkaVolterraPredatorPreyModel(),
    ChemostatModel(),
    RosenzweigMacArthurModel(),
    TypeIIIPredatorPreyModel(),
    ConsumerResourceModel(
        name="Modular Custom Consumer-Resource Model",
        category="Consumer-Resource Models",
        f_type="logistic",
        g_type="type_2_saturating",
        h_type="density_dependent_death",
    ),
]
