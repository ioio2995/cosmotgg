# T5-FLOW — Critères du flux relationnel inter-échelles modulaire

Statut : **FROZEN_T5_MODULAR_CROSS_SCALE_FLOW_CRITERIA**

```text
STATUS                         = FROZEN_T5_MODULAR_CROSS_SCALE_FLOW_CRITERIA
NOT_FROZEN                     = FALSE

T5_FLOW_CRITERIA_REVIEW        = PASS
T5_FLOW_CRITERIA_FREEZE        = FROZEN
LIONEL_ORCIL_FREEZE_APPROVAL   = GRANTED
SCIENTIFIC_CONTENT_HEAD        = 7d923bcfeb4cb2e9345a79ed9aec6f6433f08f01

T5_FLOW_CONFIRMATORY_EXECUTION = NOT_AUTHORIZED
T5_FLOW_QUALIFICATION          = NOT_EXECUTED
T5_FULL_PASS_CRITERIA          = PREMATURE
NEXT_TOY                       = NOT_AUTHORIZED
MODEL1A_REOPEN                 = NOT_REQUIRED
OPUS_ESCALATION                = NOT_REQUIRED

FROZEN_DOCUMENT_MODIFICATION   = NEW_EXPLICIT_DECISION_REQUIRED_FOR_SEMANTIC_CHANGE
```

Ce document définit le contrat normatif **gelé** de la qualification
intermédiaire `T5-FLOW` : un flux relationnel inter-échelles dérivé de
l'état, déterministe. Il ne définit ni `T5 PASS`, ni géométrie continue,
ni courbure, ni gravitation, ni nouveau toy, ni échelle physique.

Il s'appuie sur `docs/model/hypothesis.md` (gelé, v0.2),
`docs/model/tidal-relational-curvature-criteria.md` et
`docs/model/t5-relational-refinement-boundary.md`, sans les modifier.

Les critères ci-dessous sont gelés après revue scientifique finale
ChatGPT (`PASS`, contenu scientifique de référence au commit
`7d923bcfeb4cb2e9345a79ed9aec6f6433f08f01`) et validation explicite de
Lionel ORCIL. Toute modification ultérieure de sens exige une nouvelle
décision explicite (`docs/governance/documentation-governance.md` §7).

Obligatoire :

```text
DOCUMENT_FREEZE != T5_FLOW_PASS
DOCUMENT_FREEZE != T5_PASS
DOCUMENT_FREEZE != CONTINUUM
DOCUMENT_FREEZE != GEOMETRY
DOCUMENT_FREEZE != CURVATURE
DOCUMENT_FREEZE != GRAVITY
```

Le gel documentaire valide ce document comme contrat normatif de
référence ; il ne valide pas `T5-FLOW` scientifiquement par exécution.

---

## 1. Périmètre

```text
T2 = finite relational connection/curvature candidate problem.

T5 = controlled cross-scale/local/continuum reconstruction problem.

T5-FLOW =
    intermediate qualification of a deterministic state-derived
    cross-scale relational flow.
```

Obligatoire :

```text
T5_FLOW_PASS != T5_PASS
T5_FLOW_PASS != CONTINUUM_GEOMETRY
T5_FLOW_PASS != CURVATURE
T5_FLOW_PASS != GRAVITY
T5_FLOW_PASS != T4_PASS
```

L'égalité exacte de l'holonomie à échelle finie n'est pas requise par un
T5 gelé :

```text
EXACT_FINITE_SCALE_HOLONOMY_INVARIANCE_REQUIRED_FOR_T5 = NO
```

Une variation structurelle dérivée de l'état à échelle finie est admissible,
à condition que la loi soit fixée avant mesure et reste falsifiable.

---

## 2. Route courante testée

Pour la route modulaire finie de Type I actuellement testée :

$$
\rho_{n+1} \rightarrow \rho_n = \mathrm{Tr}_{I_n}[\rho_{n+1}]
$$

$$
K_n = -\log(\rho_n).
$$

```text
REFINEMENT_CATEGORY = SITE_DECIMATION_BY_PARTIAL_TRACE
```

Cette catégorie est distincte du raffinement par subdivision d'arête
impaire.

```text
REFINEMENT_CATEGORY_SUBSTITUTION = EXPLICIT
```

Aucune identification silencieuse des deux catégories n'est autorisée.

