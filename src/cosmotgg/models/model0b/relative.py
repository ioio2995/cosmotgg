"""toy0b overlap relative modular generator and derivation.

Normative source: `docs/toy-models/toy0b/specification.md` §8–§14.

This module assembles `cosmotgg.core.states.validate_density_matrix`,
`cosmotgg.core.states.partial_trace`,
`cosmotgg.core.states.conditional_expectation`,
`cosmotgg.core.states.traceless_part`, and
`cosmotgg.core.modular.modular_hamiltonian` into the relative modular
generator `Delta_(A:C|B)` (`OVERLAP_RELATIVE_MODULAR_GENERATOR`, §8,
§12) on the overlap subsystem `B` of the fixed `(2, 2, 2)`
factorization `A|B|C` declared for `model0b`, and its purely algebraic
inner derivation `D(O_B) = -i[Delta_B, O_B]`
(`OVERLAP_RELATIVE_MODULAR_DERIVATION`, §13).

It does not reimplement any generic primitive already available in
`cosmotgg.core`: no matrix logarithm, no modular Hamiltonian, no
partial trace, no commutator primitive, no conditional expectation, no
trace-free reduction. The trace-preserving conditional expectation of
§9 and the trace-free reduction `tl_B` of §11 are both promoted,
model-independent primitives of `cosmotgg.core.states`
(`conditional_expectation`, `traceless_part`); this module only
composes them with the fixed `(2, 2, 2)` factorization and the §12
sign convention of `model0b`.

`docs/toy-models/toy0b/specification.md` §19 records
`FINITE_FLOW_PARAMETER_PROBLEM = OPEN`: this module implements neither
a finite modular unitary construction nor any parameterized family of
operators built from `Delta_B`. It exposes only the algebraic
generator matrix and its inner derivation, each determined solely by
the input state / operators, with no additional free numeric
parameter.
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


def overlap_relative_modular_generator(
    rho_abc,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Overlap relative modular generator `Delta_(A:C|B)` matrix (§8, §12).

    `rho_abc` must be a faithful `(8, 8)` density matrix on the fixed
    `(2, 2, 2)` factorization `H_A ⊗ H_B ⊗ H_C` (§4 of the
    specification), validated via
    `cosmotgg.core.states.validate_density_matrix` with
    `require_faithful=True`; any shape other than `(8, 8)` is rejected
    fail-closed with `ValueError`, since this factorization is fixed for
    `model0b`. `hermiticity_tolerance`, `trace_tolerance`,
    `positivity_tolerance` are explicit, keyword-only, with no default
    value, forwarded unchanged to `validate_density_matrix` and
    `cosmotgg.core.modular.modular_hamiltonian`; no tolerance is
    invented locally.

    Construction (§8, §9, §11, §12 of the specification), reproducing
    the modular mechanism rather than the closed-form scalar formula of
    §14 (which is reserved for independent testing, not for
    production):

    1. `rho_AB = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[0, 1])`,
       `rho_BC = partial_trace(rho_abc, dimensions=(2, 2, 2), keep=[1, 2])`;
    2. `K_AB = modular_hamiltonian(rho_AB, ...)`,
       `K_BC = modular_hamiltonian(rho_BC, ...)` (§8);
    3. the trace-preserving conditional expectations onto `B` (§9),
       `E_A = conditional_expectation(K_AB, dimensions=(2, 2), keep=[1])`
       and
       `E_C = conditional_expectation(K_BC, dimensions=(2, 2), keep=[0])`
       (`cosmotgg.core.states.conditional_expectation` divides by
       `d_traced = 2 = d_A = d_C`, the explicit normalization of the
       conditional expectation of §9; omitting it would change the
       numerical value of `Delta_B` and is a distinct implementation
       defect from anything covered elsewhere in this module);
    4. the trace-free reduction `tl_B` (§11,
       `cosmotgg.core.states.traceless_part`) applied to each of `E_A`,
       `E_C`;
    5. `Delta_B = -tl_B(E_A) + tl_B(E_C)` (§12 sign convention, fixed).

    Returns the **matrix** `Delta_B` (never the scalar `delta` of §14).
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
            f"factorization of model0b, got shape={validated_rho_abc.shape}"
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

    return -traceless_part(e_a) + traceless_part(e_c)


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


def overlap_relative_modular_derivation(delta_b, observable_b) -> np.ndarray:
    """Overlap relative modular derivation `D(O_B) = -i[Delta_B, O_B]` (§13).

    Purely algebraic construction on `B(H_B)`: `-1j * (delta_b @
    observable_b - observable_b @ delta_b)`. No additional numeric
    parameter, no exponential, no finite unitary construction is
    involved; `delta_b` is normally the matrix returned by
    `overlap_relative_modular_generator`.

    `delta_b` and `observable_b` must each be a `2x2` array of finite
    entries; any other shape, non-square array, or non-finite entry is
    rejected fail-closed with `ValueError`. `observable_b` is not
    required to be hermitian: the derivation acts algebraically on any
    operator of `B(H_B)`, hermitian or not. No additional numerical
    tolerance is introduced by this function.
    """
    delta_arr = _validate_square_finite_operator(
        delta_b, expected_dimension=_QUBIT_DIMENSION, name="delta_b"
    )
    observable_arr = _validate_square_finite_operator(
        observable_b, expected_dimension=_QUBIT_DIMENSION, name="observable_b"
    )

    return -1j * (delta_arr @ observable_arr - observable_arr @ delta_arr)
