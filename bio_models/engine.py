"""Simulation and Numerical Integration Engine.

Uses SciPy adaptive ODE solvers (RK45, LSODA) and discrete recurrence
steps.
"""

import csv
import os
import time
from typing import Dict, Optional

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
    """Run continuous ODE integration or discrete iteration.

    Integrates or iterates the biological model over the given t_span.
    """
    if params is None:
        params = model.default_params.copy()

    start_time = time.perf_counter()

    t_start, t_end = float(t_span[0]), float(t_span[1])
    if t_end <= t_start:
        t_end = t_start + 10.0
    valid_t_span = (t_start, t_end)
    t_eval = np.linspace(t_start, t_end, num_points)

    if getattr(model, "is_frequency_model", False):
        # Allele frequencies lie in [0.0, 1.0]. Convert initial counts
        # or proportions into valid frequencies p and q = 1 - p.
        raw_1 = float(initial_state[0])
        raw_2 = float(initial_state[1]) if len(initial_state) > 1 else 0.0
        if (
            0.0 <= raw_1 <= 1.0
            and 0.0 <= raw_2 <= 1.0
            and (raw_1 > 0.0 or raw_2 > 0.0)
        ):
            tot = raw_1 + raw_2
            p_init = raw_1 / tot if tot > 0 else raw_1
        else:
            tot = max(1e-9, raw_1 + raw_2)
            p_init = raw_1 / tot
        n1_init = float(np.clip(p_init, 0.0, 1.0))
        n2_init = 1.0 - n1_init
    else:
        # Species individuals must be positive integers (>= 1)
        n1_init = float(max(1, int(round(float(initial_state[0])))))
        n2_init = (
            0.0
            if model.is_single_variable
            else float(max(1, int(round(float(initial_state[1])))))
        )

    if mode == "discrete":
        # In discrete mode, time advances in integer generation steps.
        # If num_points is omitted or default 500 while t_span is given,
        # compute the natural step count from t_end - t_start.
        if num_points is None or (
            num_points == 500 and (t_end - t_start) <= 250
        ):
            span_steps = max(1, int(round(t_end - t_start)))
            steps = span_steps + 1
        else:
            steps = max(2, int(num_points))

        t_arr = np.linspace(t_start, t_end, steps)
        n1_arr = np.zeros(steps)
        n2_arr = np.zeros(steps)

        if model.is_single_variable:
            curr = np.array([n1_init], dtype=float)
            n1_arr[0] = curr[0]
            for i in range(1, steps):
                try:
                    curr = model.discrete_step(curr, params)
                except NotImplementedError:
                    dt = 1.0
                    curr = curr + dt * model.rhs(float(i), curr, params)
                curr = np.nan_to_num(
                    curr, nan=0.0, posinf=1e300, neginf=0.0
                )
                curr[0] = max(0.0, curr[0])
                n1_arr[i] = curr[0]
        else:
            curr = np.array([n1_init, n2_init], dtype=float)
            n1_arr[0] = curr[0]
            n2_arr[0] = curr[1]
            for i in range(1, steps):
                try:
                    curr = model.discrete_step(curr, params)
                except NotImplementedError:
                    dt = 1.0
                    curr = curr + dt * model.rhs(float(i), curr, params)
                curr = np.nan_to_num(
                    curr, nan=0.0, posinf=1e300, neginf=0.0
                )
                if getattr(model, "is_frequency_model", False):
                    curr[0] = float(np.clip(curr[0], 0.0, 1.0))
                    curr[1] = 1.0 - curr[0]
                else:
                    curr[0] = max(0.0, curr[0])
                    curr[1] = max(0.0, curr[1])
                n1_arr[i] = curr[0]
                n2_arr[i] = curr[1]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        num_recur_steps = steps - 1
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
                "steps": num_recur_steps,
                "elapsed_ms": elapsed_ms,
                "is_single_variable": model.is_single_variable,
                "is_frequency_model": getattr(
                    model, "is_frequency_model", False
                ),
            },
            success=True,
            message=(
                f"Discrete simulation complete ({num_recur_steps} steps in "
                f"{elapsed_ms:.1f} ms)"
            ),
        )

    # Continuous integration via solve_ivp
    if model.is_single_variable:
        def ode_system(t, y):
            """ODE right-hand side for single-species system."""
            clipped = np.array([max(0.0, y[0])], dtype=float)
            return model.rhs(t, clipped, params)

        y0 = [n1_init]
    else:
        def ode_system(t, y):
            """ODE right-hand side for two-species interactions."""
            clipped = np.array([max(0.0, y[0]), max(0.0, y[1])], dtype=float)
            return model.rhs(t, clipped, params)

        y0 = [n1_init, n2_init]

    try:
        sol = solve_ivp(
            fun=ode_system,
            t_span=valid_t_span,
            y0=y0,
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
                y0=y0,
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
                metadata={
                    "elapsed_ms": elapsed_ms,
                    "solver": ode_method,
                    "is_single_variable": model.is_single_variable,
                    "is_frequency_model": getattr(
                        model, "is_frequency_model", False
                    ),
                },
                success=False,
                message=f"Solver error: {sol.message}",
            )

        if getattr(model, "is_frequency_model", False):
            n1_res = np.clip(sol.y[0], 0.0, 1.0)
            n2_res = np.clip(1.0 - n1_res, 0.0, 1.0)
        else:
            n1_res = np.maximum(0.0, sol.y[0])
            n2_res = (
                np.zeros_like(n1_res)
                if model.is_single_variable
                else np.maximum(0.0, sol.y[1])
            )

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
                "is_single_variable": model.is_single_variable,
                "is_frequency_model": getattr(
                    model, "is_frequency_model", False
                ),
            },
            success=True,
            message=(
                f"Solved {len(sol.t)} time points in {elapsed_ms:.1f} ms"
            ),
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
            metadata={
                "elapsed_ms": elapsed_ms,
                "error": str(e),
                "is_frequency_model": getattr(
                    model, "is_frequency_model", False
                ),
            },
            success=False,
            message=f"Exception during simulation: {e}",
        )


