# toy1a — Conception d'implémentation (model1a)

**Statut : `PROPOSED_IMPLEMENTATION_DESIGN`.**

Ce document décrit l'architecture logicielle cible minimale de `model1a`, sur la base de `docs/toy-models/toy1a/specification.md` et de `docs/governance/software-architecture-governance.md`.

Il ne contient aucun code, aucun notebook, aucun plan de validation, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucune norme ni seuil scalaire, et aucun critère ou verdict T2/T4.

---

## 1. Périmètre

Ce document couvre :

- l'audit architectural obligatoire des primitives `core` réutilisées et de l'absence de nouvelle promotion `core` (§3 ci-dessous) ;
- le design minimal de l'état global, des réductions et du statut modulaire (spécification §6–§9) ;
- le design minimal du lien directionnel, du pare-feu de phase, du contrat de lien inverse et du transfert d'arête physique centré (spécification §10–§13) ;
- le design minimal de l'holonomie de boucle projective, du contrôle de jauge pure et de la réponse primaire (spécification §15–§18) ;
- le design minimal des contrôles de continuité en lien faible, de limite sans relation, de covariance de base locale et des contrôles de faux positifs F0–F8 (spécification §19–§20, §25–§26).

Il ne couvre pas :

- l'implémentation elle-même (code) ;
- les fixtures numériques de qualification (`MODEL1A_QUALIFICATION_FIXTURES`, spécification §23) ;
- les tolérances numériques d'un futur protocole ;
- toute norme ou seuil scalaire d'acceptation ;
- le plan de validation ;
- un critère d'acceptation de `model1a`, de T2 ou de T4.

---

## 2. Vérification du contrat réel des primitives `core` existantes

`model1a` réutilise le mécanisme déjà établi dans `cosmotgg.core` :

- `cosmotgg.core.states.validate_density_matrix` — validation fail-closed d'une matrice densité, tolérances explicites sans valeur par défaut ;
- `cosmotgg.core.states.partial_trace` — trace partielle exacte sur un produit tensoriel explicite de dimensions locales, utilisée pour toutes les réductions \(\rho_{ij}\), \(\rho_A,\rho_B,\rho_C,\rho_D\), \(\rho_{AC},\rho_{BD}\) (spécification §7) ;
- `cosmotgg.core.modular.modular_hamiltonian` — \(K = -\ln(\rho)\) pour un état fidèle, utilisée pour \(K_{ij}\) (spécification §8).

Ces primitives sont déjà `established` (`SCIENTIFIC_METADATA.status = "established"`) et ne sont pas modifiées par ce document.

Aucune dépendance à `conditional_expectation`/`traceless_part` n'est requise par `model1a` : le lien directionnel et la réponse de boucle sont extraits directement des vecteurs/valeurs propres de \(\rho_{ij}\)/\(K_{ij}\) et de leur composition algébrique (spécification §9–§18), pas d'une espérance conditionnelle sur un sous-système de contexte.

`partial_trace` ne garantit pas nativement que la paire \(D,A\) soit retournée dans l'ordre \(D\otimes A\) (spécification §7) : dans l'ordre tensoriel global \(A,B,C,D\), la trace partielle sur \(B,C\) produit naturellement la paire dans l'ordre \(A\otimes D\). `model1a/states.py` doit donc permuter explicitement ce résultat (SWAP) vers \(D\otimes A\) avant d'exposer `rho_DA`. Aucune hypothèse silencieuse sur l'ordre de conservation d'indices de `partial_trace` n'est faite ailleurs dans `model1a`.

Possiblement de l'algèbre linéaire générique via `numpy` uniquement (diagonalisation hermitienne, produits matriciels, transposition/conjugaison).

---

## 3. Audit architectural obligatoire — aucune nouvelle promotion `core`

Conformément à `docs/governance/software-architecture-governance.md` §3 et §16, l'audit couvre les opérations candidates suivantes, spécifiques à `model1a` :

