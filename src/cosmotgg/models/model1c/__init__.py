"""`cosmotgg.models.model1c` — toy1c T5a controlled cross-scale limit candidate.

`model1c` implements the Bell-refinement family `R_cell`/`Phi` (spec
§6-§7), its derived closure `I_{n+1} o G_n = Phi o I_n` (spec §10), and
the associated analytic limit `sigma_infinity = P_BELL(rho_0)` (spec
§12), on the fixed local cell `H_c = C^2 (x) C^2`
(`cosmotgg.models.model1c.algebra`, `cosmotgg.models.model1c.local_cell`,
`cosmotgg.models.model1c.oracle`, `cosmotgg.models.model1c.refinement`,
`cosmotgg.models.model1c.diagnostics`).

`model1c` does NOT establish `T5A_PASS`, `T5_PASS`, continuum, geometry,
curvature, gravity, or non-classicality (spec §2, §23).

`PHI_PRODUCTION_PATH = local_refinement_cell -> partial_trace` (spec §7,
`cosmotgg.models.model1c.local_cell`): the closed form `Phi = 1/2 Id +
1/2 P_BELL` (`cosmotgg.models.model1c.oracle.phi_closed_form`) is an
independent test oracle only, never used in production.

`IMPLEMENTATION_CORROBORATIVE_TESTS = OUTSIDE_T5A_QUALIFICATION_RECORD`
(spec §12): the tests of this package are implementation-corroborative
checks only; they never declare `T5A_PASS`.

`MODEL1C_PRODUCTION_IMPORTS_PRIOR_MODELS = NO`: this package imports no
`cosmotgg.models.model0a`-`model0e`/`model1a`/`model1b` production API.

Normative sources:

- `docs/toy-models/toy1c/specification.md`
- `docs/toy-models/toy1c/implementation-design.md`
"""
