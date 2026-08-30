# T5a — Critères candidats de limite cross-scale contrôlée

Statut : **gelé**

```text
STATUS = FROZEN_T5A_CONTROLLED_CROSS_SCALE_LIMIT_CRITERIA

NOT_FROZEN       = FALSE

CHATGPT_T5A_TARGETED_CORRECTION_REVIEW  = PASS
CHATGPT_DRAFT_FINAL_REVIEW              = PASS
CHATGPT_T5A_CRITERIA_DRAFT_FINAL_REVIEW = PASS

T5A_CRITERIA_FREEZE              = FROZEN
LIONEL_ORCIL_T5A_FREEZE_APPROVAL = GRANTED
SCIENTIFIC_CONTENT_HEAD          = 7eb2622d9b9ef7ac9bd57751016f09e840e00acf

FROZEN_DOCUMENT_MODIFICATION = NEW_EXPLICIT_DECISION_REQUIRED_FOR_SEMANTIC_CHANGE

T5_FLOW_QUALIFICATION = PASS

T5A_CRITERIA_BOUNDARY = SUFFICIENTLY_CHARACTERIZED_FOR_DOCUMENTARY_DRAFT
T5A_PASS               = NOT_ESTABLISHED
T5_PASS                = NOT_ESTABLISHED

NEXT_TOY   = NOT_AUTHORIZED
NEXT_MODEL = NOT_AUTHORIZED
```

Obligatoire :

```text
DOCUMENT_FREEZE != T5A_PASS
DOCUMENT_FREEZE != T5_PASS

T5A_CRITERIA_FROZEN != T5A_EXECUTED
T5A_CRITERIA_FROZEN != T5A_PASS

T5A_CRITERIA_FROZEN != CONTINUUM
T5A_CRITERIA_FROZEN != LOCALITY
T5A_CRITERIA_FROZEN != GEOMETRY
T5A_CRITERIA_FROZEN != CURVATURE
T5A_CRITERIA_FROZEN != GRAVITY

T5A_PASS != T5_PASS
T5A_PASS != T5B_PASS

T5A_PASS != CONTINUUM
T5A_PASS != LOCALITY
T5A_PASS != GEOMETRY
T5A_PASS != CURVATURE
T5A_PASS != GRAVITY

T5A_PASS != PHYSICAL_SCALE
T5A_PASS != LOCAL_GENERATOR
T5A_PASS != AUTONOMOUS_REDUCED_FLOW
```

Le gel documentaire valide ce document comme référence `FROZEN` des
critères candidats `T5a` ; il ne valide pas leur exécution sur un
candidat concret et ne transforme aucun résultat en continuum,
localité, géométrie, courbure ni gravité.

---

## 0. Origine et portée

Ce document intègre, sans arbitrage scientifique autonome, une décision
déjà rendue à partir de quatre sources :

```text
SOURCE_1 = docs/model/t5-full-pass-boundary-feasibility.md (FROZEN)
SOURCE_2 = T5A-CONTROLLED-CROSS-SCALE-LIMIT-CRITERIA-DESIGN-1
SOURCE_3 = T5A-CRITERIA-TARGETED-CORRECTION-1
SOURCE_4 = arbitrage scientifique final ChatGPT
```

Il ne modifie pas `docs/model/t5-full-pass-boundary-feasibility.md`
(gelé, `SCIENTIFIC_CONTENT_HEAD = 1b81a2c991ca3ca4d1981aab6dbedfa21344c5fc`,
`FREEZE_HEAD = b6fc1ca239a54c41b8005287e4d062ba36d308bb`), et ne modifie
aucun autre document scientifique existant.

Les critères présentés ici sont `PROPOSED` / `NOT_FROZEN`. Ce document
ne déclare aucun `T5A_PASS`, aucun `T5_PASS`, n'autorise aucun nouveau
toy ni aucun nouveau modèle, et n'effectue aucune nouvelle analyse
scientifique autonome : il transcrit une décision déjà arbitrée.

---

## 1. Définition de `T5a`

```text
T5A = CONTROLLED_LIMIT_OF_STATE_DERIVED_CROSS_SCALE_FLOW
```

