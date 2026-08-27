# toy1a — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model1a`, construction candidate du toy `toy1a`.

Il transforme en contrat explicite le premier toy `NONCONFIRMATORY` de la branche T2, qualifiant un candidat de connexion/courbure relationnelle discrète et une réponse directionnelle pondérée par l'intensité des relations. Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique par lui-même.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune valeur numérique canonique de paramètre d'état, aucune tolérance numérique, aucun critère d'acceptation.

---

## 1. Identification

```text
TOY_ID   = toy1a
MODEL_ID = model1a

SPECIFICATION_STATUS = PROPOSED
```

```text
MODEL1A_CLASS = T2_PAIRWISE_MODULAR_RELATIONAL_HOLONOMY_QUALIFICATION_NONCONFIRMATORY
```

---

## 2. Position dans les tests CosmoTGG et séparation des branches

```text
COSMOTGG_TEST_TARGET = T2_MODULAR_GEOMETRY
```

Explicitement :

```text
MODEL1A_IS_T2_CONFIRMATORY_TEST = NO
MODEL1A_IS_T4_TEST              = NO

T2 = OPEN_NOT_EXECUTED
T4 = OPEN_NOT_EXECUTED
```

Cible scientifique de `model1a` :

```text
MODEL1A_TARGET = AMPLITUDE_WEIGHTED_PROJECTIVE_LOOP_RESPONSE
```

Séparation explicite des branches (organisation de dépôt/scientifique uniquement, sans réinterprétation physique) :

```text
MODEL0_SERIES = T1_RELATIONAL_CHANGE_EXPLORATION
MODEL1_SERIES = T2_RELATIONAL_CURVATURE_EXPLORATION
```

Aucun document `toy0a`–`toy0e` gelé n'est modifié par ce document.

---

## 3. Référence normative opérationnelle

La référence normative opérationnelle de ce document est `docs/model/tidal-relational-curvature-criteria.md`.

`model1a` cible les portes candidates suivantes :

```text
G1 STATE_DERIVATION
G2 FRAME_FIREWALL
G3 CURVATURE_NONTRIVIALITY
G4 RELATIVE_DEVIATION
G5 UNIFORM_RESPONSE_CONTROL
G6 TENSORIAL_CONTENT
G7 NO_PREGEOMETRIC_DISTANCE
```

```text
G8 CONTINUUM_CORRESPONDENCE_OPEN = OPEN_BY_DESIGN
```

Ces portes sont :

```text
STATUS = NECESSARY_CANDIDATE_GATES_ONLY
NOT     = T2_PASS
NOT     = T4_PASS
```

Pour G4, le nom retenu est strictement `TANGENT_RESPONSE_CANDIDATE`, jamais `GEODESIC_DEVIATION`.

---

## 4. Système

Quatre sous-structures qubit :

$$
\mathcal H_A = \mathcal H_B = \mathcal H_C = \mathcal H_D = \mathbb C^2.
$$

Ordre tensoriel : \(A, B, C, D\).

Topologie relationnelle déclarée :

```text
A -- B
|    |
D -- C
```

Arêtes uniquement :

```text
AB
BC
CD
DA
```

Aucune interprétation spatiale du carré/arête/voisin. « Boucle » désigne uniquement une structure d'incidence relationnelle.

### Orientation tensorielle canonique des arêtes

```text
EDGE_ORIENTATION_AB = A_TENSOR_B
EDGE_ORIENTATION_BC = B_TENSOR_C
EDGE_ORIENTATION_CD = C_TENSOR_D
EDGE_ORIENTATION_DA = D_TENSOR_A
```

Ainsi \(M_{AB}\) est le lien de corrélation anti-linéaire \(B\to A\), \(M_{BC}\) le lien \(C\to B\), \(M_{CD}\) le lien \(D\to C\), et \(M_{DA}\) le lien \(A\to D\) ; la boucle fermée déclarée reste \(A \leftarrow B \leftarrow C \leftarrow D \leftarrow A\) (§15).

