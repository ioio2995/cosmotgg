# Annexe A — Cartographie des idées et structures mathématiques explorées

**Statut : synchronisée avec `hypothesis.md` v0.2 — mémoire de recherche, brouillon, non gelée.**

## A.1 Objet de l’annexe

Cette annexe conserve les principales idées rencontrées pendant la construction de CosmoTGG, y compris celles qui ne font plus partie de l’hypothèse centrale.

Elle poursuit trois objectifs :

1. éviter de redécouvrir ultérieurement un résultat déjà connu ;
2. conserver les rapprochements qui pourraient redevenir pertinents ;
3. distinguer explicitement :

   * **[KNOWN]** : résultat établi ;
   * **[DERIVED]** : conséquence mathématique directe ;
   * **[HYPOTHESIS]** : hypothèse CosmoTGG ;
   * **[OPEN]** : question non résolue ;
   * **[ARCHIVED]** : piste explorée mais non retenue actuellement comme objet fondamental.

---

# A.2 Échelles quantiques et gravitationnelles

## A.2.1 Échelle de Planck

**[KNOWN]**

Les constantes

$$
\hbar,\qquad c,\qquad G
$$

permettent de construire les unités de Planck :

$$
\boxed{
\ell_P=
\sqrt{\frac{\hbar G}{c^3}}
}
$$

$$
\boxed{
t_P=
\sqrt{\frac{\hbar G}{c^5}}
=
\frac{\ell_P}{c}
}
$$

$$
\boxed{
m_P=
\sqrt{\frac{\hbar c}{G}}
}
$$

et :

$$
\boxed{
E_P=m_Pc^2=
\sqrt{\frac{\hbar c^5}{G}}.
}
$$

Les valeurs CODATA 2022 donnent notamment :

$$
\ell_P\simeq1.616255\times10^{-35}\ {\rm m}
$$

et :

$$
t_P\simeq5.391247\times10^{-44}\ {\rm s}.
$$

Ces expressions et valeurs sont standardisées par CODATA/NIST.

### Précaution essentielle

$$
\boxed{
\ell_P\neq\text{« plus petite longueur démontrée de la nature »}.
}
$$

Aucune expérience n’a établi que toute longueur inférieure à \(\ell_P\) soit interdite.

\(\ell_P\) est l’échelle dimensionnelle naturelle obtenue lorsque :

$$
\hbar,\quad c,\quad G
$$

interviennent simultanément.

**Statut CosmoTGG : référence d’échelle, pas hypothèse microscopique.**

En particulier :

$$
\boxed{\text{NO\_PLANCK\_SCALE\_INPUT}}
$$

reste une contrainte du programme lorsque l’objectif est précisément de faire émerger \(G\).

---

## A.2.2 Longueur de Compton

**[KNOWN]**

Pour une particule de masse \(m\), la longueur de Compton réduite est :

$$
\boxed{
\bar\lambda_C=
\frac{\hbar}{mc}.
}
$$

Elle représente une échelle quantique naturelle associée à la masse de la particule.

Elle ne constitue pas davantage une « taille géométrique » de la particule.

Pour l’électron :

$$
\bar\lambda_e\simeq3.86\times10^{-13}\ {\rm m}.
$$

---

## A.2.3 Échelle gravitationnelle d’une masse

Le rayon gravitationnel associé à \(m\) est :

$$
r_g=\frac{Gm}{c^2},
$$

et le rayon de Schwarzschild :

$$
\boxed{
r_s=\frac{2Gm}{c^2}.
}
$$

Pour une particule élémentaire, cette échelle est extraordinairement inférieure à son échelle quantique de Compton.

---

## A.2.4 Couplage gravitationnel sans dimension

**[KNOWN / DERIVED]**

On peut définir :

$$
\boxed{
\alpha_G(m)=
\frac{Gm^2}{\hbar c}.
}
$$

Il ne s’agit **ni d’une longueur, ni d’une géométrie minimale**.

C’est un nombre sans dimension caractérisant la faiblesse du couplage gravitationnel associé à une masse \(m\).

En utilisant les définitions précédentes :

$$
\boxed{
\alpha_G=
\left(
\frac{\ell_P}{\bar\lambda_C}
\right)^2
}
$$

et :

$$
\boxed{
r_s=
2\alpha_G\bar\lambda_C.
}
$$

Pour l’électron :

$$
\alpha_G^{(e)}
\sim1.75\times10^{-45}.
$$

À la masse de Planck :

$$
m=m_P,
$$

on obtient :

$$
\boxed{\alpha_G=1}.
$$

### Idée explorée puis corrigée

**[ARCHIVED]**

L’idée que \(\alpha_G\) puisse constituer une « échelle minimale de géométrie » a été écartée.

La lecture correcte est :

$$
\boxed{
\alpha_G
=
\text{intensité relative d’un couplage gravitationnel quantique caractéristique}.
}
$$

---

# A.3 Nombre minimal de relations et apparition d’une géométrie

## A.3.1 Un point ne définit aucune distance

**[KNOWN]**

Un élément isolé :

$$
A
$$

ne permet pas de définir intrinsèquement une distance.

Deux éléments :

$$
A,\;B
$$

permettent au minimum une relation :

$$
d_{AB}.
$$

Trois éléments :

$$
A,B,C
$$

peuvent former un triangle.

Quatre éléments :

$$
A,B,C,D
$$

permettent le premier simplexe non dégénéré tridimensionnel : le tétraèdre.

C’est la raison pour laquelle le tétraèdre constitue le premier banc d’essai naturel de CosmoTGG pour une pré-géométrie 3D relationnelle.

---

## A.3.2 Reconstruction d’un tétraèdre depuis six distances

Les six relations :

$$
d_{AB},d_{AC},d_{AD},
d_{BC},d_{BD},d_{CD}
$$

peuvent définir un tétraèdre si elles satisfont les conditions métriques appropriées.

