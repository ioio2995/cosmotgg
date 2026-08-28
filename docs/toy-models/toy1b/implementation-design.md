# toy1b — Conception d'implémentation (model1b)

**Statut : `PROPOSED_MODEL1B_T5_FLOW_DESIGN`.**

```text
STATUS                 = PROPOSED_MODEL1B_T5_FLOW_DESIGN
NOT_FROZEN              = TRUE
CHATGPT_REVIEW          = CONSISTENCY_FIX_INTEGRATED_PENDING_FINAL_CONFIRMATION
IMPLEMENTATION          = NOT_AUTHORIZED
CONFIRMATORY_EXECUTION  = NOT_AUTHORIZED
VALIDATION_PLAN         = NOT_CREATED
T5_FLOW_QUALIFICATION   = NOT_EXECUTED
```

Ce document décrit l'architecture logicielle cible minimale de `model1b`, sur la base de `docs/toy-models/toy1b/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune fixture numérique canonique, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun verdict `T5-FLOW`/`T5`.

---

## 1. Périmètre

Ce document couvre :

- l'audit architectural obligatoire des primitives `core` réutilisées et les deux promotions `core` proposées (§2–§3) ;
- l'arborescence cible minimale du paquet `model1b` (§4) ;
- le design minimal de l'état de Gibbs relationnel fin et de la hiérarchie de décimation (spécification §5–§7 pour `states.py`/`hierarchy.py`) ;
- le design minimal de la donnée modulaire canonique, de la représentation de support de Pauli et du bloc modulaire à deux corps (spécification §9–§11 pour `modular_support.py`) ;
- le design minimal du facteur polaire directionnel, de l'objet de boucle et des diagnostics invariants de jauge (spécification §12–§14, §18, §20 pour `directional.py`) ;
- l'architecture de test prévue, sans exécution ni valeur numérique canonique (§9 ci-dessous).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les fixtures numériques de qualification (`MODEL1B_QUALIFICATION_FIXTURES`, spécification §24) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire d'acceptation ;
- le plan de validation ;
- un critère d'acceptation de `model1b`, de `T5-FLOW` ou de `T5`.

---

## 2. Primitives `core` existantes réutilisées

`model1b` réutilise le mécanisme déjà établi dans `cosmotgg.core` :

- `cosmotgg.core.states.validate_density_matrix` — validation fail-closed d'une matrice densité, tolérances explicites sans valeur par défaut ;
- `cosmotgg.core.states.partial_trace` — trace partielle exacte sur un produit tensoriel explicite de dimensions locales, utilisée pour toutes les réductions \(\rho_1 = \mathrm{Tr}_{P,Q}(\rho_2)\), \(\rho_0 = \mathrm{Tr}_{X,Y}(\rho_1)\), et le contrôle direct \(\rho_{0,\mathrm{direct}} = \mathrm{Tr}_{P,Q,X,Y}(\rho_2)\) (spécification §6) ;
- `cosmotgg.core.modular.modular_hamiltonian` — \(K = -\log(\rho)\) pour un état fidèle, utilisée pour \(K_n\) à chaque niveau (spécification §9) ; sur le domaine \(\rho_2 > 0\) construit par construction (spécification §8), aucun état non fidèle n'est attendu sur la route déclarée.

Ces primitives sont déjà `established` (`SCIENTIFIC_METADATA.status = "established"`) et ne sont pas modifiées par ce document.

---

## 3. Promotions `core` proposées

Conformément à `docs/governance/software-architecture-governance.md` §3 et §8, deux additions génériques sont proposées :

### 3.1 `cosmotgg.core.states.embed_operator`

Incorpore un opérateur fini sur des facteurs tensoriels déclarés arbitraires, avec ordonnancement déterministe et gardes de dimension.

Justification `core` : cette opération ne code aucune identité de modèle, aucune constante nommée, aucune topologie particulière ; elle généralise le motif déjà répété indépendamment dans `model0e/states.py` (`_embed`) et `model1a/states.py` (`_embed_ab`/`_embed_bc`/`_embed_cd`/`_embed_da`), et est requise ici pour incorporer \(S_e(M_e)\) sur chacune des huit arêtes fines de \(\Gamma_2\) (spécification §5, §8), avec en particulier une arête (\(DA\)) dont l'ordre tensoriel naturel diffère de l'ordre global, comme déjà rencontré pour `model1a` (`docs/toy-models/toy1a/specification.md` §6–§7).

