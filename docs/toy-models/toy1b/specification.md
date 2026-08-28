# toy1b — Spécification scientifique proposée

**Statut : `PROPOSED_MODEL1B_T5_FLOW_DESIGN`.**

```text
STATUS                 = PROPOSED_MODEL1B_T5_FLOW_DESIGN
NOT_FROZEN              = TRUE
CHATGPT_REVIEW          = PENDING
IMPLEMENTATION          = NOT_AUTHORIZED
CONFIRMATORY_EXECUTION  = NOT_AUTHORIZED
VALIDATION_PLAN         = NOT_CREATED
```

Ce document définit `model1b`, construction candidate du toy `toy1b`.

Il transforme en contrat explicite un mécanisme de qualification borné pour le contrat intermédiaire `T5-FLOW`, gelé par `docs/model/t5-modular-cross-scale-flow-criteria.md`. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même, et ne redéfinit aucun critère `T5F1`–`T5F11` déjà gelé.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune fixture numérique canonique, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy1b
MODEL_ID = model1b

SPECIFICATION_STATUS = PROPOSED_MODEL1B_T5_FLOW_DESIGN
```

```text
MODEL1B_CLASS = T5_FLOW_MODULAR_CROSS_SCALE_QUALIFICATION
```

---

## 2. Objectif et périmètre déclaré

`toy1b` fournit un mécanisme borné de qualification pour le contrat intermédiaire `T5-FLOW` gelé.

Il teste si un grossissement déterministe d'état par trace partielle, suivi de la donnée modulaire complète \(K_n = -\log(\rho_n)\), supporte une structure relationnelle inter-échelles finie, cohérente, covariante de repère, préservant la platitude, et présentant une variation non triviale.

`toy1b` ne tente PAS :

```text
T5 PASS
continuum reconstruction
metric emergence
Riemann curvature
physical tidal gravity
T4
T6
T7
dark matter
cosmology
C_rel
```

---

## 3. Identité du modèle et pare-feu

```text
MODEL1B_SERIES = T5_FLOW_MODULAR_CROSS_SCALE_QUALIFICATION

