# Le fichier exemple

**100 établissements fictifs, en données synthétiques.** Le fichier a la
structure exacte d'un fichier Scalon, colonne pour colonne, mais aucune ligne
n'est réelle : communes inventées, codes postaux en 99, téléphones pris dans la
tranche réservée à la fiction, SIRET qui ne passent pas le contrôle légal,
sites en `.example`.

👉 **[Faire ta copie du fichier](https://docs.google.com/spreadsheets/d/1uicRji1utNc1jKg2r9TpVsJRJj3yWVtMfRn8QPTYwiI/copy)**
(Google Sheets, un clic, la copie t'appartient)

Il sert à monter la machine et à voir tourner les trois skills. Pour la faire
tourner sur de vrais établissements, il te faut un fichier sur ton marché :
[30 minutes avec Valentin](https://cal.com/valentin-morterol-ezc5qn/30min),
l'échantillon de 100 établissements est gratuit.

---

## D'où viennent ses proportions

Le fichier exemple reproduit, en petit, un test réel : un département entier
passé au crible pour une entreprise qui vend aux garages indépendants, ceux
que le métier appelle les **MRA** (mécaniciens réparateurs automobiles). La
question posée :

> Dans ce département, quels établissements sont réellement des garages de
> réparation automobile, avec un atelier ouvert au public ?

| Verdict | Test réel | Fichier exemple | Ce que ça veut dire |
|---|---|---|---|
| **Qualifié** | 229 | 20 | Garage de réparation en activité, atelier ouvert au public |
| **Non qualifié** | 427 | 38 | Autre métier, ou pas d'atelier ouvert. Le motif est écrit |
| **Indéterminé** | 472 | 42 | Rien de public ne confirme l'activité réelle |
| **Total** | **1 128** | **100** | |

Un établissement sur cinq est une cible, dans le test comme dans l'exemple.

## Pourquoi un code d'activité ne suffit pas

Le code NAF des garages est le 45.20A, « entretien et réparation de véhicules
automobiles légers ».

| | Test réel | Fichier exemple |
|---|---|---|
| Établissements qui portent le 45.20A | 402 | 36 |
| dont garages qualifiés | 145 | 13 |
| Garages qualifiés déclarés sous un autre code | 84 sur 229 | 7 sur 20 |

Si tu filtres une base légale sur le 45.20A, tu appelles une majorité
d'établissements qui ne sont pas des garages confirmés, et tu rates plus d'un
tiers des vrais.

## Les colonnes qui font le travail

L'onglet **Légende** du fichier définit chaque colonne. Celles qui comptent
pour prospecter :

### `Statut` et `Raison du statut`

Le verdict, et la phrase qui le fonde. C'est la raison qui rend le fichier
utilisable : ton commercial sait pourquoi il appelle avant de décrocher, et tu
peux contester un verdict ligne par ligne.

| Statut | Exemples de raisons, telles qu'écrites dans le fichier |
|---|---|
| Qualifié | « Garage indépendant, mécanique et carrosserie toutes marques, atelier ouvert, avis récents. » |
| Qualifié | « Garage AD, entretien et réparation toutes marques, atelier ouvert. » |
| Non qualifié | « Centre de contrôle technique, pas un garage de réparation. » |
| Non qualifié | « Carrosserie seule, pas de mécanique. » |
| Non qualifié | « Mandataire automobile, vente de véhicules sans atelier. » |
| Indéterminé | « Connu du seul registre : aucune fiche publique ne confirme l'activité. » |
| Indéterminé | « Aucun avis depuis plus de 3 ans : fermeture probable. » |

### `Score Ciblage Scalon`

Un entier de 0 à 100 : la probabilité que l'établissement soit vraiment dans la
cible, estimée sur l'ensemble de son dossier. Dans le fichier exemple, les
qualifiés vont de 62 à 97 (médiane 93), les non qualifiés de 2 à 14.

Le score sert à **ordonner** les qualifiés entre eux : on appelle le 96 avant
le 62.

### `Type d'établissement`

| Type | Dans le fichier exemple | Qui c'est |
|---|---|---|
| **Garage indépendant (MRA)** | 14 | L'atelier indépendant, sous enseigne de réseau ou non |
| **Agent de marque** | 3 | Le réseau secondaire d'un constructeur |
| **Concession** | 3 | Le réseau primaire, avec atelier |

### `Réseau ou marque`

L'enseigne affichée (AD, Motrio, Top Garage, Eurorepar, Precisium…) ou la
marque représentée. Sur les 14 MRA du fichier exemple, **8 n'affichent aucune
enseigne** et 6 appartiennent à un réseau. Dans le test réel : 92 sur 164.

Pour quelqu'un qui vend aux garages, cette colonne change tout. Un garage sous
enseigne achète déjà, en partie, par la centrale de son réseau. Un indépendant
sans enseigne décide seul.

### `Volume d'activité` et `Zone`

- `Volume d'activité` : Faible, Moyen ou Fort, comparé aux garages de France.
  Sur les 20 qualifiés : 6 Fort, 9 Moyen, 5 Faible.
- `Zone` : rural, petite ville, périurbain, ville moyenne. 14 des 20 qualifiés
  sont en zone rurale.

## Les colonnes pour rapprocher avec ton CRM

`SIRET` et `Téléphone` sont les deux clés. Le téléphone est présent sur les 20
qualifiés, au format international (`+33…`). Les garages sous enseigne ont pour
site une page du site de leur réseau : c'est le piège du domaine partagé,
visible dans le fichier. Voir
[`cles-de-dedoublonnage.md`](cles-de-dedoublonnage.md).

## Ce que le fichier ne dit pas

Il dit pourquoi un établissement est retenu ou écarté. Il ne dit pas si son
patron a besoin de ton produit cette semaine : ça, c'est ton appel.

Et un `Indéterminé` n'est pas un `Non qualifié`. C'est une ligne sur laquelle
rien de public ne permet de trancher. On ne l'appelle pas en premier, on ne la
supprime pas non plus.

Les numéros du fichier exemple ne mènent nulle part : ne les appelle pas, et ne
les importe pas dans ton vrai CRM.