**Sémantique d'ordre de `positions`.** Pour `embed_operator(operator, dimensions, positions)`, l'ordre de `positions` est l'ordre des facteurs tensoriels de `operator` lui-même. Exemple : `operator_DA` agit sur \(\mathcal H_D \otimes \mathcal H_A\), donc `positions=(D, A)` signifie que le premier facteur local de `operator_DA` appartient à \(D\) et le second à \(A\). L'implémentation doit ensuite permuter explicitement le résultat vers l'ordre tensoriel global canonique.

```text
POSITIONS_ORDER                                = OPERATOR_TENSOR_FACTOR_ORDER
GLOBAL_PLACEMENT                               = EXPLICIT_PERMUTATION_TO_CANONICAL_GLOBAL_ORDER
POSITIONS_SORTING_WITHOUT_OPERATOR_PERMUTATION = FORBIDDEN
```

Aucun tri implicite de l'ordre sémantique des sous-systèmes. Ceci est en particulier obligatoire pour l'arête \(DA\).

### 3.2 `cosmotgg.core.modular.hermitian_exp`

Exponentielle spectrale d'une matrice hermitienne finie, sans dépendance `scipy`, préservant l'hermiticité.

Justification `core` : requise pour \(\rho_2 = \exp(H_{\mathrm{rel}})/\mathrm{Tr}[\exp(H_{\mathrm{rel}})]\) (spécification §8), avec \(H_{\mathrm{rel}}\) hermitien et fini. Distincte de `hermitian_log`/`_hermitian_power` déjà présents dans `cosmotgg.core.modular` (exposant réel spectral, pas d'exponentielle) et de `_modular_unitary` (exponentielle du produit \(i \times \text{hermitien} \times s\), pas de l'hermitien lui-même) : aucune primitive existante ne couvre `exp(H)` pour \(H\) hermitien fini. Générique, indépendante de toute construction `model1b`.

`hermitian_exp` reste un candidat `core` générique et n'implémente aucun décalage spectral par elle-même : le décalage \(H_{\mathrm{shifted}} = H_{\mathrm{rel}} - \lambda_{\max} I\) de stabilité numérique (spécification §8, identité exacte sous normalisation) appartient à la construction de l'état de Gibbs propre à `model1b` (`states.py`, §6 ci-dessous), pas à la primitive `core` elle-même.

Aucune infrastructure générique supplémentaire n'est introduite au seul motif de l'abstraction.

```text
CORE_PROMOTION_PROPOSED_1 = embed_operator (cosmotgg.core.states)
CORE_PROMOTION_PROPOSED_2 = hermitian_exp (cosmotgg.core.modular)
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
CODE_MODIFIED_THIS_LOT           = FALSE
```

Si un audit `docs` ultérieur identifie une frontière `core`/`model1b` plus étroite, il est rapporté pour revue ChatGPT ; il ne modifie pas silencieusement le contrat scientifique ci-dessus.

---

## 4. Frontière de promotion `core`

```text
GENERIC_ESTABLISHED_MATH        vs.  MODEL1B_SCIENTIFIC_CONSTRUCTION
```

Générique (candidats `core`, §3) :

```text
embed_operator
hermitian_exp
```

Propre à `model1b` (reste dans `models/model1b`) :

```text
Pauli support decomposition for this qubit toy
J block extraction
directional polar domain policy
loop diagnostics
tree oracle
hierarchy bookkeeping
Gibbs fixtures
```

Aucune physique propre à `model1b` n'est promue vers `core`.

---

## 5. Arborescence cible minimale

```text
src/cosmotgg/models/model1b/__init__.py
src/cosmotgg/models/model1b/states.py
src/cosmotgg/models/model1b/hierarchy.py
src/cosmotgg/models/model1b/modular_support.py
src/cosmotgg/models/model1b/directional.py

tests/models/model1b/__init__.py
tests/models/model1b/test_states.py
tests/models/model1b/test_hierarchy.py
tests/models/model1b/test_modular_support.py
tests/models/model1b/test_directional.py
```

Ce découpage en quatre modules peut être réduit par le rôle `code` si une conception plus simple et propre le justifie, sans changer la définition normative des responsabilités scientifiques ci-dessous.

Aucun des éléments suivants n'est introduit :

```text
graph library
scipy dependency
symbolic algebra dependency
new framework
class Model1B
```

`model1b` n'importe aucune API `model0a`–`model0e`/`model1a` en production :

