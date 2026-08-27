# T5 — Frontière structurelle du raffinement relationnel post-model1a

Statut : **T5_RELATIONAL_REFINEMENT_STRUCTURAL_BOUNDARY_NOTE**

Ce document consigne la frontière structurelle établie après la clôture de
qualification de `model1a` entre relation élémentaire, transport de chemin,
raffinement inter-échelles et futur problème T5. Il ne modifie pas
`docs/model/hypothesis.md`, ne modifie pas le critère T2 gelé, ne modifie pas
`docs/model/tidal-relational-curvature-criteria.md`, ne définit aucun
`T5 PASS` et n'autorise la conception d'aucun nouveau toy.

---

## 1. Pare-feu T2 / T5

```text
T2 = state-derived relational connection/curvature
     at declared finite relational level.

T5 = future controlled cross-scale/local/continuum reconstruction.
```

Conséquence :

```text
REFINEMENT_CYLINDRICALITY_REQUIRED_FOR_T2 = NO
REFINEMENT_CYLINDRICALITY_RELEVANT_TO_T5  = YES
```

Aucun renforcement rétroactif de G1 n'est apporté par ce document.

---

## 2. Transport relationnel en deux étages

Terminologie gelée par ce document :

```text
ELEMENTARY_RELATIONAL_LINK:

    extracted directly from an admissible elementary edge state
    rho_ij.

    U_(i<-j)(X) = M_ij X^T M_ij†.

COMPOSITE_PATH_TRANSPORT:

    deterministic ordered composition of elementary links along
    declared path gamma.

    U_gamma = U_en o ... o U_e1.
```

Distinction obligatoire :

```text
ELEMENTARY_LINK = DIRECT_STATE_EXTRACTION
PATH_TRANSPORT  = DERIVED_FROM_STATE_DERIVED_LINKS

PATH_TRANSPORT_IS_ENDPOINT_PAIR_MARGINAL = NO
PATH_TRANSPORT_IS_ENDPOINT_PAIR_RELATION = NO
```

sauf établissement séparé par un travail scientifique futur.

La dépendance au chemin est autorisée. Des chemins différents entre les
mêmes extrémités peuvent différer. Cette différence ne doit jamais être
effacée en forçant un état de paire commun unique.

---

## 3. Graduation Z2

Structure établie enregistrée exactement :

```text
det(U_edge) = -1

det(U_gamma) = (-1)^number_of_edges.
```

Chemin impair : type transposition.
Chemin pair : type conjugaison.

```text
Z2_GRADED_PATH_TRANSPORT = ACCEPTED_STRUCTURAL_FEATURE
```

Enregistré :

```text
TWO_SEGMENT_REPLACEMENT_OF_ELEMENTARY_EDGE = TYPE_INCOMPATIBLE
ODD_SEGMENT_REPLACEMENT                    = TYPE_COMPATIBLE_ONLY
```

Mais aussi :

```text
ODD_ONLY_REFINEMENT_GLOBAL_PROJECTIVE_SYSTEM = NOT_ESTABLISHED
```

---

## 4. Non-directivité (no-go)

Contre-exemple Opus enregistré :

```text
Gamma1:
    A-B

Gamma2:
    A-X-B
```

Sous la règle de remplacement d'arête élémentaire impaire uniquement, il
n'existe aucun raffinement commun satisfaisant les deux décompositions.

Conséquence :

```text
REFINEMENT_POSET_DIRECTEDNESS = FALSE_FOR_CURRENT_ODD_REFINEMENT_RULE
```

Donc :

```text
STANDARD_PROJECTIVE_LIMIT_OVER_ALL_ADMISSIBLE_GRAPHS = UNAVAILABLE_AS_CURRENTLY_DEFINED
```

Ce résultat n'est pas réparé en supprimant silencieusement des graphes
admissibles. Des alternatives potentielles restent `OPEN`, non conçues :

```text
nested directed refinement family
richer graded coarse objects
different incidence category
different state family
```

---

## 5. Non-go au niveau de l'état pour les extrémités

Pour la famille additive par paire actuelle :

```text
rho = 2^-n [ I + sum_e eps_e S_e ]
```

avec termes d'arête sans trace, si A et B n'ont pas d'arête élémentaire
directe, alors :

```text
rho_AB = I_AB/4
```

dans la construction de chaîne testée. Conséquence :

```text
PARTIAL_TRACE_ENDPOINT_COARSE_LINK = ABSENT

STATE_LEVEL_ENDPOINT_REFINEMENT_CURRENT_ADDITIVE_FAMILY = BLOCKED
```

Mais :

```text
T2_GENERAL = NOT_BLOCKED_BY_THIS_RESULT
```

La trace partielle elle-même n'est pas décrite comme défectueuse.
L'obstruction appartient à l'ansatz additif par paire actuel.