`T5A_PASS` signifie uniquement : existence et contrôle d'une limite non
triviale d'un objet cross-scale explicitement déclaré, pour une famille
de raffinement déclarée, sous une loi générative et une architecture de
comparaison pré-déclarées, dans un espace et une notion de convergence
déclarés, avec une classe de preuve suffisante et des faux positifs/nulls
explicitement exclus.

La revendication est relative au schéma de raffinement déclaré.

Obligatoire :

```text
T5A_PASS != T5_PASS
T5A_PASS != T5B_PASS
T5A_PASS != CONTINUUM
T5A_PASS != LOCALITY
T5A_PASS != GEOMETRY
T5A_PASS != CURVATURE
T5A_PASS != GRAVITY

T5A_PASS != PHYSICAL_SCALE
T5A_PASS != LOCAL_GENERATOR
T5A_PASS != AUTONOMOUS_REDUCED_FLOW
```

---

## 2. `T5A1` — Indice de raffinement et direction de limite déclarés

```text
T5A1   = DECLARED_REFINEMENT_INDEX_AND_LIMIT_DIRECTION
SOURCE = T5C1
```

`PASS_REQUIRES` :

```text
* Lambda nonempty ;
* preorder déclaré ;
* direction finer/coarser déclarée ;
* famille déclarée dirigée dans la direction pertinente ;
* direction de limite explicitement déclarée ;
* aucun élément maximal dans cette direction ;
* structure suffisamment non bornée pour donner un sens asymptotique
  non terminal.
```

Ne PAS imposer :

```text
* ordre total ;
* indexation par N ;
* dénombrabilité ;
* coordonnée numérique r ;
* poset dirigé global sur tous les graphes.
```

Pare-feu :

```text
lambda != LENGTH
lambda != DISTANCE
lambda != AREA
lambda != TIME
lambda != ENERGY
lambda != INVERSE_TEMPERATURE
```

```text
T5F3_ESTABLISHES        = FINITE_DECLARED_REDUCTION_COMPOSITION
T5F3_DOES_NOT_ESTABLISH = EXISTENCE_OF_AN_INFINITE_PROJECTIVE_STATE_FAMILY

PROJECTIVE_STATE_FAMILY = OPTIONAL_ROUTE_FOR_T5A

LIMIT_DIRECTION = DECLARED_NOT_IMPOSED
```

---

## 3. `T5A2` — Architecture de comparaison cross-level

```text
T5A2   = CROSS_LEVEL_COMPARISON_ARCHITECTURE
SOURCE = T5C3 + T5C11
```

Le critère doit accepter **deux** architectures.

### Route A — `COMMON_TARGET_ROUTE`

Pour chaque niveau :

$$
I_\lambda : X_\lambda \to X_*
$$

avec `X_*` espace de comparaison commun déclaré.

`PASS_REQUIRES` :

```text
* I_lambda pré-déclaré ;
* dérivé de la structure de famille/refinement/extraction déclarée ;
* indépendant des valeurs observées de D ;
* objets correctement typés ;
* si l'objet est gauge-covariant :
  equivariance/frame handling declared ;
* si l'objet est gauge-invariant :
  aucune exigence d'alignement covariant artificielle.
```

La convergence porte sur :

$$
I_\lambda(D_\lambda) \to D_\infty \ \text{in}\ X_*
$$

Aucune composition \(C_{\nu\leftarrow\mu}\circ C_{\mu\leftarrow\lambda}\)
n'est exigée dans cette route.

### Route B — `TRANSITION_MAP_ROUTE`

$$
C_{\mu\leftarrow\lambda} : X_\lambda \to X_\mu
$$

`PASS_REQUIRES` :

```text
* C pré-déclaré ;

* indépendant des valeurs observées ;

* identity on equal levels ;

* EITHER exact composition

      C_{nu<-mu} o C_{mu<-lambda}
          =
      C_{nu<-lambda}

  OR derived bound on the ACCUMULATED coherence defect
  tending to zero ;

* basepoint/label compatibility when applicable ;

* local-frame equivariance when the compared object carries a
  nontrivial local-frame action.
```

`FAIL_IF` :

```text
* comparison law defined from observed D values ;
* hidden retuning ;
* pairwise residual claimed sufficient without accumulated control ;
* implicit object identification.
```

---

## 4. `T5A3` — Famille générative contrôlée

