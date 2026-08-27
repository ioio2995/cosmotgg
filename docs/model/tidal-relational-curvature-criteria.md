# T2 — Critères opérationnels de la courbure relationnelle et de la réponse de marée

Statut : **TIDAL_RELATIONAL_CURVATURE_OPERATIONAL_DEFINITION_NOTE**

Ce document formalise la nouvelle porte opérationnelle entre courbure
relationnelle et contenu gravitationnel local mesurable. Il ne modifie pas
l'hypothèse fondatrice gelée (`docs/model/hypothesis.md`) et n'autorise la
conception d'aucun nouveau toy.

Il complète opérationnellement le test T2 gelé (`docs/model/hypothesis.md`
§15 : *« Une famille de structures modulaires produit-elle une connexion et
une courbure non arbitraires ? »*). Il ne modifie pas le critère PASS de
`hypothesis.md`, ne remplace pas `hypothesis.md`, ne constitue pas un plan de
validation, ne préenregistre pas T2 et n'autorise pas de `model0f`.

---

## 1. Ancrage gelé et absence de réouverture

```text
FROZEN_HYPOTHESIS_REOPEN = NOT_REQUIRED
```

Raison : l'hypothèse fondatrice gelée cible déjà la courbure relationnelle
intrinsèque en premier, la gravitation collective seulement ensuite. Ceci est
déjà inscrit dans `docs/model/hypothesis.md` :

- §8–9 (branche géométrie) : \(\{\rho_{ij}\}\rightarrow\{K_{ij}\}\rightarrow\)
  connexion relationnelle \(\rightarrow\) courbure relationnelle, la courbure
  étant définie *avant* son éventuelle interprétation comme courbure d'un
  espace-temps continu ;
- §10 : « à ce stade, courbure ≠ encore gravitation » ;
- §17 (formulation centrale gelée) : le schéma gelé place explicitement
  « changement relationnel / courbure relationnelle » avant \(N\gg1\rightarrow
  \{\tau,g_{\mu\nu}\}\) puis \(\delta g\stackrel{?}{=}\kappa_*\delta T\).

Aucune modification n'est apportée à `docs/model/hypothesis.md` ni à
`docs/model/hypothesis-annex-a.md` par le présent document.

---

## 2. Frontière de relativité générale connue

Rappel standard de relativité générale (aucune nouvelle hypothèse
CosmoTGG) :

1. les coefficients de connexion / l'accélération uniforme de chute libre
   peuvent être annulés localement par un choix de repère (référentiel
   localement inertiel) ;
2. la courbure de Riemann ne peut pas être supprimée par une telle
   transformation locale de repère ;
3. la déviation géodésique relie la courbure à l'accélération relative :

$$
\frac{D^2\xi^i}{D\tau^2} = -R(u,\xi)\,u
$$

   (à convention de signe près) ;

4. les mesures de marée opérationnalisent donc la courbure à travers la
   déviation relative ;
5. la courbure peut exister dans le vide par la courbure de Weyl ;
6. le couplage Einstein/source est une couche dynamique additionnelle.

```text
VACUUM_CURVATURE_EXISTS   = TRUE (Weyl)
LOCAL_FRAME_REMOVES_CONNECTION_NOT_CURVATURE = TRUE
GEODESIC_DEVIATION_OPERATIONALIZES_CURVATURE = TRUE
EINSTEIN_SOURCE_COUPLING_IS_ADDITIONAL_LAYER = TRUE
```

Références standard : Misner, Thorne & Wheeler, *Gravitation*, W. H.
Freeman (1973) ; Wald, *General Relativity*, University of Chicago Press
(1984) — équivalence locale/déviation géodésique, courbure de Weyl dans le
vide, couplage source/Einstein comme couche additionnelle.

---

## 3. Traduction CosmoTGG (pré-géométrique)

Interdit pré-géométriquement :