```text
composant                            | placement | justification                                                  | dépendances       | validation
extraction du projecteur fondamental | model1a   | sélection « unique valeur propre minimale de K_ij / maximale     | numpy.linalg.eigh  | tests/models/model1a
unique de K_ij / rho_ij (§8)         |           | de rho_ij » est une règle de construction candidate model1a,     |                    |
                                      |           | pas une primitive core générique                                 |                    |

extraction du lien directionnel      | model1a   | reformage vecteur -> matrice M_ij = sqrt(2) Psi_matrix,           | numpy              | tests/models/model1a
M_ij (§10)                           |           | spécifique à la construction maximalement intriquée model1a       |                    |

carte antilinéaire J/U_(i<-j)         | model1a   | dépend du reformage M_ij ci-dessus, spécifique à la construction  | numpy              | tests/models/model1a
et transfert centré L_(i<-j) (§10,§13)|           | candidate model1a                                                  |                    |

composition de boucle projective     | model1a   | dépend de l'ordre d'arête déclaré (A<-B<-C<-D<-A) propre à la      | numpy              | tests/models/model1a
H_A, Ad_HA, L_carre, R_carre (§15,   |           | topologie candidate model1a ; pas une brique de graphe générique   |                    |
§17-§18)                             |           |                                                                     |                    |
```

Décision explicite, conformément au mandat :

```text
CORE_PROMOTION_NEEDED            = NO
CORE_PROMOTION_EXECUTED_THIS_LOT = FALSE
CODE_MODIFIED_THIS_LOT           = FALSE
```

Ces opérations restent dans `model1a` initialement, même lorsqu'elles ont l'apparence mathématique d'une brique générique (extraction de projecteur extrémal, composition de liens antilinéaires, holonomie de boucle projective). Elles ne sont pas promues vers `core` au seul motif d'une généralité apparente, conformément au mandat explicite du présent lot. Une promotion future resterait possible sur la base d'un second modèle concret réutilisant identiquement l'une de ces briques (`docs/governance/software-architecture-governance.md` §7).

Aucun cadre de graphe, aucune hiérarchie de classes de connexion, aucun cadre de courbure n'est introduit, conformément au mandat explicite.

---

## 4. Arborescence cible minimale

```text
src/cosmotgg/models/model1a/__init__.py
src/cosmotgg/models/model1a/states.py
src/cosmotgg/models/model1a/links.py
src/cosmotgg/models/model1a/loop.py

tests/models/model1a/__init__.py
tests/models/model1a/test_states.py
tests/models/model1a/test_links.py
tests/models/model1a/test_loop.py
```

Ces zones cibles sont proposées sous réserve des conventions du dépôt ; les noms techniques exacts peuvent être ajustés par le rôle `code` sans changer leur définition normative.

Aucun des éléments suivants n'est introduit à ce stade :

```text
model.py
framework
factory
plugin
class Model1A
graph/groupoid abstraction
connection class hierarchy
curvature framework
```

`model1a` n'importe aucune API `model0a`–`model0e` en production :

```text
MODEL1A_PRODUCTION_IMPORTS_PRIOR_MODELS = NO
```

En particulier, aucune API `model0e` n'est utilisée en production, et aucune direction de changement T1 (\(U\)) n'est introduite.

Les modèles précédents peuvent être mentionnés uniquement dans les tests/le notebook comme continuité scientifique et séparation de branche (`MODEL0_SERIES` / `MODEL1_SERIES`, spécification §2).

---

## 5. Responsabilité de `model1a/states.py`

Responsabilité scientifique strictement bornée aux spécification §4–§7 :

- constantes de la donnée d'arête maximalement intriquée canonique : \(|\Phi^+\rangle\), \(P_{ij}\), \(S_{ij}\) (spécification §5), portées comme valeurs de module ou fonctions auxiliaires privées, sans revendication de base préférée au niveau de l'API publique ;
- constructeur de l'état global `four_qubit_relational_loop_state(eps_AB, eps_BC, eps_CD, eps_DA, M_AB, M_BC, M_CD, M_DA, *, ...)` (spécification §6), assemblé par combinaison linéaire explicite de produits tensoriels ;
- validation fail-closed du domaine fidèle suffisant (spécification §6), sans tolérance ni epsilon, frontière rejetée ;
- réductions \(\rho_{ij}\) pour les quatre arêtes, \(\rho_A,\rho_B,\rho_C,\rho_D\), \(\rho_{AC},\rho_{BD}\) (spécification §7), obtenues via `cosmotgg.core.states.partial_trace` sur les dimensions déclarées `(2,2,2,2)` ; pour `rho_DA`, permutation explicite (SWAP) du résultat brut de `partial_trace` (ordre naturel \(A\otimes D\)) vers l'ordre canonique \(D\otimes A\) (spécification §7, §4) — aucune hypothèse silencieuse sur l'ordre de sortie de la primitive.