Son volume peut être obtenu par le déterminant de Cayley–Menger :

$$
\boxed{
288V^2=
\det
\begin{pmatrix}
0&1&1&1&1\\
1&0&d_{AB}^2&d_{AC}^2&d_{AD}^2\\
1&d_{AB}^2&0&d_{BC}^2&d_{BD}^2\\
1&d_{AC}^2&d_{BC}^2&0&d_{CD}^2\\
1&d_{AD}^2&d_{BD}^2&d_{CD}^2&0
\end{pmatrix}.
}
$$

### Précaution CosmoTGG

Une corrélation quantique :

$$
I(A:B)
$$

n’est **pas automatiquement une distance** :

$$
\boxed{
I(A:B)\neq d_{AB}
}
$$

sans démonstration supplémentaire.

Une éventuelle fonction :

$$
d_{AB}=F[I(A:B)]
$$

devra notamment satisfaire les propriétés métriques nécessaires et ne doit jamais être choisie uniquement pour fabriquer la géométrie recherchée.

---

# A.4 Masse, énergie et configurations stables

## A.4.1 Énergie de repos

**[KNOWN]**

Pour une particule de masse \(m\) :

$$
\boxed{
E_0=mc^2.
}
$$

La masse n’est pas une quantité universellement conservée indépendamment de l’énergie.

Des processus comme :

$$
e^-+e^+\rightarrow\gamma+\gamma
$$

convertissent de l’énergie de masse en énergie électromagnétique tout en conservant l’énergie-impulsion et les charges requises.

---

## A.4.2 Matière comme excitation de champs

**[KNOWN]**

En théorie quantique des champs, les champs sont les objets fondamentaux du formalisme et les particules correspondent à leurs excitations quantifiées.

Une particule élémentaire n’est donc pas décrite comme une petite géométrie classique contenant plusieurs champs.

---

## A.4.3 Matière comme configuration stable

**[ARCHIVED mais potentiellement utile]**

L’idée :

$$
\boxed{
\text{particule}
=
\text{configuration localisée stable d’un champ}
}
$$

possède des précédents réels dans les théories de solitons.

Le modèle de Skyrme, par exemple, traite les baryons comme des solitons topologiques d’une théorie effective de champs mésoniques.

Cette piste a été examinée au début de l’exploration mais n’est plus actuellement nécessaire à CosmoTGG, dont le niveau fondamental est relationnel plutôt que construit autour d’un nouveau champ scalaire.

---

# A.5 Le tenseur énergie-impulsion

## A.5.1 Structure

**[KNOWN]**

La source classique de la géométrie en relativité générale est :

$$
\boxed{T_{\mu\nu}}
$$

et non uniquement une densité de matière.

Schématiquement :

