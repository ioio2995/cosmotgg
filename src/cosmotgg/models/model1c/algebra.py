"""model1c qubit Pauli stack, Bell generators, Bell projectors, `P_BELL`.

Normative source: `docs/toy-models/toy1c/specification.md` §5, §7 (closed
form only).

This module exposes the local qubit Pauli stack `{I, X, Y, Z}`
(`PAULI_STACK`), the four Bell generators `G_BELL = {II, XX, ZZ, YY}`
(spec §5) as explicit `(4, 4)` operators on the cell space `H_c = C^2 (x)
C^2`, the four rank-one standard-Bell-basis projectors `BELL_PROJECTORS`
(spec §5), and the closed-form Bell twirl

    P_BELL(rho) = 1/4 sum_g g rho g^dagger = sum_k Pi_k rho Pi_k

(spec §5, §7, `p_bell`/`p_bell_via_projectors`).

`p_bell` is an independent analytic oracle only (`ORACLE_ROLE =
INDEPENDENT_CROSS_CHECK_ONLY`): it is never called by the production path
of `R_cell`/`Phi`
(`cosmotgg.models.model1c.local_cell.local_refinement_cell`/`phi`), only
by `cosmotgg.models.model1c.oracle` and
`cosmotgg.models.model1c.diagnostics`.

This module builds no ancilla, no controlled unitary, no refinement rule.
"""

from __future__ import annotations

import numpy as np

_IDENTITY2 = np.eye(2, dtype=complex)
_SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
_SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# Local qubit Pauli stack {I, X, Y, Z}, index 0..3.
PAULI_STACK = np.stack([_IDENTITY2, _SIGMA_X, _SIGMA_Y, _SIGMA_Z], axis=0)

# Bell generators G_BELL = {II, XX, ZZ, YY} (spec §5), fixed order: this is
# the ancilla basis order used by `alpha`
# (`cosmotgg.models.model1c.local_cell.ALPHA`, diag(5/8, 1/8, 1/8, 1/8))
# and by the controlled unitary `U`
# (`cosmotgg.models.model1c.local_cell.controlled_bell_unitary`).
G_BELL_LABELS = ("II", "XX", "ZZ", "YY")

G_BELL = {
    "II": np.kron(_IDENTITY2, _IDENTITY2),
    "XX": np.kron(_SIGMA_X, _SIGMA_X),
    "ZZ": np.kron(_SIGMA_Z, _SIGMA_Z),
    "YY": np.kron(_SIGMA_Y, _SIGMA_Y),
}

G_BELL_ORDERED = tuple(G_BELL[label] for label in G_BELL_LABELS)

_INV_SQRT2 = 1.0 / np.sqrt(2.0)

# Standard Bell basis on H_c = C^2 (x) C^2, computational basis order
# |00>, |01>, |10>, |11> (spec §5): |Phi+>, |Phi->, |Psi+>, |Psi->. This is
# the standard maximally-entangled basis that jointly diagonalizes the
# Klein-four group G_BELL (spec §5, simultaneous eigenbasis, standard
# mathematical fact used in exact closed form, not rederived here).
_BELL_VECTORS = (
    _INV_SQRT2 * np.array([1.0, 0.0, 0.0, 1.0], dtype=complex),
    _INV_SQRT2 * np.array([1.0, 0.0, 0.0, -1.0], dtype=complex),
    _INV_SQRT2 * np.array([0.0, 1.0, 1.0, 0.0], dtype=complex),
    _INV_SQRT2 * np.array([0.0, 1.0, -1.0, 0.0], dtype=complex),
)

BELL_PROJECTORS = tuple(np.outer(v, v.conj()) for v in _BELL_VECTORS)


def _validate_square_operator(operator, *, dim: int, name: str) -> np.ndarray:
    """Fail-closed shape/finiteness check for a `(dim, dim)` operator.

    No hermiticity, trace, or positivity requirement is imposed here:
    `p_bell` is a linear map defined for any finite operator on `H_c`, not
    only for density matrices (spec §7's algebraic definition of `Phi` is
    not restricted to positive operators). Malformed input (wrong shape,
    non-finite entries) fails closed with `ValueError`; no coercion, no
    repair.
    """
    arr = np.asarray(operator)
    if arr.ndim != 2 or arr.shape != (dim, dim):
        raise ValueError(f"{name} must have shape ({dim}, {dim}), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr.astype(complex, copy=False)


def p_bell(rho) -> np.ndarray:
    """Closed-form Bell twirl `P_BELL(rho) = 1/4 sum_g g rho g^dagger` (spec §5, §7).

    Independent analytic oracle only (`ORACLE_ROLE =
    INDEPENDENT_CROSS_CHECK_ONLY`): never called by the production path of
    `cosmotgg.models.model1c.local_cell.local_refinement_cell`/`phi`.
    """
    arr = _validate_square_operator(rho, dim=4, name="rho")
    total = np.zeros((4, 4), dtype=complex)
    for g in G_BELL_ORDERED:
        total = total + g @ arr @ g.conj().T
    return total / 4.0


def p_bell_via_projectors(rho) -> np.ndarray:
    """`sum_k Pi_k rho Pi_k`, independent regression cross-check of `p_bell`
    against the simultaneous-Bell-eigenbasis form (spec §5, §7)."""
    arr = _validate_square_operator(rho, dim=4, name="rho")
    total = np.zeros((4, 4), dtype=complex)
    for pi in BELL_PROJECTORS:
        total = total + pi @ arr @ pi
    return total
