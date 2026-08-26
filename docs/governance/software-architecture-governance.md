# Gouvernance de l’architecture logicielle

**Statut : gelé**

Ce document définit les règles transverses d’organisation du code du dépôt `cosmotgg`.

Il complète :

```text
docs/governance/collaboration-governance.md
docs/governance/documentation-governance.md
```

Son objectif est de garantir que les modèles jouets successifs construisent progressivement une bibliothèque scientifique et numérique réutilisable, sans transformer chaque modèle en implémentation isolée ni anticiper artificiellement les besoins de modèles futurs.

---

## 1. Principe général

L’architecture distingue deux responsabilités :

```text
core/
    briques physiques, mathématiques et numériques réutilisables

models/modelXX/
    définition, configuration et assemblage propres au modèle XX
```

Un modèle jouet est un **consommateur** des briques disponibles dans `core`.

Le fait qu’une fonction soit développée pour la première fois à l’occasion d’un modèle particulier ne signifie pas qu’elle appartient à ce modèle.

Le critère principal est :

> **Une brique appartient à `core` lorsque sa définition et son comportement peuvent être formulés indépendamment de l’assemblage particulier du modèle qui l’utilise.**

À l’inverse, une construction appartient à `models/modelXX/` lorsqu’elle encode une décision, une configuration, une composition, un protocole ou un oracle propre au modèle concerné.

Le principe architectural du projet est donc :

```math
\boxed{
\text{bibliothèque commune progressive}
+
\text{modèles comme assemblages consommateurs}
}
```

---

## 2. Arborescence de référence

L’organisation cible du code est :

```text
src/
└── cosmotgg/
    ├── core/
    │   └── ...
    │
    └── models/
        ├── model0a/
        │   └── ...
        ├── modelXX/
        │   └── ...
        └── ...
```

Les tests suivent une séparation explicite :

```text
tests/
├── architecture/
│   └── ...
├── core/
│   └── ...
└── models/
    ├── model0a/
    │   └── ...
    └── ...
```

Rôle de ces espaces :

- `tests/architecture/` : invariants structurels et règles transverses du dépôt ;
- `tests/core/` : tests unitaires purs des briques communes ;
- `tests/models/modelXX/` : tests d’intégration et tests d’acceptation scientifique du modèle.

`tests/architecture/` est un espace de contrôle transverse : il peut inspecter ou importer `core` et `models` lorsque cela est nécessaire pour vérifier les invariants du dépôt. Cette capacité ne s’étend pas à `tests/core/`, qui reste strictement model-free.

Les dossiers ne sont créés que lorsqu’un besoin réel apparaît.

Cette arborescence est fonctionnelle : elle n’impose pas à l’avance la liste des modules qui devront exister dans `core`.

---

## 3. Critères d’entrée dans `core`

Une fonction, classe ou module peut être placé dans `core` lorsque sa définition est indépendante de l’assemblage d’un modèle particulier.

Les critères suivants servent de guide :

1. son API peut être formulée sans référence à l’identité d’un modèle particulier ;
2. elle ne code pas en dur des constantes, états nommés, observables ou résultats attendus propres à un modèle ;
3. son comportement possède une signification propre indépendamment du benchmark qui l’utilise ;
4. elle peut être testée unitairement sans reconstruire intégralement un modèle jouet particulier.

Cela peut notamment couvrir :

- mathématiques générales ;
- physique connue ;
- algèbre linéaire ;
- représentation d’espaces d’états ;
- opérateurs génériques ;
- méthodes numériques ;
- procédures générales d’identifiabilité ;
- constructions scientifiques nouvelles répondant aux conditions du §5.

Le caractère réutilisable est déterminé par la **nature actuelle de la brique**, et non par l’hypothèse qu’un modèle futur pourrait éventuellement en avoir besoin.

### 3.1 Principe de placement conservateur

Lorsqu’un composant pourrait raisonnablement appartenir à `core`, mais que son abstraction réutilisable n’est pas encore suffisamment établie, il reste dans le modèle qui l’introduit.

La promotion vers `core` suit ensuite §8 dès qu’un usage supplémentaire, ou une clarification suffisante de son API indépendante du modèle, la justifie.

Le choix par défaut est donc :

```math
\boxed{
\text{ambigu} \rightarrow \text{model-specific}
}
```

Cette règle ne s’applique pas aux briques dont le caractère générique est déjà intrinsèque et non ambigu.

Elle privilégie le choix le plus réversible : une extraction ultérieure vers `core` est acceptable ; une abstraction prématurée dans la bibliothèque commune est évitée.

---

## 4. Contenu propre à `models/modelXX`

Un modèle contient les éléments qui définissent son assemblage particulier.

Cela peut notamment comprendre :