Typage des sites éliminés cumulés (utilisé par T5F3, §6) : relativement à
un étiquetage de sites fins fixé une fois pour toutes, pour chaque niveau
\(n\) on note \(E_n\) l'ensemble cumulé des sites déjà éliminés pour
produire \(\rho_n\). Si \(n_1 \le n_2\) (niveau \(n_1\) plus grossier ou
égal), alors \(E_{n_1} \supseteq E_{n_2}\). L'ensemble éliminé à une étape
unique est :

$$
I_n = E_n \setminus E_{n+1},
$$

de sorte que \(\rho_n = \mathrm{Tr}_{I_n}[\rho_{n+1}]\) ci-dessus s'écrit de
façon équivalente et bien typée :

$$
\rho_n = \mathrm{Tr}_{E_n \setminus E_{n+1}}[\rho_{n+1}].
$$

La donnée d'échelle canonique testée est définie comme :

```text
CANONICAL_SCALE_DATUM_n = K_n = -log(rho_n)
```

sur l'algèbre factorisée tensoriellement déclarée au niveau \(n\) (cf.
T5F4, §7). Sa décomposition résolue en support complet constitue une
représentation de bookkeeping et d'analyse du flux, notée :

```text
COMPLETE_REPRESENTATION_OF_K_n
```

Cette décomposition n'est pas une seconde donnée physique indépendante de
\(K_n\). Aucun coefficient local particulier de cette décomposition (par
exemple un unique coefficient de Pauli) n'est déclaré invariant de repère :
chaque bloc se transforme selon sa représentation tensorielle sous
unitaire local (T5F6, §9).

```text
FULL_MODULAR_STRUCTURE_AS_SCALE_DATUM = CURRENT_ROUTE_CANDIDATE
```

Obligatoire :

```text
CANONICAL_SCALE_DATUM_IS_GEOMETRY   = NO
CANONICAL_SCALE_DATUM_IS_CONNECTION = NO
CANONICAL_SCALE_DATUM_IS_CURVATURE  = NO
```

---

## 3. Pare-feu d'échelle

Obligatoire :

```text
DECIMATION_LEVEL != PHYSICAL_LENGTH_SCALE
DECIMATION_LEVEL != DISTANCE
DECIMATION_LEVEL != AREA
DECIMATION_LEVEL != TIME

lambda != PHYSICAL_SCALE
lambda != TIME
lambda != DISTANCE
lambda != AREA
lambda != INVERSE_PHYSICAL_TEMPERATURE

theta != PHYSICAL_INVERSE_TEMPERATURE
```

Aucune métrique, aucune coordonnée, aucune distance, aucune aire, aucun
\(G\), aucune échelle de Planck ne peut entrer dans la loi
inter-échelles pré-géométrique.

---

## 4. T5F1 — Loi de grossissement dérivée de l'état

Critère : `T5F1_STATE_DERIVED_COARSE_LAW`.

`PASS` requiert que \(\rho_n\) soit obtenu à partir de \(\rho_{n+1}\) par
une application d'état admissible fixée, déclarée avant exécution.

Pour la route courante :

$$
\rho_n = \mathrm{partial\_trace}(\rho_{n+1}, I_n).
$$

`FAIL` si :

- un état cible grossier choisi indépendamment est fourni ;
- des paramètres grossiers sont ajustés pour reproduire une géométrie
  désirée ;
- une normalisation externe est insérée pour réparer un résultat.

---

## 5. T5F2 — Catégorie de raffinement et sélection des sites

Critère : `T5F2_REFINEMENT_CATEGORY_AND_SELECTION`.

`PASS` requiert :

- la catégorie de raffinement déclarée ;
- les ensembles de sites emboîtés déclarés ;
- une sélection déterministe du sous-système éliminé ;
- une loi de sélection déclarée avant mesure.

Obligatoire :

```text
SITE_SELECTION_LAW = DECLARED_BEFORE_CONFIRMATORY_EXECUTION
```

Aucune signification spatiale physique ne peut être inférée du nombre de
sites ou de la profondeur de décimation.

---

## 6. T5F3 — Composition d'états

Critère : `T5F3_STATE_COMPOSITION`.

En utilisant les ensembles de sites cumulés \(E_n\) déclarés au §2,
relatifs à un unique étiquetage de sites fins fixé, pour trois niveaux
emboîtés \(n_0 \le n_1 \le n_2\) (donc \(E_{n_0} \supseteq E_{n_1}
\supseteq E_{n_2}\)), requis :