$$
T_{\mu\nu}
\sim
\begin{pmatrix}
\text{densité d'énergie} & \text{flux d'énergie}\\
\text{densité d'impulsion} & \text{pressions/contraintes}
\end{pmatrix}.
$$

L’équation d’Einstein est :

$$
\boxed{
G_{\mu\nu}
=
\frac{8\pi G}{c^4}T_{\mu\nu}.
}
$$

---

## A.5.2 Les champs électromagnétiques gravitent

**[KNOWN]**

Le champ électromagnétique possède son propre tenseur énergie-impulsion.

Sa densité d’énergie dans le vide vaut :

$$
\boxed{
u_{\rm EM}
=
\frac{\varepsilon_0}{2}E^2
+
\frac{1}{2\mu_0}B^2.
}
$$

Donc :

$$
\boxed{
\text{matière massive}
}
$$

n’est pas la seule source de gravitation.

La lumière, les champs électriques, les champs magnétiques, les pressions et les flux d’énergie contribuent à \(T_{\mu\nu}\).

### Conséquence méthodologique

Toute théorie candidate dans laquelle la source fondamentale serait seulement :

$$
\rho_{\rm matière}
$$

est insuffisante.

La source macroscopique obtenue doit au minimum pouvoir reproduire l’information portée par :

$$
T_{\mu\nu}.
$$

---

# A.6 Géométrie d’un champ et géométrie de l’espace-temps

**[KNOWN]**

Une distinction importante a été établie pendant l’exploration :

$$
\boxed{
\text{géométrie/configuration d’un champ}
\neq
\text{géométrie de l’espace-temps}.
}
$$

Par exemple, les lignes d’un champ magnétique peuvent être courbes :

$$
\mathbf B(\mathbf x),
$$

sans que cette courbure graphique soit une courbure de Riemann.

La courbure de l’espace-temps est caractérisée par :

$$
R^\rho{}_{\sigma\mu\nu}.
$$

Le champ électromagnétique peut néanmoins **produire** de la courbure parce que son énergie-impulsion contribue à :

$$
T_{\mu\nu}.
$$

Cette distinction doit être conservée afin de ne jamais confondre :

$$
\text{forme d’une distribution}
$$

et :

$$
\text{forme de l’espace dans lequel elle est définie}.
$$

---

# A.7 Rythme des horloges et gravitation statique

## A.7.1 Facteur de redshift

**[KNOWN]**

Dans un espace-temps statique :

$$
ds^2=
-N^2(\mathbf x)c^2dt^2
+
h_{ij}dx^idx^j.
$$

Pour un observateur statique :

$$
\boxed{
d\tau=N\,dt.
}
$$

\(N\) encode donc le rapport entre temps propre et coordonnée temporelle dans ce découpage.

---

## A.7.2 Limite faible

Pour :

$$
\left|\frac{\Phi}{c^2}\right|\ll1,
$$

on a :

$$
N\simeq1+\frac{\Phi}{c^2}.
$$

L’accélération newtonienne est alors reliée au gradient de ce facteur :

$$
\boxed{
\mathbf a\simeq
-c^2\nabla\ln N
\simeq
-\nabla\Phi.
}
$$

Cette observation a motivé temporairement l’idée que la gravitation pourrait n’être qu’un gradient de rythme temporel.

---

## A.7.3 Pourquoi le temps seul ne suffit pas

**[KNOWN / ARCHIVED]**

Dans le formalisme post-newtonien, la métrique faible peut être écrite schématiquement :

$$
g_{00}
\simeq
-\left(1+\frac{2\Phi}{c^2}\right)
$$

et :

$$
g_{ij}
\simeq
\left(1-2\gamma\frac{\Phi}{c^2}\right)\delta_{ij}.
$$

La relativité générale correspond à :

$$
\boxed{\gamma=1}.
$$

La déviation lumineuse dépend du facteur :

$$
1+\gamma.
$$

Un modèle reproduisant seulement la composante temporelle mais aucune réponse spatiale correspondrait schématiquement à \(\gamma=0\) et ne reproduirait qu’une partie de la déviation observée. Ce résultat est déjà codifié dans le formalisme PPN et ne doit plus faire l’objet d’une redérivation spécifique CosmoTGG.

**Conclusion archivée :**

$$
\boxed{
\text{gravitation}\neq
\text{simple gradient scalaire du rythme des horloges}.
}
$$

---

# A.8 Homogénéisation et équations statiques d’Einstein

Cette piste reste conceptuellement importante parce qu’elle est proche de l’intuition historique d’un état tendant vers l’homogénéité.

## A.8.1 Équations du lapse dans le vide

**[KNOWN]**

Pour les données statiques de vide \((\Sigma,h,N)\), les équations d’Einstein impliquent :

$$
\boxed{
\Delta_hN=0
}
$$

et :

$$
\boxed{
N\,R_{ij}(h)=D_iD_jN.
}
$$

Ainsi, le lapse est harmonique dans le vide et sa Hessienne est liée à la courbure de la géométrie spatiale.

Ces équations donnent un analogue mathématique réel à l’intuition :

$$
\text{source}
\rightarrow
\text{inhomogénéité}
\rightarrow
\text{raccordement harmonique dans le vide}.
$$

### Mais

**[CRITICAL CAVEAT]**

Le lapse dépend du choix de foliation.

Il ne doit donc pas être identifié à un degré de liberté physique fondamental de CosmoTGG.

La partie physiquement pertinente doit être formulée en termes de relations invariantes entre observateurs ou sous-systèmes.

---

# A.9 Temps, gravité et équilibre thermique

## A.9.1 Relation de Tolman–Ehrenfest

**[KNOWN]**

Dans un espace-temps statique à l’équilibre thermique :

$$
\boxed{
T(\mathbf x)\sqrt{-g_{00}(\mathbf x)}
=
T_\infty
=
\text{constante}.
}
$$

Une température locale uniforme n’est donc pas la condition d’équilibre dans un champ gravitationnel statique.

Ce résultat relie directement :

$$
\text{équilibre thermodynamique}
$$

et :

$$
\text{rythme local des horloges}.
$$

Rovelli et Smerlak ont également analysé cette relation dans le cadre du temps thermique et interprété la température comme liée au taux du temps thermique relativement au temps propre.

**Statut CosmoTGG : source conceptuelle, pas mécanisme démontré d’émergence du temps.**

---

# A.10 Fluctuations quantiques et apparition d’un régime classique

## A.10.1 Ancienne intuition de fluctuation relative (archivée comme telle)

**[ARCHIVED — intuition, distincte du critère de Kuo–Ford]**

L’idée explorée était :

$$
R=
\frac{\Delta X}
{|\langle X\rangle|}.
$$

avec :

$$
R\gtrsim1
$$

pour un régime fortement fluctuant et :

$$
R\ll1
$$

pour une observable relativement bien définie.

Cette quantité \(\Delta X/|\langle X\rangle|\) (reprise dans `hypothesis.md` §12 sous la forme \(R_{\mathcal G}\)) est un **indicateur possible** de faible fluctuation, **ni nécessaire ni suffisant** pour établir une limite classique, et son usage est limité aux observables dont la moyenne est non nulle et convenablement bornée loin de zéro dans le régime testé. Elle doit être explicitement distinguée du critère de Kuo–Ford ci-dessous, qui porte une définition et une normalisation propres.

---

## A.10.2 Kuo–Ford

**[KNOWN]**

Kuo et Ford ont étudié dès 1993 une mesure sans dimension des fluctuations du tenseur énergie-impulsion afin d’évaluer la validité de la gravité semi-classique.

Leur critère s'écrit sous sa forme propre :

$$
\boxed{
\Delta(x)
=
\left|
\frac{
\langle:T_{00}^2(x):\rangle
-
\langle:T_{00}(x):\rangle^2
}{
\langle:T_{00}^2(x):\rangle
}
\right|
}
$$

et :

$$
\Delta\ll1
$$

est leur indicateur de petites fluctuations dans le cadre étudié.

Leur idée fondamentale est que :

$$
\boxed{
\text{grandes fluctuations de }T_{\mu\nu}
\Rightarrow
\text{métrique classique moyenne potentiellement insuffisante}.
}
$$

Ils trouvent notamment des fluctuations importantes pour plusieurs états quantiques non classiques.

### Correction importante

Un seuil universel du type :

$$
R=1
$$

ne constitue **pas** une frontière démontrée entre géométrie quantique et géométrie classique. Le critère \(\Delta\ll1\) de Kuo–Ford n'est pas non plus présenté comme une frontière universelle entre géométrie quantique et classique : c'est leur indicateur de petites fluctuations dans le cadre étudié.

Le résultat dépend de l’observable, de l’état, du lissage spatial/temporel et des corrélations.

**Statut : notre ancien \(R_C\) est archivé comme intuition (A.10.1) ; il ne constitue pas un nouveau critère physique et ne doit pas être confondu avec le critère de Kuo–Ford (A.10.2).**

---

# A.11 Gravité stochastique

**[KNOWN]**

La gravité stochastique étend la gravité semi-classique en tenant compte des fluctuations du tenseur énergie-impulsion.

L’objet central est le *noise kernel* :

$$
\boxed{
N_{abcd}(x,y)
=
\frac12
\left\langle
\left\{
\hat t_{ab}(x),
\hat t_{cd}(y)
\right\}
\right\rangle
}
$$

avec :

$$
\hat t_{ab}
=
\hat T_{ab}
-
\langle\hat T_{ab}\rangle.
$$

Il s’agit donc d’une corrélation à deux points des fluctuations de l’énergie-impulsion.

Ce formalisme montre qu’un objet relationnel :

$$
(x,y)
$$

porte davantage d’information que la variance en un point unique.

### Pertinence CosmoTGG

Cette théorie ne fait pas émerger la géométrie à partir de zéro : elle suppose déjà un fond géométrique semi-classique.

Elle constitue néanmoins un précédent important pour :

$$
\boxed{
\text{corrélations quantiques}
\rightarrow
\text{fluctuations géométriques}.
}
$$

---

# A.12 TGFT, géométrogenèse et critère de Ginzburg

**[KNOWN — programme de gravité quantique spécifique]**

Dans les Tensorial Group Field Theories, les degrés de liberté fondamentaux peuvent être interprétés comme des briques discrètes de géométrie.

Les travaux Landau–Ginzburg sur des modèles TGFT lorentziens étudient une transition entre un vide trivial et une phase à champ moyen non nul candidate à une phase géométrique collective.

Le critère de Ginzburg compare les fluctuations autour du champ moyen à celui-ci.

Dans les modèles étudiés, les fluctuations restent petites à grande longueur de corrélation, ce qui permet de contrôler l’approximation de champ moyen.

### Correction d’une idée antérieure

Il ne faut pas identifier :

$$
Q\sim1
$$

à :

$$
\text{« naissance de la géométrie »}.
$$

\(Q\) mesure plutôt la validité de l’approximation de champ moyen.

Le régime :

$$
\boxed{Q\ll1}
$$

indique que les fluctuations relatives sont suffisamment petites pour que le champ moyen soit fiable.

### Statut CosmoTGG

TGFT constitue un **candidat de réalisation microscopique ultérieure**, mais n’est plus le point de départ du programme.

---

# A.13 Invariance d’échelle, anomalie et émergence du temps

## A.13.1 Transmutation dimensionnelle

**[KNOWN — mécanisme général RG]**

Une théorie possédant initialement des couplages sans dimension peut générer dynamiquement une échelle lorsque les corrections quantiques rendent :

$$
\beta(g)\neq0.
$$

Pour un exemple schématique :

$$
\beta(g)
=
\frac{dg}{d\ln\mu}
=
-bg^2,
$$

on obtient une échelle RG de la forme :

$$
\boxed{
\Lambda
=
\mu
\exp\left(
-\frac{1}{bg(\mu)}
\right).
}
$$

Le point important est qu’une échelle physique peut donc apparaître alors que la formulation classique ne contenait pas directement de masse caractéristique.

---

## A.13.2 Scale Anomaly as the Origin of Time

**[KNOWN — preuve de principe dans un modèle particulier]**

Barbour, Lostaglio et Mercati ont étudié un modèle relationnel invariant d’échelle dans lequel la quantification produit une anomalie conforme.

Le flot de renormalisation résultant est alors interprété comme une évolution temporelle émergente.

La chaîne conceptuelle est :

$$
\boxed{
\text{invariance d’échelle}
\rightarrow
\text{anomalie quantique}
\rightarrow
\text{flot RG}
\rightarrow
\text{temps émergent}.
}
$$

### Pertinence pour CosmoTGG

Ce résultat constitue une preuve de principe qu’un temps peut émerger du même mécanisme qui génère une échelle.

Il ne démontre pas que ce mécanisme produit notre univers, une géométrie 3+1D ou la gravitation.

---

# A.14 Gravité induite et origine possible de \(G\)

## A.14.1 Sakharov

**[KNOWN — famille de modèles]**

L’idée de gravité induite de Sakharov consiste à ne pas considérer nécessairement le terme d’Einstein–Hilbert comme fondamental.

Les fluctuations quantiques des champs de matière peuvent produire dans l’action effective un terme :

$$
\boxed{
S_{\rm eff}
\supset
\frac{1}{16\pi G_{\rm eff}}
\int d^4x\sqrt{-g}\,R.
}
$$

Dans ces constructions :

$$
G_{\rm eff}
$$

dépend typiquement de la microphysique et d’une échelle UV.

### Pertinence

Cela démontre qu’il est légitime de demander :

$$
\boxed{
G=\text{paramètre effectif}
}
$$

plutôt que :

$$
G=\text{constante microscopique nécessairement fondamentale}.
$$

Mais cela ne constitue pas encore une prédiction non circulaire de la valeur observée de \(G\).

**Réserve (universalité vs. microphysique) :** dans les scénarios de gravité induite de type Sakharov, la valeur de \(G_{\rm eff}\) peut dépendre du contenu microscopique et de l'échelle UV. Cela ne doit pas être confondu avec la question de l'universalité du couplage dans la théorie effective obtenue (cf. `hypothesis.md` §13) : l'universalité recherchée par CosmoTGG signifie qu'un même coefficient gouverne la réponse géométrique aux différentes sources admissibles dans une phase et une classe de systèmes déclarées, pas une indépendance absolue de toute microphysique.

---

# A.15 Gravité comme thermodynamique / équilibre d’intrication

## A.15.1 Jacobson 1995

**[KNOWN — sous hypothèses explicites]**

Jacobson montre que la relation :

$$
\boxed{
\delta Q=T\,dS
}
$$

appliquée aux horizons locaux de Rindler, associée à une entropie proportionnelle à l’aire :

$$
dS=\eta\,dA,
$$

conduit à l’équation d’Einstein.

Cela motive l’interprétation :

$$
\boxed{
\text{équation d’Einstein}
\sim
\text{équation d’état macroscopique}.
}
$$

Le coefficient \(\eta\) fixe alors le couplage gravitationnel.

Cette observation reste particulièrement importante pour la question :

$$
\boxed{\text{d’où vient }G\ ?}
$$

**Précision de portée :** Jacobson déplace la question de l'origine de \(G\) vers le coefficient entropie/aire ; il ne la résout pas. Le résultat ne dérive donc pas la valeur de \(G\) à partir de zéro.

---

## A.15.2 Jacobson 2016 (Entanglement Equilibrium)

**[KNOWN — sous hypothèses spécifiques]**

Jacobson montre également qu’une condition de stationnarité de l’entropie d’intrication du vide dans de petites boules géodésiques **à volume fixé** peut être reliée à l’équation d’Einstein semi-classique au premier ordre (Physical Review Letters 116, 201101, 2016 ; arXiv:1505.04753).

Ce résultat donne un précédent concret à :

$$
\boxed{
\text{équilibre quantique}
\rightarrow
\text{dynamique géométrique}.
}
$$

Il suppose cependant déjà des structures géométriques telles que les petites boules géodésiques, et l'hypothèse entropique utilisée contient déjà un coefficient aire/entropie faisant intervenir le couplage gravitationnel. Ce n'est donc pas une dérivation de \(G\).

---

# A.16 Première loi de l’intrication

**[KNOWN]**

Pour deux états infinitésimalement proches :

$$
\rho
\rightarrow
\rho+\delta\rho,
$$

la première variation de l’entropie satisfait :

$$
\boxed{
\delta S
=
\delta\langle K\rangle
}
$$

avec :

$$
K=-\ln\rho_0
$$

l’Hamiltonien modulaire de l’état de référence.

Cette identité constitue un des raccords centraux entre :

$$
\text{état quantique},
\quad
\text{information},
\quad
\text{structure modulaire}.
$$

---

# A.17 Intrication et équations gravitationnelles holographiques

**[KNOWN — uniquement dans le cadre holographique concerné]**

Faulkner et al. montrent que, dans une CFT possédant un dual gravitationnel semi-classique approprié, les contraintes provenant de la première loi de l’intrication pour toutes les régions sphériques sont équivalentes aux équations gravitationnelles linéarisées du bulk.

Lorsque l’entropie holographique est donnée par :

$$
S=\frac{A}{4G_N},
$$

on retrouve les équations d’Einstein linéarisées.

### Limite essentielle

$$
\boxed{
G_N
}
$$

est déjà présent dans la correspondance aire-entropie.

Ce résultat ne constitue donc pas une dérivation de \(G\) à partir de zéro.

---

# A.18 Temps thermique et structure modulaire

**[KNOWN / HYPOTHÈSE PHYSIQUE EXISTANTE]**

Connes et Rovelli proposent la *Thermal Time Hypothesis*.

Un état sur une algèbre d’observables définit, via la théorie de Tomita–Takesaki, un groupe d’automorphismes modulaires.

Schématiquement :

$$
\boxed{
\rho
\rightarrow
K=-\ln\rho
\rightarrow
\sigma_s.
}
$$

Ils proposent d’interpréter ce flot déterminé par l’état comme origine du temps physique dans un cadre généralement covariant.

### Limite

Le paramètre modulaire :

$$
s
$$

n’est pas automatiquement une durée mesurée en secondes.

La calibration du temps physique reste une question distincte.

### Convention de signe

Avec \(K=-\ln\rho\), CosmoTGG adopte la convention physique \(O(s)=e^{+iKs}Oe^{-iKs}\) (`hypothesis.md` §4). Cette convention correspond au choix de signe utilisé par Connes–Rovelli pour le temps thermique et est opposée à une convention mathématique courante du paramètre modulaire de Tomita–Takesaki. Elle est conservée dans tout CosmoTGG et n'a pas été inversée lors de la présente correction.

---

## A.18.2 Dynamique relationnelle sans horloge externe : littérature établie

**[KNOWN]**

La notion générale de dynamique relationnelle sans temps externe possède plusieurs formulations établies dans la littérature, distinctes de la Thermal Time Hypothesis :

* Page et Wootters (1983) montrent qu'une évolution observée peut être décrite relativement aux lectures d'une horloge interne dans un état global stationnaire ;
* les observables relationnelles / observables de Dirac constituent une autre famille de formulations relationnelles du changement ;
* Höhn, Smith et Lock (2021) montrent une équivalence entre plusieurs formulations modernes de dynamique quantique relationnelle.

### Frontière propre à CosmoTGG

Compte tenu de cette littérature, la question CosmoTGG n'est plus « peut-on avoir un changement relationnel sans temps externe ? » mais :

$$
\boxed{
\text{Peut-on construire un temps relationnel physique à partir des relations
entre plusieurs structures modulaires, sans ajouter un degré de liberté
fondamental désigné comme horloge, et en utilisant la même famille de
structures relationnelles que celle dont la géométrie est supposée émerger ?}
}
$$

(cf. `hypothesis.md` §7). La composition et l'orientation existent pour le groupe modulaire lui-même mais restent à démontrer pour l'éventuel temps physique relationnel dérivé.

---

## A.18.3 Du modèle fini de type I à la théorie modulaire algébrique

**[OPEN]**

La réalisation matricielle finie \(\rho_X/K_X=-\ln\rho_X\) utilisée dans `hypothesis.md` §4 est un modèle de type I employé comme banc d'essai minimal. Elle ne constitue pas encore la formulation adaptée aux algèbres locales de théorie quantique des champs, souvent de type III. Le passage à une structure modulaire algébrique appropriée à la QFT (théorie d'Araki des opérateurs modulaires relatifs) reste un verrou scientifique **[OPEN]** de CosmoTGG : \(\text{TYPE\_I\_TO\_ALGEBRAIC\_MODULAR\_BRIDGE}=\text{OPEN}\).

