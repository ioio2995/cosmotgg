# T5 — Frontière corrigée de faisabilité vers `T5_FULL_PASS`

Statut : **note corrigée, non gelée**

```text
STATUS = PROPOSED_T5_FULL_PASS_BOUNDARY_FEASIBILITY_CORRECTED

NOT_FROZEN     = TRUE
CHATGPT_REVIEW = PENDING_FINAL_REVIEW

T5_FLOW_QUALIFICATION = PASS
T5                     = OPEN_NOT_EXECUTED
T5_FULL_PASS           = NOT_ESTABLISHED

FUNDAMENTAL_BLOCKING = NONE_DEMONSTRATED

T5_FULL_PASS_BOUNDARY = SUFFICIENTLY_CHARACTERIZED_FOR_NEXT_BOUNDED_PHASE

NEXT_MODEL = NOT_AUTHORIZED
NEXT_TOY   = NOT_AUTHORIZED
```

---

## 0. Origine et portée

Ce document intègre, sans arbitrage scientifique autonome, une décision
déjà rendue à partir de trois sources :

```text
SOURCE_1 = rapport initial T5-FULL-PASS-BOUNDARY-FEASIBILITY-1
SOURCE_2 = contre-expertise Opus T5-FULL-PASS-BOUNDARY-OPUS-REVIEW-1
SOURCE_3 = arbitrage scientifique ChatGPT
```

Il s'appuie sur `docs/model/hypothesis.md` (gelé, v0.2),
`docs/model/t5-relational-refinement-boundary.md`,
`docs/model/t5-modular-cross-scale-flow-criteria.md` (gelé) et
`docs/model/tidal-relational-curvature-criteria.md`, sans modifier
aucun de ces documents.

Il porte sur la fixture confirmée de `model1b`
(`docs/toy-models/toy1b/closure-report.md`,
`MODEL1B_STATUS = CLOSED_AT_T5_FLOW_QUALIFICATION_LEVEL`,
`T5_FLOW_QUALIFICATION = PASS`) et sur la frontière ouverte qu'elle
laisse vers `T5`.

Ce document ne déclare aucun `T5 PASS`, ne gèle rien, ne crée aucun
nouveau toy, ne conçoit ni `specification.md` ni
`implementation-design.md`, n'exécute aucun notebook, n'introduit
aucune métrique, distance, aire, temps ni `G`, et ne transforme `T5a`
ni en continuum ni en géométrie.

---

## 1. Scission de travail `T5a` / `T5b`

Enregistrée comme **structure de travail non gelée**, utile à la
lecture du reste de ce document :

```text
T5A = CONTROLLED_LIMIT_OF_STATE_DERIVED_CROSS_SCALE_FLOW
T5B = LOCAL_CONTINUUM_CORRESPONDENCE
```

Obligatoire :

```text
T5A_PASS != T5_PASS
T5A_PASS != T5B_PASS
T5A_PASS != CONTINUUM
T5A_PASS != LOCALITY
T5A_PASS != GEOMETRY
T5A_PASS != CURVATURE
T5A_PASS != GRAVITY
```

Cette scission clarifie les dépendances mais n'est pas encore une
redéfinition normative de `T5`.

---

## 2. Correction B1 — projection complète en `K` / Pauli

La projection à deux corps du datum modulaire canonique est exacte,
et non une approximation :

$$
J_{i\leftarrow j}^{ab}(K_n)
=
-\,2^{-N_n}\,\mathrm{Tr}\!\big[K_n\,\sigma_a^{(i)}\,\sigma_b^{(j)}\big]
$$

et, par orthogonalité de Pauli :

$$
J_{i\leftarrow j}^{ab}(K_n) = -\,c_{(i,a;j,b)}(K_n).
$$

```text
EXACT_DERIVED_TWO_BODY_PROJECTION = TRUE

H_GE3_CONTRIBUTION_TO_J = EXACTLY_ZERO
R_PAIR_IS_ERROR_ON_J    = FALSE

PAIR_ONLY_RECONSTRUCTION_PRESERVING_WEIGHT2_COEFFICIENTS
PRESERVES_J_AT_FIXED_LEVEL = TRUE
```

Conservées simultanément :

```text
CANONICAL_SCALE_DATUM         = FULL_K_n
FULL_K_n_MUST_REMAIN_CANONICAL = TRUE

PAIR_ONLY_COARSE_DATUM = FORBIDDEN_AS_EXACT_ROUTE
```

