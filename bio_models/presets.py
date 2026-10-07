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
            "name": "Discrete Chaos & Limit Cycles",
            "description": (
                "In discrete recursion, strong growth rates (r > 2.0) "
                "generate period-doubling overshoots, limit cycles, and chaos."
            ),
            "initial": (20, 0),
            "t_span": (0.0, 40.0),
            "params": {
                "r": 2.65,
                "K": 100,
            },
        },
    ],
    "Haploid Selection Model": [
        {
            "name": "Directional Selection (Advantageous A)",
            "description": (
                "Allele A has higher reproductive fitness (W_A > W_a) and "
                "steadily rises to complete fixation (p = 1)."
            ),
            "initial": (5, 95),
            "t_span": (0.0, 40.0),
            "params": {
                "W_A": 1.25,
                "W_a": 1.00,
            },
        },
        {
            "name": "Deleterious Allele Purging",
            "description": (
                "Allele A has lower fitness (W_A < W_a) and is purged by "
                "natural selection (p decays toward 0)."
            ),
            "initial": (80, 20),
            "t_span": (0.0, 40.0),
            "params": {
                "W_A": 0.80,
                "W_a": 1.00,
            },
        },
        {
            "name": "Null Hypothesis: Neutral Drift (Equal Fitness)",
            "description": (
                "Both alleles have identical fitness (W_A = W_a = 1.0), "
                "maintaining constant frequencies across generations."
            ),
            "initial": (50, 50),
            "t_span": (0.0, 30.0),
            "params": {
                "W_A": 1.00,
                "W_a": 1.00,
            },
        },
        {
            "name": "Strong Selective Sweep",
            "description": (
                "Strong positive selection (W_A = 2.0 vs W_a = 1.0) "
                "drives rare allele A to fixation within a few steps."
            ),
            "initial": (1, 99),
            "t_span": (0.0, 20.0),
            "params": {
                "W_A": 2.00,
                "W_a": 1.00,
            },
        },
    ],
    "Diploid Selection Model": [
        {
            "name": (
                "Null Hypothesis: Neutral Drift "
                "(Equal Fitness / Hardy-Weinberg)"
            ),
            "description": (
                "Evolutionary null hypothesis: all genotypes have equal "
                "fitness (W_AA = W_Aa = W_aa = 1.0), maintaining allele "
                "frequencies constant across generations."
            ),
            "initial": (50, 50),
            "t_span": (0.0, 40.0),
            "params": {
                "W_AA": 1.00,
                "W_Aa": 1.00,
                "W_aa": 1.00,
            },
        },
        {
            "name": "Directional Selection (Advantageous A)",
            "description": (
                "Additive selection (W_AA > W_Aa > W_aa) where beneficial "
                "allele A rises monotonically toward fixation."
            ),
            "initial": (5, 95),
            "t_span": (0.0, 50.0),
            "params": {
                "W_AA": 1.30,
                "W_Aa": 1.15,
                "W_aa": 1.00,
            },
        },
        {
            "name": "Heterozygote Advantage (Balanced Polymorphism)",
            "description": (
                "Overdominance (W_Aa > W_AA, W_aa) maintains both alleles "
                "at a stable polymorphic internal equilibrium (e.g. "
                "sickle-cell anemia)."
            ),
            "initial": (15, 85),
            "t_span": (0.0, 50.0),
            "params": {
                "W_AA": 0.90,
                "W_Aa": 1.20,
                "W_aa": 0.60,
            },
        },
        {
            "name": "Heterozygote Disadvantage (Disruptive Selection)",
            "description": (
                "Underdominance (W_Aa < W_AA, W_aa) creates an unstable "
                "internal equilibrium; populations fix for whichever "
                "allele is initially more common."
            ),
            "initial": (55, 45),
            "t_span": (0.0, 40.0),
            "params": {
                "W_AA": 1.15,
                "W_Aa": 0.80,
                "W_aa": 1.15,
            },
        },
        {
            "name": "Recessive Beneficial Allele",
            "description": (
                "Allele A is beneficial only in homozygotes (W_AA > W_Aa "
                "= W_aa); initial rise is slow, then sweeps rapidly once "
                "common."
            ),
            "initial": (5, 95),
            "t_span": (0.0, 60.0),
            "params": {
                "W_AA": 1.30,
                "W_Aa": 1.00,
                "W_aa": 1.00,
            },
        },
        {
            "name": "Dominant Beneficial Allele",
            "description": (
                "Allele A is dominant (W_AA = W_Aa > W_aa); rises rapidly "
                "from rarity but slows down near fixation as recessive a "
                "hides in heterozygotes."
            ),
            "initial": (5, 95),
            "t_span": (0.0, 60.0),
            "params": {
                "W_AA": 1.25,
                "W_Aa": 1.25,
                "W_aa": 1.00,
            },
        },
    ],
    "Mutation-Selection Model": [
        {
            "name": (
                "Null Hypothesis: Neutral Drift (Equal Fitness, Zero Mutation)"
            ),
            "description": (
                "Evolutionary null hypothesis: equal fitnesses "
                "(W_A = W_a = 1.0) and zero mutation (μ = ν = 0) keep "
                "allele frequencies constant across generations."
            ),
            "initial": (50, 50),
            "t_span": (0.0, 40.0),
            "params": {
                "W_A": 1.00,
                "W_a": 1.00,
                "mu": 0.00,
                "nu": 0.00,
            },
        },
        {
            "name": (
                "Mutation-Selection Balance (Purifying Selection vs Mutation)"
            ),
            "description": (
                "Favorable allele A (W_A = 1.0) suffers recurrent deleterious "
                "mutation (μ = 0.02) to inferior allele a (W_a = 0.85), "
                "stabilizing at balance q̂ ≈ μ/s."
            ),
            "initial": (95, 5),
            "t_span": (0.0, 60.0),
            "params": {
                "W_A": 1.00,
                "W_a": 0.85,
                "mu": 0.02,
                "nu": 0.001,
            },
        },
        {
            "name": "Mutational Equilibrium (Two-Way Neutral Mutation)",
            "description": (
                "Equal reproductive fitness (W_A = W_a = 1.0) with forward "
                "(μ = 0.03) and reverse (ν = 0.01) mutations converges to "
                "equilibrium p̂ = ν/(μ + ν) = 0.25."
            ),
            "initial": (80, 20),
            "t_span": (0.0, 80.0),
            "params": {
                "W_A": 1.00,
                "W_a": 1.00,
                "mu": 0.03,
                "nu": 0.01,
            },
        },
        {
            "name": "Adaptive Mutation Sweep (Novel Beneficial Allele)",
            "description": (
                "Rare beneficial allele A (W_A = 1.30 vs W_a = 1.0) is "
                "continuously seeded by mutation (ν = 0.01), accelerating "
                "its sweep toward near-fixation."
            ),
            "initial": (1, 99),
            "t_span": (0.0, 40.0),
            "params": {
                "W_A": 1.30,
                "W_a": 1.00,
                "mu": 0.005,
                "nu": 0.01,
            },
        },
    ],
    "Migration-Selection Model": [
        {
            "name": (
                "Null Hypothesis: Neutral Drift "
                "(Isolated Island, Zero Migration)"
            ),
            "description": (
                "Evolutionary null hypothesis: equal fitnesses "
                "(W_A = W_a = 1.0) and zero gene flow (m = 0) keep island "
                "allele frequencies in perpetual stasis."
            ),
            "initial": (50, 50),
            "t_span": (0.0, 40.0),
            "params": {
                "W_A": 1.00,
                "W_a": 1.00,
                "m": 0.00,
                "p_m": 0.50,
            },
        },
        {
            "name": (
                "Migration-Selection Balance (Local Adaptation vs Gene Flow)"
            ),
            "description": (
                "Allele A is locally favored on island (W_A = 1.25 vs "
                "W_a = 1.0), but maladapted migrants from mainland "
                "(p_m = 0.05, m = 0.06) sustain polymorphism."
            ),
            "initial": (70, 30),
            "t_span": (0.0, 60.0),
            "params": {
                "W_A": 1.25,
                "W_a": 1.00,
                "m": 0.06,
                "p_m": 0.05,
            },
        },
        {
            "name": "Gene Swamping (Migration Overcomes Local Selection)",
            "description": (
                "High migration rate (m = 0.25) from mainland fixed for a "
                "(p_m = 0.0) overwhelms weak local adaptation (s = 0.10), "
                "driving allele A to extinction."
            ),
            "initial": (80, 20),
            "t_span": (0.0, 50.0),
            "params": {
                "W_A": 1.10,
                "W_a": 1.00,
                "m": 0.25,
                "p_m": 0.00,
            },
        },
        {
            "name": "Island Rescue (Immigrant Influx Sustains Allele A)",
            "description": (
                "Allele A is locally disfavored on island (W_A = 0.85 vs "
                "W_a = 1.0), but massive immigration from mainland where A "
                "is common (p_m = 0.90, m = 0.12) rescues it."
            ),
            "initial": (10, 90),
            "t_span": (0.0, 50.0),
            "params": {
                "W_A": 0.85,
                "W_a": 1.00,
                "m": 0.12,
                "p_m": 0.90,
            },
        },
        {
            "name": "Neutral Gene Flow (Swamping to Mainland Frequency)",
            "description": (
                "No selection differentials (W_A = W_a = 1.0); pure gene "
                "flow (m = 0.10) smoothly drives the island frequency toward "
                "mainland source frequency p_m = 0.75."
            ),
            "initial": (15, 85),
            "t_span": (0.0, 50.0),
            "params": {
                "W_A": 1.00,
                "W_a": 1.00,
                "m": 0.10,
                "p_m": 0.75,
            },
        },
    ],
    "Classic SIR Model (Kermack & McKendrick)": [
        {
            "name": "Epidemic Wave (R₀ = 2.0, Major Outbreak)",
            "description": (
                "Classic epidemic outbreak with R₀ ≈ 1.98. The infectious "
                "wave climbs to a prominent peak before herd immunity "
                "exhausts transmission, leaving uninfected survivors."
            ),
            "initial": (990, 10, 0),
            "t_span": (0.0, 70.0),
            "params": {
                "beta": 0.0002,
                "gamma": 0.10,
            },
        },
        {
            "name": "Sub-Threshold Outbreak (R₀ = 0.8, Self-Limiting)",
            "description": (
                "Sub-critical pathogen transmission (R₀ < 1.0). Each "
                "infected individual fails to replace themselves, leading to "
                "monotonic disease decay without an epidemic wave."
            ),
            "initial": (990, 10, 0),
            "t_span": (0.0, 50.0),
            "params": {
                "beta": 0.00008,
                "gamma": 0.10,
            },
        },
        {
            "name": "High Contagion / Rapid Wave (R₀ = 3.5)",
            "description": (
                "Highly contagious disease (R₀ ≈ 3.47). Produces an "
                "intense, early infection spike and rapidly consumes "
                "the susceptible pool down to low final endemic escape."
            ),
            "initial": (990, 10, 0),
            "t_span": (0.0, 45.0),
            "params": {
                "beta": 0.00035,
                "gamma": 0.10,
            },
        },
        {
            "name": "Herd Immunity Buffer (Pre-Immune Population)",
            "description": (
                "A population with 54% pre-existing immunity (R₀ = 1000). "
                "The effective reproduction number R_eff drops below 1.0, "
                "protecting the remaining susceptibles from an outbreak."
            ),
            "initial": (450, 10, 540),
            "t_span": (0.0, 50.0),
            "params": {
                "beta": 0.0002,
                "gamma": 0.10,
            },
        },
    ],
    "SIS Model (Endemic Diseases)": [
        {
            "name": "Endemic Persistence (R₀ = 2.0, Stable Equilibrium)",
            "description": (
                "Infection without permanent immunity (R₀ = 2.0). Recurrent "
                "re-susceptibility prevents disease clearance, stabilizing at "
                "endemic equilibrium I* = N(1 - 1/R₀) = 500 individuals."
            ),
            "initial": (950, 50),
            "t_span": (0.0, 60.0),
            "params": {
                "beta": 0.0002,
                "gamma": 0.10,
            },
        },
        {
            "name": "Disease Eradication (R₀ = 0.75, Below Threshold)",
            "description": (
                "Sub-threshold transmission (R₀ = 0.75). Recovery outpaces "
                "transmission, eradicating the pathogen and restoring the "
                "disease-free equilibrium (I → 0, S → N)."
            ),
            "initial": (850, 150),
            "t_span": (0.0, 50.0),
            "params": {
                "beta": 0.000075,
                "gamma": 0.10,
            },
        },
        {
            "name": "High Endemic Prevalence (R₀ = 4.0)",
            "description": (
                "Severe reinfection pressure (R₀ = 4.0). Overcomes rapid "
                "recovery, locking 75% of the total population into the "
                "infectious state at endemic steady state."
            ),
            "initial": (980, 20),
            "t_span": (0.0, 50.0),
            "params": {
                "beta": 0.0004,
                "gamma": 0.10,
            },
        },
        {
            "name": "Critical Bifurcation Boundary (R₀ ≈ 1.05)",
            "description": (
                "Near-transcritical bifurcation threshold (R₀ = 1.05). "
                "Transmission barely exceeds recovery, sustaining a tenuous "
                "low-level endemic equilibrium (I* ≈ 48)."
            ),
            "initial": (950, 50),
            "t_span": (0.0, 100.0),
            "params": {
                "beta": 0.000105,
                "gamma": 0.10,
            },
        },
    ],
    "SEIR Model with Incubation Period": [
        {
            "name": "Influenza-Like Epidemic (Short Latency, R₀ = 2.2)",
            "description": (
                "Acute viral infection with rapid incubation (1/σ = 2 days). "
                "The exposed compartment peak precedes the infectious peak, "
                "broadening the epidemic wave."
            ),
            "initial": (990, 5, 5, 0),
            "t_span": (0.0, 70.0),
            "params": {
                "beta": 0.00022,
                "sigma": 0.50,
                "gamma": 0.10,
            },
        },
        {
            "name": "Prolonged Latency / Wave Flattening (Long Latency)",
            "description": (
                "Extended incubation period (1/σ = 10 days, σ = 0.10). "
                "Substantially flattens and delays the infectious peak "
                "without changing the basic reproduction number R₀."
            ),
            "initial": (990, 5, 5, 0),
            "t_span": (0.0, 100.0),
            "params": {
                "beta": 0.00022,
                "sigma": 0.10,
                "gamma": 0.10,
            },
        },
        {
            "name": "Sub-Threshold Latent Outbreak (R₀ = 0.85)",
            "description": (
                "Sub-critical latent pathogen (R₀ = 0.83). Exposed carriers "
                "transition to infectiousness but fail to replace themselves, "
                "resulting in spontaneous disease clearance."
            ),
            "initial": (980, 10, 10, 0),
            "t_span": (0.0, 60.0),
            "params": {
                "beta": 0.000085,
                "sigma": 0.25,
                "gamma": 0.10,
            },
        },
        {
            "name": "Transmission Slashing / Lockdown Intervention",
            "description": (
                "Simulates contact rate reduction mid-outbreak, dropping "
                "R_eff below 1.0. Drains the latent exposed reservoir and "
                "quenches the transmission chain."
            ),
            "initial": (800, 80, 60, 60),
            "t_span": (0.0, 60.0),
            "params": {
                "beta": 0.00007,
                "sigma": 0.20,
                "gamma": 0.10,
            },
        },
    ],
}
