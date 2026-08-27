# toy0e — Conception d'implémentation (model0e)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model0e`, sur la base de `docs/toy-models/toy0e/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun critère ou verdict T1.

---

## 1. Périmètre

Ce document couvre :

- l'audit architectural obligatoire des primitives `core` réutilisées et de l'absence de nouvelle promotion `core` (§3 ci-dessous) ;
- le design minimal de la famille d'états et des réductions (spécification §7–§9) ;
- le design minimal des contextes modulaires et de l'extraction de référence \(\mathbb Z_3\) (spécification §10–§15) ;
- le design minimal des états conditionnels physiques, de la carte de corrélation et de la loi fixe dérivée (spécification §19, §21–§22) ;
- le design minimal des contrôles C1–C7 (spécification §19–§32) et des contrôles de faux positifs F0–F6 (spécification §33).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les fixtures numériques de qualification (`MODEL0E_QUALIFICATION_FIXTURES`, spécification §34) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire d'acceptation ;
- le plan de validation ;
- un critère d'acceptation de `model0e` ou de T1.

---

## 2. Vérification du contrat réel des primitives `core` existantes

`model0e` réutilise le mécanisme déjà établi dans `cosmotgg.core` :

- `cosmotgg.core.states.validate_density_matrix` — validation fail-closed d'une matrice densité, tolérances explicites sans valeur par défaut ;
- `cosmotgg.core.states.partial_trace` — trace partielle exacte sur un produit tensoriel explicite de dimensions locales, utilisée pour toutes les réductions \(\rho_{AB}, \rho_A, \rho_B, \rho_{AC}, \rho_{AD}, \rho_{BC}, \rho_{BD}\) (spécification §9) ;
- `cosmotgg.core.states.conditional_expectation` — espérance conditionnelle traciale, utilisée pour \(E_X^C\), \(E_X^D\) (spécification §10) ;
- `cosmotgg.core.states.traceless_part` — partie sans trace, utilisée pour \(H_Q^X\), \(H_N^X\) (spécification §10) ;
- `cosmotgg.core.modular.modular_hamiltonian` — \(K = -\ln(\rho)\) pour un état fidèle, utilisée pour \(K_{XC}\), \(K_{XD}\) (spécification §10).

Ces primitives sont déjà `established` (`SCIENTIFIC_METADATA.status = "established"`) et ne sont pas modifiées par ce document.

---

## 3. Audit architectural obligatoire — aucune nouvelle promotion `core`

Conformément à `docs/governance/software-architecture-governance.md` §3 et §16, l'audit couvre les opérations candidates suivantes, spécifiques à `model0e` :

```text
composant                          | placement | justification                                              | dépendances        | validation
extraction spectrale ordonnée      | model0e   | dépend d'un ordre déclaré propre à la construction candidate | numpy.linalg.eigh   | tests/models/model0e
(H_N -> P_0,P_1,P_2, R_X, U_X)     |           | (§14 spécification), pas une primitive mathématique générique|                     |
(pas de généralisation d'ordre)    |           | indépendante de tout contexte                                |                     |

projecteur propre maximal (H_Q)    | model0e   | sélection « unique valeur propre maximale » est une règle     | numpy.linalg.eigh   | tests/models/model0e
                                    |           | de construction candidate model0e, pas une primitive core     |                     |

portail de module égal (§15)       | model0e   | seuil/test candidat model0e, pas une brique core               | —                   | tests/models/model0e

carte de corrélation anti-linéaire | model0e   | dépend de l'identification vecteur propre maximal <-> matrice  | numpy               | tests/models/model0e
J_AB, M_AB (§21)                   |           | reshape, spécifique à la construction candidate model0e        |                     |

loi fixe dérivée V_A, Lambda (§22) | model0e   | dérivation depuis rho_AB et U_B, spécifique au candidat         | numpy               | tests/models/model0e

règle de changement de référence   | model0e   | dépend de la carte de corrélation model0e ci-dessus              | numpy               | tests/models/model0e
(§29)                              |           |                                                                  |                     |
```

Décision explicite, conformément au mandat :

```text
CORE_PROMOTION_NEEDED           = NO
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
CODE_MODIFIED_THIS_LOT          = FALSE
```

Ces opérations restent dans `model0e` initialement, même lorsqu'elles ont l'apparence mathématique d'une brique générique (extraction de projecteurs spectraux ordonnés, exponentielle cyclique d'un opérateur de rang, carte de corrélation anti-linéaire). Elles ne sont pas promues vers `core` au seul motif d'une généralité apparente, conformément au mandat explicite du présent lot. Une promotion future resterait possible sur la base d'un second modèle concret réutilisant identiquement l'une de ces briques (`docs/governance/software-architecture-governance.md` §7).

