"""model1c canonical branch extraction and bounded global refinement.

Normative source: `docs/toy-models/toy1c/specification.md` §8, §9, §10.

Two distinct production paths, never conflated (spec §6.1/§6.2 of
`docs/toy-models/toy1c/implementation-design.md`):

- `canonical_branch_sequence`: production, licensed by the closure lemma
  `I_{n+1} o G_n = Phi o I_n` (spec §10, demonstrated analytically, not
  re-derived here) — computes `I_n(rho_n) = Phi^n(rho_0)` by iterating
  `cosmotgg.models.model1c.local_cell.phi` on a single `(4, 4)` cell
  state, at any `n`, never constructing a global `H_n` space
  (`NO_GLOBAL_H_N_CONSTRUCTION_FOR_THIS_PATH = TRUE`);
- `global_refinement`: corroborative-only, bounded to a few small levels
  (`GLOBAL_REFINEMENT_SCOPE = STRUCTURAL_CLOSURE_CORROBORATION_ONLY`),
  acting explicitly on the GLOBAL, possibly inter-cell-correlated state
  `rho_n` (dimension `4 ** (2 ** n)`):

      rho_extended = rho_n (x) alpha^(x) N_n
      rho_{n+1}    = U_all rho_extended U_all^dagger

  followed by an explicit tensor-factor reordering into the canonical
  level-`(n+1)` order (`cosmotgg.core.states.embed_operator`, never an
  implicit sort). Computing per-cell local marginals, refining them
  independently, and retensoring is FORBIDDEN
  (`LOCAL_MARGINAL_REFINEMENT_AND_RETENSORING = FORBIDDEN`): it would
  destroy inter-cell correlations already present in `rho_n` and would
  not compute `G_n`.
"""

from __future__ import annotations

from functools import reduce

import numpy as np

from cosmotgg.core.states import embed_operator, validate_density_matrix
from cosmotgg.models.model1c.local_cell import ALPHA, controlled_bell_unitary, phi


def _validate_level(n) -> int:
    if isinstance(n, (bool, np.bool_)):
        raise ValueError(f"n must be a non-negative integer, not bool: got {n!r}")
    if not isinstance(n, (int, np.integer)):
        raise ValueError(f"n must be a non-negative integer, got {type(n).__name__}: {n!r}")
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    return int(n)


def canonical_branch_sequence(
    seed,
    n_max,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> tuple[np.ndarray, ...]:
    """`(I_0(rho_0), ..., I_{n_max}(rho_{n_max}))` along `c_n = 0^n` (spec §9, §10).

    `CANONICAL_BRANCH_COMPUTATION = ITERATED_PHI_ON_SINGLE_CELL`, licensed
    by the closure lemma (spec §10, demonstrated, not re-derived here):
    each step is exactly `cosmotgg.models.model1c.local_cell.phi`; no
    global `H_n` space is ever constructed by this function, at any `n`.
    """
    n_max_v = _validate_level(n_max)
    seed_v = validate_density_matrix(
        seed,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if seed_v.shape != (4, 4):
        raise ValueError(f"seed must have shape (4, 4), got shape={seed_v.shape}")

    sequence = [seed_v]
    current = seed_v
    for _ in range(n_max_v):
        current = phi(
            current,
            hermiticity_tolerance=hermiticity_tolerance,
            trace_tolerance=trace_tolerance,
            positivity_tolerance=positivity_tolerance,
        )
        sequence.append(current)
    return tuple(sequence)


def global_refinement(
    rho_n,
    n,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Explicit multi-cell `G_n(rho_n)` on the GLOBAL state (spec §8), corroborative only.

    `rho_n` must be a valid `(4 ** N_n, 4 ** N_n)` density matrix,
    `N_n = 2 ** n` (fail-closed on any other shape/invalidity). Acts on
    the whole correlated global state — never on independently-refined
    local marginals (`LOCAL_MARGINAL_REFINEMENT_AND_RETENSORING =
    FORBIDDEN`):

        rho_extended = rho_n (x) alpha^(x) N_n
        rho_{n+1}    = U_all rho_extended U_all^dagger

    `GLOBAL_REFINEMENT_SCOPE = STRUCTURAL_CLOSURE_CORROBORATION_ONLY`:
    reserved for bounded structural-closure corroboration at a few small
    `n` only (spec §10 corroboration); the canonical branch at large `n`
    is always computed by `canonical_branch_sequence` instead.
    """
    n_v = _validate_level(n)
    num_cells = 2**n_v
    expected_dim = 4**num_cells

    rho_n_v = validate_density_matrix(
        rho_n,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    if rho_n_v.shape != (expected_dim, expected_dim):
        raise ValueError(
            f"rho_n must have shape ({expected_dim}, {expected_dim}) for n={n_v} "
            f"(N_n=2**n={num_cells} cells), got shape={rho_n_v.shape}"
        )

    # rho_extended = rho_n (x) alpha^(x) N_n: one fresh, independent ancilla
    # `alpha` per cell (spec §8), tensored globally onto the whole
    # correlated `rho_n` (never a per-cell marginal/retensoring shortcut).
    alpha_all = reduce(np.kron, [ALPHA] * num_cells)
    rho_extended = np.kron(rho_n_v, alpha_all)

    # Raw factor order after tensoring: [cell_0, ..., cell_{N-1},
    # anc_0, ..., anc_{N-1}] (2 * num_cells factors, dim 4 each).
    extended_dims = (4,) * (2 * num_cells)
    u_bell = controlled_bell_unitary()

    # U_all = product of the U_b, each acting on the disjoint pair
    # (cell_b, anc_b) and as identity elsewhere (spec §8); disjoint
    # supports commute, so the multiplication order is immaterial.
    u_all = np.eye(4 ** (2 * num_cells), dtype=complex)
    for b in range(num_cells):
        u_b = embed_operator(u_bell, dimensions=extended_dims, positions=(b, num_cells + b))
        u_all = u_b @ u_all

    rho_next_raw = u_all @ rho_extended @ u_all.conj().T

    # Explicit reordering from the raw factor order
    # [cell_0, ..., cell_{N-1}, anc_0, ..., anc_{N-1}] to the canonical
    # level-(n+1) interleaved order
    # [cell_0, anc_0, cell_1, anc_1, ..., cell_{N-1}, anc_{N-1}]
    # (= lexicographic (n+1)-bit-string order, spec §8): never an implicit
    # sort, always this explicit permutation via `embed_operator`.
    target_positions = tuple(2 * i for i in range(num_cells)) + tuple(
        2 * (i - num_cells) + 1 for i in range(num_cells, 2 * num_cells)
    )
    rho_next = embed_operator(rho_next_raw, dimensions=extended_dims, positions=target_positions)

    return validate_density_matrix(
        rho_next,
        require_faithful=False,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
