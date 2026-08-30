# toy1c — Conception d'implémentation (model1c)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model1c`, sur la base de `docs/toy-models/toy1c/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune fixture numérique de qualification au-delà des seeds déjà fermées par la spécification, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun verdict `T5a`/`T5`.

```text
MODEL1C_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

T5A_PASS = NOT_ESTABLISHED
T5_PASS  = NOT_ESTABLISHED

IMPLEMENTATION   = NOT_AUTHORIZED
VALIDATION_PLAN  = NOT_AUTHORIZED
NEXT_MODEL       = NOT_AUTHORIZED
```

---

## 1. Périmètre

Ce document couvre :

- l'audit des primitives `core` déjà disponibles et directement réutilisables (§2) — aucune nouvelle promotion `core` n'est proposée par ce lot ;
- l'arborescence cible minimale du paquet `model1c` (§3) ;
- le design minimal de l'algèbre de Bell locale, de la cellule de raffinement `R_cell` et de sa carte réduite dérivée `Phi` (spécification §5–§7, pour `algebra.py`/`local_cell.py`) ;
- le design de l'oracle analytique fermé (`Phi` fermé, `Phi^n` fermé) utilisé exclusivement comme oracle de test indépendant, jamais en production (spécification §7, §12, pour `oracle.py`) ;
- le design de l'extraction canonique le long de la branche `c_n = 0^n`, licite par le lemme de fermeture §10 de la spécification, sans jamais construire l'espace global `H_n` pour ce calcul (pour `refinement.py`) ;
- le design borné d'une construction multi-cellules explicite, réservée aux contrôles corroboratifs de fermeture structurelle à quelques niveaux seulement (spécification §10, `refinement.py`) ;
- les diagnostics de non-trivialité et de fidélité (spécification §13, §16, pour `diagnostics.py`) ;
- l'architecture de test prévue, sans exécution ni valeur numérique canonique au-delà des seeds déjà fermés par la spécification (§9 ci-dessous).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les valeurs `KAPPA_VALUES_BEYOND_0_AND_1_4` (spécification §24) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire d'acceptation ;
- le plan de validation ;
- un critère d'acceptation de `model1c`, de `T5a` ou de `T5`.

---

## 2. Primitives `core` existantes réutilisées

`model1c` réutilise, sans modification, le mécanisme déjà établi dans `cosmotgg.core` :

- `cosmotgg.core.states.validate_density_matrix` — validation fail-closed d'une matrice densité, tolérances explicites sans valeur par défaut ; utilisée pour valider tout seed \(\rho_0\) (fidèle ou non, `require_faithful` selon le contexte) avant construction ;
- `cosmotgg.core.states.partial_trace` — trace partielle exacte sur un produit tensoriel explicite de dimensions locales ; utilisée pour l'extraction canonique \(I_n\) (spécification §9) et pour la trace `Tr_new` dérivant `Phi` de `R_cell` (spécification §7) ;
- `cosmotgg.core.states.embed_operator` — incorporation d'un opérateur fini sur des facteurs tensoriels déclarés arbitraires ; utilisée pour construire l'unitaire contrôlé `U` (spécification §6) sur \(H_c\otimes H_c\) à partir des blocs `g` et pour construire, aux niveaux corroboratifs bornés, la construction multi-cellules explicite de `G_n` (§6 ci-dessous).

Aucune nouvelle primitive `core` n'est requise : `model1c` ne construit ni logarithme ni exponentielle matricielle (`Phi`/`R_cell` sont des combinaisons positives explicites de conjugaisons unitaires, spécification §6–§7), contrairement à `model0d`/`model1b`.

```text
CORE_PROMOTION_PROPOSED_THIS_LOT = NONE
CODE_MODIFIED_THIS_LOT           = FALSE
```

---

## 3. Arborescence cible minimale

```text
src/cosmotgg/models/model1c/__init__.py
src/cosmotgg/models/model1c/algebra.py
src/cosmotgg/models/model1c/local_cell.py
src/cosmotgg/models/model1c/oracle.py
src/cosmotgg/models/model1c/refinement.py
src/cosmotgg/models/model1c/diagnostics.py

tests/models/model1c/__init__.py
tests/models/model1c/test_algebra.py
tests/models/model1c/test_local_cell.py
tests/models/model1c/test_oracle.py
tests/models/model1c/test_refinement.py
tests/models/model1c/test_diagnostics.py
```

Ce découpage en cinq modules peut être réduit par le rôle `code` si une conception plus simple et propre le justifie, sans changer la définition normative des responsabilités scientifiques ci-dessous.

Aucun des éléments suivants n'est introduit :

```text
graph library
scipy dependency
symbolic algebra dependency
new framework
class Model1C
```

