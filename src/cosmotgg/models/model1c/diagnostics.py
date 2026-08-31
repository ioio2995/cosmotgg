"""model1c non-triviality separator, anti-collapse support, fidelity check.

Normative source: `docs/toy-models/toy1c/specification.md` §13, §15, §16.

    connected_xx_correlator(rho) = Tr[XX rho] - Tr[XI rho] Tr[IX rho]

(spec §13, analytic non-triviality separator). `bell_projection_gap`
supports the anti-collapse oracle `N9` (spec §15):
`algebra.p_bell(sigma_a) - algebra.p_bell(sigma_b)`, for two admissible
seeds with distinct Bell content. `require_faithful_state` delegates
strict-fidelity validation entirely to
`cosmotgg.core.states.validate_density_matrix(require_faithful=True,
...)` (spec §16): no pseudo-inverse, no clipping, no silent
regularization.

This module builds no cell, no refinement rule, no closed-form oracle.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import validate_density_matrix
from cosmotgg.models.model1c.algebra import PAULI_STACK, p_bell

_XX = np.kron(PAULI_STACK[1], PAULI_STACK[1])
_XI = np.kron(PAULI_STACK[1], PAULI_STACK[0])
_IX = np.kron(PAULI_STACK[0], PAULI_STACK[1])


def connected_xx_correlator(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> float:
    """`C_XX(rho) = <XX> - <XI><IX>` (spec §13), analytic non-triviality separator."""
    rho_v = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if rho_v.shape != (4, 4):
        raise ValueError(f"rho must have shape (4, 4), got shape={rho_v.shape}")

    # Tr[O rho] is real by construction for hermitian O and hermitian rho
    # (exact algebraic identity, not a numerical repair — same convention
    # as cosmotgg.models.model1b.modular_support.global_two_body_block).
    exp_xx = float(np.trace(_XX @ rho_v).real)
    exp_xi = float(np.trace(_XI @ rho_v).real)
    exp_ix = float(np.trace(_IX @ rho_v).real)
    return exp_xx - exp_xi * exp_ix


def bell_projection_gap(sigma_a, sigma_b) -> np.ndarray:
    """`P_BELL(sigma_a) - P_BELL(sigma_b)` (spec §15), anti-collapse support (`N9`).

    Delegates entirely to `cosmotgg.models.model1c.algebra.p_bell` (an
    independent analytic oracle): fails closed on malformed `sigma_a`/
    `sigma_b` exactly as `p_bell` does; no additional validation logic here.
    """
    return p_bell(sigma_a) - p_bell(sigma_b)


def require_faithful_state(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Strict-fidelity check (spec §16): delegates entirely to
    `cosmotgg.core.states.validate_density_matrix(require_faithful=True,
    ...)`.

    No pseudo-inverse, no clipping, no silent regularization: an
    insufficiently-faithful `rho` fails closed with `ValueError`.
    """
    return validate_density_matrix(
        rho,
        require_faithful=True,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
