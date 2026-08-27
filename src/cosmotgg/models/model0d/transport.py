"""toy0d finite relative contextual-state transport.

Normative source: `docs/toy-models/toy0d/specification.md` §5, §7,
§15.

This module reconstructs an auxiliary contextual state `omega_X` from
a projected relative modular generator `chi_X` (§5,
`contextual_state_from_projected_generator`), assembles the finite
relative contextual-state transporter `F` between two such contextual
states (§7, `finite_relative_contextual_state_transporter`), and
exposes non-normative numerical qualification guards for that
transporter (§15,
`finite_relative_contextual_state_transport_guards`).

`omega` is an auxiliary contextual state, not a reduced physical state
of `B`: `omega_X` is reconstructed from the projected generator
`chi_X`, distinct from the reduced state `rho_B` of the overlap
algebra (specification §5).

`FINITE_TRANSFORM_STATUS = FINITE_RELATIVE_STATE_TRANSPORT_ONLY`
(specification §2, §7): this module constructs and names nothing
beyond a finite, directed, invertible transport between two contextual
states.

The transporter `F` is assembled by delegating entirely to
`cosmotgg.core.modular.connes_cocycle_at_minus_i_half` (the analytic
half-point of the Connes cocycle, `[D rho : D sigma]_(-i/2) =
rho^(1/2) sigma^(-1/2)`); this module never recomputes
`sqrt(omega_target) @ inverse_sqrt(omega_source)` locally.

No real scalar parameter is exposed anywhere in this module
(`FINITE_FLOW_PARAMETER_PROBLEM = OPEN`, specification §18, §20): this
module implements neither a parameterized unitary family nor any
generic transport framework.

`model0d` does not import `cosmotgg.models.model0c` in production
(`MODEL0D_PRODUCTION_IMPORTS_MODEL0C = NO`,
`docs/toy-models/toy0d/implementation-design.md` §4, §11): this module
accepts any hermitian, finite `chi` on a common finite-dimensional
overlap algebra, with no assumption on its upstream provenance.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import connes_cocycle_at_minus_i_half


def _validate_tolerance(value, *, name: str) -> float:
    """Validate a real, finite, non-negative numeric scalar tolerance.

    Local, private duplicate of the tolerance contract already enforced
    by `cosmotgg.core` (explicit, keyword-only, no default, finite,
    non-negative): kept private and local to this module so that
    `model0d` never imports a private symbol of `cosmotgg.core`.
    """
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a real numeric scalar, not bool: got {value!r}")

    arr = np.asarray(value)
    if arr.ndim != 0:
        raise ValueError(f"{name} must be a scalar, got shape={arr.shape}")
    if not np.issubdtype(arr.dtype, np.number):
        raise ValueError(
            f"{name} must be a real numeric scalar, got {type(value).__name__}: {value!r}"
        )
    if np.iscomplexobj(arr):
        raise ValueError(f"{name} must be real, not complex: got {value!r}")

    scalar = float(arr)
    if not np.isfinite(scalar):
        raise ValueError(f"{name} must be finite, got {scalar}")
    if scalar < 0.0:
        raise ValueError(f"{name} must be >= 0, got {scalar}")
    return scalar


def contextual_state_from_projected_generator(
    chi,
    *,
    hermiticity_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Auxiliary contextual state `omega = exp(-chi) / Tr(exp(-chi))` (spec §5).

    `chi` is a projected relative modular generator: a square, finite,
    hermitian (within `hermiticity_tolerance`) operator on a common
    finite-dimensional overlap algebra `B`. `chi` is NOT required to be
    positive, and is NOT required to be a density matrix (`Tr(chi) = 0`
    is the upstream scientific convention, spec §5, but is not
    re-validated here with a hidden tolerance: any finite hermitian
    `chi` is accepted, and any additive scalar part of `chi` disappears
    exactly under normalization, spec §5-§6).

    `omega` is an auxiliary contextual state, not a reduced physical
    state of `B`.

    Computed via a numerically stable common eigenvalue shift, exact
    under normalization (spec §5): diagonalize `chi = V diag(k)
    V^dagger` (`numpy.linalg.eigh`), shift `shifted = k - min(k)`,
    weight `w = exp(-shifted)`, normalize `p = w / sum(w)`,
    reconstruct `omega = V diag(p) V^dagger`. This shift is an exact
    algebraic identity under normalization (`exp(-(chi - c*I)) /
    Tr(...) == exp(-chi) / Tr(...)`), not a clipping, regularization,
    or repair. No `scipy` dependency is used.

    After reconstruction, `omega`'s eigenvalues (exactly `p` above)
    must satisfy `lambda_min > positivity_tolerance`; otherwise this
    function fails closed with `ValueError` (spec §15,
    `BOUNDARY_REGIME = OUT_OF_SCOPE_FOR_MODEL0D_QUALIFICATION`). No
    clipping, no individual eigenvalue renormalization, no
    pseudoinverse, no ridge is ever applied.

    `hermiticity_tolerance`, `positivity_tolerance` are explicit,
    keyword-only, with no default value.
    """
    hermiticity_tol = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")
    positivity_tol = _validate_tolerance(positivity_tolerance, name="positivity_tolerance")

    chi_arr = np.asarray(chi)
    if chi_arr.ndim != 2 or chi_arr.shape[0] != chi_arr.shape[1]:
        raise ValueError(f"chi must be a square 2D array, got shape={chi_arr.shape}")
    if chi_arr.shape[0] == 0:
        raise ValueError("chi must have a nonzero dimension")
    if not np.all(np.isfinite(chi_arr)):
        raise ValueError("chi must contain only finite values")

    chi_arr = chi_arr.astype(complex, copy=False)
    deviation = np.max(np.abs(chi_arr - chi_arr.conj().T))
    if deviation > hermiticity_tol:
        raise ValueError(
            "chi is not hermitian within hermiticity_tolerance="
            f"{hermiticity_tol}: max |chi - chi^dagger| = {deviation}"
        )

    eigvals, eigvecs = np.linalg.eigh(chi_arr)
    shifted = eigvals - np.min(eigvals)
    weights = np.exp(-shifted)
    normalized_weights = weights / np.sum(weights)

    lambda_min = np.min(normalized_weights)
    if not (lambda_min > positivity_tol):
        raise ValueError(
            "reconstructed contextual state omega is not faithful within "
            f"positivity_tolerance={positivity_tol}: minimal eigenvalue={lambda_min}"
        )

    return (eigvecs * normalized_weights) @ eigvecs.conj().T