Contrat de validation d'entrée fail-closed du constructeur `four_qubit_relational_loop_state(...)` :

- chaque entrée \(\varepsilon_{ij}\) doit être réelle, finie, scalaire ; un `bool`/`numpy.bool_` est rejeté ;
- chaque entrée \(M_{ij}\) doit être de forme `(2,2)`, finie, et unitaire à une tolérance `max_entanglement_unitarity_tolerance` explicitement fournie par l'appelant, sans valeur par défaut ;
- aucune réparation polaire, aucune réparation par normalisation, aucune réparation QR, aucune projection vers l'unitaire le plus proche ; un \(M_{ij}\) invalide lève `ValueError` ;
- ce contrat ne change pas la famille mathématique déclarée (spécification §6) ; il rend uniquement le constructeur fail-closed sur son domaine déclaré.

Ce module ne construit aucun contexte modulaire, aucun lien directionnel, aucune holonomie de boucle.

---

## 6. Responsabilité de `model1a/links.py`

Responsabilité scientifique strictement bornée aux spécification §8–§14 :

- statut modulaire \(K_{ij} = -\ln(\rho_{ij})\) via `cosmotgg.core.modular.modular_hamiltonian`, identification du projecteur extrémal unique (spécification §8) ;
- extraction de la force relationnelle d'arête depuis l'écart spectral de \(\rho_{ij}\) (spécification §9), sans recevoir \(\varepsilon_{ij}\) comme argument indépendant ;
- extraction du lien directionnel \(M_{ij} = \sqrt2\,\Psi_{\text{matrix}}\) depuis le coefficient de l'état fondamental modulaire unique, avec vérification d'unitarité à tolérance explicite (spécification §10) ;
- carte de corrélation vectorielle anti-linéaire \(J_{(i\leftarrow j)}\) (structure de support) et action primaire sur tangentes hermitiennes sans trace \(U_{(i\leftarrow j)}\) (spécification §10) ;
- contrat de lien inverse \(M_{ji} = M_{ij}^{\mathsf T}\), \(U_{(j\leftarrow i)} \circ U_{(i\leftarrow j)} = \text{identité}\) (spécification §12), sans diagonalisation indépendante de \(\rho_{ji}\) ;
- transfert d'arête physique centré \(L_{(i\leftarrow j)}(X) = 2\operatorname{Tr}_j[(I\otimes X)(\rho_{ij}-I_{ij}/4)]\), vérifié contre l'identité analytique gelée \(L_{(i\leftarrow j)} = \varepsilon_{ij}\,U_{(i\leftarrow j)}\) (spécification §13). Nom d'API de production préféré : `centered_edge_transfer`/`state_derived_centered_edge_transfer` ; pas de nom contenant `physical_transfer` (spécification §13, note de terminologie).

Ce module ne construit aucune holonomie de boucle, aucune réponse de boucle.

---

## 7. Responsabilité de `model1a/loop.py`

Responsabilité scientifique strictement bornée aux spécification §15–§22, §25 :

- holonomie de boucle projective \(H_A = M_{AB}\,\overline{M_{BC}}\,M_{CD}\,\overline{M_{DA}}\) et action primaire indépendante de la phase \(\operatorname{Ad}_{H_A}\) (spécification §15), utilisant exactement \(M_{DA}\) dans son orientation canonique \(D\otimes A\) (spécification §4, §12, §15) : aucune substitution silencieuse d'une matrice orientée \(A\otimes D\) de façon incorrecte n'est acceptée — régression d'orientation obligatoire (§9 ci-dessous) ;
- contrôle de jauge pure : vérification que des repères unitaires locaux factorisables \(M_{ij}=G_iG_j^{\mathsf T}\) impliquent \(\operatorname{Ad}_{H_A}=\text{identité}\) (spécification §16) ;
- force de boucle \(w_{\square} = \varepsilon_{AB}\varepsilon_{BC}\varepsilon_{CD}\varepsilon_{DA}\), dérivée des forces d'arête, jamais ajustée indépendamment (spécification §17) ;
- transfert de boucle \(L_{\square}\), composition explicite des quatre transferts centrés, vérifié contre l'identité exacte \(L_{\square}(X)=w_{\square}\operatorname{Ad}_{H_A}(X)\) (spécification §17) ;
- réponse primaire `model1a`, `AMPLITUDE_WEIGHTED_PROJECTIVE_LOOP_RESPONSE` : \(R_{\square}(X)=L_{\square}(X)-w_{\square}X=w_{\square}[\operatorname{Ad}_{H_A}(X)-X]\) (spécification §18) ;
- continuité en lien faible et limite sans relation, comme propriétés vérifiées de \(R_{\square}\) (spécification §19–§20) ;
- covariance de base locale de \(U_{(i\leftarrow j)}\) et de \(R_{\square}\) sous \(V_A\otimes V_B\otimes V_C\otimes V_D\) (spécification §25).

