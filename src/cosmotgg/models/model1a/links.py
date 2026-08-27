"""toy1a state-derived directional link, phase firewall, reverse link, centered edge transfer.

Normative source: `docs/toy-models/toy1a/specification.md` §8-§14.

This module extracts, for a single declared edge, the state-derived
directional correlation link (`state_derived_edge_link`, §8-§10): the
modular Hamiltonian `K_ij = -ln(rho_ij)`, its unique minimal
eigenprojector (coinciding, for the declared family, with the unique
maximal eigenprojector of `rho_ij`), the edge relational strength
(spectral gap of `rho_ij`, §9), and the phase-independent correlation
matrix `M_ij` (§10). It exposes the primary directional action
`U_(i<-j)` on traceless Hermitian tangents (`apply_directional_link`,
§10), the reverse-link contract `M_ji = M_ij^T`
(`reverse_correlation_matrix`, §12), and the centered edge transfer
`L_(i<-j)(X) = 2 Tr_j[(I (x) X)(rho_ij - I/4)]`
(`state_derived_centered_edge_transfer`, §13), verified against the
frozen analytic identity `L = eps * U` in tests, never assumed in
production.

`DIRECTIONAL_CONNECTION = U`, `PHYSICAL_CENTERED_EDGE_TRANSFER = L = eps
U` (§13): "physical" here means derived from the relational strength
carried by the density matrix, not an established physical
process/channel/tidal observable. This module never names a production
function `*_physical_transfer*`.

This module builds no loop holonomy, no loop response
(`cosmotgg.models.model1a.loop`).
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import modular_hamiltonian
from cosmotgg.core.states import validate_density_matrix


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


def state_derived_edge_link(
    rho_ij,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
    edge_spectral_tolerance: float,
    max_entanglement_unitarity_tolerance: float,
) -> dict:
    """State-derived directional edge link (spec §8-§10).

    `rho_ij` must have shape `(4, 4)` and be a faithful density matrix
    (validated via `cosmotgg.core.states.validate_density_matrix`).
    `K_ij = modular_hamiltonian(rho_ij, ...)`. The declared family
    contract (§8) requires: (1) a unique largest eigenvalue of
    `rho_ij`; (2) its three orthogonal remaining eigenvalues mutually
    degenerate within `edge_spectral_tolerance`; (3) a unique minimum
    eigenvalue of `K_ij`; (4) the modular minimum eigenprojector agrees
    with the state maximum eigenprojector within
    `edge_spectral_tolerance`. Any violation fails closed with
    `ValueError` — no degeneracy repair.

    The edge relational strength is extracted ONLY from `rho_ij`'s
    spectrum: `strength = lambda_plus - lambda_minus` (spec §9). The
    directional correlation matrix is extracted from the modular
    ground-state coefficient: `M_ij = sqrt(2) * Psi_matrix`, where
    `Psi_matrix = psi.reshape((2, 2), order="C")` and `psi` is the
    modular ground eigenvector; `M_ij` must be unitary within
    `max_entanglement_unitarity_tolerance` (no default value) — no
    polar repair, no normalization repair, no QR repair, no
    nearest-unitary projection.

    Returns a `dict` with exactly the keys `modular_hamiltonian`,
    `modular_ground_projector`, `strength`, `correlation_matrix`. No
    PASS/FAIL score is returned: failure is exclusively signalled by
    `ValueError`.
    """
    rho_arr = np.asarray(rho_ij)
    if rho_arr.ndim != 2 or rho_arr.shape != (4, 4):
        raise ValueError(f"rho_ij must have shape (4, 4), got shape={rho_arr.shape}")

    validated_rho = validate_density_matrix(
        rho_arr,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )

    edge_spec_tol = _validate_tolerance(edge_spectral_tolerance, name="edge_spectral_tolerance")
    unitarity_tol = _validate_tolerance(
        max_entanglement_unitarity_tolerance, name="max_entanglement_unitarity_tolerance"
    )

    k_ij = modular_hamiltonian(
        validated_rho,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )

    eigvals_rho, eigvecs_rho = np.linalg.eigh(validated_rho)
    lower_gap_1 = eigvals_rho[1] - eigvals_rho[0]
    lower_gap_2 = eigvals_rho[2] - eigvals_rho[1]
    top_gap = eigvals_rho[3] - eigvals_rho[2]
    if not (abs(lower_gap_1) <= edge_spec_tol and abs(lower_gap_2) <= edge_spec_tol):
        raise ValueError(
            "rho_ij's three lower eigenvalues are not mutually degenerate within "
            f"edge_spectral_tolerance={edge_spec_tol}: eigenvalues={eigvals_rho}"
        )
    if not (top_gap > edge_spec_tol):
        raise ValueError(
            "rho_ij does not have a unique largest eigenvalue within "
            f"edge_spectral_tolerance={edge_spec_tol}: eigenvalues={eigvals_rho}"
        )

    lambda_plus = eigvals_rho[3]
    lambda_minus = (eigvals_rho[0] + eigvals_rho[1] + eigvals_rho[2]) / 3.0
    strength = float(lambda_plus - lambda_minus)

    eigvals_k, eigvecs_k = np.linalg.eigh(k_ij)
    k_bottom_gap = eigvals_k[1] - eigvals_k[0]
    if not (k_bottom_gap > edge_spec_tol):
        raise ValueError(
            "K_ij does not have a unique minimum eigenvalue within "
            f"edge_spectral_tolerance={edge_spec_tol}: eigenvalues={eigvals_k}"
        )

    top_state_vector = eigvecs_rho[:, -1]
    bottom_modular_vector = eigvecs_k[:, 0]

    modular_ground_projector = np.outer(bottom_modular_vector, bottom_modular_vector.conj())
    state_top_projector = np.outer(top_state_vector, top_state_vector.conj())

    consistency = np.max(np.abs(modular_ground_projector - state_top_projector))
    if consistency > edge_spec_tol:
        raise ValueError(
            "modular ground projector disagrees with state maximum projector beyond "
            f"edge_spectral_tolerance={edge_spec_tol}: max|difference|={consistency}"
        )

    psi_matrix = top_state_vector.reshape((2, 2), order="C")
    m_ij = np.sqrt(2.0) * psi_matrix
    m_ij = _validate_unitary_2x2(m_ij, tolerance=unitarity_tol, name="correlation_matrix")

    return {
        "modular_hamiltonian": k_ij,
        "modular_ground_projector": modular_ground_projector,
        "strength": strength,
        "correlation_matrix": m_ij,
    }


def apply_directional_link(
    correlation_matrix,
    tangent,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    max_entanglement_unitarity_tolerance: float,
) -> np.ndarray:
    """Primary directional connection action `U_(i<-j)(X) = M X^T M^dagger` (spec §10).

    `correlation_matrix` must have shape `(2, 2)` and be unitary within
    `max_entanglement_unitarity_tolerance`; `tangent` must have shape
    `(2, 2)`, be hermitian within `hermiticity_tolerance`, and traceless
    within `trace_tolerance`. The exact operation is `M @ X.T @
    M.conj().T` (the transpose contract, NOT `M @ X.conj() @ ...`, even
    though hermiticity of `X` numerically relates the two).
    """
    m_matrix = _validate_unitary_2x2(
        correlation_matrix, tolerance=max_entanglement_unitarity_tolerance, name="correlation_matrix"
    )
    x_matrix = _validate_hermitian_traceless_2x2(
        tangent, hermiticity_tolerance=hermiticity_tolerance, trace_tolerance=trace_tolerance, name="tangent"
    )
    return m_matrix @ x_matrix.T @ m_matrix.conj().T


def reverse_correlation_matrix(correlation_matrix, *, max_entanglement_unitarity_tolerance: float) -> np.ndarray:
    """Reverse-link correlation matrix `M_ji = M_ij^T` (spec §12).

    No independent eigendecomposition of `rho_ji` is performed: the
    reverse matrix is derived algebraically from the same edge datum.
    """
    m_matrix = _validate_unitary_2x2(
        correlation_matrix, tolerance=max_entanglement_unitarity_tolerance, name="correlation_matrix"
    )
    return m_matrix.T


def state_derived_centered_edge_transfer(
    rho_ij,
    tangent,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Centered edge transfer `L_(i<-j)(X) = 2 Tr_j[(I (x) X)(rho_ij - I/4)]` (spec §13).

    Computed DIRECTLY from `rho_ij` (no `M`/`epsilon` argument). `rho_ij`
    must have shape `(4, 4)` and be a faithful density matrix; `tangent`
    (`X_j`) must have shape `(2, 2)`, be hermitian within
    `hermiticity_tolerance`, and traceless within `trace_tolerance`. No
    normalization is applied. The frozen analytic identity `L = eps *
    U` (spec §13) is an independent property verified by tests, never
    assumed here.
    """
    rho_arr = np.asarray(rho_ij)
    if rho_arr.ndim != 2 or rho_arr.shape != (4, 4):
        raise ValueError(f"rho_ij must have shape (4, 4), got shape={rho_arr.shape}")

    validated_rho = validate_density_matrix(
        rho_arr,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    x_matrix = _validate_hermitian_traceless_2x2(
        tangent, hermiticity_tolerance=hermiticity_tolerance, trace_tolerance=trace_tolerance, name="tangent"
    )

    identity4 = np.eye(4, dtype=complex)
    centered = validated_rho - identity4 / 4.0
    op = np.kron(np.eye(2, dtype=complex), x_matrix) @ centered
    tensor = op.reshape(2, 2, 2, 2)  # (row_i, row_j, col_i, col_j)
    reduced = np.einsum("ikjk->ij", tensor)  # trace over j (second factor)
    result = 2.0 * reduced

    if not np.all(np.isfinite(result)):
        raise ValueError("state_derived_centered_edge_transfer produced non-finite output")
    return result
