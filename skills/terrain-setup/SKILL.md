---
name: terrain-setup
version: 1.0.0
description: |
  Monte une machine de prospection sur un fichier d'établissements locaux
  (garages, restaurants, commerces, artisans : ceux qui ne sont pas sur
  LinkedIn). Interroge l'utilisateur sur son client idéal, lit le fichier et
  sa légende, repriorise chaque établissement par rapport à cet ICP, ajoute
  les colonnes de suivi d'appel, puis enchaîne sur le dédoublonnage CRM.
  Fonctionne en direct sur Google Sheets, ou sur un export CSV sans aucune
  connexion.
  Use when the user says "/terrain-setup", "configure mon fichier de
  prospection", "je viens d'installer le blueprint no linkedin", "priorise
  mon fichier d'établissements", or runs this skill for the first time.
triggers:
  - terrain-setup
  - configure mon fichier de prospection
  - priorise mon fichier
---

# terrain-setup

**Exécute cette skill dans la conversation, ne la délègue pas à un subagent.**
Elle est faite d'aller-retours avec l'utilisateur.

Elle se lance une fois par fichier. À la fin, l'utilisateur a un fichier où
chaque établissement porte **sa** priorité, les colonnes pour suivre ses
appels, et une file d'appels prête.

## Ce que tu as sous la main

`install.sh` a déposé ceci dans `~/.claude/terrain/` :

| Fichier | À quoi il sert |
|---|---|
| `fichier-demo.md` | Ce que contient le fichier exemple, et le lien pour le copier |
| `colonnes-de-suivi.md` | Les douze colonnes à ajouter, les statuts, les règles d'écriture |
| `cles-de-dedoublonnage.md` | Les clés de rapprochement CRM et les exports par CRM |
| `mcp.md` | Les commandes pour brancher Sheets, le CRM, Notion et Allo |
| `scripts/dedup.py` | Le rapprochement fichier / CRM, Python standard |
| `prompts/` | Les mêmes étapes, en prompts à coller |

**Lis ces fichiers au moment où tu en as besoin.** Ne reconstitue rien de
mémoire. Si l'un manque, dis-le et propose de relancer l'installation.

<br>

> **Les trois règles qui gouvernent cette skill.**
> 1. **Les colonnes d'origine du fichier sont en lecture seule.** Tu ajoutes
>    des colonnes à droite, tu ne modifies jamais `Statut`, `Raison du statut`,
>    `Score Ciblage Scalon` ni aucune autre colonne livrée.
> 2. **Tu désignes une colonne par son en-tête et une ligne par son
>    `ID Scalon`.** Jamais par une lettre, jamais par un numéro de ligne.
>    Relis l'en-tête avant chaque écriture.
> 3. **Tu n'inventes rien sur un établissement.** La priorité se déduit des
>    colonnes du fichier et de l'ICP de l'utilisateur, de rien d'autre.

---

## Les six phases

| Phase | Ce qu'on fait | Arrêt |
|---|---|---|
| 1 | Trouver le fichier et choisir le mode de travail | **Il choisit Sheets ou CSV** |
| 2 | Lire le fichier et sa légende, en rendre compte | aucun |
| 3 | Définir son ICP | **Il valide la fiche ICP** |
| 4 | Repriorisation : `Priorité ICP` et `Raison priorité` | **Il valide le premier lot de 50** |
| 5 | Ajouter les colonnes de suivi et la vue d'appel | aucun |
| 6 | Passer la main | aucun |

---

## Phase 1 · le fichier et le mode de travail

Demande d'abord :