---

## 6. État de chemin effectif dérivé

Pour un chemin impair gamma tel que `U_gamma = U_C` et
`eps_gamma = product edge strengths`, l'encodage :

```text
rho_eff(gamma) = (1-eps_gamma) I/4 + eps_gamma P(C)
```

ne peut être enregistré que comme :

```text
DERIVED_PATH_ENCODING
```

Il n'est pas :

```text
partial trace
reduced endpoint state
canonical quantum coarse-graining
evidence of state-level cylindrical consistency
```

Obligatoire :

```text
EFFECTIVE_ODD_PATH_STATE = DERIVED_ENCODING_ONLY
```

Sa dépendance à gamma doit rester explicite.

---

## 7. Couches structurelle / de réponse

Enregistré :

```text
NORMALIZED_DIRECTIONAL_LINK_U = STRUCTURAL_CONNECTION_LAYER_CANDIDATE
PROJECTIVE_HOLONOMY_AdH       = STRUCTURAL_CURVATURE_CARRIER_CANDIDATE

CENTERED_TRANSFER_L               = STATE_RESPONSE_LAYER
AMPLITUDE_WEIGHTED_RESPONSE_R     = STATE_SUPPORTED_RESPONSE_LAYER
```

Les transferts pondérés ne sont pas des morphismes de connexion car :

```text
L_reverse o L_forward = eps^2 I
```

plutôt que `I`.

---

## 8. Flux d'amplitude

Enregistré :

```text
WEIGHTED_RESPONSE_CYLINDRICALITY = NOT_REQUIRED_AT_CURRENT_T2_STAGE
```

L'amplitude peut varier avec l'échelle uniquement si cette variation reste
dérivée de données d'état admissibles. Aucun paramètre de renormalisation
indépendant. Aucune normalisation compensatoire insérée à la main.

Pare-feu obligatoires :

```text
epsilon != length
epsilon != refinement scale
w_loop  != area
w_loop  != cell measure
```

Avertissement structurel enregistré : sous composition répétée de chemins,

```text
product epsilon -> 0
```

pour la construction de réponse actuelle. Conséquence :

```text
AMPLITUDE_WEIGHTED_RESPONSE = NOT_A_CONTINUUM_CURVATURE_CARRIER_BY_ITSELF
```

Toute compensation future exige une dérivation indépendante et une revue G7.

---

## 9. Avertissement G3 / G4

`model1a` a qualifié G3/G4 en utilisant la réponse directionnelle pondérée.
Si un futur travail T5 utilise uniquement l'holonomie projective comme
porteur inter-échelles :

```text
G3/G4 MUST BE REESTABLISHED FOR THAT CROSS-SCALE CONSTRUCTION
```

G3/G4 ne sont pas hérités automatiquement de `model1a` dans ce cas.

---

## 10. Route multipartite

Enregistré :

```text
MULTIPARTITE_RELATIONAL_TERMS = LEGITIMATE_OPEN_ROUTE
```

Raison : l'hypothèse fondatrice et G1 ne restreignent pas les données d'état
relationnel admissibles aux termes additifs par paire. Aucun terme n'est
conçu ici. Aucun terme cible rétro-conçu n'est autorisé.

```text
MULTIPARTITE_EXTENSION = OPEN_NOT_DESIGNED
```

---

## 11. Exigences ouvertes T5

Enregistré comme `OPEN`, pas comme critère `PASS` :

```text
1. directed or otherwise controlled refinement family;
2. parity-compatible coarse/fine path mapping;
3. cross-scale projective connection compatibility;
4. admissible family of state data at each scale;
5. state/connection compatibility across scales;
6. local basis covariance;
7. derived amplitude flow if response layer retained;
8. intrinsic normalization/scale problem;
9. topology/global-holonomy firewall;
10. eventual local/continuum generator.
```

```text
NO metric.
NO distance.
NO area.
NO coordinates.
NO G.
```

---

## 12. Pare-feu Jacobi

```text
RELATIONAL_JACOBI_OPERATOR = PREMATURE
```

Raison : aucune autoparallèle/trajectoire relationnelle, aucune dérivée
suivant une direction relationnelle, aucun champ de déviation transporté le
long d'une telle trajectoire, aucun générateur de courbure locale contrôlé.

---

## 13. Statut suivant

```text
MODEL1A = CLOSED_AT_QUALIFICATION_LEVEL
MODEL1B = NOT_AUTHORIZED

NEXT_MODEL             = OPEN
NEXT_TOY               = NOT_AUTHORIZED
NEXT_SCIENTIFIC_TARGET = T5_REFINEMENT_ROUTE_FEASIBILITY

T2 = OPEN_NOT_EXECUTED
T4 = OPEN_NOT_EXECUTED
T5 = OPEN_NOT_EXECUTED
```