```text
spacetime point
spatial distance
xi as pre-existing spatial vector
proper time tau
metric g_mu_nu
Riemann tensor assumed in input
Newtonian potential Phi
G
```

Structure abstraite visée :

```text
RELATIONAL_DEVIATION =
    difference/tangent between nearby admissible relational
    configurations

RELATIONAL_CHANGE_DIRECTION =
    internally derived candidate direction from relational data

RELATIONAL_CURVATURE =
    curvature/holonomy/commutator derived from relational
    connection data

RELATIONAL_TIDAL_RESPONSE =
    action of relational curvature on relational deviation
    along a relational change direction.
```

Schéma uniquement (non identifié au Riemann physique à ce stade) :

$$
J_{\mathrm{rel}}(U)[\Xi] = R_{\mathrm{rel}}(\Xi,U)\,U
$$

```text
NOT_YET_IDENTIFIED_WITH_PHYSICAL_RIEMANN = TRUE
```

---

## 4. Portes nécessaires candidates G1–G8

```text
STATUS = NECESSARY_CANDIDATE_GATES_ONLY
NOT     = T2_PASS
NOT     = T4_PASS
```

### G1 — STATE_DERIVATION

Connexion/courbure construites uniquement depuis des données quantiques
relationnelles admissibles.

### G2 — FRAME_FIREWALL

Les changements purs de repère/base locaux peuvent modifier les
représentants de connexion mais pas la prédiction de courbure/déviation
déclarée.

### G3 — CURVATURE_NONTRIVIALITY

Une structure de courbure non nulle doit avoir une conséquence opérationnelle
invariante et calculable.

### G4 — RELATIVE_DEVIATION

Au moins deux configurations relationnelles voisines reçoivent des réponses
prédites différentes, gouvernées par une structure de courbure fixe unique.

### G5 — UNIFORM_RESPONSE_CONTROL

Une contribution commune/uniforme supprimable par choix de référence ne
compte pas comme contenu de marée.

### G6 — TENSORIAL_CONTENT

La qualification ne peut pas reposer uniquement sur un score de courbure
scalaire unique ; le contenu directionnel/opérateur doit être conservé.

### G7 — NO_PREGEOMETRIC_DISTANCE

Aucune métrique/séparation spatiale n'est insérée pour définir la variable
de déviation microscopique.

### G8 — CONTINUUM_CORRESPONDENCE_OPEN

Ce n'est que plus tard que la réponse relationnelle pourra être testée
contre l'opérateur de Jacobi/déviation géodésique.

---

## 5. Relation T1 / T2 / T4

```text
T1 = relational change branch
T2 = relational connection/curvature branch

POTENTIAL_COMMON_ORIGIN_BRIDGE = RELATIONAL_JACOBI_LAW
STATUS                         = PLAUSIBLE_OPEN_TARGET
```

Le critère T4 gelé (`docs/model/hypothesis.md` §15, note sur T4) n'est pas
modifié. Aucune origine commune entre T1 et T2 n'est revendiquée établie par
le présent document.

---

## 6. Pare-feu gravité / couplage G

```text
TIDAL_CURVATURE          = NOT_EQUIVALENT_TO_EINSTEIN_SOURCE_LAW
VACUUM_TIDAL_CURVATURE   = ALLOWED_IN_GR

T6 = remains late collective universal response/source problem
T7 = remains dimensional coupling comparison

G  = never inserted into microscopic construction
```

---

## 7. Porte de conception suivante

```text
NEXT_TOY_CONCEPTUAL_DESIGN = NOT_AUTHORIZED_BY_THIS_DOCUMENT
```

La prochaine question mathématique autorisée est :

> Can a family of relational modular connections admit a deviation object
> and a curvature action such that a common contribution is removable while
> a differential response remains?

```text
NEXT_MODEL = OPEN_PENDING_MATHEMATICAL_CANDIDATE
NEXT_TOY   = NOT_AUTHORIZED
```