- le nombre de sites ;
- la topologie ou le graphe choisi ;
- l’orientation des liens ;
- les dimensions locales retenues ;
- les conditions aux limites ;
- les charges ou fonds propres au modèle ;
- les paramètres et seuils propres au protocole ;
- les contraintes particulières assemblées à partir de briques génériques ;
- les états physiques nommés ;
- les observables propres au benchmark ;
- les familles de mesure retenues ;
- les états témoins ;
- les protocoles instrumentaux propres au modèle ;
- les assemblages de briques `core` ;
- les résultats analytiques attendus ;
- les oracles d’acceptation scientifique.

Un modèle ne doit pas recopier une fonctionnalité générique existant déjà dans `core`.

---

## 5. Physique connue, physique nouvelle et traçabilité

La localisation logicielle et le statut scientifique sont deux propriétés indépendantes.

Une construction de physique connue peut naturellement appartenir à `core`.

Une construction scientifique nouvelle introduite par le projet peut également appartenir à `core` lorsqu’elle constitue une brique réutilisable indépendante de l’assemblage d’un modèle particulier.

Le placement dans `core` ne constitue jamais une promotion implicite de son statut scientifique.

En particulier :

```text
core != physique établie
réutilisable != validé physiquement
```

### 5.1 Métadonnées scientifiques normalisées

Chaque module public de `core` doit exposer une métadonnée machine-readable :

```python
SCIENTIFIC_METADATA = {
    "status": "...",
    "origin_model": None,
    "normative_reference": None,
}
```

Le champ `status` prend exactement l'une des deux valeurs suivantes :

```text
SCIENTIFIC_METADATA.status ∈ {
    "established",
    "project-defined",
}
```

Cette taxonomie est volontairement minimale et fermée. Aucune autre valeur n'est autorisée ; aucune troisième catégorie n'est créée localement dans le code sans passer par §24.

**`established`**

Construction mathématique, numérique ou physique qui ne constitue pas une proposition scientifique propre au projet CosmoTGG.

```python
SCIENTIFIC_METADATA = {
    "status": "established",
    "origin_model": None,
    "normative_reference": None,
}
```

`origin_model` et `normative_reference` peuvent rester à `None`.

**`project-defined`**

Construction scientifique introduite par CosmoTGG et dont la définition ou le statut doit rester traçable vers une source normative du projet. `origin_model` et `normative_reference` sont alors obligatoires.

```python
SCIENTIFIC_METADATA = {
    "status": "project-defined",
    "origin_model": "modelXX",
    "normative_reference":
        "docs/toy-models/modelXX/specification.md#...",
}
```

Le placement dans `core` reste indépendant du statut scientifique : une brique `project-defined` ne devient pas scientifiquement établie du seul fait de son placement dans `core` (§5).

Inversement, une procédure numérique ou mathématique générale (par exemple : décomposition en valeurs singulières, calcul de rang, de noyau ou de conditionnement) reste `established` même lorsqu'elle est utilisée au service d'un protocole scientifique propre au projet. C'est l'usage protocolaire — porté par le modèle qui assemble et pré-enregistre ses propres seuils et observables — qui peut être `project-defined`, pas la méthode générique elle-même.

