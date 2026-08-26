"""Generic modular theory primitives: hermitian log, K, and modular flow.

This module implements the finite-dimensional, type-I modular theory
primitives used as the numerical backbone of CosmoTGG: the hermitian matrix
logarithm, the modular Hamiltonian `K = -log(rho)` (restricted to faithful
states), and the modular flow `O(s) = exp(+i K s) O exp(-i K s)`.

The sign convention of the modular flow is frozen by
`docs/model/hypothesis.md` (`O(s) = e^{+iKs} O e^{-iKs}`, the Connes–Rovelli
convention) and is not a free implementation choice.

The flow parameter `s` is a finite real scalar. It carries no physical time
interpretation, no unit, and no relation to an external spacetime metric or
gravitational scale; it is intentionally not named `time`/`physical_time`/`t`
anywhere in this API.

All numerical tolerances accepted by the public functions of this module are
explicit, keyword-only, and have no default value.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import (
    _hermitian_eigendecomposition,
    _validate_faithful,
    validate_density_matrix,
)

SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}


def hermitian_log(
    matrix, *, hermiticity_tolerance: float, positivity_tolerance: float
) -> np.ndarray:
    """Hermitian matrix logarithm via spectral decomposition.

    `matrix` must be hermitian within `hermiticity_tolerance` and strictly
    positive (`lambda_min > positivity_tolerance`); otherwise this function
    fails closed with `ValueError`. The logarithm is computed by
    diagonalizing `matrix` (`numpy.linalg.eigh`), taking the logarithm of
    its (real, strictly positive) eigenvalues, and reconstructing the
    hermitian result in the original eigenbasis. No `scipy` dependency is
    used.

    This primitive is generic: it makes no assumption that `Tr(matrix) == 1`.
    """
    _, eigvals, eigvecs = _hermitian_eigendecomposition(
        matrix, hermiticity_tolerance=hermiticity_tolerance, name="matrix"
    )
    _validate_faithful(eigvals, positivity_tolerance=positivity_tolerance, name="matrix")

    log_eigvals = np.log(eigvals)
    return (eigvecs * log_eigvals) @ eigvecs.conj().T


def modular_hamiltonian(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Modular Hamiltonian `K = -log(rho)` for a faithful density matrix.

    `rho` is validated as a density matrix (`validate_density_matrix`) with
    `require_faithful=True`: non-faithful `rho` is rejected, matching the
    domain currently frozen by `docs/model/hypothesis.md`. There is no free
    additive constant in this API: the definition implemented is exactly
    `K = -log(rho)`.
    """
    validated_rho = validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    log_rho = hermitian_log(
        validated_rho,
        hermiticity_tolerance=hermiticity_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    return -log_rho


def modular_flow(
    operator, modular_hamiltonian_matrix, s, *, hermiticity_tolerance: float
) -> np.ndarray:
    """Modular flow `O(s) = exp(+i K s) O exp(-i K s)`.

    `modular_hamiltonian_matrix` (`K`) must be hermitian within
    `hermiticity_tolerance`. `operator` (`O`) must have matching
    dimensions. `s` must be a finite real scalar; it carries no physical
    time interpretation and no unit.

    `exp(+i K s)` is computed without `scipy`, by diagonalizing `K`
    (`numpy.linalg.eigh`) and exponentiating spectrally; `exp(-i K s)` is
    obtained as its conjugate transpose, which holds exactly because `K` is
    hermitian and `s` is real.

    Sign convention: `+i K s` on the left, `-i K s` on the right. This must
    never be inverted; see `docs/model/hypothesis.md`.
    """
    _, eigvals, eigvecs = _hermitian_eigendecomposition(
        modular_hamiltonian_matrix,
        hermiticity_tolerance=hermiticity_tolerance,
        name="modular_hamiltonian_matrix",
    )

    o_arr = np.asarray(operator)
    if o_arr.ndim != 2 or o_arr.shape[0] != o_arr.shape[1]:
        raise ValueError("operator must be a square 2D array")
    if o_arr.shape != eigvecs.shape:
        raise ValueError(
            "operator and modular_hamiltonian_matrix must have matching "
            f"dimensions: got {o_arr.shape} and {eigvecs.shape}"
        )
    o_arr = o_arr.astype(complex, copy=False)

    s_arr = np.asarray(s)
    if s_arr.ndim != 0:
        raise ValueError("s must be a scalar")
    if not np.isreal(s_arr):
        raise ValueError("s must be real")
    s_value = float(s_arr.real)
    if not np.isfinite(s_value):
        raise ValueError("s must be finite")

    phase_plus = np.exp(1j * eigvals * s_value)
    exp_plus_k_s = (eigvecs * phase_plus) @ eigvecs.conj().T

    return exp_plus_k_s @ o_arr @ exp_plus_k_s.conj().T
