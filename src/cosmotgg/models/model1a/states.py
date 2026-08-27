"""toy1a maximally-entangled edge data, global state, and reductions.

Normative source: `docs/toy-models/toy1a/specification.md` §4-§7.

This module constructs the canonical maximally-entangled edge data
(`|Phi+>`, `P_ij`, `S_ij`, §5), the four-qubit even closed relational
loop state family
`four_qubit_relational_loop_state(eps_AB, eps_BC, eps_CD, eps_DA,
M_AB, M_BC, M_CD, M_DA, *, ...)` on `H_A (x) H_B (x) H_C (x) H_D =
C^2 (x) C^2 (x) C^2 (x) C^2` (§6), validates its declared sufficient
faithful domain fail-closed without tolerance (§6), and exposes its
reductions (§7) via `cosmotgg.core.states.partial_trace`, with an
explicit permutation ("SWAP") of the `D (x) A` edge to its canonical
tensor orientation (§4, §7).

No spatial/metric interpretation is attached to any embedding or
reduction: "loop" designates a purely relational incidence structure
(§4).
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import partial_trace, validate_density_matrix

_DIMENSIONS = (2, 2, 2, 2)
_IDENTITY2 = np.eye(2, dtype=complex)
_IDENTITY4 = np.eye(4, dtype=complex)
_IDENTITY16 = np.eye(16, dtype=complex)

# Canonical Bell state |Phi+> = (|00>+|11>)/sqrt(2), index = 2*i+j.
_PHI_PLUS = np.zeros(4, dtype=complex)
_PHI_PLUS[0] = 1.0 / np.sqrt(2.0)
_PHI_PLUS[3] = 1.0 / np.sqrt(2.0)


def _validate_real_finite_scalar(value, *, name: str) -> float:
    """Validate that `value` is a real, finite numeric scalar.

    Fail-closed (raise `ValueError`) on `bool`/`numpy.bool_`, complex,
    `NaN`, `+/-inf`, non-scalar, or non-numeric input. Private,
    model-specific.
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

    Fail-closed (`ValueError`); no polar repair, no normalization
    repair, no QR repair, no nearest-unitary projection.
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


def _phi_from_m(m_matrix: np.ndarray) -> np.ndarray:
    """`|Phi(M)> = (M (x) I)|Phi+>`; coefficient matrix is `M/sqrt(2)` (spec §5)."""
    return (m_matrix / np.sqrt(2.0)).reshape(4)


def _s_edge(m_matrix: np.ndarray) -> np.ndarray:
    """`S_ij = 4 P_ij - I_ij` for the edge datum determined by `M_ij` (spec §5)."""
    phi = _phi_from_m(m_matrix)
    p_edge = np.outer(phi, phi.conj())
    return 4.0 * p_edge - _IDENTITY4


def _embed_ab(op_ab: np.ndarray) -> np.ndarray:
    return np.kron(op_ab, np.kron(_IDENTITY2, _IDENTITY2))


def _embed_bc(op_bc: np.ndarray) -> np.ndarray:
    return np.kron(_IDENTITY2, np.kron(op_bc, _IDENTITY2))


def _embed_cd(op_cd: np.ndarray) -> np.ndarray:
    return np.kron(_IDENTITY2, np.kron(_IDENTITY2, op_cd))


def _embed_da(op_da: np.ndarray) -> np.ndarray:
    """Explicit `Embed_DA` matrix-element oracle (spec §6):

        [Embed_DA(O)]_{(a,b,c,d),(a',b',c',d')} = O_{(d,a),(d',a')} * delta_bb' * delta_cc'

    `op_da` is given in `(D, A)` row/col order. No implicit `kron`
    reordering trick is used: every global matrix element is assigned
    explicitly from the oracle above.
    """
    tensor = op_da.reshape(2, 2, 2, 2)  # (row_D, row_A, col_D, col_A)
    full = np.zeros((2, 2, 2, 2, 2, 2, 2, 2), dtype=complex)
    for a in range(2):
        for a_prime in range(2):
            for d in range(2):
                for d_prime in range(2):
                    value = tensor[d, a, d_prime, a_prime]
                    if value == 0:
                        continue
                    for b in range(2):
                        for c in range(2):
                            full[a, b, c, d, a_prime, b, c, d_prime] = value
    return full.reshape(16, 16)


def _swap_pair_order(op_xy: np.ndarray) -> np.ndarray:
    """Explicit `SWAP` permutation of a `(4, 4)` operator from `(X, Y)` to
    `(Y, X)` row/col order (spec §7: `rho_AD = SWAP rho_DA SWAP`)."""
    tensor = op_xy.reshape(2, 2, 2, 2)  # (rowX, rowY, colX, colY)
    swapped = np.transpose(tensor, (1, 0, 3, 2))  # (rowY, rowX, colY, colX)
    return swapped.reshape(4, 4)