```text
MODEL1C_PRODUCTION_IMPORTS_PRIOR_MODELS = NO
```

---

## 4. Responsabilité de `model1c/algebra.py`

Responsabilité scientifique strictement bornée à la spécification §5 :

- pile de Pauli locale \(\{I,X,Y,Z\}\) sur un facteur qubit (même motif que `model1b/modular_support.py`, sans promotion `core`, propre au modèle) ;
- les quatre générateurs de Bell \(G_{\mathrm{BELL}} = \{II, XX, ZZ, YY\}\) comme opérateurs \(4\times4\) explicites sur \(H_c=\mathbb C^2\otimes\mathbb C^2\) ;
- les quatre projecteurs de Bell \(\Pi_k\) (base de Bell standard), avec un contrôle de régression vérifiant \(\sum_k \Pi_k = I\) et l'orthogonalité deux-à-deux ;
- une fonction `p_bell(rho)` implémentant la forme fermée \(P_{\mathrm{BELL}}(\rho) = \tfrac14\sum_g g\rho g^\dagger\), avec contrôle de régression croisé contre la forme `sum_k Pi_k rho Pi_k` (identité algébrique, spécification §5, §7).

`p_bell` sert exclusivement d'**oracle analytique** (§6 ci-dessous) : elle n'est jamais appelée par la construction en production de `R_cell`/`Phi` (§5).

Ce module ne construit aucune ancilla, aucun unitaire contrôlé, aucune règle de raffinement.

---

## 5. Responsabilité de `model1c/local_cell.py`

Responsabilité scientifique strictement bornée à la spécification §6–§7 :

- ancilla \(\alpha = \operatorname{diag}(5/8,1/8,1/8,1/8)\) dans la base indexée par \(G_{\mathrm{BELL}}\) (constante fixe, aucun paramètre) ;
- unitaire contrôlé \(U = \sum_g g\otimes|g\rangle\langle g|\) sur \(H_c\otimes H_c\) (dimension 16), construit via `embed_operator`/somme explicite des quatre blocs `g` sur les sous-espaces orthogonaux \(|g\rangle\langle g|\) ;
- `local_refinement_cell(rho)` = \(R_{\mathrm{cell}}(\rho) = U(\rho\otimes\alpha)U^\dagger\), **production**, CPTP par construction (spécification §6) ; retourne l'état joint des deux cellules filles (dimension 16) ;
- `phi(rho)` = \(\Phi(\rho) = \mathrm{Tr}_{\mathrm{new}}[R_{\mathrm{cell}}(\rho)]\), **dérivée de `local_refinement_cell` via `cosmotgg.core.states.partial_trace`** (`keep` = la cellule « système », trace la cellule « nouvelle ») — jamais raccourcie vers la forme fermée `p_bell` (spécification §7 : `Phi ne doit JAMAIS être introduite comme loi indépendante`).

Ce module ne construit aucune multi-cellule, aucun diagnostic.

```text
PHI_PRODUCTION_PATH = local_refinement_cell -> partial_trace (via core)
PHI_CLOSED_FORM_PATH = oracle.py ONLY (jamais en production)
```

---

## 6. Responsabilité de `model1c/refinement.py`

Responsabilité scientifique strictement bornée à la spécification §8–§10 :

### 6.1 Extraction canonique (production, tout `n`)

- `canonical_branch_sequence(seed, n_max)` : calcule \(I_0(\rho_0),\dots,I_{n_{\max}}(\rho_{n_{\max}})\) le long de la branche canonique \(c_n=0^n\) **exclusivement par itération de `local_cell.phi`** sur un unique état de cellule (dimension 4), c'est-à-dire \(I_n(\rho_n) = \Phi^n(\rho_0)\), en application directe du lemme de fermeture démontré (spécification §10). Aucun espace global `H_n` (dimension \(4^{2^n}\)) n'est jamais construit par cette fonction, à aucun `n`, y compris grand.

```text
CANONICAL_BRANCH_COMPUTATION = ITERATED_PHI_ON_SINGLE_CELL
LICENSED_BY                  = CLOSURE_LEMMA (spécification §10, démontrée
                                analytiquement, pas supposée)
NO_GLOBAL_H_N_CONSTRUCTION_FOR_THIS_PATH = TRUE
```

### 6.2 Construction multi-cellules explicite (corroborative, `n` borné)

- `global_refinement(rho_n, n)` : construit explicitement \(G_n(\rho_n)\) (spécification §8) en appliquant `local_cell.local_refinement_cell` **indépendamment à chaque cellule** du niveau `n`, avec une ancilla fraîche par cellule, puis en réordonnant les facteurs tensoriels vers l'ordre canonique du niveau `n+1` (`embed_operator`/permutation explicite, jamais de tri implicite). Cette fonction est réservée aux contrôles corroboratifs de fermeture structurelle (§9 ci-dessous) et n'est jamais utilisée pour calculer la branche canonique à grand `n`.