def _format_csv_number(val: float) -> str:
    # Format numerical values cleanly with high scientific precision.
    if np.isnan(val) or np.isinf(val):
        return str(val)
    if abs(val) >= 1e-4 and abs(val) < 1e7 and val == int(val):
        return str(int(val))
    return f"{val:.8g}"


def export_simulation_to_csv(
    result: SimulationResult, target_path: str
) -> str:
    """Export simulation time-series data to a standard CSV file.

    Writes commented metadata headers (#) followed by tabular data
    columns for time and state variables.
    """
    abs_path = os.path.abspath(target_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    is_freq = result.metadata.get(
        "is_frequency_model", False
    ) or ("(p)" in result.n1_label and "(q)" in result.n2_label)
    is_single = result.metadata.get("is_single_variable", False)

    mode = result.metadata.get("mode", "continuous")
    param_str = ", ".join(
        f"{k}={v}" for k, v in result.parameters.items()
    )

    with open(abs_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        f.write("# BioModel Studio - Simulation Data Export\n")
        f.write(f"# Model: {result.model_name}\n")
        f.write(f"# Mode: {mode}\n")
        f.write(f"# Parameters: {param_str}\n")
        if is_freq:
            f.write(f"# Column p: {result.n1_label}\n")
            f.write(f"# Column q: {result.n2_label}\n")
            writer.writerow(["time", "p", "q"])
            for t_val, p_val, q_val in zip(
                result.t, result.n1, result.n2
            ):
                writer.writerow([
                    _format_csv_number(float(t_val)),
                    _format_csv_number(float(p_val)),
                    _format_csv_number(float(q_val)),
                ])
        elif is_single:
            f.write(f"# Column n: {result.n1_label}\n")
            writer.writerow(["time", "n"])
            for t_val, n_val in zip(result.t, result.n1):
                writer.writerow([
                    _format_csv_number(float(t_val)),
                    _format_csv_number(float(n_val)),
                ])
        else:
            f.write(f"# Column n1: {result.n1_label}\n")
            f.write(f"# Column n2: {result.n2_label}\n")
            writer.writerow(["time", "n1", "n2"])
            for t_val, n1_val, n2_val in zip(
                result.t, result.n1, result.n2
            ):
                writer.writerow([
                    _format_csv_number(float(t_val)),
                    _format_csv_number(float(n1_val)),
                    _format_csv_number(float(n2_val)),
                ])

    return abs_path
