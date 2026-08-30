# toy1c — Spécification scientifique proposée

**Statut : `PROPOSED`.**

Ce document définit `model1c`, construction candidate du toy `toy1c`.

Il transforme en contrat explicite une famille analytique de raffinement Bell retenue comme premier candidat concret pour débloquer `NEXT_TOY_SCIENTIFICALLY_DESIGNABLE = PREMATURE` (`docs/model/t5a-controlled-cross-scale-limit-criteria.md` §15, `UNBLOCKING_CONDITION`). Il n'ouvre, ne clôt et n'arbitre aucune décision scientifique nouvelle par lui-même au-delà de la construction mathématique déjà arbitrée : famille de raffinement, cellule locale, ancilla, unitaire contrôlé, route de comparaison, seed, seed nul, limite analytique.

Ce document n'est pas un plan de validation, n'inclut aucun code, aucun notebook, aucune fixture numérique de qualification, aucune tolérance numérique, aucun critère d'acceptation.

```text
TOY_ID   = toy1c
MODEL_ID = model1c

MODEL1C_CLASS = T5A_CONTROLLED_CROSS_SCALE_LIMIT_CANDIDATE

MODEL1C_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

T5_FLOW_QUALIFICATION = PASS
T5A_PASS              = NOT_ESTABLISHED
T5_PASS               = NOT_ESTABLISHED

IMPLEMENTATION   = NOT_AUTHORIZED
VALIDATION_PLAN  = NOT_AUTHORIZED
NEXT_MODEL       = NOT_AUTHORIZED
```

---

## 1. Identification

```text
TOY_ID   = toy1c
MODEL_ID = model1c

SPECIFICATION_STATUS = PROPOSED
```

---

## 2. Objectif et périmètre déclaré

`toy1c` cherche uniquement à qualifier une limite contrôlée d'un état réduit bipartite dans un espace cible fixe, sous une famille de raffinement structurelle indexée par un entier `n`, une loi générative locale unique et une route de comparaison commune préenregistrées.

```text
PRIMARY_CLAIM_CLASS = L2_STATE_OBSERVABLE_LIMIT
```

`toy1c` ne revendique PAS :

```text
transport de chemin
L3
L4
continuum
localité physique
métrique
courbure
gravité
non-classicalité
temps relationnel
générateur continu
```

```text
MODEL1C_IS_T5A_PASS                = NO
MODEL1C_IS_T5_PASS                 = NO
MODEL1C_IS_CONTINUUM               = NO
MODEL1C_IS_GEOMETRY                = NO
MODEL1C_IS_CURVATURE               = NO
MODEL1C_IS_GRAVITY                 = NO
MODEL1C_IS_NONCLASSICALITY_PROOF   = NO
```

```text
REFINEMENT_INDEX     = NOT_TIME
BELL_CORRELATION     = NOT_SPACETIME_CURVATURE
BINARY_BRANCHING     = NOT_PHYSICAL_DIMENSION
```

Ce document ne fait pas non plus de `model1c` une exécution de `T5a` : il en est le contrat de conception préalable.

---

## 3. Référence normative opérationnelle

La référence normative opérationnelle et gelée de ce document est `docs/model/t5a-controlled-cross-scale-limit-criteria.md` (`T5A1`–`T5A8`, `T5A-C1`–`T5A-C6`, algèbre de qualification, oracles négatifs `N1`–`N9`, pare-feu faux-positifs `F1`–`F10`, frontière `T5a`/`T5b`), gelé au commit `SCIENTIFIC_CONTENT_HEAD = 7eb2622d9b9ef7ac9bd57751016f09e840e00acf` (`FREEZE_HEAD = 01fb8437034f43547a5f33f95585db5093b98386`).

S'y ajoutent, en lecture et sans modification :

```text
docs/model/t5-full-pass-boundary-feasibility.md
docs/model/t5-modular-cross-scale-flow-criteria.md
docs/model/hypothesis.md
docs/model/hypothesis-annex-a.md
```

En référence uniquement (portée/style, ne redéfinit rien ici) :

```text
docs/toy-models/toy1b/specification.md
docs/toy-models/toy1b/implementation-design.md
```

Ce document préserve intégralement, sans les rouvrir :

```text
T5_FLOW_QUALIFICATION = PASS
T5A_PASS  = NOT_ESTABLISHED
T5_PASS   = NOT_ESTABLISHED
```

---

## 4. Famille de raffinement structurelle

```text
Lambda = N (entiers naturels, n >= 0)

DIRECTION = n -> +infinity = finer structural refinement
```

Nombre de cellules au niveau `n` :

$$
N_n = 2^n.
$$

```text
STRUCTURAL_BRANCHING = BINARY
TERNARY_REFINEMENT    = NOT_USED
```

Le passage \(n \to n+1\) remplace **simultanément** chaque cellule du niveau `n` par deux cellules selon une **même** règle locale (§7).

Pare-feu obligatoire :

```text
n != TIME
n != LENGTH
n != DISTANCE
n != AREA
n != ENERGY
n != PHYSICAL_SCALE
```

`Lambda` est non bornée dans la direction de limite déclarée (aucun élément maximal), dirigée par l'ordre usuel de `N`, sans indexation numérique par une coordonnée physique.

---

## 5. Cellule élémentaire et algèbre de Bell

Chaque cellule élémentaire porte :

$$
H_c = \mathbb C^2 \otimes \mathbb C^2,
$$

dimension locale 4, elle-même un couple de deux facteurs qubit \((c_L, c_R)\) internes à la cellule.

Structure au niveau `n` :

$$
H_n = H_c^{\otimes N_n} = H_c^{\otimes 2^n}.
$$

Chaque cellule porte les quatre matrices de Pauli locales \(\{I, X, Y, Z\}\) sur chacun de ses deux facteurs \(c_L, c_R\).