Tout objet d'arête (\(P_{ij}\), \(S_{ij}\), \(\rho_{ij}\), \(M_{ij}\)) est représenté dans le produit tensoriel ordonné \(\mathcal H_i \otimes \mathcal H_j\) correspondant exactement à son indice. En particulier, l'arête \(DA\) est représentée dans \(\mathcal H_D \otimes \mathcal H_A\), distinct de l'ordre global \(A,B,C,D\) : \(\rho_{DA} \neq \rho_{AD}\) en tant que représentation matricielle brute. Ces deux représentations ne sont reliées que par un SWAP (§7, §12).

Interdit :

```text
distance
area
plaquette area
coordinate
metric
```

---

## 5. Données d'arête maximalement intriquées

Pour un unitaire \(M_{ij} \in U(2)\), représenté dans l'ordre tensoriel \(\mathcal H_i \otimes \mathcal H_j\) fixé par l'orientation canonique d'arête (§4), définir :

$$
|\Phi(M_{ij})\rangle = (M_{ij} \otimes I)\,|\Phi^+\rangle,
\qquad
|\Phi^+\rangle = \frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

La matrice de coefficients de \(|\Phi(M)\rangle\) est \(M/\sqrt2\).

Définir :

$$
P_{ij} = |\Phi(M_{ij})\rangle\langle\Phi(M_{ij})|,
\qquad
S_{ij} = 4\,P_{ij} - I_{ij}.
$$

Propriétés :

$$
\operatorname{Tr}_i S_{ij} = 0,
\qquad
\operatorname{Tr}_j S_{ij} = 0,
\qquad
\|S_{ij}\| = 3.
$$

Les matrices canoniques \(M\) sont une représentation de fixture uniquement. Les revendications de production sont covariantes par changement de base locale (§25).

---

## 6. État global

### Notation d'inclusion non ambiguë

Définir la notation d'inclusion (« embedding ») :

$$
\operatorname{Embed}_{ij}^{ABCD}(O_{ij})
$$

signifiant : \(O\) agit sur les facteurs \(i,j\) DANS CET ORDRE, l'identité agit sur les facteurs restants, et la matrice globale résultante est représentée dans l'ordre tensoriel global \(A,B,C,D\).

Pour \(AB\), \(BC\), \(CD\), cet ordre coïncide avec l'ordre global (aucune permutation requise). Pour \(DA\), un oracle explicite d'élément de matrice est fourni :

$$
\big[\operatorname{Embed}_{DA}(O)\big]_{(abcd),(a'b'c'd')}
=
O_{(da),(d'a')}\;\delta_{bb'}\,\delta_{cc'}.
$$

### État global

Définir, conceptuellement avec la notation d'inclusion ci-dessus :

$$
\rho_{ABCD}
=
\frac1{16}\Big[
I
+ \varepsilon_{AB}\,\operatorname{Embed}_{AB}(S_{AB})
+ \varepsilon_{BC}\,\operatorname{Embed}_{BC}(S_{BC})
+ \varepsilon_{CD}\,\operatorname{Embed}_{CD}(S_{CD})
+ \varepsilon_{DA}\,\operatorname{Embed}_{DA}(S_{DA})
\Big].
$$

Cette notation peut être abrégée, une fois la convention ci-dessus rendue explicite, en écrivant simplement :

$$
\rho_{ABCD}
=
\frac1{16}\Big[
I
+ \varepsilon_{AB}\,S_{AB}
+ \varepsilon_{BC}\,S_{BC}
+ \varepsilon_{CD}\,S_{CD}
+ \varepsilon_{DA}\,S_{DA}
\Big],
$$

avec l'entente implicite d'inclusion ci-dessus pour chaque terme, en particulier pour \(\operatorname{Embed}_{DA}\). Aucune interprétation spatiale de l'inclusion/l'ordre.

