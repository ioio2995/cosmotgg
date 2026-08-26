# Gouvernance normative de la documentation

Statut : **gelé**

Ce document définit l'architecture documentaire normative du dépôt `cosmotgg`.

## 1. Principe

Une information normative possède une seule source de vérité principale. Les index, README, décisions et fichiers de compatibilité peuvent la résumer ou y renvoyer, mais ne doivent pas maintenir une définition divergente.

Le code implémente les documents normatifs. Il ne redéfinit jamais silencieusement une convention scientifique.

Les documents de gouvernance s'appliquent transversalement aux documents et au code relevant de leur domaine. Lorsqu'une règle de gouvernance transverse précise ou restreint un choix d'implémentation plus ancien sans modifier son contenu scientifique, cette gouvernance s'applique jusqu'à remise en cohérence du document concerné.

## 2. Arborescence cible

```text
docs/
├── governance/
│   ├── collaboration-governance.md
│   ├── documentation-governance.md
│   ├── software-architecture-governance.md
│   ├── current-task.md
│   └── agents/
│       ├── code-governance.md
│       ├── docs-governance.md
│       └── physic-governance.md
├── model/
│   ├── hypothesis.md
│   └── hypothesis-annex-a.md
├── decisions/
│   ├── decisions.md
│   └── Dxxx-*.md
└── toy-models/
    └── toyN/
        ├── specification.md
        ├── implementation-design.md
        ├── validation-plan.md      # lorsqu'il existe
        └── closure-report.md       # lorsqu'il existe

experiments/
└── toyN/
    ├── ... manifeste/protocole applicable
    └── toyN.ipynb

schemas/
└── toyN/
```

Les dossiers vides ne sont pas créés à l'avance. Cette arborescence est la cible normative ; l'écart entre elle et l'état réel du dépôt à un instant donné est décrit en §10.

## 3. Rôle des fonctions documentaires

### `docs/governance/`

Règles transverses du dépôt : architecture documentaire, collaboration, architecture logicielle, publication, statuts, contrôles, et état courant du contrat de continuité.

### `docs/governance/agents/`

Contrats normatifs des rôles spécialisés utilisés par les agents ou outils de collaboration. Ces documents définissent le comportement d'un rôle sans remplacer les gouvernances transverses.

Les configurations locales d'agents ne sont pas des sources normatives et ne sont pas tenues d'être versionnées. Elles doivent référencer le contrat versionné correspondant au lieu d'en maintenir une copie divergente.

### `docs/model/`

Hypothèse fondatrice générale du projet et conventions communes à plusieurs modèles jouets.

### `docs/decisions/`

Le fichier `decisions.md` conserve le journal historique. Une décision structurante volumineuse peut être portée par un fichier `Dxxx-*.md`, référencé par l'index et par le journal lors de sa prochaine consolidation.

Une ancienne décision gelée n'est jamais réécrite pour masquer l'historique.

### `docs/toy-models/toyN/`

Documentation propre à un modèle jouet : spécification, conception d'implémentation, plan de validation et clôture. Le `closure-report.md` reste le document de synthèse et de décision de fermeture d'un toy lorsque celui-ci est formellement clos ; le notebook d'exécution (`experiments/toyN/toyN.ipynb`) peut y être référencé comme `EXECUTABLE_EVIDENCE`, sans remplacer la décision de clôture.

### `experiments/toyN/`

Le dossier n'existe que lorsqu'un besoin réel apparaît. Il contient les artefacts versionnés liés à l'exécution du toy, notamment selon les besoins :

- manifestes préenregistrés ;
- protocoles d'exécution ;
- notebook Jupyter exécutable de présentation et de traçabilité de l'exécution ;
- autres artefacts explicitement autorisés.

Le notebook n'existe que lorsqu'il apporte une valeur réelle. Il est un artefact **dérivé** d'exécution ; il n'est jamais une source normative scientifique (voir `docs/governance/software-architecture-governance.md` §23).

### `schemas/toyN/`

Contrats de sérialisation versionnés.

### `features/`

Propositions temporaires non gelées. Après validation, leur contenu est migré vers les emplacements fonctionnels puis le brouillon est supprimé.

## 4. Hiérarchie des sources

Les documents de gouvernance ont autorité sur les règles transverses relevant explicitement de leur domaine, notamment collaboration, architecture documentaire et architecture logicielle.

Une gouvernance de rôle spécialisée sous `docs/governance/agents/` est subordonnée aux gouvernances transverses et fait autorité pour le comportement du rôle qu'elle définit. Une configuration locale ou un mandat courant peut restreindre davantage ce rôle mais ne peut pas affaiblir sa gouvernance ni une gouvernance transverse.

À l'intérieur du contenu scientifique ou expérimental, en cas de divergence :

1. décision gelée la plus récente ;
2. manifeste pré-enregistré pour les valeurs propres à une campagne ou une expérience ;
3. spécification du modèle jouet concerné ;
4. hypothèse C générale (`docs/model/`) ;
5. plan de validation ;
6. schéma de données ;
7. index et README ;
8. document exploratoire.

