"""toy0a structural diagnostics of the finite Connes cocycle qualification.

Normative source: `docs/toy-models/toy0a/specification.md` §9.

This module implements the model-specific diagnostic assembly for the
canonical pair `(rho_AB, sigma_AB = rho_A ⊗ rho_B)` of `model0a`: the
reference state `sigma_AB` (§4), the log-commutator obstruction `C_AB`
(§9.4), and the ordinary-group defect `G(s1, s2)` (§9.5). It does not
reimplement any generic primitive already available in `cosmotgg.core`:
no partial trace, no matrix logarithm, no modular Hamiltonian, no
cocycle. It only assembles `cosmotgg.core.states.partial_trace`,
`cosmotgg.core.modular.modular_hamiltonian`, and
`cosmotgg.core.modular.finite_connes_cocycle`.

Per §9.10 of the specification, this module defines no scalar norm,
threshold, score, ratio, or PASS/FAIL classifier: `log_commutator_obstruction`
and `ordinary_group_defect` always return a **matrix**, never a scalar
diagnostic.

The finite Connes cocycle satisfies its own cocycle identity
(`docs/toy-models/toy0a/specification.md` §7); `ordinary_group_defect`
does not question that. It measures only whether the cocycle also
happens to satisfy the unrelated, stronger property of an ordinary
unitary group under direct multiplication.

Maximal authorized interpretation (§9.8 of the specification): this
structure distinguishes the commuting from the non-commuting structure
of the canonical pair, beyond its first-order tangent `R_AB`. It does
not establish emergent time, causal order, an arrow of time, geometry,
or gravity.
"""

from __future__ import annotations

import numpy as np

from cosmotgg.core.modular import finite_connes_cocycle, modular_hamiltonian
from cosmotgg.core.states import partial_trace


def model0a_reference_state(rho_ab) -> np.ndarray:
    """Reference (product-of-marginals) state `sigma_AB = rho_A ⊗ rho_B`.

    `rho_A = partial_trace(rho_ab, dimensions=(2, 2), keep=[0])` and
    `rho_B = partial_trace(rho_ab, dimensions=(2, 2), keep=[1])`
    (`cosmotgg.core.states.partial_trace`), then `sigma_AB = kron(rho_A,
    rho_B)` (`numpy.kron`) — the canonical pair assembly of
    `docs/toy-models/toy0a/specification.md` §4. This is a model-specific
    assembly of `core` primitives: no dimension/structural validation is
    performed beyond what `partial_trace` already performs, and `rho_ab`
    is never normalized or repaired.
    """
    rho_a = partial_trace(rho_ab, dimensions=(2, 2), keep=[0])
    rho_b = partial_trace(rho_ab, dimensions=(2, 2), keep=[1])
    return np.kron(rho_a, rho_b)


def log_commutator_obstruction(
    rho_ab,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Log-commutator obstruction `C_AB = [ln(rho_ab), ln(sigma_ab)]` (§9.4).

    `sigma_ab = model0a_reference_state(rho_ab)`. Computed as
    `K_rho @ K_sigma - K_sigma @ K_rho`, where `K_rho =
    modular_hamiltonian(rho_ab, ...) = -ln(rho_ab)` and `K_sigma =
    modular_hamiltonian(sigma_ab, ...) = -ln(sigma_ab)`
    (`cosmotgg.core.modular.modular_hamiltonian`): the two minus signs
    cancel exactly in the commutator, so this equals `[ln(rho_ab),
    ln(sigma_ab)]` exactly, without reimplementing the matrix logarithm.

    Returns the obstruction **matrix**; this function defines no norm,
    threshold, score, or PASS/FAIL classification (§9.10 of the
    specification). `C_AB` distinguishes commuting from non-commuting
    modular structure of the canonical pair; it is not a curvature, a
    time generator, or a causal generator (§9.4).

    `hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`
    are forwarded unchanged to `modular_hamiltonian`; no tolerance is
    defined locally by `model0a`.
    """
    sigma_ab = model0a_reference_state(rho_ab)

    k_rho = modular_hamiltonian(
        rho_ab,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )
    k_sigma = modular_hamiltonian(
        sigma_ab,
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )

    return k_rho @ k_sigma - k_sigma @ k_rho


def ordinary_group_defect(
    rho_ab,
    s1,
    s2,
    *,
    hermiticity_tolerance: float,
    trace_tolerance: float,
    positivity_tolerance: float,
) -> np.ndarray:
    """Ordinary-group defect `G(s1, s2) = v_(s1+s2) - v_s1 @ v_s2` (§9.5).

    `sigma_ab = model0a_reference_state(rho_ab)`; `v_s1`, `v_s2`,
    `v_(s1+s2)` are each obtained from
    `cosmotgg.core.modular.finite_connes_cocycle(rho_ab, sigma_ab, s,
    ...)`. The finite Connes cocycle satisfies its own cocycle identity
    (`docs/toy-models/toy0a/specification.md` §7); this diagnostic does
    not question that identity. `G` measures only whether the cocycle
    also happens to satisfy the separate, stronger property of an
    ordinary unitary group under direct multiplication
    (`v_(s1+s2) = v_s1 v_s2`), which it need not.

    `s1`, `s2` are forwarded unchanged to `finite_connes_cocycle`, which
    already validates each as a finite real scalar fail-closed; no
    validation is duplicated here, and no modular-parameter domain,
    grid, or sampling policy is introduced by this function.

    Returns the defect **matrix**; this function defines no norm,
    threshold, or PASS/FAIL classification (§9.10 of the specification).
    """
    sigma_ab = model0a_reference_state(rho_ab)

    cocycle_kwargs = dict(
        hermiticity_tolerance=hermiticity_tolerance,
        trace_tolerance=trace_tolerance,
        positivity_tolerance=positivity_tolerance,
    )

    v_1 = finite_connes_cocycle(rho_ab, sigma_ab, s1, **cocycle_kwargs)
    v_2 = finite_connes_cocycle(rho_ab, sigma_ab, s2, **cocycle_kwargs)
    v_12 = finite_connes_cocycle(rho_ab, sigma_ab, s1 + s2, **cocycle_kwargs)

    return v_12 - v_1 @ v_2
