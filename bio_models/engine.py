"""
Simulation and Numerical Integration Engine.
Uses SciPy adaptive ODE solvers (RK45, LSODA) and discrete recurrence steps.
"""

import time
from typing import Dict, Any, Optional
import numpy as np
from scipy.integrate import solve_ivp

from bio_models.models import BiologicalModel, SimulationResult


Tuple_State = tuple[float, float]


def simulate_model(
    model: BiologicalModel,
    initial_state: Tuple_State = (20.0, 10.0),
    t_span: Tuple_State = (0.0, 50.0),
    num_points: int = 500,
    params: Optional[Dict[str, float]] = None,
    mode: str = "continuous",  # "continuous" or "discrete"
    ode_method: str = "RK45",  # "RK45", "LSODA", "Radau"
) -> SimulationResult:
    """
    Run continuous ODE integration or discrete iteration for the biological model.
    """
    if params is None:
        params = model.default_params.copy()

    start_time = time.perf_counter()

    t_start, t_end = float(t_span[0]), float(t_span[1])
    if t_end <= t_start:
        t_end = t_start + 10.0
    valid_t_span = (t_start, t_end)

    t_eval = np.linspace(t_start, t_end, num_points)
    n1_init, n2_init = max(0.0, float(initial_state[0])), max(0.0, float(initial_state[1]))

    if mode == "discrete":
        # Discrete iteration step by step
        steps = num_points
        t_arr = np.linspace(t_start, t_end, steps)
        n1_arr = np.zeros(steps)
        n2_arr = np.zeros(steps)
        curr = np.array([n1_init, n2_init], dtype=float)
        n1_arr[0] = curr[0]
        n2_arr[0] = curr[1]

        for i in range(1, steps):
            try:
                curr = model.discrete_step(curr, params)
            except NotImplementedError:
                # Approximate Euler step if discrete recursion not explicitly defined
                dt = 1.0
                curr = curr + dt * model.rhs(float(i), curr, params)
                curr[0] = max(0.0, curr[0])
                curr[1] = max(0.0, curr[1])
            n1_arr[i] = curr[0]
            n2_arr[i] = curr[1]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SimulationResult(
            t=t_arr,
            n1=n1_arr,
            n2=n2_arr,
            model_name=model.name,
            n1_label=model.n1_label,
            n2_label=model.n2_label,
            parameters=params,
            metadata={
                "mode": "discrete",
                "steps": steps,
                "elapsed_ms": elapsed_ms,
            },
            success=True,
            message=f"Discrete simulation complete ({steps} steps in {elapsed_ms:.1f} ms)",
        )

    # Continuous integration via solve_ivp
    def ode_system(t, y):
        # Clip state to prevent non-physical negative numbers during solver steps
        clipped = np.array([max(0.0, y[0]), max(0.0, y[1])], dtype=float)
        return model.rhs(t, clipped, params)

    try:
        sol = solve_ivp(
            fun=ode_system,
            t_span=valid_t_span,
            y0=[n1_init, n2_init],
            t_eval=t_eval,
            method=ode_method,
            rtol=1e-6,
            atol=1e-8,
        )

        # Fallback to LSODA if RK45 encounters stiffness or failure
        if not sol.success and ode_method != "LSODA":
            sol = solve_ivp(
                fun=ode_system,
                t_span=valid_t_span,
                y0=[n1_init, n2_init],
                t_eval=t_eval,
                method="LSODA",
                rtol=1e-6,
                atol=1e-8,
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        if not sol.success:
            return SimulationResult(
                t=t_eval,
                n1=np.zeros_like(t_eval),
                n2=np.zeros_like(t_eval),
                model_name=model.name,
                n1_label=model.n1_label,
                n2_label=model.n2_label,
                parameters=params,
                metadata={"elapsed_ms": elapsed_ms, "solver": ode_method},
                success=False,
                message=f"Solver error: {sol.message}",
            )

        n1_res = np.maximum(0.0, sol.y[0])
        n2_res = np.maximum(0.0, sol.y[1])

        return SimulationResult(
            t=sol.t,
            n1=n1_res,
            n2=n2_res,
            model_name=model.name,
            n1_label=model.n1_label,
            n2_label=model.n2_label,
            parameters=params,
            metadata={
                "mode": "continuous",
                "solver": ode_method,
                "nfev": sol.nfev,
                "elapsed_ms": elapsed_ms,
            },
            success=True,
            message=f"Solved {len(sol.t)} time points in {elapsed_ms:.1f} ms using {ode_method}",
        )

    except Exception as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SimulationResult(
            t=t_eval,
            n1=np.zeros_like(t_eval),
            n2=np.zeros_like(t_eval),
            model_name=model.name,
            n1_label=model.n1_label,
            n2_label=model.n2_label,
            parameters=params,
            metadata={"elapsed_ms": elapsed_ms, "error": str(e)},
            success=False,
            message=f"Exception during simulation: {e}",
        )
