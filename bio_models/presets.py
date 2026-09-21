"""Predefined biological scenarios and parameter sets illustrating
textbook phenomena from Otto & Day (Chapter 3).
"""

from typing import Any, Dict, List

PRESETS: Dict[str, List[Dict[str, Any]]] = {
    "Lotka-Volterra Competition & Species Interactions": [
        {
            "name": "Stable Coexistence (Interspecific < Intraspecific)",
            "description": (
                "Both species exert weak competition on each other "
                "(α₁₂ < K₁/K₂ and α₂₁ < K₂/K₁), resulting in stable "
                "coexistence."
            ),
            "initial": (25, 20),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.8,
                "r2": 0.7,
                "K1": 100,
                "K2": 100,
                "alpha12": 0.45,
                "alpha21": 0.40,
            },
        },
        {
            "name": "Competitive Exclusion (Species 1 Wins)",
            "description": (
                "Species 1 outcompetes Species 2 regardless of initial "
                "densities, driving Species 2 to extinction."
            ),
            "initial": (15, 40),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.9,
                "r2": 0.6,
                "K1": 120,
                "K2": 80,
                "alpha12": 0.35,
                "alpha21": 1.25,
            },
        },
        {
            "name": "Competitive Exclusion (Species 2 Wins)",
            "description": (
                "Species 2 dominates and drives Species 1 to zero."
            ),
            "initial": (40, 15),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.6,
                "r2": 0.9,
                "K1": 80,
                "K2": 120,
                "alpha12": 1.30,
                "alpha21": 0.35,
            },
        },
        {
            "name": (
                "Bistability / Founder Control (Unstable Equilibrium)"
            ),
            "description": (
                "Interspecific competition is stronger than intraspecific "
                "(α > 1). The species with higher initial advantage wins; "
                "other goes extinct."
            ),
            "initial": (45, 50),
            "t_span": (0.0, 60.0),
            "params": {
                "r1": 0.8,
                "r2": 0.8,
                "K1": 100,
                "K2": 100,
                "alpha12": 1.30,
                "alpha21": 1.25,
            },
        },
        {
            "name": "Mutualism / Symbiosis (Negative α)",
            "description": (
                "Both α₁₂ < 0 and α₂₁ < 0: each species promotes the "
                "abundance and carrying capacity of the other."
            ),
            "initial": (20, 20),
            "t_span": (0.0, 40.0),
            "params": {
                "r1": 0.7,
                "r2": 0.7,
                "K1": 80,
                "K2": 80,
                "alpha12": -0.35,
                "alpha21": -0.30,
            },
        },
        {
            "name": "Commensalism (Species 2 benefits Species 1)",
            "description": (
                "α₁₂ < 0 and α₂₁ = 0: Species 2 provides nesting/refuge to "
                "Species 1 without any benefit or cost to itself."
            ),
            "initial": (15, 25),
            "t_span": (0.0, 45.0),
            "params": {
                "r1": 0.6,
                "r2": 0.6,
                "K1": 70,
                "K2": 90,
                "alpha12": -0.45,
                "alpha21": 0.0,
            },
        },
    ],
    "Classic Lotka-Volterra Predator-Prey (Eq 3.18)": [
        {
            "name": "Neutral Periodic Oscillations (Standard)",
            "description": (
                "Classic closed orbits where prey and predator cycle "
                "perpetually out of phase (Eq 3.18)."
            ),
            "initial": (30, 10),
            "t_span": (0.0, 50.0),
            "params": {
                "r": 0.9,
                "a": 0.05,
                "c": 0.4,
                "epsilon": 0.5,
                "delta": 0.25,
            },
        },
        {
            "name": "High Amplitude Boom-and-Bust Cycles",
            "description": (
                "Higher prey growth rate creates dramatic population booms "
                "followed by severe predator crashes."
            ),
            "initial": (40, 5),
            "t_span": (0.0, 60.0),
            "params": {
                "r": 1.4,
                "a": 0.04,
                "c": 0.5,
                "epsilon": 0.6,
                "delta": 0.35,
            },
        },
    ],
    "Nutrient Inflow / Chemostat Model (Eq 3.17)": [
        {
            "name": "Chemostat Steady State (Algal Inflow Equilibrium)",
            "description": (
                "Constant nutrient replenishment (θ) maintains an equilibrium "
                "balance between nutrient and consumer/algae."
            ),
            "initial": (25, 5),
            "t_span": (0.0, 60.0),
            "params": {
                "theta": 18.0,
                "a": 0.06,
                "c": 0.25,
                "epsilon": 0.65,
                "delta": 0.30,
            },
        },
        {
            "name": "Nutrient Depletion Shock (Low Inflow)",
            "description": (
                "Low nutrient inflow causes consumer population to collapse "
                "due to starvation."
            ),
            "initial": (15, 20),
            "t_span": (0.0, 50.0),
            "params": {
                "theta": 3.0,
                "a": 0.05,
                "c": 0.3,
                "epsilon": 0.5,
                "delta": 0.35,
            },
        },
    ],
    "Rosenzweig-MacArthur (Type II Limit Cycles)": [
        {
            "name": "Stable Limit Cycle (Paradox of Enrichment)",
            "description": (
                "High carrying capacity K pushes the equilibrium into the "
                "unstable zone, producing a robust, stable limit cycle."
            ),
            "initial": (40, 15),
            "t_span": (0.0, 100.0),
            "params": {
                "r": 1.2,
                "K": 140,
                "a": 0.8,
                "c": 0.9,
                "b": 25.0,
                "epsilon": 0.45,
                "delta": 0.22,
            },
        },
        {
            "name": "Damped Spiral to Stable Coexistence Focus",
            "description": (
                "Moderate carrying capacity produces damped oscillations "
                "spiraling inward to a stable interior equilibrium."
            ),
            "initial": (60, 25),
            "t_span": (0.0, 80.0),
            "params": {
                "r": 0.9,
                "K": 65,
                "a": 0.7,
                "c": 0.8,
                "b": 30.0,
                "epsilon": 0.50,
                "delta": 0.25,
            },
        },
    ],
    "Generalized Type III Predator-Prey (Sigmoidal)": [
        {
            "name": "Prey Refuge Protection (k = 2.0)",
            "description": (
                "Sigmoidal functional response protects prey at low density "
                "(prey switching / habitat refuges)."
            ),
            "initial": (30, 12),
            "t_span": (0.0, 80.0),
            "params": {
                "r": 1.0,
                "K": 100,
                "a": 0.6,
                "c": 1.0,
                "b": 350.0,
                "k": 2.2,
                "epsilon": 0.5,
                "delta": 0.22,
            },
        },
    ],
    "Modular Custom Consumer-Resource (Table 3.3)": [
        {
            "name": (
                "Logistic Prey + Type II + Density-Dependent "
                "Predator Mortality"
            ),
            "description": (
                "Self-limiting predators (γ > 0) stabilize what would "
                "otherwise be unstable limit cycles."
            ),
            "initial": (50, 20),
            "t_span": (0.0, 70.0),
            "params": {
                "r": 1.1,
                "K": 120,
                "a": 0.8,
                "c": 1.0,
                "b": 25.0,
                "epsilon": 0.45,
                "delta": 0.15,
                "gamma": 0.008,
            },
        },
    ],
}
