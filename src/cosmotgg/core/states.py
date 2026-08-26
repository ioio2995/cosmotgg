"""Generic finite-dimensional quantum state primitives.

This module provides model-independent primitives for finite-dimensional
density matrices: structural/numerical validation and partial trace over an
arbitrary finite tensor product of subsystems. Nothing here encodes a
particular CosmoTGG model, named state, dimension, or protocol threshold.

All numerical tolerances accepted by the public functions of this module are
explicit, keyword-only, and have no default value: a caller (typically a
model or protocol) must always provide them.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}


# ---------------------------------------------------------------------------
# Internal auxiliaries shared across cosmotgg.core (states / information /
# modular). Factored here to avoid duplicating shape, hermiticity, trace and
# positivity checks in every module. Not part of the public API.
# ---------------------------------------------------------------------------


def _validate_square_hermitian(
    matrix, *, hermiticity_tolerance: float, name: str
) -> np.ndarray:
    """Validate a finite, square, 2D, hermitian array and return it as complex.

    Checks performed: 2D shape, square shape, nonzero dimension, finite
    values, hermiticity within `hermiticity_tolerance`. The returned array
    has the same numerical values as the input, only cast to complex dtype
    for uniform downstream linear algebra; no value is corrected,
    symmetrized, or renormalized.
    """
    arr = np.asarray(matrix)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be a 2D array, got ndim={arr.ndim}")
    if arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be square, got shape={arr.shape}")
    if arr.shape[0] == 0:
        raise ValueError(f"{name} must have a nonzero dimension")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")

    arr = arr.astype(complex, copy=False)
    deviation = np.max(np.abs(arr - arr.conj().T))
    if deviation > hermiticity_tolerance:
        raise ValueError(
            f"{name} is not hermitian within hermiticity_tolerance="
            f"{hermiticity_tolerance}: max |M - M^dagger| = {deviation}"
        )
    return arr


def _hermitian_eigendecomposition(
    matrix, *, hermiticity_tolerance: float, name: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Validate hermiticity then return `(matrix, eigvals, eigvecs)`.

    `eigvals` are real and ascending, `eigvecs` are the corresponding
    orthonormal eigenvectors, as returned by `numpy.linalg.eigh`.
    """
    arr = _validate_square_hermitian(
        matrix, hermiticity_tolerance=hermiticity_tolerance, name=name
    )
    eigvals, eigvecs = np.linalg.eigh(arr)
    return arr, eigvals, eigvecs


def _validate_trace(
    matrix: np.ndarray, *, trace_tolerance: float, expected: float, name: str
) -> None:
    trace = np.trace(matrix)
    deviation = abs(trace - expected)
    if deviation > trace_tolerance:
        raise ValueError(
            f"{name} has trace {trace} deviating from expected {expected} "
            f"by more than trace_tolerance={trace_tolerance}"
        )


def _validate_positive_semidefinite(
    eigvals: np.ndarray, *, positivity_tolerance: float, name: str
) -> None:
    """Numerical PSD check: `lambda_min >= -positivity_tolerance`."""
    lambda_min = eigvals[0]
    if lambda_min < -positivity_tolerance:
        raise ValueError(
            f"{name} is not positive-semidefinite within "
            f"positivity_tolerance={positivity_tolerance}: "
            f"minimal eigenvalue={lambda_min}"
        )


