"""model1b fine relational Gibbs state on the eight-site cycle `Gamma_2`.

Normative source: `docs/toy-models/toy1b/specification.md` §5, §8.

This module constructs the deterministic fine graph of eight declared fine
edges `AX, XY, YB, BC, CP, PQ, QD, DA` on the fixed fine site order
`(A, X, Y, B, C, P, Q, D)` (`cosmotgg.models.model1b.hierarchy`), the edge
datum `S_e(M_e) = 4 P_e(M_e) - I_e` for `M_e in U(2)` under the same
maximally-entangled orientation convention as the declared edge
(`fine_relational_hamiltonian`), and the fine relational Gibbs state
`rho_2 = exp(H_rel) / Tr[exp(H_rel)]` via the numerically stable common
spectral shift `H_shifted = H_rel - lambda_max I`
(`fine_relational_gibbs_state`, spec §8,
`COMMON_SPECTRAL_SHIFT_UNDER_NORMALIZATION = EXACT_IDENTITY`).

`theta_e` is a real, finite relational coupling parameter only: it is never
named/interpreted as a physical temperature, time, length, area, or
refinement scale (spec §8).

`MODEL1B_PRODUCTION_IMPORTS_PRIOR_MODELS = NO`: this module does not import
`cosmotgg.models.model0a`-`model0e`/`model1a` in production; the edge datum
construction below is written independently, even though it follows the
same standard maximally-entangled-edge mathematical form already used by
`model1a` (`docs/toy-models/toy1a/specification.md` §5, reference only).

This module builds no reduction, no modular datum, no directional/loop
diagnostic.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from cosmotgg.core.modular import hermitian_exp
from cosmotgg.core.states import embed_operator, validate_density_matrix
from cosmotgg.models.model1b.hierarchy import FINE_DIMENSIONS, FINE_SITE_ORDER

FINE_EDGES = ("AX", "XY", "YB", "BC", "CP", "PQ", "QD", "DA")

_SITE_POSITIONS = {label: index for index, label in enumerate(FINE_SITE_ORDER)}
_IDENTITY4 = np.eye(4, dtype=complex)


def _validate_real_finite_scalar(value, *, name: str) -> float:
    """Validate that `value` is a real, finite numeric scalar.

    Fail-closed (raise `ValueError`) on: `bool`/`numpy.bool_`, complex
    values, `NaN`, `+/-inf`, non-scalar arrays/sequences, and any other
    non-numeric type. No coercion beyond reading the already-numeric scalar
    value as `float`; no default value, no repair of an invalid input.
    Private, model-specific: not shared with any other model.
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


def _validate_tolerance(value, *, name: str) -> float:
    """Validate a real, finite, non-negative numeric scalar tolerance."""
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