Générateurs de Bell déclarés (opérateurs \(4\times4\) sur \(H_c\), Pauli identiques sur les deux facteurs) :

$$
G_{\mathrm{BELL}} = \{\, II,\ XX,\ ZZ,\ YY \,\}.
$$

Projecteurs de Bell \(\Pi_k\) (\(k=1,\dots,4\)) : les quatre projecteurs de rang un sur la base de Bell standard de \(H_c\) (états maximalement intriqués \(|\Phi^\pm\rangle\), \(|\Psi^\pm\rangle\)), diagonalisant conjointement \(G_{\mathrm{BELL}}\).

```text
G_BELL_GROUP    = ABELIAN_KLEIN_FOUR_UP_TO_GLOBAL_PHASE
BELL_BASIS_ROLE = SIMULTANEOUS_EIGENBASIS_OF_G_BELL
```

Il s'agit d'un fait mathématique standard (le tordage/« twirl » d'un opérateur sous le groupe de Klein \(\{II,XX,ZZ,YY\}\) coïncide, à conjugaison par phase globale près sur chaque générateur, avec la mesure projective dans la base de Bell) ; il est utilisé sous la forme exacte donnée en §8, pas rederivé ici.

---

## 6. Règle locale de raffinement `R_cell`

Fixer analytiquement le taux de contraction cible vers le secteur de Bell :

```text
p = 1/2
```

Ancilla ajoutée à chaque cellule (dimension 4, indexée par \(G_{\mathrm{BELL}}\)) :

$$
\alpha = \operatorname{diag}\!\Big(\tfrac58,\ \tfrac18,\ \tfrac18,\ \tfrac18\Big)
$$

dans la base \(\{|II\rangle,|XX\rangle,|ZZ\rangle,|YY\rangle\}\) indexée par \(G_{\mathrm{BELL}}\).

Unitaire contrôlé (Pauli contrôlé par l'ancilla), sur \(H_c \otimes H_c\) (dimension \(4\times4=16\), le second facteur \(H_c\) portant la base \(\{|g\rangle\}_{g\in G_{\mathrm{BELL}}}\)) :

$$
U = \sum_{g \in G_{\mathrm{BELL}}} g \otimes |g\rangle\langle g|.
$$

`U` est unitaire (chaque bloc `g` est unitaire, les blocs sont orthogonaux par construction).

Règle locale :

$$
R_{\mathrm{cell}}(\rho) = U\,(\rho \otimes \alpha)\,U^\dagger,
\qquad \rho \in \mathcal D(H_c).
$$

Forme explicite (\(\alpha\) diagonale) :

$$
R_{\mathrm{cell}}(\rho) = \sum_{g \in G_{\mathrm{BELL}}} p_g\, (g\rho g^\dagger) \otimes |g\rangle\langle g|,
\qquad p_{II}=\tfrac58,\ p_{XX}=p_{ZZ}=p_{YY}=\tfrac18.
$$

`R_cell` est CPTP au niveau de la réduction de la première cellule : les opérateurs de Kraus \(K_g = \sqrt{p_g}\, g \otimes |g\rangle\) satisfont \(\sum_g K_g^\dagger K_g = \sum_g p_g\, g^\dagger g \otimes 1 = \big(\sum_g p_g\big) I = I\) puisque chaque `g` est unitaire (\(g^\dagger g = I\)) et \(\sum_g p_g = 1\).

`R_cell` produit un état joint sur **deux** cellules filles (dimension \(4\times4=16\)) : la cellule « système » (premier facteur, dite cellule `0`) et la cellule « nouvelle »/ancilla (second facteur, dite cellule `1`).

---

## 7. Carte réduite dérivée `Phi`

```text
Phi ne doit JAMAIS être introduite comme loi indépendante.
Phi doit être dérivée de R_cell.
```

$$
\Phi(\rho) = \mathrm{Tr}_{\mathrm{new}}\big[R_{\mathrm{cell}}(\rho)\big]
= \sum_{g \in G_{\mathrm{BELL}}} p_g\, g\rho g^\dagger.
$$

Démonstration de l'identité fermée : puisque \(\{|g\rangle\}\) est orthonormée, \(\mathrm{Tr}[\,|g\rangle\langle g|\,]=1\), donc \(\Phi(\rho)=\sum_g p_g\,(g\rho g^\dagger)\).

Avec \(p_{II}=5/8\), \(p_{XX}=p_{ZZ}=p_{YY}=1/8\) :

$$
\Phi(\rho) = \tfrac58 \rho + \tfrac18\big(XX\,\rho\,XX + ZZ\,\rho\,ZZ + YY\,\rho\,YY\big).
$$

Définir le projecteur de Bell :

$$
P_{\mathrm{BELL}}(\rho) = \tfrac14 \sum_{g \in G_{\mathrm{BELL}}} g\rho g^\dagger
= \sum_k \Pi_k \rho \Pi_k.
$$

Identité algébrique exacte :

$$
\tfrac12\,\mathrm{Id}(\rho) + \tfrac12\,P_{\mathrm{BELL}}(\rho)
= \tfrac12\rho + \tfrac18\big(\rho+XX\rho XX+ZZ\rho ZZ+YY\rho YY\big)
= \tfrac58\rho + \tfrac18\big(XX\rho XX+ZZ\rho ZZ+YY\rho YY\big)
= \Phi(\rho).
$$

Donc :

$$
\boxed{\ \Phi = \tfrac12\,\mathrm{Id} + \tfrac12\,P_{\mathrm{BELL}}\ }
$$

`p = 1/2` (§6) est exactement ce coefficient : il n'est pas un paramètre libre supplémentaire, il est arithmétiquement encodé dans les valeurs fixes de `alpha`.

---

## 8. Règle générative globale `G_n`

Pour chaque niveau `n`, `G_n` applique `R_cell` **simultanément et indépendamment** aux `N_n = 2^n` cellules, chacune avec sa propre ancilla fraîche (état `alpha`, non corrélée entre cellules et non corrélée avec l'état courant).

Formellement, en identifiant les cellules du niveau `n` par des chaînes binaires \(b \in \{0,1\}^n\) (niveau 0 : cellule unique, chaîne vide) :

$$
G_n(\rho_n) = \Big(\bigotimes_{b\in\{0,1\}^n} U_b\Big)\;
\Big(\rho_n \otimes \bigotimes_{b\in\{0,1\}^n} \alpha_b\Big)\;
\Big(\bigotimes_{b\in\{0,1\}^n} U_b\Big)^{\!\dagger},
$$

où \(U_b\) agit comme `U` (§6) sur la cellule `b` et son ancilla fraîche dédiée, et comme l'identité ailleurs. Les \(U_b\) agissant sur des facteurs tensoriels deux-à-deux disjoints, ils commutent : l'ordre du produit est sans importance (`TENSORIAL_LOCALITY`, ingrédient utilisé en §10).

Après application, chaque cellule `b` du niveau `n` devient exactement deux cellules `b0` (fille « système », cellule `0` de `R_cell`) et `b1` (fille « ancilla »/nouvelle, cellule `1` de `R_cell`) du niveau `n+1`, dans cet ordre fixe.

```text
E1  une seule loi générative prédéclarée (G_n ci-dessus)
E2  zéro paramètre libre discrétionnaire indépendant par niveau
    (U et alpha sont fixes, identiques à tout n et à toute cellule)
E3  règle d'héritage déclarée pour toute quantité dépendant du niveau :
    R_cell identique à chaque cellule et à chaque n
E5  conventions d'extraction/sélection indépendantes du niveau (§9)
E6  classe de normalisation admissible déclarée : R_cell est CPTP
    (préserve la trace) par construction (§6), aucune normalisation
    post-hoc
```

Interdit :

```text
p_n
retuning
fitted contraction
fitted asymptotic law
post-hoc normalization
```

`E4*` (`HELD_OUT_LEVEL_PREDICTIVITY`) : `NOT_REQUIRED`, `G_n` est entièrement analytique, exacte, complètement prédéclarée, sans élément appris ni calibré.

---

## 9. Route de comparaison commune (`COMMON_TARGET_ROUTE`) et extraction canonique

```text
COMPARISON_ARCHITECTURE = COMMON_TARGET_ROUTE
```

Branche canonique de descendants :

$$
c_n = 0^n \in \{0,1\}^n
$$

(la chaîne de `n` zéros ; niveau 0 : chaîne vide, cellule unique).

Espace de comparaison commun :

$$
X_* = \mathcal D(H_c).
$$

Extraction canonique :

$$
I_n(\rho_n) = \mathrm{Tr}_{H_n \setminus H_{c_n}}(\rho_n) \ \in X_*,
$$

l'état réduit de la cellule `c_n` (trace sur toutes les autres cellules du niveau `n`).

`I_n` est prédéclarée, dérivée uniquement de la structure de famille/raffinement/branche déclarée ci-dessus (§4, §8), indépendante des valeurs observées de l'état. Aucune tour projective n'est requise ; aucune composition \(C_{\nu\leftarrow\mu}\circ C_{\mu\leftarrow\lambda}\) n'est exigée dans cette route.

La convergence visée porte sur :

$$
I_n(\rho_n) \ \longrightarrow\ \sigma_\infty \ \text{dans } X_*.
$$

```text
X_STAR_TOPOLOGY       = TRACE_NORM_TOPOLOGY_ON_D(H_c)
X_STAR_HAUSDORFF       = YES (norme trace, espace métrique standard)
CONVERGENCE_NOTION     = EXACT_CONVERGENCE_IN_TRACE_NORM (limite fermée, cf. §13)
```

---

## 10. Lemme de fermeture obligatoire (`T5A-C3`)

```text
T5A-C3 = REDUCED_PARAMETRIZATION_CLOSURE (ACTIVÉ)
```

**Énoncé.** Sur tout le domaine admissible (\(\rho_n \in \mathcal D(H_n)\) quelconque, corrélé ou non entre cellules) :

$$
I_{n+1} \circ G_n = \Phi \circ I_n.
$$

**Ingrédients requis** (tous utilisés ci-dessous, aucun autre) :

```text
(1) localité tensorielle de G_n ;
(2) caractère trace-preserving des opérations sur les autres cellules ;
(3) même R_cell sur toutes les cellules ;
(4) héritage canonique de la branche c_n.
```

**Lemme auxiliaire (algèbre standard de la trace partielle).** Pour tout opérateur bipartite \(M\) sur \(H_A\otimes H_B\) (corrélé ou non), tout opérateur `A` sur \(H_A\) et tout unitaire `B` sur \(H_B\) :

$$
\mathrm{Tr}_B\big[(A\otimes B)\,M\,(A\otimes B)^\dagger\big] = A\,\mathrm{Tr}_B[M]\,A^\dagger.
$$

(Identité élémentaire : en composantes, \([(A\otimes B)M(A\otimes B)^\dagger]_{ab,a'b'} = \sum_{b_1,b_2} A_{a,\cdot}B_{b,b_1}M_{\cdot b_1,\cdot b_2}B^*_{b',b_2}A^*_{a',\cdot}\) ; sommer sur \(b=b'\) fait apparaître \(\sum_b B_{b,b_1}B^*_{b,b_2} = (B^\dagger B)_{b_2,b_1} = \delta_{b_1 b_2}\) par unitarité de `B`, ce qui réduit exactement à \(A\,\mathrm{Tr}_B[M]\,A^\dagger\).) C'est précisément l'ingrédient (2) : le caractère unitaire — donc trace-preserving — de l'opération sur le facteur tracé.

**Démonstration du lemme de fermeture.** Fixer `n` et \(\rho_n \in \mathcal D(H_n)\), \(H_n = H_{c_n} \otimes H_{\mathrm{rest}}\) (\(c_n = 0^n\)). Étendre à l'espace d'ancillas fraîches : \(H_n \otimes H_{\mathrm{anc}}\), avec \(H_{\mathrm{anc}} = H_{\mathrm{anc},c_n} \otimes H_{\mathrm{anc,rest}}\) (une ancilla fraîche par cellule, tensoriellement disjointes, ingrédient (1)). Regrouper en \(H_{c_n,\mathrm{ext}} \otimes H_{\mathrm{rest,ext}}\), avec \(H_{c_n,\mathrm{ext}} = H_{c_n}\otimes H_{\mathrm{anc},c_n}\) (dimension 16, domaine de `U`, ingrédient (3) : même `R_cell`/`U`/`alpha` pour la cellule `c_n` qu'à toute autre cellule et tout autre niveau) et \(H_{\mathrm{rest,ext}} = H_{\mathrm{rest}}\otimes H_{\mathrm{anc,rest}}\).

Par (1), \(G_n\) agit, dans ce regroupement, comme \(U_{c_n} \otimes V_{\mathrm{rest}}\), où \(U_{c_n}=U\) (§6) et \(V_{\mathrm{rest}}\) est le produit tensoriel (unitaire, car produit de facteurs disjoints deux-à-deux unitaires) des \(U_b\) pour \(b \neq c_n\), agissant uniquement sur \(H_{\mathrm{rest,ext}}\). L'état étendu d'entrée est \(M = \rho_n \otimes \alpha_{c_n} \otimes \alpha_{\mathrm{rest}}\) (\(\alpha_{\mathrm{rest}} = \bigotimes_{b\neq c_n}\alpha_b\)), généralement corrélé entre les facteurs \(c_n,\mathrm{ext}\) et \(\mathrm{rest,ext}\) puisque \(\rho_n\) corrèle en général \(c_n\) et le reste.

Appliquer le lemme auxiliaire avec \(A=U_{c_n}\), \(B=V_{\mathrm{rest}}\) (unitaire par (1)) :

$$
\mathrm{Tr}_{\mathrm{rest,ext}}\big[(U_{c_n}\otimes V_{\mathrm{rest}})\,M\,(U_{c_n}\otimes V_{\mathrm{rest}})^\dagger\big]
= U_{c_n}\,\mathrm{Tr}_{\mathrm{rest,ext}}[M]\,U_{c_n}^\dagger.
$$

Or \(\mathrm{Tr}_{\mathrm{rest,ext}}[M] = \mathrm{Tr}_{H_{\mathrm{rest}}}[\rho_n] \otimes \alpha_{c_n} \otimes \mathrm{Tr}_{H_{\mathrm{anc,rest}}}[\alpha_{\mathrm{rest}}] = I_n(\rho_n)\otimes\alpha_{c_n}\) (trace d'un état normalisé \(=1\)). Donc le membre de gauche, qui est exactement l'état joint des deux cellules filles de \(c_n\) dans \(G_n(\rho_n)\), vaut :

$$
U_{c_n}\big(I_n(\rho_n)\otimes\alpha_{c_n}\big)U_{c_n}^\dagger = R_{\mathrm{cell}}\big(I_n(\rho_n)\big).
$$

Enfin, par (4) : \(c_{n+1} = c_n\!\cdot\!0\) est par définition la cellule fille « système » de `R_cell` (§6). Tracer la cellule sœur \(c_n\!\cdot\!1\) (« nouvelle ») donne, par la définition de `Phi` (§7) :

$$
I_{n+1}(G_n(\rho_n)) = \mathrm{Tr}_{\mathrm{new}}\big[R_{\mathrm{cell}}(I_n(\rho_n))\big] = \Phi(I_n(\rho_n)). \qquad \blacksquare
$$

Aucun test numérique n'est utilisé dans cette démonstration ; aucune fermeture n'est supposée, elle est établie sur tout le domaine admissible.

**Conséquence par récurrence.** Puisque \(I_0(\rho_0) = \rho_0\) (niveau 0 : cellule unique, \(c_0\) = chaîne vide) :

$$
I_n(\rho_n) = \Phi^n(\rho_0), \qquad \rho_n = G_{n-1}\circ\cdots\circ G_0(\rho_0).
$$

Préservé explicitement :

```text
AUTONOMOUS_REDUCED_FLOW_ON_PAIR_OR_LOOP_DATA = NOT_ESTABLISHED
```

(la fermeture ci-dessus porte sur \(I_n(\rho_n)\in\mathcal D(H_c)\), pas sur une paire/boucle au sens de `docs/model/t5-modular-cross-scale-flow-criteria.md`).

---

## 11. Seed canonique et famille admissible

Seed analytique canonique fidèle :

$$
\sigma_0 = \tfrac14\Big[ I + \tfrac14 XX + \tfrac14 XI \Big].
$$

Spectre : \(\{1/8,\,1/4,\,1/4,\,3/8\}\) (somme \(=1\)), donc \(\sigma_0 > 0\).

Seed global initial :

$$
\rho_0 = \sigma_0.
$$

Seed nul structurel :

$$
\sigma_0^{\mathrm{null}} = \tfrac14\Big[ I + \tfrac14 XI \Big].
$$

Famille admissible à un paramètre (généralisation structurelle strictement conservatrice, mêmes générateurs \(XX\)/\(XI\), même normalisation, seul le coefficient de \(XX\) varie) :

$$
\sigma_0(\kappa) = \tfrac14\Big[ I + \kappa\, XX + \tfrac14 XI \Big],
$$

avec \(\sigma_0(1/4) = \sigma_0\) (seed canonique) et \(\sigma_0(0) = \sigma_0^{\mathrm{null}}\) (seed nul). Le domaine admissible de \(\kappa\) est celui garantissant \(\sigma_0(\kappa) \ge 0\) (positivité semi-définie) ; les valeurs numériques exactes utilisées pour une qualification confirmatoire au-delà de \(\kappa\in\{0,1/4\}\) restent `OPEN` (§21).

Domaine :

```text
DOMAIN = D(H_c) (toute matrice densité valide, hermitienne, trace 1, positive semi-définie)
```

`R_cell`/`Phi` sont bien définis sur tout `D(H_c)`, sans exigence de fidélité stricte du seed (§7 : combinaisons positives de conjugaisons unitaires, aucune inversion ni logarithme). La fidélité stricte, quand elle est présente au seed, est en outre préservée (§17).

---

## 12. Limite analytique

Idempotence du projecteur de Bell : \(P_{\mathrm{BELL}}^2 = P_{\mathrm{BELL}}\) (les \(\Pi_k\) sont des projecteurs orthogonaux deux-à-deux, \(P_{\mathrm{BELL}}(\rho)=\sum_k\Pi_k\rho\Pi_k\) est le pinçage sur cette famille de projecteurs, idempotent par construction standard).

Avec \(\Phi = \tfrac12\mathrm{Id} + \tfrac12 P_{\mathrm{BELL}}\) (§7) et \(P_{\mathrm{BELL}}\) idempotent, `Id` et \(P_{\mathrm{BELL}}\) commutent et se décomposent en somme directe de deux sous-espaces spectraux (image de \(P_{\mathrm{BELL}}\), valeur propre \(1\) pour \(\Phi\) ; noyau de \(P_{\mathrm{BELL}}\), valeur propre \(1/2\) pour \(\Phi\)) :

$$
\Phi^n = P_{\mathrm{BELL}} + 2^{-n}\,(\mathrm{Id} - P_{\mathrm{BELL}}).
$$

Pour le seed canonique, \(P_{\mathrm{BELL}}(\sigma_0) = \tfrac14\big[I + \tfrac14 XX\big]\) (\(P_{\mathrm{BELL}}\) fixe \(I\) et \(XX\in G_{\mathrm{BELL}}\), annule \(XI\notin G_{\mathrm{BELL}}\) — cf. §14) :

$$
\sigma_n = \Phi^n(\sigma_0) = P_{\mathrm{BELL}}(\sigma_0) + 2^{-n}\big[\sigma_0 - P_{\mathrm{BELL}}(\sigma_0)\big]
= \tfrac14\Big[ I + \tfrac14 XX + 2^{-n}\,\tfrac14\, XI \Big].
$$

Limite :

$$
\sigma_\infty = \lim_{n\to\infty}\sigma_n = \tfrac14\Big[ I + \tfrac14 XX \Big],
$$

exacte (pas de plateau numérique) : \(\lVert \sigma_n - \sigma_\infty\rVert = 2^{-n}\cdot\lVert\tfrac14\cdot\tfrac14 XI\rVert\to 0\), convergence géométrique en norme trace, établie analytiquement.

Pour le seed nul : \(P_{\mathrm{BELL}}(\sigma_0^{\mathrm{null}}) = \tfrac14 I\), donc \(\sigma_n^{\mathrm{null}} \to I/4\).

Pour la famille \(\sigma_0(\kappa)\) : \(P_{\mathrm{BELL}}(\sigma_0(\kappa)) = \tfrac14[I+\kappa\,XX]\), donc \(\sigma_n(\kappa)\to\tfrac14[I+\kappa\,XX]\) pour tout \(\kappa\) admissible.

Par §10, \(I_n(\rho_n) = \Phi^n(\rho_0)\) : cette limite est donc exactement la limite `T5a` visée par la route `COMMON_TARGET_ROUTE` (§9), établie sans aucune donnée numérique.

```text
EVIDENCE_CLASS  = A_ANALYTIC_LIMIT_PROOF
NUMERICAL_ROLE  = NONE
```

Aucun fit, plateau ou extrapolation numérique n'intervient dans cette preuve. Les tests numériques futurs (implémentation, §22) seront uniquement `CORROBORATIVE_IMPLEMENTATION_CHECKS`, ne faisant pas partie de la preuve `T5a`.

---

## 13. Non-trivialité et séparation des nulls (`T5A6`)

Classe triviale `T` (appropriée à `L2`), contenant au minimum :

```text
* les états produits A tensor B ;
* I/4 (état maximalement mixte de H_c) ;
* la famille nulle déclarée sigma_0^null et sa limite I/4 ;
* toute limite structurellement forcée indépendamment de l'état
  (valeur imposée par la construction quelle que soit la donnée d'entrée).
```

Séparateur analytique :

$$
C_{XX}(\sigma) = \langle XX\rangle_\sigma - \langle XI\rangle_\sigma \langle IX\rangle_\sigma,
\qquad \langle O\rangle_\sigma := \mathrm{Tr}[O\,\sigma].
$$

Pour le seed live à la limite : \(\sigma_\infty = \tfrac14[I+\tfrac14 XX]\), donc \(\langle XI\rangle_\infty = 0\), \(\langle IX\rangle_\infty = 0\), \(\langle XX\rangle_\infty = 1/4\) (coefficient direct dans la décomposition de Pauli normalisée \(\mathrm{Tr}[XX\cdot XX]/4=1\)). Donc :

$$
C_{XX}(\sigma_\infty) = \tfrac14 \neq 0.
$$

Pour tout état produit \(A\otimes B\) : \(\langle XX\rangle = \langle X\rangle_A\langle X\rangle_B = \langle XI\rangle\langle IX\rangle\), donc \(C_{XX}\equiv 0\) — la classe produit appartient bien à `T` sous ce séparateur.

$$
\sigma_\infty \notin \overline{T}, \qquad \mathrm{dist}(C_{XX}(\sigma_\infty), C_{XX}(T)) = 1/4 > 0.
$$

Important :

```text
RELATIONAL_CORRELATION != ENTANGLEMENT
```

`toy1c` n'exige ni ne revendique que \(\sigma_\infty\) soit intriqué : \(C_{XX}\) est un séparateur de corrélation connectée (fonction de covariance de Pauli), pas un critère d'intrication.

Un microscopique \(2^{-n}\,\tfrac14\,XI \to 0\) n'implique donc PAS \(\sigma_\infty \in T\) (§12–§13, conformément à `T5A6`, `MICROSCOPIC_PARAMETER -> 0` n'implique pas `D_infinity IN T`) : la disparition du terme \(XI\) laisse subsister le terme \(XX\) structurellement conservé.

---

## 14. Secteur fixe relationnel `FIX(Phi)`

```text
FIX(Phi) = algèbre/famille d'états Bell-diagonaux
```

\(P_{\mathrm{BELL}}\) fixe exactement l'espace engendré par \(\{I, XX, ZZ, YY\}\) (les générateurs de \(G_{\mathrm{BELL}}\) eux-mêmes, chacun invariant sous le pinçage \(P_{\mathrm{BELL}}\) car élément du groupe tordant) et annule les observables locales non triviales :

$$
XI,\ YI,\ ZI,\ IX,\ IY,\ IZ \ \longmapsto\ 0 \text{ sous } P_{\mathrm{BELL}}.
$$

Les observables jointes \(XX, YY, ZZ\) sont préservées.

```text
CANDIDATE_SPECIFIC_PROPERTY = YES
UNIVERSAL_T5A_CRITERION      = NO
```

Cette propriété appartient à la construction `model1c` ; elle n'est promue à aucun nouveau critère universel `T5a`.

---

## 15. Anti-comparaison-collapse (`N9`)

```text
N9 = COMPARISON_COLLAPSE (discrimination requise)
```

Preuve requise : \(I_n\) ne fabrique pas artificiellement une limite universelle indépendante de l'état d'entrée.

Utiliser deux seeds pré-déclarés de la famille admissible (§11) avec un contenu Bell distinct : tout couple \(\kappa_a \neq \kappa_b\) admissible, en particulier les deux fixtures déjà pré-déclarées \(\kappa_a = 1/4\) (seed live), \(\kappa_b = 0\) (seed nul).

$$
P_{\mathrm{BELL}}(\sigma_0(\kappa_a)) - P_{\mathrm{BELL}}(\sigma_0(\kappa_b))
= \tfrac14(\kappa_a-\kappa_b)\,XX \neq 0
\quad \text{pour } \kappa_a \neq \kappa_b.
$$

Sous \(I_n\) (§10, \(I_n(\rho_0(\kappa)) = \Phi^n(\sigma_0(\kappa))\)) :

$$
\sigma_n(\kappa_a) - \sigma_n(\kappa_b)
= \tfrac14(\kappa_a-\kappa_b)\,XX
+ 2^{-n}\big[(\sigma_0(\kappa_a)-P_{\mathrm{BELL}}(\sigma_0(\kappa_a))) - (\sigma_0(\kappa_b)-P_{\mathrm{BELL}}(\sigma_0(\kappa_b)))\big].
$$

Le premier terme est constant, non nul, indépendant de `n` ; le second tend vers zéro. La distinction ne tend donc pas vers zéro sous `I_n` — elle converge vers la valeur constante non nulle \(\tfrac14(\kappa_a-\kappa_b)\,XX\).

```text
COMPARISON_COLLAPSE = EXCLUDED_ANALYTICALLY
```

Les valeurs numériques exactes d'un troisième couple \((\kappa_a,\kappa_b)\) éventuel, au-delà de \(\{0,1/4\}\), restent `OPEN` pour un futur protocole confirmatoire (§21) ; le mécanisme de séparation ci-dessus est établi pour tout couple admissible, sans dépendre d'une valeur numérique particulière.

---

## 16. Fidélité (`FAITHFULNESS`)

Pour \(\rho > 0\) (fidèle) et \(\alpha > 0\) (fidèle, §6 : \(\{5/8,1/8,1/8,1/8\}\) strictement positifs) :

$$
\rho \otimes \alpha > 0.
$$

La conjugaison par un unitaire (`U`, §6) conserve la stricte positivité (spectre inchangé). Donc \(R_{\mathrm{cell}}(\rho) > 0\) pour tout \(\rho>0\), et par récurrence la famille globale \(\rho_n = G_{n-1}\circ\cdots\circ G_0(\rho_0)\) est fidèle à tout niveau pour tout seed fidèle \(\rho_0\).

Puisque \(I_n\) est une trace partielle d'un état fidèle sur un facteur tensoriel, l'état réduit \(I_n(\rho_n)\) est également fidèle à tout niveau (la trace partielle d'un état strictement positif reste strictement positive).

```text
NO_PSEUDOINVERSE = TRUE
NO_CLIPPING       = TRUE
NO_SILENT_REGULARIZATION = TRUE
```

---

## 17. Invariance d'indexation (`T5A7`)

`Lambda = N` avec l'ordre usuel : tout relabellisation pure de l'indice (renommage de `n` en `n'` préservant l'ordre et la correspondance structurelle avec `N_n = 2^n`) laisse le verdict inchangé.

```text
ABSTRACT_LABEL_RENAMING       = VERDICT_INVARIANT
STRUCTURAL_CARDINALITY_CHANGE = NOT_A_RELABELING_TEST
```

Un changement qui modifierait \(N_n\) (par exemple un raffinement ternaire au lieu de binaire) n'est pas un test de relabellisation admissible ; c'est un changement de construction distinct, hors périmètre de `toy1c`.

Sous `EVIDENCE_CLASS_A` (§12), l'invariance sous sous-réseau cofinal de la limite mathématique effective est un théorème (conséquence de \(\Phi^n\to P_{\mathrm{BELL}}\) le long de tout sous-réseau cofinal de `N`), rapportée `VACUOUS/INHERITED`, pas comme preuve indépendante.

---

## 18. Table de correspondance `T5A` requise

```text
T5A1   -> famille de raffinement N indexée, direction n -> +infinity déclarée, §4
T5A2   -> COMMON_TARGET_ROUTE, I_n dérivée de la structure déclarée, §9
T5A3   -> famille générative unique G_n, E1-E6, §8
T5A4   -> PRIMARY_CLAIM_CLASS = L2, X_* = D(H_c), topologie norme trace, §9
T5A5   -> EVIDENCE_CLASS = A, NUMERICAL_ROLE = NONE, §12
T5A6   -> classe triviale T, séparateur C_XX, §13
T5A7   -> invariance de relabellisation, §17
T5A8   -> préenregistrement P_CORE complet, §19
T5A-C3 -> lemme de fermeture I_{n+1} o G_n = Phi o I_n, §10 (ACTIVÉ)
```

Pour chaque critère, mécanisme/statut avant exécution/condition d'échec :

| Critère | `MECHANISM` | `STATUS_BEFORE_EXECUTION` | `FAIL_CONDITION` |
|---|---|---|---|
| T5A1 | `Lambda=N`, `N_n=2^n`, direction déclarée, §4 | `NOT_EXECUTED` | indice réinterprété comme échelle physique ; direction non déclarée |
| T5A2 | `I_n` dérivée de la branche canonique `c_n=0^n`, §9 | `NOT_EXECUTED` | route construite depuis des valeurs observées ; identification implicite d'objets |
| T5A3 | `G_n` unique, `R_cell` fixe, §8 | `NOT_EXECUTED` | paramètre libre par niveau ; retuning ; loi ajustée a posteriori |
| T5A4 | `L2`, `X_*=D(H_c)`, norme trace, §9 | `NOT_EXECUTED` | promotion de classe sans requalification ; convergence scalaire présentée comme convergence de structure complète |
| T5A5 | preuve analytique fermée, §10, §12 | `NOT_EXECUTED` | preuve remplacée par un fit/plateau numérique |
| T5A6 | `T`, `C_XX`, §13 | `NOT_EXECUTED` | `sigma_infinity` non séparé de `T` ; paramètre microscopique confondu avec appartenance à `T` |
| T5A7 | invariance de relabellisation, §17 | `NOT_EXECUTED` | verdict dépendant du nom de l'indice ; changement de cardinalité présenté comme relabellisation |
| T5A8 | préenregistrement `P_CORE`, §19 | `NOT_EXECUTED` | qualification exécutée sans préenregistrement complet |
| T5A-C3 | lemme de fermeture, §10 | `NOT_EXECUTED` (preuve analytique déjà établie dans ce document, hors exécution) | fermeture supposée sans preuve indépendante ; preuve remplacée par un test numérique |

---

## 19. Préenregistrement `P_CORE` complet (`T5A8`)

```text
1.  refinement family/index         = Lambda=N, N_n=2^n, §4
2.  limit direction/unboundedness   = n -> +infinity, non borné, §4
3.  G / seed / inheritance          = G_n (§8), R_cell/U/alpha fixes (§6),
                                      rho_0 = sigma_0 (§11), R_cell identique
                                      à toute cellule/tout niveau (E3)
4.  COMMON_TARGET_ROUTE + I_n       = X_* = D(H_c), I_n via branche
                                      canonique c_n=0^n, §9
5.  PRIMARY_CLAIM_CLASS             = L2_STATE_OBSERVABLE_LIMIT, §2
6.  X_* / topologie / Hausdorff     = D(H_c), norme trace, Hausdorff, §9
7.  convergence notion              = convergence exacte en norme trace, §9, §12
8.  EVIDENCE_CLASS / NUMERICAL_ROLE = A_ANALYTIC_LIMIT_PROOF / NONE, §12
9.  trivial/null class + seeds      = T (§13), sigma_0 (live), sigma_0^null
                                      (null), sigma_0(kappa) (famille), §11, §13
10. routes conditionnelles          = T5A-C3 ACTIVÉ (§10) ;
                                      T5A-C1, T5A-C2, T5A-C4, T5A-C5, T5A-C6
                                      = NOT_ACTIVATED (§20)
11. domaine / fail-closed           = domaine D(H_c) (§11) ; aucune
                                      pseudo-inverse, aucun clipping, aucune
                                      régularisation silencieuse (§16) ;
                                      seed hors D(H_c) rejeté fail-closed
```

```text
P_NUM = NONE (NUMERICAL_ROLE = NONE, aucun P_NUM artificiel, §12)
```

---

## 20. Critères conditionnels non activés

```text
T5A-C1 = NOT_ACTIVATED  — aucune revendication de taux/exposant/scaling/dérivée
                          par rapport à une coordonnée de raffinement continue ;
                          la contraction géométrique 2^-n de §12 est une
                          conséquence exacte de l'idempotence de P_BELL, pas
                          un exposant de scaling revendiqué séparément.
T5A-C2 = NOT_ACTIVATED  — aucune revendication de générateur continu
                          (REFINEMENT_INDEX = NOT_TIME, §2).
T5A-C4 = NOT_ACTIVATED  — aucun objet directionnel promu porteur de courbure
                          relationnelle cross-scale.
T5A-C5 = NOT_ACTIVATED  — PRIMARY_CLAIM_CLASS = L2, pas L1.
T5A-C6 = NOT_ACTIVATED  — PRIMARY_CLAIM_CLASS = L2, pas L4.
```

Aucune contradiction scientifique découverte pendant la conception ne justifie l'activation de l'un de ces critères.

---

## 21. Oracles négatifs

```text
N1  null seed -> I/4 -> classe triviale, §12-§13
    (sigma_0^null -> I/4, appartenance à T)

N3  index relabeling ne change pas le verdict, §17

N6  tout retuning par niveau -> FAIL
    (E2, §8 : U et alpha fixes, aucun p_n)

N9  comparison collapse : les seeds Bell-distincts ne doivent pas devenir
    indiscernables, §15 (P_BELL(sigma_a) != P_BELL(sigma_b) préservé
    exactement à la limite)
```

Contrôles additionnels spécifiques au candidat :

```text
CLOSE-FAIL
    perturbation de la construction telle que la fermeture réduite ne
    dépende plus seulement de I_n -> T5A-C3 doit échouer.

    Perturbation de référence : remplacer l'ancilla fraîche et
    indépendante alpha_b de chaque cellule b (§8) par une ancilla
    PARTAGÉE entre deux cellules distinctes (ou coupler U_b et U_{b'}
    par une porte agissant conjointement sur les cellules b et b'). La
    démonstration du §10 utilise explicitement, à l'ingrédient (1), que
    les U_b agissent sur des facteurs tensoriels deux-à-deux disjoints :
    une telle perturbation brise cette hypothèse, le lemme auxiliaire de
    trace partielle (§10) ne s'applique plus telle quelle sur la cellule
    c_n isolée, et I_{n+1}(G_n(rho_n)) dépend alors en général de
    corrélations extérieures à I_n(rho_n) seul. Ceci reste une
    construction alternative hors périmètre de `model1c` (§2), déclarée
    ici uniquement comme oracle négatif de conception pour T5A-C3.

LOCAL-ONLY
    seed portant XI mais aucune corrélation de Bell -> limite
    relationnelle triviale, §13 (sigma_0^null, kappa=0 : P_BELL(sigma_0^
    null) = I/4, C_XX(sigma_infinity^null) = 0).

RELATIONAL-LIVE
    seed portant XX -> limite relationnelle non triviale, §13 (sigma_0,
    kappa=1/4 : C_XX(sigma_infinity) = 1/4 != 0).
```

---

## 22. Pare-feu confirmatoire

Aucune exécution numérique n'est requise pour établir la preuve `T5a` de ce candidat (`EVIDENCE_CLASS = A`, §12). Les futures vérifications d'implémentation (§ci-dessous) resteront `CORROBORATIVE_IMPLEMENTATION_CHECKS`, jamais une composante de la preuve de limite elle-même.

Avant toute exécution confirmatoire éventuelle, un document séparé :

```text
docs/toy-models/toy1c/validation-plan.md
```

devra être créé puis gelé, s'il s'avère nécessaire, préenregistrant au minimum les fixtures numériques exactes (valeurs de \(\kappa\) additionnelles éventuelles au-delà de \(\{0,1/4\}\)), les tolérances numériques de régression, et le protocole d'exécution des contrôles corroboratifs.

`validation-plan.md` n'est PAS créé par ce document.

---

## 23. Ce que `toy1c` n'établit pas

```text
T5A_PASS
T5_PASS
T5B_PASS
CONTINUUM
LOCALITY
GEOMETRY
CURVATURE
GRAVITY
PHYSICAL_SCALE
LOCAL_GENERATOR
AUTONOMOUS_REDUCED_FLOW
NONCLASSICALITY
```

Le gel/l'exécution de `T5a` sur ce candidat n'est ni revendiqué ni exécuté par ce document.

---

## 24. Paramètres qui restent `OPEN`

```text
KAPPA_VALUES_BEYOND_0_AND_1_4        = OPEN
NUMERICAL_TOLERANCES                 = OPEN
MODEL1C_ACCEPTANCE_CRITERION         = OPEN
T5A_CONFIRMATORY_PROTOCOL            = NOT_DEFINED
T5A_QUALIFICATION                    = NOT_EXECUTED
```

Sont explicitement `CLOSED` par ce document (contenu structurel/analytique, pas des tolérances d'exécution) :

```text
REFINEMENT_FAMILY       = CLOSED — cf. §4
LOCAL_REFINEMENT_CELL   = CLOSED — cf. §6
REDUCED_PHI             = CLOSED — cf. §7
GLOBAL_GENERATIVE_RULE  = CLOSED — cf. §8
COMMON_TARGET_ROUTE     = CLOSED — cf. §9
CLOSURE_LEMMA           = CLOSED (démontrée) — cf. §10
CANONICAL_SEED          = CLOSED — cf. §11
NULL_SEED               = CLOSED — cf. §11
ANALYTIC_LIMIT          = CLOSED — cf. §12
```

---

## 25. Sources

Référence normative opérationnelle et gelée : `docs/model/t5a-controlled-cross-scale-limit-criteria.md` (`T5A1`–`T5A8`, `T5A-C1`–`T5A-C6`, `N1`–`N9`, `F1`–`F10`).

Frontière de faisabilité amont : `docs/model/t5-full-pass-boundary-feasibility.md` (gelé).

Contrat intermédiaire préservé : `docs/model/t5-modular-cross-scale-flow-criteria.md` (`T5_FLOW_QUALIFICATION = PASS`, non rouvert).

Hypothèse fondatrice : `docs/model/hypothesis.md` (gelé, v0.2) et `docs/model/hypothesis-annex-a.md`.

Référence de style/portée uniquement : `docs/toy-models/toy1b/specification.md`, `docs/toy-models/toy1b/implementation-design.md`.

---

## 26. Statut et prochaine étape

```text
MODEL1C_DESIGN_STATUS = PROPOSED_PENDING_CHATGPT_REVIEW

T5A_PASS = NOT_ESTABLISHED
T5_PASS  = NOT_ESTABLISHED

IMPLEMENTATION   = NOT_AUTHORIZED
VALIDATION_PLAN  = NOT_AUTHORIZED
NEXT_MODEL       = NOT_AUTHORIZED
```

Aucun gel automatique. Aucune implémentation automatique.

La prochaine étape autorisée est la revue à distance de ce design par ChatGPT.