---

# A.19 Courbure de Berry modulaire

**[KNOWN — cadre holographique]**

Une famille d’Hamiltoniens modulaires permet de définir une connexion de Berry modulaire.

Dans certaines constructions AdS/CFT, sous leurs hypothèses propres, certaines données de connexion/courbure modulaire (\(\mathcal F_{\rm mod}\)) sont reliées à des données géométriques du bulk, notamment à des composantes de la courbure de Riemann. Czech, Lamprou, McCandlish et Sully, ainsi que Czech, de Boer, Ge et Lamprou, montrent explicitement cette relation dans le domaine holographique semi-classique considéré.

### Pertinence CosmoTGG

C’est actuellement le précédent mathématique le plus proche de :

$$
\boxed{
\text{structure relationnelle quantique}
\rightarrow
\text{courbure}.
}
$$

Mais CosmoTGG ne suppose aucune identité générale entre courbure modulaire et courbure de l'espace-temps : la relation \(\mathcal F_{\rm mod}\leftrightarrow R_{\mu\nu\rho\sigma}\) observée dans ces constructions holographiques n’est **pas** une identité générale de la mécanique quantique.

La construction sans bulk géométrique préalable constitue précisément l’un des tests CosmoTGG.

---

# A.20 Information mutuelle et opérateur modulaire relationnel

