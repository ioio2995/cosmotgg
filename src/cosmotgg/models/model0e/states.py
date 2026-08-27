"""toy0e canonical qutrit representative, state family, and reductions.

Normative source: `docs/toy-models/toy0e/specification.md` §6-§9.

This module constructs the canonical qutrit representative (`|Phi3>`,
`S_AB`, `N`, `|q0>`, `Q`, §6), the `FOUR_PARTITE_DISCRETE_MULTIMODULAR_
REFERENCE_FAMILY` state `rho_ABCD(eta, gamma, mu_A, mu_B, delta, nu_A,
nu_B)` on `H_A (x) H_B (x) H_C (x) H_D = C^3 (x) C^3 (x) C^2 (x) C^2`
(§7), validates its declared sufficient faithful domain and branch
conditions fail-closed without tolerance (§8), and exposes its
reductions (§9) via `cosmotgg.core.states.partial_trace`. It does not
reimplement any generic primitive already available in `cosmotgg.core`.

The canonical representative constants of §6 (`Q`, `N`, `|q0>`, ...) are
private to this module: the specification explicitly requires that no
preferred-basis claim is made at the public API level (§6, "Important").

This module builds no modular context, no reference extraction, no
conditional state (`cosmotgg.models.model0e.reference`,
`cosmotgg.models.model0e.conditional`).
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import partial_trace, validate_density_matrix

_DIMENSIONS = (3, 3, 2, 2)

_IDENTITY2 = np.eye(2, dtype=complex)
_IDENTITY3 = np.eye(3, dtype=complex)
_PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# Canonical qutrit representative (specification §6). Private: no
# preferred-basis claim is made at the public API level.
_Q0 = np.ones(3, dtype=complex) / np.sqrt(3.0)
_Q = np.outer(_Q0, _Q0.conj()) - _IDENTITY3 / 3.0
_N = np.diag([-1.0, 0.0, 1.0]).astype(complex)

_PHI3 = np.zeros(9, dtype=complex)
for _i in range(3):
    _PHI3[_i * 3 + _i] = 1.0 / np.sqrt(3.0)
_P_PHI = np.outer(_PHI3, _PHI3.conj())
_S_AB = 9.0 * _P_PHI - np.eye(9, dtype=complex)


def _validate_real_finite_scalar(value, *, name: str) -> float:
    """Validate that `value` is a real, finite numeric scalar.

    Fail-closed (raise `ValueError`) on: `bool`/`numpy.bool_`, complex
    values, `NaN`, `+/-inf`, non-scalar arrays/sequences, and any other
    non-numeric type. No coercion beyond reading the already-numeric
    scalar value as `float`; no default value, no repair of an invalid
    input. Private, model-specific: not shared with any other model.
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
    return scalar


def _embed(op: np.ndarray, which: int) -> np.ndarray:
    """Embed a local operator acting on subsystem `which` (0=A,1=B,2=C,3=D)
    into the full `A (x) B (x) C (x) D` space, identity elsewhere."""
    mats = []
    for index, dimension in enumerate(_DIMENSIONS):
        if index == which:
            mats.append(op)
        else:
            mats.append(np.eye(dimension, dtype=complex))
    result = mats[0]
    for mat in mats[1:]:
        result = np.kron(result, mat)
    return result