Tous les \(\varepsilon\) sont réels.

Branche de production déclarée :

$$
\varepsilon_{AB} > 0,\qquad
\varepsilon_{BC} > 0,\qquad
\varepsilon_{CD} > 0,\qquad
\varepsilon_{DA} > 0.
$$

Domaine fidèle suffisant :

$$
3\big(\varepsilon_{AB}+\varepsilon_{BC}+\varepsilon_{CD}+\varepsilon_{DA}\big) < 1.
$$

Strict. Aucune tolérance dans cette condition de domaine. Aucune recherche de domaine exact de positivité.

---

## 7. Réductions

Pour chaque arête déclarée, dans son ordre tensoriel canonique (§4) :

$$
\rho_{ij} = (1-\varepsilon_{ij})\,\frac{I_{ij}}4 + \varepsilon_{ij}\,P_{ij}.
$$

### Contrat d'orientation de réduction

Le contrat de réduction de production doit retourner \(\rho_{AB}\) en ordre \(A\otimes B\), \(\rho_{BC}\) en ordre \(B\otimes C\), \(\rho_{CD}\) en ordre \(C\otimes D\), et \(\rho_{DA}\) en ordre \(D\otimes A\).

Si la primitive générique de trace partielle produit naturellement la dernière paire en ordre \(A\otimes D\) (ordre induit par le produit tensoriel global \(A,B,C,D\)), la couche `model1a` doit permuter explicitement le résultat vers \(D\otimes A\). Aucune hypothèse silencieuse sur l'ordre de conservation d'indices de la primitive de trace partielle.

Oracle analytique explicite, en ordre \(D\otimes A\) :

$$
\rho_{DA} = (1-\varepsilon_{DA})\,\frac{I_{DA}}4 + \varepsilon_{DA}\,P_{DA}.
$$

\(\rho_{AD}\) peut optionnellement être exposé, uniquement si clairement nommé et relié par :

$$
\rho_{AD} = \mathrm{SWAP}\,\rho_{DA}\,\mathrm{SWAP}.
$$

Ceci n'est pas requis par `model1a`.

Réductions à un site :

$$
\rho_A = \rho_B = \rho_C = \rho_D = \frac I2.
$$

Réductions de paires non-arêtes :

$$
\rho_{AC} = \frac{I}4,
\qquad
\rho_{BD} = \frac{I}4.
$$

Ce sont des oracles analytiques exacts.

---

## 8. Statut modulaire

Pour chaque arête :

$$
K_{ij} = -\ln(\rho_{ij}).
$$

Pour \(\varepsilon_{ij} > 0\) :

$$
\text{sous-espace propre maximal unique de } \rho_{ij}
=
\text{sous-espace propre minimal unique de } K_{ij}
=
\operatorname{span}\{|\Phi(M_{ij})\rangle\}.
$$

Le lien directionnel peut donc être extrait du projecteur fondamental modulaire.

```text
MODULAR_LINK_PROJECTOR = UNIQUE_MINIMUM_PROJECTOR_OF_K_IJ
STATE_LINK_PROJECTOR   = UNIQUE_MAXIMUM_PROJECTOR_OF_RHO_IJ
```

et :

$$
\text{MODULAR\_LINK\_PROJECTOR} = \text{STATE\_LINK\_PROJECTOR}
$$

pour la famille déclarée. Aucune revendication au-delà de la famille.

---

## 9. Force relationnelle d'arête

Spectre :

$$
\lambda_+ = \frac{1+3\varepsilon_{ij}}4,
\qquad
\lambda_- = \frac{1-\varepsilon_{ij}}4 \quad (\text{multiplicité } 3).
$$

Donc :

$$
\varepsilon_{ij} = \lambda_+ - \lambda_-.
$$

L'extraction de production doit dériver la force depuis \(\rho_{ij}\), et ne pas recevoir \(\varepsilon_{ij}\) comme argument de lien indépendant.

