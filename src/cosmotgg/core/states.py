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
# modular). Factored here to avoid duplicating shape, hermiticity, trace,
# positivity, dimension and tolerance checks in every module. Not part of
# the public API.
# ---------------------------------------------------------------------------


def _validate_tolerance(tolerance, *, name: str) -> float:
    """Validate that `tolerance` is a real, finite, non-negative scalar.

    Fail-closed (raise `ValueError`) on: NaN, `+inf`, `-inf`, negative
    values, complex values, non-scalar arrays/sequences, `bool`/`numpy.bool_`,
    and any other non-numeric type (e.g. `str`). A tolerance of exactly
    `0.0` is a valid, accepted value. No coercion is performed beyond
    reading the already-numeric scalar value; there is no default value.
    """
    if isinstance(tolerance, (bool, np.bool_)):
        raise ValueError(f"{name} must be a real numeric scalar, not bool: got {tolerance!r}")

    arr = np.asarray(tolerance)
    if arr.ndim != 0:
        raise ValueError(f"{name} must be a scalar, got shape={arr.shape}")
    if not np.issubdtype(arr.dtype, np.number):
        raise ValueError(
            f"{name} must be a real numeric scalar, got {type(tolerance).__name__}: {tolerance!r}"
        )
    if np.iscomplexobj(arr):
        raise ValueError(f"{name} must be real, not complex: got {tolerance!r}")

    value = float(arr)
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value}")
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0, got {value}")
    return value


def _validate_dimensions(dimensions, *, name: str) -> tuple:
    """Validate a non-empty sequence of already-integer, positive local dimensions.

    Accepted element types: `int`, `numpy.integer` (excluding `bool` /
    `numpy.bool_`, which are technically integer-like but are rejected here
    to avoid a silent `True`/`False` -> `1`/`0` dimension). Rejected element
    types include, non-exhaustively: `bool`, `numpy.bool_`, `float`,
    `numpy.floating`, `str`, `complex`.

    No coercion is performed: a rejected value is never converted, only
    validated; on success the original values are returned unchanged.
    """
    dims_list = list(dimensions)
    if len(dims_list) == 0:
        raise ValueError(f"{name} must be a non-empty sequence")
    for d in dims_list:
        if isinstance(d, (bool, np.bool_)):
            raise ValueError(f"{name} entries must be integers, not bool: got {d!r}")
        if not isinstance(d, (int, np.integer)):
            raise ValueError(
                f"{name} entries must already be integers (int or numpy.integer), "
                f"got {type(d).__name__}: {d!r}"
            )
        if d <= 0:
            raise ValueError(f"{name} entries must be strictly positive, got {d!r}")
    return tuple(dims_list)


def _validate_square_hermitian(
    matrix, *, hermiticity_tolerance: float, name: str
) -> np.ndarray:
    """Validate a finite, square, 2D, hermitian array and return it as complex.

    Checks performed: `hermiticity_tolerance` itself is validated
    (`_validate_tolerance`); then 2D shape, square shape, nonzero
    dimension, finite values, hermiticity within `hermiticity_tolerance`.
    The returned array has the same numerical values as the input, only
    cast to complex dtype for uniform downstream linear algebra; no value
    is corrected, symmetrized, or renormalized.
    """
    hermiticity_tolerance = _validate_tolerance(hermiticity_tolerance, name="hermiticity_tolerance")
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
    trace_tolerance = _validate_tolerance(trace_tolerance, name="trace_tolerance")
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
    positivity_tolerance = _validate_tolerance(positivity_tolerance, name="positivity_tolerance")
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
    positivity_tolerance = _validate_tolerance(positivity_tolerance, name="positivity_tolerance")
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

    dims = _validate_dimensions(dimensions, name="dimensions")

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