```text
MODEL1B_PRODUCTION_IMPORTS_PRIOR_MODELS = NO
```

---

## 6. Responsabilité de `model1b/states.py`

Responsabilité scientifique strictement bornée à la spécification §5, §8 :

- \(S_e(M_e) = 4\,P_e(M_e) - I_e\) sur les huit arêtes fines déclarées de \(\Gamma_2\), en utilisant `embed_operator` (§3.1) pour l'incorporation sur les facteurs tensoriels déclarés ; pour l'arête \(DA\), `positions=(D, A)` (ordre tensoriel de \(S_{DA}(M_{DA})\)) puis permutation explicite du résultat vers l'ordre tensoriel global canonique (§3.1) — aucun tri implicite ;
- construction déterministe du graphe fin (huit sites \((A,X,Y,B,C,P,Q,D)\), huit arêtes `AX,XY,YB,BC,CP,PQ,QD,DA`) ;
- état de Gibbs relationnel fin \(\rho_2 = \exp(H_{\mathrm{rel}})/\mathrm{Tr}[\exp(H_{\mathrm{rel}})]\), \(H_{\mathrm{rel}} = \sum_e \theta_e S_e(M_e)\), calculé via la construction numériquement stable \(H_{\mathrm{shifted}} = H_{\mathrm{rel}} - \lambda_{\max} I\) puis `hermitian_exp` (§3.2, spécification §8, identité exacte sous normalisation).

Ce module ne construit aucune réduction, aucune donnée modulaire, aucun diagnostic directionnel.

---

## 7. Responsabilité de `model1b/hierarchy.py`

Responsabilité scientifique strictement bornée à la spécification §6 :

- étiquetage et ordre fixes des sites fins \((A,X,Y,B,C,P,Q,D)\) ;
- ensembles cumulés \(E_2=\varnothing\), \(E_1=\{P,Q\}\), \(E_0=\{P,Q,X,Y\}\) ;
- réductions \(\rho_1 = \mathrm{Tr}_{P,Q}(\rho_2)\), \(\rho_0 = \mathrm{Tr}_{X,Y}(\rho_1)\), via `cosmotgg.core.states.partial_trace` ;
- contrôle direct \(\rho_{0,\mathrm{direct}} = \mathrm{Tr}_{P,Q,X,Y}(\rho_2)\), même primitive, sans logique de composition dupliquée.

Ce module ne construit aucune donnée modulaire, aucun diagnostic directionnel.

---

## 8. Responsabilité de `model1b/modular_support.py`

Responsabilité scientifique strictement bornée à la spécification §9–§11 :

- \(K_n = -\log(\rho_n)\) via `cosmotgg.core.modular.modular_hamiltonian`, à chaque niveau (§9) ;
- coefficients de Pauli complets \(c_s(K_n) = 2^{-N_n}\,\mathrm{Tr}[K_n P_s]\), sans troncature de poids (§10) ;
- poids de support \(w(s)\) et normes \(W_w(K_n)\) (§10), diagnostics de bookkeeping ;
- extraction du bloc modulaire global \(J_{i\leftarrow j}^{ab}(K_n) = -2^{-N_n}\,\mathrm{Tr}[K_n \sigma_a^{(i)}\sigma_b^{(j)}]\) pour chaque paire voisine ordonnée du cycle actif \(\Gamma_n\) (§11).

Ce module ne construit aucun facteur polaire directionnel, aucun objet de boucle.

---

## 9. Responsabilité de `model1b/directional.py`

Responsabilité scientifique strictement bornée à la spécification §12–§14, §18, §20 :

- facteur polaire directionnel fail-closed \(\mathrm{DIRECTIONAL\_FACTOR}(J) = O\) pour \(J \in GL(3,\mathbb R)\), `UNDEFINED` (raison `SINGULAR_DIRECTIONAL_FACTOR`) si \(J\) singulier, sans pseudo-inverse ni réparation (§12) ;
- vérification de typage \(\mathbb Z_2\) de route pour chaque facteur directionnel d'arête active, \(\det(O_{i\leftarrow j})=-1\) attendu ; `TYPE_MISMATCH_FAIL_CLOSED` (raison `Z2_DIRECTIONAL_TYPE_MISMATCH`) si \(\det(O)=+1\), sans réparation ni inversion de signe insérée à la main — cette raison n'est jamais confondue avec un facteur singulier (§12) ;
- objet de boucle du cycle actif \(Q_n\), conséquence de domaine \(Q_n\in SO(3)\) pour tout cycle actif à nombre pair d'arêtes dont tous les facteurs sont typés/définis ; résultat générique `LOOP_DIAGNOSTIC=UNDEFINED_DIRECTIONAL_DOMAIN` sinon, avec `LOOP_UNDEFINED_REASON` préservant explicitement `SINGULAR_DIRECTIONAL_FACTOR` ou `Z2_DIRECTIONAL_TYPE_MISMATCH` (§13) ;
- diagnostic de platitude \(d_{\mathrm{flat}}(Q_n)\) et scalaire de classe de conjugaison \(\chi_n\) (§14) ;
- comparaison inter-échelles \(\Delta\chi(n,m)\) (§14) ;
- diagnostic relatif d'arbre \(D_{\mathrm{tree}} = O_{\mathrm{path}}^{\mathsf T}\,O_{\mathrm{coarse}}\) (§18).