```text
EDGE_RELATIONAL_STRENGTH = SPECTRAL_GAP_OF_RHO_IJ
```

À \(\varepsilon \to 0\) : la force de relation \(\to 0\), le projecteur modulaire/d'état devient dégénéré au point limite.

---

## 10. Lien directionnel

À partir du coefficient de l'état fondamental modulaire unique :

$$
M_{ij} = \sqrt2\,\Psi_{\text{matrix}}.
$$

Exigence : \(M_{ij}\) unitaire, à tolérance d'implémentation explicite près. Aucune tolérance par défaut n'est fournie : un \(M_{ij}\) non unitaire au-delà de la tolérance déclarée est rejeté (`ValueError`), sans réparation polaire, sans réparation par normalisation, sans réparation QR, sans projection vers l'unitaire le plus proche. La phase globale reste arbitraire.

Carte de corrélation vectorielle anti-linéaire (structure de support) :

$$
J_{(i\leftarrow j)}(v) = M_{ij}\,v^{*}.
$$

L'objet de connexion PRIMAIRE agit sur les tangentes d'opérateurs hermitiens sans trace :

$$
U_{(i\leftarrow j)}(X) = M_{ij}\,X^{\mathsf T}\,M_{ij}^\dagger.
$$

Propriétés :

- hermitien \(\to\) hermitien ;
- sans trace \(\to\) sans trace ;
- norme de Hilbert–Schmidt préservée.

```text
DIRECTIONAL_CONNECTION_LINK = U_(i<-j)
```

\(J\) est une structure de support uniquement.

---

## 11. Pare-feu de phase

Sous :

$$
M_{ij} \to e^{i\theta}\,M_{ij},
$$

\(P_{ij}\) et \(U_{(i\leftarrow j)}\) sont inchangés.

```text
RAW_M_PHASE = GAUGE
```

Aucune quantité physique ne peut dépendre de la phase globale du vecteur propre.

---

## 12. Contrat de lien inverse

Pour l'orientation inversée, définir depuis LES MÊMES données d'arête :

$$
M_{ji} = M_{ij}^{\mathsf T}
$$

à une phase compatible non pertinente près. Alors :

$$
U_{(j\leftarrow i)} \circ U_{(i\leftarrow j)} = \text{identité}
$$

sur les tangentes d'opérateurs hermitiens sans trace.

Ne pas diagonaliser indépendamment \(\rho_{ji}\) et choisir un contrat de phase/orientation non lié dans la composition du chemin de production. Aucune revendication d'inverse de carte pondérée.

Pour l'arête de fermeture de boucle (arête stockée/orientée \(DA\), §4) :

$$
M_{AD} = M_{DA}^{\mathsf T}.
$$

Ne pas confondre la réorientation tensorielle \(DA \leftrightarrow AD\) avec une nouvelle diagonalisation arbitraire : la matrice inverse \(M_{AD}\) est dérivée de la même relation d'arête que \(M_{DA}\).

---

## 13. Transfert d'arête physique centré

Pour \(X_j\) hermitien sans trace, définir directement :

$$
L_{(i\leftarrow j)}(X_j)
=
2\,\operatorname{Tr}_j\Big[
(I_i \otimes X_j)\,\big(\rho_{ij} - \tfrac{I_{ij}}4\big)
\Big].
$$

Identité analytique gelée :

$$
L_{(i\leftarrow j)}(X) = \varepsilon_{ij}\,U_{(i\leftarrow j)}(X) = \varepsilon_{ij}\,M_{ij}\,X^{\mathsf T}\,M_{ij}^\dagger.
$$

Distinction enregistrée :

```text
DIRECTIONAL_CONNECTION          = U
PHYSICAL_CENTERED_EDGE_TRANSFER  = L = eps U
```

Aucune normalisation arbitraire.