```text
T5A3   = CONTROLLED_GENERATIVE_FAMILY
SOURCE = T5C4
```

Utiliser :

$$
S_\lambda = G(\text{seed}, \lambda)
$$

où `G` désigne un **unique predeclared generative scheme**.

Ne PAS interpréter « single rule » comme interdisant une dépendance
structurelle explicite à `lambda`.

`CORE PASS_REQUIRES` :

```text
E1
one predeclared generative scheme ;

E2
zero independent discretionary per-level free parameters ;

E3
declared inheritance/evolution rule for every
level-dependent quantity ;

E5
level-independent extraction and selection conventions,
sauf dépendance structurelle explicitement déclarée ;

E6
declared admissible normalization class ;
no post-hoc normalization selection.
```

Conditionnel :

```text
E4*
HELD_OUT_LEVEL_PREDICTIVITY

ACTIVATED iff any rule/parameter/form/window/threshold/etc
was selected, fitted or calibrated from observed finite levels,
or if absence of such selection cannot be established.

When activated:
a genuinely unused level must be predicted before evaluation.

NOT REQUIRED:
for a fully analytic, exact, completely predeclared G with no
learned/calibrated element.
```

```text
E7*
DETERMINISTIC_REGENERATION_CONTROL

activated only when numerics is used.
```

---

## 5. `T5A4` — Classe d'objet limite, espace et convergence déclarés

```text
T5A4   = DECLARED_LIMIT_OBJECT_CLASS_SPACE_AND_CONVERGENCE
SOURCE = T5C6
```

Classes primaires :

```text
L1 FULL_MODULAR_DATUM_LIMIT
L2 STATE_OBSERVABLE_LIMIT
L3 DERIVED_OPERATOR_LIMIT
L4 GAUGE_COVARIANT_OBJECT_LIMIT
L5 GAUGE_INVARIANT_DIAGNOSTIC_LIMIT
```

Exigence :

```text
PRIMARY_CLAIM_CLASS = EXACTLY_ONE_DECLARED_CLASS
```

`PASS` est accordé uniquement à la classe primaire déclarée.

Espace :

```text
* declared X ;
* declared topology/tau ;
* Hausdorff OR explicit equivalence/quotient convention ;
* completeness declared when a Cauchy argument relies on it ;
* convergence notion explicitly declared.
```

Route de l'espace limite et définissabilité de la classe triviale `T`
(voir aussi `T5A6`) :

```text
LIMIT_SPACE_ROUTE = HAUSDORFF_SPACE
    -> T est définie comme classe triviale dans X.

LIMIT_SPACE_ROUTE = EQUIVALENCE_OR_QUOTIENT
    -> T doit être :
       - soit définie directement comme sous-ensemble/classe du
         quotient ;
       - soit saturée relativement à la relation d'équivalence
         déclarée.
```

```text
TRIVIAL_CLASS_WELL_DEFINEDNESS =
    if quotient/equivalence is used,
    triviality must be representative-independent.
```

La convergence set-valued / omega-limit peut être utilisée lorsque
explicitement revendiquée.

Des résultats dérivés plus faibles peuvent être rapportés **ssi** :

```text
* the deriving map is proved limit-preserving for the declared
  topology/domain ;
* the result inherits the evidence class ;
* it is labelled DERIVED.
```

```text
DERIVED_RESULT_CONVERGENCE    = MAY_BE_INHERITED_WITH_LIMIT_PRESERVING_MAP
DERIVED_RESULT_EVIDENCE_CLASS = MAY_BE_INHERITED
DERIVED_RESULT_NONTRIVIALITY  = NOT_AUTOMATICALLY_INHERITED
```

Pour déclarer un résultat dérivé non trivial, exiger l'une des deux
conditions suivantes :

```text
EITHER
    une classe triviale T_derived propre à la classe dérivée, avec
    la séparation T5A6 correspondante ;

OR
    une preuve explicite que l'application dérivante préserve la
    non-trivialité relativement aux classes triviales déclarées.
```

```text
PRIMARY_CLASS_NONTRIVIALITY => DERIVED_CLASS_NONTRIVIALITY
```

sans l'une de ces deux preuves est interdit.

```text
CLASS_PROMOTION_WITHOUT_REQUALIFICATION = FORBIDDEN

SCALAR_CONVERGENCE => FULL_STRUCTURE_CONVERGENCE = FORBIDDEN
```