API publique nommée `loop_response`/`projective_loop_response`/`relational_curvature_response_candidate` uniquement (spécification §18) ; interdiction explicite de nommer une fonction de production `riemann`, `tidal_acceleration`, `geodesic_deviation` ou `gravity`.

Ce module n'importe ni `model0a`, ni `model0b`, ni `model0c`, ni `model0d`, ni `model0e`.

---

## 8. Diagnostics et contrôles — statut de conception

Contrôles définis par la spécification, à exposer comme fonctions ou valeurs auxiliaires, sans seuil normatif :

```text
G1 STATE_DERIVATION             : rho_ABCD, K_ij dérivés uniquement des données d'état (states.py, links.py)
G2 FRAME_FIREWALL                : covariance de base locale de U_(i<-j)/R_carre (spécification §25)
G3 CURVATURE_NONTRIVIALITY       : R_carre != 0 pour X1 sur une fixture non centrale (spécification §22)
G4 RELATIVE_DEVIATION            : TANGENT_RESPONSE_CANDIDATE, R_carre agissant différemment sur des tangentes distinctes
G5 UNIFORM_RESPONSE_CONTROL      : F0/F1 (jauge pure/phase centrale) -> R_carre = 0
G6 TENSORIAL_CONTENT             : existence de X0 avec R_carre(X0)=0 et X1 avec R_carre(X1)!=0 (spécification §22)
G7 NO_PREGEOMETRIC_DISTANCE      : absence de distance/aire/plaquette/coordonnée/métrique dans states.py/links.py/loop.py
G8 CONTINUUM_CORRESPONDENCE_OPEN : non ciblé, laissé OPEN
```

Faux positifs (spécification §26), chacun réalisé par une fixture ou une perturbation, sans nouvelle API de production :

```text
F0 — PURE_GAUGE                              -> tests/models/model1a/test_loop.py
F1 — CENTRAL_PHASE                           -> tests/models/model1a/test_loop.py
F2 — WEAK_LINK                               -> tests/models/model1a/test_loop.py
F3 — NO_RELATION                             -> tests/models/model1a/test_loop.py
F4 — REPHASING                               -> tests/models/model1a/test_links.py
F5 — LOCAL_BASIS                             -> tests/models/model1a/test_loop.py
F6 — NONMAX_ENTANGLED                        -> tests/models/model1a/test_links.py
F7 — DEGENERATE_EDGE                         -> tests/models/model1a/test_links.py
F8 — OPEN_PATH_ATTENUATION_FALSE_POSITIVE    -> tests/models/model1a/test_loop.py
```

Ce sont des `NUMERICAL_QUALIFICATION_GUARDS`/contrôles structurels, pas des observables physiques normatives. Aucun seuil scientifique n'est fixé par ce document ; les tolérances numériques d'un futur protocole restent `OPEN` (spécification §31).

---

## 9. Tests prévus — `model1a` (proposition, sans valeur canonique)

Sans fixer de valeur canonique définitive, les tests devront couvrir au minimum :

**`test_states.py`** :

- construction de l'état global sur la fixture analytique primaire (\(M_{AB}=I\), \(M_{BC}=\sigma_X\), \(M_{CD}=I\), \(M_{DA}=\sigma_Y\), \(\varepsilon_{ij}=0.05\)) et sur la fixture de sensibilité d'inégalité de force (spécification §23) ;
- rejet fail-closed hors du domaine fidèle suffisant (spécification §6) ;
- rejet fail-closed des entrées \(\varepsilon_{ij}\) non réelles/non finies/non scalaires (y compris `bool`) et des entrées \(M_{ij}\) de forme incorrecte, non finies, ou non unitaires au-delà de `max_entanglement_unitarity_tolerance` (spécification §10, §6 ci-dessus) : `ValueError` attendu, sans réparation polaire/normalisation/QR/projection ;
- réductions exactes \(\rho_{ij}\), \(\rho_A,\rho_B,\rho_C,\rho_D\), \(\rho_{AC},\rho_{BD}\) contre les formules analytiques du §7 (oracle indépendant), y compris \(\rho_{DA}\) explicitement en ordre \(D\otimes A\) et sa relation par SWAP à \(\rho_{AD}\) si ce dernier est exposé (spécification §7).