Note de terminologie : l'étiquette `PHYSICAL_CENTERED_EDGE_TRANSFER` est conservée uniquement comme raccourci historique. « Physical » signifie ici *dérivé de la force de relation portée par la matrice densité*, et non un processus, canal ou observable de marée physique établi. Aucune interprétation CPTP/processus n'est introduite par cette étiquette. Le nom d'API de production préféré est `centered_edge_transfer`/`state_derived_centered_edge_transfer`, pas un nom contenant `physical_transfer`.

---

## 14. Portée boucle paire

Les liens au niveau vecteur sont anti-linéaires. La composition autour de la boucle déclarée à quatre arêtes est donc linéaire.

`model1a` est explicitement limité à :

```text
EVEN_CLOSED_LOOP
```

Aucune revendication pour un cycle impair arbitraire.

```text
ODD_LOOP_GENERALIZATION = OUT_OF_SCOPE_OPEN
```

Aucun cadre de graphe n'est inventé pour le résoudre.

---

## 15. Holonomie de boucle projective

Pour :

$$
A \leftarrow B \leftarrow C \leftarrow D \leftarrow A,
$$

définir :

$$
H_A = M_{AB}\,\overline{M_{BC}}\,M_{CD}\,\overline{M_{DA}}.
$$

Cette expression utilise exactement \(M_{DA}\) dans l'orientation \(D\otimes A\) (§4, §12) : substituer silencieusement une matrice ordonnée de façon incorrecte (\(A\otimes D\)) ne doit jamais se produire ; le chemin de production doit reproduire l'holonomie canonique gelée (§23) à partir des réductions reconstruites depuis l'état global.

\(H_A\) est unitaire. Sa matrice brute n'est définie qu'à une phase scalaire près.

Action primaire indépendante de la phase :

$$
\operatorname{Ad}_{H_A}(X) = H_A\,X\,H_A^\dagger.
$$

```text
PROJECTIVE_LOOP_HOLONOMY = Ad_HA
```

Plate projectivement ssi :

$$
\operatorname{Ad}_{H_A} = \text{identité}
$$

de façon équivalente, dans \(M_2(\mathbb C)\) : \(H_A\) proportionnel à \(I\).

Aucune signification physique n'est attribuée à la phase globale.

---

## 16. Contrôle de jauge pure

S'il existe des repères unitaires locaux \(G_i\) tels que :

$$
M_{ij} = G_i\,G_j^{\mathsf T}
$$

pour les quatre arêtes, alors :

$$
\operatorname{Ad}_{H_A} = \text{identité}.
$$

```text
VERTEX_FACTORIZABLE_LINK_FAMILY = PROJECTIVELY_FLAT
```

Contrôle analytique obligatoire. Ceci ne constitue pas une preuve à propos de connexions plates arbitraires du continuum.

---

## 17. Force et transfert de boucle

Force de boucle :

$$
w_{\square} = \varepsilon_{AB}\,\varepsilon_{BC}\,\varepsilon_{CD}\,\varepsilon_{DA}.
$$

Ce n'est pas un paramètre ajusté indépendamment ; il est dérivé des quatre écarts spectraux d'arête.

Composer les transferts centrés :

$$
L_{\square} = L_{(A\leftarrow B)} \circ L_{(B\leftarrow C)} \circ L_{(C\leftarrow D)} \circ L_{(D\leftarrow A)}.
$$

Identité exacte :

$$
L_{\square}(X) = w_{\square}\,\operatorname{Ad}_{H_A}(X).
$$

---

## 18. Réponse primaire model1a

Définir :

$$
R_{\square}(X) = L_{\square}(X) - w_{\square}\,X,
$$

donc :

$$
R_{\square}(X) = w_{\square}\big[\operatorname{Ad}_{H_A}(X) - X\big].
$$

Nom canonique :

```text
AMPLITUDE_WEIGHTED_PROJECTIVE_LOOP_RESPONSE
```

Ceci est l'objet candidat PRIMAIRE de `model1a`.

Interdit pour l'API de production :

```text
riemann
tidal_acceleration
geodesic_deviation
gravity
```

