"""toy0c projected relative modular generators, generator, and noncollinearity operator.

Normative source: `docs/toy-models/toy0c/specification.md` §8–§14, §21.

This module assembles `cosmotgg.core.states.validate_density_matrix`,
`cosmotgg.core.states.partial_trace`,
`cosmotgg.core.states.conditional_expectation`,
`cosmotgg.core.states.traceless_part`, and
`cosmotgg.core.modular.modular_hamiltonian` into the projected relative
modular generators `chi_A`, `chi_C` on the overlap subsystem `B` of the
fixed `(2, 2, 2)` factorization `A|B|C` declared for `model0c`
(`overlap_relative_modular_projections`, §8–§10), the relative
generator `Delta = -chi_A + chi_C` (`overlap_relative_modular_generator`,
§10), the noncollinearity operator `N = i[chi_A, chi_C]`
(`overlap_projected_noncollinearity_operator`, §13), and the algebraic
derivation `D(O_B) = -i[Delta, O_B]` (`overlap_relative_modular_derivation`,
§21, inherited from `model0b` §13 without redefinition).

It does not reimplement any generic primitive already available in
`cosmotgg.core`: no matrix logarithm, no modular Hamiltonian, no
partial trace, no conditional expectation, no trace-free reduction.
`conditional_expectation` and `traceless_part` are the promoted,
model-independent primitives of `cosmotgg.core.states`; this module
only composes them with the fixed `(2, 2, 2)` factorization and the
§10/§13 conventions of `model0c`. No commutator primitive exists in
`cosmotgg.core`; the commutators of `overlap_projected_noncollinearity_operator`
and `overlap_relative_modular_derivation` are assembled model-specific
here, as already done by `model0a/diagnostics.py` and `model0b/relative.py`.

`docs/toy-models/toy0c/specification.md` §20 records
`FINITE_FLOW_PARAMETER_PROBLEM = OPEN`: this module implements neither
a finite modular unitary construction nor any parameterized family of
operators built from `Delta`. It exposes only the algebraic projected
generators, the relative generator, the noncollinearity operator, and
the inner derivation, each determined solely by the input state /
operators, with no additional free numeric parameter.

The contribution of `overlap_projected_noncollinearity_operator` is
purely algebraic (`N = i[chi_A, chi_C]`): this module never classifies
`N` as zero/nonzero, never applies a norm, threshold, or PASS/FAIL
verdict. That classification belongs to `tests/models/model0c` and any
future qualification notebook, not to production code.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import modular_hamiltonian
from cosmotgg.core.states import (
    conditional_expectation,
    partial_trace,
    traceless_part,
    validate_density_matrix,
)

_ABC_DIMENSIONS = (2, 2, 2)
_PAIR_DIMENSIONS = (2, 2)
_QUBIT_DIMENSION = 2


def overlap_relative_modular_projections(
    rho_abc,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Projected relative modular generators `(chi_A, chi_C)` (§8–§10).

    `rho_abc` must be a faithful `(8, 8)` density matrix on the fixed
    `(2, 2, 2)` factorization `H_A ⊗ H_B ⊗ H_C` (§4 of the
    specification), validated via
    `cosmotgg.core.states.validate_density_matrix` with
    `require_faithful=True`; any shape other than `(8, 8)` is rejected
    fail-closed with `ValueError`, since this factorization is fixed for
    `model0c`. `hermiticity_tolerance`, `trace_tolerance`,
    `positivity_tolerance` are explicit, keyword-only, with no default
    value, forwarded unchanged to `validate_density_matrix` and
    `cosmotgg.core.modular.modular_hamiltonian`; no tolerance is
    invented locally.

    Construction (§7–§10 of the specification), reproducing the modular
    mechanism rather than the closed-form scalar formulas of §11
    (reserved for independent testing, not for production):

    1. `rho_AB = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[0, 1])`,
       `rho_BC = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[1, 2])`;
    2. `K_AB = modular_hamiltonian(rho_AB, ...)`,
       `K_BC = modular_hamiltonian(rho_BC, ...)` (§8);
    3. the trace-preserving conditional expectations onto `B` (§8),
       `E_A = conditional_expectation(K_AB, dimensions=(2, 2), keep=[1])`
       and
       `E_C = conditional_expectation(K_BC, dimensions=(2, 2), keep=[0])`;
    4. the trace-free reduction (§9,
       `cosmotgg.core.states.traceless_part`) applied to each of `E_A`,
       `E_C`: `chi_A = traceless_part(E_A)`, `chi_C = traceless_part(E_C)`
       (§10).

    Returns the **matrices** `(chi_A, chi_C)` (never the analytic
    scalar coefficients of §11).
    """
    validated_rho_abc = validate_density_matrix(
        rho_abc,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if validated_rho_abc.shape != (8, 8):
        raise ValueError(
            "rho_abc must have shape (8, 8) for the fixed (2, 2, 2) A|B|C "
            f"factorization of model0c, got shape={validated_rho_abc.shape}"
        )

    rho_ab = partial_trace(validated_rho_abc, dimensions=_ABC_DIMENSIONS, keep=[0, 1])
    rho_bc = partial_trace(validated_rho_abc, dimensions=_ABC_DIMENSIONS, keep=[1, 2])

    modular_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    k_ab = modular_hamiltonian(rho_ab, **modular_kwargs)
    k_bc = modular_hamiltonian(rho_bc, **modular_kwargs)

    e_a = conditional_expectation(k_ab, dimensions=_PAIR_DIMENSIONS, keep=[1])
    e_c = conditional_expectation(k_bc, dimensions=_PAIR_DIMENSIONS, keep=[0])

    chi_a = traceless_part(e_a)
    chi_c = traceless_part(e_c)

    return chi_a, chi_c


def _validate_square_finite_operator(matrix, *, expected_dimension: int, name: str) -> np.ndarray:
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be a square 2D array, got shape={arr.shape}")
    if arr.shape[0] != expected_dimension:
        raise ValueError(
            f"{name} must have shape ({expected_dimension}, {expected_dimension}), "
            f"got shape={arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr.astype(complex, copy=False)


def overlap_relative_modular_generator(chi_a, chi_c) -> np.ndarray:
    """Relative modular generator `Delta = -chi_A + chi_C` (§10).

    Purely algebraic combination of the two projected generators
    returned by `overlap_relative_modular_projections`. `chi_a`,
    `chi_c` must each be a `2x2` array of finite entries; any other
    shape or non-finite entry is rejected fail-closed with
    `ValueError`. No numerical tolerance is introduced by this
    function. Hermiticity of `chi_a`/`chi_c` is not required at this
    entry point (the production chain of
    `overlap_relative_modular_projections` always supplies hermitian
    `chi_A`/`chi_C`, in which case `Delta` is hermitian by
    construction).
    """
    chi_a_arr = _validate_square_finite_operator(
        chi_a, expected_dimension=_QUBIT_DIMENSION, name="chi_a"
    )
    chi_c_arr = _validate_square_finite_operator(
        chi_c, expected_dimension=_QUBIT_DIMENSION, name="chi_c"
    )
    return -chi_a_arr + chi_c_arr


def overlap_projected_noncollinearity_operator(chi_a, chi_c) -> np.ndarray:
    """Noncollinearity operator `N = i[chi_A, chi_C]` (§13).

    Purely algebraic construction: `1j * (chi_a @ chi_c - chi_c @
    chi_a)`. `chi_a`, `chi_c` must each be a `2x2` array of finite
    entries; any other shape or non-finite entry is rejected
    fail-closed with `ValueError`. No numerical tolerance is
    introduced by this function; `N` is hermitian by construction when
    `chi_a`, `chi_c` are hermitian (as produced by
    `overlap_relative_modular_projections`).

    This function never classifies `N` as zero or nonzero, applies no
    norm or threshold, and returns no boolean/PASS-FAIL verdict: it
    returns the matrix `N` itself. Any such classification is a test
    or qualification-notebook concern, not a production concern.
    """
    chi_a_arr = _validate_square_finite_operator(
        chi_a, expected_dimension=_QUBIT_DIMENSION, name="chi_a"
    )
    chi_c_arr = _validate_square_finite_operator(
        chi_c, expected_dimension=_QUBIT_DIMENSION, name="chi_c"
    )
    return 1j * (chi_a_arr @ chi_c_arr - chi_c_arr @ chi_a_arr)


def overlap_relative_modular_derivation(delta, observable_b) -> np.ndarray:
    """Overlap relative modular derivation `D(O_B) = -i[Delta, O_B]` (§21).

    Purely algebraic construction on `B(H_B)`: `-1j * (delta @
    observable_b - observable_b @ delta)`. No additional numeric
    parameter, no exponential, no finite unitary construction is
    involved; `delta` is normally the matrix returned by
    `overlap_relative_modular_generator`. Inherited from `model0b`
    §13 without redefinition.

    `delta` and `observable_b` must each be a `2x2` array of finite
    entries; any other shape, non-square array, or non-finite entry is
    rejected fail-closed with `ValueError`. `observable_b` is not
    required to be hermitian: the derivation acts algebraically on any
    operator of `B(H_B)`, hermitian or not. No additional numerical
    tolerance is introduced by this function.
    """
    delta_arr = _validate_square_finite_operator(
        delta, expected_dimension=_QUBIT_DIMENSION, name="delta"
    )
    observable_arr = _validate_square_finite_operator(
        observable_b, expected_dimension=_QUBIT_DIMENSION, name="observable_b"
    )

    return -1j * (delta_arr @ observable_arr - observable_arr @ delta_arr)