La conclusion correcte de l'observation confirmatoire de `model1b`
(`docs/toy-models/toy1b/closure-report.md` §6) :

```text
PAIR_TRUNCATION_FLOW_OBSERVATION = NONCLOSED_ABOVE_SIGNAL_FLOOR
```

est :

```text
PAIR_SECTOR_CLOSED_UNDER_FULL_STATE_FLOW = FALSE_FOR_MODEL1B_CONFIRMED_FIXTURE
```

Mais **pas** :

```text
NO_AUTONOMOUS_EFFECTIVE_PAIR_FLOW_EXISTS   (rejeté)
```

Enregistré à la place :

```text
AUTONOMOUS_REDUCED_FLOW_ON_PAIR_OR_LOOP_DATA = NOT_ESTABLISHED
```

Toute future loi autonome directement sur les coefficients de poids 2,
sur \(J\), \(Q\) ou \(\chi\), doit démontrer séparément sa
fermeture/suffisance : elle n'en hérite d'aucune par défaut.

---

## 3. Correction B2 — `SO(3)` / `log Q`

Facteur directionnel actif par arête :

```text
det(O) = -1
```

Pour un cycle de longueur active paire :

```text
Q_n in SO(3)
```

et, lorsque la comparaison inter-échelles est bien typée :

```text
Q_{n+1} Q_n^{-1} in SO(3)
```

Le logarithme réel antisymétrique existe pour tout élément de
`SO(3)`. Donc :

```text
Z2_OBSTRUCTION_TO_LOG_Q = FALSE
```

Le vrai problème n'est pas une obstruction \(\mathbb{Z}_2\), mais la
non-unicité de branche de la correspondance d'objets inter-échelles :

```text
CROSS_SCALE_OBJECT_CORRESPONDENCE
BRANCH_NONUNIQUENESS
```

À rotation d'angle \(\pi\) :

```text
LOG_Q_BRANCH = NON_UNIQUE
```

```text
FAIL_CLOSED_AT_PI = ADMISSIBLE_CONSERVATIVE_ROUTE
FAIL_CLOSED_AT_PI != MATHEMATICALLY_REQUIRED
```

Cette route de fermeture stricte à \(\pi\) n'est pas imposée par la
présente note de frontière :

```text
R3_LOG_Q_STATUS = OPTIONAL_LEGITIMATE_ROUTE_WITH_DECLARED_BRANCH_POLICY
```

---

## 4. Correction B3 — indice de raffinement vs coordonnée

Distinction explicite :

```text
REFINEMENT_INDEX =
    ordered/directed label identifying finer/coarser elements

REFINEMENT_COORDINATE =
    optional numerical structural coordinate r
```

Pour une simple revendication de convergence `T5a` :

```text
NUMERICAL_REFINEMENT_COORDINATE_REQUIRED = NO
```

Requis au minimum :

```text
DECLARED_ORDERED_OR_DIRECTED_REFINEMENT_INDEX = YES
```

Si un taux, un exposant, une dérivée ou un générateur est revendiqué :

```text
STRUCTURAL_REFINEMENT_COORDINATE = REQUIRED_FOR_THAT_ROUTE
```

et alors, obligatoirement :

```text
r != LENGTH
r != DISTANCE
r != AREA
r != TIME
r != ENERGY
r != INVERSE_TEMPERATURE
```

Non imposé :

```text
REFINEMENT_PARAMETER_ADDITIVITY = REQUIRED   (rejeté comme exigence générale)
```

L'additivité éventuelle est classée :

```text
CONVENIENT_GAUGE_CHOICE | ROUTE_SPECIFIC
```

La cofinalité est également route-dependent.

---

## 5. Correction B4 — tour projective

Retiré :

```text
UPWARD_PROJECTIVE_STATE_TOWER = NECESSARY_FOR_ANY_T5_LIMIT   (rejeté)
```

Remplacé par :

```text
DECLARED_REFINEMENT_INDEXED_FAMILY  = NECESSARY_CANDIDATE
DECLARED_CROSS_LEVEL_COMPARISON_LAW = NECESSARY_CANDIDATE

PROJECTIVE_STATE_CONSISTENCY = OPTIONAL_ROUTE
INDUCTIVE_ALGEBRA_FAMILY     = OPTIONAL_ROUTE
```