---

## 6. `T5A5` — Classe de preuve d'établissement de la limite

```text
T5A5   = LIMIT_ESTABLISHMENT_EVIDENCE_CLASS
SOURCE = T5C6 + T5C7
```

Un `T5a PASS` requiert l'une des classes suivantes :

```text
EVIDENCE_CLASS_A = ANALYTIC_LIMIT_PROOF
```

```text
EVIDENCE_CLASS_B = DERIVED_TAIL_BOUND
```

avec une borne du type :

$$
\lVert D_\lambda - D_\infty \rVert \le \epsilon(\lambda), \qquad
\epsilon(\lambda) \to 0
$$

où `epsilon` est **dérivé** de la règle déclarée, jamais ajusté sur la
queue observée.

```text
EVIDENCE_CLASS_B_PRIME = DERIVED_EXISTENCE_WITHOUT_KNOWN_LIMIT
```

exemples :

```text
* contraction theorem ;
* monotone + bounded theorem ;
* Cauchy argument in a declared complete space ;
* other mathematically equivalent derived argument.
```

Numérique :

```text
PREREGISTERED_NUMERICAL_CORROBORATION = ALLOWED

PURE_FINITE_NUMERICAL_REGRESSION => T5A_PASS = FORBIDDEN

FIT_QUALITY != LIMIT_PROOF
SMALL_SUCCESSIVE_DIFFERENCE != CONVERGENCE
LAST_TWO_LEVELS_AGREE != LIMIT
```

Rôle du numérique dans le dossier de qualification (voir aussi
`T5A8`, `P_NUM`) :

```text
NUMERICAL_ROLE = NONE | CORROBORATIVE | SUPPORTING_SUBCLAIM
```

Quel que soit `NUMERICAL_ROLE`, la preuve de l'existence de la limite
reste obligatoirement de classe `EVIDENCE_CLASS = A | B | B'` : le
numérique ne peut seul établir la queue infinie. Il peut réfuter ou
corroborer A/B/B', ou vérifier des constantes/hypothèses utilisées par
une borne dérivée, qu'il soit purement corroboratif ou porteur d'un
sous-claim nécessaire à A/B/B'. Une preuve purement analytique sans
donnée numérique porte `NUMERICAL_ROLE = NONE`.

---

## 7. `T5A6` — Non-trivialité et séparation des nulls

```text
T5A6   = NONTRIVIALITY_AND_NULL_SEPARATION
SOURCE = T5C7
```

Déclarer une classe triviale `T`, appropriée à `PRIMARY_CLAIM_CLASS`.

`T` doit contenir, selon le cas :

```text
* zero-relation / decoupled limit class ;
* product/trivial relation class ;
* values structurally forced independently of the state ;
* values produced by declared null families.
```

**Exigence centrale** :

`D_infinity` doit être séparé de `T`.

Formulation topologique générique :

$$
D_\infty \notin \overline{T}
$$

ou une autre séparation topologique explicitement déclarée équivalente.

Ne PAS exiger universellement une distance/marge numérique.

Uniquement si `X` possède une métrique/norme déclarée appropriée à la
revendication, on peut utiliser :

$$
\mathrm{dist}(D_\infty, T) > \delta, \qquad \delta > 0
$$

établie au niveau de la classe de preuve déclarée.

Important :

```text
MICROSCOPIC_PARAMETER -> 0
```

n'implique PAS :

```text
D_infinity IN T
```

Un paramètre microscopique qui s'annule n'est pas en lui-même un
`FAIL`.

Si une compensation/rescaling/croissance du nombre de pas est
impliquée, son mécanisme doit faire partie de `G` ou de la structure de
normalisation préenregistrée, jamais introduit a posteriori.

```text
NT3 :
a structurally forced null must land in T, the live family must not.

NT4 :
finite-size plateau / numerical-floor exclusion is activated only
when numerics is used.
```

Lorsque `LIMIT_SPACE_ROUTE = EQUIVALENCE_OR_QUOTIENT` (`T5A4`) :

```text
TRIVIAL_CLASS_SATURATION_REQUIRED_UNDER_DECLARED_EQUIVALENCE = TRUE

NONTRIVIALITY_SEPARATION_SPACE = DECLARED_QUOTIENT_SPACE
```