**`test_links.py`** :

- statut modulaire : projecteur extrémal unique de \(K_{ij}\) coïncide avec celui de \(\rho_{ij}\), pour \(\varepsilon_{ij}>0\) (spécification §8) ;
- force relationnelle d'arête contre l'oracle spectral \(\varepsilon_{ij}=\lambda_+-\lambda_-\) (spécification §9) ;
- unitarité de \(M_{ij}\) à tolérance explicite (spécification §10) ;
- **F6** (état propre extrémal non maximalement intriqué, test-only) : échec attendu de la porte de lien directionnel unitaire, aucune réparation polaire ;
- **F7** (sous-espace propre extrémal dégénéré, test-only, \(\varepsilon_{ij}=0\)) : échec attendu de l'extraction du lien directionnel, aucune sélection arbitraire de base ;
- contrat de lien inverse \(M_{ji}=M_{ij}^{\mathsf T}\), \(U_{(j\leftarrow i)}\circ U_{(i\leftarrow j)}=\text{identité}\) (spécification §12) ;
- transfert d'arête physique centré \(L_{(i\leftarrow j)}\) contre l'identité analytique gelée \(L=\varepsilon\,U\) (spécification §13) ;
- **F4** (rephasage \(M_{ij}\to e^{i\theta}M_{ij}\)) : \(P_{ij}\), \(U_{(i\leftarrow j)}\) inchangés (spécification §11, §26).

**`test_loop.py`** :

