"""toy0c canonical state family: `THREE_QUBIT_NONCOLLINEAR_OVERLAP_RELATION_FAMILY`.

Normative source: `docs/toy-models/toy0c/specification.md` §5–§7.

This module constructs the state family `rho_ABC(alpha, gamma, lambda_,
mu)` on `H_A ⊗ H_B ⊗ H_C = C^2 ⊗ C^2 ⊗ C^2` and validates its exact
analytic domain (§6) fail-closed. It does not reimplement any generic
primitive already available in `cosmotgg.core`: no matrix logarithm,
no modular Hamiltonian, no partial trace, no conditional expectation.
A consumer obtains the reduced states of §7 (`rho_AB`, `rho_BC`,
`rho_B`, `rho_A`, `rho_C`) directly via
`cosmotgg.core.states.partial_trace`, as designed by
`docs/toy-models/toy0c/implementation-design.md` §6.

The analytic domain of §6 (`abs(alpha) + abs(gamma) + hypot(lambda_,
mu) < 1`) is the sole normative definition of faithfulness for this
family: it is neither approximated nor relaxed by a numerical
tolerance local to this module (`NUMERICAL_TOLERANCES` remains `OPEN`
at the `cosmotgg.core` protocol level; see
`docs/toy-models/toy0c/specification.md` §23). Any parameter outside
this exact domain is rejected fail-closed with `ValueError`; the
constructor never repairs, clips, symmetrizes, or otherwise corrects
an out-of-domain input.
"""

from __future__ import annotations

import math

import numpy as np


def _validate_real_finite_scalar(value, *, name: str) -> float:
    """Validate that `value` is a real, finite numeric scalar.

    Fail-closed (raise `ValueError`) on: `bool`/`numpy.bool_`, complex
    values, `NaN`, `+inf`, `-inf`, non-scalar arrays/sequences, and any
    other non-numeric type (e.g. `str`). No coercion is performed beyond
    reading the already-numeric scalar value as `float`; there is no
    default value and no repair of an invalid input.

    Private, model-specific: not imported from `cosmotgg.models.model0b`
    or any other model.
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


def three_qubit_noncollinear_overlap_relation_state(alpha, gamma, lambda_, mu) -> np.ndarray:
    """Canonical three-qubit, noncollinear overlap relation state `rho_ABC(alpha, gamma, lambda_, mu)`.

    In the computational basis `|abc>` of `H_A ⊗ H_B ⊗ H_C`
    (`docs/toy-models/toy0c/specification.md` §5), tensor order `A, B,
    C`:

        rho_ABC = 1/8 * [I + alpha*X_A + gamma*Z_C + lambda_*X_A X_B + mu*Y_B Z_C]

    where `X_A`, `Z_C`, `X_A X_B`, `Y_B Z_C` denote the full
    three-qubit operators with identities on the unwritten factors
    (e.g. `X_A` denotes `X_A ⊗ I_B ⊗ I_C`). Returned as a complex
    `numpy.ndarray` of shape `(8, 8)`, for `core` compatibility, with
    each qubit in the standard computational basis.

    Domain (§6 of the specification, normative, strict inequality, no
    tolerance, no epsilon, no clipping):

        abs(alpha) + abs(gamma) + sqrt(lambda_**2 + mu**2) < 1

    Any `alpha, gamma, lambda_, mu` outside this exact domain is
    rejected fail-closed with `ValueError`; no value is corrected or
    clipped into range. The bound is evaluated via
    `abs(alpha) + abs(gamma) + math.hypot(lambda_, mu) < 1`, using
    `math.hypot` for the Euclidean norm of `(lambda_, mu)` as a
    numerically robust alternative to `sqrt(lambda_**2 + mu**2)` that
    avoids unnecessary overflow on large finite inputs while testing
    exactly the same mathematical condition; this is not a relaxation
    of the domain.

    `alpha`, `gamma`, `lambda_`, `mu` must each be a real, finite
    numeric scalar (see `_validate_real_finite_scalar`); `bool`,
    complex values, `NaN`, `+/-inf`, non-scalar values, and non-numeric
    types are rejected fail-closed.

    This function performs no `cosmotgg.core.states.validate_density_matrix`
    call with an invented numerical tolerance: the exact analytic domain
    above already guarantees hermiticity, unit trace, and faithfulness
    mathematically (§6 of the specification: spectrum
    `(1 + alpha*x + gamma*z +/- hypot(lambda_, mu)) / 8` for `x, z in
    {-1, +1}`). Numerical validation with explicit tolerances (e.g. via
    `validate_density_matrix`) is left to consumers/protocols, which
    supply their own explicit, non-default tolerances.
    """
    alpha_value = _validate_real_finite_scalar(alpha, name="alpha")
    gamma_value = _validate_real_finite_scalar(gamma, name="gamma")
    lambda_value = _validate_real_finite_scalar(lambda_, name="lambda_")
    mu_value = _validate_real_finite_scalar(mu, name="mu")

    radius = abs(alpha_value) + abs(gamma_value) + math.hypot(lambda_value, mu_value)
    if not (radius < 1.0):
        raise ValueError(
            "alpha, gamma, lambda_, mu must satisfy abs(alpha) + abs(gamma) + "
            f"hypot(lambda_, mu) < 1, got alpha={alpha_value}, gamma={gamma_value}, "
            f"lambda_={lambda_value}, mu={mu_value} (radius={radius})"
        )

    identity2 = np.eye(2, dtype=complex)
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

    x_a = np.kron(pauli_x, np.kron(identity2, identity2))
    z_c = np.kron(identity2, np.kron(identity2, pauli_z))
    x_a_x_b = np.kron(pauli_x, np.kron(pauli_x, identity2))
    y_b_z_c = np.kron(identity2, np.kron(pauli_y, pauli_z))

    identity8 = np.eye(8, dtype=complex)
    return (
        identity8
        + alpha_value * x_a
        + gamma_value * z_c
        + lambda_value * x_a_x_b
        + mu_value * y_b_z_c
    ) / 8.0
