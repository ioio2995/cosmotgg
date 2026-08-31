"""model1c local refinement cell `R_cell`, its derived reduced map `Phi`,
and the pre-registered seeds of spec §11.

Normative source: `docs/toy-models/toy1c/specification.md` §6, §7, §11.

Production path only:

    local_refinement_cell -> partial_trace -> phi

`Phi` is never introduced as an independent law (spec §7): `phi` below is
computed exclusively by tracing the "new" ancilla daughter cell out of
`local_refinement_cell`'s output, via `cosmotgg.core.states.partial_trace`
(`PHI_PRODUCTION_PATH = local_refinement_cell -> partial_trace`). The
closed algebraic form `Phi = 1/2 Id + 1/2 P_BELL`
(`cosmotgg.models.model1c.oracle.phi_closed_form`) is an independent test
oracle only, never used here (`PHI_CLOSED_FORM_PATH = oracle.py ONLY`).

This module also exposes the pre-registered seeds of spec §11: the
faithful canonical seed `SIGMA_0`, the structural null seed
`SIGMA_0_NULL`, and the one-parameter admissible family
`sigma_0_family(kappa)` (`sigma_0_family(1/4) == SIGMA_0`,
`sigma_0_family(0) == SIGMA_0_NULL`).

This module builds no multi-cell state, no diagnostic.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import partial_trace, validate_density_matrix
from cosmotgg.models.model1c.algebra import G_BELL, G_BELL_LABELS, PAULI_STACK

# alpha = diag(5/8, 1/8, 1/8, 1/8) in the G_BELL-indexed ancilla basis
# (II, XX, ZZ, YY), spec §6: fixed constant, no free parameter.
ALPHA = np.diag([5.0 / 8.0, 1.0 / 8.0, 1.0 / 8.0, 1.0 / 8.0]).astype(complex)


def controlled_bell_unitary() -> np.ndarray:
    """`U = sum_g g (x) |g><g|` on `H_c (x) H_c` (dim 16), spec §6.

    Fixed, parameter-free unitary: block `g` acts on the "system" factor,
    `|g><g|` selects the matching ancilla basis vector on the "new" factor
    (ancilla basis order `G_BELL_LABELS = (II, XX, ZZ, YY)`, matching
    `ALPHA`).
    """
    dim_anc = len(G_BELL_LABELS)
    u = np.zeros((4 * dim_anc, 4 * dim_anc), dtype=complex)
    for index, label in enumerate(G_BELL_LABELS):
        projector = np.zeros((dim_anc, dim_anc), dtype=complex)
        projector[index, index] = 1.0
        u = u + np.kron(G_BELL[label], projector)
    return u


def local_refinement_cell(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`R_cell(rho) = U (rho (x) alpha) U^dagger` (spec §6), production.

    `rho` must be a valid `(4, 4)` density matrix on `D(H_c)` (fail-closed
    via `cosmotgg.core.states.validate_density_matrix`; `require_faithful=
    False`, spec §11: `R_cell`/`Phi` are defined on the whole of `D(H_c)`,
    without a strict-fidelity requirement on the seed). No pseudo-inverse,
    no clipping, no silent regularization.

    Returns the joint two-daughter-cell state (dimension 16): first factor
    the "system" daughter (cell `0`), second factor the "new"/ancilla
    daughter (cell `1`), spec §6.
    """
    rho_v = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if rho_v.shape != (4, 4):
        raise ValueError(f"rho must have shape (4, 4), got shape={rho_v.shape}")
    joint = np.kron(rho_v, ALPHA)
    u = controlled_bell_unitary()
    return u @ joint @ u.conj().T


def phi(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`Phi(rho) = Tr_new[R_cell(rho)]` (spec §7), production.

    Derived exclusively from `local_refinement_cell` via
    `cosmotgg.core.states.partial_trace` (`PHI_PRODUCTION_PATH =
    local_refinement_cell -> partial_trace`): `Phi` is never introduced as
    an independent law here (spec §7). The closed algebraic form is an
    independent test oracle only
    (`cosmotgg.models.model1c.oracle.phi_closed_form`), never used in this
    production path.
    """
    joint = local_refinement_cell(
        rho,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    return partial_trace(joint, dimensions=(4, 4), keep=(0,))


def _validate_kappa(kappa) -> float:
    if isinstance(kappa, (bool, np.bool_)):
        raise ValueError(f"kappa must be a real numeric scalar, not bool: got {kappa!r}")
    arr = np.asarray(kappa)
    if arr.ndim != 0:
        raise ValueError(f"kappa must be a scalar, got shape={arr.shape}")
    if not np.issubdtype(arr.dtype, np.number):
        raise ValueError(
            f"kappa must be a real numeric scalar, got {type(kappa).__name__}: {kappa!r}"
        )
    if np.iscomplexobj(arr):
        raise ValueError(f"kappa must be real, not complex: got {kappa!r}")
    value = float(arr)
    if not np.isfinite(value):
        raise ValueError(f"kappa must be finite, got {value}")
    return value


_IDENTITY4 = np.kron(PAULI_STACK[0], PAULI_STACK[0])
_XX = np.kron(PAULI_STACK[1], PAULI_STACK[1])
_XI = np.kron(PAULI_STACK[1], PAULI_STACK[0])


def sigma_0_family(kappa) -> np.ndarray:
    """One-parameter admissible seed family
    `sigma_0(kappa) = 1/4 [I + kappa XX + 1/4 XI]` (spec §11).

    `sigma_0_family(1.0 / 4.0) == SIGMA_0` (canonical seed),
    `sigma_0_family(0.0) == SIGMA_0_NULL` (structural null seed). `kappa`
    must be a real, finite numeric scalar (`bool` rejected). Positivity of
    the resulting operator (an admissibility requirement, spec §11) is NOT
    checked here — this is a pure algebraic construction; positivity is
    deferred to `cosmotgg.core.states.validate_density_matrix` at the
    point of use (fail-closed, no silent repair).
    """
    kappa_v = _validate_kappa(kappa)
    return 0.25 * (_IDENTITY4 + kappa_v * _XX + 0.25 * _XI)


# Pre-registered seeds (spec §11), CLOSED, not free parameters.
SIGMA_0 = sigma_0_family(0.25)
SIGMA_0_NULL = sigma_0_family(0.0)