Interdit :

```text
REPRESENTATIVE_DEPENDENT_T5A6_VERDICT = TRUE
```

Retiré du noyau universel :

```text
RELATIONAL_STRENGTH_BOUNDED_AWAY_FROM_ZERO

classification : OPTIONAL_ROUTE_SPECIFIC_SUFFICIENT_CONTROL
```

---

## 8. `T5A7` — Invariance du verdict sous indexation/normalisation

```text
T5A7   = INDEXING_AND_NORMALIZATION_INVARIANCE_OF_THE_VERDICT
SOURCE = T5C8
```

Le test de réindexation concerne un **pur isomorphisme de
relabellisation**.

Il doit préserver :

```text
* the order/filter structure ;
* assignment of physical/structural systems to abstract levels ;
* declared structural quantities.
```

Il ne doit PAS changer une quantité structurelle significative au seul
motif que cette quantité était encodée numériquement dans l'indice.

Ainsi :

```text
ABSTRACT_LABEL_RENAMING       = VERDICT_INVARIANT
STRUCTURAL_CARDINALITY_CHANGE = NOT_A_RELABELING_TEST
```

Exiger en plus :

```text
* no verdict dependence on arbitrary label names ;
* verdict invariant in the declared admissible normalization class ;
* if an estimator is used, estimator stability under appropriate
  cofinal selections within declared uncertainty.
```

Sous `EVIDENCE_CLASS_A` : l'invariance sous sous-réseau cofinal de la
limite mathématique effective est un théorème et doit être rapportée
comme `VACUOUS/INHERITED`, pas comme preuve indépendante.

La reparamétrisation de coordonnée/échelle appartient à `T5A-C1`.

---

## 9. `T5A8` — Préenregistrement cross-scale et fail-closed

```text
T5A8   = CROSS_SCALE_PREREGISTRATION_AND_FAIL_CLOSED
SOURCE = T5C1, T5C3, T5C4, T5C6, T5C7, T5C8
```

`P_CORE` — universel : geler avant qualification :

```text
1. refinement family/index ;
2. limit direction/unboundedness ;
3. generative scheme G/seed/inheritance ;
4. comparison architecture and route ;
5. primary claim object/class ;
6. limit space/topology/separation/completeness if applicable ;
7. convergence notion ;
8. evidence class A/B/B' and whether numerics is used ;
9. trivial/null class and null families ;
10. activated conditional routes ;
11. domain/fail-closed rules.
```

`P_NUM` — préenregistrement numérique conditionnel (voir aussi
`T5A5`, `NUMERICAL_ROLE`) :

```text
P_NUM s'active dès que des résultats numériques font partie du
dossier de qualification, qu'ils soient :

* NUMERICAL_ROLE = CORROBORATIVE ;
* ou NUMERICAL_ROLE = SUPPORTING_SUBCLAIM (porteurs d'un sous-claim
  nécessaire à EVIDENCE_CLASS A/B/B').
```

Seuls les champs applicables doivent être exigés :

```text
* computed finite level set ;
* precision/uncertainty protocol ;
* FIT_WINDOW  = REQUIRED_IF_FIT_USED ;
* SIGNAL_FLOOR = REQUIRED_IF_SIGNAL_FLOOR_APPLICABLE ;
* D_MIN        = REQUIRED_IF_FINITE_NUMERICAL_INFERENCE_USED ;
* asymptotic law/parameter count/window if fitted ;
* level rejection rules ;
* numerical tolerances/thresholds.
```

```text
NUMERICAL_ROLE = NONE => aucun P_NUM artificiel.
```

Une preuve purement analytique sans donnée numérique porte
`NUMERICAL_ROLE = NONE` et ne doit avoir aucun `P_NUM` artificiel.

Fail-closed en cas d'ambiguïté sur le rôle du numérique.

Une preuve analytique NE DOIT PAS échouer parce qu'un paramètre
numérique non applicable est absent.

Aucun changement a posteriori ne peut convertir `FAIL`/`UNRESOLVED` en
`PASS`.

---

## 10. Critères conditionnels

### `T5A-C1` — Non-dégénérescence de la coordonnée de raffinement et classe de reparamétrisation