def four_partite_discrete_multimodular_reference_state(
    eta,
    gamma,
    mu_a,
    mu_b,
    delta,
    nu_a,
    nu_b,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Canonical state `rho_ABCD(eta, gamma, mu_A, mu_B, delta, nu_A, nu_B)` (spec §7).

    In the fixed tensor order `A, B, C, D`:

        rho_ABCD = 1/36 [
            I
            + eta * S_AB
            + gamma * Z_C
            + (mu_A Q_A + mu_B Q_B) * Z_C
            + delta * Z_D
            + (nu_A N_A + nu_B N_B) * Z_D
        ]

    assembled by explicit tensor-product combination (no analytic
    shortcut), where `Q_A = Q_B = Q`, `N_A = N_B = N` are the private
    canonical qutrit representative of §6, and `Z_C`, `Z_D` are the
    Pauli `Z` convention already used by `docs/toy-models/toy0b/
    specification.md`/`docs/toy-models/toy0c/specification.md`.

    All seven state parameters must be real, finite, numeric scalars
    (`bool` rejected). The declared branch conditions of §8 are then
    checked EXACTLY, with no tolerance and no epsilon (`NO_TOLERANCE`,
    `NO_EPSILON`, `BOUNDARY_REJECTED`):

        eta > 0,  gamma >= 0,  mu_A > 0,  mu_B > 0,
        delta > 0,  0 < nu_A < delta,  0 < nu_B < delta

    and the sufficient (deliberately non-tight) faithful-domain bound:

        8|eta| + |gamma| + (2/3)(|mu_A|+|mu_B|) + |delta| + |nu_A|+|nu_B| < 1

    strictly. Any parameter outside this domain is rejected fail-closed
    with `ValueError`; nothing is corrected, clipped, or repaired.

    `hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`
    are explicit, keyword-only, with no default value; they are used
    exclusively for the final numerical validation of the constructed
    matrix via `cosmotgg.core.states.validate_density_matrix` with
    `require_faithful=True` (never for the exact branch/domain checks
    above).
    """
    eta_v = _validate_real_finite_scalar(eta, name="eta")
    gamma_v = _validate_real_finite_scalar(gamma, name="gamma")
    mu_a_v = _validate_real_finite_scalar(mu_a, name="mu_a")
    mu_b_v = _validate_real_finite_scalar(mu_b, name="mu_b")
    delta_v = _validate_real_finite_scalar(delta, name="delta")
    nu_a_v = _validate_real_finite_scalar(nu_a, name="nu_a")
    nu_b_v = _validate_real_finite_scalar(nu_b, name="nu_b")

    if not (eta_v > 0.0):
        raise ValueError(f"eta must satisfy eta > 0, got {eta_v}")
    if not (gamma_v >= 0.0):
        raise ValueError(f"gamma must satisfy gamma >= 0, got {gamma_v}")
    if not (mu_a_v > 0.0):
        raise ValueError(f"mu_a must satisfy mu_a > 0, got {mu_a_v}")
    if not (mu_b_v > 0.0):
        raise ValueError(f"mu_b must satisfy mu_b > 0, got {mu_b_v}")
    if not (delta_v > 0.0):
        raise ValueError(f"delta must satisfy delta > 0, got {delta_v}")
    if not (0.0 < nu_a_v < delta_v):
        raise ValueError(f"nu_a must satisfy 0 < nu_a < delta, got nu_a={nu_a_v}, delta={delta_v}")
    if not (0.0 < nu_b_v < delta_v):
        raise ValueError(f"nu_b must satisfy 0 < nu_b < delta, got nu_b={nu_b_v}, delta={delta_v}")

    bound = (
        8.0 * abs(eta_v)
        + abs(gamma_v)
        + (2.0 / 3.0) * (abs(mu_a_v) + abs(mu_b_v))
        + abs(delta_v)
        + abs(nu_a_v)
        + abs(nu_b_v)
    )
    if not (bound < 1.0):
        raise ValueError(
            "parameters must satisfy the strict sufficient faithful-domain bound "
            "8|eta|+|gamma|+(2/3)(|mu_a|+|mu_b|)+|delta|+|nu_a|+|nu_b| < 1, "
            f"got bound={bound}"
        )

    q_a_full = _embed(_Q, 0)
    q_b_full = _embed(_Q, 1)
    n_a_full = _embed(_N, 0)
    n_b_full = _embed(_N, 1)
    z_c_full = _embed(_PAULI_Z, 2)
    z_d_full = _embed(_PAULI_Z, 3)
    s_ab_full = np.kron(np.kron(_S_AB, _IDENTITY2), _IDENTITY2)
    identity36 = np.eye(36, dtype=complex)

    rho = (1.0 / 36.0) * (
        identity36
        + eta_v * s_ab_full
        + gamma_v * z_c_full
        + mu_a_v * (q_a_full @ z_c_full)
        + mu_b_v * (q_b_full @ z_c_full)
        + delta_v * z_d_full
        + nu_a_v * (n_a_full @ z_d_full)
        + nu_b_v * (n_b_full @ z_d_full)
    )

    return validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )


def four_partite_discrete_multimodular_reductions(rho_abcd) -> dict[str, np.ndarray]:
    """Reductions of `rho_ABCD` (spec §9): `rho_AB, rho_A, rho_B, rho_AC, rho_AD, rho_BC, rho_BD`.

    `rho_abcd` must be a square `(36, 36)` array of finite entries;
    otherwise this function fails closed with `ValueError`. Each
    reduction is obtained via `cosmotgg.core.states.partial_trace` on
    the declared `(3, 3, 2, 2)` `A, B, C, D` factorization; no analytic
    shortcut is used in this production reduction.

    Returns a `dict` with exactly the keys `rho_ab`, `rho_a`, `rho_b`,
    `rho_ac`, `rho_ad`, `rho_bc`, `rho_bd`.
    """
    arr = np.asarray(rho_abcd)
    if arr.ndim != 2 or arr.shape != (36, 36):
        raise ValueError(f"rho_abcd must have shape (36, 36), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("rho_abcd must contain only finite values")
    arr = arr.astype(complex, copy=False)

    return {
        "rho_ab": partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 1]),
        "rho_a": partial_trace(arr, dimensions=_DIMENSIONS, keep=[0]),
        "rho_b": partial_trace(arr, dimensions=_DIMENSIONS, keep=[1]),
        "rho_ac": partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 2]),
        "rho_ad": partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 3]),
        "rho_bc": partial_trace(arr, dimensions=_DIMENSIONS, keep=[1, 2]),
        "rho_bd": partial_trace(arr, dimensions=_DIMENSIONS, keep=[1, 3]),
    }