Ce module n'importe ni `model0a`–`model0e`, ni `model1a`.

---

## 10. Diagnostics et contrôles — statut de conception

```text
CANONICAL_DATUM        = FULL_K_n
LOOP_DIAGNOSTIC         = GAUGE_COVARIANT (Q_n) ; verdicts invariants (d_flat, chi_n) ;
                          UNDEFINED_DIRECTIONAL_DOMAIN si un facteur d'arête active
                          requis est indisponible, avec LOOP_UNDEFINED_REASON distinct
                          (SINGULAR_DIRECTIONAL_FACTOR | Z2_DIRECTIONAL_TYPE_MISMATCH,
                          spécification §12-§13) ; les deux raisons ne sont jamais
                          confondues
TREE_ORACLE             = D_tree = O_path^T O_coarse, verdict D_tree = I
PURE_GAUGE_ORACLE        = MANDATORY_NEGATIVE_ORACLE (spécification §16)
FAIL_CLOSED_DOMAIN       = DIRECTIONAL_FACTOR UNDEFINED (SINGULAR_DIRECTIONAL_FACTOR) on
                          singular J (spécification §12, §19) ; DIRECTIONAL_RELATIONAL_TYPE
                          TYPE_MISMATCH_FAIL_CLOSED (Z2_DIRECTIONAL_TYPE_MISMATCH) on
                          det(O)=+1 for an invertible active relational edge (spécification §12)
```

Aucun seuil scientifique n'est fixé par ce document ; les tolérances numériques d'un futur protocole restent `OPEN` (spécification §24).

---

## 11. Architecture de test — proposition, sans exécution ni valeur canonique

**Tests `core` (nouvelles primitives, model-free) :**

- `embed_operator` : incorporation correcte sur facteurs déclarés arbitraires, ordonnancement déterministe, gardes de dimension ;
- `hermitian_exp` : oracle spectral indépendant, covariance sous conjugaison unitaire, domaine (matrice hermitienne finie), préservation de l'hermiticité.

**Tests unitaires `model1b` :**

- normalisation/fidélité de l'état de Gibbs ;
- gardes d'ordre/hiérarchie ;
- composition exacte de trace partielle (§15 de la spécification, `T5F3`/`T5F11` par construction) ;
- donnée modulaire depuis un \(\rho\) réel ;
- reconstruction de la décomposition de support ;
- bookkeeping des poids de support ;
- covariance de \(J\) ;
- comportement de domaine exact de la décomposition polaire ;
- \(J\) singulier fail-closed, raison `SINGULAR_DIRECTIONAL_FACTOR` ;
- typage \(\mathbb Z_2\) fail-closed (\(\det(O)=-1\) attendu sur arête active ; \(\det(O)=+1\) rejeté `TYPE_MISMATCH_FAIL_CLOSED`, raison `Z2_DIRECTIONAL_TYPE_MISMATCH`, sans réparation ni inversion de signe cachée) ;
- non-confusion des deux raisons de domaine directionnel : un facteur singulier n'est jamais étiqueté `Z2_DIRECTIONAL_TYPE_MISMATCH`, et réciproquement ;
- résultat générique `LOOP_DIAGNOSTIC=UNDEFINED_DIRECTIONAL_DOMAIN` avec `LOOP_UNDEFINED_REASON` correct pour chacun des deux cas ;
- covariance de \(Q_n\) ;
- invariance par conjugaison de \(d_{\mathrm{flat}}\)/\(\chi_n\) ;
- direction non définie à relation nulle, raison `SINGULAR_DIRECTIONAL_FACTOR` (jamais `Z2_DIRECTIONAL_TYPE_MISMATCH`).