- holonomie de boucle projective \(H_A\), \(\operatorname{Ad}_{H_A}\) contre l'oracle de la fixture analytique primaire (\(H_A=-i\sigma_Z\) à phase près, spécification §23) ;
- **régression d'orientation obligatoire** : recomposer \(H_A\) depuis les réductions reconstruites de l'état global (pas depuis les \(M_{ij}\) fournis en fixture) et vérifier que le résultat coïncide avec l'oracle canonique ; substituer délibérément, dans un test dédié, une matrice \(M_{DA}\) ordonnée de façon incorrecte (\(A\otimes D\) au lieu de \(D\otimes A\)) doit produire un résultat détectablement différent de l'oracle canonique, jamais un passage silencieux (spécification §15) ;
- **F0** (liens factorisables par sommet \(M_{ij}=G_iG_j^{\mathsf T}\)) : \(\operatorname{Ad}_{H_A}=\text{identité}\), `VERTEX_FACTORIZABLE_LINK_FAMILY = PROJECTIVELY_FLAT` (spécification §16) ;
- **F1** (\(H_A=e^{i\phi}I\), \(\varepsilon\) non nuls) : \(R_{\square}=0\) (spécification §26) ;
- force de boucle \(w_{\square}=\varepsilon_{AB}\varepsilon_{BC}\varepsilon_{CD}\varepsilon_{DA}\) et transfert de boucle \(L_{\square}\) contre l'identité exacte \(L_{\square}=w_{\square}\operatorname{Ad}_{H_A}\) (spécification §17) ;
- réponse primaire \(R_{\square}\) contre les oracles de la fixture analytique primaire : \(R_{\square}(Z)=0\), \(R_{\square}(X)=-2w_{\square}X\), \(R_{\square}(Y)=-2w_{\square}Y\) (spécification §23) ;
- **F2** (continuité en lien faible, un \(\varepsilon\to0^+\), holonomie non centrale) : réponse projective brute non nulle, mais \(R_{\square}\to0\) (spécification §19, §26) ;
- **F3** (limite sans relation, tous \(\varepsilon\to0^+\)) : \(\rho\to I/16\), \(w_{\square}\to0\), \(R_{\square}\to0\) (spécification §20, §26) ;
- **F5** (covariance de base locale \(V_A\otimes V_B\otimes V_C\otimes V_D\)) : \(R_{\square}'(V_AXV_A^\dagger)=V_AR_{\square}(X)V_A^\dagger\) (spécification §25, §26) ;
- **F8** (atténuation de chemin ouvert, liens projectivement plats mais forces d'arête inégales sur les deux chemins) : prédictions de chemin ouvert brutes potentiellement différentes, tandis que \(R_{\square}=0\) (spécification §24, §26) ;
- contenu directionnel (spécification §22) : \(X_1\) avec \(R_{\square}(X_1)\neq0\) et \(X_0\) avec \(R_{\square}(X_0)=0\), sur la fixture analytique primaire ;
- absence d'import de `model0a`, `model0b`, `model0c`, `model0d`, `model0e` dans `src/cosmotgg/models/model1a/` (contrôle structurel, cohérent avec `MODEL1A_PRODUCTION_IMPORTS_PRIOR_MODELS = NO`, §4 ci-dessus) ; absence de toute direction de changement T1 (\(U\)) importée.

Les valeurs de test restent explicitement marquées `NON_NORMATIVE_TEST_FIXTURE` et ne constituent pas des `MODEL1A_QUALIFICATION_FIXTURES` normatifs (spécification §31, qui restent `OPEN`).

---

## 10. Intégration croisée avec les modèles précédents

Dépendance de production :

```text
model1a -X-> model0a, model0b, model0c, model0d, model0e
```

Aucune importée en production, conformément au §4 ci-dessus. Un futur notebook pourra mentionner la séparation de branche \(T1\)/\(T2\) (`MODEL0_SERIES` / `MODEL1_SERIES`, spécification §2) sans introduire de dépendance de production.

---

## 11. Absence de scalaire normatif

Ce document ne définit aucun `threshold`, `normalized score`, `ratio`, ni indicateur scalaire de courbure. De telles quantités pourront être introduites ultérieurement par un futur plan de validation ; elles ne font pas partie de la définition scientifique actuelle.

---

## 12. Paramètres non fermés par ce document

```text
NUMERICAL_TOLERANCES                       = OPEN
EDGE_SPECTRAL_TOLERANCE                    = OPEN
MAX_ENTANGLEMENT_UNITARITY_TOLERANCE       = OPEN
MODEL1A_QUALIFICATION_FIXTURES             = OPEN
MODEL1A_ACCEPTANCE_CRITERION               = OPEN
T2_CONFIRMATORY_PROTOCOL                   = NOT_DEFINED
T4_OPERATIONAL_CRITERION                   = UNCHANGED_OPEN
```

---

## 13. Gel documentaire

Ce document et `docs/toy-models/toy1a/specification.md` constituent l'unique lot `docs` pré-implémentation de `toy1a`. Au premier lot de code de `model1a` :

```text
TOY1A_SPECIFICATION         = READ_ONLY_DURING_IMPLEMENTATION
TOY1A_IMPLEMENTATION_DESIGN = READ_ONLY_DURING_IMPLEMENTATION
```

Le récit scientifique de l'exécution appartiendra ensuite à `experiments/toy1a/toy1a.ipynb` (`docs/governance/documentation-governance.md` §11.3). Aucun lot `docs` supplémentaire n'est attendu après le démarrage de l'implémentation, sauf `FUNDAMENTAL_BLOCKING_ONLY` (`docs/governance/documentation-governance.md` §11.2).

---

## 14. Statut et prochaine étape

```text
MODEL1A_IMPLEMENTATION_DESIGN_STATUS = PROPOSED_CORRECTED_PENDING_CHATGPT_REVIEW
MODEL1A_DESIGN_CORRECTION            = EDGE_TENSOR_ORIENTATION_AND_FAIL_CLOSED_INPUT_CONTRACT
```

Corrections apportées par le lot `MODEL1A-DESIGN-CORRECTION-1` : note explicite sur la permutation requise du résultat de `partial_trace` pour `rho_DA` (§2, §5) ; contrat de validation d'entrée fail-closed du constructeur (`states.py`, §5) ; réaffirmation de l'orientation \(D\otimes A\) de \(M_{DA}\) dans l'holonomie et régression d'orientation obligatoire (`loop.py`, §7, §9) ; préférence de nommage `centered_edge_transfer`/`state_derived_centered_edge_transfer` (`links.py`, §6) ; tests supplémentaires de rejet fail-closed et d'orientation (§9). Aucun changement scientifique supplémentaire.

La prochaine étape autorisée est la revue à distance de ce design corrigé par ChatGPT.
