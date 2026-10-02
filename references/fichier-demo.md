# Le fichier de démonstration

**999 établissements du Loir-et-Cher (41), relevés le 28/09/2026.** C'est un
vrai fichier Scalon, produit comme test pour une entreprise qui vend aux
garages indépendants, ceux que le métier appelle les **MRA** (mécaniciens
réparateurs automobiles).

👉 **[Faire ta copie du fichier](https://docs.google.com/spreadsheets/d/1B3-JFoqKLBg3WmGM3EKy5pjQ0Q6-nPBeKiDvNFQWbDE/copy)**
(Google Sheets, un clic, la copie t'appartient)

Le fichier ne vaut que pour cette cible. Si tu vends aux restaurants, aux
salons de coiffure ou aux artisans du bâtiment, sers-toi de lui pour monter ta
machine, puis demande ton propre échantillon sur ton marché :
[30 minutes avec Valentin](https://cal.com/valentin-morterol-ezc5qn/30min).

---

## La question posée au fichier

> Dans le Loir-et-Cher, quels établissements sont réellement des garages de
> réparation automobile, avec un atelier ouvert au public ?

Le point de départ est large, volontairement : tout ce qui, dans le
département, est déclaré ou se présente comme une activité automobile. Puis
chaque établissement est regardé un par un.

| Verdict | Établissements | Ce que ça veut dire |
|---|---|---|
| **Qualifié** | 229 | Garage de réparation en activité, atelier ouvert au public |
| **Non qualifié** | 298 | Autre métier, ou pas d'atelier ouvert. Le motif est écrit |
| **Indéterminé** | 472 | Rien de public ne confirme l'activité réelle |
| **Total** | **999** | |

Moins d'un établissement sur quatre est une cible. Les 770 autres sont le
temps que ton équipe perd aujourd'hui, au téléphone ou sur une carte.

## Pourquoi un code d'activité ne suffit pas

Le code NAF des garages est le 45.20A, « entretien et réparation de véhicules
automobiles légers ». Dans ce fichier :

- **372** établissements portent ce code. **145** sont des garages qualifiés.
- **84** garages qualifiés sur 229 sont déclarés sous **un autre code**, dont
  63 en 45.11Z (commerce de voitures).

Si tu filtres une base légale sur le 45.20A, tu appelles 227 établissements
qui ne sont pas des garages confirmés, et tu rates plus d'un tiers des vrais.

## Les colonnes qui font le travail

L'onglet **Légende** du fichier définit chaque colonne. Les cinq qui comptent
pour prospecter :

### `Statut` et `Raison du statut`

Le verdict, et la phrase qui le fonde. C'est la raison qui rend le fichier
utilisable : ton commercial sait pourquoi il appelle avant de décrocher, et tu
peux contester un verdict ligne par ligne.

| Statut | Exemples de raisons, telles qu'écrites dans le fichier |
|---|---|
| Qualifié | « Garage indépendant, mécanique, carrosserie et tôlerie » |
| Qualifié | « Garage AD, entretien et réparation toutes marques » |
| Non qualifié | « Centre de contrôle technique, pas un garage de réparation. » |
| Non qualifié | « Carrosserie seule, pas de mécanique » |
| Non qualifié | « Mandataire automobile, vente de véhicules sans atelier » |
| Indéterminé | « Connu du seul registre : aucune fiche publique ne confirme l'activité » |
| Indéterminé | « Aucun avis depuis plus de 3 ans : fermeture probable. » |

### `Score Ciblage Scalon`

Un entier de 0 à 100 : la probabilité que l'établissement soit vraiment dans la
cible, estimée sur l'ensemble de son dossier.

| | Score le plus bas | Score médian | Score le plus haut |
|---|---|---|---|
| Qualifié | 30 | 93 | 97 |
| Non qualifié | 3 | 4 | 14 |

158 des 229 qualifiés sont à 90 ou plus. Le score sert à **ordonner** les
qualifiés entre eux : on appelle le 96 avant le 62.

### `Type d'établissement`

| Type | Nombre | Qui c'est |
|---|---|---|
| **Garage indépendant (MRA)** | 164 | L'atelier indépendant, sous enseigne de réseau ou non |
| **Agent de marque** | 38 | Le réseau secondaire d'un constructeur |
| **Concession** | 27 | Le réseau primaire, avec atelier |

### `Réseau ou marque`

L'enseigne affichée (AD, Motrio, Autoprimo, Top Garage, Eurorepar, Precisium…)
ou la marque représentée. Sur les 164 MRA, **92 n'affichent aucune enseigne**
et 72 appartiennent à un réseau.

Pour quelqu'un qui vend aux garages, cette colonne change tout. Un garage sous
enseigne achète déjà, en partie, par la centrale de son réseau. Un indépendant
sans enseigne décide seul.

### `Volume d'activité` et `Zone`

- `Volume d'activité` : Faible, Moyen ou Fort, comparé aux garages de France.
  Sur les 229 qualifiés : 63 Fort, 103 Moyen, 62 Faible.
- `Zone` : rural, petite ville, périurbain, ville moyenne. 151 des 229
  qualifiés sont en zone rurale.

## Les colonnes pour rapprocher avec ton CRM

`SIRET` et `Téléphone` sont les deux clés. Le téléphone est présent sur 226 des
229 qualifiés, au format international (`+33…`). Voir
[`cles-de-dedoublonnage.md`](cles-de-dedoublonnage.md).

## Ce que le fichier ne dit pas

Il dit pourquoi un établissement est retenu ou écarté. Il ne dit pas si son
patron a besoin de ton produit cette semaine : ça, c'est ton appel.

Et un `Indéterminé` n'est pas un `Non qualifié`. C'est une ligne sur laquelle
rien de public ne permet de trancher. On ne l'appelle pas en premier, on ne la
supprime pas non plus.
