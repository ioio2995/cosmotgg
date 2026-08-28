# Rapport de clôture — `model1b`

Statut : **clôture au niveau de qualification `T5-FLOW`**

Ce document clôt formellement `model1b` au niveau exact atteint par son
exécution confirmatoire `T5-FLOW`, acceptée par revue distante ChatGPT
(`PASS`). Il n'ajoute, ne recalcule et n'invente aucune valeur
scientifique : il enregistre factuellement les résultats déjà produits
par `experiments/toy1b/toy1b.ipynb` et déjà consignés par
`docs/governance/current-task.md`.

Ce document est **documentaire uniquement**. Il ne modifie ni le
modèle, ni le protocole gelé, ni l'implémentation, ni le notebook
confirmatoire.

---

## 1. Références normatives

```text
MODEL1B_IMPLEMENTATION_ACCEPTED_HEAD            = 788337f4d383962947586084c342edcf395af234
MODEL1B_VALIDATION_PLAN_FROZEN_HEAD             = 9712c4b68d4dea84878dd0281dd903fea56a7fd6
MODEL1B_VALIDATION_PLAN_SCIENTIFIC_CONTENT_HEAD = d9c7474de8a747d0ada0685a06549dcdccfcb977
MODEL1B_CONFIRMATORY_RUN_HEAD                   = 64bda0525af9eb69813d487c8f429a5db31f5c01

CONFIRMATORY_RUN                    = MODEL1B_T5_FLOW_CONFIRMATORY_RUN_1
CHATGPT_CONFIRMATORY_RUN_REVIEW     = PASS
```

Documents gelés amont, non rouverts par ce rapport :

```text
docs/toy-models/toy1b/specification.md         = FROZEN
docs/toy-models/toy1b/implementation-design.md = FROZEN
docs/toy-models/toy1b/validation-plan.md       = FROZEN_MODEL1B_T5_FLOW_VALIDATION_PLAN
experiments/toy1b/toy1b.ipynb                  = ACCEPTED_CONFIRMATORY_RUN
```

---

## 2. Statut de clôture

```text
MODEL1B_STATUS = CLOSED_AT_T5_FLOW_QUALIFICATION_LEVEL

MODEL1B_T5_FLOW_CONFIRMATORY_RUN = ACCEPTED

T5_FLOW_EXECUTION_STATUS = COMPLETED
T5_FLOW_QUALIFICATION    = PASS

T5 = OPEN_NOT_EXECUTED

SCIENTIFIC_BLOCKING = NONE_FOR_T5_FLOW_QUALIFICATION

T5_FULL_PASS = NOT_ESTABLISHED
```

---

## 3. Résultat confirmatoire (table `T5F1`–`T5F11`)

Recopié tel quel depuis la table finale du notebook accepté
(§22–23 de `experiments/toy1b/toy1b.ipynb`), sans réexécution ni
recalcul :

```text
T5F1  = PASS
T5F2  = PASS
T5F3  = PASS / SATISFIED_BY_CONSTRUCTION_CONFIRMED
T5F4  = PASS
T5F5  = PASS
T5F6  = PASS
T5F7  = PASS
T5F8  = PASS
T5F9  = PASS
T5F10 = PASS
T5F11 = PASS / SATISFIED_BY_CONSTRUCTION_CONFIRMED
```

Oracles négatifs et observations associées :

```text
PAIR_TRUNCATION_FLOW_OBSERVATION = NONCLOSED_ABOVE_SIGNAL_FLOOR
TREE_DIRECTIONAL_RUNNING         = ABSENT
```

---

## 4. Preuve numérique clé

Rapportée comme synthèse du notebook accepté, sans recalcul :

```text
T5F3_STATE_COMPOSITION_RESIDUAL = 3.868e-17

T5F4_MODULAR_PATH_RESIDUAL = 1.205e-15

T5F5_PAULI_RECONSTRUCTION_RESIDUALS =
  K2 = 1.836e-16
  K1 = 2.256e-16
  K0 = 1.267e-16

T5F5_HIGHER_BODY_OBSERVATIONS (OBSERVATION ONLY) =
  H_GE3_K1  = 3.341e-04
  H_GE3_K0  = 3.115e-04
  R_PAIR_K1 = 7.588e-05
  R_PAIR_K0 = 1.059e-04

T5F6_MAX_COVARIANCE_RESIDUAL = 1.251e-13

T5F7_MAX_PURE_GAUGE_D_FLAT = 1.647e-14

T5F8_MAX_DELTA                     = 2.900e-06
T5F8_SIGNAL_FLOOR                  = 1.000e-08
T5F8_SIGNAL_TO_FLOOR_RATIO_APPROX  = 290

TREE_RESIDUAL_8_TO_6 = 1.005e-14
TREE_RESIDUAL_6_TO_4 = 4.657e-14
```

Les quatre valeurs `T5F5_HIGHER_BODY_OBSERVATIONS` restent
**observation only** : elles ne déterminent aucun verdict `T5F1`–`T5F11`
et ne sont pas utilisées comme critère de `PASS`/`FAIL`.

---

## 5. Ce que `model1b` qualifie