$$
\mathrm{Tr}_{E_{n_0}\setminus E_{n_1}}\Big[\mathrm{Tr}_{E_{n_1}\setminus E_{n_2}}(\rho_{n_2})\Big]
=
\mathrm{Tr}_{E_{n_0}\setminus E_{n_2}}(\rho_{n_2}).
$$

Cas particulier utile pour l'exigence multi-étapes (T5F11, §14), avec
\(E_2=\varnothing\) au niveau fin de référence :

$$
\mathrm{Tr}_{E_0\setminus E_1}\big[\mathrm{Tr}_{E_1}(\rho_2)\big]
=
\mathrm{Tr}_{E_0}(\rho_2).
$$

Une notation équivalente par pas disjoints (\(I_{n_1}=E_{n_1}\setminus
E_{n_2}\), \(I_{n_0}=E_{n_0}\setminus E_{n_1}\)) n'est admissible que si la
condition de disjonction \(I_{n_0}\cap I_{n_1}=\varnothing\) est rendue
explicite.

Opérationnellement :

```text
DIRECT_REDUCTION = SEQUENTIAL_REDUCTION.
```

`PASS` requiert l'indépendance de chemin au niveau de l'état pour chaque
chaîne de qualification déclarée.

---

## 7. T5F4 — Donnée modulaire canonique

Critère : `T5F4_CANONICAL_MODULAR_DATUM`.

À chaque niveau :

$$
K_n = -\log \rho_n.
$$

`PASS` requiert :

- \(\rho_n\) fidèle dans le domaine de Type I fini ;
- \(K_n\) calculé depuis le \(\rho_n\) réel ;
- convention scalaire additive déclarée ;
- aucun \(K_n\) cible indépendant.

Obligatoire :

```text
AUTONOMOUS_K_FLOW_REQUIRED = NO
```

Aucune application autonome \(K_{n+1} \rightarrow K_n\) n'est requise.

La loi primaire reste :

$$
\rho_{n+1} \rightarrow \rho_n \rightarrow K_n.
$$

---

## 8. T5F5 — Complétude du support

Critère : `T5F5_MODULAR_SUPPORT_COMPLETENESS`.

La décomposition complète du support de \(K_n\)
(`COMPLETE_REPRESENTATION_OF_K_n`, cf. §2) doit rester admissible.

Si la réduction engendre des termes à 3 corps, 4 corps, ..., N corps, ils
sont conservés comme données effectives génuinement dérivées de l'état.

Obligatoire :

```text
PAIR_EDGE_CLOSURE_REQUIRED_AT_ALL_SCALES = NO
PAIR_TRUNCATION_IS_FUNDAMENTAL_DATUM     = NO
```

Une projection de poids ≤ 2 ne peut apparaître que comme une approximation
explicitement déclarée, avec un contrôle d'erreur préenregistré
indépendamment. Elle ne doit jamais redéfinir le flux exact.

---

## 9. T5F6 — Covariance de repère

Critère : `T5F6_LOCAL_FRAME_COVARIANCE`.

Au niveau fin, avant décimation, un unitaire local se factorise selon les
facteurs survivants et éliminés :

$$
U_{\mathrm{fine}} = U_{\mathrm{surviving}} \otimes U_{\mathrm{eliminated}}.
$$

Alors :

$$
\mathrm{Tr}_{I}\big[U_{\mathrm{fine}}\,\rho\,U_{\mathrm{fine}}^{\dagger}\big]
=
U_{\mathrm{surviving}}\,\mathrm{Tr}_{I}[\rho]\,U_{\mathrm{surviving}}^{\dagger}.
$$

Les unitaires locaux agissant uniquement sur les facteurs tracés
s'annulent sous la trace partielle.

À chaque échelle \(n\), on définit :

$$
U_n = \bigotimes_i U_i^{(n)},
$$

produit tensoriel de changements de base locaux sur les facteurs
survivants à l'échelle \(n\). Requis :

$$
\rho_n' = U_n \rho_n U_n^{\dagger}, \qquad K_n' = U_n K_n U_n^{\dagger}.
$$

Chaque bloc de support dérivé de \(K_n\) doit se transformer selon sa
représentation tensorielle sous \(U_n\).