```text
GLOBAL_REFINEMENT_SCOPE = STRUCTURAL_CLOSURE_CORROBORATION_ONLY
GLOBAL_REFINEMENT_BOUNDED_LEVELS = n = 0 -> 1 (dimension 4 -> 16),
                                    éventuellement n = 1 -> 2 (16 -> 256) ;
                                    aucune revendication de preuve à ces
                                    niveaux (spécification §12 : la preuve
                                    est analytique, EVIDENCE_CLASS = A)
```

Ce module n'importe ni `model0a`–`model0e`, ni `model1a`, ni `model1b`.

---

## 7. Responsabilité de `model1c/oracle.py`

Responsabilité scientifique strictement bornée à la spécification §7, §12 :

- `phi_closed_form(rho)` = \(\tfrac12\rho + \tfrac12\,P_{\mathrm{BELL}}(\rho)\) (via `algebra.p_bell`) ;
- `phi_pow_closed_form(rho, n)` = \(P_{\mathrm{BELL}}(\rho) + 2^{-n}(\rho - P_{\mathrm{BELL}}(\rho))\) ;
- ces deux fonctions sont des **oracles analytiques indépendants**, utilisés uniquement dans les tests pour confirmer que `local_cell.phi` (production) coïncide exactement avec la forme fermée, et que l'itération de `local_cell.phi` (production, §6.1) coïncide exactement avec `phi_pow_closed_form` à tout `n` testé — jamais appelées par le chemin de production lui-même.

```text
ORACLE_ROLE = INDEPENDENT_CROSS_CHECK_ONLY
ORACLE_NEVER_CALLED_BY_PRODUCTION_PATH = TRUE
```

---

## 8. Responsabilité de `model1c/diagnostics.py`

Responsabilité scientifique strictement bornée à la spécification §13, §15–§16 :

- `connected_xx_correlator(rho)` = \(C_{XX}(\rho) = \mathrm{Tr}[XX\rho] - \mathrm{Tr}[XI\rho]\,\mathrm{Tr}[IX\rho]\) (séparateur analytique de non-trivialité, spécification §13) ;
- vérification de fidélité stricte (spectre minimal strictement positif) le long de la branche canonique, sans pseudo-inverse, sans clipping, sans régularisation silencieuse (spécification §16) — délègue la validation structurelle à `cosmotgg.core.states.validate_density_matrix(require_faithful=True, ...)` ;
- comparaison de séparation Bell pour deux seeds admissibles (`algebra.p_bell(sigma_a) - algebra.p_bell(sigma_b)`), support du contrôle anti-collapse (spécification §15).

Ce module ne construit aucune cellule, aucune règle de raffinement, aucun oracle fermé.

---

## 9. Architecture de test — proposition, sans exécution ni valeur canonique

**Tests unitaires `model1c` (`algebra.py`) :**