> Sur quel fichier on travaille ?
> - **le fichier exemple** (100 établissements fictifs, en données
>   synthétiques, qualifiés pour quelqu'un qui vend aux garages indépendants)
> - **ton échantillon Scalon**, si tu en as reçu un
> - **un autre fichier d'établissements** que tu as déjà

**Fichier exemple.** Lis `~/.claude/terrain/fichier-demo.md` et donne
le lien de copie qu'il contient. La personne clique, obtient sa copie dans son
Google Drive, et te donne l'URL de **sa copie**. Ne travaille jamais sur
l'original : tu n'y as pas accès en écriture, et c'est voulu.

**Autre fichier.** Il doit avoir au moins un nom, un téléphone et un code
postal par ligne. S'il n'a pas d'identifiant stable, crée une colonne `ID`
(`ET-0001`, `ET-0002`…) avant toute autre écriture, et utilise-la partout où
cette skill dit `ID Scalon`. S'il n'a ni verdict ni score, dis-le : les phases
3 et 4 feront le tri, mais sur moins de matière.

Puis regarde ce qui est branché. Cherche parmi tes outils un outil Google
Sheets capable de **lire et d'écrire** des cellules.

- **S'il y en a un : mode Sheets.** Tu travailles en direct sur la copie.
- **S'il n'y en a pas : propose le choix**, sans pousser.

> Je n'ai pas d'accès Google Sheets ici. Deux possibilités :
> - **Brancher Google Drive et Google Sheets à Claude**, quinze minutes une
>   fois pour toutes. Les étapes sont dans `~/.claude/terrain/mcp.md`. Je
>   travaille ensuite directement dans ta copie.
> - **Télécharger le fichier, tout de suite.** Dans ta copie : Fichier →
>   Télécharger → Microsoft Excel (.xlsx), un seul fichier avec tous les
>   onglets. Ou en CSV, une fois sur l'onglet Établissements, une fois sur
>   l'onglet Légende. Donne-moi le ou les chemins. Je travaille en local et je
>   te rends un fichier à réimporter. Aucune connexion, cinq minutes.

Si la personne donne un `.xlsx`, convertis d'abord chaque onglet utile en CSV
dans le dossier de travail (un `.xlsx` est une archive zip de fichiers XML :
Python standard suffit, `openpyxl` si elle est installée), en gardant les
SIRET et les téléphones en texte. Le reste de la skill travaille sur ces CSV.

Crée le dossier de travail `~/terrain/` et écris le choix dans
`~/terrain/config.json`. Tout ce qui appartient à l'utilisateur vit dans ce
dossier (sa configuration, sa fiche ICP, ses exports), jamais dans
`~/.claude/` :

```json
{
  "mode": "sheets",
  "sheet_url": "https://docs.google.com/spreadsheets/d/…",
  "onglet_etablissements": "Établissements",
  "csv_etablissements": null,
  "dossier_travail": "~/terrain"
}
```

En mode CSV, `mode` vaut `"csv"` et `csv_etablissements` porte le chemin. **Tu ne modifies jamais le CSV d'origine** : tu
écris `~/terrain/etablissements-travail.csv`, et c'est lui qui vit ensuite.

## Phase 2 · lire le fichier

Lis l'onglet `Légende` **en entier** avant de regarder une seule ligne de
données. Elle définit chaque colonne et son vocabulaire fermé. Sans elle tu
devines, et tu devines mal.

Puis lis l'onglet des établissements et rends compte, en dix lignes au plus :

- le nombre de lignes ;
- la répartition de la colonne de verdict (`Statut` dans un fichier Scalon) ;
- parmi les qualifiés, la répartition du type d'établissement ;
- la fourchette et la médiane du score, par verdict ;
- le taux de remplissage du téléphone et du SIRET sur les qualifiés ;
- trois exemples de `Raison du statut`, un par verdict, cités mot pour mot.

Sur un gros fichier, calcule avec un script plutôt que de lire toutes les
lignes dans la conversation.

Termine par une phrase qui dit ce que ces chiffres changent pour quelqu'un qui
prospecte. Par exemple, sur le fichier exemple : 20 qualifiés sur
100, donc quatre appels sur cinq évités avant d'avoir décroché.

## Phase 3 · définir son ICP

**Ne priorise rien avant cette phase.** Le fichier dit ce qu'est chaque
établissement. Il ne dit pas lequel est le client de cette personne-là.

Demande du contexte, en laissant le choix de la forme :

> Pour prioriser, j'ai besoin de savoir à qui tu vends. Le plus rapide pour
> toi : l'URL de ton site, un copier-coller de ta plaquette, ou trois phrases.

S'il donne une URL, lis-la. Puis pose ces questions **une par une**, en
attendant chaque réponse :

1. Tes trois meilleurs clients actuels dans ce type d'établissement : qu'est-ce
   qu'ils ont en commun ? Leur taille, leur enseigne, leur zone, leur volume.
2. Et un client que tu regrettes d'avoir signé, ou un type d'établissement que
   tu appelles pour rien ?
3. L'appartenance à un réseau ou à une enseigne change-t-elle quelque chose ?
   Un affilié achète souvent par la centrale de son réseau.
4. Y a-t-il une taille en dessous de laquelle ce n'est pas rentable, ou
   au-dessus de laquelle la décision ne se prend plus sur place ?
5. Ta zone : tout le fichier, ou seulement une partie ?

Écris ensuite la **fiche ICP**, en utilisant uniquement des colonnes qui
existent dans le fichier. Pour chaque critère : la colonne, les valeurs
retenues, et ce que le critère vaut.

Exemple de forme, pour quelqu'un qui vend des pièces aux garages
indépendants (c'est un exemple de format, pas un contenu à reprendre) :

```
Fiche ICP

Cible : garages indépendants qui décident seuls de leurs achats.

A · on appelle en premier
  Statut = Qualifié
  Type d'établissement = Garage indépendant (MRA)
  Réseau ou marque = vide (aucune enseigne)
  Volume d'activité = Moyen ou Fort

B · ensuite
  Statut = Qualifié, Type = Garage indépendant (MRA)
  et (sous enseigne de réseau, ou Volume d'activité = Faible)

C · en dernier
  Statut = Qualifié, Type = Agent de marque

Hors cible
  Statut = Non qualifié
  Type = Concession (achète par le constructeur)

À vérifier
  Statut = Indéterminé avec un téléphone
```

**Arrêt.** Montre la fiche et le nombre de lignes que chaque niveau donnerait
sur le fichier. Si A contient moins de 2 % ou plus de la moitié des
qualifiés, le critère est mal réglé : dis-le et propose l'ajustement. Attends un accord explicite, puis enregistre la
fiche dans `~/terrain/icp.md`.

## Phase 4 · repriorisation

Ajoute deux colonnes à droite du fichier : `Priorité ICP` et `Raison priorité`.

`Priorité ICP` prend cinq valeurs et cinq seulement : `A`, `B`, `C`,
`À vérifier`, `Hors cible`.

`Raison priorité` est une phrase courte qui cite le critère décisif, dans les
mots du fichier : « MRA sans enseigne, volume Fort », « Sous enseigne AD »,
« Concession : achète par le constructeur ». Jamais « correspond à l'ICP ».

Trois garde-fous :

- Une ligne `Non qualifié` est toujours `Hors cible`. Tu ne requalifies pas un
  établissement que le fichier a écarté avec un motif.
- Une ligne `Indéterminé` n'est jamais `A`, `B` ou `C`. Elle est `À vérifier`
  si elle a un téléphone, `Hors cible` sinon.
- À priorité égale, c'est `Score Ciblage Scalon` qui ordonne. Tu ne le recopies
  pas, tu ne le modifies pas, tu tries dessus.

**Travaille d'abord sur 50 lignes**, prises parmi les qualifiés (toutes, si le
fichier en compte moins de 50, comme le fichier exemple), et montre-les en
tableau : nom, type, réseau, volume, priorité, raison.

**Arrêt.** C'est le moment le plus important de la skill. Si tu as mal compris
la cible, ça se voit là, en trente secondes. Demande :

> Regarde ces lignes. Y en a-t-il une que tu aurais classée autrement ?

S'il corrige, c'est la fiche ICP qui est fausse, pas la ligne : corrige la
fiche, réécris `~/terrain/icp.md`, relance sur les mêmes 50. Quand il valide, applique à
tout le fichier et donne le compte par niveau.

En mode Sheets, écris par lots, en retrouvant chaque ligne par son
`ID Scalon`. En mode CSV, écris dans `etablissements-travail.csv`.

## Phase 5 · les colonnes de suivi

Lis `~/.claude/terrain/colonnes-de-suivi.md` et applique-le à la lettre.

Ajoute, à droite : `Dans le CRM`, `Clé de rapprochement`, `ID CRM`,
`Propriétaire CRM`, `Appelé`, `Statut d'appel`, `Nb appels`, `Dernier appel`,
`Prochaine action`, `Notes`.

Initialise :

- `Statut d'appel` = `À appeler` sur les lignes `A`, `B`, `C` ; vide ailleurs ;
- `Nb appels` = 0 sur les mêmes lignes ;
- `Appelé` décoché partout.

En mode Sheets, pose les mises en forme : ligne d'en-tête et deux premières
colonnes figées, listes déroulantes sur `Priorité ICP`, `Dans le CRM` et
`Statut d'appel`, cases à cocher sur `Appelé`, filtre sur l'en-tête. Si ton
outil Sheets ne sait pas poser une mise en forme, dis laquelle et donne le
geste à faire à la main (Insertion → Case à cocher ; Données → Validation des
données).

En mode CSV, dis-le clairement : les cases à cocher et les listes déroulantes
se poseront après le réimport. `Appelé` contient `FALSE`, que Google Sheets
transforme en case en un clic (sélectionner la colonne, Insertion → Case à
cocher).

## Phase 6 · passer la main

Récapitule en cinq lignes : le fichier, le nombre de lignes par priorité, la
file d'appels du jour (les `A`, triées par score décroissant), et où trouver la
fiche ICP.

En mode CSV, donne le chemin de `etablissements-travail.csv` et le geste de
réimport : dans le Sheet, Fichier → Importer → Importer → « Remplacer la
feuille actuelle ».

Puis propose la suite, sans la lancer d'office :

> Deux choses à faire maintenant :
> - **`/terrain-dedup`** : je compare le fichier à ton CRM et je te dis combien
>   de ces établissements tu n'avais pas. C'est ce qui évite d'appeler un
>   client existant.
> - **`/terrain-appels`**, ce soir après ta première session : je lis les cases
>   cochées et tes notes, je classe et je mets à jour.

Si la personne travaillait sur le fichier exemple, dis-lui franchement que la
machine est montée mais que ces établissements sont fictifs : leurs numéros ne
mènent nulle part, il ne faut ni les appeler ni les importer dans un vrai CRM.
Donne le lien pour demander un échantillon de 100 vrais établissements sur son
marché : https://cal.com/valentin-morterol-ezc5qn/30min
