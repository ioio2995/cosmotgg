"""model1c independent analytic oracles: closed-form `Phi` and `Phi^n`.

Normative source: `docs/toy-models/toy1c/specification.md` §7, §12.

    phi_closed_form(rho)       = 1/2 rho + 1/2 P_BELL(rho)
    phi_pow_closed_form(rho,n) = P_BELL(rho) + 2^-n (rho - P_BELL(rho))

(spec §7, §12, using the idempotence of `P_BELL`). Both are independent
analytic oracles (`ORACLE_ROLE = INDEPENDENT_CROSS_CHECK_ONLY`,
`ORACLE_NEVER_CALLED_BY_PRODUCTION_PATH = TRUE`): used only in tests to
cross-check `cosmotgg.models.model1c.local_cell.phi` (production) and
`cosmotgg.models.model1c.refinement.canonical_branch_sequence` (production,
iterated `phi`), never called by that production path itself.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.states import validate_density_matrix
from cosmotgg.models.model1c.algebra import p_bell


def _validate_cell_state(rho, *, hermiticity_tolerance, trace_tolerance, positivity_tolerance):
    rho_v = validate_density_matrix(
        rho,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if rho_v.shape != (4, 4):
        raise ValueError(f"rho must have shape (4, 4), got shape={rho_v.shape}")
    return rho_v


def phi_closed_form(
    rho,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`Phi = 1/2 Id + 1/2 P_BELL`, closed form (spec §7), oracle only."""
    rho_v = _validate_cell_state(
        rho,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    return 0.5 * rho_v + 0.5 * p_bell(rho_v)


def _validate_level(n) -> int:
    if isinstance(n, (bool, np.bool_)):
        raise ValueError(f"n must be a non-negative integer, not bool: got {n!r}")
    if not isinstance(n, (int, np.integer)):
        raise ValueError(f"n must be a non-negative integer, got {type(n).__name__}: {n!r}")
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    return int(n)


def phi_pow_closed_form(
    rho,
    n,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """`Phi^n = P_BELL + 2^-n (Id - P_BELL)` applied to `rho` (spec §12), oracle only."""
    rho_v = _validate_cell_state(
        rho,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    n_v = _validate_level(n)
    bell_part = p_bell(rho_v)
    return bell_part + (2.0**-n_v) * (rho_v - bell_part)
