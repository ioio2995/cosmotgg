# toy0b — Conception d'implémentation (model0b)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model0b`, sur la base de `docs/toy-models/toy0b/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun critère ou verdict T1.

---

## 1. Périmètre

Ce document couvre :

- la construction de la famille d'états de `model0b` (`docs/toy-models/toy0b/specification.md` §5) ;
- le design minimal du générateur relatif \(\Delta_{(A:C|B)}\) et de sa dérivation (spécification §8–§14) ;
- le design minimal des tests structurels R0–R3 et de covariance locale (spécification §16, §21).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les valeurs numériques de \(\beta,\lambda,\mu\) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire ;
- le plan de validation ;
- un critère d'acceptation de `model0b` ou de T1 ;
- tout flot fini paramétré par \(\tau\) (spécification §19, `FINITE_FLOW_PARAMETER_PROBLEM = OPEN`).

---

## 2. Vérification du contrat réel de `cosmotgg.core.states.partial_trace`

Avant de décider de la réutilisation de `core` pour la conditional expectation normalisée sur le chevauchement (spécification §9), le contrat réel de `cosmotgg.core.states.partial_trace` a été vérifié (`src/cosmotgg/core/states.py`).

Constat :

- la signature est `partial_trace(operator, *, dimensions, keep)` : le paramètre s'appelle `operator`, pas `rho` ni `density_matrix` ;
- la docstring énonce explicitement : *« This primitive makes no assumption about the number of subsystems, their dimensions, or any bipartite/qubit structure »* ;
- l'implémentation ne valide ni hermiticité, ni trace, ni positivité de `operator` ; elle ne fait qu'un contrôle de forme (carré, 2D) et de cohérence dimensionnelle avec `dimensions` ;
- aucun appel à `validate_density_matrix` n'est effectué à l'intérieur de `partial_trace`.

Décision :

```text
CORE_REUSE_DECISION = REUSE_CORE
```

`cosmotgg.core.states.partial_trace` est un opérateur linéaire générique sur un produit tensoriel fini explicite ; sa sémantique n'est pas restreinte aux matrices densité. Il peut donc être appliqué tel quel à un hamiltonien modulaire \(K_{AB}\) ou \(K_{BC}\) (hermitien, mais pas nécessairement de trace 1 ni positif), sans détourner son contrat.

Conséquence pour la conditional expectation normalisée (spécification §9) :

$$
E_B^A(X_{AB}) = \frac{1}{d_A}\,\texttt{partial\_trace}(X_{AB},\ \text{dimensions}=(d_A,d_B),\ \text{keep}=[1]),
$$

$$
E_B^C(X_{BC}) = \frac{1}{d_C}\,\texttt{partial\_trace}(X_{BC},\ \text{dimensions}=(d_B,d_C),\ \text{keep}=[0]).
$$

La division scalaire par \(d_A\)/\(d_C\) est une opération triviale assemblée dans `model0b`, pas une nouvelle primitive `core`.

La réduction sans trace \(\operatorname{tl}_B\) (spécification §11) opère sur un opérateur déjà réduit à \(\mathcal H_B\) seul (pas de structure tensorielle multi-facteurs à cet endroit) : elle utilise la trace ordinaire (`numpy.trace`) et `numpy.eye(d_B)`, pas `partial_trace`. Aucune primitive `core` générique de « réduction sans trace » n'existe actuellement ; conformément au principe de placement conservateur (`docs/governance/software-architecture-governance.md` §3.1), cette construction reste model-specific et n'est pas promue dans `core` par ce lot.

Aucun nouveau core spéculatif n'est créé par ce lot.

---

## 3. Primitives `core` réutilisées

Sont réutilisées telles quelles :

```text
cosmotgg.core.states.validate_density_matrix
cosmotgg.core.states.partial_trace

cosmotgg.core.modular.modular_hamiltonian
```

Aucune de ces primitives n'est dupliquée dans `model0b`.

`cosmotgg.core.modular.modular_hamiltonian` calcule \(K=-\ln(\rho)\) pour un état fidèle ; elle est appliquée à \(\rho_{AB}\) et \(\rho_{BC}\) (états réduits, obtenus via `partial_trace` sur \(\rho_{ABC}\)) pour obtenir \(K_{AB}\), \(K_{BC}\) (spécification §8). Ces réductions sont fidèles par construction dans le domaine fermé du §6 de la spécification (voir §7 de la spécification) ; aucune tolérance de fidélité n'est inventée localement.