Préféré :

```text
loop_response
projective_loop_response
relational_curvature_response_candidate
```

---

## 19. Continuité en lien faible

Exigence structurelle obligatoire : pour des données de lien directionnel fixées et toute arête \(e\) :

$$
\varepsilon_e \to 0^+
\quad\Longrightarrow\quad
R_{\square}(X) \to 0
$$

pour tout \(X\) borné.

Brut :

$$
\operatorname{Ad}_{H_A}(X) - X
$$

peut rester non nul. Cette distinction doit être explicite.

À \(\varepsilon_e = 0\) exactement : l'extraction directionnelle d'arête devient non canonique. Aucune réparation. La réponse physique a une limite nulle continue.

---

## 20. Limite sans relation

Lorsque tous les \(\varepsilon_{ij} \to 0^+\) :

$$
\rho_{ABCD} \to \frac I{16},
\qquad
w_{\square} \to 0,
\qquad
R_{\square} \to 0.
$$

Au point limite exact : les orientations de lien sont non définies/non canoniques, mais la limite de réponse est ZÉRO. Aucune orientation ne peut être sélectionnée silencieusement depuis du bruit numérique.

---

## 21. Sonde tangente

\(X\) appartient aux opérateurs hermitiens sans trace \(2\times2\).

Interprétation :

```text
LOCAL_STATE_SPACE_TANGENT_PROBE
```

À \(\rho_A = I/2\), pour tout \(X\) hermitien sans trace fini, il existe un intervalle non vide autour de \(s=0\) tel que :

$$
\rho_A(s) = \frac I2 + sX
$$

est une matrice densité. Intervalle analytique suffisant :

$$
|s|\,\|X\|_{\text{op}} < \frac12.
$$

Aucune interprétation physique de \(s\). \(X\) n'est PAS :

```text
séparation spatiale
vecteur de déplacement
vitesse
accélération
```

---

## 22. Contenu directionnel

Requis, pour une boucle non centrale : il existe \(X_1\) tel que :

$$
R_{\square}(X_1) \neq 0.
$$

De préférence, exhiber \(X_0\) tel que :

$$
R_{\square}(X_0) = 0.
$$

Ceci démontre un contenu opérateur/directionnel. Aucun score de courbure scalaire ne suffit.

---

## 23. Fixtures non normatives

`NON_NORMATIVE_QUALIFICATION_FIXTURE` — fixture analytique primaire :

```text
M_AB = I
M_BC = Pauli_X
M_CD = I
M_DA = Pauli_Y

eps_AB = 0.05
eps_BC = 0.05
eps_CD = 0.05
eps_DA = 0.05
```

Borne fidèle : \(3 \times 0.20 = 0.60 < 1\).

Oracle :

$$
H_A = -i\,\sigma_Z
$$

à phase scalaire près. Donc :

$$
\operatorname{Ad}_{H_A}(Z) = Z,
\qquad
\operatorname{Ad}_{H_A}(X) = -X,
\qquad
\operatorname{Ad}_{H_A}(Y) = -Y.
$$

Et :

$$
w_{\square} = 0.05^4.
$$

Donc :

$$
R_{\square}(Z) = 0,
\qquad
R_{\square}(X) = -2\,w_{\square}\,X,
\qquad
R_{\square}(Y) = -2\,w_{\square}\,Y.
$$

Ce sont des oracles de test indépendants.

Fixture de sensibilité d'inégalité de force (`NON_NORMATIVE`) :

```text
eps_AB = 0.04
eps_BC = 0.05
eps_CD = 0.03
eps_DA = 0.06
```

Mêmes matrices directionnelles \(M\). But :

$$
\text{amplitude}_{AB\_BC} \neq \text{amplitude}_{AD\_DC}.
$$

Aucune revendication que l'atténuation de chemin ouvert inégale est de la courbure.

---

## 24. Pare-feu de boucle fermée

