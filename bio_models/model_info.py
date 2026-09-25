"""
Model information, mathematical governing equations, and biological scenarios.
Provides formatted HTML for hover tooltips on the model info badge.
"""

from typing import Any, Dict


MODEL_DETAILS: Dict[str, Dict[str, Any]] = {
    "Lotka-Volterra Competition & Species Interactions": {
        "title": "Lotka-Volterra Competition & Multi-Species Interactions",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = r₁·n₁·(1 - (n₁ + α₁₂·n₂) / K₁)",
            "dn₂/dt = r₂·n₂·(1 - (n₂ + α₂₁·n₁) / K₂)",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + r₁·n₁(t)·(1 - (n₁(t) + α₁₂·n₂(t)) / K₁)",
            "n₂(t+1) = n₂(t) + r₂·n₂(t)·(1 - (n₂(t) + α₂₁·n₁(t)) / K₂)",
        ],
        "scenarios": (
            "Models competitive interactions between two species utilizing "
            "shared, limiting environmental resources (e.g. food, light, "
            "territory). Primary biological scenarios include:<br>"
            "• <b>Competitive Exclusion</b>: When interspecific competition "
            "is stronger than intraspecific regulation, one species drives "
            "the other to extinction (Gause's Principle).<br>"
            "• <b>Stable Coexistence</b>: Niche partitioning where each "
            "species limits itself more than its competitor (α₁₂ &lt; K₁/K₂ "
            "and α₂₁ &lt; K₂/K₁).<br>"
            "• <b>Founder Control / Priority Effects</b>: The initial "
            "dominant population excludes the other.<br>"
            "• <b>Mutualism / Commensalism</b>: Cooperative or asymmetric "
            "interactions when interaction coefficients α take negative or "
            "zero values."
        ),
    },
    "Classic Lotka-Volterra Predator-Prey": {
        "title": "Classic Lotka-Volterra Predator-Prey Model",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = r·n₁ - a·c·n₁·n₂",
            "dn₂/dt = ε·a·c·n₁·n₂ - δ·n₂",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + r·n₁(t) - a·c·n₁(t)·n₂(t)",
            "n₂(t+1) = n₂(t) + ε·a·c·n₁(t)·n₂(t) - δ·n₂(t)",
        ],
        "scenarios": (
            "Foundational baseline model for trophic interactions between a "
            "resource/prey and a specialized consumer/predator:<br>"
            "• <b>Cyclical Oscillations</b>: Periodic, undamped population "
            "cycles where predator peaks lag behind prey booms (e.g. lynx "
            "and snowshoe hare).<br>"
            "• <b>Unchecked Prey Growth</b>: Exponential prey reproduction in "
            "the absence of predation.<br>"
            "• <b>Linear Functional Response</b>: Predator consumption "
            "scales linearly with prey density without satiation (Holling "
            "Type I).<br>"
            "• <b>Neutral Stability</b>: Closed elliptical orbits in phase "
            "space conserving an ecological invariant."
        ),
    },
    "Nutrient Inflow / Chemostat Model": {
        "title": "Nutrient Inflow / Chemostat Model",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = θ - a·c·n₁·n₂",
            "dn₂/dt = ε·a·c·n₁·n₂ - δ·n₂",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + θ - a·c·n₁(t)·n₂(t)",
            "n₂(t+1) = n₂(t) + ε·a·c·n₁(t)·n₂(t) - δ·n₂(t)",
        ],
        "scenarios": (
            "Models open ecosystems and continuous-flow bioreactors receiving "
            "constant nutrient inflow (θ):<br>"
            "• <b>Continuous Culture & Fermentation</b>: Industrial and "
            "laboratory microbial cultivation where fresh substrate is "
            "continuously fed and effluent washed out.<br>"
            "• <b>Aquatic Plankton Blooms</b>: Phytoplankton grazing "
            "sustained by steady upwelling or riverine nutrient runoff.<br>"
            "• <b>Gut Microbiome Dynamics</b>: Steady dietary nutrient "
            "replenishment supporting resident microbial populations."
        ),
    },
    "Rosenzweig-MacArthur (Type II Limit Cycles)": {
        "title": "Rosenzweig-MacArthur Model (Holling Type II)",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = r·n₁·(1 - n₁/K) - (a·c·n₁ / (b + n₁))·n₂",
            "dn₂/dt = ε·(a·c·n₁ / (b + n₁))·n₂ - δ·n₂",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + r·n₁(t)·(1 - n₁(t)/K) - "
            "(a·c·n₁(t) / (b + n₁(t)))·n₂(t)",
            "n₂(t+1) = n₂(t) + ε·(a·c·n₁(t) / (b + n₁(t)))·n₂(t) - δ·n₂(t)",
        ],
        "scenarios": (
            "Incorporates realistic prey self-limitation (carrying capacity "
            "K) and predator handling time saturation (Holling Type II):<br>"
            "• <b>Predator Satiation & Handling Time</b>: Consumption "
            "plateaus at high prey densities as predators spend time "
            "capturing and digesting.<br>"
            "• <b>Stable Limit Cycles</b>: Non-linear oscillations where "
            "trajectories are attracted to an isolated closed cycle.<br>"
            "• <b>Paradox of Enrichment</b>: Increasing resource carrying "
            "capacity K destabilizes an otherwise stable equilibrium into "
            "destructive oscillations."
        ),
    },
    "Generalized Type III Predator-Prey (Sigmoidal)": {
        "title": "Generalized Type III Predator-Prey Model",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = r·n₁·(1 - n₁/K) - (a·c·n₁ᵏ / (b + n₁ᵏ))·n₂",
            "dn₂/dt = ε·(a·c·n₁ᵏ / (b + n₁ᵏ))·n₂ - δ·n₂",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + r·n₁(t)·(1 - n₁(t)/K) - "
            "(a·c·n₁ᵏ(t) / (b + n₁ᵏ(t)))·n₂(t)",
            "n₂(t+1) = n₂(t) + ε·(a·c·n₁ᵏ(t) / (b + n₁ᵏ(t)))·n₂(t) - "
            "δ·n₂(t)",
        ],
        "scenarios": (
            "Incorporates an S-shaped (sigmoidal Holling Type III) response "
            "where predation is suppressed at low prey densities:<br>"
            "• <b>Prey Switching & Search Images</b>: Generalist predators "
            "switch away from rare prey to more abundant alternatives.<br>"
            "• <b>Physical Refuges</b>: Prey find safety in burrows or "
            "dense cover at low densities, protecting them from total "
            "extinction.<br>"
            "• <b>Ecosystem Stability</b>: Damps violent oscillations and "
            "fosters persistence in diverse communities."
        ),
    },
    "Modular Custom Consumer-Resource Model": {
        "title": "Modular Custom Consumer-Resource Model",
        "diff_eq_type": "Coupled Ordinary Differential Equations",
        "diff_eq": [
            "dn₁/dt = f(n₁) - g(n₁, n₂)",
            "dn₂/dt = ε·g(n₁, n₂) - h(n₂)",
        ],
        "disc_eq_type": "Coupled Discrete Difference Equations (Recursion)",
        "disc_eq": [
            "n₁(t+1) = n₁(t) + f(n₁(t)) - g(n₁(t), n₂(t))",
            "n₂(t+1) = n₂(t) + ε·g(n₁(t), n₂(t)) - h(n₂(t))",
        ],
        "scenarios": (
            "A generalized framework enabling combinatorial investigation of "
            "ecological interaction functions:<br>"
            "• <b>Resource Renewal f(n₁)</b>: Logistic growth, constant "
            "inflow/outflow, exponential growth, or exponential decline.<br>"
            "• <b>Functional Response g(n₁, n₂)</b>: Linear (Type I), "
            "Saturating (Type II), or Sigmoidal (Type III).<br>"
            "• <b>Consumer Mortality h(n₂)</b>: Constant per-capita mortality "
            "or density-dependent intraspecific interference (γ·n₂²).<br>"
            "• <b>Bespoke Scenarios</b>: Plant-herbivore dynamics, bio-"
            "filtration, host-parasitoid dynamics, and multi-trophic balance."
        ),
    },
    "Exponential Growth Model": {
        "title": "Exponential Population Growth Model",
        "diff_eq_type": "Ordinary Differential Equation",
        "diff_eq": [
            "dn/dt = r·n",
            "(where r = b - d: per capita birth rate - death rate)",
        ],
        "disc_eq_type": "Discrete Difference Equation (Recursion)",
        "disc_eq": [
            "n(t+1) = R·n(t)",
            "(where R = 1 + r_d = (1 - d)·(1 + b))",
        ],
        "scenarios": (
            "Models unrestricted population growth in an ideal, limitless "
            "environment where resource availability per individual is "
            "constant regardless of population size (Otto & Day 2007). "
            "Primary biological scenarios include:<br>"
            "• <b>Colonization & Island Expansion</b>: Rapid population boom "
            "following introduction into unexploited habitats (e.g. "
            "Protection Island pheasants, Lack 1954).<br>"
            "• <b>Microbial / Bacterial Fission</b>: Constant binary fission "
            "rate under continuous nutrient excess in culture blooms.<br>"
            "• <b>Population Decline / Extinction</b>: Per capita death rate "
            "exceeding birth rate (d &gt; b, r &lt; 0, R &lt; 1) causing "
            "exponential decay toward zero.<br>"
            "• <b>Generational Replacement</b>: Perfect demographic balance "
            "(b = d, R = 1, r = 0) maintaining a stationary population."
        ),
    },
    "Logistic Growth Model": {
        "title": "Logistic Population Growth Model",
        "diff_eq_type": "Ordinary Differential Equation",
        "diff_eq": [
            "dn/dt = r·n·(1 - n / K)",
            "(where r is intrinsic growth rate and K is carrying capacity)",
        ],
        "disc_eq_type": "Discrete Difference Equation (Recursion)",
        "disc_eq": [
            "n(t+1) = n(t) + r_d·n(t)·(1 - n(t) / K)",
            "(where r_d is discrete growth rate and K is carrying capacity)",
        ],
        "scenarios": (
            "Incorporates density-dependent regulation where resource "
            "limitation and intraspecific competition linearly reduce per "
            "capita growth as density approaches carrying capacity K "
            "(Otto & Day 2007). Primary biological scenarios include:<br>"
            "• <b>Sigmoidal Carrying Capacity Approach</b>: Classic S-shaped "
            "curve with initial exponential growth transitioning into "
            "asymptotic saturation at K.<br>"
            "• <b>Cell Culture Growth (Mable & Otto 2001)</b>: Haploid vs. "
            "diploid yeast cultures reaching distinct carrying capacities "
            "based on cell volume and nutrient demand.<br>"
            "• <b>Overcapacity Damping</b>: Populations introduced above "
            "carrying capacity (n &gt; K) experiencing resource shortages "
            "and declining back down to K.<br>"
            "• <b>Discrete Overshoot & Chaos (May 1976)</b>: In discrete "
            "time, strong growth rates (r &gt; 2.0) generate delayed feedback "
            "overshoots, stable limit cycles, and deterministic chaos."
        ),
    },
}