Une chaîne, une famille dirigée ou un net peuvent être admissibles
selon la revendication portée. Un poset dirigé global sur tous les
graphes n'est pas exigé.

---

## 6. Correction B5 — générateur

```text
FLOW_GENERATOR             = OPTIONAL_ROUTE
LOCAL_GEOMETRIC_GENERATOR  = STRONGER_OPTIONAL_ROUTE

GENERATOR_REQUIRED_FOR_T5A_LIMIT = NO
```

Une limite `T5a` peut être définie par convergence/compatibilité sans
générateur différentiel.

Reste vrai comme avertissement structurel :

```text
CURRENT_PARTIAL_TRACE_CHAIN_IS_NOT_AN_ITERATION_OF_ONE_SEMIGROUP = TRUE
```

Mais :

```text
NO_SEMIGROUP_GENERATOR != NO_T5A_LIMIT
```

---

## 7. Correction B6 — type I

Retiré :

```text
LIMIT_GENERICALLY_LEAVES_TYPE_I   (rejeté)
```

Distinction enregistrée :

```text
FINITE_APPROXIMANTS = TYPE_I_FINITE

INDUCTIVE_CSTAR_LIMIT = TYPE_NOT_APPLICABLE_AS_VON_NEUMANN_FACTOR_CLASSIFICATION

GNS_VON_NEUMANN_CLOSURE_TYPE = STATE_DEPENDENT
```

Une extension Tomita–Takesaki ne devient nécessaire que si une
revendication de donnée modulaire limite sort réellement du cadre où
\(K=-\log(\rho)\) est défini comme opérateur borné de densité :

```text
LIMIT_MODULAR_DOMAIN_DECLARATION = CONDITIONAL_NECESSITY
```

```text
T5A_FINITE_LEVEL_DIAGNOSTIC_LIMIT
DOES_NOT_AUTOMATICALLY_REQUIRE
TYPE_I_TO_TOMITA_TAKESAKI_EXTENSION
```

---

## 8. Schéma de décimation

```text
WELL_DEFINED_WITHIN_DECLARED_REFINEMENT_SCHEME = NECESSARY

UNIVERSAL_ACROSS_REFINEMENT_SCHEMES = NOT_REQUIRED_FOR_T5A
```

mais :

```text
SCHEME_INTRINSICITY_OR_UNIVERSALITY =
    NECESSARY_CANDIDATE_FOR_T5B_OR_INTRINSIC_CONTINUUM_CLAIM
```

---

## 9. `G3` / `G4`

```text
G3_FOR_T5 = CONDITIONALLY_NECESSARY
```

Condition : si une structure directionnelle/holonomique est utilisée
comme porteur d'une revendication cross-scale de courbure
relationnelle (cf. `docs/model/tidal-relational-curvature-criteria.md`
§4, `G3 — CURVATURE_NONTRIVIALITY`).

```text
G4_FOR_T5A                              = NOT_REQUIRED
G4_FOR_GENERIC_T5_LIMIT                 = NOT_REQUIRED
G4_FOR_RELATIONAL_TIDAL_RESPONSE_CLAIM  = NECESSARY_IN_ITS_NATIVE_STAGE
```

`T5` n'est pas confondu avec `T2`/`T4`/`T6`/`T7`.

---

## 10. Richesse de contenu invariant

Observation Opus enregistrée : pour une unique matrice \(Q \in
SO(3)\), sa classe de conjugaison est déterminée par un angle, donc
par un invariant scalaire équivalent à \(\chi\).

```text
CHI_VS_SO3_CONJUGACY_CLASS = SAME_INVARIANT_INFORMATION_FOR_SINGLE_Q
```

Correction du faux positif :

```text
OLD_F5        = chi convergence != conjugacy-class convergence
OLD_F5_STATUS = INVALID_FOR_SINGLE_SO3_LOOP
```

```text
NEW_F5 = CONVERGENCE_OF_ONE_SCALAR_INVARIANT
         !=
         TENSORIAL_OR_GEOMETRIC_CONTENT
```

Non imposé :

```text
INVARIANT_DIMENSION_GREATER_THAN_ONE = REQUIRED_FOR_T5A_MATHEMATICAL_LIMIT   (rejeté)
```