`cosmotgg.core.states._hermitian_eigendecomposition` est un auxiliaire privé de `core` et n'est pas importé par `model0e` ; l'extraction spectrale de `model0e` s'appuie directement sur `numpy.linalg.eigh`, appliqué à des opérateurs hermitiens déjà validés en amont par les primitives `core` réutilisées (§2 ci-dessus).

---

## 4. Arborescence cible minimale

```text
src/cosmotgg/models/model0e/__init__.py
src/cosmotgg/models/model0e/states.py
src/cosmotgg/models/model0e/reference.py
src/cosmotgg/models/model0e/conditional.py

tests/models/model0e/__init__.py
tests/models/model0e/test_states.py
tests/models/model0e/test_reference.py
tests/models/model0e/test_conditional.py
```

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model0E
class Clock
class Time
graph/groupoid abstraction
```

`model0e` n'importe pas `model0a`, `model0b`, `model0c`, `model0d` en production :

```text
MODEL0E_PRODUCTION_IMPORTS_PRIOR_MODELS = NO
```

Les modèles précédents peuvent être mentionnés uniquement dans les tests/le notebook comme continuité scientifique.

Le partage exact des responsabilités entre `states.py`, `reference.py` et `conditional.py` ci-dessous constitue une proposition ; les noms techniques exacts peuvent être ajustés par le rôle `code` sans changer leur définition normative, conformément aux conventions du dépôt.

---

## 5. Responsabilité de `model0e/states.py`

Responsabilité scientifique strictement bornée aux spécification §6–§9 :

- constantes du représentant canonique qutrit : \(|\Phi_3\rangle\), \(P_\Phi\), \(S_{AB}\), \(N\), \(|q_0\rangle\), \(Q\) (spécification §6), portées comme valeurs de module ou fonctions auxiliaires privées, sans revendication de base préférée au niveau de l'API publique (spécification §6, « Important ») ;
- constructeur de la famille d'états `four_partite_discrete_multimodular_reference_state(eta, gamma, mu_A, mu_B, delta, nu_A, nu_B, *, ...)` (spécification §7), assemblé par combinaison linéaire explicite de produits tensoriels, sans raccourci analytique masquant le développement du §7 ;
- validation fail-closed du domaine fidèle suffisant et des conditions de branche (spécification §8), sans tolérance ni epsilon, frontière rejetée ;
- réductions \(\rho_{AB}, \rho_A, \rho_B, \rho_{AC}, \rho_{AD}, \rho_{BC}, \rho_{BD}\) (spécification §9), obtenues via `cosmotgg.core.states.partial_trace` sur les dimensions déclarées `(3,3,2,2)`.

Ce module ne construit aucun contexte modulaire, aucune extraction de référence, aucun état conditionnel.

---

## 6. Responsabilité de `model0e/reference.py`

Responsabilité scientifique strictement bornée aux spécification §10–§18 :

- contextes modulaires projetés \(H_Q^X\), \(H_N^X\) pour \(X \in \{A,B\}\), via `modular_hamiltonian` + `conditional_expectation` + `traceless_part` (spécification §10) ;
- extraction ordonnée des projecteurs spectraux de \(H_N^X\), construction de l'opérateur de rang \(R_X\) et de l'unitaire cyclique \(U_X = \exp(-2\pi i R_X/3)\) (spécification §14), sans utiliser les écarts numériques de \(H_N^X\) ;
- sélection du projecteur propre maximal unique \(E_0^X\) de \(H_Q^X\), formulée en priorité au niveau des projecteurs (spécification §14) ;
- construction de la famille PVM \(\{E_k^X\}_{k=0,1,2}\) par conjugaison cyclique (spécification §14) ;
- portail de module égal (spécification §15), exposé comme diagnostic de qualification explicite, sans réparation ni remplacement silencieux de semence en cas d'échec ;
- application de la jauge de relabellisation affine \(\mathbb Z_3\) (spécification §17) comme fonction explicite, pas comme convention implicite.

Ce module ne construit aucun état conditionnel physique, aucune carte de corrélation, aucune loi fixe.

---

## 7. Responsabilité de `model0e/conditional.py`

Responsabilité scientifique strictement bornée aux spécification §19–§32 :

- états conditionnels physiques \(p_B(k)\), \(\rho_{A|k}\) à partir de \(\rho_{AB}\) et de la PVM de référence \(\{E_k^B\}\) (spécification §19) ;
- statistiques \(p_A(j \mid k)\) pour C3 (spécification §20) ;
- carte de corrélation anti-linéaire \(M_{AB}\), \(J_{AB}\) depuis le vecteur propre maximal de \(\rho_{AB}\) (spécification §21) ;
- loi fixe dérivée \(V_A\), \(\Lambda_{(k_2 \leftarrow k_1)}\) (spécification §22), sans transposition/conjugaison codée en dur, en dérivant \(V_A\) depuis \(\rho_{AB}\) et \(U_B\) ;
- comparaison directe/loi pour C4C (spécification §25) ;
- règle de changement de référence et carte d'étiquette \(\pi\) pour C7 (spécification §29).

Les diagnostics de sensibilité (asymétrie d'amplitude A/B, spécification §31 ; projection pondérée, spécification §32) sont des variantes de calcul des fonctions ci-dessus (contexte pondéré au lieu de tracial), pas une API de production distincte.

Ce module n'importe pas `model0c` ni les autres modèles précédents.

---

## 8. Diagnostics et contrôles — statut de conception

Contrôles définis par la spécification, à exposer comme fonctions ou valeurs auxiliaires, sans seuil normatif :

```text
REFERENCE_EXTRACTION status (PASS/FAIL selon portail de module égal, spécification §15)

