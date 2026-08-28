"""model1b canonical modular datum, full Pauli support, and global two-body block.

Normative source: `docs/toy-models/toy1b/specification.md` §9-§11.

This module exposes the canonical scale datum `K_n = -log(rho_n)`
(`modular_datum`, delegated entirely to
`cosmotgg.core.modular.modular_hamiltonian`, spec §9,
`CANONICAL_SCALE_DATUM = FULL_K_n`), the complete qubit Pauli support
decomposition `c_s(K_n) = 2^-N Tr[K_n P_s]` and its weight-graded norms
`W_w(K_n)` (spec §10, bookkeeping diagnostics only, `PAIR_DATA_IS_
CANONICAL_SCALE_DATUM = NO`), and the global modular two-body block
`J_{i<-j}^{ab}(K_n) = -2^-N Tr[K_n sigma_a^(i) sigma_b^(j)]` for every
ordered pair of surviving sites (spec §11, `PAIR_BLOCK = DERIVED_
DIAGNOSTIC_FROM_FULL_K`, `PAIR_BLOCK != CANONICAL_DATUM`).

`Tr[K_n sigma_a^(i) sigma_b^(j)]` is real by construction for hermitian
`K_n` and hermitian Pauli factors: `global_two_body_block` returns a real
(not complex) `(3, 3)` array, taking the exact real part of this
mathematically real trace (an exact algebraic identity, not a numerical
approximation or repair).

For `N` surviving qubits, the full Pauli coefficient tensor has `4**N`
entries (spec §10, `PAIR_TRUNCATION_CLOSED_UNDER_FLOW = TESTED, NOT
ASSUMED`); no coefficient sector is ever silently discarded. For `N = 8`
(the finest declared level, spec §6), this module never constructs the
`4**8` individual dense `256 x 256` Pauli matrices: the coefficient tensor
and its reconstruction are computed by a single tensorized `numpy.einsum`
contraction against the eight `(4, 2, 2)` local Pauli stacks, one leg pair
per site, instead.

This module builds no directional polar factor, no loop object
(`cosmotgg.models.model1b.directional`).
"""

from __future__ import annotations

import string

import numpy as np

from cosmotgg.core.modular import modular_hamiltonian
from cosmotgg.core.states import embed_operator

_IDENTITY2 = np.eye(2, dtype=complex)
_SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
_SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# Local Pauli stack {I, X, Y, Z}, index 0..3 (spec §10: sigma_0 = I,
# sigma_{1,2,3} the Pauli matrices).
PAULI_STACK = np.stack([_IDENTITY2, _SIGMA_X, _SIGMA_Y, _SIGMA_Z], axis=0)

_MAX_QUBITS_FOR_EINSUM_LABELS = len(string.ascii_lowercase) // 3