Classé plutôt :

```text
T5C17_INVARIANT_CONTENT_RICHNESS =
    OPTIONAL_FOR_T5A_LIMIT
    | NECESSARY_CANDIDATE_FOR_G6_OR_GEOMETRIC_CARRIER_CLAIM
```

---

## 11. Portes candidates corrigées

Présentées comme **`PROPOSED` / `NON_FROZEN`**.

### T5C1 — Indice de raffinement déclaré

```text
T5C1         = DECLARED_REFINEMENT_INDEX
classification = NECESSARY_CANDIDATE
```

Condition minimale : un ordre/direction permettant de distinguer
finer/coarser.

### T5C2 — Non-dégénérescence de la coordonnée de raffinement

```text
T5C2         = REFINEMENT_COORDINATE_NONDEGENERACY
classification = CONDITIONAL_NECESSARY
```

Seulement si un taux, un scaling ou un générateur est revendiqué.

### T5C3 — Famille indexée et comparaison inter-niveaux

```text
T5C3         = DECLARED_REFINEMENT_INDEXED_FAMILY_AND_CROSS_LEVEL_COMPARISON
classification = NECESSARY_CANDIDATE
```

Tour projective : `OPTIONAL_ROUTE`.

### T5C4 — Compatibilité de famille contrôlée

```text
T5C4         = CONTROLLED_FAMILY_COMPATIBILITY
classification = NECESSARY_CANDIDATE
```

Aucune cofinalité universelle ni aucun poset global dirigé n'est
imposé.

### T5C5 — Intrinsicité du schéma de raffinement

```text
T5C5         = REFINEMENT_SCHEME_INTRINSICITY
classification = OPTIONAL_FOR_T5A
                  NECESSARY_CANDIDATE_FOR_T5B_INTRINSIC_CONTINUUM
```

### T5C6 — Espace-objet limite et notion de convergence déclarés

```text
T5C6         = DECLARED_LIMIT_OBJECT_SPACE_AND_CONVERGENCE_NOTION
classification = NECESSARY_CANDIDATE
```

### T5C7 — Comportement asymptotique non trivial

```text
T5C7         = NONTRIVIAL_ASYMPTOTIC_BEHAVIOUR
classification = NECESSARY_CANDIDATE
```

Inclut : nombre de niveaux suffisant ; nul de trivialisation ;
comportement asymptotique déclaré avant qualification.

### T5C8 — Pare-feu reindexing/reparamétrisation

```text
T5C8         = REINDEXING_REPARAMETRIZATION_FIREWALL
classification = NECESSARY_CANDIDATE
```

Pour une simple limite : invariance sous reindexing/reformulation
cofinale admissible. Pour une revendication de taux/générateur :
covariance sous \(r \to f(r)\).

### T5C9 — Déclaration du type de générateur

```text
T5C9         = GENERATOR_TYPE_DECLARATION
classification = OPTIONAL_ROUTE
```

### T5C10 — Fermeture de flux de toute paramétrisation réduite

```text
T5C10        = FLOW_CLOSURE_OF_ANY_REDUCED_PARAMETRIZATION
classification = CONDITIONAL_NECESSARY
```

Si une loi autonome réduite est revendiquée, sa fermeture doit être
démontrée. Ni `H_GE3` ni `R_PAIR` ne sont associés à une erreur sur
\(J\) (cf. §2).

### T5C11 — Correspondance d'objets cross-scale déclarée

```text
T5C11        = DECLARED_CROSS_SCALE_OBJECT_CORRESPONDENCE
classification = NECESSARY_CANDIDATE
```

Pour `model1b`, `A` survit et le point de base est commun. Pour une
famille future, la correspondance de cycles/objets doit être
déclarée.

### T5C12 — Requalification cross-scale `G3`

```text
T5C12        = G3_CROSS_SCALE_REQUALIFICATION
classification = CONDITIONAL_NECESSARY
```

Seulement si l'objet directionnel est promu porteur de courbure
relationnelle cross-scale.

### T5C13 — Requalification cross-scale `G4`

```text
T5C13        = G4_CROSS_SCALE_REQUALIFICATION
classification = NOT_REQUIRED_FOR_T5A_OR_GENERIC_LIMIT
                  NATIVE_TO_TIDAL_RESPONSE_STAGE
```