Cette métadonnée code porte seulement une classification minimale de provenance scientifique. Elle ne duplique pas le statut scientifique détaillé porté par la documentation normative applicable (spécification, décision, contrat d'implémentation) — voir §15.

### 5.2 Vérification automatique

Un test sous `tests/architecture/` vérifie au minimum :

- la présence de `SCIENTIFIC_METADATA` pour les modules publics de `core` ;
- la validité du champ `status` au regard du vocabulaire fermé défini au §5.1 (`established`, `project-defined`) ;
- la présence de `origin_model` et `normative_reference` lorsque le statut l’exige ;
- l’existence réelle du fichier pointé par `normative_reference` ;
- lorsqu’une ancre de section est présente, l’existence d’un titre correspondant dans le document référencé.

Une référence normative cassée doit faire échouer le contrôle d’architecture au même titre qu’une métadonnée absente.

Une métadonnée déclarative non vérifiée n’est pas considérée comme un mécanisme de gouvernance suffisant.

---

## 6. Dépendances autorisées

La direction des dépendances est un invariant architectural :

```text
models  --->  core
```

Un module de `models/modelXX/` peut utiliser `core`.

Un module de `core` ne doit jamais importer un modèle particulier.

Donc :

```text
core  -X->  models
```

est interdit.

Une brique `core` ne doit pas connaître :

- `model0a` ;
- `model0b` ;
- `modelXX` ;
- les états nommés d’un modèle ;
- les oracles scientifiques d’un modèle ;
- ses résultats attendus ;
- ses seuils ou tolérances protocolaires.

### 6.1 Vérification automatique

Un test sous `tests/architecture/` parcourt les imports des modules de `core` et échoue sur toute dépendance vers `cosmotgg.models`.

Le contrôle doit couvrir au minimum les imports standards Python détectables par AST :

```python
import cosmotgg.models...
from cosmotgg.models... import ...
```

Le même invariant s’applique aux tests unitaires de `core` :

```text
tests/core  -X->  models
```

---

## 7. Généralisation progressive

Le projet ne construit pas à l’avance un framework destiné à des modèles hypothétiques.

Une API `core` doit être aussi générique que sa définition actuelle le permet, mais **pas plus**.

Principe :

> **Généraliser ce qui est déjà intrinsèquement générique ; ne pas anticiper ce qui ne l’est pas encore.**

Si une primitive fermionique est naturellement définie pour un nombre arbitraire de modes, elle ne doit pas être artificiellement limitée aux trois sites du premier modèle qui l’utilise.

En revanche, aucun système générique de graphes, groupes de jauge, représentations, topologies ou protocoles ne doit être conçu uniquement parce qu’un modèle futur pourrait éventuellement en avoir besoin.

L’évolution se fait par besoins concrets :

```text
modèle courant
    ↓
besoin réel
    ↓
brique générique minimale
    ↓
core
    ↓
tests unitaires
```

Un modèle ultérieur peut enrichir ou généraliser une brique existante lorsque son besoin réel rend cette évolution nécessaire.

---

## 8. Promotion d’une brique vers `core`

Lorsqu’une fonctionnalité apparaît initialement dans un modèle et qu’il devient établi que sa définition est indépendante de celui-ci, elle doit être extraite vers `core` plutôt que dupliquée.

Cette extraction doit préserver :

- les tests existants ;
- la traçabilité scientifique ;
- les invariants du modèle qui l’a introduite ;
- les dépendances autorisées ;
- les comportements déjà contractualisés au sens du §17.

La promotion dans `core` n’autorise pas à élargir simultanément son API au-delà du besoin démontré.

Une promotion vers `core` est une opération d’architecture, pas une promotion du statut scientifique de la construction.

---

## 9. Tolérances et seuils numériques

Une tolérance susceptible d’affecter un résultat scientifique ou numérique fait partie du protocole ou du modèle qui l’utilise.

Aucune fonction `core` ne doit définir silencieusement une valeur par défaut pour :

- un seuil de rang ;
- un seuil d’égalité ;
- un seuil de convergence ;
- une coupure spectrale ;
- une tolérance de noyau ;
- une tolérance de conditionnement ;
- ou toute autre valeur pouvant modifier l’interprétation numérique du résultat.

Une fonction `core` doit recevoir ces valeurs explicitement.

Lorsqu’une tolérance est un paramètre scientifique ou numérique de protocole, elle doit être **obligatoire et keyword-only** afin d’éviter qu’un argument positionnel numérique soit confondu silencieusement avec un autre seuil.

Signature conforme :

```python
def analyze_identifiability(matrix, *, rank_tolerance):
    ...
```

Signature interdite :

```python
def analyze_identifiability(matrix, rank_tolerance=1e-12):
    ...
```

Un appel depuis un modèle peut naturellement fournir explicitement sa valeur préenregistrée :

```python
analyze_identifiability(matrix, rank_tolerance=1e-12)
```

Ainsi, un seuil comme :

```text
epsilon_rank = 1e-12
```

appartient à la configuration normative du modèle ou du benchmark qui le préenregistre, et non au moteur d’identifiabilité lui-même.

Une tolérance purement technique sans incidence sur un résultat scientifique peut être autorisée si elle est explicitement documentée comme telle et ne masque aucune décision de protocole.

En cas de doute, la tolérance est considérée comme paramètre explicite.

---

## 10. Tests unitaires de `core`

Chaque brique `core` doit disposer de tests unitaires indépendants des modèles.

Ces tests sont placés sous :

```text
tests/core/
```

Ils peuvent notamment vérifier :

- domaine d’entrée ;
- cas limites ;
- conventions de signe ;
- relations algébriques ;
- propriétés matricielles ;
- comportement numérique ;
- erreurs attendues ;
- invariants propres à l’algorithme.

`tests/core/` est strictement **model-free**.

Il est interdit à un test sous `tests/core/` d’importer ou de construire un module de `models/modelXX/`.

Si une vérification nécessite l’assemblage d’un modèle, elle appartient à `tests/models/modelXX/`.

---

## 11. Tests des modèles

Les tests propres à un modèle sont placés sous :

```text
tests/models/modelXX/
```

Ils vérifient deux catégories distinctes.

### 11.1 Tests d’intégration du modèle

Ils vérifient que les briques `core` sont correctement assemblées par le modèle.

Exemple conceptuel :

```text
core.fermions
+
core.links
+
configuration model0a
→
observable assemblée attendue
```

### 11.2 Tests d’acceptation scientifique

Ils vérifient les résultats analytiques ou numériques préenregistrés propres au modèle.

Les oracles scientifiques particuliers restent dans les tests du modèle et dans les documents normatifs applicables.

Ils ne doivent pas migrer dans le code de production `core`.

---

## 12. Séparation des responsabilités de test

La stratégie de validation suit trois niveaux :

```text
tests unitaires du core
        ↓
tests d'intégration du modèle
        ↓
tests d'acceptation scientifique
```

À ces trois niveaux s’ajoutent les invariants transverses :

```text
tests/architecture/
```

Un échec doit pouvoir être localisé autant que possible à l’un de ces niveaux.

Un modèle ne doit pas être utilisé comme substitut aux tests unitaires d’une primitive générique.

Inversement, le succès des tests unitaires de `core` ne remplace jamais la validation de l’assemblage et des résultats propres au modèle.

---

## 13. Oracles et code de production

Les résultats analytiques particuliers d’un modèle ne doivent jamais être utilisés par les fonctions de production pour fabriquer le résultat attendu.

Les valeurs telles que :

```text
rang attendu
spectre attendu
états témoins attendus
valeurs propres attendues
matrices analytiques attendues
conditionnement attendu
```

restent dans les tests ou dans les documents normatifs du modèle.

Une constante physique constituant une **donnée d’entrée du modèle** n’est pas un oracle et peut naturellement faire partie de sa configuration.

Une tolérance scientifique ou numérique préenregistrée est également une donnée du modèle ou du protocole, pas une valeur par défaut du `core`.

---

## 14. Déterminisme et reproductibilité

Tout calcul destiné à participer à un benchmark, un test d’acceptation ou un résultat scientifique doit être reproductible dans un environnement enregistré.

### 14.1 Aléatoire

`core` ne doit pas dépendre d’un générateur pseudo-aléatoire global ou d’une graine implicite.

Lorsqu’un algorithme utilise de l’aléatoire, le générateur ou la graine doit être fourni explicitement.

Exemple recommandé :

```python
function(..., rng)
```

L’état global d’un module ne doit pas influencer silencieusement un résultat scientifique.

### 14.2 Ordre déterministe

Toute collection dont l’ordre influence :

- une base ;
- une matrice ;
- un spectre sérialisé ;
- une liste d’observables ;
- un rapport ;
- un fichier de résultat ;

doit utiliser un ordre déterministe explicitement défini.

Le code ne doit pas dépendre d’un ordre d’itération dont le contrat n’est pas garanti.

### 14.3 Environnement

Pour chaque benchmark accepté, l’environnement de référence doit permettre d’identifier au minimum :

```text
version Python
version NumPy
versions des dépendances scientifiques pertinentes
```

Les dépendances nécessaires à la reproductibilité doivent être épinglées dans l’environnement de référence du projet.

Les rapports sérialisés utilisés pour comparaison ou non-régression doivent adopter un ordre stable.

---

## 15. Statut scientifique et localisation logicielle

Les axes suivants sont indépendants :

```text
localisation logicielle
-----------------------
core
model-specific

statut scientifique
-------------------
déterminé par la documentation normative applicable
```

Il est donc possible d’avoir :

```text
location                      = core
SCIENTIFIC_METADATA.status    = project-defined
origin_model                  = modelXX
statut scientifique détaillé  = déterminé par la documentation normative applicable
```

sans contradiction. Le champ `SCIENTIFIC_METADATA.status` (§5.1) ne porte que la classification minimale de provenance (`established` ou `project-defined`) ; le statut scientifique détaillé d’une construction — hypothèse, expérimental, validé, ou tout autre qualificatif porté par sa documentation normative — reste de la responsabilité exclusive de cette documentation et n’est jamais dupliqué dans le code.

Aucune conclusion scientifique ne doit être inférée du seul emplacement d’un module dans l’arborescence.

---

## 16. Audit architectural d’un lot

Tout audit préalable à l’implémentation d’un modèle doit vérifier la conformité avec la présente gouvernance.

La profondeur de l’audit doit être proportionnelle à la taille et à la complexité du lot.

Pour chaque groupe cohérent de composants, l’audit fournit au minimum :

```text
composant | placement | justification | dépendances | validation
```

Lorsque cela apporte une information réelle, l’audit précise également :

```text
statut scientifique
source normative
origine du composant
```

L’audit doit vérifier explicitement :

- qu’aucune brique intrinsèquement générique n’est enfermée inutilement dans un modèle ;
- qu’aucune configuration spécifique n’est remontée artificiellement dans `core` ;
- que `core` ne dépend d’aucun modèle ;
- que `tests/core/` reste model-free ;
- que les tolérances scientifiques sont fournies par les modèles ou protocoles ;
- que les tests unitaires de `core` peuvent être exécutés indépendamment des benchmarks ;
- qu’aucune abstraction future spéculative n’a été introduite ;
- que les constructions scientifiques nouvelles placées dans `core` sont correctement tracées.

Lorsqu’un notebook Jupyter fait partie du lot audité, l’audit vérifie également :

- l’absence de logique scientifique définie uniquement dans le notebook (§23.3) ;
- l’absence de duplication d’une brique `core`/`model` déjà existante ;
- que les dépendances du notebook restent limitées à `model`/`core` (§23.2) ;
- l’absence de dépendance de `tests/` vers un notebook ;
- la présence d’une provenance lorsque des résultats sont conservés (§23.11) ;
- le respect du firewall confirmatoire (§23.8) ;
- l’absence d’état caché revendiqué dans une exécution archivée (§23.9).

L’audit peut regrouper les composants similaires et ne doit pas devenir une formalité disproportionnée par rapport au lot.

---

## 17. Contrat observable d’une brique `core`

Le contrat observable d’une brique `core` est constitué de :

1. ses tests unitaires ;
2. les invariants architecturaux qui lui sont applicables ;
3. les tests d’intégration des modèles déjà acceptés qui dépendent de son comportement ;
4. les tests d’acceptation scientifique de ces modèles lorsqu’ils dépendent effectivement de la brique.

Une évolution de `core` n’est compatible que si cet ensemble reste satisfait, sauf changement normatif explicitement autorisé.

### 17.1 Gel des oracles des modèles acceptés

Les oracles et tests d’acceptation scientifique d’un modèle accepté sont gelés avec le modèle qu’ils valident.

Ils ne doivent jamais être modifiés dans le seul but de faire accepter une évolution de `core`.

Toute modification de leur sens exige :

1. une justification scientifique documentée ;
2. l’identification explicite de l’oracle modifié et de la raison ;
3. l’application de la procédure normative définie au §24 ;
4. une nouvelle validation explicite du modèle affecté.

La seule nécessité de faire repasser les tests après une évolution du `core` ne constitue jamais une justification suffisante.

Ainsi :

```text
tests/core
+
tests/architecture
+
tests/models des modèles acceptés
=
surface de non-régression du core
```

### 17.2 Exemple canonique : convention Jordan-Wigner

Une primitive fermionique peut appartenir à `core`.

Sa convention de signe est testée unitairement sous `tests/core/`.

Un modèle peut ensuite dépendre de cette convention pour produire un résultat observable particulier.

Par exemple, si un modèle possède un témoin vérifiant :

```math
O|\chi\rangle=-|\phi\rangle,
```

ce test d’acceptation du modèle participe lui aussi au contrat observable de la primitive `core` qui produit le signe.

Modifier `core` tout en conservant uniquement ses tests unitaires verts ne suffit donc pas : les modèles déjà acceptés constituent également des tests de non-régression de la bibliothèque commune.

---

## 18. Évolution du `core`

Le `core` est une bibliothèque progressive.

Chaque nouveau modèle peut :

```text
réutiliser
étendre
faire généraliser
ou ajouter
```

des briques communes lorsque son besoin le justifie.

Toute évolution doit préserver les comportements contractualisés au sens du §17, ou suivre une procédure normative explicite lorsqu’une incompatibilité est nécessaire.

Il est interdit de modifier silencieusement une brique `core` pour satisfaire un nouveau modèle au détriment des modèles existants.

Ainsi :

```math
\boxed{
\text{core}_{N+1}
=
\text{core}_N
+
\text{briques réellement nécessaires aux nouveaux modèles}
}
```

et non :

```math
\text{core}_{N+1}
=
\text{architecture supposée de tous les modèles futurs}.
```

---

## 19. Invariants architecturaux vérifiables

Les règles suivantes doivent être automatisées lorsque cela est techniquement fiable.

### 19.1 Dépendances

```text
core -X-> models
tests/core -X-> models
```

### 19.2 Métadonnées scientifiques

Les modules publics de `core` doivent porter les métadonnées définies au §5.

### 19.3 Déterminisme vérifiable

Lorsque cela peut être contrôlé mécaniquement, les tests d’architecture doivent signaler :

- les imports ou usages d’un RNG global interdit ;
- les dépendances structurelles contraires à la gouvernance ;
- l’absence de métadonnées obligatoires.

### 19.4 Limites de l’automatisation

Certaines violations ne sont pas détectables de manière fiable par analyse syntaxique, notamment :

- duplication sémantique d’une fonctionnalité ;
- abstraction prématurée ;
- constante conceptuellement propre à un modèle mais présentée comme générique ;
- généralisation inutile d’une API.

Ces points restent des contrôles obligatoires de l’audit et de la revue du diff.

Une règle n’est déclarée « automatiquement vérifiée » que si le test couvre réellement l’invariant annoncé.

### 19.5 Invariants relatifs aux notebooks

```text
NOTEBOOK_IS_NORMATIVE_SOURCE = FALSE
NOTEBOOK_IS_CODE_LIBRARY = FALSE
NOTEBOOK_ONLY_SCIENTIFIC_LOGIC = FORBIDDEN
TESTS_DEPEND_ON_NOTEBOOK = FORBIDDEN
CONFIRMATORY_NOTEBOOK_WITHOUT_AUTHORIZATION = FORBIDDEN
HIDDEN_KERNEL_STATE_FOR_ARCHIVED_RESULT = FORBIDDEN
```

Conformément au §19.4, ces règles ne sont pas toutes vérifiables automatiquement de manière fiable :

```text
AUTOMATICALLY_CHECKABLE
    TESTS_DEPEND_ON_NOTEBOOK
        (absence d’import d’un fichier .ipynb depuis tests/)

HUMAN/AGENT_REVIEW_REQUIRED
    NOTEBOOK_IS_NORMATIVE_SOURCE
    NOTEBOOK_IS_CODE_LIBRARY
    NOTEBOOK_ONLY_SCIENTIFIC_LOGIC
    CONFIRMATORY_NOTEBOOK_WITHOUT_AUTHORIZATION
    HIDDEN_KERNEL_STATE_FOR_ARCHIVED_RESULT
```

---

## 20. Ambiguïtés

### 20.1 Ambiguïté de placement

Appliquer d’abord le principe conservateur du §3.1 :

```text
ambigu → model-specific
```

Cette décision ne nécessite pas d’arrêt tant qu’elle ne modifie aucune convention scientifique et ne contredit aucun document normatif.

### 20.2 Ambiguïté scientifique

Si la réponse dépend de la portée, de la définition ou du statut scientifique d’une construction :

```text
Claude Code s'arrête
→ ChatGPT analyse
→ Lionel tranche
```

### 20.3 Ambiguïté purement logicielle

Si la nature scientifique est claire mais que seul le découpage interne est en question, Claude Code peut proposer une solution dans son audit.

Elle reste soumise à la revue du lot avant implémentation.

---

## 21. Interdictions

Il est notamment interdit :

- de créer un `core` dépendant des modèles ;
- de créer des tests unitaires `core` dépendant des modèles ;
- de copier une brique commune dans plusieurs modèles ;
- de placer dans `core` des oracles propres à un benchmark ;
- d’introduire dans `core` une tolérance scientifique implicite ;
- de rendre générique une API uniquement en prévision d’un modèle inexistant ;
- de coder une primitive générale avec des dimensions ou constantes propres au premier modèle qui l’utilise lorsque celles-ci ne font pas partie de sa définition ;
- de considérer qu’une construction est scientifiquement validée parce qu’elle a été déplacée dans `core` ;
- de modifier silencieusement une brique `core` pour satisfaire un nouveau modèle au détriment des modèles existants ;
- de modifier un oracle ou un test d’acceptation d’un modèle accepté uniquement pour faire accepter une évolution de `core` ;
- de dépendre d’un RNG global ou d’un ordre d’itération non contractualisé pour produire un résultat scientifique ;
- de présenter comme invariant automatique une règle que les tests ne savent pas réellement vérifier ;
- de définir dans un notebook une logique scientifique (primitive générique, observable, oracle, seuil, critère PASS/FAIL) qui n’appartient pas à `core` ou à `models/modelXX` (§23.3) ;
- de faire dépendre un test `pytest` de l’exécution d’un notebook ;
- de lancer une exécution confirmatoire depuis un notebook sans l’autorisation explicite exigée par le firewall confirmatoire (§23.8) ;
- de revendiquer comme artefact d’exécution valide un notebook archivé reposant sur un état de kernel caché (§23.9).

---

## 22. Principe de synthèse

La règle architecturale du projet est :

```math
\boxed{
\text{bibliothèque commune progressive}
+
\text{modèles comme assemblages consommateurs}
}
```

Une brique générique n’appartient pas au modèle qui l’a fait apparaître.

Un modèle ne contient que ce qui le définit effectivement comme modèle particulier.

En cas d’ambiguïté, le composant reste dans le modèle jusqu’à ce que sa généralité soit suffisamment établie.

La bibliothèque commune évolue avec les besoins scientifiques réellement rencontrés.

Elle est protégée par :

```text
tests unitaires du core
+
tests d'architecture
+
tests d'intégration des modèles
+
tests d'acceptation scientifique des modèles acceptés
```

La localisation logicielle d’une construction ne modifie jamais son statut scientifique.

---

## 23. Notebooks Jupyter d’exécution scientifique

Principe :

```text
NOTEBOOK_ROLE = EXECUTABLE_SCIENTIFIC_REPORT
```

et :

```text
NOTEBOOK_IS_NORMATIVE_SOURCE = FALSE
NOTEBOOK_IS_CODE_LIBRARY = FALSE
```

Un notebook Jupyter d’un modèle jouet (« toy ») est un artefact d’exécution scientifique versionné permettant de réunir :

- contexte ;
- équations de rappel ;
- imports ;
- configuration d’exécution ;
- appels au code de production ;
- tableaux ;
- figures ;
- résultats ;
- interprétation ;
- provenance.

Il ne constitue jamais la source canonique :

- des primitives `core` ;
- de la définition du modèle ;
- des paramètres normatifs ;
- des oracles ;
- des seuils ;
- des critères PASS/FAIL ;
- du protocole confirmatoire.

### 23.1 Arborescence

L’arborescence fonctionnelle du dépôt (§2) est complétée par l’espace d’exécution :

```text
experiments/
└── toyN/
    └── toyN.ipynb
```

Le nom réel d’un futur notebook suit l’identité du toy concerné, par exemple :

```text
experiments/toy0a/toy0a.ipynb
```

Ce dossier et ce fichier ne sont pas créés par la présente gouvernance : conformément au §2, les dossiers ne sont créés que lorsqu’un besoin réel apparaît.

### 23.2 Direction des dépendances

La direction des dépendances définie au §6 s’étend aux notebooks :

```text
notebook
    ↓
model
    ↓
core
```

Un notebook peut importer :

```text
cosmotgg.core
cosmotgg.models.modelXX
```

selon les besoins du toy. Un notebook peut également appeler directement une primitive `core` lorsqu’aucun assemblage model-specific n’est nécessaire.

Sont interdits :

```text
core   -X-> notebook
model  -X-> notebook
tests  -X-> notebook
```

En particulier, aucun code de production ne doit importer un fichier `.ipynb`, et aucun test `pytest` ne doit dépendre de l’exécution d’un notebook.

### 23.3 Source canonique du code

Le notebook consomme le code de production. Il ne le redéfinit pas.

Toute fonction qui calcule une quantité scientifique utilisée dans les résultats d’un toy appartient, selon sa nature, à :

```text
src/cosmotgg/core/
```

ou :

```text
src/cosmotgg/models/modelXX/
```

avec les tests correspondants (§10, §11).

Il est interdit de définir uniquement dans le notebook :

- une primitive mathématique générique ;
- un observable scientifique du modèle ;
- une dynamique ou transformation propre au modèle ;
- une fonction utilisée pour décider PASS/FAIL ;
- un oracle ;
- une règle de normalisation scientifique ;
- un seuil ou une tolérance normative.

Autrement dit :

```text
NOTEBOOK_ONLY_SCIENTIFIC_LOGIC = FORBIDDEN
```

### 23.4 Helpers locaux autorisés

Un notebook peut contenir des helpers locaux strictement présentationnels, par exemple :

- mise en forme de tableau ;
- libellés ;
- formatage d’affichage ;
- construction de légende ;
- mise en page d’une figure.

Condition : leur modification ne doit pouvoir changer ni la valeur scientifique calculée ni le verdict du toy.

Si un helper transforme réellement des données scientifiques, il doit être extrait vers `core` ou `models/modelXX` selon les critères des §3 et §4.

### 23.5 Notebook et tests

```text
NOTEBOOK != UNIT_TEST
NOTEBOOK != INTEGRATION_TEST
NOTEBOOK != ACCEPTANCE_TEST
```

La stratégie de test définie aux §10, §11 et §12 reste inchangée :

```text
tests/core/
tests/architecture/
tests/models/modelXX/
```

Le notebook peut afficher les résultats de calculs ou de contrôles, mais ne remplace jamais les tests automatisés. Un résultat scientifique n’est pas considéré comme validé au seul motif qu’une cellule Jupyter s’exécute sans erreur.

### 23.6 Notebook et documents normatifs

La chaîne documentaire applicable à un toy est :

```text
specification.md
    ↓
implementation-design.md
    ↓
validation-plan.md / manifeste préenregistré
    ↓
code core + model
    ↓
notebook d’exécution
    ↓
closure-report.md
```

Le notebook constitue une vue exécutable et narrative de l’expérience. Le `closure-report.md` reste le document de synthèse et de fermeture du toy lorsque celui-ci est formellement clos.

Le notebook ne peut modifier ou remplacer silencieusement une décision contenue dans la spécification, le plan de validation ou un manifeste préenregistré.

### 23.7 Exécution non confirmatoire

Un notebook peut être utilisé pendant la qualification, l’exploration autorisée ou le développement. Ses résultats doivent alors rester explicitement :

```text
NONCONFIRMATORY
```

Il ne peut pas convertir une exploration en test confirmatoire a posteriori.

### 23.8 Exécution confirmatoire

Le firewall confirmatoire existant s’applique intégralement aux notebooks. La valeur par défaut reste :

```text
CONFIRMATORY_EXECUTION = NOT_AUTHORIZED
```

Une campagne confirmatoire lancée depuis un notebook exige la même autorisation explicite que toute autre campagne.

Pour une exécution confirmatoire, les paramètres, la grille, les tolérances, les oracles, les critères et le protocole doivent provenir des sources préenregistrées applicables. Le notebook ne peut pas les remplacer ou les surcharger silencieusement.

Toute cellule permettant une modification interactive d’un paramètre confirmatoire doit être soit absente, soit incapable d’affecter la route confirmatoire autorisée.

### 23.9 Exécution propre

Avant qu’un notebook comportant des résultats soit considéré comme un artefact d’exécution valide, les conditions suivantes doivent être satisfaites :

```text
RESTART_KERNEL
RUN_ALL_TOP_TO_BOTTOM
NO_HIDDEN_STATE
```

L’exécution ne doit pas dépendre :

- de variables créées lors d’une exécution antérieure ;
- de cellules exécutées hors ordre ;
- d’un état manuel caché du kernel ;
- d’un fichier local non versionné non déclaré ;
- d’un RNG global implicite.

Une cellule doit pouvoir être comprise comme faisant partie d’une exécution séquentielle propre du notebook.

### 23.10 Déterminisme

Les règles de déterminisme du §14 s’appliquent aux notebooks. Si un notebook utilise de l’aléatoire, le générateur (`rng`) et la graine (`seed`) doivent provenir explicitement du protocole ou de la configuration d’exécution applicable. Aucun `np.random` global implicite ne doit être utilisé pour produire un résultat scientifique.

### 23.11 Provenance

Tout notebook dont les sorties sont conservées comme résultat ou preuve d’exécution doit exposer clairement une provenance comprenant au minimum :

```text
TOY_ID
EXECUTION_CLASS
SOURCE_HEAD
PROTOCOL_REFERENCE
```

ainsi que la version Python, la version NumPy et les versions des autres dépendances scientifiques pertinentes, conformément au §14.3.

```text
EXECUTION_CLASS = QUALIFICATION | CONFIRMATORY
```

`SOURCE_HEAD` désigne le commit du code ou du protocole effectivement exécuté. Le notebook n’a pas à connaître son propre futur commit SHA.

### 23.12 Sorties commitées

Règle par défaut : un notebook de développement ou de qualification voit ses sorties nettoyées avant commit, sauf résultat explicitement conservé comme artefact utile.

Pour un notebook destiné à archiver les résultats d’une exécution autorisée :

```text
COMMITTED_OUTPUTS = ALLOWED
```

uniquement si :

- exécution propre top-to-bottom (§23.9) ;
- provenance présente (§23.11) ;
- contexte d’exécution déclaré ;
- statut qualification/confirmatoire explicite.

Les sorties commitées restent :

```text
DERIVED_EVIDENCE
```

et non source normative.

### 23.13 Figures et tableaux

Les figures et tableaux du notebook peuvent être construits à partir des résultats produits par le code source. La logique purement visuelle peut rester dans le notebook.

En revanche, si une transformation de données affecte une quantité scientifique rapportée, cette transformation appartient au code testé de `core` ou de `models/modelXX` selon sa généralité (§3, §4).

### 23.14 Dépendances Jupyter

Le présent lot documentaire n’ajoute aucune dépendance.

```text
JUPYTER_DEPENDENCY = ADD_ONLY_WHEN_FIRST_NOTEBOOK_IS_IMPLEMENTED
```

L’ajout futur de Jupyter, ipykernel, nbformat ou équivalent devra :

- répondre à un besoin concret ;
- suivre la règle des dépendances du projet ;
- être explicitement autorisé dans le mandat concerné ;
- être intégré à l’environnement reproductible (§14.3).

Aucune distribution ou paquet particulier n’est imposé par la présente gouvernance.

---

## 24. Évolution de cette gouvernance

Toute modification de sens de cette gouvernance exige :

1. une proposition explicite ;
2. l’identification des conséquences sur le code et les modèles existants ;
3. la mise à jour des documents de gouvernance ou d’architecture affectés ;
4. la vérification du diff documentaire réel ;
5. la validation explicite de Lionel ORCIL.

Une correction éditoriale sans changement de sens ne nécessite pas de nouvelle décision scientifique, mais reste soumise aux règles documentaires générales du dépôt.