def get_model_info_html(
    model_name: str, mode: str = "continuous", theme: str = "dark"
) -> str:
    """Return styled HTML information for the given model and calculation mode.

    Informs which equations (differential vs difference) are used to draw
    the graph and details the general biological scenarios modeled.
    """
    details = MODEL_DETAILS.get(
        model_name,
        MODEL_DETAILS["Lotka-Volterra Competition & Species Interactions"],
    )

    is_dark = theme.lower() == "dark"
    is_discrete = mode.lower() == "discrete"

    title_color = "#ffffff" if is_dark else "#0f172a"
    eq_badge_color = (
        ("#f87171" if is_dark else "#dc2626")
        if is_discrete
        else ("#38bdf8" if is_dark else "#0284c7")
    )
    code_bg = "#111113" if is_dark else "#f1f5f9"
    code_border = "#27272a" if is_dark else "#cbd5e1"
    code_color = "#f4f4f5" if is_dark else "#0f172a"
    section_title = "#a1a1aa" if is_dark else "#475569"
    body_color = "#d4d4d8" if is_dark else "#334155"

    eq_type = (
        details["disc_eq_type"] if is_discrete else details["diff_eq_type"]
    )
    eq_lines = details["disc_eq"] if is_discrete else details["diff_eq"]
    eq_text = "<br>".join(eq_lines)

    title_html = (
        f'<div style="font-weight: 700; font-size: 13px; color: {title_color};'
        f' margin-bottom: 4px;">{details["title"]}</div>'
    )
    eq_header_html = (
        f'<div style="font-size: 11px; font-weight: 700; '
        f'color: {eq_badge_color}; margin-top: 6px; margin-bottom: 3px; '
        f'text-transform: uppercase; letter-spacing: 0.3px;">'
        f'Governing Equations ({eq_type}):</div>'
    )
    code_html = (
        f'<div style="font-family: monospace; font-size: 11px; '
        f'background-color: {code_bg}; border: 1px solid {code_border}; '
        f'color: {code_color}; padding: 6px 8px; border-radius: 4px; '
        f'margin-bottom: 8px;">{eq_text}</div>'
    )
    scenario_header_html = (
        f'<div style="font-size: 11px; font-weight: 700; '
        f'color: {section_title}; margin-top: 6px; margin-bottom: 3px; '
        f'text-transform: uppercase; letter-spacing: 0.3px;">'
        f'Biological Scenarios & Applications:</div>'
    )
    body_html = (
        f'<div style="font-size: 11px; color: {body_color};">'
        f'{details["scenarios"]}</div>'
    )

    html = (
        f'<div style="line-height: 1.45; max-width: 380px;">'
        f'{title_html}{eq_header_html}{code_html}'
        f'{scenario_header_html}{body_html}</div>'
    )
    return html