def modular_datum(
    rho_n,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`K_n = -log(rho_n)`, the full canonical scale datum (spec §9).

    Delegates entirely to `cosmotgg.core.modular.modular_hamiltonian`; no
    reimplementation of the hermitian logarithm, no support truncation.
    """
    return modular_hamiltonian(
        rho_n,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )


def _validate_k_matrix(k_matrix, n_sites: int, *, name: str) -> np.ndarray:
    arr = np.asarray(k_matrix)
    expected_dim = 2 ** n_sites
    if arr.ndim != 2 or arr.shape != (expected_dim, expected_dim):
        raise ValueError(
            f"{name} must have shape ({expected_dim}, {expected_dim}) for "
            f"n_sites={n_sites}, got shape={arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr.astype(complex, copy=False)


def _einsum_letters(n_sites: int) -> tuple[str, str, str]:
    if n_sites > _MAX_QUBITS_FOR_EINSUM_LABELS:
        raise ValueError(
            "full Pauli support decomposition supports at most "
            f"{_MAX_QUBITS_FOR_EINSUM_LABELS} qubits with this implementation, "
            f"got n_sites={n_sites}"
        )
    letters = string.ascii_lowercase
    row_letters = letters[0:n_sites]
    col_letters = letters[n_sites : 2 * n_sites]
    s_letters = letters[2 * n_sites : 3 * n_sites]
    return row_letters, col_letters, s_letters


def modular_pauli_coefficients(k_matrix, n_sites: int) -> np.ndarray:
    """Full Pauli coefficient tensor `c_s(K_n) = 2^-N Tr[K_n P_s]` (spec §10).

    `k_matrix` must have shape `(2**n_sites, 2**n_sites)`. Returns a complex
    array of shape `(4,) * n_sites`, one entry per Pauli string `s`, `s_i in
    {0, 1, 2, 3}` indexing `{I, X, Y, Z}` (`PAULI_STACK`). Every coefficient
    is retained (`PAIR_TRUNCATION_CLOSED_UNDER_FLOW = TESTED, NOT ASSUMED`).

    Computed by a single tensorized `numpy.einsum` contraction of the
    `k_matrix` reshaped into a rank-`2*n_sites` tensor against the `n_sites`
    local `(4, 2, 2)` Pauli stacks (one leg-pair contraction per site);
    the `4**n_sites` dense `256 x 256`-sized Pauli matrices are never
    constructed for `n_sites = 8`.
    """
    arr = _validate_k_matrix(k_matrix, n_sites, name="k_matrix")
    row_letters, col_letters, s_letters = _einsum_letters(n_sites)

    k_tensor = arr.reshape((2,) * (2 * n_sites))
    operand_subscripts = [row_letters + col_letters]
    operands = [k_tensor]
    for i in range(n_sites):
        # Tr[K P_s] = sum_{r,c} K[r,c] P_s[c,r]: each local Pauli factor is
        # contracted in (col, row) order against K's (row, col) legs, not
        # (row, col), since Tr[AB] = sum_{a,b} A[a,b] B[b,a].
        operand_subscripts.append(s_letters[i] + col_letters[i] + row_letters[i])
        operands.append(PAULI_STACK)
    einsum_str = ",".join(operand_subscripts) + "->" + s_letters

    coefficients = np.einsum(einsum_str, *operands, optimize=True)
    return coefficients / (2 ** n_sites)


def support_weights(coefficient_tensor) -> np.ndarray:
    """Integer array of support weights `w(s)`, same shape as
    `coefficient_tensor` (spec §10): number of non-identity local factors
    per Pauli string multi-index."""
    arr = np.asarray(coefficient_tensor)
    n_sites = arr.ndim
    weight = np.zeros(arr.shape, dtype=int)
    for axis in range(n_sites):
        shape = [1] * n_sites
        shape[axis] = 4
        axis_weight = (np.arange(4) != 0).astype(int).reshape(shape)
        weight = weight + axis_weight
    return weight


def support_weight_norms(coefficient_tensor) -> dict[int, float]:
    """`W_w(K_n) = sqrt(sum_{w(s)=w} |c_s|^2)` for every weight `w` (spec §10).

    Bookkeeping diagnostic only (`W_w != PHYSICAL_DISTANCE`, `W_w !=
    CURVATURE`, `W_4 != CURVATURE`). Returns a `dict` with keys `0 ..
    n_sites` (`n_sites = coefficient_tensor.ndim`).
    """
    arr = np.asarray(coefficient_tensor)
    n_sites = arr.ndim
    weight = support_weights(arr)
    magnitudes_squared = np.abs(arr) ** 2
    norms = {}
    for w in range(n_sites + 1):
        mask = weight == w
        norms[w] = float(np.sqrt(np.sum(magnitudes_squared[mask])))
    return norms


def reconstruct_from_pauli_coefficients(coefficient_tensor) -> np.ndarray:
    """`K = sum_s c_s P_s`, full reconstruction from the complete
    decomposition (spec §10, T5F5 support: the decomposition must be able to
    reconstruct the complete `K_n`, never only a truncated projection).
    """
    arr = np.asarray(coefficient_tensor)
    n_sites = arr.ndim
    row_letters, col_letters, s_letters = _einsum_letters(n_sites)

    operand_subscripts = [s_letters]
    operands = [arr]
    for i in range(n_sites):
        operand_subscripts.append(s_letters[i] + row_letters[i] + col_letters[i])
        operands.append(PAULI_STACK)
    einsum_str = ",".join(operand_subscripts) + "->" + row_letters + col_letters

    tensor = np.einsum(einsum_str, *operands, optimize=True)
    dim = 2 ** n_sites
    return tensor.reshape(dim, dim)


def global_two_body_block(k_matrix, n_sites: int, site_i: int, site_j: int) -> np.ndarray:
    """Global modular two-body block `J_{i<-j}^{ab}(K_n)` (spec §11).

        J_{i<-j}^{ab} = -2^-N Tr[K_n sigma_a^(i) sigma_b^(j)],  a, b in {x, y, z}

    Derived directly from the FULL `k_matrix` (`n_sites`-qubit algebra);
    no pair-state shortcut. Rows correspond to `sigma_a` at `site_i`,
    columns to `sigma_b` at `site_j` (`site_i`, `site_j` are 0-based
    positions into the `n_sites`-site algebra of `k_matrix`, ordered `x, y,
    z` -> row/column index `0, 1, 2`). `site_i == site_j` or an out-of-range
    position fails closed with `ValueError`.

    Returns a real (not complex) `(3, 3)` array: `Tr[K_n sigma_a^(i)
    sigma_b^(j)]` is real by construction for hermitian `K_n` and hermitian
    Pauli factors (an exact algebraic identity, not a numerical repair).
    `PAIR_BLOCK = DERIVED_DIAGNOSTIC_FROM_FULL_K`, `PAIR_BLOCK !=
    CANONICAL_DATUM`.
    """
    if site_i == site_j:
        raise ValueError(f"site_i and site_j must differ, got site_i=site_j={site_i}")
    if not (0 <= site_i < n_sites) or not (0 <= site_j < n_sites):
        raise ValueError(
            f"site_i, site_j must be valid positions in [0, {n_sites}), "
            f"got ({site_i}, {site_j})"
        )
    arr = _validate_k_matrix(k_matrix, n_sites, name="k_matrix")
    dim = 2 ** n_sites
    dimensions = (2,) * n_sites

    j_block = np.zeros((3, 3), dtype=complex)
    for a in range(1, 4):
        for b in range(1, 4):
            op4 = np.kron(PAULI_STACK[a], PAULI_STACK[b])
            embedded = embed_operator(op4, dimensions=dimensions, positions=(site_i, site_j))
            j_block[a - 1, b - 1] = -np.trace(arr @ embedded) / dim

    # Tr[K_n sigma_a^(i) sigma_b^(j)] is real by construction (hermitian
    # operand): the residual complex128 imaginary part is ordinary
    # floating-point roundoff, not scientific content, so it is dropped
    # here exactly as a typing/bookkeeping step, never as a numerical
    # repair of a mathematically genuine complex quantity.
    return j_block.real