**Contrôles de qualification, plus tard notebook/plan de validation :**

- platitude multi-échelle de jauge pure (spécification §16) ;
- variation inter-échelles non centrale finie (spécification §17) ;
- oracle négatif d'arbre (spécification §18) ;
- génération complète du support modulaire ;
- non-fermeture de la troncature par paire ;
- covariance de repère local (spécification §20) ;
- flux multi-étapes.

Aucune fixture confirmatoire dans les tests unitaires ordinaires, sauf déclarée séparément non confirmatoire.

---

## 12. Gel documentaire

```text
TOY_IMPLEMENTATION_DOCUMENT_FREEZE = ENABLED
```

Au premier lot de code de `model1b` :

```text
TOY1B_SPECIFICATION         = READ_ONLY_DURING_IMPLEMENTATION
TOY1B_IMPLEMENTATION_DESIGN = READ_ONLY_DURING_IMPLEMENTATION
```

Réouverture uniquement :

```text
FUNDAMENTAL_BLOCKING_ONLY
```

Après démarrage de l'implémentation :

```text
MARKDOWN_NORMATIVE = CONTRACT
PYTHON_CODE        = MECHANISM
NOTEBOOK           = EXECUTABLE_EXPERIMENTAL_NARRATIVE
```

Aucun résultat d'implémentation ordinaire ne peut réécrire le design gelé.

---

## 13. Paramètres non fermés par ce document

```text
MODEL1B_QUALIFICATION_FIXTURES         = OPEN
NUMERICAL_TOLERANCES                   = OPEN
CONDITIONING_ADMISSIBILITY_THRESHOLD   = OPEN
TREE_TOPOLOGY_AND_PARAMETERS           = OPEN
PASS_FAIL_TOLERANCES                   = OPEN
MODEL1B_ACCEPTANCE_CRITERION           = OPEN
T5_FLOW_CONFIRMATORY_PROTOCOL          = NOT_DEFINED
T5_FLOW_QUALIFICATION                  = NOT_EXECUTED
```

---

## 14. Statut et prochaine étape

```text
MODEL1B_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_MODEL1B_T5_FLOW_DESIGN
MODEL1B_DESIGN_CORRECTION             = Z2_DIRECTIONAL_TYPE_DOMAIN_AND_STABILITY_CLARIFICATIONS
MODEL1B_CONSISTENCY_FIX               = SINGULAR_VS_Z2_TYPE_MISMATCH_DISTINCTION
MODEL1B_IMPLEMENTATION                = NOT_AUTHORIZED
MODEL1B_CONFIRMATORY_QUALIFICATION    = NOT_AUTHORIZED
```

Corrections apportées par le lot `MODEL1B-T5-FLOW-DESIGN-CORRECTION-1` : sémantique d'ordre explicite de `positions` pour `embed_operator` (ordre des facteurs tensoriels de l'opérande, permutation explicite obligatoire vers l'ordre global canonique, en particulier pour `DA`, §3.1, §6) ; `hermitian_exp` réaffirmé comme candidat `core` générique, décalage spectral de stabilité `H_shifted = H_rel - lambda_max I` explicitement propre à la construction de Gibbs `model1b` (§3.2, §6) ; contrôle de typage \(\mathbb Z_2\) fail-closed du facteur directionnel d'arête active (§9–§10, tests §11).

Correction de cohérence apportée par le lot `MODEL1B-T5-FLOW-DESIGN-CONSISTENCY-1` : distinction explicite, jamais confondue, entre les deux échecs de domaine directionnel — `DIRECTIONAL_FACTOR=UNDEFINED`/`SINGULAR_DIRECTIONAL_FACTOR` (facteur singulier) et `DIRECTIONAL_RELATIONAL_TYPE=TYPE_MISMATCH_FAIL_CLOSED`/`Z2_DIRECTIONAL_TYPE_MISMATCH` (facteur inversible de mauvais type) — dans `directional.py` (§9), le bloc de diagnostics (§10) et l'architecture de test (§11) ; résultat générique unifié `LOOP_DIAGNOSTIC=UNDEFINED_DIRECTIONAL_DOMAIN` avec `LOOP_UNDEFINED_REASON` explicite. Aucun changement de code, aucune promotion `core` exécutée, aucune fixture ni tolérance numérique introduite.

La prochaine étape autorisée est la confirmation finale à distance de ce design par ChatGPT.