def finite_relative_contextual_state_transporter(
    omega_source,
    omega_target,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Finite relative contextual-state transporter `F` (spec §7).

    For faithful contextual states `omega_source`, `omega_target` on
    the same finite-dimensional overlap algebra `B`:

        F = omega_target^(1/2) @ omega_source^(-1/2)
          = connes_cocycle_at_minus_i_half(omega_target, omega_source)

    i.e. `F @ omega_source @ F.conj().T == omega_target` exactly. This
    is entirely delegated to
    `cosmotgg.core.modular.connes_cocycle_at_minus_i_half`: this
    function never recomputes `sqrt(omega_target) @
    inverse_sqrt(omega_source)` locally. `hermiticity_tolerance`,
    `trace_tolerance`, `positivity_tolerance` are forwarded unchanged;
    non-faithfulness, non-hermiticity, bad trace, or mismatched
    dimensions of `omega_source`/`omega_target` all fail closed with
    `ValueError`, delegated entirely to
    `connes_cocycle_at_minus_i_half`.

    `omega_source`, `omega_target` are auxiliary contextual states, not
    reduced physical states of `B`. No real scalar parameter is
    exposed by this function.
    """
    return connes_cocycle_at_minus_i_half(
        omega_target,
        omega_source,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )


def finite_relative_contextual_state_transport_guards(
    omega_source,
    omega_target,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> dict[str, float]:
    """Non-normative numerical qualification guards for `F` (spec §15).

    Returns a `dict` with (at least) the following keys, each a plain
    `float` computed via `numpy.linalg.norm`/`numpy.linalg.eigvalsh`,
    with no additional normalization:

        lambda_min_source
        lambda_min_target
        sqrt_inverse_residual_source
        transport_residual
        inverse_residual

    exactly as defined by the specification (§15): `lambda_min_source`
    / `lambda_min_target` are the minimal eigenvalues of
    `omega_source` / `omega_target`;
    `sqrt_inverse_residual_source = ||
    connes_cocycle_at_minus_i_half(omega_source, omega_source) - I ||`;
    `transport_residual = || F_st @ omega_source @ F_st.conj().T -
    omega_target ||`; `inverse_residual = || F_ts @ F_st - I ||`, where
    `F_st = finite_relative_contextual_state_transporter(omega_source,
    omega_target, ...)` and `F_ts =
    finite_relative_contextual_state_transporter(omega_target,
    omega_source, ...)`.

    These are `NUMERICAL_QUALIFICATION_GUARDS`, not physical
    observables and not scientific scores: this function applies no
    threshold, no PASS/FAIL verdict, and never modifies
    `omega_source`/`omega_target`. `analytic_oracle_residual` (spec
    §15) is intentionally not exposed here: it requires an external
    analytic oracle specific to a `d_B = 2` test fixture, and remains
    test/notebook-only.
    """
    core_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )

    f_source_to_target = finite_relative_contextual_state_transporter(
        omega_source, omega_target, **core_kwargs
    )
    f_target_to_source = finite_relative_contextual_state_transporter(
        omega_target, omega_source, **core_kwargs
    )
    sqrt_inverse_check = connes_cocycle_at_minus_i_half(omega_source, omega_source, **core_kwargs)

    omega_source_arr = np.asarray(omega_source, dtype=complex)
    omega_target_arr = np.asarray(omega_target, dtype=complex)
    identity = np.eye(omega_source_arr.shape[0], dtype=complex)

    lambda_min_source = float(np.min(np.linalg.eigvalsh(omega_source_arr)))
    lambda_min_target = float(np.min(np.linalg.eigvalsh(omega_target_arr)))

    sqrt_inverse_residual_source = float(np.linalg.norm(sqrt_inverse_check - identity))
    transport_residual = float(
        np.linalg.norm(
            f_source_to_target @ omega_source_arr @ f_source_to_target.conj().T
            - omega_target_arr
        )
    )
    inverse_residual = float(np.linalg.norm(f_target_to_source @ f_source_to_target - identity))

    return {
        "lambda_min_source": lambda_min_source,
        "lambda_min_target": lambda_min_target,
        "sqrt_inverse_residual_source": sqrt_inverse_residual_source,
        "transport_residual": transport_residual,
        "inverse_residual": inverse_residual,
    }