Pour deux sous-systèmes :

$$
A,\;B,
$$

on a :

$$
I(A:B)
=
S_A+S_B-S_{AB}
$$

et l’identité :

$$
\boxed{
I(A:B)
=
D(
\rho_{AB}
\Vert
\rho_A\otimes\rho_B
).
}
$$

Avec :

$$
K_A=-\ln\rho_A,
\qquad
K_B=-\ln\rho_B,
\qquad
K_{AB}=-\ln\rho_{AB},
$$

la combinaison :

$$
\boxed{
\mathcal R_{AB}
=
K_A\otimes I_B
+
I_A\otimes K_B
-
K_{AB}
}
$$

satisfait :

$$
\boxed{
I(A:B)
=
\operatorname{Tr}
(
\rho_{AB}\mathcal R_{AB}
).
}
$$

Ce résultat constitue le raccord mathématique actuellement retenu par CosmoTGG entre :

$$
\text{relation quantique}
$$

et :

$$
\text{structure modulaire}.
$$

Il ne nécessite aucune nouvelle constante physique.

### Domaine de validité et limite de portée

Le domaine de travail v0.2 est celui d'un état réduit joint fidèle \(\rho_{AB}>0\), ce qui garantit la fidélité des marginales \(\rho_A,\rho_B\) dans ce cadre fini (`hypothesis.md` §5). \(\mathcal R_{AB}\) est une combinaison opératorielle définie pour ce modèle fini ; elle ne doit pas être identifiée au logarithme de l'opérateur modulaire relatif général de Tomita–Takesaki/Araki dans le cas non commutatif.