C1  — physical carriers                : rho_A|k, rho_AB, rho_A, rho_B (états physiques déjà exposés par states.py/conditional.py)
C2  — internal relational reference    : PVM {E_k^B}, {E_j^A} dérivées de reference.py
C3  — observable nontriviality         : p_A(j|k), spécification §20
C4A — reference covariance             : U_X, V_A comme loi unique, spécification §24
C4B — fixed law overdetermination      : NUMBER_OF_INDEPENDENT_TARGET_STATE_INPUTS = ZERO, spécification §22
C4C — two-reading consistency          : p_direct vs p_law, spécification §25
C5  — physical admissibility           : normalisation/canal unitaire, spécification §26
C6  — reparametrization firewall       : absence de s/t/tau exposé, spécification §27
C7  — reference nonprivilege           : matrice de recouvrement/pi, spécification §29–§30
```

Faux positifs (spécification §33), chacun réalisé par une fixture ou une perturbation test-only, sans nouvelle API de production :

```text
F0 — eta = 0                                    -> tests/models/model0e/test_conditional.py
F1 — mu_X = 0                                   -> tests/models/model0e/test_reference.py
F2 — nu_X = 0                                   -> tests/models/model0e/test_reference.py
F3 — semence de module inégal (test-only)       -> tests/models/model0e/test_reference.py
F4 — trois états conditionnels arbitraires       -> tests/models/model0e/test_conditional.py
    (test-only, hors orbite Z3 dérivée)