def _validate_faithful(
    eigvals: np.ndarray, *, positivity_tolerance: float, name: str
) -> None:
    """Faithfulness check: `lambda_min > positivity_tolerance`."""
    lambda_min = eigvals[0]
    if not (lambda_min > positivity_tolerance):
        raise ValueError(
            f"{name} is not faithful (strictly positive) within "
            f"positivity_tolerance={positivity_tolerance}: "
            f"minimal eigenvalue={lambda_min}"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_density_matrix(
    rho,
    *,
    require_faithful: bool,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Validate that `rho` is an acceptable finite-dimensional density matrix.

    Checks performed, all fail-closed (raise `ValueError` on failure):

    - `rho` is a 2D square array of nonzero dimension with finite entries;
    - `rho` is hermitian within `hermiticity_tolerance`;
    - `Tr(rho) == 1` within `trace_tolerance`;
    - `rho` is positive-semidefinite within `positivity_tolerance`, i.e.
      its minimal eigenvalue satisfies `lambda_min >= -positivity_tolerance`.

    If `require_faithful` is `True`, an additional strict-positivity check
    is applied: `lambda_min > positivity_tolerance`. If `require_faithful`
    is `False`, positive-semidefinite non-faithful states are accepted.

    All tolerances are keyword-only and have no default value.

    `rho` is never silently normalized, symmetrized, or corrected. On
    success, this function returns the validated matrix as a complex
    `numpy.ndarray` with unchanged numerical values (only dtype is
    normalized to complex for downstream linear algebra).
    """
    arr, eigvals, _ = _hermitian_eigendecomposition(
        rho, hermiticity_tolerance=hermiticity_tolerance, name="rho"
    )
    _validate_trace(arr, trace_tolerance=trace_tolerance, expected=1.0, name="rho")
    _validate_positive_semidefinite(
        eigvals, positivity_tolerance=positivity_tolerance, name="rho"
    )
    if require_faithful:
        _validate_faithful(eigvals, positivity_tolerance=positivity_tolerance, name="rho")
    return arr


def partial_trace(
    operator, *, dimensions: Sequence[int], keep: Sequence[int]
) -> np.ndarray:
    """Partial trace of a finite operator over an explicit tensor product.

    `operator` acts on a tensor product of subsystems whose local
    dimensions are given explicitly, in order, by `dimensions`
    (`product(dimensions)` must equal the dimension of `operator`).
    `keep` lists the subsystem indices (0-based, into `dimensions`) that
    are kept; all other subsystems are traced out.

    Requirements (fail-closed, raise `ValueError` otherwise):

    - `operator` is a square 2D array;
    - `product(dimensions) == operator.shape[0]`;
    - `keep` indices are valid (`0 <= index < len(dimensions)`), unique,
      and given in strictly increasing order.

    The strictly-increasing-order requirement on `keep` makes the output
    deterministic and avoids an implicit permutation of the kept factors:
    the output acts on the tensor product of the kept subsystems taken in
    the same relative order as in `dimensions`, and has dimension
    `product(dimensions[i] for i in keep)`.

    This primitive makes no assumption about the number of subsystems, their
    dimensions, or any bipartite/qubit structure: it operates on a finite
    tensor product of arbitrary, explicitly supplied dimensions.
    """
    arr = np.asarray(operator)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("operator must be a square 2D array")

    dims = tuple(int(d) for d in dimensions)
    if len(dims) == 0:
        raise ValueError("dimensions must be a non-empty sequence")
    if any(d <= 0 for d in dims):
        raise ValueError("dimensions must be strictly positive integers")

    total_dim = 1
    for d in dims:
        total_dim *= d
    if arr.shape[0] != total_dim:
        raise ValueError(
            f"operator dimension {arr.shape[0]} does not match "
            f"product(dimensions)={total_dim}"
        )

    keep_list = list(keep)
    if len(keep_list) == 0:
        raise ValueError("keep must be a non-empty sequence of subsystem indices")
    if len(set(keep_list)) != len(keep_list):
        raise ValueError("keep indices must be unique")
    if any((not isinstance(k, (int, np.integer))) or not (0 <= k < len(dims)) for k in keep_list):
        raise ValueError("keep indices must be valid subsystem indices into dimensions")
    if keep_list != sorted(keep_list):
        raise ValueError(
            "keep indices must be given in strictly increasing order "
            "(deterministic output order, no implicit permutation)"
        )

    n = len(dims)
    keep_set = set(keep_list)

    tensor = arr.reshape(dims + dims)

    row_labels = list(range(n))
    next_free_label = n
    col_labels: list[int] = []
    for i in range(n):
        if i in keep_set:
            col_labels.append(next_free_label)
            next_free_label += 1
        else:
            col_labels.append(row_labels[i])

    operand_subscript = row_labels + col_labels
    output_subscript = [row_labels[i] for i in keep_list] + [col_labels[i] for i in keep_list]

    result_tensor = np.einsum(tensor, operand_subscript, output_subscript)

    kept_dim = 1
    for i in keep_list:
        kept_dim *= dims[i]
    return result_tensor.reshape(kept_dim, kept_dim)
