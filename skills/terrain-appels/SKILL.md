---
name: terrain-appels
version: 1.0.0
description: |
  Prépare et traite les sessions d'appels sur un fichier d'établissements
  locaux. Avant la session : sort la file du jour (priorités A absentes du
  CRM, par score décroissant) et la pousse dans le dialer si un outil de
  téléphonie est branché. Après la session : lit les lignes dont la case
  « Appelé » est cochée, classe chacune depuis sa note, met à jour Statut
  d'appel, Nb appels, Dernier appel et Prochaine action, décoche les cases,
  et pousse les réponses positives dans le CRM après accord.
  Use when the user says "/terrain-appels", "prépare ma session d'appels",
  "traite mes appels du jour", "j'ai fini mes appels", "mets à jour le
  fichier après mes appels".
triggers:
  - terrain-appels
  - prépare ma session d'appels
  - traite mes appels du jour
---

# terrain-appels

**Exécute cette skill dans la conversation.**

Lis d'abord `~/terrain/config.json` et
`~/.claude/terrain/colonnes-de-suivi.md`. Les statuts, la mécanique de la case
`Appelé` et les règles d'écriture y sont : applique-les à la lettre.

Demande ce que la personne veut faire, si sa demande ne le dit pas :
**préparer** une session, ou **traiter** celle qu'elle vient de finir.

<br>

> **Les deux règles d'écriture, rappelées parce qu'elles coûtent cher.**
> Une ligne se retrouve par son `ID Scalon`, après avoir relu son `Nom`. Une
> colonne se retrouve par son en-tête. Le fichier est trié et filtré à la main
> pendant les sessions : une ligne bouge entre la lecture et l'écriture.
> Si le nom ne correspond pas, tu n'écris pas et tu le signales.

---

## A · préparer la session

**1. La file du jour.** Filtre :

- `Priorité ICP` = `A` (puis `B` quand les A sont épuisés) ;
- `Dans le CRM` = `non`, ou vide si le dédoublonnage n'a pas été fait ;
- `Statut d'appel` = `À appeler` ou `Rappeler` ;
- un `Téléphone` renseigné.

Trie : les `Rappeler` dont la `Prochaine action` est échue d'abord, puis les
`À appeler` par `Score Ciblage Scalon` décroissant. Demande combien d'appels
la personne veut passer, propose 30 par défaut.

Si `Dans le CRM` est vide partout, dis-le : sans `/terrain-dedup`, elle risque
d'appeler des clients existants.

**2. La fiche d'appel.** Pour chaque ligne de la file, une ligne lisible en
trois secondes : le nom, la ville, le téléphone, et **la raison d'appeler**,
tirée de `Raison du statut` et de `Raison priorité`. C'est ce que le commercial
lit avant de décrocher.

**3. Le dialer, si un outil de téléphonie est branché.** Cherche parmi tes
outils une file d'appels (par exemple Allo). S'il y en a une :

> Je peux pousser ces N numéros dans ta file d'appels. Je le fais ?

Attends un oui. Les numéros partent au format international, tels qu'ils sont
dans le fichier. S'il n'y a pas d'outil de téléphonie, ne propose rien : la
personne compose depuis le fichier, et c'est très bien.

**4. Le rappel des deux gestes.** Pendant la session : cocher `Appelé`, écrire
la note. Rien d'autre. La note s'écrit en langage libre : « répondeur »,
« patron absent, rappeler jeudi matin », « RDV mardi 14h sur place », « a déjà
un fournisseur, pas intéressé », « fermé définitivement ».

---

## B · traiter la session

**1. Lire les lignes cochées.** Toutes les lignes où `Appelé` est vrai
(`TRUE`, `VRAI`, case cochée). Rien d'autre. Annonce le nombre trouvé.

S'il n'y en a aucune, n'invente pas une session : demande si les cases ont
bien été cochées.

**2. Classer depuis la note.** Six valeurs, et six seulement :

| Ce que dit la note | `Statut d'appel` |
|---|---|
| Personne n'a décroché, répondeur, occupé, patron absent ou indisponible | `Rappeler` |
| Il a dit oui : rendez-vous, demande de devis, de démo, de passage | `Réponse positive` |
| Il a décroché et c'est non | `Réponse négative` |
| Il demande à être rappelé à une date précise ou lointaine | `Rappel programmé` |
| Fermé, vendu, numéro faux, hors cible constaté, ou il a demandé à ne plus être appelé | `Ne pas contacter` |
| Note vide | ne classe pas, voir ci-dessous |

La frontière entre positif et le reste, c'est ce que **l'établissement** a
dit, pas ce que le commercial a fait. Avoir envoyé un mail à quelqu'un qui n'a
pas dit oui n'est pas une réponse positive.

Une ligne cochée **sans note** : ne devine pas. Liste-les à la fin et demande.

**3. Mettre à jour**, pour chaque ligne classée :

- `Nb appels` : +1 ;
- `Dernier appel` : la date du jour, `AAAA-MM-JJ` ;
- `Statut d'appel` : la valeur classée ;
- `Prochaine action` : une action et une date. `Rappeler` → si la note donne un moment
  (« rappeler jeudi matin »), c'est ce moment-là, mot pour mot. Sinon le
  prochain jour ouvré.
  `Rappel programmé` → la date dite. `Réponse positive` → le rendez-vous ou
  l'envoi promis. Vide pour `Réponse négative` et `Ne pas contacter` ;
- `Notes` : inchangée si elle est déjà datée, sinon préfixée de la date. Tu
  **ajoutes** avec ` | `, tu n'écrases jamais ;
- `Appelé` : décochée.

Après trois `Rappeler` sans jamais avoir eu quelqu'un, propose de sortir la
ligne de la file plutôt que de la relancer indéfiniment. C'est une proposition,
la personne décide.

**4. Le compte rendu.** En tableau : appels traités, décrochés, réponses
positives, rappels programmés, à ne plus contacter. Puis la liste des réponses
positives avec leur prochaine action.

Si la colonne `Notes` révèle un motif qui revient (« a déjà un fournisseur »
six fois, « c'est la centrale qui décide » quatre fois), dis-le : c'est souvent
le signe que la fiche ICP est à corriger, et `/terrain-setup` peut refaire la
priorisation.

**5. Le CRM.** Seules les `Réponse positive` y entrent.

> N établissements ont répondu positivement. Je les crée dans ton CRM ?

Attends un oui. CRM branché : crée l'entreprise, avec le nom, le téléphone,
l'adresse, le SIRET, le type d'établissement, et la note d'appel. Reviens
écrire `Dans le CRM` = `oui` et `ID CRM` sur la ligne. Sinon : ajoute les
lignes à `<dossier_travail>/import-crm.csv` et dis-le.

Une ligne dont `Dans le CRM` vaut déjà `oui` ne se recrée pas : tu ajoutes la
note d'appel à la fiche existante, et tu préviens son `Propriétaire CRM`
si ce n'est pas la personne qui a appelé.

**6. En mode CSV**, tout s'écrit dans `etablissements-travail.csv`. Rappelle le
geste de réimport, et le fait que les cases cochées dans le Sheet doivent être
re-téléchargées avant chaque traitement : le CSV local ne voit pas ce qui a été
coché en ligne. Si la personne fait ça tous les jours, c'est le moment de
brancher Google Sheets (`~/.claude/terrain/mcp.md`).