```text
T5A-C1 = REFINEMENT_COORDINATE_NONDEGENERACY_AND_REPARAM_CLASS
```

Activation : revendication de taux/exposant/scaling/dérivée.

Préserver : `r != length/distance/area/time/energy/inverse temperature`.

Une reparamétrisation monotone arbitraire ne préserve pas un exposant
de scaling ; la classe de reparamétrisation admissible doit donc être
explicitement déclarée.

### `T5A-C2` — Type de générateur et mode de convergence d'opérateur

```text
T5A-C2 = GENERATOR_TYPE_AND_OPERATOR_CONVERGENCE_MODE
```

Activation : revendication de générateur.

Exiger : type de générateur, statut de paramétrisation/semi-groupe et
mode de convergence d'opérateur.

```text
FINITE_RUNNING != GENERATOR
```

### `T5A-C3` — Fermeture de paramétrisation réduite

```text
T5A-C3 = REDUCED_PARAMETRIZATION_CLOSURE
```

Activation : flot réduit autonome sur pair/J/Q/chi/etc.

Exiger : preuve indépendante de fermeture/suffisance.

Préserver :

```text
AUTONOMOUS_REDUCED_FLOW_ON_PAIR_OR_LOOP_DATA = NOT_ESTABLISHED
```

### `T5A-C4` — Requalification cross-scale `G3`

```text
T5A-C4 = G3_CROSS_SCALE_REQUALIFICATION
```

Activation : objet directionnel promu porteur de courbure
relationnelle cross-scale.

Exiger : requalification `G3` pour cette construction.

### `T5A-C5` — Déclaration du domaine modulaire limite

```text
T5A-C5 = LIMIT_MODULAR_DOMAIN_DECLARATION
```

Activation : `L1 FULL_MODULAR_DATUM_LIMIT`.

Exiger : domaine modulaire limite déclaré, statut borné/non
borné ou d'affiliation, et notion de convergence appropriée.

Ne pas supposer la convergence en norme de `K` sans bornitude.

### `T5A-C6` — Alignement de l'objet covariant

```text
T5A-C6 = COVARIANT_OBJECT_ALIGNMENT
```

Activation : `L4 GAUGE_COVARIANT_OBJECT_LIMIT`.

Exiger une route déclarée parmi :

```text
* quotient convergence with valid quotient structure ;
  or
* declared cross-level frame alignment/equivariant comparison.
```

Une convergence uniquement invariante ne peut pas qualifier une
revendication `L4`.

---

## 11. Algèbre de qualification

```text
T5A_QUALIFICATION = PASS | FAIL | NOT_EXECUTED

UNDEFINED = PROPERTY_OF_OBJECT_OR_DOMAIN
            NOT_A_QUALIFICATION_VERDICT
```

`PASS` doit porter :

```text
EVIDENCE_CLASS = A | B | B'
```

plus métadonnées de corroboration numérique si applicable.

`FAIL` doit porter un code de raison tiré d'un ensemble déclaré
comprenant au moins :

```text
DOMAIN_INADMISSIBLE
LIMIT_NOT_ESTABLISHED
TRIVIAL_LIMIT
NOT_RESOLVED_ABOVE_FLOOR
NULL_NOT_SEPARATED
FAMILY_NOT_CONTROLLED
COMPARISON_NOT_ADMISSIBLE
PREREGISTRATION_VIOLATION
ROUTE_GATE_MISSING
```

---

## 12. Classes d'oracles négatifs

Ces classes définissent des catégories, pas des fixtures concrètes.
Pour chacune, le faux positif qu'elle doit discriminer est indiqué.

