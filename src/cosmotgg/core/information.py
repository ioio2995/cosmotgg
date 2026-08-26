"""Generic quantum information primitives on finite-dimensional states.

This module provides von Neumann entropy, Umegaki relative entropy, mutual
information for a bipartite state, and a generic log-density difference
primitive. All of them accept positive-semidefinite (possibly non-faithful)
density matrices where their established mathematical definition supports
it; `log_density_difference` is the one exception documented below, since it
requires both ordinary matrix logarithms to be finite.

All numerical tolerances accepted by the public functions of this module are
explicit, keyword-only, and have no default value.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import hermitian_log
from cosmotgg.core.states import (
    _hermitian_eigendecomposition,
    _validate_positive_semidefinite,
    _validate_trace,
    partial_trace,
    validate_density_matrix,
)

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}


def _clipped_eigenvalues(eigvals: np.ndarray) -> np.ndarray:
    """Clip small negative eigenvalues (already validated as PSD) to zero.

    This must only be called after `_validate_positive_semidefinite` has
    passed, so that any negative value here lies within the explicit
    positivity window supplied by the caller.
    """
    return np.where(eigvals < 0.0, 0.0, eigvals)


def _entropy_from_eigenvalues(eigvals: np.ndarray) -> float:
    """`-sum_i lambda_i log(lambda_i)` with convention `0 log 0 = 0`."""
    positive_mask = eigvals > 0.0
    log_vals = np.zeros_like(eigvals)
    log_vals[positive_mask] = np.log(eigvals[positive_mask])
    return float(-np.sum(eigvals * log_vals))


def von_neumann_entropy(
    rho, *, hermiticity_tolerance: float, trace_tolerance: float, positivity_tolerance: float
) -> float:
    """Von Neumann entropy `S(rho) = -Tr(rho log rho) = -sum_i lambda_i log(lambda_i)`.

    Convention `0 log 0 = 0`. Accepts positive-semidefinite, possibly
    non-faithful, density matrices (`require_faithful` is never requested
    here). Eigenvalues found within the explicit `positivity_tolerance`
    window below zero are treated as exactly zero for this computation,
    only after the positive-semidefiniteness check has passed; there is no
    silent renormalization.
    """
    arr, eigvals, _ = _hermitian_eigendecomposition(
        rho, hermiticity_tolerance=hermiticity_tolerance, name="rho"
    )
    _validate_trace(arr, trace_tolerance=trace_tolerance, expected=1.0, name="rho")
    _validate_positive_semidefinite(eigvals, positivity_tolerance=positivity_tolerance, name="rho")

    safe_eigvals = _clipped_eigenvalues(eigvals)
    return _entropy_from_eigenvalues(safe_eigvals)


def relative_entropy(
    rho,
    sigma,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
    support_tolerance: float,
) -> float:
    """Umegaki relative entropy `D(rho || sigma) = Tr[rho(log rho - log sigma)]`.

    Both `rho` and `sigma` are validated as positive-semidefinite,
    possibly non-faithful, density matrices (`require_faithful=False`).

    Support extension: if `supp(rho)` is not numerically contained in
    `supp(sigma)` within `support_tolerance`, this function returns
    `+inf` (`numpy.inf`) rather than a finite value, matching the standard
    convention for the Umegaki relative entropy. `support_tolerance` is
    distinct from `positivity_tolerance`: `positivity_tolerance` controls
    the numerical PSD acceptability of `rho`/`sigma` themselves, while
    `support_tolerance` controls the numerical resolution used to decide
    the support-inclusion condition between the two spectra.

    Both spectra are obtained via `numpy.linalg.eigh`; no `scipy` is used.
    """
    rho_arr, rho_eigvals, rho_eigvecs = _hermitian_eigendecomposition(
        rho, hermiticity_tolerance=hermiticity_tolerance, name="rho"
    )
    _validate_trace(rho_arr, trace_tolerance=trace_tolerance, expected=1.0, name="rho")
    _validate_positive_semidefinite(
        rho_eigvals, positivity_tolerance=positivity_tolerance, name="rho"
    )

    sigma_arr, sigma_eigvals, sigma_eigvecs = _hermitian_eigendecomposition(
        sigma, hermiticity_tolerance=hermiticity_tolerance, name="sigma"
    )
    _validate_trace(sigma_arr, trace_tolerance=trace_tolerance, expected=1.0, name="sigma")
    _validate_positive_semidefinite(
        sigma_eigvals, positivity_tolerance=positivity_tolerance, name="sigma"
    )

    if rho_arr.shape != sigma_arr.shape:
        raise ValueError("rho and sigma must have matching dimensions")

    rho_safe = _clipped_eigenvalues(rho_eigvals)
    sigma_safe = _clipped_eigenvalues(sigma_eigvals)

    overlaps = np.abs(rho_eigvecs.conj().T @ sigma_eigvecs) ** 2

    sigma_kernel_mask = sigma_safe <= support_tolerance
    if np.any(sigma_kernel_mask):
        leaking_weight = float(
            np.sum(rho_safe[:, None] * overlaps[:, sigma_kernel_mask])
        )
        if leaking_weight > support_tolerance:
            return float(np.inf)

    term_rho = _entropy_from_eigenvalues(rho_safe) * -1.0  # Tr[rho log rho] = -S(rho)

    sigma_positive_mask = sigma_safe > 0.0
    log_sigma_positive = np.log(sigma_safe[sigma_positive_mask])
    term_cross = float(
        np.sum(
            rho_safe[:, None]
            * overlaps[:, sigma_positive_mask]
            * log_sigma_positive[None, :]
        )
    )

    return term_rho - term_cross


def mutual_information(
    rho_ab,
    *,
    dimensions,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> float:
    """Mutual information `I(A:B) = S(rho_A) + S(rho_B) - S(rho_AB)`.

    `rho_ab` is a bipartite state on a tensor product of two explicit
    local dimensions `dimensions = (d_A, d_B)`. Marginals are obtained via
    `cosmotgg.core.states.partial_trace` (no duplicated trace logic).
    `rho_ab` may be non-faithful; all three entropies accept
    positive-semidefinite states.
    """
    dims = tuple(int(d) for d in dimensions)
    if len(dims) != 2:
        raise ValueError(
            "mutual_information expects exactly two explicit local "
            "dimensions (d_A, d_B)"
        )

    arr, eigvals, _ = _hermitian_eigendecomposition(
        rho_ab, hermiticity_tolerance=hermiticity_tolerance, name="rho_ab"
    )
    _validate_trace(arr, trace_tolerance=trace_tolerance, expected=1.0, name="rho_ab")
    _validate_positive_semidefinite(
        eigvals, positivity_tolerance=positivity_tolerance, name="rho_ab"
    )

    rho_a = partial_trace(arr, dimensions=dims, keep=[0])
    rho_b = partial_trace(arr, dimensions=dims, keep=[1])

    entropy_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    entropy_ab = von_neumann_entropy(arr, **entropy_kwargs)
    entropy_a = von_neumann_entropy(rho_a, **entropy_kwargs)
    entropy_b = von_neumann_entropy(rho_b, **entropy_kwargs)

    return entropy_a + entropy_b - entropy_ab


def log_density_difference(
    rho, sigma, *, hermiticity_tolerance: float, trace_tolerance: float, positivity_tolerance: float
) -> np.ndarray:
    """Generic log-density difference `L(rho, sigma) = log(rho) - log(sigma)`.

    Both `rho` and `sigma` must be faithful (strictly positive) density
    matrices, so that both ordinary hermitian matrix logarithms are finite
    on the whole space; non-faithful inputs fail closed with `ValueError`.

    This function is NOT named `R_AB`, and is NOT:

    - the general relative modular operator;
    - `log(rho sigma^{-1})` when `rho` and `sigma` do not commute;
    - a new physical observable.

    It is the plain difference of two ordinary hermitian matrix
    logarithms. A future consumer may form the quantity denoted `R_AB` in
    `docs/model/hypothesis.md` by evaluating
    `log_density_difference(rho_AB, kron(rho_A, rho_B), ...)`, but that
    specific notation is not encoded by this module.
    """
    validated_rho = validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    validated_sigma = validate_density_matrix(
        sigma,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if validated_rho.shape != validated_sigma.shape:
        raise ValueError("rho and sigma must have matching dimensions")

    log_rho = hermitian_log(
        validated_rho,
        hermiticity_tolerance=hermiticity_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    log_sigma = hermitian_log(
        validated_sigma,
        hermiticity_tolerance=hermiticity_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    return log_rho - log_sigma