---

# A.21 L’intuition historique « \(1\rightarrow0\) »

**[HYPOTHESIS / HEURISTIC ONLY]**

L’expression :

$$
1\rightarrow0
$$

a servi historiquement à représenter l’intuition suivante :

> un système possède une tendance vers un état plus homogène ou plus symétrique, mais sa structure quantique empêche éventuellement que cet état soit réalisé exactement.

Elle ne doit **jamais** être interprétée actuellement comme une équation dynamique :

$$
q(t)\rightarrow0.
$$

Cela introduirait précisément le temps que CosmoTGG cherche à faire émerger.

Une formulation mathématique acceptable devra plutôt introduire une mesure d’écart à un état de référence :

$$
\boxed{
\epsilon[\rho]\ge0
}
$$

avec :

$$
\epsilon[\rho_0]=0,
$$

sans supposer :

$$
\frac{d\epsilon}{dt}.
$$

Un éventuel ordre de changement devra émerger ultérieurement de la structure relationnelle elle-même.

### Statut

$$
\boxed{\text{OPEN}}
$$

Aucune fonction \(\epsilon[\rho]\) n’est actuellement définie par CosmoTGG.

---

# A.22 Hypothèse historique « temps et gravitation ont la même origine »

Cette intuition est conservée, mais dans une formulation désormais beaucoup plus stricte.

Elle ne signifie pas :

$$
\text{temps}\rightarrow\text{gravité}
$$

ni :

$$
\text{gravité}\rightarrow\text{temps}.
$$

L’hypothèse recherchée est :

$$
\boxed{
\text{structure quantique relationnelle}
\rightarrow
\begin{cases}
\text{flot/changement}\\
\text{connexion/courbure}
\end{cases}
}
$$

puis éventuellement, dans une limite collective :

$$
\boxed{
\begin{cases}
\text{flot relationnel}
\rightarrow
\tau\\[1mm]
\text{courbure relationnelle}
\rightarrow
g_{\mu\nu}
\end{cases}
}
$$

et seulement ensuite :

$$
\boxed{
\text{réponse universelle de }g_{\mu\nu}
\rightarrow
\text{gravitation}.
}
$$

**[OPEN]**

Il reste à démontrer que les deux branches proviennent réellement d’une même structure dynamique plutôt que d’être seulement deux constructions possibles à partir du même état.

Le test T4 (`hypothesis.md` §15) formalise cette question. Sa condition « relation stable et non accidentelle » n'est pas suffisamment opératoire : \(\text{T4\_OPERATIONAL\_CRITERION}=\text{OPEN}\). T4 ne pourra être exécuté qu'après définition et préenregistrement d'un critère capable de distinguer (A) deux constructions mathématiques indépendantes utilisant les mêmes données \(\rho\) de (B) deux manifestations contraintes d'une structure commune. Cette formalisation sera traitée dans un lot scientifique ultérieur.