```text
N1 TRIVIAL_ZERO_RELATION
    -> discrimine une limite triviale (relation nulle/découplée)
       confondue avec une limite non triviale contrôlée.

N2 FINITE_SIZE_PLATEAU
    -> discrimine un plateau numérique fini de taille finie confondu
       avec une convergence établie.

N3 INDEX_RELABELING
    -> discrimine un changement de cardinalité structurelle déguisé en
       simple relabellisation d'indice.

N4 NONCONVERGENT_BUT_SMALL_LAST_STEP
    -> discrimine un dernier pas numériquement petit confondu avec la
       convergence de la suite.

N5 NUMERICAL_NOISE_FLOOR
    -> discrimine un plancher de bruit numérique confondu avec un
       résidu résolu au-dessus du plancher.

N6 RETUNED_PER_LEVEL_FAMILY
    -> discrimine une famille réajustée niveau par niveau (paramètres
       discrétionnaires cachés) confondue avec une famille générative
       unique contrôlée.

N7 IDENTITY_BY_CONSTRUCTION
    -> discrimine une identification implicite d'objets par
       construction confondue avec une comparaison cross-level
       explicitement contrôlée.

N8 INVARIANT_ONLY_CONVERGENCE
    -> discrimine une convergence uniquement au niveau des invariants
       confondue avec une convergence de l'objet covariant complet
       (classe L4).

N9 COMPARISON_COLLAPSE
    -> discrimine un effondrement de l'architecture de comparaison
       confondu avec une architecture de comparaison admissible. Ce
       cas recouvre trois situations à distinguer :

       1. comparaison construite à partir des valeurs observées ;
       2. retuning caché ;
       3. architecture qui force le PRIMARY_CLAIM_OBJECT vers une
          valeur indépendante de l'état/relation pertinente, puis
          présente cette convergence forcée comme non triviale.

       Le cas 3 est rejeté conjointement par T5A2 (architecture de
       comparaison) et T5A6 (non-trivialité et séparation des nulls) :
       une valeur forcée indépendamment de l'état appartient à la
       classe triviale déclarée.
```

Clarification sur la dégénérescence de l'application de comparaison :

```text
GLOBAL_COMPARISON_MAP_INJECTIVITY        != REQUIRED
INFORMATION_PRESERVING_FULL_STRUCTURE_MAP != REQUIRED

DECLARED_REDUCTIVE_PROJECTION = ALLOWED

STRUCTURALLY_FORCED_STATE_INDEPENDENT_LIMIT => CLAIMED_AS_NONTRIVIAL = FAIL

L5_DIAGNOSTIC_ROUTE = ADMISSIBLE
```

Une projection volontairement réductrice reste admissible si la
revendication est explicitement bornée à sa `PRIMARY_CLAIM_CLASS`
déclarée (`T5A4`). Cette clarification ne crée aucune nouvelle porte
`T5A` : elle précise la discrimination opérée par `N9` et son
articulation avec `T5A2`/`T5A6`.

---

## 13. Pare-feu faux-positifs

```text
F1  finite running mistaken for controlled limit
        -> T5A5 (evidence class), T5A8 (fail-closed)

F2  refinement index mistaken for physical distance
        -> T5A1 (firewall lambda != LENGTH/DISTANCE/AREA/TIME/ENERGY/
           INVERSE_TEMPERATURE)

F3  vanishing running mistaken for nontrivial fixed point
        -> T5A6 (nontriviality/null separation, MICROSCOPIC_PARAMETER
           -> 0 does not imply D_infinity IN T)

F4  nonzero running mistaken for local generator
        -> T5A-C2 (generator type / FINITE_RUNNING != GENERATOR)

F5  single scalar invariant mistaken for tensorial/geometric
    convergence
        -> T5A4 (PRIMARY_CLAIM_CLASS = EXACTLY_ONE_DECLARED_CLASS,
           SCALAR_CONVERGENCE => FULL_STRUCTURE_CONVERGENCE = FORBIDDEN)

F6  reduced parametrization assumed dynamically closed
        -> T5A-C3 (reduced parametrization closure,
           AUTONOMOUS_REDUCED_FLOW_ON_PAIR_OR_LOOP_DATA =
           NOT_ESTABLISHED)

F7  arbitrary normalization producing fake scaling
        -> T5A3 (E6, declared admissible normalization class), T5A-C1
           (reparametrization class)

F8  tree/cycle distinction mistaken for curvature
        -> T5A-C4 (G3 cross-scale requalification)

F9  local-frame covariance mistaken for spacetime covariance
        -> T5A2 (equivariance/frame handling declared), T5A-C6
           (covariant object alignment)

F10 mathematical controlled limit mistaken for gravity
        -> §14 (T5a/T5b boundary, T5A DOES NOT ESTABLISH gravity)
```

---

## 14. Frontière `T5a` / `T5b`

`T5a` établit uniquement :

