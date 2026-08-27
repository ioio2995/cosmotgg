"""toy1a projective loop holonomy, centered loop transfer, primary response candidate.

Normative source: `docs/toy-models/toy1a/specification.md` §15-§22, §25.

This module assembles the projective loop holonomy `H_A = M_AB
M_BC* M_CD M_DA*` and its phase-independent action `Ad_HA(X) = H_A X
H_A^dagger` (`projective_loop_holonomy`, `projective_loop_action`,
§15), using `M_DA` exactly in its canonical `D (x) A` orientation
(spec §4, §12): no silently mis-ordered `A (x) D` matrix is ever
substituted. It assembles the centered loop transfer directly from
state data (`state_derived_loop_transfer`, §17, no holonomy shortcut),
verified in tests against `L_square(X) = w_square Ad_HA(X)`. The
primary public API,
`relational_curvature_response_candidate` (§18,
`AMPLITUDE_WEIGHTED_PROJECTIVE_LOOP_RESPONSE`), derives edge strength
and correlation matrices structurally from the four supplied edge
states only (no independent `epsilon`/`M`/holonomy/loop-strength
argument is accepted), enforcing `G1 STATE_DERIVATION` by
construction.

This module never names a production function `riemann`,
`tidal_acceleration`, `geodesic_deviation`, or `gravity`; it imports no
`model0a`-`model0e` API and introduces no T1 change-direction object.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.models.model1a.links import (
    state_derived_centered_edge_transfer,
    state_derived_edge_link,
)


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


def _validate_hermitian_traceless_2x2(
    matrix, *, hermiticity_tolerance: float, trace_tolerance: float, name: str
) -> np.ndarray:
    herm_tol = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")
    trace_tol = _validate_tolerance(trace_tolerance, name="trace_tolerance")
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape != (2, 2):
        raise ValueError(f"{name} must have shape (2, 2), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    arr = arr.astype(complex, copy=False)
    herm_dev = np.max(np.abs(arr - arr.conj().T))
    if herm_dev > herm_tol:
        raise ValueError(
            f"{name} is not hermitian within hermiticity_tolerance={herm_tol}: "
            f"max|{name} - {name}^dagger| = {herm_dev}"
        )
    trace_dev = abs(np.trace(arr))
    if trace_dev > trace_tol:
        raise ValueError(
            f"{name} is not traceless within trace_tolerance={trace_tol}: "
            f"|Tr({name})| = {trace_dev}"
        )
    return arr


def projective_loop_holonomy(
    m_ab,
    m_bc,
    m_cd,
    m_da,
    *,
    max_entanglement_unitarity_tolerance: float,
) -> np.ndarray:
    """Projective loop holonomy `H_A = M_AB M_BC* M_CD M_DA*` (spec §15).

    Each `m_ij` must have shape `(2, 2)` and be unitary within
    `max_entanglement_unitarity_tolerance` (no default value). `m_da`
    MUST be supplied in its canonical `D (x) A` orientation (spec §4,
    §12): this function never substitutes a mis-ordered `A (x) D`
    matrix. The resulting `H_A` is validated unitary; no phase fixing
    is performed.
    """
    m_ab_v = _validate_unitary_2x2(m_ab, tolerance=max_entanglement_unitarity_tolerance, name="m_ab")
    m_bc_v = _validate_unitary_2x2(m_bc, tolerance=max_entanglement_unitarity_tolerance, name="m_bc")
    m_cd_v = _validate_unitary_2x2(m_cd, tolerance=max_entanglement_unitarity_tolerance, name="m_cd")
    m_da_v = _validate_unitary_2x2(m_da, tolerance=max_entanglement_unitarity_tolerance, name="m_da")

    holonomy = m_ab_v @ m_bc_v.conj() @ m_cd_v @ m_da_v.conj()
    holonomy = _validate_unitary_2x2(
        holonomy, tolerance=max_entanglement_unitarity_tolerance, name="holonomy"
    )
    return holonomy


def projective_loop_action(
    holonomy,
    tangent,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    max_entanglement_unitarity_tolerance: float,
) -> np.ndarray:
    """Phase-independent projective loop action `Ad_HA(X) = H_A X H_A^dagger` (spec §15).

    This induced action, not the raw scalar phase of `H_A`, carries the
    physical/projective information.
    """
    h_matrix = _validate_unitary_2x2(
        holonomy, tolerance=max_entanglement_unitarity_tolerance, name="holonomy"
    )
    x_matrix = _validate_hermitian_traceless_2x2(
        tangent, hermiticity_tolerance=hermiticity_tolerance, trace_tolerance=trace_tolerance, name="tangent"
    )
    return h_matrix @ x_matrix @ h_matrix.conj().T


def state_derived_loop_transfer(
    rho_ab,
    rho_bc,
    rho_cd,
    rho_da,
    tangent_a,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Centered loop transfer `L_square = L_(A<-B) o L_(B<-C) o L_(C<-D) o L_(D<-A)` (spec §17).

    Composed DIRECTLY from the four edge states (no holonomy shortcut
    inside this function): this is the independent state-space
    mechanism used to verify `L_square(X) = w_square Ad_HA(X)`.
    `rho_da` must already be supplied in its canonical `D (x) A`
    orientation (spec §4, §7).
    """
    edge_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    x_d = state_derived_centered_edge_transfer(rho_da, tangent_a, **edge_kwargs)
    x_c = state_derived_centered_edge_transfer(rho_cd, x_d, **edge_kwargs)
    x_b = state_derived_centered_edge_transfer(rho_bc, x_c, **edge_kwargs)
    x_a_returned = state_derived_centered_edge_transfer(rho_ab, x_b, **edge_kwargs)
    return x_a_returned