---

# A.23 Idées explicitement archivées

Les pistes suivantes ont été explorées mais ne doivent plus être utilisées comme point de départ sans justification nouvelle :

### A.23.1 Nouveau champ scalaire fondamental

$$
\boxed{\text{ARCHIVED}}
$$

Aucun nouveau champ scalaire n’est actuellement nécessaire.

---

### A.23.2 Facteur temporel unique expliquant toute la gravitation

$$
\boxed{\text{ARCHIVED}}
$$

Le redshift temporel reproduit une partie importante de la phénoménologie gravitationnelle, mais ne contient pas à lui seul toute la structure métrique de GR.

---

### A.23.3 Géométrie fixe d’une particule élémentaire

$$
\boxed{\text{ARCHIVED}}
$$

Aucune géométrie interne classique d’une particule élémentaire n’est supposée.

---

### A.23.4 \(\alpha_G\) comme quantum minimal de géométrie

$$
\boxed{\text{REJECTED}}
$$

\(\alpha_G\) est sans dimension et mesure un couplage caractéristique.

---

### A.23.5 \(R\sim1\) comme seuil universel de géométrisation

$$
\boxed{\text{REJECTED}}
$$

Une fluctuation relative d’ordre unité peut signaler l’échec d’une approximation moyenne, mais ne définit pas universellement la naissance d’une géométrie.

---

### A.23.6 Identifier directement le lapse à un objet fondamental

$$
\boxed{\text{REJECTED}}
$$

Le lapse dépend du découpage choisi.

Les observables fondamentales recherchées doivent être relationnelles/invariantes.

---

# A.24 Questions complémentaires actuellement ouvertes

Les questions suivantes restent pertinentes mais ne doivent pas être résolues avant les tests centraux de CosmoTGG.

### Q1 — Existe-t-il une véritable échelle minimale ?

$$
\boxed{\text{OPEN}}
$$

La longueur de Planck constitue une échelle naturelle, pas une preuve d’un quantum minimal de longueur.

---

### Q2 — Une géométrie continue peut-elle émerger uniquement des relations quantiques ?

$$
\boxed{\text{OPEN}}
$$

Il faut obtenir notamment :

* dimension effective ;
* voisinage/localité ;
* distances ;
* angles ;
* signature ;
* causalité ;
* courbure.

---

### Q3 — Le flot modulaire peut-il devenir le temps propre ?

$$
\boxed{\text{OPEN}}
$$

Il faut établir :

$$
s_{\rm mod}
\rightarrow
\tau_{\rm physique}
$$

sans horloge externe arbitraire.

---

### Q4 — Une échelle physique peut-elle émerger dynamiquement ?

$$
\boxed{\text{OPEN}}
$$

La transmutation dimensionnelle et les anomalies d’échelle fournissent des précédents mathématiques, mais le raccord avec une longueur ou une durée physique émergente reste à démontrer.

---

### Q5 — \(G\) peut-il être une susceptibilité collective ?

$$
\boxed{\text{OPEN}}
$$

La cible reste :

$$
\delta\mathcal G
=
\kappa_{\rm eff}
\delta\mathcal E
$$

avec :

$$
\kappa_{\rm eff}\rightarrow\kappa_*
$$

dans une limite collective universelle, puis :

$$
\boxed{
\kappa_*
\stackrel{?}{=}
\frac{8\pi G}{c^4}.
}
$$

---

### Q6 — Temps et \(G\) peuvent-ils dépendre de la même échelle émergente ?

$$
\boxed{\text{OPEN}}
$$

Une possibilité explorée est :

$$
\text{même état collectif}
\rightarrow
\begin{cases}
\text{échelle de changement}\\
\text{réponse géométrique}
\end{cases}
$$

mais aucune dérivation n’est actuellement disponible.

---

### Q7 — Comment calibrer dimensionnellement un coefficient émergent, et quel est le statut de \(c\) ?

$$
\boxed{\text{OPEN}}
$$

Avant toute comparaison entre \(\kappa_*\) et \(8\pi G/c^4\), les observables émergentes doivent recevoir une interprétation dimensionnelle physique, définie indépendamment de toute mesure gravitationnelle cible : \(\text{DIMENSIONAL\_CALIBRATION}=\text{OPEN}\) (`hypothesis.md` §13). \(c\) n'est pas utilisé comme échelle microscopique de calibration dans le modèle fondamental v0.2 ; son statut fondamental ou émergent dans une éventuelle théorie complète reste **[OPEN]**.

---

# A.25 Carte synthétique

| Idée explorée                                   | Structure mathématique connue    | Statut CosmoTGG                 |
| ----------------------------------------------- | --------------------------------- | -------------------------------- |
| Échelle quantique-gravitationnelle              | \(\ell_P,t_P,m_P\)               | référence, pas fondement        |
| Intensité gravitationnelle microscopique        | \(\alpha_G=Gm^2/\hbar c\)        | référence                       |
| Géométrie minimale relationnelle                | simplexes, Cayley–Menger         | outil potentiel                 |
| Matière comme soliton                           | Skyrme / solitons topologiques   | archivé                         |
| Énergie comme source géométrique                | \(T_{\mu\nu}\)                   | connu                           |
| Champ EM gravitant                              | \(T_{\mu\nu}^{EM}\)              | connu                           |
| Rythme d’horloge gravitationnel                 | \(d\tau=Ndt\)                    | connu                           |
| Homogénéisation statique                        | \(\Delta_hN=0\) dans le vide     | analogie utile                  |
| Temps seul \(\rightarrow\) gravité complète     | PPN, \(\gamma\)                  | écarté                          |
| Équilibre température/temps                     | Tolman–Ehrenfest                 | connu                           |
| Fluctuation relative                            | Kuo–Ford                         | connu, critère insuffisant seul |
| Corrélation des fluctuations                    | noise kernel                     | gravité stochastique            |
| Transition vers régime collectif                | Ginzburg/TGFT                    | candidat                        |
| Échelle créée par le quantique                  | RG / anomalie d’échelle          | connu                           |
| Anomalie \(\rightarrow\) temps                  | Barbour–Lostaglio–Mercati        | preuve de principe              |
| \(G\) induit                                    | Sakharov                         | preuve de principe              |
| Équilibre \(\rightarrow\) Einstein              | Jacobson                         | connu sous hypothèses           |
| État \(\rightarrow\) flot                       | Tomita–Takesaki / Connes–Rovelli | base actuelle                   |
| Intrication \(\rightarrow\) géométrie dynamique | holographie                      | connu dans cadre spécifique     |
| Structure modulaire \(\rightarrow\) courbure    | modular Berry curvature          | connu dans cadre holographique  |
| Temps + géométrie issus du même état            | —                                 | **hypothèse centrale CosmoTGG** |
| Même mécanisme \(\rightarrow G\)                | —                                 | **ouvert**                      |