L'invariant PRIMAIRE est la réponse de boucle fermée. Ne PAS définir le candidat de courbure comme :

$$
\text{chemin brut}_1 - \text{chemin brut}_2
$$

car des forces d'arête inégales peuvent produire une différence non nulle même pour des liens directionnels projectivement plats.

```text
OPEN_PATH_RAW_DIFFERENCE = NOT_CURVATURE_INVARIANT
```

L'analyse à deux chemins ne peut apparaître que comme diagnostic, après fermeture explicite à un référentiel de base commun. Aucune normalisation silencieuse des amplitudes de chemin.

---

## 25. Covariance de base locale

Sous :

$$
V_A \otimes V_B \otimes V_C \otimes V_D,
$$

exiger que \(U_{(i\leftarrow j)}\) se transforme de façon covariante, et qu'en base \(A\) :

$$
R_{\square}'(V_A\,X\,V_A^\dagger) = V_A\,R_{\square}(X)\,V_A^\dagger.
$$

\(M\) et \(H_A\) bruts peuvent changer. Le statut physique du candidat est porté par l'action induite.

---

## 26. Contrôles de faux positifs

**F0 — PURE_GAUGE** : liens \(M_{ij}\) factorisables par sommet, \(\varepsilon\) non nuls \(\Rightarrow R_{\square} = 0\).

**F1 — CENTRAL_PHASE** : \(H_A = e^{i\phi} I\), \(\varepsilon\) non nuls \(\Rightarrow R_{\square} = 0\).

**F2 — WEAK_LINK** : un \(\varepsilon \to 0^+\), avec holonomie directionnelle non centrale \(\Rightarrow\) la réponse projective brute reste non nulle mais \(R_{\square} \to 0\).

**F3 — NO_RELATION** : tous les \(\varepsilon \to 0^+ \Rightarrow \rho \to I/16 \Rightarrow R_{\square} \to 0\).

**F4 — REPHASING** : \(M_{ij} \to e^{i\theta_{ij}} M_{ij} \Rightarrow R_{\square}\) inchangé.

**F5 — LOCAL_BASIS** : matrices brutes changent \(\Rightarrow\) réponse covariante.

**F6 — NONMAX_ENTANGLED** : état propre extrémal unique d'arête non maximalement intriqué \(\Rightarrow\) échec de la porte de lien directionnel unitaire. Aucune réparation polaire.

**F7 — DEGENERATE_EDGE** : sous-espace propre extrémal d'arête dégénéré \(\Rightarrow\) échec de l'extraction du lien directionnel. Aucune sélection arbitraire de base.

**F8 — OPEN_PATH_ATTENUATION_FALSE_POSITIVE** : utiliser des liens directionnels projectivement plats mais des produits inégaux de forces d'arête sur \(A\text{-}B\text{-}C\) et \(A\text{-}D\text{-}C\). Attendu : les prédictions de chemin ouvert brutes peuvent différer, tandis que \(R_{\square} = 0\). Donc :

```text
OPEN_PATH_DIFFERENCE != CURVATURE
```

Ce contrôle est obligatoire.

---

## 27. Matrice cible des portes G1–G8

```text
G1 STATE_DERIVATION
G2 FRAME_FIREWALL
G3 CURVATURE_NONTRIVIALITY
G4 RELATIVE_DEVIATION
G5 UNIFORM_RESPONSE_CONTROL
G6 TENSORIAL_CONTENT
G7 NO_PREGEOMETRIC_DISTANCE
```

```text
G8 = OPEN
```

Pour G4, utiliser strictement `TANGENT_RESPONSE_CANDIDATE`, pas `GEODESIC_DEVIATION`.

---

## 28. Claim maximal autorisé

Si la qualification réussit, formulation maximale autorisée :

