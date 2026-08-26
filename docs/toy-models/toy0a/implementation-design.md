# toy0a — Conception d'implémentation (model0a)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model0a`, sur la base de `docs/toy-models/toy0a/specification.md` (§2–§3) et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucun domaine du paramètre modulaire \(s\) et aucun critère ou verdict T1.

---

## 1. Périmètre

Ce lot de conception couvre uniquement la construction de la famille d'états de `model0a` (`docs/toy-models/toy0a/specification.md` §3) et son assemblage à partir des primitives `core` existantes.

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les valeurs numériques de `a, b, c, eta` ;
- le domaine ou les valeurs du paramètre modulaire `s` ;
- les tolérances numériques d'un futur protocole ;
- le plan de validation ;
- un critère d'acceptation de `model0a` ou de T1.

---

## 2. Primitives `core` réutilisées

Conformément à `docs/governance/software-architecture-governance.md` §1–§6, `model0a` est un **consommateur** de `core` et ne redéfinit aucune brique générique.

Sont réutilisées telles quelles :

```text
cosmotgg.core.states.validate_density_matrix
cosmotgg.core.states.partial_trace

cosmotgg.core.information.log_density_difference
cosmotgg.core.information.mutual_information

cosmotgg.core.modular.finite_connes_cocycle
```

Aucun wrapper `R_AB` n'est créé dans `core` ni dans `model0a` : un consommateur obtient la quantité notée `R_AB` par `docs/model/hypothesis.md` en appelant `cosmotgg.core.information.log_density_difference(rho_AB, sigma_AB, ...)`, conformément à la décision déjà enregistrée dans `docs/governance/current-task.md` (`R_AB_CODE_CLASSIFICATION = NO_PROJECT_SPECIFIC_PRIMITIVE_YET`).

```text
MODEL0A-CORE-COCYCLE-1 = IMPLEMENTED

CORE_COCYCLE_HEAD  = 094feb0966c0ca8e885ff3a90dbb7ea6fcec188d
CORE_COCYCLE_TESTS = PASS
```

La primitive `cosmotgg.core.modular.finite_connes_cocycle` est consommée par `model0a` ; elle n'est pas redéfinie.

---

## 3. Arborescence cible minimale

```text
src/cosmotgg/models/__init__.py
src/cosmotgg/models/model0a/__init__.py
src/cosmotgg/models/model0a/states.py

tests/models/model0a/test_states.py
```

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model0A
```

---

## 4. Responsabilité de `model0a/states.py`

La responsabilité scientifique propre à ce module est strictement bornée à la famille d'états de `docs/toy-models/toy0a/specification.md` §3 :

- construire \(\rho_{AB}(a,b,c,\eta)\) selon la matrice normative du §3 ;
- déclarer et valider son domaine analytique (§3.2), de façon fail-closed et sans tolérance numérique implicite ;
- fournir, si utile, ses marginales via les primitives `core` (`cosmotgg.core.states.partial_trace`) ;
- fournir \(\sigma_{AB} = \rho_A \otimes \rho_B\) par assemblage explicite.

Ce module ne réimplémente pas :

```text
logarithme matriciel
modular Hamiltonian
cocycle
mutual information
partial trace
```

Ces briques restent exclusivement dans `cosmotgg.core`.

### 4.1 Validation du domaine analytique

La construction échoue (fail-closed) sur des paramètres `a, b, c, eta` hors du domaine analytique normatif défini par `docs/toy-models/toy0a/specification.md` §3.2. Cette définition de domaine est celle de la spécification ; elle n'est ni approximée ni assouplie par une tolérance numérique locale au module.

Les futures tolérances numériques d'un protocole d'exécution (validation de la matrice produite, hermiticité, trace, positivité via `cosmotgg.core.states.validate_density_matrix`) restent des contrôles d'implémentation distincts de cette validation de domaine analytique, et ne la redéfinissent pas.

---

## 5. API proposée

Une seule fonction paramétrique couvre les trois régimes canoniques (§3.3 de la spécification), plutôt que trois constructeurs séparés :

```text
two_qubit_fixed_marginal_correlation_state(a, b, c, eta)
```

Ce nom technique reprend l'identifiant `STATE_FAMILY = TWO_QUBIT_FIXED_MARGINAL_CORRELATION_FAMILY` de la spécification à des fins de traçabilité ; il ne porte aucune sémantique scientifique supplémentaire par rapport à celle-ci. Le rôle `code` reste libre d'ajuster ce nom lors de l'implémentation, dans la mesure où il reste descriptif et ne modifie pas le sens de la construction.

Les tranches N0/N1/N2 (§3.3 de la spécification) sont obtenues par choix des arguments (`c = eta = 0` pour N0, `c != 0, eta = 0` pour N1, `eta != 0, a + b != 1` pour N2) plutôt que par des fonctions dédiées séparées.

---

## 6. Tests prévus (`tests/models/model0a/test_states.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

- trace analytique égale à 1 ;
- marginales exactes attendues (\(\rho_A=\operatorname{diag}(a,1-a)\), \(\rho_B=\operatorname{diag}(b,1-b)\)) ;
- indépendance de \(\sigma_{AB}\) vis-à-vis de \(c\) et \(\eta\) à \(a,b\) fixés ;
- identité produit N0 ;
- commutation N1 (`COMMUTING_CORRELATED_REGIME`) ;
- non-commutation N2 lorsque \(\eta \neq 0\) et \(a+b \neq 1\) ;
- fidélité pour des paramètres admissibles (domaine §3.2) ;
- rejet des paramètres hors domaine.

Les tests pourront utiliser des valeurs déterministes purement unitaires/de développement, explicitement marquées :

```text
NON_NORMATIVE_TEST_FIXTURE
```

Ces valeurs ne constituent pas des `STATE_PARAMETER_VALUES` au sens de la spécification (§15), qui restent `OPEN`.

---

## 7. Paramètres non fermés par ce document

```text
STATE_PARAMETER_VALUES        = OPEN
MODULAR_PARAMETER_DOMAIN      = OPEN
NUMERICAL_TOLERANCES          = OPEN
T1_NONTRIVIALITY_CRITERION    = OPEN
MODEL0A_ACCEPTANCE_CRITERION  = OPEN
CONFIRMATORY_PROTOCOL         = NOT_DEFINED
```

---

## 8. Statut et prochaine étape

```text
MODEL0A_IMPLEMENTATION_DESIGN = PROPOSED
```

La prochaine étape autorisée est l'implémentation bornée de la famille d'états de `model0a` par le rôle `code` (Claude Sonnet 5).