### T5C14 — Correspondance continuum minimale `G8`

```text
T5C14        = G8_MINIMAL_CONTINUUM_CORRESPONDENCE
classification = T5B_TARGET
                  PREMATURE_FOR_T5A
```

### T5C15 — Déclaration du domaine modulaire limite

```text
T5C15        = LIMIT_MODULAR_DOMAIN_DECLARATION
classification = CONDITIONAL_NECESSARY
```

Seulement si un véritable datum modulaire limite est revendiqué.

### T5C16 — Non-classicalité

```text
T5C16        = NONCLASSICALITY
classification = NOT_REQUIRED_FOR_T5A_MATHEMATICAL_LIMIT
                  REQUIRED_FIREWALL_BEFORE_PHYSICAL_QUANTUM_GEOMETRY_CLAIM
```

### T5C17 — Richesse de contenu invariant

```text
T5C17        = INVARIANT_CONTENT_RICHNESS
classification = OPTIONAL_FOR_T5A_LIMIT
                  NECESSARY_CANDIDATE_FOR_G6_OR_GEOMETRIC_CARRIER_CLAIM
```

---

## 12. Ensemble faux-positifs / no-go

Conservés inchangés :

```text
F1  finite running mistaken for continuum
F2  refinement index mistaken for physical distance
F3  vanishing running mistaken for nontrivial fixed point
F4  nonzero running mistaken for local generator
F7  arbitrary normalization producing fake scaling
F8  tree/cycle distinction mistaken for curvature
F9  local-frame covariance mistaken for spacetime covariance
F10 mathematical continuum limit mistaken for gravity
```

Corrigés :

```text
F5 = single scalar invariant mistaken for tensorial/geometric convergence

F6 = reduced parametrization assumed dynamically closed without proof
```

---

## 13. Frontière minimale `T5a`

Présentée comme cible de phase suivante **non gelée**.

```text
T5A_MINIMAL_CANDIDATE_GATES =
    T5C1
    T5C3
    T5C4
    T5C6
    T5C7
    T5C8
    T5C11
```

plus les portes conditionnelles si la route les utilise :

```text
    T5C2
    T5C9
    T5C10
    T5C12
    T5C15
```

`T5C5` fort, `T5C14` et le contenu `G6`/`T5C17` fort appartiennent
plutôt à `T5b` ou à une revendication géométrique plus forte.

```text
T5A_MINIMAL_CANDIDATE_GATES_STATUS = NOT_YET_DECLARED_SUFFICIENT
                                       NOT_FROZEN
```

---

## 14. Conclusion

```text
T5_FULL_PASS_BOUNDARY = SUFFICIENTLY_CHARACTERIZED_FOR_NEXT_BOUNDED_PHASE

NEXT_BOUNDED_PHASE = T5A_CONTROLLED_CROSS_SCALE_LIMIT_CRITERIA_DESIGN

FUNDAMENTAL_BLOCKING = NONE_DEMONSTRATED
```

Mais :

```text
T5A_CRITERIA = NOT_YET_FROZEN
T5A_PASS     = NOT_ESTABLISHED
T5_PASS      = NOT_ESTABLISHED

NEXT_MODEL = NOT_AUTHORIZED
NEXT_TOY   = NOT_AUTHORIZED
```

---

## 15. Statut suivant

```text
T5_FULL_PASS_BOUNDARY_DOCUMENT = docs/model/t5-full-pass-boundary-feasibility.md
T5_FULL_PASS_BOUNDARY_STATUS   = PROPOSED_T5_FULL_PASS_BOUNDARY_FEASIBILITY_CORRECTED
NOT_FROZEN                     = TRUE
CHATGPT_REVIEW                 = PENDING_FINAL_REVIEW

NEXT_MODEL = NOT_AUTHORIZED
NEXT_TOY   = NOT_AUTHORIZED
```

Ce document ne modifie pas `docs/model/hypothesis.md`, ne modifie pas
`docs/model/t5-relational-refinement-boundary.md`, ne modifie pas
`docs/model/t5-modular-cross-scale-flow-criteria.md` (`FROZEN`), ne
modifie pas `docs/model/tidal-relational-curvature-criteria.md`, ne
modifie aucun fichier de `docs/toy-models/toy1b/**`, ne définit aucun
`T5 PASS`, et n'autorise la conception d'aucun nouveau toy.