`cosmotgg.core.information.log_density_difference` et `cosmotgg.core.modular.finite_connes_cocycle` ne sont pas utilisées par `model0b` : la spécification (§8) formule le candidat directement à partir de \(K_{AB}\), \(K_{BC}\), pas à partir du cocycle ou de \(\mathcal R_{AB}\).

Aucun commutateur générique n'existe dans `core` ; le commutateur \([\Delta_B, O_B]\) de la dérivation (spécification §13) est assemblé model-specific (`Delta_B @ O_B - O_B @ Delta_B`), à l'image de la construction déjà retenue par `model0a/diagnostics.py` pour \(C_{AB} = [\ln(\rho),\ln(\sigma)]\).

---

## 4. Arborescence cible minimale

```text
src/cosmotgg/models/model0b/__init__.py
src/cosmotgg/models/model0b/states.py
src/cosmotgg/models/model0b/relative.py

tests/models/model0b/test_states.py
tests/models/model0b/test_relative.py
```

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model0B
```

---

## 5. Responsabilité de `model0b/states.py`

Responsabilité scientifique strictement bornée à la famille d'états de `docs/toy-models/toy0b/specification.md` §5 :

- construire \(\rho_{ABC}(\beta,\lambda,\mu)\) selon la matrice normative du §5 ;
- déclarer et valider son domaine analytique (§6), de façon fail-closed et sans tolérance numérique implicite ;
- fournir, si utile, les états réduits \(\rho_{AB}\), \(\rho_{BC}\), \(\rho_B\) (§7 de la spécification), par assemblage explicite des chaînes de Pauli ou via `cosmotgg.core.states.partial_trace`.

Ce module ne réimplémente pas : logarithme matriciel, hamiltonien modulaire, partial trace générique, conditional expectation. Ces briques restent dans `cosmotgg.core` ou dans `model0b/relative.py` (§6 ci-dessous).

### 5.1 Validation du domaine analytique

La construction échoue (fail-closed) sur des paramètres \(\beta,\lambda,\mu\) hors du domaine analytique normatif du §6 de la spécification (\(\beta^2+\lambda^2+\mu^2 < 1\)). Cette définition de domaine n'est ni approximée ni assouplie par une tolérance numérique locale au module.

---

## 6. Responsabilité de `model0b/relative.py`

Responsabilité scientifique strictement bornée aux §8–§14 de la spécification :

- construire \(K_{AB} = -\ln(\rho_{AB})\), \(K_{BC} = -\ln(\rho_{BC})\) via `cosmotgg.core.modular.modular_hamiltonian` ;
- construire \(E_B^A(K_{AB})\), \(E_B^C(K_{BC})\) via `cosmotgg.core.states.partial_trace` et division scalaire par \(d_A\)/\(d_C\) (§2 ci-dessus) ;
- appliquer \(\operatorname{tl}_B\) (§11 de la spécification) ;
- assembler \(\Delta_{(A:C|B)} = -\chi_{(A\to B)} + \chi_{(C\to B)}\) (§12 de la spécification, convention de signe fixée une fois) ;
- appliquer la dérivation \(D(O_B) = -i[\Delta_B, O_B]\) (§13 de la spécification).

Ce module ne construit aucun flot fini paramétré par \(\tau\) : `FINITE_FLOW_PARAMETER_PROBLEM = OPEN` (§19 de la spécification) n'est pas fermé par ce lot, et aucune fonction du type `exp(-i tau Delta) O exp(+i tau Delta)` n'est prévue.

---

## 7. API proposée — famille d'états

```text
three_qubit_overlapping_pauli_relation_state(beta, lambda_, mu)
```

Ce nom technique reprend l'identifiant `STATE_FAMILY = THREE_QUBIT_OVERLAPPING_PAULI_RELATION_FAMILY` de la spécification à des fins de traçabilité ; il ne porte aucune sémantique scientifique supplémentaire par rapport à celle-ci. Le paramètre est nommé `lambda_` (`lambda` étant un mot réservé Python) ; ce choix technique n'affecte pas la définition normative \(\lambda\) de la spécification.

Le rôle `code` reste libre d'ajuster ce nom lors de l'implémentation, dans la mesure où il reste descriptif et ne modifie pas le sens de la construction.

---

## 8. API proposée — générateur et dérivation relatifs

```text
overlap_relative_modular_generator(
    rho_abc,
    *,
    hermiticity_tolerance,
    trace_tolerance,
    positivity_tolerance,
)
```

Retourne la **matrice** \(\Delta_{(A:C|B)}\) agissant sur \(\mathcal H_B\), jamais le scalaire \(\delta\) (§14 de la spécification).

```text
overlap_relative_modular_derivation(
    delta_b,
    observable_b,
)
```

Applique uniquement \(-i[\Delta_B, O_B]\) (§13 de la spécification). Aucun flot fini n'est exposé par cette fonction ni par une autre fonction de ce module.

Les tolérances numériques (`hermiticity_tolerance`, `trace_tolerance`, `positivity_tolerance`) sont explicites, keyword-only, sans valeur par défaut, transmises telles quelles à `cosmotgg.core.states.validate_density_matrix` et `cosmotgg.core.modular.modular_hamiltonian`, à l'image des conventions déjà en place dans `cosmotgg.core` et `model0a/diagnostics.py`. Aucune tolérance n'est inventée localement par `model0b`.

Ces noms techniques peuvent être ajustés par le rôle `code` sans changer leur définition normative.

---

## 9. Tests prévus — famille d'états (`tests/models/model0b/test_states.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

