"""Predefined biological scenarios and parameter sets illustrating
fundamental ecological population interaction dynamics.
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
            "name": "Competitive Exclusion (Species 1 Outcompetes Species 2)",
            "description": (
                "Species 1 has strong competitive effect on species 2 "
                "(α₂₁ > K₂/K₁) while species 2 is weak, driving species 2 "
                "to extinction."
            ),
            "initial": (20, 25),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.9,
                "r2": 0.6,
                "K1": 120,
                "K2": 80,
                "alpha12": 0.3,
                "alpha21": 1.2,
            },
        },
        {
            "name": "Competitive Exclusion (Species 2 Outcompetes Species 1)",
            "description": (
                "Species 2 has strong competitive effect on species 1 "
                "(α₁₂ > K₁/K₁), driving species 1 to extinction."
            ),
            "initial": (25, 15),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.6,
                "r2": 0.9,
                "K1": 80,
                "K2": 120,
                "alpha12": 1.3,
                "alpha21": 0.35,
            },
        },
        {
            "name": (
                "Bistability / Founder Control (Unstable Equilibrium)"
            ),
            "description": (
                "Both species compete fiercely (α₁₂ > K₁/K₂ and α₂₁ > K₂/K₁). "
                "Whichever species starts with higher initial advantage wins."
            ),
            "initial": (40, 20),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.8,
                "r2": 0.8,
                "K1": 100,
                "K2": 100,
                "alpha12": 1.2,
                "alpha21": 1.2,
            },
        },
        {
            "name": "Obligate / Strong Mutualism (α₁₂, α₂₁ < 0)",
            "description": (
                "Both species benefit each other; negative α coefficients "
                "facilitate rapid reciprocal growth."
            ),
            "initial": (15, 15),
            "t_span": (0.0, 40.0),
            "params": {
                "r1": 0.5,
                "r2": 0.5,
                "K1": 80,
                "K2": 80,
                "alpha12": -0.35,
                "alpha21": -0.35,
            },
        },
        {
            "name": "Exploitative / Parasitic Dynamics (+ / -)",
            "description": (
                "Species 1 benefits (α₁₂ < 0) at the direct expense of "
                "species 2 (α₂₁ > 0)."
            ),
            "initial": (20, 25),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.6,
                "r2": 0.6,
                "K1": 100,
                "K2": 100,
                "alpha12": -0.4,
                "alpha21": 0.6,
            },
        },
        {
            "name": "Commensalism (+ / 0)",
            "description": (
                "Species 1 benefits from species 2 (α₁₂ < 0) while species 2 "
                "is unaffected (α₂₁ = 0)."
            ),
            "initial": (10, 30),
            "t_span": (0.0, 50.0),
            "params": {
                "r1": 0.7,
                "r2": 0.5,
                "K1": 90,
                "K2": 90,
                "alpha12": -0.45,
                "alpha21": 0.0,
            },
        },
    ],
    "Classic Lotka-Volterra Predator-Prey": [
        {
            "name": "Neutral Periodic Oscillations (Standard)",
            "description": (
                "Classic closed orbits where prey and predator cycle "
                "perpetually out of phase."
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
    "Nutrient Inflow / Chemostat Model": [
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
                "c": 0.3,
                "epsilon": 0.6,
                "delta": 0.25,
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
            "initial": (45, 15),
            "t_span": (0.0, 80.0),
            "params": {
                "r": 1.2,
                "K": 130,
                "a": 0.8,
                "c": 1.0,
                "b": 30.0,
                "epsilon": 0.4,
                "delta": 0.2,
            },
        },
        {
            "name": "Damped Spiral to Stable Coexistence Focus",
            "description": (
                "Lower carrying capacity K dampens oscillations, "
                "spiraling inward to a stable interior equilibrium."
            ),
            "initial": (40, 10),
            "t_span": (0.0, 80.0),
            "params": {
                "r": 1.0,
                "K": 60,
                "a": 0.8,
                "c": 1.0,
                "b": 30.0,
                "epsilon": 0.4,
                "delta": 0.2,
            },
        },
    ],
    "Generalized Type III Predator-Prey (Sigmoidal)": [
        {
            "name": "Sigmoidal Response with Prey Refuge",
            "description": (
                "S-shaped functional response buffers low prey numbers, "
                "preventing severe predator crashes."
            ),
            "initial": (35, 10),
            "t_span": (0.0, 70.0),
            "params": {
                "r": 1.0,
                "K": 100,
                "a": 0.5,
                "c": 1.0,
                "b": 350.0,
                "k": 2.2,
                "epsilon": 0.5,
                "delta": 0.22,
            },
        },
    ],
    "Modular Custom Consumer-Resource Model": [
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
    "Exponential Growth Model": [
        {
            "name": "Protection Island Pheasants (Lack 1954)",
            "description": (
                "Introduction of 8 pheasants onto Protection Island (1937), "
                "tripling annually in an unconstrained habitat (Lack 1954; "
                "Otto & Day 2007)."
            ),
            "initial": (8, 0),
            "t_span": (0.0, 5.0),
            "params": {
                "r": 1.10,
            },
        },
        {
            "name": "Rapid Bacterial Binary Fission",
            "description": (
                "Exponential microbial reproduction doubling every generation "
                "(doubling time t_d = ln(2)/r ≈ 1) under constant nutrient "
                "excess."
            ),
            "initial": (10, 0),
            "t_span": (0.0, 8.0),
            "params": {
                "r": 0.693,
            },
        },
        {
            "name": "Population Decline / Extinction Risk",
            "description": (
                "Per capita death rate exceeds birth rate (d > b, r < 0), "
                "causing continuous exponential decline toward zero."
            ),
            "initial": (120, 0),
            "t_span": (0.0, 25.0),
            "params": {
                "r": -0.15,
            },
        },
        {
            "name": "Stationary Replacement Equilibrium",
            "description": (
                "Exact demographic replacement where birth rate equals death "
                "rate (b = d, r = 0, R = 1), maintaining stationary "
                "population."
            ),
            "initial": (50, 0),
            "t_span": (0.0, 30.0),
            "params": {
                "r": 0.0,
            },
        },
    ],
    "Logistic Growth Model": [
        {
            "name": "Sigmoidal Carrying Capacity Approach",
            "description": (
                "Classic S-shaped logistic curve exhibiting initial "
                "exponential acceleration followed by density-dependent "
                "deceleration toward K = 100."
            ),
            "initial": (5, 0),
            "t_span": (0.0, 20.0),
            "params": {
                "r": 0.6,
                "K": 100,
            },
        },
        {
            "name": "Yeast Culture: Haploids (Mable & Otto 2001)",
            "description": (
                "Haploid Saccharomyces cerevisiae culture reaching carrying "
                "capacity K = 370 (3.7 × 10⁸ cells) with r = 0.55 /hr (Mable "
                "& Otto 2001)."
            ),
            "initial": (10, 0),
            "t_span": (0.0, 35.0),
            "params": {
                "r": 0.55,
                "K": 370,
            },
        },
        {
            "name": "Yeast Culture: Diploids (Mable & Otto 2001)",
            "description": (
                "Diploid Saccharomyces cerevisiae culture: larger cells "
                "require more resources, yielding lower carrying capacity "
                "K = 230 (2.3 × 10⁸ cells)."
            ),
            "initial": (10, 0),
            "t_span": (0.0, 35.0),
            "params": {
                "r": 0.55,
                "K": 230,
            },
        },
        {
            "name": "Overcapacity Crash & Damping",
            "description": (
                "Population starts above carrying capacity (n > K) and "
                "experiences negative net growth, decaying back down to K."
            ),
            "initial": (180, 0),
            "t_span": (0.0, 20.0),
            "params": {
                "r": 0.5,
                "K": 100,
            },
        },
        {
            "name": "Discrete Chaos & Limit Cycles (May 1976)",
            "description": (
                "In discrete recursion, strong growth rates (r > 2.0) "
                "generate period-doubling overshoots, limit cycles, and chaos "
                "(Robert May 1976)."
            ),
            "initial": (20, 0),
            "t_span": (0.0, 40.0),
            "params": {
                "r": 2.65,
                "K": 100,
            },
        },
    ],
}