Un objet de boucle fermée \(Q_{\mathrm{loop}}\) (holonomie, action
projective, ou diagnostic directionnel analogue) se transforme par
conjugaison au point de base :

$$
Q_{\mathrm{loop}}' = R_{\mathrm{base}}\, Q_{\mathrm{loop}}\, R_{\mathrm{base}}^{\mathsf T}.
$$

Il est donc :

```text
LOOP_OBJECT = GAUGE_COVARIANT_LOOP_OBJECT
```

et non une matrice invariante de jauge. Sont invariants de jauge :

- ses données de classe de conjugaison ;
- un diagnostic scalaire explicitement déclaré invariant par conjugaison ;
- le verdict de platitude projective (T5F7, §10) ;
- toute comparaison explicitement démontrée invariante sous conjugaison au
  point de base (T5F8, §11).

```text
FLATNESS_VERDICT = GAUGE_INVARIANT
```

`PASS` requiert une vérification explicite de la covariance (annulation
des unitaires purement éliminés sous trace partielle, transformation
\(U_n\) de \(\rho_n\)/\(K_n\), transformation par conjugaison au point de
base de tout objet de boucle) pour la construction de qualification
déclarée. Aucune revendication de symétrie physique au-delà de cette
covariance de repère local n'est faite.

---

## 10. T5F7 — Préservation de la platitude

Critère : `T5F7_FLATNESS_PRESERVATION`.

Porte candidate nécessaire :

```text
FINE_PROJECTIVELY_FLAT -> COARSE_PROJECTIVELY_FLAT
```

à chaque niveau de réduction défini.

L'objet de boucle fermée lui-même est `GAUGE_COVARIANT`, pas invariant
(T5F6, §9). Utiliser exclusivement un verdict de platitude dérivé de cet
objet gauge-covariant par une donnée invariante par conjugaison au point
de base (classe de conjugaison, ou diagnostic scalaire explicitement
déclaré invariant) :

```text
FLATNESS_VERDICT = GAUGE_INVARIANT
```

Le `skew(J_ij)` brut d'une paire isolée n'est pas un verdict de platitude
admissible.

Aucune réciproque requise :

```text
FLAT_COARSE_IMPLIES_FLAT_FINE = NOT_REQUIRED
```

`FAIL` si la réduction canonique fabrique une direction de boucle
projective non triviale à partir d'un état déclaré de jauge pure.

---

## 11. T5F8 — Variation non triviale dérivée de l'état

Critère : `T5F8_NONTRIVIAL_STATE_DERIVED_RUNNING`.

`PASS` requiert au moins une fixture non triviale déclarée pour laquelle :

- la même loi grossière d'état est utilisée ;
- la même loi d'extraction est utilisée ;
- aucune géométrie grossière cible n'est fournie ;
- un diagnostic structurel relationnel change entre au moins deux niveaux
  finis, cette comparaison utilisant exclusivement des données invariantes
  de jauge (classe de conjugaison, diagnostic scalaire explicitement
  déclaré invariant) ou un alignement de covariance explicitement déclaré
  (même conjugaison de base appliquée aux deux niveaux comparés) :

```text
RUNNING_COMPARISON = MUST_USE_GAUGE_INVARIANT_DATA
                      OR_EXPLICIT_COVARIANT_ALIGNMENT
```

L'égalité exacte à échelle finie n'est pas requise. La variation doit être
observée à force relationnelle finie non nulle. Un accord obtenu
uniquement lorsque tout le contenu d'interaction tend vers zéro ne compte
pas comme limite T5-flow non triviale.

Obligatoire :

```text
WEAK_COUPLING_ZERO_RELATION_LIMIT != CONTINUUM_LIMIT
```

---

## 12. T5F9 — Absence de loi post-hoc

Critère : `T5F9_NO_POST_HOC_EXTRACTION`.

Avant tout gel d'exécution confirmatoire :

- famille d'états ;
- graphe/incidence ;
- séquence de décimation des sites ;
- loi d'extraction modulaire ;
- diagnostic de boucle ;
- normes ;
- conventions de normalisation ;
- seuils PASS/FAIL lorsqu'un seuil est inévitable.

Obligatoire :

```text
EXTRACTION_LAW_DECLARED_BEFORE_MEASUREMENT = REQUIRED
NO_POST_HOC_LAW_ADJUSTMENT                 = REQUIRED
NO_TARGET_GEOMETRY_FITTING                 = REQUIRED
```