def _validate_unitary_2x2(matrix, *, tolerance: float, name: str) -> np.ndarray:
    """Validate a `(2, 2)`, finite, unitary (within `tolerance`) matrix.

    Fail-closed (`ValueError`); no polar repair, no normalization repair, no
    QR repair, no nearest-unitary projection.
    """
    tol = _validate_tolerance(tolerance, name="max_entanglement_unitarity_tolerance")
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape != (2, 2):
        raise ValueError(f"{name} must have shape (2, 2), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    arr = arr.astype(complex, copy=False)
    identity = np.eye(2, dtype=complex)
    dev_left = np.max(np.abs(arr.conj().T @ arr - identity))
    dev_right = np.max(np.abs(arr @ arr.conj().T - identity))
    if dev_left > tol or dev_right > tol:
        raise ValueError(
            f"{name} is not unitary within max_entanglement_unitarity_tolerance={tol}: "
            f"max|M^dagger M - I|={dev_left}, max|M M^dagger - I|={dev_right}"
        )
    return arr


def _s_edge(m_matrix: np.ndarray) -> np.ndarray:
    """`S_e(M) = 4 |phi(M)><phi(M)| - I`, `phi(M) = (M/sqrt2)` flattened
    row-major (spec §8): standard maximally-entangled edge datum, written
    independently of `model1a` (`MODEL1B_PRODUCTION_IMPORTS_PRIOR_MODELS =
    NO`)."""
    phi = (m_matrix / np.sqrt(2.0)).reshape(4)
    p_edge = np.outer(phi, phi.conj())
    return 4.0 * p_edge - _IDENTITY4


def fine_relational_hamiltonian(
    thetas: Mapping[str, float],
    correlation_matrices: Mapping[str, np.ndarray],
    *,
    max_entanglement_unitarity_tolerance: float,
) -> np.ndarray:
    """`H_rel = sum_e theta_e S_e(M_e)` on the eight declared fine edges (spec §5, §8).

    `thetas` and `correlation_matrices` must each declare EXACTLY the eight
    fine edges `FINE_EDGES` as keys (missing, extra/unknown edge keys fail
    closed with `ValueError`; a Python `Mapping` cannot carry a duplicate
    key, so duplicate edge data is structurally excluded by this API).

    Each `theta_e` must be a real, finite, numeric scalar (`bool` rejected;
    no positivity requirement, spec §8: `theta_e` are finite real
    relational coupling parameters, `THETA != PHYSICAL_TEMPERATURE`).

    Each `M_e` must have shape `(2, 2)` and be unitary within
    `max_entanglement_unitarity_tolerance` (no default value); an invalid
    `M_e` fails closed with `ValueError` — no polar repair, no
    normalization repair, no QR repair, no nearest-unitary projection.

    For each edge `"XY"`, the operand `S_e(M_e)` (row/col order `(X, Y)`) is
    embedded via `cosmotgg.core.states.embed_operator` with
    `positions=(position of X, position of Y)`, i.e. in the operand's own
    declared factor order (spec §5: `AX, XY, YB, BC, CP, PQ, QD, DA`), in
    particular `positions=(position of D, position of A)` for the `DA`
    edge — never a silently reordered orientation.
    """
    declared = set(FINE_EDGES)
    theta_keys = set(thetas.keys())
    if theta_keys != declared:
        raise ValueError(
            f"thetas must declare exactly the fine edges {FINE_EDGES}, got {sorted(theta_keys)}"
        )
    m_keys = set(correlation_matrices.keys())
    if m_keys != declared:
        raise ValueError(
            "correlation_matrices must declare exactly the fine edges "
            f"{FINE_EDGES}, got {sorted(m_keys)}"
        )

    dim = 2 ** len(FINE_SITE_ORDER)
    h_rel = np.zeros((dim, dim), dtype=complex)
    for edge in FINE_EDGES:
        theta_v = _validate_real_finite_scalar(thetas[edge], name=f"thetas[{edge!r}]")
        m_v = _validate_unitary_2x2(
            correlation_matrices[edge],
            tolerance=max_entanglement_unitarity_tolerance,
            name=f"correlation_matrices[{edge!r}]",
        )
        site_1, site_2 = edge[0], edge[1]
        positions = (_SITE_POSITIONS[site_1], _SITE_POSITIONS[site_2])
        s_e = _s_edge(m_v)
        h_rel = h_rel + theta_v * embed_operator(
            s_e, dimensions=FINE_DIMENSIONS, positions=positions
        )
    return h_rel


def fine_relational_gibbs_state(
    h_rel,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`rho_2` via the numerically stable common spectral shift (spec §8).

        lambda_max = max eig(H_rel)
        H_shifted  = H_rel - lambda_max * I
        rho_2      = exp(H_shifted) / Tr[exp(H_shifted)]

    Mathematically identical, under normalization, to `exp(H_rel) /
    Tr[exp(H_rel)]` for any finite hermitian `H_rel`
    (`COMMON_SPECTRAL_SHIFT_UNDER_NORMALIZATION = EXACT_IDENTITY`, spec
    §8): the shift is exact numerical-stability bookkeeping, never a
    regularization, physical renormalization, or free parameter. No
    clipping, no pseudo-inverse, no arbitrary offset. `hermitian_exp`
    (`cosmotgg.core.modular`) itself applies no spectral shift; the shift
    is entirely this function's responsibility.

    `h_rel` must be a square `(256, 256)` array of finite entries and
    hermitian within `hermiticity_tolerance`; otherwise this function fails
    closed with `ValueError`. The final `rho_2` is validated fidele (`Tr =
    1`, PSD, strictly positive) via
    `cosmotgg.core.states.validate_density_matrix` with
    `require_faithful=True`.
    """
    arr = np.asarray(h_rel)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"h_rel must be a square 2D array, got shape={arr.shape}")
    expected_dim = 2 ** len(FINE_SITE_ORDER)
    if arr.shape[0] != expected_dim:
        raise ValueError(
            f"h_rel must have shape ({expected_dim}, {expected_dim}), got shape={arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError("h_rel must contain only finite values")
    arr = arr.astype(complex, copy=False)

    herm_tol = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")
    deviation = np.max(np.abs(arr - arr.conj().T))
    if deviation > herm_tol:
        raise ValueError(
            f"h_rel is not hermitian within hermiticity_tolerance={herm_tol}: "
            f"max|H_rel - H_rel^dagger| = {deviation}"
        )

    lambda_max = float(np.linalg.eigvalsh(arr)[-1])
    identity = np.eye(expected_dim, dtype=complex)
    h_shifted = arr - lambda_max * identity

    exp_shifted = hermitian_exp(h_shifted, hermiticity_tolerance=herm_tol)
    trace_value = float(np.trace(exp_shifted).real)
    rho_2 = exp_shifted / trace_value

    return validate_density_matrix(
        rho_2,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