`model1b` qualifie, au niveau `T5-FLOW` et à ce niveau seulement, les
éléments suivants :

```text
STATE_DERIVED_COARSE_GRAINING                    = QUALIFIED
CANONICAL_MODULAR_DATUM_FROM_STATE               = QUALIFIED
COMPLETE_MODULAR_SUPPORT                         = QUALIFIED
LOCAL_FRAME_COVARIANCE                           = QUALIFIED
PURE_GAUGE_FLATNESS_PRESERVATION                 = QUALIFIED
FINITE_SCALE_STATE_DERIVED_DIRECTIONAL_RUNNING   = QUALIFIED
FAIL_CLOSED_DIRECTIONAL_DOMAIN                   = QUALIFIED
MULTISTEP_CROSS_SCALE_FLOW                       = QUALIFIED

T5_FLOW = QUALIFIED
```

---

## 6. Observation importante — non-fermeture par paire

Le coarse-graining confirmatoire engendre effectivement, aux niveaux
grossiers, un contenu modulaire qui n'est pas fermé dans le secteur à
deux corps sous le `SIGNAL_FLOOR` préenregistré :

```text
PAIR_TRUNCATION_FLOW_OBSERVATION = NONCLOSED_ABOVE_SIGNAL_FLOOR
```

Cette observation ne doit pas être promue en axiome. En particulier :

```text
PAIR_NONCLOSURE != T5_PASS
PAIR_NONCLOSURE != GEOMETRY
PAIR_NONCLOSURE != CURVATURE
```

Elle renforce seulement la nécessité de conserver le datum modulaire
complet `K_n` dans tout travail `T5` ultérieur, sans jamais lui
substituer une troncature par paire.

---

## 7. Pare-feu scientifique

```text
T5_FLOW_PASS != T5_PASS
T5_FLOW_PASS != T4_PASS

T5_FLOW_PASS != CONTINUUM
T5_FLOW_PASS != LOCAL_GEOMETRIC_GENERATOR
T5_FLOW_PASS != METRIC_RECONSTRUCTION
T5_FLOW_PASS != RIEMANN_CURVATURE
T5_FLOW_PASS != GRAVITY
T5_FLOW_PASS != DIMENSIONAL_CALIBRATION

FINITE_SCALE_RUNNING != CONTINUUM

DECIMATION_LEVEL != PHYSICAL_LENGTH_SCALE

PAIR_TRUNCATION_FLOW_OBSERVATION != PHYSICAL_GEOMETRY
```

---

## 8. Frontières ouvertes après `model1b`

Recopiées fidèlement comme frontières ouvertes, sans résolution dans ce
rapport :

```text
T5_OPEN_1 = INTRINSIC_LOCAL_OR_REFINEMENT_NOTION
T5_OPEN_2 = NONTRIVIAL_NESTED_OR_INFINITE_LIMIT
T5_OPEN_3 = EVENTUAL_LOCAL_OR_CONTINUUM_GENERATOR
T5_OPEN_4 = EFFECTIVE_CONTINUOUS_GEOMETRY
T5_OPEN_5 = CROSS_SCALE_G3_G4_REQUALIFICATION_WHEN_REQUIRED
T5_OPEN_6 = G8_CONTINUUM_CORRESPONDENCE
T5_OPEN_7 = NONCLASSICALITY_FIREWALL_BEFORE_PHYSICAL_QUANTUM_GEOMETRY
```

Contrainte structurelle héritée :

```text
FULL_K_n_MUST_REMAIN_CANONICAL = TRUE
PAIR_ONLY_COARSE_DATUM         = FORBIDDEN_AS_EXACT_ROUTE
```

---

## 9. Prochaine cible scientifique

Cette clôture n'autorise directement aucun nouveau toy.

```text
NEXT_MODEL = NOT_YET_AUTHORIZED
NEXT_TOY   = NOT_YET_AUTHORIZED

NEXT_SCIENTIFIC_TARGET = T5_FULL_PASS_BOUNDARY_AND_LOCAL_LIMIT_FEASIBILITY
```

L'étape scientifique suivante doit être une analyse/critérisation
distincte déterminant quelles portes minimales permettraient de passer
de `T5_FLOW_PASS` à un candidat `T5_PASS`, en particulier autour de :

- famille de raffinements contrôlée/emboîtée ;
- notion intrinsèque de pas de raffinement sans introduire de longueur ;
- limite non triviale ;
- existence éventuelle d'un générateur local du flux ;
- compatibilité inter-échelles de la structure directionnelle ;
- requalification `G3`/`G4` ;
- frontière `G8` continuum.

Aucune solution particulière n'est imposée par ce rapport de clôture.

---

## 10. Portée du présent document

Ce rapport n'établit, ne modifie et ne reformule aucune décision
scientifique. Il n'est pas une source normative concurrente de
`docs/toy-models/toy1b/validation-plan.md` (`FROZEN`) ni de
`experiments/toy1b/toy1b.ipynb` (run confirmatoire accepté) : il en
constitue un résumé de clôture fidèle, borné au périmètre
`MODEL1B-T5-FLOW-CONFIRMATORY-CLOSURE-1`.