---

# A.26 Références complémentaires

**[A1]** CODATA 2022, valeurs recommandées des constantes fondamentales : unités de Planck et constantes fondamentales.

**[A2]** Kuo, C.-I. & Ford, L. H. (1993), *Semiclassical Gravity Theory and Quantum Fluctuations*, Physical Review D 47, 4510, arXiv:gr-qc/9304008. DOI 10.1103/PhysRevD.47.4510.

**[A3]** Hu, B. L. & Verdaguer, E. (2008), *Stochastic Gravity: Theory and Applications*, Living Reviews in Relativity 11, 3.

**[A4]** Tolman, R. C. & Ehrenfest, P. (1930), *Temperature Equilibrium in a Static Gravitational Field*, Physical Review 36, 1791. DOI 10.1103/PhysRev.36.1791.

**[A5]** Rovelli, C. & Smerlak, M. (2011), *Thermal time and the Tolman-Ehrenfest effect: temperature as the "speed of time"*, arXiv:1005.2985.

**[A6]** Marchetti, L., Oriti, D., Pithis, A. G. A. & Thürigen, J. (2023), *Phase transitions in TGFT: a Landau-Ginzburg analysis of Lorentzian quantum geometric models*, JHEP 02 (2023) 074.

**[A7]** Barbour, J., Lostaglio, M. & Mercati, F. (2013), *Scale Anomaly as the Origin of Time*, General Relativity and Gravitation 45, 911–938, arXiv:1301.6173.

**[A8]** Visser, M. (2002), *Sakharov's Induced Gravity: a Modern Perspective*, Modern Physics Letters A 17, 977–992, arXiv:gr-qc/0204062.

**[A9]** Connes, A. & Rovelli, C. (1994), *Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories*, Classical and Quantum Gravity 11, 2899–2917, arXiv:gr-qc/9406019.

**[A10]** Jacobson, T. (1995), *Thermodynamics of Spacetime: The Einstein Equation of State*, Physical Review Letters 75, 1260, arXiv:gr-qc/9504004.

**[A11]** Blanco, D. D., Casini, H., Hung, L.-Y. & Myers, R. C. (2013), *Relative Entropy and Holography*, arXiv:1305.3182.

**[A12]** Faulkner, T., Guica, M., Hartman, T., Myers, R. C. & Van Raamsdonk, M. (2014), *Gravitation from Entanglement in Holographic CFTs*, JHEP 03 (2014) 051, arXiv:1312.7856.

**[A13]** Jacobson, T. (2016), *Entanglement Equilibrium and the Einstein Equation*, Physical Review Letters 116, 201101, arXiv:1505.04753.

**[A14]** Czech, B., de Boer, J., Ge, D. & Lamprou, L. (2019), *A Modular Sewing Kit for Entanglement Wedges*, JHEP 11 (2019) 094, arXiv:1903.04493.

**[A15]** Czech, B., Lamprou, L., McCandlish, S. & Sully, J. (2018), *Modular Berry Connection for Entangled Subregions in AdS/CFT*, Physical Review Letters 120, 091601, arXiv:1712.07123. DOI 10.1103/PhysRevLett.120.091601.

**[A16]** Umegaki, H. (1962), *Conditional expectation in an operator algebra, IV (Entropy and information)*, Kodai Mathematical Seminar Reports 14(2), 59–85. DOI 10.2996/kmj/1138844604.

**[A17]** Araki, H. (1976), *Relative Entropy of States of von Neumann Algebras*, Publications of the Research Institute for Mathematical Sciences 11(3), 809–833. DOI 10.2977/prims/1195191148.

**[A18]** Page, D. N. & Wootters, W. K. (1983), *Evolution without evolution: Dynamics described by stationary observables*, Physical Review D 27, 2885. DOI 10.1103/PhysRevD.27.2885.

**[A19]** Höhn, P. A., Smith, A. R. H. & Lock, M. P. E. (2021), *Trinity of relational quantum dynamics*, Physical Review D 104, 066001, arXiv:1912.00033. DOI 10.1103/PhysRevD.104.066001.

---

## A.27 Règle d’utilisation de cette annexe

Cette annexe constitue une **mémoire de recherche**, pas un ensemble d’hypothèses imposées à CosmoTGG.

Lorsqu’une nouvelle idée apparaît, la première opération doit être :

$$
\boxed{
\text{nouvelle intuition}
\rightarrow
\text{recherche dans cette cartographie}
\rightarrow
\text{recherche bibliographique}
}
$$

avant :

$$
\boxed{
\text{nouveau modèle ou nouvelle équation}.
}
$$

Une piste archivée peut être réactivée uniquement si un nouveau résultat établit qu'elle apporte une information qui n'est pas déjà contenue dans les structures connues.

La priorité reste donc :

$$
\boxed{
\text{identifier la frontière de la littérature avant de construire au-delà}.
}
$$