Le notebook d'exécution d'un toy (`experiments/toyN/toyN.ipynb`) ne prend jamais priorité sur une décision gelée, un manifeste préenregistré, une spécification, un plan de validation ou une gouvernance. En cas de divergence, la source normative prévaut ; le notebook est alors considéré obsolète ou incohérent et doit être régénéré ou corrigé. Le notebook n'est pas ajouté comme source normative concurrente dans la présente hiérarchie.

Une conception d'implémentation applique à la fois la spécification scientifique et les gouvernances transverses. Elle ne peut déroger implicitement à une gouvernance gelée plus récente.

Cette hiérarchie sert à résoudre temporairement la divergence ; la contradiction doit ensuite être corrigée.

## 5. Statuts

```text
brouillon
revue en cours
validé pour gel
gelé
clos
supersédé
archivé
```

Un document ne peut être gelé si une contradiction de statut ou de valeur subsiste.

## 6. Non-duplication

Les documents secondaires utilisent un renvoi vers la source principale. Les résumés sont autorisés s'ils sont clairement identifiés comme tels et mis à jour dans le même paquet lorsqu'ils changent de sens.

Une configuration locale d'agent contient uniquement les éléments techniques nécessaires à son chargement et les références vers sa gouvernance versionnée ; elle ne maintient pas une seconde définition normative du rôle.

## 7. Modification d'une norme gelée

Toute modification de sens exige :

1. une nouvelle décision ;
2. la mise à jour de la spécification concernée ;
3. la mise à jour du manifeste et du plan de validation si nécessaire ;
4. une nouvelle version de schéma en cas d'incompatibilité ;
5. la mise à jour des index et renvois.

Une correction éditoriale sans changement de sens ne nécessite pas de décision.

Une gouvernance transverse nouvellement gelée peut rendre nécessaire la remise en cohérence d'un document d'implémentation antérieur. Cette remise en cohérence est traitée dans le lot suivant applicable et ne modifie pas implicitement la physique gelée.

## 8. Compatibilité des anciens chemins

Lors d'une migration, un ancien chemin peut être conservé temporairement comme fichier de redirection marqué `supersédé`.

Ce fichier :

- ne contient aucune définition normative ;
- indique uniquement le nouveau chemin canonique ;
- n'est jamais utilisé dans un nouveau document ;
- est supprimé après vérification que plus aucun outil ou document actif ne le référence.

## 9. Contrôle avant publication documentaire

Avant de déclarer une migration terminée :

- vérifier la présence réelle des nouveaux fichiers ;
- vérifier que les anciens chemins ne contiennent plus de source normative dupliquée ;
- vérifier les statuts et valeurs gelées ;
- vérifier les liens des README et index ;
- vérifier le diff global fichier par fichier ;
- identifier explicitement les fichiers de compatibilité restants ;
- fournir le SHA final.

Un succès d'API Git ou une mise à jour de référence ne prouve pas à lui seul que le contenu annoncé est présent.

## 10. État actuel des sources canoniques

Les sources canoniques sont :

```text
docs/governance/collaboration-governance.md                    — gelé
docs/governance/documentation-governance.md                    — gelé
docs/governance/software-architecture-governance.md            — gelé
docs/governance/current-task.md                                — état courant
docs/governance/agents/code-governance.md                      — validé pour gel
docs/governance/agents/docs-governance.md                      — validé pour gel
docs/governance/agents/physic-governance.md                    — validé pour gel
docs/model/hypothesis.md                                       — gelé (FROZEN, v0.2)
docs/model/hypothesis-annex-a.md                                — gelé (FROZEN, synchronisée avec hypothesis.md v0.2)
```

Aucun document sous `docs/decisions/`, `docs/toy-models/`, `experiments/` ou `schemas/` n'existe encore. `docs/model/hypothesis.md` est la première source scientifique du projet : elle pose la question de recherche et l'hypothèse centrale de CosmoTGG, distingue explicitement `[KNOWN]`, `[DERIVED]`, `[HYPOTHESIS]` et `[OPEN]`, et est au statut `FROZEN` (v0.2) conformément au §5 et au §7, le contenu scientifique de référence étant celui du commit `SCIENTIFIC_CONTENT_HEAD = 589b0727ad880670435bfbb50a268d7472e5410f`. Ce gel documentaire ne signifie pas une validation de la vérité physique de l'hypothèse : les paramètres `GAP-1` à `GAP-6` restent explicitement `OPEN`. `docs/model/hypothesis-annex-a.md` complète cette source comme mémoire de recherche (annexe A), gelée en synchronisation avec `hypothesis.md` v0.2 : elle trace les idées, résultats de la littérature et pistes explorées puis écartées (`[ARCHIVED]`, `[REJECTED]`) pendant la construction de l'hypothèse, afin d'éviter de redécouvrir un résultat déjà connu ; elle ne redéfinit aucun objet normatif de `hypothesis.md`. Les autres dossiers ne sont créés que lorsqu'un besoin réel apparaît, conformément au §2.