`FAIL` si une loi est modifiée pour annuler un résidu déjà observé.

---

## 13. T5F10 — Domaine / fermeture sur échec

Critère : `T5F10_DOMAIN_AND_FAIL_CLOSED`.

Le logarithme modulaire fini requiert \(\rho_n > 0\) à chaque niveau où
\(K_n\) est utilisé.

Si un bloc directionnel requiert une direction inverse/polaire :

- objet singulier => `UNDEFINED` / `FAIL_CLOSED` ;
- aucune pseudo-inverse arbitraire ;
- aucune réparation epsilon ;
- aucune orientation cachée dépendante d'une tolérance.

Le conditionnement numérique doit être rapporté séparément de l'existence
mathématique.

---

## 14. T5F11 — Exigence multi-étapes

Critère : `T5F11_MULTISTEP_FLOW`.

Une qualification T5-FLOW ne peut pas utiliser uniquement un passage
fin → grossier unique. Requis au minimum :

$$
\rho_2 \rightarrow \rho_1 \rightarrow \rho_0
$$

plus un contrôle direct :

$$
\rho_2 \rightarrow \rho_0.
$$

`PASS` requiert :

```text
STATE_FLOW_PATH_INDEPENDENCE            = PASS
MODULAR_STATE_DERIVED_PATH_INDEPENDENCE = PASS
```

Ceci établit une loi inter-échelles, pas un continuum.

---

## 15. Oracles courants de la famille de Gibbs

Ces oracles sont propres à la route courante. Ce ne sont pas des axiomes
T5 universels.

Oracles négatifs obligatoires de la route Gibbs courante :

```text
GIBBS_NEGATIVE_ORACLE_1:
TREE_DIRECTIONAL_RUNNING = ABSENT_FOR_DECLARED_GIBBS_TREE_FAMILY

GIBBS_NEGATIVE_ORACLE_2:
PURE_GAUGE_MULTISCALE_FLATNESS = REQUIRED
```

Le résultat sur cycle n'est pas un oracle négatif. Il est classé
séparément comme candidat contextuel :

```text
GIBBS_CONTEXTUAL_CANDIDATE_1:
CYCLE_CONTEXT_CAN_SUPPORT_DIRECTIONAL_RUNNING = YES_CANDIDATE
```

`GIBBS_CONTEXTUAL_CANDIDATE_1` n'est pas une porte négative obligatoire
indépendante. La variation non triviale dérivée de l'état requise pour
T5-FLOW reste couverte par `T5F8` (§11).

Pare-feu obligatoire :

```text
CYCLE_CONTEXT_REQUIRED_IN_DECLARED_FIXTURES != CYCLE_IS_CURVATURE
```

et :

```text
CYCLE_CONTEXT != CYCLE_SUFFICIENT_FOR_RUNNING.
```

Ces oracles ne sont pas élevés au rang de physique universelle.

---

## 16. Pare-feu de non-classicalité

```text
NONCLASSICALITY_NECESSITY = NOT_ESTABLISHED
```

Un état classiquement corrélé séparable peut posséder une structure
d'interaction modulaire non nulle. Par conséquent :

```text
MODULAR_INTERACTION != QUANTUM_GEOMETRY
CORRELATION        != QUANTUM_GEOMETRY
```

Ceci ne bloque pas la qualification mathématique T5-FLOW. Cependant, avant
toute revendication de :

```text
PHYSICAL_QUANTUM_GEOMETRY
```

le programme doit soit :

A. fournir un discriminant de non-classicalité déclaré ;

soit :

B. établir explicitement que la construction est intentionnellement
insensible à la non-classicalité, et réviser la revendication physique en
conséquence.

Obligatoire :

```text
NONCLASSICALITY_FIREWALL = REQUIRED_BEFORE_PHYSICAL_GEOMETRY_CLAIM
```

---

## 17. Relation à G1–G8

```text
T5-FLOW does NOT inherit a full G1-G8 PASS.
```

Au minimum, sont préservées :

- **G1** : dérivation depuis l'état / absence de géométrie cible ;
- **G2** : pare-feu de repère local ;
- **G7** : aucune entrée métrique/distance/aire pré-géométrique.

Si une holonomie/réponse directionnelle projective est utilisée
inter-échelles :

```text
G3/G4 MUST BE REESTABLISHED for that cross-scale construction.
```

