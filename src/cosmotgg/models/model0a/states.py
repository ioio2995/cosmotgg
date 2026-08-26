"""toy0a canonical state family: `TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY`.

Normative source: `docs/toy-models/toy0a/specification.md` §3.

This module constructs the state family `rho_AB(a, b, c, eta)` on
`H_A ⊗ H_B = C^2 ⊗ C^2` and validates its exact analytic domain (§3.2)
fail-closed. It does not reimplement any generic primitive already
available in `cosmotgg.core`: no matrix logarithm, no modular
Hamiltonian, no cocycle, no mutual information, no partial trace. A
consumer obtains marginals via `cosmotgg.core.states.partial_trace` and
`sigma_AB = rho_A ⊗ rho_B` via `numpy.kron`, directly, as designed by
`docs/toy-models/toy0a/implementation-design.md` §2, §4.

The analytic domain of §3.2 is the sole normative definition of
faithfulness for this family: it is neither approximated nor relaxed by
a numerical tolerance local to this module (`NUMERICAL_TOLERANCES`
remains `OPEN` at the `cosmotgg.core` protocol level; see
`docs/toy-models/toy0a/specification.md` §15). Any parameter outside
this exact domain is rejected fail-closed with `ValueError`; the
constructor never repairs, clips, symmetrizes, or otherwise corrects an
out-of-domain input.
"""

from __future__ import annotations

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


def two_qubit_fixed_marginal_correlation_state(a, b, c, eta) -> np.ndarray:
    """Canonical two-qubit, fixed-marginal correlation state `rho_AB(a,b,c,eta)`.

    In the basis `|00>, |01>, |10>, |11>`, returns exactly:

        [[ a*b+c,          0,              0,          eta          ],
         [ 0,               a*(1-b)-c,     0,          0            ],
         [ 0,               0,              (1-a)*b-c, 0            ],
         [ eta,              0,              0,          (1-a)*(1-b)+c]]

    (`docs/toy-models/toy0a/specification.md` §3), as a complex
    `numpy.ndarray` of shape `(4, 4)`, for `core` compatibility.

    Domain (§3.2 of the specification, normative, all inequalities
    strict, no tolerance, no epsilon, no clipping):

        0 < a < 1
        0 < b < 1
        lower_c < c < upper_c
            where lower_c = -min(a*b, (1-a)*(1-b))
                  upper_c =  min(a*(1-b), (1-a)*b)
        eta**2 < (a*b + c) * ((1-a)*(1-b) + c)

    Any `a, b, c, eta` outside this exact domain is rejected fail-closed
    with `ValueError`; no value is corrected or clipped into range. The
    `eta` bound is evaluated as `abs(eta) < sqrt(block_product)` (a
    numerically safer, mathematically equivalent form of
    `eta**2 < block_product` that avoids squaring `eta` unnecessarily);
    this is not a relaxation of the domain, and `block_product` is
    strictly positive whenever `a, b, c` already satisfy the domain
    above, so the square root is always well-defined here.

    `a`, `b`, `c`, `eta` must each be a real, finite numeric scalar
    (see `_validate_real_finite_scalar`); `bool`, complex values, `NaN`,
    `+/-inf`, non-scalar values, and non-numeric types are rejected
    fail-closed.

    Fixed exact marginals (§3.1 of the specification, not verified by
    this function beyond the domain check above, but relied upon by
    consumers): `rho_A = diag(a, 1-a)`, `rho_B = diag(b, 1-b)`,
    independently of `c` and `eta`.

    This function performs no `cosmotgg.core.states.validate_density_matrix`
    call with an invented numerical tolerance: the exact analytic domain
    above already guarantees hermiticity, unit trace, and faithfulness
    mathematically. Numerical validation with explicit tolerances (e.g.
    via `validate_density_matrix`) is left to consumers/protocols, which
    supply their own explicit, non-default tolerances.
    """
    a_value = _validate_real_finite_scalar(a, name="a")
    b_value = _validate_real_finite_scalar(b, name="b")
    c_value = _validate_real_finite_scalar(c, name="c")
    eta_value = _validate_real_finite_scalar(eta, name="eta")

    if not (0.0 < a_value < 1.0):
        raise ValueError(f"a must satisfy 0 < a < 1, got {a_value}")
    if not (0.0 < b_value < 1.0):
        raise ValueError(f"b must satisfy 0 < b < 1, got {b_value}")

    lower_c = -min(a_value * b_value, (1.0 - a_value) * (1.0 - b_value))
    upper_c = min(a_value * (1.0 - b_value), (1.0 - a_value) * b_value)
    if not (lower_c < c_value < upper_c):
        raise ValueError(
            f"c must satisfy {lower_c} < c < {upper_c} for a={a_value}, "
            f"b={b_value}, got {c_value}"
        )

    block_product = (a_value * b_value + c_value) * (
        (1.0 - a_value) * (1.0 - b_value) + c_value
    )
    if not (abs(eta_value) < np.sqrt(block_product)):
        raise ValueError(
            f"eta must satisfy eta**2 < {block_product} for a={a_value}, "
            f"b={b_value}, c={c_value}, got eta={eta_value}"
        )

    rho_ab = np.zeros((4, 4), dtype=complex)
    rho_ab[0, 0] = a_value * b_value + c_value
    rho_ab[1, 1] = a_value * (1.0 - b_value) - c_value
    rho_ab[2, 2] = (1.0 - a_value) * b_value - c_value
    rho_ab[3, 3] = (1.0 - a_value) * (1.0 - b_value) + c_value
    rho_ab[0, 3] = eta_value
    rho_ab[3, 0] = eta_value

    return rho_ab
