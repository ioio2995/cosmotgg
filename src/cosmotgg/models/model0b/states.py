"""toy0b canonical state family: `THREE_QUBIT_OVERLAPPING_PAULI_RELATION_FAMILY`.

Normative source: `docs/toy-models/toy0b/specification.md` §5–§7.

This module constructs the state family `rho_ABC(beta, lambda_, mu)` on
`H_A ⊗ H_B ⊗ H_C = C^2 ⊗ C^2 ⊗ C^2` and validates its exact analytic
domain (§6) fail-closed. It does not reimplement any generic primitive
already available in `cosmotgg.core`: no matrix logarithm, no modular
Hamiltonian, no partial trace, no conditional expectation. A consumer
obtains the reduced states of §7 (`rho_AB`, `rho_BC`, `rho_B`, `rho_A`,
`rho_C`) directly via `cosmotgg.core.states.partial_trace`, as designed
by `docs/toy-models/toy0b/implementation-design.md` §5.

The analytic domain of §6 (`beta**2 + lambda**2 + mu**2 < 1`) is the
sole normative definition of faithfulness for this family: it is
neither approximated nor relaxed by a numerical tolerance local to this
module (`NUMERICAL_TOLERANCES` remains `OPEN` at the `cosmotgg.core`
protocol level; see `docs/toy-models/toy0b/specification.md` §23). Any
parameter outside this exact domain is rejected fail-closed with
`ValueError`; the constructor never repairs, clips, symmetrizes, or
otherwise corrects an out-of-domain input.
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


def three_qubit_overlapping_pauli_relation_state(beta, lambda_, mu) -> np.ndarray:
    """Canonical three-qubit, overlapping Pauli relation state `rho_ABC(beta, lambda_, mu)`.

    In the computational basis `|abc>` of `H_A ⊗ H_B ⊗ H_C`
    (`docs/toy-models/toy0b/specification.md` §5):

        rho_ABC = 1/8 * [I + beta*Z_B + lambda_*X_A X_B + mu*Y_B Y_C]

    where `Z_B`, `X_A X_B`, `Y_B Y_C` denote the full three-qubit
    operators with identities on the unwritten factors (e.g. `Z_B`
    denotes `I_A ⊗ Z_B ⊗ I_C`). Returned as a complex `numpy.ndarray` of
    shape `(8, 8)`, for `core` compatibility, with tensor order `A, B,
    C` and each qubit in the standard computational basis.

    Domain (§6 of the specification, normative, strict inequality, no
    tolerance, no epsilon, no clipping):

        beta**2 + lambda_**2 + mu**2 < 1

    Any `beta, lambda_, mu` outside this exact domain is rejected
    fail-closed with `ValueError`; no value is corrected or clipped into
    range. The bound is evaluated via `math.hypot(beta, lambda_, mu) < 1`,
    a numerically robust Euclidean norm that avoids unnecessary overflow
    on large finite inputs while testing exactly the same mathematical
    condition as squaring and summing directly; this is not a relaxation
    of the domain.

    `beta`, `lambda_`, `mu` must each be a real, finite numeric scalar
    (see `_validate_real_finite_scalar`); `bool`, complex values, `NaN`,
    `+/-inf`, non-scalar values, and non-numeric types are rejected
    fail-closed.

    This function performs no `cosmotgg.core.states.validate_density_matrix`
    call with an invented numerical tolerance: the exact analytic domain
    above already guarantees hermiticity, unit trace, and faithfulness
    mathematically (§6 of the specification: spectrum `(1+r)/8` with
    multiplicity 4, `(1-r)/8` with multiplicity 4, `r = sqrt(beta**2 +
    lambda_**2 + mu**2) < 1`). Numerical validation with explicit
    tolerances (e.g. via `validate_density_matrix`) is left to
    consumers/protocols, which supply their own explicit, non-default
    tolerances.
    """
    beta_value = _validate_real_finite_scalar(beta, name="beta")
    lambda_value = _validate_real_finite_scalar(lambda_, name="lambda_")
    mu_value = _validate_real_finite_scalar(mu, name="mu")

    if not (math.hypot(beta_value, lambda_value, mu_value) < 1.0):
        raise ValueError(
            "beta, lambda_, mu must satisfy beta**2 + lambda_**2 + mu**2 < 1, "
            f"got beta={beta_value}, lambda_={lambda_value}, mu={mu_value}"
        )

    identity2 = np.eye(2, dtype=complex)
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

    z_b = np.kron(identity2, np.kron(pauli_z, identity2))
    x_a_x_b = np.kron(pauli_x, np.kron(pauli_x, identity2))
    y_b_y_c = np.kron(identity2, np.kron(pauli_y, pauli_y))

    identity8 = np.eye(8, dtype=complex)
    return (identity8 + beta_value * z_b + lambda_value * x_a_x_b + mu_value * y_b_y_c) / 8.0