def relational_curvature_response_candidate(
    rho_ab,
    rho_bc,
    rho_cd,
    rho_da,
    tangent_a,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
    edge_spectral_tolerance: float,
    max_entanglement_unitarity_tolerance: float,
) -> np.ndarray:
    """Primary `model1a` response candidate `R_square(X) = w_square [Ad_HA(X) - X]` (spec §18).

    `AMPLITUDE_WEIGHTED_PROJECTIVE_LOOP_RESPONSE`: this API derives
    edge strength and correlation matrices STRUCTURALLY from the four
    supplied edge states only (`state_derived_edge_link` on each of
    `rho_ab`, `rho_bc`, `rho_cd`, `rho_da`); no independent `epsilon`,
    `M`, holonomy, or loop-strength argument is accepted
    (`G1 STATE_DERIVATION` enforced by construction). `rho_da` must
    already be in its canonical `D (x) A` orientation.

    `w_square = strength_ab * strength_bc * strength_cd * strength_da`;
    `H_A = projective_loop_holonomy(...)`. Returns `w_square * (H_A
    tangent_a H_A^dagger - tangent_a)`.
    """
    link_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
        edge_spectral_tolerance=edge_spectral_tolerance,
        max_entanglement_unitarity_tolerance=max_entanglement_unitarity_tolerance,
    )
    link_ab = state_derived_edge_link(rho_ab, **link_kwargs)
    link_bc = state_derived_edge_link(rho_bc, **link_kwargs)
    link_cd = state_derived_edge_link(rho_cd, **link_kwargs)
    link_da = state_derived_edge_link(rho_da, **link_kwargs)

    w_square = (
        link_ab["strength"] * link_bc["strength"] * link_cd["strength"] * link_da["strength"]
    )

    holonomy = projective_loop_holonomy(
        link_ab["correlation_matrix"],
        link_bc["correlation_matrix"],
        link_cd["correlation_matrix"],
        link_da["correlation_matrix"],
        max_entanglement_unitarity_tolerance=max_entanglement_unitarity_tolerance,
    )

    x_matrix = _validate_hermitian_traceless_2x2(
        tangent_a,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        name="tangent_a",
    )

    action = projective_loop_action(
        holonomy,
        x_matrix,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        max_entanglement_unitarity_tolerance=max_entanglement_unitarity_tolerance,
    )

    return w_square * (action - x_matrix)