MODEL1B_IS_MODEL1A_REOPEN     = NO
MODEL1B_IS_T5_PASS             = NO
MODEL1B_IS_CONTINUUM_MODEL     = NO
MODEL1B_IS_CURVATURE_MODEL     = NO
MODEL1B_IS_GRAVITY_MODEL       = NO
MODEL1B_IS_COSMOLOGY_MODEL     = NO
```

```text
T5_FLOW_PASS       != T5_PASS
FINITE_SCALE_RUNNING != CONTINUUM
FINITE_SCALE_RUNNING != CURVATURE
LOOP_OBJECT        != RIEMANN_CURVATURE
MODULAR_SUPPORT    != PHYSICAL_GEOMETRY
WEIGHT4            != CURVATURE
STATE_SEMIGROUP    != GEOMETRY
```

```text
NO_EXTERNAL_TIME       = TRUE
NO_GRAVITY_SCALE_INPUT = TRUE
```

---

## 4. Référence normative opérationnelle

La référence normative opérationnelle et gelée de ce document est `docs/model/t5-modular-cross-scale-flow-criteria.md` (`T5F1`–`T5F11`, oracles Gibbs, pare-feu de non-classicalité, relation à G1–G8, logique du `T5-FLOW PASS`).

S'y ajoutent, en lecture et sans modification :

```text
docs/model/t5-relational-refinement-boundary.md
docs/model/tidal-relational-curvature-criteria.md
docs/model/hypothesis.md
docs/model/hypothesis-annex-a.md
```

En référence uniquement (portée, style, ne redéfinit rien ici) :

```text
docs/toy-models/toy1a/specification.md
docs/toy-models/toy1a/implementation-design.md
```

Explicitement `EXPLORATORY_ONLY` / `NON_NORMATIVE`, et exclu du contenu scientifique de `model1b` :

```text
features/cosmotgg-early-universe-note.md
```

Ce qui suit ne doit entrer dans `model1b` sous aucune forme :

```text
C_rel
cohesion tensor
early-universe scenario
vacuum memory
local-duration reinterpretation
dark-matter phenomenology
spherical/tangential absorption
```

---

## 5. Système fin et ordre des sites

Huit facteurs qubit, avec un unique étiquetage fin canonique déclaré :

$$
(A, X, Y, B, C, P, Q, D).
$$

Espace de Hilbert :

$$
\mathcal H_2
=
\mathcal H_A \otimes \mathcal H_X \otimes \mathcal H_Y \otimes \mathcal H_B
\otimes \mathcal H_C \otimes \mathcal H_P \otimes \mathcal H_Q \otimes \mathcal H_D.
$$

Chaque facteur local est \(\mathbb C^2\).

Le cycle fin déclaré est :

$$
\Gamma_2:\quad
A \leftarrow X \leftarrow Y \leftarrow B \leftarrow C \leftarrow P \leftarrow Q \leftarrow D \leftarrow A.
$$

Arêtes fines :

```text
AX
XY
YB
BC
CP
PQ
QD
DA
```

L'ordre tensoriel canonique et tout ordre de réduction doivent être explicites. Aucun réordonnancement implicite après trace partielle.

---

## 6. Hiérarchie de décimation

Relativement aux étiquettes fines fixées, on définit des ensembles cumulés de sites éliminés :

$$
E_2 = \varnothing,
\qquad
E_1 = \{P, Q\},
\qquad
E_0 = \{P, Q, X, Y\}.
$$

Ainsi :

$$
\rho_1 = \mathrm{Tr}_{P,Q}(\rho_2),
\qquad
\rho_0 = \mathrm{Tr}_{X,Y}(\rho_1),
$$

et, comme contrôle direct :

$$
\rho_{0,\mathrm{direct}} = \mathrm{Tr}_{P,Q,X,Y}(\rho_2).
$$

Sites survivants ordonnés :

```text
LEVEL_2:
    (A, X, Y, B, C, P, Q, D)

LEVEL_1:
    (A, X, Y, B, C, D)

LEVEL_0:
    (A, B, C, D)
```

Cycles actifs :

$$
\Gamma_2 : A \leftarrow X \leftarrow Y \leftarrow B \leftarrow C \leftarrow P \leftarrow Q \leftarrow D \leftarrow A,
$$
$$
\Gamma_1 : A \leftarrow X \leftarrow Y \leftarrow B \leftarrow C \leftarrow D \leftarrow A,
$$
$$
\Gamma_0 : A \leftarrow B \leftarrow C \leftarrow D \leftarrow A.
$$

```text
REFINEMENT_CATEGORY = SITE_DECIMATION_BY_PARTIAL_TRACE
```

Cette catégorie n'est PAS l'ancien poset de raffinement par subdivision d'arête impaire (`docs/model/t5-relational-refinement-boundary.md`).

```text
REFINEMENT_CATEGORY_SUBSTITUTION = EXPLICIT
```

---

## 7. Exigence de typage de segment impair

La hiérarchie retenue doit préserver le typage de transport \(\mathbb Z_2\) déjà établi (`docs/model/t5-relational-refinement-boundary.md` §3).

Au niveau 1 :

$$
C \leftarrow P \leftarrow Q \leftarrow D
$$

est remplacé par le lien effectif \(C \leftarrow D\), au moyen d'un chemin à TROIS segments.

Au niveau 0 :

$$
A \leftarrow X \leftarrow Y \leftarrow B
$$

est remplacé par le lien effectif \(A \leftarrow B\), au moyen d'un chemin à TROIS segments.

Les deux liens fins éliminés ont donc chacun une longueur de chemin impaire.

```text
COARSE_REPLACEMENT_PATH_PARITY = ODD
TWO_SEGMENT_REPLACEMENT        = FORBIDDEN_FOR_THIS_ROUTE
WHY_8_6_4                      = PRESERVES_ODD_SEGMENT_RELATIONAL_TYPE
```

La hiérarchie exploratoire \(6\to5\to4\) ne fait pas partie de `toy1b`. Ses résultats de scratch restent `NONCONFIRMATORY` et `NONQUALIFYING`.

---

## 8. État de Gibbs relationnel fin

Famille d'états fins :

$$
\rho_2 = \frac{\exp(H_{\mathrm{rel}})}{\mathrm{Tr}[\exp(H_{\mathrm{rel}})]},
$$

avec

$$
H_{\mathrm{rel}} = \sum_{e \in \Gamma_2} \theta_e\, S_e(M_e),
$$

et

$$
S_e(M_e) = 4\, P_e(M_e) - I_e
$$

incorporé sur l'arête fine déclarée, avec \(M_e \in U(2)\).

\(P_e(M_e)\) est le projecteur de rang un maximalement intriqué associé à \(M_e\) sous la même convention d'orientation que l'arête déclarée.

\(\theta_e\) sont des paramètres de couplage relationnel réels finis.

Obligatoire :

```text
THETA != PHYSICAL_TEMPERATURE
THETA != TIME
THETA != LENGTH
THETA != AREA
THETA != REFINEMENT_SCALE
```

Pour \(H_{\mathrm{rel}}\) fini :

$$
\rho_2 > 0
$$

par construction.

Les états grossiers \(\rho_1\) et \(\rho_0\) sont UNIQUEMENT des traces partielles de \(\rho_2\).

Interdit :

```text
independent coarse Hamiltonian target
independent coarse state target
coarse refitting
target geometry
renormalization chosen to match a result
```

---

## 9. Donnée modulaire canonique

À chaque niveau :

$$
K_n = -\log(\rho_n).
$$

C'est la donnée d'échelle canonique.

```text
CANONICAL_SCALE_DATUM = FULL_K_n