def four_qubit_relational_loop_state(
    eps_ab,
    eps_bc,
    eps_cd,
    eps_da,
    m_ab,
    m_bc,
    m_cd,
    m_da,
    *,
    max_entanglement_unitarity_tolerance: float,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Four-qubit even closed relational loop state `rho_ABCD` (spec §6).

    In the fixed tensor order `A, B, C, D`, with each declared edge
    (`AB`, `BC`, `CD`, `DA`) represented in its own canonical tensor
    orientation (spec §4):

        rho_ABCD = 1/16 [
            I
            + eps_AB * Embed_AB(S_AB)
            + eps_BC * Embed_BC(S_BC)
            + eps_CD * Embed_CD(S_CD)
            + eps_DA * Embed_DA(S_DA)
        ]

    `Embed_AB`, `Embed_BC`, `Embed_CD` coincide with the global tensor
    order (direct embedding); `Embed_DA` is the explicit matrix-element
    oracle of spec §6 (the `D (x) A` edge is never silently reordered
    via an implicit `kron` trick).

    Each `eps_ij` must be a real, finite, numeric scalar (`bool`
    rejected), strictly `> 0` (declared production branch, spec §6).
    The sufficient faithful-domain bound `3*(eps_AB+eps_BC+eps_CD+eps_DA)
    < 1` is checked EXACTLY, with no tolerance. Each `m_ij` must have
    shape `(2, 2)`, be finite, and unitary within
    `max_entanglement_unitarity_tolerance` (no default value); an
    invalid `m_ij` fails closed with `ValueError` — no polar repair, no
    normalization repair, no QR repair, no nearest-unitary projection.

    `hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`
    are explicit, keyword-only, with no default value, used exclusively
    for the final numerical validation of the constructed matrix via
    `cosmotgg.core.states.validate_density_matrix` with
    `require_faithful=True` (never for the exact domain/branch checks
    above).
    """
    eps_ab_v = _validate_real_finite_scalar(eps_ab, name="eps_ab")
    eps_bc_v = _validate_real_finite_scalar(eps_bc, name="eps_bc")
    eps_cd_v = _validate_real_finite_scalar(eps_cd, name="eps_cd")
    eps_da_v = _validate_real_finite_scalar(eps_da, name="eps_da")

    for name, value in (
        ("eps_ab", eps_ab_v),
        ("eps_bc", eps_bc_v),
        ("eps_cd", eps_cd_v),
        ("eps_da", eps_da_v),
    ):
        if not (value > 0.0):
            raise ValueError(f"{name} must satisfy {name} > 0, got {value}")

    bound = 3.0 * (eps_ab_v + eps_bc_v + eps_cd_v + eps_da_v)
    if not (bound < 1.0):
        raise ValueError(
            "parameters must satisfy the strict sufficient faithful-domain bound "
            f"3*(eps_ab+eps_bc+eps_cd+eps_da) < 1, got bound={bound}"
        )

    unitarity_tol = max_entanglement_unitarity_tolerance
    m_ab_v = _validate_unitary_2x2(m_ab, tolerance=unitarity_tol, name="m_ab")
    m_bc_v = _validate_unitary_2x2(m_bc, tolerance=unitarity_tol, name="m_bc")
    m_cd_v = _validate_unitary_2x2(m_cd, tolerance=unitarity_tol, name="m_cd")
    m_da_v = _validate_unitary_2x2(m_da, tolerance=unitarity_tol, name="m_da")

    s_ab = _s_edge(m_ab_v)
    s_bc = _s_edge(m_bc_v)
    s_cd = _s_edge(m_cd_v)
    s_da = _s_edge(m_da_v)

    rho = (1.0 / 16.0) * (
        _IDENTITY16
        + eps_ab_v * _embed_ab(s_ab)
        + eps_bc_v * _embed_bc(s_bc)
        + eps_cd_v * _embed_cd(s_cd)
        + eps_da_v * _embed_da(s_da)
    )

    return validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )


def four_qubit_relational_loop_reductions(rho_abcd) -> dict[str, np.ndarray]:
    """Reductions of `rho_ABCD` (spec §7).

    `rho_abcd` must be a square `(16, 16)` array of finite entries;
    otherwise this function fails closed with `ValueError`. Each
    reduction is obtained via `cosmotgg.core.states.partial_trace` on
    the declared `(2, 2, 2, 2)` `A, B, C, D` factorization; no analytic
    shortcut is used.

    `rho_da` is returned in its canonical `D (x) A` tensor orientation
    (spec §4, §7): `partial_trace` naturally returns the `keep=[0, 3]`
    pair in `A (x) D` order (the global tensor order), so this function
    explicitly permutes ("SWAP") that result to `D (x) A` before
    returning it. No silent assumption is made about the index-order
    convention of `partial_trace`.

    Returns a `dict` with exactly the keys `rho_ab`, `rho_bc`, `rho_cd`,
    `rho_da`, `rho_a`, `rho_b`, `rho_c`, `rho_d`, `rho_ac`, `rho_bd`.
    """
    arr = np.asarray(rho_abcd)
    if arr.ndim != 2 or arr.shape != (16, 16):
        raise ValueError(f"rho_abcd must have shape (16, 16), got shape={arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("rho_abcd must contain only finite values")
    arr = arr.astype(complex, copy=False)

    rho_ab = partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 1])
    rho_bc = partial_trace(arr, dimensions=_DIMENSIONS, keep=[1, 2])
    rho_cd = partial_trace(arr, dimensions=_DIMENSIONS, keep=[2, 3])
    rho_ad_natural = partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 3])  # natural A(x)D order
    rho_da = _swap_pair_order(rho_ad_natural)  # explicit permutation to D(x)A

    rho_a = partial_trace(arr, dimensions=_DIMENSIONS, keep=[0])
    rho_b = partial_trace(arr, dimensions=_DIMENSIONS, keep=[1])
    rho_c = partial_trace(arr, dimensions=_DIMENSIONS, keep=[2])
    rho_d = partial_trace(arr, dimensions=_DIMENSIONS, keep=[3])

    rho_ac = partial_trace(arr, dimensions=_DIMENSIONS, keep=[0, 2])
    rho_bd = partial_trace(arr, dimensions=_DIMENSIONS, keep=[1, 3])

    return {
        "rho_ab": rho_ab,
        "rho_bc": rho_bc,
        "rho_cd": rho_cd,
        "rho_da": rho_da,
        "rho_a": rho_a,
        "rho_b": rho_b,
        "rho_c": rho_c,
        "rho_d": rho_d,
        "rho_ac": rho_ac,
        "rho_bd": rho_bd,
    }