- matrice d'état exacte pour des paramètres de développement `NON_NORMATIVE_TEST_FIXTURE` ;
- trace analytique égale à 1 ;
- fidélité dans le domaine (§6 de la spécification) ;
- rejet fail-closed des paramètres hors domaine ;
- états réduits exacts \(\rho_{AB}\), \(\rho_{BC}\), \(\rho_B\), \(\rho_A\), \(\rho_C\) (§7 de la spécification).

---

## 10. Tests prévus — générateur relatif (`tests/models/model0b/test_relative.py`)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

- identité analytique de \(\Delta_{(A:C|B)}\) (§14 de la spécification, \(\Delta = \beta[f(r_{AB})-f(r_{BC})]Z_B\)) ;
- \(D(X_B)=2\delta Y_B\), \(D(Y_B)=-2\delta X_B\), \(D(Z_B)=0\) (§14 de la spécification) ;
- condition exacte de non-nullité \(\Delta\neq0 \iff \beta\neq0 \text{ et } \lambda^2\neq\mu^2\) (§15 de la spécification) ;
- R0 (`lambda=0, mu=0` ⟹ `Delta=0`) ;
- R1 (`|lambda|=|mu|≠0` ⟹ `Delta=0`) ;
- R2 (`beta≠0, |lambda|≠|mu|` ⟹ `Delta≠0`) ;
- R3 (`beta=0` ⟹ `rho_B=I/2`, `Delta=0`) ;
- covariance sous \(U_A\otimes U_B\otimes U_C\) : \(\Delta \to U_B\,\Delta\,U_B^\dagger\) (§21 de la spécification), bornée à `LOCAL_PRODUCT_UNITARY_COVARIANCE` ;
- \(\Delta\) est hermitien et sans trace (\(\operatorname{Tr}(\Delta)=0\)) ;
- absence de toute API de flot fini paramétré par \(\tau\) dans `model0b/relative.py` (contrôle structurel/d'architecture, pas un test numérique).

Les valeurs de test restent, comme au §9, explicitement marquées `NON_NORMATIVE_TEST_FIXTURE` et ne constituent pas des `BETA_VALUE`/`LAMBDA_VALUE`/`MU_VALUE` normatifs (§23 de la spécification, qui restent `OPEN`).

---

## 11. Absence de scalaire normatif

Ce document ne définit aucun `threshold`, `normalized score`, `ratio`, ni indicateur scalaire de temps. De telles quantités pourront être introduites ultérieurement par un futur plan de validation ; elles ne font pas partie de la définition scientifique actuelle.

---

## 12. Paramètres non fermés par ce document

```text
BETA_VALUE                    = OPEN
LAMBDA_VALUE                  = OPEN
MU_VALUE                      = OPEN
NUMERICAL_TOLERANCES          = OPEN
MODEL0B_ACCEPTANCE_CRITERION  = OPEN
T1_NONTRIVIALITY_CRITERION    = OPEN
CONFIRMATORY_PROTOCOL         = NOT_DEFINED
FINITE_FLOW_PARAMETER_PROBLEM = OPEN
ALGEBRAIC_GENERALIZATION_OF_DELTA  = OPEN
TYPE_I_TO_ALGEBRAIC_MODULAR_BRIDGE = OPEN
```

---

## 13. Statut et prochaine étape

```text
MODEL0B_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
