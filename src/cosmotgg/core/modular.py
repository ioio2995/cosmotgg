"""Generic modular theory primitives: hermitian log, K, modular flow, cocycle.

This module implements the finite-dimensional, type-I modular theory
primitives used as the numerical backbone of CosmoTGG: the hermitian matrix
logarithm, the modular Hamiltonian `K = -log(rho)` (restricted to faithful
states), the modular flow `O(s) = exp(+i K s) O exp(-i K s)`, the finite
Connes cocycle `v_s(rho, sigma) = rho^(-is) sigma^(+is)` between two faithful
density matrices on the same finite-dimensional algebra, and the Connes
cocycle evaluated at the fixed analytic point `t = -i/2`,
`connes_cocycle_at_minus_i_half(rho, sigma) = rho^(1/2) sigma^(-1/2)`.

The sign convention of the modular flow is frozen by
`docs/model/hypothesis.md` (`O(s) = e^{+iKs} O e^{-iKs}`, the Connes–Rovelli
convention) and is not a free implementation choice. The finite Connes
cocycle is defined consistently with this same convention: with
`K_rho = -log(rho)` and `K_sigma = -log(sigma)`, `rho^(-is) = exp(+i K_rho s)`
and `sigma^(+is) = exp(+i K_sigma s)^dagger`.

The flow/cocycle parameter `s` is a finite real scalar. It carries no
physical time interpretation, no unit, and no relation to an external
spacetime metric or gravitational scale; it is intentionally not named
`time`/`physical_time`/`t` anywhere in this API.

With the standard Tomita-Takesaki notation for the Connes cocycle,
`[D rho : D sigma]_t = rho^(+it) sigma^(-it)`, `finite_connes_cocycle` and
this convention are related by a sign flip of the analytic parameter only:

    finite_connes_cocycle(rho, sigma, s) == [D rho : D sigma]_(-s)

`finite_connes_cocycle` only ever accepts a finite *real* scalar `s`
(`_validate_modular_parameter`); it has no complex-parameter variant, and
none is added by this module. `connes_cocycle_at_minus_i_half` is a
separate, standalone primitive: it is the value of `[D rho : D sigma]_t` at
the single fixed point `t = -i/2`, computed directly from `rho^(1/2)` and
`sigma^(-1/2)`, and it is not, and cannot be, expressed as a call to
`finite_connes_cocycle` with any real `s`.

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


def _validate_modular_parameter(s, *, name: str) -> float:
    """Validate that `s` is a real, finite scalar and return it as `float`.

    Shared by `modular_flow` and `finite_connes_cocycle`. `s` carries no
    physical time interpretation, no unit, and no relation to an external
    spacetime metric or gravitational scale; it is intentionally never
    named `time`/`physical_time`/`t`. Fail-closed (raise `ValueError`) on:
    non-scalar values, complex values, `NaN`, `+inf`, `-inf`.
    """
    s_arr = np.asarray(s)
    if s_arr.ndim != 0:
        raise ValueError(f"{name} must be a scalar")
    if not np.isreal(s_arr):
        raise ValueError(f"{name} must be real")
    s_value = float(s_arr.real)
    if not np.isfinite(s_value):
        raise ValueError(f"{name} must be finite")
    return s_value


def _modular_unitary(
    hermitian_matrix, s, *, hermiticity_tolerance: float, name: str
) -> np.ndarray:
    """Spectral evaluation of `exp(+i * hermitian_matrix * s)`.

    `hermitian_matrix` must be hermitian within `hermiticity_tolerance`.
    `s` must be a finite real scalar (validated via
    `_validate_modular_parameter`); it carries no physical time
    interpretation and no unit. Computed without `scipy`, by diagonalizing
    `hermitian_matrix` (`numpy.linalg.eigh`) and exponentiating spectrally.

    Shared by `modular_flow` and `finite_connes_cocycle` to avoid
    duplicating the validation of `s`, the diagonalization of the
    hermitian generator, and the spectral reconstruction of
    `exp(+i * hermitian_matrix * s)`.
    """
    s_value = _validate_modular_parameter(s, name="s")
    _, eigvals, eigvecs = _hermitian_eigendecomposition(
        hermitian_matrix, hermiticity_tolerance=hermiticity_tolerance, name=name
    )
    phase = np.exp(1j * eigvals * s_value)
    return (eigvecs * phase) @ eigvecs.conj().T


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
    exp_plus_k_s = _modular_unitary(
        modular_hamiltonian_matrix,
        s,
        hermiticity_tolerance=hermiticity_tolerance,
        name="modular_hamiltonian_matrix",
    )

    o_arr = np.asarray(operator)
    if o_arr.ndim != 2 or o_arr.shape[0] != o_arr.shape[1]:
        raise ValueError("operator must be a square 2D array")
    if o_arr.shape != exp_plus_k_s.shape:
        raise ValueError(
            "operator and modular_hamiltonian_matrix must have matching "
            f"dimensions: got {o_arr.shape} and {exp_plus_k_s.shape}"
        )
    o_arr = o_arr.astype(complex, copy=False)

    return exp_plus_k_s @ o_arr @ exp_plus_k_s.conj().T


def finite_connes_cocycle(
    rho,
    sigma,
    s,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Finite Connes cocycle `v_s(rho, sigma) = rho^(-is) sigma^(+is)`.

    `rho` and `sigma` must both be faithful (strictly positive) density
    matrices of matching dimensions, validated via `modular_hamiltonian`
    (which itself validates hermiticity, unit trace, and faithfulness);
    non-faithful inputs, or mismatched dimensions, fail closed with
    `ValueError`. `s` must be a finite real scalar; it carries no physical
    time interpretation and no unit (see module docstring).

    With `K_rho = -log(rho)` and `K_sigma = -log(sigma)` (CosmoTGG
    convention, `modular_hamiltonian`), this is computed as:

        v_s = exp(+i K_rho s) @ exp(+i K_sigma s)^dagger

    which is exactly `rho^(-is) sigma^(+is)`, since `exp(+i K_rho s)
    = rho^(-is)` and `exp(+i K_sigma s)^dagger = sigma^(+is)` (the second
    identity holds exactly because `K_sigma` is hermitian and `s` is real).
    No `scipy` dependency is used. `rho` and `sigma` are never silently
    normalized, symmetrized, or corrected.

    With the standard Tomita-Takesaki notation `[D rho : D sigma]_t
    = rho^(+it) sigma^(-it)`, this function computes
    `finite_connes_cocycle(rho, sigma, s) == [D rho : D sigma]_(-s)`. `s` is
    restricted to a finite real scalar here (see module docstring); no
    complex-parameter variant of this function exists or is added by this
    module. The fixed analytic point `t = -i/2` is provided instead by the
    separate, standalone primitive `connes_cocycle_at_minus_i_half`.

    This is the finite Connes cocycle of Tomita–Takesaki modular theory
    (Connes, 1973): a generic, model-independent construction between any
    two faithful states on the same finite-dimensional algebra. It carries
    no CosmoTGG-specific semantics on its own; a caller may separately form
    the quantity denoted `R_AB` in `docs/model/hypothesis.md` via
    `cosmotgg.core.information.log_density_difference`, but that specific
    notation, and any particular choice of `rho`/`sigma` pair, is not
    encoded by this function.
    """
    k_rho = modular_hamiltonian(
        rho,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    k_sigma = modular_hamiltonian(
        sigma,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if k_rho.shape != k_sigma.shape:
        raise ValueError("rho and sigma must have matching dimensions")

    u_rho = _modular_unitary(
        k_rho, s, hermiticity_tolerance=hermiticity_tolerance, name="modular_hamiltonian of rho"
    )
    u_sigma = _modular_unitary(
        k_sigma,
        s,
        hermiticity_tolerance=hermiticity_tolerance,
        name="modular_hamiltonian of sigma",
    )

    return u_rho @ u_sigma.conj().T


def _hermitian_power(
    matrix, power: float, *, hermiticity_tolerance: float, positivity_tolerance: float, name: str
) -> np.ndarray:
    """Spectral evaluation of `matrix**power` for a hermitian, faithful matrix.

    `matrix` must be hermitian within `hermiticity_tolerance` and strictly
    positive (`lambda_min > positivity_tolerance`), checked exactly as in
    `hermitian_log` (via `_hermitian_eigendecomposition` then
    `_validate_faithful`); otherwise this function fails closed with
    `ValueError`. Computed by diagonalizing `matrix` (`numpy.linalg.eigh`)
    and raising its (real, strictly positive) eigenvalues to the real
    exponent `power`, then reconstructing the hermitian result in the
    original eigenbasis. No `scipy` dependency is used; no clipping,
    pseudoinverse, ridge, or other regularization is applied.

    Private to this module; shared by `connes_cocycle_at_minus_i_half`
    (`power = +0.5` and `power = -0.5`) to avoid duplicating the
    diagonalization, faithfulness check, and spectral reconstruction logic
    already used by `hermitian_log`/`modular_hamiltonian`. This is not a
    general matrix-power API: `power` is a plain real scalar exponent, and
    no complex exponent is accepted.
    """
    _, eigvals, eigvecs = _hermitian_eigendecomposition(
        matrix, hermiticity_tolerance=hermiticity_tolerance, name=name
    )
    _validate_faithful(eigvals, positivity_tolerance=positivity_tolerance, name=name)

    powered_eigvals = eigvals**power
    return (eigvecs * powered_eigvals) @ eigvecs.conj().T


def connes_cocycle_at_minus_i_half(
    rho,
    sigma,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Connes cocycle at the fixed analytic point `t = -i/2`.

    With the standard Tomita-Takesaki notation `[D rho : D sigma]_t
    = rho^(+it) sigma^(-it)`, analytic continuation to the purely imaginary
    point `t = -i/2` gives `[D rho : D sigma]_(-i/2) = rho^(1/2)
    sigma^(-1/2)`, which is exactly what this function computes:

        F = rho^(1/2) @ sigma^(-1/2)

    `rho` and `sigma` must both be faithful (strictly positive) density
    matrices of matching dimensions, each validated independently via
    `validate_density_matrix` with `require_faithful=True`; non-faithful
    inputs, mismatched dimensions, non-hermitian input, bad trace, or
    non-positive-semidefinite input all fail closed with `ValueError`.

    `rho^(1/2)` and `sigma^(-1/2)` are each computed by diagonalizing the
    corresponding matrix (`numpy.linalg.eigh`) and applying the real
    exponent (`+1/2` resp. `-1/2`) spectrally to its strictly positive
    eigenvalues, then reconstructing the hermitian result in the original
    eigenbasis (`_hermitian_power`). No `scipy` dependency is used; no
    clipping, pseudoinverse, ridge, or other silent regularization is ever
    applied.

    This is a purely mathematical, model-independent identity between two
    faithful density matrices on the same finite-dimensional algebra:
    `F @ sigma @ F.conj().T == rho` holds exactly, by construction, for the
    `F` returned by this function.

    This function is unrelated, as an API, to `finite_connes_cocycle(rho,
    sigma, s)`: that function implements `v_s(rho, sigma) = rho^(-is)
    sigma^(+is)` for a finite *real* scalar `s` only (`finite_connes_cocycle(
    rho, sigma, s) == [D rho : D sigma]_(-s)`; see module docstring).
    `finite_connes_cocycle` never accepts a complex parameter, and there is
    no real value of `s` for which it equals the result of this function.
    This function is a separate, standalone primitive for the single fixed
    point `t = -i/2`, not a special case reached through
    `finite_connes_cocycle`.
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

    sqrt_rho = _hermitian_power(
        validated_rho,
        0.5,
        hermiticity_tolerance=hermiticity_tolerance,
        positivity_tolerance=positivity_tolerance,
        name="rho",
    )
    invsqrt_sigma = _hermitian_power(
        validated_sigma,
        -0.5,
        hermiticity_tolerance=hermiticity_tolerance,
        positivity_tolerance=positivity_tolerance,
        name="sigma",
    )

    return sqrt_rho @ invsqrt_sigma