F5 — perturbation rho_AB trace-nulle (test-only) -> tests/models/model0e/test_conditional.py
F6 — relabellisation affine Z3                   -> tests/models/model0e/test_reference.py
```

Ce sont des `NUMERICAL_QUALIFICATION_GUARDS`/contrôles structurels, pas des observables physiques normatives. Aucun seuil scientifique n'est fixé par ce document ; les tolérances numériques d'un futur protocole restent `OPEN` (spécification §38).

---

## 9. Tests prévus — `model0e` (proposition, sans valeur canonique)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

**`test_states.py`** :

- construction de la famille d'états sur une fixture `NON_NORMATIVE_TEST_FIXTURE` symétrique et sur la fixture amplitude-asymétrique ;
- rejet fail-closed hors du domaine fidèle suffisant (spécification §8) et des conditions de branche ;
- réductions exactes \(\rho_{AB}, \rho_A, \rho_B, \rho_{AC}, \rho_{AD}, \rho_{BC}, \rho_{BD}\) contre les formules analytiques du §9 (oracle indépendant) ;
- contrôle négatif **F0** (\(\eta=0\)) au niveau de l'état, préparatoire au contrôle C3 de `test_conditional.py`.

**`test_reference.py`** :

- \(\Delta_Q^X > 0\) et \(H_Q^X = \Delta_Q^X Q_X\) contre l'oracle analytique du §11 ;
- ordre \(h_N^X(-1) < h_N^X(0) < h_N^X(+1)\) et non-dégénérescence contre l'oracle analytique du §12 ;
- propriétés exactes de la PVM \(\{E_k^X\}\) : orthogonalité, résolution de l'identité, covariance cyclique \(E_{k+1}=U_X E_k U_X^\dagger\), \(U_X^3=I\) (spécification §14) ;
- portail de module égal \(|\langle n|q_0\rangle|^2 = 1/3\) (spécification §15) ;
- covariance de base locale \(V_A \otimes V_B \otimes V_C \otimes V_D\) à jauge d'étiquette près (spécification §18) ;
- **F1** (\(\mu_X=0\)) : `REFERENCE_EXTRACTION = FAIL` attendu ;
- **F2** (\(\nu_X=0\)) : `REFERENCE_EXTRACTION = FAIL` attendu ;
- **F3** (semence de module inégal, test-only) : `Z3_PVM_GATE = FAIL` attendu ;
- **F6** (relabellisation affine \(\mathbb Z_3\)) : invariance des probabilités physiques après transformation d'étiquette correspondante ;
- contrôle d'asymétrie d'amplitude A/B (spécification §31) : amplitudes différentes, PVM compatibles par corrélation ;
- sensibilité de projection pondérée (spécification §32) : projecteurs/ordre inchangés, amplitude non robuste.

**`test_conditional.py`** :

- \(p_B(k) = 1/3\) et \(\rho_{A|k}\) contre l'oracle analytique du §19 (valeurs propres, fidélité, distinction pour \(k\) différents sous \(\eta>0\)) ;
- C3 : au moins un \(j\) avec \(p_A(j|k_1) \neq p_A(j|k_2)\) pour \(\eta \neq 0\) ; **F0** (\(\eta=0\)) : `C3 = FAIL` attendu ;
- \(M_{AB}\) unitaire à tolérance près pour la famille déclarée (spécification §21) ;
- \(V_A^3 = I\) à phase globale près, et \(\rho_{A|(k+1)} = V_A \rho_{A|k} V_A^\dagger\) (spécification §22) ;
- C4B : `NUMBER_OF_INDEPENDENT_TARGET_STATE_INPUTS = 0` (contrôle structurel de signature, pas de paramètre cible dans `Lambda`) ;
- C4C : \(p_{\text{law}} = p_{\text{direct}}\) pour une sonde physique déclarée indépendamment de la cible (spécification §25) ;
- C7 : matrice de recouvrement `Tr[E_j^A J_AB(E_k^B)]` égale à une permutation à valeurs `{0,1}`, extraction de \(\pi\) comme relabellisation affine \(\mathbb Z_3\) (spécification §29–§30) ;
- **F4** (trois états conditionnels arbitraires, test-only) : `FIXED_LAW_OVERDETERMINATION = FAIL` attendu ;
- **F5** (perturbation \(\rho_{AB}\) trace-nulle, test-only) : `FIXED_LAW = FAIL` ou `REFERENCE_CHANGE_COMPATIBILITY = FAIL` attendu, tout en pouvant laisser les états conditionnels directs distincts ;
- absence d'import de `model0a`, `model0b`, `model0c`, `model0d` dans `src/cosmotgg/models/model0e/` (contrôle structurel, cohérent avec `MODEL0E_PRODUCTION_IMPORTS_PRIOR_MODELS = NO`, §4 ci-dessus).

Les valeurs de test restent explicitement marquées `NON_NORMATIVE_TEST_FIXTURE` et ne constituent pas des `MODEL0E_QUALIFICATION_FIXTURES` normatifs (spécification §34, qui restent `OPEN`).

---

## 10. Intégration croisée avec les modèles précédents

Dépendance de production :

```text
model0e -X-> model0a, model0b, model0c, model0d
```

Aucune importée en production, conformément au §4 ci-dessus. Un futur notebook pourra mentionner la continuité scientifique avec `model0a`–`model0d` (spécification §4) sans introduire de dépendance de production.

---

## 11. Absence de scalaire normatif

Ce document ne définit aucun `threshold`, `normalized score`, `ratio`, ni indicateur scalaire de temps. De telles quantités pourront être introduites ultérieurement par un futur plan de validation ; elles ne font pas partie de la définition scientifique actuelle.

---

## 12. Paramètres non fermés par ce document

```text
MODEL0E_QUALIFICATION_FIXTURES     = OPEN / NON_NORMATIVE_AT_IMPLEMENTATION
NUMERICAL_TOLERANCES               = OPEN
REFERENCE_SPECTRAL_TOLERANCE       = OPEN
REFERENCE_EQUAL_MODULUS_TOLERANCE  = OPEN
MODEL0E_ACCEPTANCE_CRITERION       = OPEN
T1_NONTRIVIALITY_CRITERION         = OPEN
CONFIRMATORY_PROTOCOL              = NOT_DEFINED
```

---

## 13. Gel documentaire

Ce document et `docs/toy-models/toy0e/specification.md` constituent l'unique lot `docs` pré-implémentation de `toy0e`. Au premier lot de code de `model0e` :

```text
TOY0E_SPECIFICATION             = READ_ONLY_DURING_IMPLEMENTATION
TOY0E_IMPLEMENTATION_DESIGN     = READ_ONLY_DURING_IMPLEMENTATION
```

Le récit scientifique de l'exécution appartiendra ensuite à `experiments/toy0e/toy0e.ipynb` (`docs/governance/documentation-governance.md` §11.3). Aucun lot `docs` supplémentaire n'est attendu après le démarrage de l'implémentation, sauf `FUNDAMENTAL_BLOCKING_ONLY` (`docs/governance/documentation-governance.md` §11.2).

---

## 14. Statut et prochaine étape

```text
MODEL0E_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