`G8` reste `OPEN`.

Aucun diagnostic T5-FLOW ne peut être appelé courbure de Riemann, déviation
géodésique, accélération de marée ou gravité.

---

## 18. Logique du PASS T5-FLOW

Statut futur :

```text
T5_FLOW_QUALIFICATION = PASS | FAIL | NOT_EXECUTED
```

`PASS` ne peut être retourné que si toutes les portes générales passent :

```text
T5F1
T5F2
T5F3
T5F4
T5F5
T5F6
T5F7
T5F8
T5F9
T5F10
T5F11
```

Pour la route Gibbs courante, `GIBBS_NEGATIVE_ORACLE_1` et
`GIBBS_NEGATIVE_ORACLE_2` (§15) doivent également passer.
`GIBBS_CONTEXTUAL_CANDIDATE_1` n'est pas une porte négative obligatoire ;
la variation non triviale dérivée de l'état qu'il peut soutenir reste
couverte par `T5F8`.

La non-classicalité peut rester `OPEN` pour la qualification mathématique
T5-FLOW. Mais tant qu'elle est `OPEN` :

```text
PHYSICAL_QUANTUM_GEOMETRY_CLAIM = FORBIDDEN.
```

---

## 19. Ce que le PASS T5-FLOW n'établit pas

Obligatoire :

```text
T5_FLOW_PASS != T5_PASS
T5_FLOW_PASS != T4_PASS
T5_FLOW_PASS != CONTINUUM
T5_FLOW_PASS != LOCAL_GEOMETRIC_GENERATOR
T5_FLOW_PASS != METRIC_RECONSTRUCTION
T5_FLOW_PASS != RIEMANN_CURVATURE
T5_FLOW_PASS != GRAVITY
T5_FLOW_PASS != DIMENSIONAL_CALIBRATION
```

Restent `OPEN` après T5-FLOW :

- notion intrinsèque de limite locale/de raffinement ;
- limite non triviale infinie/emboîtée ;
- générateur local/continuum éventuel ;
- géométrie continue effective ;
- requalification G3/G4 lorsque nécessaire ;
- correspondance continuum G8 ;
- non-classicalité avant toute revendication de géométrie quantique
  physique.

---

## 20. Pare-feu confirmatoire

Ce document est un contrat de critères uniquement, désormais gelé.

Obligatoire :

```text
T5_FLOW_CONFIRMATORY_EXECUTION = NOT_AUTHORIZED
T5_FLOW_TOY_DESIGN              = NOT_AUTHORIZED
T5_FLOW_VALIDATION_PLAN         = NOT_CREATED
```

La séquence de gel est complète :

1. revue des critères par ChatGPT — `PASS` ;
2. acceptation par Lionel ORCIL — accordée ;
3. gel documentaire — effectué par ce lot.

Restent à venir, sur mandat séparé :

4. conception du mécanisme minimal de qualification ;
5. plan de validation gelé avant exécution confirmatoire.

Aucun résultat de qualification ne peut être importé des audits de
faisabilité exploratoires précédents. Ces audits ont motivé les critères
mais ne comptent pas comme preuve confirmatoire ; le gel du présent
document ne les requalifie pas.

---

## Statut suivant

```text
T5_FLOW_CRITERIA_DOCUMENT      = docs/model/t5-modular-cross-scale-flow-criteria.md
T5_FLOW_CRITERIA_STATUS        = FROZEN
T5_FLOW_CRITERIA_FREEZE        = FROZEN
T5_FLOW_CRITERIA_FINAL_REVIEW  = PASS
SCIENTIFIC_CONTENT_HEAD        = 7d923bcfeb4cb2e9345a79ed9aec6f6433f08f01
T5_FLOW_CONFIRMATORY_EXECUTION = NOT_AUTHORIZED
T5_FLOW_QUALIFICATION          = NOT_EXECUTED

NEXT_TOY         = NOT_AUTHORIZED
OPUS_ESCALATION  = NOT_REQUIRED
```

Ce document ne modifie pas `docs/model/hypothesis.md`, ne modifie pas
`docs/model/tidal-relational-curvature-criteria.md`, ne modifie pas
`docs/model/t5-relational-refinement-boundary.md`, ne définit aucun
`T5-FLOW PASS`, ne définit aucun `T5 PASS`, et n'autorise la conception
d'aucun nouveau toy.