PAIR_DATA_IS_CANONICAL_SCALE_DATUM       = NO
LOOP_DATA_IS_CANONICAL_SCALE_DATUM        = NO
SUPPORT_DECOMPOSITION_IS_CANONICAL_DATUM = NO
```

La décomposition de support et les objets de boucle sont uniquement des diagnostics dérivés. Aucune troncature de support n'est autorisée dans \(K_n\).

---

## 10. Représentation de support de Pauli

Pour \(N_n\) qubits survivants, chaînes de Pauli :

$$
P_s = \sigma_{s_1} \otimes \cdots \otimes \sigma_{s_N},
$$

avec \(\sigma_0 = I\) et \(\sigma_{1,2,3}\) les matrices de Pauli.

Coefficient :

$$
c_s(K_n) = 2^{-N_n}\, \mathrm{Tr}[K_n\, P_s].
$$

Poids de support :

$$
w(s) = \text{nombre de facteurs locaux non-identité}.
$$

Décomposition complète :

$$
K_n = \sum_s c_s\, P_s,
$$

et norme de support de Hilbert–Schmidt normalisée :

$$
W_w(K_n) = \sqrt{\sum_{s : w(s)=w} |c_s|^2},
$$

équivalente à la norme de Hilbert–Schmidt normalisée de la composante de poids \(w\).

Ce sont des diagnostics de bookkeeping.

Obligatoire :

```text
W_w != PHYSICAL_DISTANCE
W_w != CURVATURE
W_4 != CURVATURE
```

La qualification `T5F5` doit conserver tous les poids générés.

```text
PAIR_TRUNCATION_CLOSED_UNDER_FLOW = TESTED, NOT ASSUMED
```

---

## 11. Bloc modulaire global à deux corps

Pour chaque paire voisine ordonnée \((i \leftarrow j)\) du cycle ACTIF \(\Gamma_n\), dérivé du \(K_n\) COMPLET :

$$
J_{i\leftarrow j}^{ab}(K_n)
=
-\, 2^{-N_n}\,
\mathrm{Tr}\!\left[K_n\, \sigma_a^{(i)}\, \sigma_b^{(j)}\right],
\qquad a,b \in \{x,y,z\}.
$$

Les lignes appartiennent au site \(i\), les colonnes au site \(j\).

Cette normalisation est fixée pour `toy1b`. Ce n'est pas une normalisation physique ni une constante de renormalisation.

Sous changement de repère local induisant \(R_i, R_j \in SO(3)\) :

$$
J'_{i\leftarrow j} = R_i\, J_{i\leftarrow j}\, R_j^{\mathsf T}.
$$

Obligatoire :

```text
PAIR_BLOCK = DERIVED_DIAGNOSTIC_FROM_FULL_K
PAIR_BLOCK != CANONICAL_DATUM
```

---

## 12. Facteur polaire directionnel

Pour un bloc réel \(3\times3\) \(J\) mathématiquement inversible, définir sa décomposition polaire droite :

$$
J = O\,S,
$$

avec

$$
S = \sqrt{J^{\mathsf T} J} > 0,
\qquad
O = J\,(J^{\mathsf T} J)^{-1/2},
\qquad
O \in O(3).
$$

Définir :

$$
\mathrm{DIRECTIONAL\_FACTOR}(J) = O.
$$

Domaine : \(J \in GL(3,\mathbb R)\).

Si \(J\) est singulier :

```text
DIRECTIONAL_FACTOR = UNDEFINED
```

Aucune pseudo-inverse. Aucune réparation epsilon. Aucun écrêtage silencieux. Aucun seuil de rang arbitraire.

Le conditionnement numérique doit être rapporté séparément de l'existence mathématique.

Un futur plan de validation pourra préenregistrer un seuil d'admissibilité de conditionnement si nécessaire.

---

## 13. Objet de boucle du cycle actif

À chaque niveau, la même loi d'extraction :

$$
K_n \;\rightarrow\; J_{i\leftarrow j} \;\rightarrow\; O_{i\leftarrow j} \;\rightarrow\; Q_n.
$$

Pour le cycle actif :

$$
\Gamma_n : v_0 = A \leftarrow v_1 \leftarrow \cdots \leftarrow v_m = A,
$$

définir :

$$
Q_n = O_{v_0\leftarrow v_1}\, O_{v_1\leftarrow v_2}\, \cdots\, O_{v_{m-1}\leftarrow v_0}.
$$

Le point de base est toujours \(A\).

Le nombre de facteurs varie selon le cycle actif, mais la loi d'extraction ne varie pas.

Sous changement de repère local :

$$
Q_n' = R_A\, Q_n\, R_A^{\mathsf T}.
$$

Par conséquent :

```text
LOOP_OBJECT = GAUGE_COVARIANT
```

et non gauge-invariant.

---

## 14. Diagnostics de boucle invariants de jauge

Chaque cycle actif ayant une longueur paire, la route admissible déclarée attend \(Q_n \in SO(3)\) lorsque tous les facteurs d'arête sont définis avec l'orientation voulue.

Définir le diagnostic de platitude projective :

$$
d_{\mathrm{flat}}(Q_n) = \frac{\|Q_n - I_3\|_F}{\sqrt8}.
$$

Ce scalaire est invariant sous \(Q_n \to R_A\, Q_n\, R_A^{\mathsf T}\).

Plat projectivement signifie \(Q_n = I_3\) mathématiquement. Aucune tolérance numérique de `PASS` n'est fixée dans ce lot de conception.

Définir également le scalaire de classe de conjugaison :

$$
\chi_n = \frac{\mathrm{Tr}(Q_n) - 1}{2}.
$$

Pour \(Q_n \in SO(3)\) : \(\chi_n = \cos(\phi_n)\), invariant de jauge.

Définir la comparaison de variation inter-échelles finie :

$$
\Delta\chi(n,m) = |\chi_n - \chi_m|.
$$

Ceci est un diagnostic structurel dérivé uniquement.

Obligatoire :

```text
Delta_chi != CURVATURE
Delta_chi != CONTINUUM
Delta_chi != PHYSICAL_FORCE
```

---

## 15. Contrôles `T5F3`/`T5F11` par construction

Indépendance de chemin au niveau de l'état :

$$
\mathrm{Tr}_{X,Y}\big[\mathrm{Tr}_{P,Q}(\rho_2)\big]
=
\mathrm{Tr}_{P,Q,X,Y}(\rho_2)
$$

est une conséquence algébrique de la composition de traces partielles.

```text
STATE_FLOW_PATH_INDEPENDENCE = SATISFIED_BY_CONSTRUCTION
```

\(K_0\) est une fonction déterministe de l'état résultant \(\rho_0\) :

$$
K_0 = -\log(\rho_0),
$$

donc l'indépendance de chemin modulaire correspondante est également :

```text
MODULAR_STATE_DERIVED_PATH_INDEPENDENCE = SATISFIED_BY_CONSTRUCTION
```

Les contrôles exécutables sont uniquement des gardes de régression.

Obligatoire :

```text
PARTIAL_TRACE_ASSOCIATIVITY != EMERGENT_GEOMETRY_EVIDENCE
```

---

## 16. Contrôle de cycle de jauge pure

Définir une famille d'arêtes fines de jauge pure via des données unitaires locales par site \(G_i\) :

$$
M_{ij} = G_i\, G_j^{\mathsf T}
$$

sous la convention d'orientation déclarée, avec des forces relationnelles finies \(\theta_e\). Aucune exigence que les amplitudes restent inchangées sous grossissement.

Comportement de qualification requis :

$$
\text{FINE\_PROJECTIVELY\_FLAT}
\rightarrow
\text{LEVEL\_1\_PROJECTIVELY\_FLAT}
\rightarrow
\text{LEVEL\_0\_PROJECTIVELY\_FLAT},
$$

où tout \(Q_n\) défini doit satisfaire la platitude projective.

La variation d'amplitude est autorisée. La non-platitude directionnelle/de boucle ne l'est pas.

```text
PURE_GAUGE_MULTISCALE_FLATNESS = MANDATORY_NEGATIVE_ORACLE
```

---

## 17. Cycle générique non central

Définir une famille de fixture avec :

- \(\theta_e\) finis non nuls ;
- au moins deux \(\theta_e\) distincts ;
- \(M_e\) non gauge-équivalent à un cycle de jauge pure ;
- une structure de cycle fin non centrale/non triviale ;
- aucun paramètre ajusté sur un résultat grossier.

Les valeurs numériques exactes de la fixture NE SONT PAS sélectionnées dans ce lot de conception. Elles doivent être préenregistrées avant l'exécution confirmatoire.

Comportement candidat requis : tous les facteurs directionnels requis sont définis aux niveaux de qualification déclarés ; et au moins une paire finie de niveaux \(n \neq m\) satisfait :

$$
\Delta\chi(n,m) \neq 0
$$

à force relationnelle finie non nulle.

Classer uniquement comme :

```text
FINITE_SCALE_STATE_DERIVED_DIRECTIONAL_RUNNING
```

Jamais :

```text
curvature
continuum
gravity
```

---

## 18. Oracle négatif d'arbre

La route de Gibbs courante requiert :

```text
TREE_DIRECTIONAL_RUNNING = ABSENT_FOR_DECLARED_GIBBS_TREE_FAMILY
```

Définir un contrôle d'arbre dérivé en retirant une arête fine de fermeture de cycle.

Pour chaque chemin fin impair raffiné qui devient une relation de paire grossière induite, comparer :

$$
O_{\mathrm{path}} = \text{produit ordonné des facteurs directionnels fins/de chemin}
$$

avec

$$
O_{\mathrm{coarse}} = \text{facteur polaire directionnel extrait du } K \text{ grossier réel}.
$$

Les deux se transforment selon \(O \to R_{\mathrm{left}}\, O\, R_{\mathrm{right}}^{\mathsf T}\), donc définir l'objet relatif :

$$
D_{\mathrm{tree}} = O_{\mathrm{path}}^{\mathsf T}\, O_{\mathrm{coarse}},
$$

qui se transforme par conjugaison à une extrémité.

L'accord directionnel d'arbre requiert :

$$
D_{\mathrm{tree}} = I
$$

au moyen d'un verdict invariant de jauge.

La topologie d'arbre exacte et les paramètres numériques doivent être gelés avant l'exécution confirmatoire. La fixture d'arbre ne doit pas être utilisée pour fabriquer une boucle.

---

## 19. Contrôle de domaine à relation nulle

Poser :

$$
\theta_e = 0 \quad \text{pour toute arête fine.}
$$

Alors :

$$
H_{\mathrm{rel}} = 0,
\qquad
\rho_2 = \frac{I}{2^8},
$$

et tout \(\rho_n\) est maximalement mixte.

Donc :

$$
K_n = \log(2^{N_n})\, I,
$$

et tout coefficient de Pauli non-identité s'annule.

Par conséquent :

$$
J_{i\leftarrow j} = 0,
$$

et :

```text
DIRECTIONAL_FACTOR = UNDEFINED
```

Obligatoire :

```text
ZERO_RELATION_LOOP_DIRECTION = UNDEFINED_FAIL_CLOSED
```

Aucune orientation arbitraire ne peut être retournée.

---

## 20. Contrôle de covariance de repère local

Pour \(U_i \in SU(2)\) arbitraires sur les sites survivants et éliminés :

- l'état fin se transforme unitairement ;
- la trace partielle doit annuler les changements unitaires agissant exclusivement sur les facteurs éliminés ;
- à chaque niveau survivant :

$$
\rho_n' = U_n\, \rho_n\, U_n^\dagger,
\qquad
K_n' = U_n\, K_n\, U_n^\dagger,
$$
$$
J'_{i\leftarrow j} = R_i\, J_{i\leftarrow j}\, R_j^{\mathsf T},
\qquad
O'_{i\leftarrow j} = R_i\, O_{i\leftarrow j}\, R_j^{\mathsf T},
$$
$$
Q_n' = R_A\, Q_n\, R_A^{\mathsf T},
$$

et :

$$
d_{\mathrm{flat}}(Q_n') = d_{\mathrm{flat}}(Q_n),
\qquad
\chi_n' = \chi_n.
$$

Ceci doit devenir un contrôle de qualification exécutable.

---

## 21. Table de correspondance `T5F` requise

```text
T5F1  -> deterministic partial-trace state law
T5F2  -> fixed cumulative eliminated-site hierarchy
T5F3  -> state path independence, by construction
T5F4  -> full K_n = -log rho_n
T5F5  -> complete modular support, no pair closure
T5F6  -> local-frame covariance
T5F7  -> pure-gauge flatness preservation
T5F8  -> finite noncentral state-derived running
T5F9  -> extraction/fixture/threshold preregistration firewall
T5F10 -> faithful state + singular directional block fail-closed
T5F11 -> 8 -> 6 -> 4 multi-step flow + direct control
```

Pour chaque critère, mécanisme/statut avant exécution/condition d'échec :

| Critère | `MECHANISM` | `STATUS_BEFORE_EXECUTION` | `FAIL_CONDITION` |
|---|---|---|---|
| T5F1 | Grossissement \(\rho_n = \mathrm{Tr}_{I_n}(\rho_{n+1})\), déterministe, §6 | `NOT_EXECUTED` | état grossier cible indépendant fourni ; normalisation externe insérée |
| T5F2 | \(E_2/E_1/E_0\) fixés (§6), sélection déterministe | `NOT_EXECUTED` | sélection non déclarée avant exécution |
| T5F3 | Composition de traces partielles, §15 | `SATISFIED_BY_CONSTRUCTION` | violation numérique de l'identité algébrique (bug) |
| T5F4 | \(K_n = -\log(\rho_n)\), §9 | `NOT_EXECUTED` | \(\rho_n\) non fidèle ; \(K_n\) cible indépendant |
| T5F5 | Support de Pauli complet conservé, §10 | `NOT_EXECUTED` | troncature de poids ≤2 utilisée comme flux exact |
| T5F6 | Covariance de repère local, §20 | `NOT_EXECUTED` | échec de covariance de \(\rho_n\)/\(K_n\)/\(J\)/\(O\)/\(Q_n\) |
| T5F7 | Platitude de jauge pure, §16 | `NOT_EXECUTED` | \(Q_n \neq I_3\) pour une famille de jauge pure déclarée |
| T5F8 | Variation non triviale, §17 | `NOT_EXECUTED` | \(\Delta\chi = 0\) pour toute paire de niveaux à force finie non nulle |
| T5F9 | Préenregistrement avant mesure, §18–19 (renvoi) | `NOT_EXECUTED` | loi modifiée après observation d'un résidu |
| T5F10 | Fermeture sur échec, §12, §19 | `NOT_EXECUTED` | pseudo-inverse, réparation epsilon, ou orientation arbitraire retournée |
| T5F11 | \(\rho_2\to\rho_1\to\rho_0\) plus contrôle direct, §6, §15 | `SATISFIED_BY_CONSTRUCTION` | contrôle direct non implémenté ou divergent |

---

## 22. Pare-feu confirmatoire

Aucun résultat d'audit exploratoire antérieur ne compte comme preuve de qualification `toy1b`.

Y compris :

```text
8->6->4 exploratory audits
6->5->4 exploratory audit
perturbative lambda audits
order-7 audits
global modular scratch audits
```

Tous restent :

```text
NONCONFIRMATORY
NONQUALIFYING
MOTIVATING_EVIDENCE_ONLY
```

Avant toute exécution confirmatoire, un document séparé :

```text
docs/toy-models/toy1b/validation-plan.md
```

doit être créé puis gelé.

Ce futur plan doit préenregistrer au minimum :

- les fixtures numériques exactes ;
- les valeurs exactes \(G_i\)/\(M_e\) site-locales ;
- les valeurs \(\theta\) ;
- la topologie d'arbre ;
- les normes numériques ;
- les niveaux de comparaison ;
- la politique de conditionnement ;
- les tolérances `PASS`/`FAIL` lorsque inévitables ;
- le protocole d'exécution.

`validation-plan.md` n'est PAS créé par ce document.

---

## 23. Ce que `toy1b` n'établit pas

```text
T5 PASS
T4
T6
T7
continuum reconstruction
metric emergence
Riemann curvature
physical tidal gravity
dark matter
cosmology
C_rel
```

`T5-FLOW PASS` lui-même n'est ni revendiqué ni exécuté par ce document (`docs/model/t5-modular-cross-scale-flow-criteria.md` §18–§20).

---

## 24. Paramètres qui restent `OPEN`

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

Aucune valeur n'est fermée par cette spécification.

---

## 25. Sources

Référence normative opérationnelle et gelée : `docs/model/t5-modular-cross-scale-flow-criteria.md` (`T5F1`–`T5F11`).

Frontière structurelle post-`model1a` : `docs/model/t5-relational-refinement-boundary.md`.

Ancrage T2 : `docs/model/tidal-relational-curvature-criteria.md`.

Hypothèse fondatrice : `docs/model/hypothesis.md` (gelé, v0.2) et `docs/model/hypothesis-annex-a.md`.

Référence de style/portée uniquement : `docs/toy-models/toy1a/specification.md`, `docs/toy-models/toy1a/implementation-design.md`.

Exclu du contenu scientifique : `features/cosmotgg-early-universe-note.md` (`EXPLORATORY_ONLY`/`NON_NORMATIVE`).

---

## 26. Statut et prochaine étape

```text
MODEL1B_SPECIFICATION_STATUS = PROPOSED_MODEL1B_T5_FLOW_DESIGN
MODEL1B_DESIGN                = AUTHORIZED
MODEL1B_IMPLEMENTATION         = NOT_AUTHORIZED
MODEL1B_CONFIRMATORY_QUALIFICATION = NOT_AUTHORIZED
MODEL1A_REOPEN                 = NO
```

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