## 11. Cycle documentaire d'un toy après démarrage de l'implémentation

### 11.1 Gel de la spécification et de la conception d'implémentation

Principe :

```text
TOY_IMPLEMENTATION_DOCUMENT_FREEZE = ENABLED
```

À partir du premier lot d'implémentation de code d'un toy, `specification.md` et `implementation-design.md` de ce toy deviennent :

```text
READ_ONLY_DURING_IMPLEMENTATION
```

pour le cycle d'implémentation courant.

```text
CODE_LOT_DOES_NOT_IMPLY_DOCS_LOT = TRUE
```

L'ajout d'une fonction, d'un test, d'un diagnostic, d'un refactor, d'un graphique, d'un résultat exploratoire ou d'une observation numérique ne déclenche pas automatiquement une modification de `specification.md` ou de `implementation-design.md`.

### 11.2 Condition de réouverture

```text
DOCUMENT_REOPEN_CONDITION = FUNDAMENTAL_BLOCKING_ONLY
```

La réouverture de `specification.md` ou de `implementation-design.md` pendant l'implémentation n'est autorisée que si un blocage fondamental démontre que le contrat doit changer, par exemple : une définition normative mathématiquement incorrecte ; une contradiction scientifique démontrée ; une impossibilité structurelle d'implémenter le contrat ; une hypothèse ou un invariant gelé incompatible avec l'implémentation ; un changement structurel indispensable du modèle explicitement arbitré par ChatGPT/Lionel.

Ne constituent pas une raison suffisante : un nouveau diagnostic exploratoire, un résultat intéressant, un besoin de commentaire, l'ajout d'une fonction, un changement de nom technique, un refactor, un graphique supplémentaire, une nouvelle observation du comportement du toy.

Toute réouverture exige, dans cet ordre : un verdict `BLOCKED` démontré, un arbitrage explicite de ChatGPT/Lionel, puis un mandat documentaire borné.

### 11.3 Rôle narratif du notebook

Le rôle normatif du notebook d'exécution d'un toy reste défini par `docs/governance/software-architecture-governance.md` §23 (`NOTEBOOK_ROLE = EXECUTABLE_SCIENTIFIC_REPORT`, `NOTEBOOK_IS_NORMATIVE_SOURCE = FALSE`, `NOTEBOOK_IS_CODE_LIBRARY = FALSE`) ; la présente section ne le redéfinit pas.

À partir du démarrage de l'implémentation d'un toy, ce notebook porte également le récit scientifique courant de l'expérience — question étudiée, motivation d'une étape, cheminement expérimental, introduction des diagnostics, équations utiles à la compréhension, appels au code testé, contrôles, tableaux et graphiques, résultats, interprétation, limites, résultat négatif éventuel, motivation de l'étape suivante — plutôt qu'une succession de micro-lots documentaires. Formulation conceptuelle complémentaire à `docs/governance/software-architecture-governance.md` §23 :

```text
MARKDOWN_NORMATIVE = CONTRACT
PYTHON_CODE        = MECHANISM
NOTEBOOK           = EXECUTABLE_EXPERIMENTAL_NARRATIVE
```

Cette formulation n'affaiblit aucune restriction déjà posée par `docs/governance/software-architecture-governance.md` §23.3 : le notebook ne contient pas comme seule définition une primitive générique, une définition normative du modèle, un oracle scientifique, un seuil d'acceptation, une tolérance normative, ou une logique PASS/FAIL.

### 11.4 Plan de validation et gel confirmatoire

Un `validation-plan.md` n'est pas nécessaire pendant l'exploration normale d'un toy. Il devient nécessaire avant une exécution réellement confirmatoire :

```text
CONFIRMATORY_PROTOCOL_FREEZE_BEFORE_EXECUTION = REQUIRED
```

Le protocole confirmatoire doit être défini puis gelé avant l'exécution correspondante. Une fois l'exécution confirmatoire commencée :

```text
validation-plan.md = READ_ONLY_DURING_CONFIRMATORY_EXECUTION
```

Il ne peut pas être modifié en fonction des résultats observés. Toute correction fondamentale suit le même mécanisme qu'au §11.2 (`BLOCKED`, arbitrage, puis nouveau protocole ou nouvelle version explicite). Le présent paragraphe clarifie le cycle documentaire du plan de validation ; il ne modifie aucune règle scientifique existante du pare-feu confirmatoire (`docs/governance/software-architecture-governance.md` §23.7–§23.8).

### 11.5 Closure report

`closure-report.md` reste le document de synthèse et de décision de fermeture d'un toy lorsque celui-ci est formellement clos (§3). Il n'est pas entretenu après chaque étape intermédiaire de l'implémentation.