- \(G_{\mathrm{BELL}}\) unitaire, hermitien, involutif (\(g^2=I\)) pour chaque générateur ;
- \(\sum_k \Pi_k = I\), orthogonalité des \(\Pi_k\), idempotence \(P_{\mathrm{BELL}}^2=P_{\mathrm{BELL}}\) (régression numérique de l'identité algébrique, spécification §12) ;
- équivalence exacte `p_bell` via `sum_g` et via `sum_k Pi_k(.)Pi_k`.

**Tests unitaires `model1c` (`local_cell.py`) :**

- `U` unitaire (\(U^\dagger U = I\)) ;
- `local_refinement_cell` CPTP (trace préservée, positivité préservée) sur un échantillon d'états admissibles ;
- `phi` (production, via trace partielle de `local_refinement_cell`) coïncide exactement avec `oracle.phi_closed_form` (contrôle de régression, spécification §7) ;
- fidélité stricte préservée par `local_refinement_cell`/`phi` sur seed fidèle (spécification §16) ; comportement fail-closed sur seed hors domaine `D(H_c)` (délégué à `validate_density_matrix`).

**Tests unitaires `model1c` (`refinement.py`) :**

- **fermeture structurelle** (`CLOSE-FAIL` négatif attendu absent) : à `n=0 -> 1` (et, si tractable, `1 -> 2`), `refinement.canonical_branch_sequence` coïncide exactement avec la réduction de `refinement.global_refinement` à la cellule canonique — contrôle corroboratif borné du lemme de fermeture déjà démontré analytiquement (spécification §10), jamais présenté comme la preuve elle-même ;
- `canonical_branch_sequence` coïncide exactement, à tout `n` testé, avec `oracle.phi_pow_closed_form` appliqué au seed (spécification §12) ;
- oracle négatif `N6` : toute tentative de faire varier `alpha`/`U` par niveau dans `refinement.py` doit être absente de la conception de production (contrôle de conception, pas seulement de test) ;
- oracle négatif `N3` : le verdict de convergence ne dépend pas du nom/de l'étiquetage de `n` (relabellisation pure).

**Tests unitaires `model1c` (`diagnostics.py`) :**

- oracle négatif `N1` : `canonical_branch_sequence(sigma_0_null, n)` \(\to I/4\), `connected_xx_correlator \to 0` ;
- `LOCAL-ONLY` : seed portant `XI` sans `XX` (\(\kappa=0\)) \(\to\) `connected_xx_correlator` \(\to 0\) à la limite ;
- `RELATIONAL-LIVE` : seed canonique (\(\kappa=1/4\)) \(\to\) `connected_xx_correlator \to 1/4\) exactement (comparaison exacte, pas de tolérance de plateau) ;
- oracle négatif `N9` (anti-collapse) : pour deux \(\kappa\) admissibles distincts pré-déclarés (au minimum \(\{0, 1/4\}\)), \(P_{\mathrm{BELL}}(\sigma_a) \neq P_{\mathrm{BELL}}(\sigma_b)\) et cette différence ne décroît pas vers zéro le long de `canonical_branch_sequence` (comparaison à plusieurs `n` croissants, vérification que la différence converge vers la valeur constante non nulle attendue, spécification §15) ;
- fidélité stricte à la limite pour le seed canonique (spécification §16).

**Contrôle négatif de conception (`CLOSE-FAIL`, non exécuté en production) :**

- documenté comme un scénario alternatif hors périmètre (spécification §21) : ancilla partagée entre deux cellules, ou couplage direct de deux `U_b` distincts. Ce module ne l'implémente pas dans le chemin de production ; un test dédié, s'il est ajouté, doit être clairement marqué `NEGATIVE_CONTROL`/hors périmètre `model1c`, jamais confondu avec `global_refinement` (§6.2).

Aucune fixture confirmatoire dans les tests unitaires ordinaires, sauf déclarée séparément non confirmatoire.

---

## 10. Diagnostics et contrôles — statut de conception

```text
PRIMARY_CLAIM_OBJECT   = I_n(rho_n) in D(H_c), branche canonique c_n=0^n
CLOSURE_MECHANISM      = I_{n+1} o G_n = Phi o I_n (démontré, spécification §10)
LIMIT_OBJECT            = sigma_infinity = P_BELL(rho_0), exact
NONTRIVIALITY_ORACLE    = C_XX(rho) = <XX> - <XI><IX>
ANTI_COLLAPSE_ORACLE    = P_BELL(sigma_a) != P_BELL(sigma_b), différence
                          non évanescente sous I_n
FAIL_CLOSED_DOMAIN      = D(H_c) via validate_density_matrix, aucune
                          pseudo-inverse, aucun clipping
```

Aucun seuil scientifique n'est fixé par ce document ; les tolérances numériques d'un futur protocole restent `OPEN` (spécification §24).

---

## 11. Gel documentaire

```text
TOY_IMPLEMENTATION_DOCUMENT_FREEZE = ENABLED
```

Au premier lot de code de `model1c`, ce document et `docs/toy-models/toy1c/specification.md` deviendront `READ_ONLY_DURING_IMPLEMENTATION`, réouverts uniquement pour un blocage fondamental démontré (`docs/governance/documentation-governance.md` §11.1–§11.2). Ce lot ne les gèle pas encore : ils restent `PROPOSED`, en attente de revue ChatGPT.

Après démarrage de l'implémentation :

```text
MARKDOWN_NORMATIVE = CONTRACT
PYTHON_CODE        = MECHANISM
NOTEBOOK           = EXECUTABLE_EXPERIMENTAL_NARRATIVE
```

---

## 12. Paramètres non fermés par ce document

```text
KAPPA_VALUES_BEYOND_0_AND_1_4        = OPEN
NUMERICAL_TOLERANCES                 = OPEN
MODEL1C_ACCEPTANCE_CRITERION         = OPEN
T5A_CONFIRMATORY_PROTOCOL            = NOT_DEFINED
T5A_QUALIFICATION                    = NOT_EXECUTED
```

---

## 13. Statut et prochaine étape

```text
MODEL1C_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

T5A_PASS = NOT_ESTABLISHED
T5_PASS  = NOT_ESTABLISHED

IMPLEMENTATION   = NOT_AUTHORIZED
VALIDATION_PLAN  = NOT_AUTHORIZED
NEXT_MODEL       = NOT_AUTHORIZED
```

Aucun gel automatique. Aucune implémentation automatique.

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