```text
* existence of the declared limit ;
* controlled cross-level comparison ;
* nontriviality relative to declared null/trivial class ;
* qualification at the declared object class ;
* scheme-relative result.
```

`T5a` n'établit PAS :

```text
* locality ;
* intrinsic continuum ;
* refinement-scheme universality ;
* G8 ;
* metric ;
* dimension ;
* tensorial geometry ;
* Riemann curvature ;
* tidal response ;
* gravity ;
* nonclassicality ;
* physical length/time/area/energy scale ;
* autonomous reduced flow ;
* local generator.
```

`T5b` reste responsable de la correspondance local/continuum plus
forte.

---

## 15. Statut du toy — faisabilité de conception

```text
T5A_CRITERIA_BOUNDARY = SUFFICIENTLY_CHARACTERIZED_FOR_DOCUMENTARY_DRAFT

NEXT_TOY_SCIENTIFICALLY_DESIGNABLE = PREMATURE
```

Raison : aucune famille indexée par raffinement, non bornée dans une
direction de limite déclarée, munie d'une architecture de comparaison
admissible et d'une route de classe de preuve A/B/B' plausible, n'a
encore été identifiée.

Ne PAS affirmer qu'une tour d'états projective est requise.

```text
UNBLOCKING_CONDITION =
    identify at least one refinement-indexed family, unbounded in a
    declared limit direction, with an admissible comparison
    architecture (COMMON_TARGET_ROUTE or TRANSITION_MAP_ROUTE), for
    which an analytic limit proof or a derived tail/existence argument
    is scientifically plausible.
```

---

## 16. Statut final

```text
T5A_CRITERIA_DOCUMENT = docs/model/t5a-controlled-cross-scale-limit-criteria.md
T5A_CRITERIA_STATUS   = FROZEN_T5A_CONTROLLED_CROSS_SCALE_LIMIT_CRITERIA
T5A_CRITERIA_FREEZE   = FROZEN
NOT_FROZEN            = FALSE

CHATGPT_T5A_TARGETED_CORRECTION_REVIEW  = PASS
CHATGPT_DRAFT_FINAL_REVIEW              = PASS
CHATGPT_T5A_CRITERIA_DRAFT_FINAL_REVIEW = PASS
LIONEL_ORCIL_T5A_FREEZE_APPROVAL        = GRANTED
SCIENTIFIC_CONTENT_HEAD                 = 7eb2622d9b9ef7ac9bd57751016f09e840e00acf

FROZEN_DOCUMENT_MODIFICATION = NEW_EXPLICIT_DECISION_REQUIRED_FOR_SEMANTIC_CHANGE

T5A_PASS = NOT_ESTABLISHED
T5_PASS  = NOT_ESTABLISHED

FUNDAMENTAL_BLOCKING = NONE_DEMONSTRATED

NEXT_MODEL = NOT_AUTHORIZED
NEXT_TOY   = NOT_AUTHORIZED
```

Ce document ne modifie pas `docs/model/hypothesis.md`, ne modifie pas
`docs/model/t5-relational-refinement-boundary.md`, ne modifie pas
`docs/model/t5-modular-cross-scale-flow-criteria.md`, ne modifie pas
`docs/model/tidal-relational-curvature-criteria.md`, ne modifie pas
`docs/model/t5-full-pass-boundary-feasibility.md` (gelé), ne modifie
aucun fichier de `docs/toy-models/**`, `experiments/`, `src/` ni
`tests/`.

Le gel documentaire valide les critères candidats `T5a` tels que
rédigés (`T5A1`–`T5A8`, `T5A-C1`–`T5A-C6`) comme document de référence
`FROZEN` ; il ne déclare aucun `T5A_PASS` ni `T5_PASS`, n'exécute ces
critères sur aucun candidat, et ne rend pas le prochain toy
scientifiquement concevable
(`NEXT_TOY_SCIENTIFICALLY_DESIGNABLE = PREMATURE`, §15). Le prochain
travail scientifique autorisable après ce gel est
`T5A_CANDIDATE_LIMIT_FAMILY_FEASIBILITY`, non `NEW_TOY_DESIGN`, et
requiert un mandat scientifique distinct explicite. Toute modification
ultérieure de sens de ce document exige une nouvelle décision
explicite, conformément à
`docs/governance/documentation-governance.md` §7.
