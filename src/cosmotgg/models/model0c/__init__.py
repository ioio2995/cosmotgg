"""`cosmotgg.models.model0c` — toy0c model-specific assembly.

`model0c` tests whether two overlapping modular structures (`rho_AB`,
`rho_BC`) sharing a common subsystem `B`, on the three-qubit factorized
Hilbert space `H_A ⊗ H_B ⊗ H_C` of `toy0c`, can produce two
noncollinear operator directions on `B`: the projected relative
modular generators `chi_A`, `chi_C`
(`cosmotgg.models.model0c.relative.overlap_relative_modular_projections`),
the relative generator `Delta = -chi_A + chi_C`
(`overlap_relative_modular_generator`), and the noncollinearity
operator `N = i[chi_A, chi_C]`
(`overlap_projected_noncollinearity_operator`), assembled from the
state family (`cosmotgg.models.model0c.states`).

Normative sources:

- `docs/toy-models/toy0c/specification.md`
- `docs/toy-models/toy0c/implementation-design.md`
"""