> Dans la famille finie déclarée à quatre qubits en boucle paire, l'état relationnel par paire détermine des liens de corrélation directionnels indépendants de la phase et leur holonomie de boucle fermée projective. Les mêmes états de paire déterminent les forces d'arête depuis leurs écarts spectraux. Leurs transferts de corrélation centrés se composent en une réponse de boucle projective pondérée par l'amplitude qui est covariante par changement de base locale, directionnelle, nulle pour une jauge pure ou une holonomie centrale, et tend continûment vers zéro lorsqu'une relation requise disparaît. Ceci qualifie un CANDIDAT DE RÉPONSE de courbure relationnelle discrète satisfaisant G1–G7 à l'intérieur de la famille déclarée.

Interdit :

```text
Riemann curvature established
geodesic deviation established
physical tidal acceleration established
spacetime established
gravity established
T2 PASS
T4 PASS
```

---

## 29. Pare-feu T1/T4

```text
NO_MODEL0E_API_IN_PRODUCTION = TRUE
NO_T1_DIRECTION_U_INTRODUCED = TRUE

RELATIONAL_JACOBI_LAW    = NOT_CONSTRUCTED
T1_T2_COMMON_ORIGIN       = NOT_ESTABLISHED

T4 = OPEN_NOT_EXECUTED
T2 = OPEN_NOT_EXECUTED
```

---

## 30. Ce que model1a ne teste pas

Sont exclus :

```text
Riemann curvature
geodesic deviation
physical tidal acceleration
spacetime
gravity
T1 relational change direction
T1 PASS
T2 PASS
T4 PASS
odd-cycle generalization
continuum correspondence
```

---

## 31. Paramètres qui restent `OPEN`

```text
NUMERICAL_TOLERANCES                       = OPEN
EDGE_SPECTRAL_TOLERANCE                    = OPEN
MAX_ENTANGLEMENT_UNITARITY_TOLERANCE       = OPEN
MODEL1A_QUALIFICATION_FIXTURES             = OPEN
MODEL1A_ACCEPTANCE_CRITERION               = OPEN
T2_CONFIRMATORY_PROTOCOL                   = NOT_DEFINED
T4_OPERATIONAL_CRITERION                   = UNCHANGED_OPEN
```

Aucune valeur n'est fermée par cette spécification.

---

## 32. Sources

Référence normative opérationnelle : `docs/model/tidal-relational-curvature-criteria.md` (portes G1–G8, pare-feu gravité/G, frontière GR connue).

Ancrage gelé du test T2 : `docs/model/hypothesis.md` §15 (« T2 — Modular Geometry »).

Séparation de branche par rapport à T1 : `docs/model/t1-relational-physical-change-criteria.md`.

---

## 33. Statut et prochaine étape

```text
MODEL1A_SPECIFICATION_STATUS = PROPOSED_CORRECTED_PENDING_CHATGPT_REVIEW
MODEL1A_DESIGN_CORRECTION    = EDGE_TENSOR_ORIENTATION_AND_FAIL_CLOSED_INPUT_CONTRACT
```

Corrections apportées par le lot `MODEL1A-DESIGN-CORRECTION-1` : déclaration explicite de l'orientation tensorielle canonique de chaque arête (§4, `EDGE_ORIENTATION_AB/BC/CD/DA`), notation d'inclusion non ambiguë avec oracle explicite pour \(DA\) (§6), contrat d'orientation de réduction interdisant toute hypothèse silencieuse sur l'ordre de `partial_trace` (§7), contrat de lien inverse explicite \(M_{AD}=M_{DA}^{\mathsf T}\) (§12), réaffirmation de l'orientation \(D\otimes A\) utilisée par l'holonomie (§15), clarification fail-closed de la validation d'entrée du constructeur (§10), et note de terminologie sur l'étiquette historique `PHYSICAL_CENTERED_EDGE_TRANSFER` (§13). Aucun changement scientifique supplémentaire ; l'oracle canonique d'holonomie (§23) est préservé inchangé.

La prochaine étape autorisée est la revue à distance de ce design corrigé par ChatGPT.
