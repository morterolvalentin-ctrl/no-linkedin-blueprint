---
name: terrain-dedup
version: 1.0.0
description: |
  Rapproche un fichier d'établissements du CRM de l'utilisateur, pour savoir
  lesquels il a déjà et lesquels sont nouveaux. Quatre clés dans l'ordre :
  SIRET, téléphone normalisé, domaine du site, nom + code postal. Écrit le
  verdict dans le fichier, produit le compte de ce que le CRM n'avait pas, et
  n'importe jamais rien dans le CRM sans accord explicite. Fonctionne avec un
  export CSV de n'importe quel CRM, ou en direct si le CRM est branché à
  Claude. Propose un CRM de démonstration pour tester sans CRM.
  Use when the user says "/terrain-dedup", "dédoublonne avec mon CRM",
  "compare le fichier à mon HubSpot", "lesquels j'ai déjà", "combien de
  nouveaux dans ce fichier".
triggers:
  - terrain-dedup
  - dédoublonne avec mon CRM
  - compare le fichier à mon CRM
---

# terrain-dedup

**Exécute cette skill dans la conversation.** Elle a deux arrêts où
l'utilisateur valide.

Lis d'abord `~/terrain/config.json` (le fichier, le mode de travail) et
`~/.claude/terrain/cles-de-dedoublonnage.md` (les clés, les pièges, les exports
par CRM). Si `config.json` n'existe pas, `/terrain-setup` n'a pas tourné :
propose de le lancer, ou demande simplement le fichier et continue.

<br>

> **La règle qui prime sur tout le reste.**
> Cette skill **lit** le CRM. Elle n'y écrit rien tant que l'utilisateur n'a
> pas relu le rapport et dit oui, en toutes lettres, à un import précis. Un
> import dans un CRM se défait mal.

---

## Les quatre phases

| Phase | Ce qu'on fait | Arrêt |
|---|---|---|
| 1 | Obtenir les comptes du CRM | **Il fournit l'export, ou choisit la démo** |
| 2 | Rapprocher | aucun |
| 3 | Rendre le rapport et écrire dans le fichier | **Il relit les « à vérifier »** |
| 4 | Décider quoi faire des nouveaux | **Il valide tout import** |

---

## Phase 1 · obtenir les comptes du CRM

Demande :

> Où sont tes comptes aujourd'hui ?
> - **Un CRM** (HubSpot, Salesforce, Pipedrive, Zoho…) : exporte tes
>   entreprises en CSV et donne-moi le chemin du fichier
> - **Un CRM déjà branché à Claude** : je le lis directement
> - **Un tableur** : télécharge-le en CSV
> - **Pas de CRM, ou je veux juste tester** : je fabrique un CRM de
>   démonstration à partir du fichier

**Export CSV.** Donne le chemin de menu de son CRM, tel qu'il figure dans
`cles-de-dedoublonnage.md`. Il faut les **entreprises**, pas les contacts, avec
au minimum : nom, téléphone, code postal, identifiant de fiche, propriétaire.
SIRET et site web s'il les a.

**CRM branché.** Vérifie que tu as bien un outil qui lit ce CRM. Lis les
entreprises par pages, ne garde que les champs utiles, et écris-les dans
`<dossier_travail>/export-crm.csv`. Au-delà de quelques milliers de fiches,
dis-le : l'export CSV sera plus rapide.

**CRM de démonstration.** Pour quelqu'un qui teste. Fabrique
`<dossier_travail>/crm-demo.csv` à partir du fichier lui-même, pour imiter ce
qu'est un vrai CRM de terrain :

- prends 60 établissements au hasard parmi les qualifiés ;
- pour 30 d'entre eux, mets le téléphone au format national avec espaces
  (`02 54 55 22 22`) et pas de SIRET ;
- pour 15, garde le SIRET et retire le téléphone ;
- pour 15, ne garde que le nom en majuscules précédé de « SARL » et le code
  postal ;
- ajoute 40 lignes inventées qui ne sont pas dans le fichier (noms et numéros
  fictifs, d'un autre département) ;
- colonnes : `Record ID`, `Company name`, `Phone Number`, `Postal Code`,
  `SIRET`, `Company owner`, avec deux prénoms de commerciaux fictifs.

Dis clairement que c'est une simulation, et ce qu'elle doit donner : environ 45
retrouvés par une clé forte, 15 « à vérifier », le reste absent.

## Phase 2 · rapprocher

Il faut le fichier en CSV. En mode CSV, c'est
`etablissements-travail.csv`. En mode Sheets, lis l'onglet et écris-le dans
`<dossier_travail>/etablissements.csv`, toutes colonnes, en-têtes inchangés.

Puis lance le script, tel quel :

```bash
python3 ~/.claude/terrain/scripts/dedup.py \
  --fichier <etablissements.csv> \
  --crm <export-crm.csv> \
  --sortie <dossier_travail>/dedup
```

Il reconnaît seul les en-têtes français et anglais des exports courants. S'il
s'arrête sur « Aucune clé commune », lis les en-têtes qu'il affiche, repère la
colonne du téléphone ou du SIRET, et relance avec `--crm-telephone "<en-tête>"`
(ou `--crm-siret`, `--crm-site`, `--crm-nom`, `--crm-code-postal`, `--crm-id`,
`--crm-proprietaire`).

Pour un fichier qui n'est pas un fichier Scalon, ajoute
`--id-fichier "<colonne identifiant>"`.

**Ne réécris pas la logique de rapprochement toi-même.** Le script normalise
les téléphones, écarte les domaines de réseau et ne donne jamais `oui` sur un
nom seul. Une comparaison improvisée dans la conversation rate ces trois cas.

## Phase 3 · le rapport, puis l'écriture

Lis `dedup/rapport.txt` et rends-le en clair :

> Sur les N établissements du fichier :
> - **X sont déjà dans ton CRM** (dont tant par SIRET, tant par téléphone)
> - **Y sont à vérifier** : même nom et même code postal, sans clé forte
> - **Z ne sont pas dans ton CRM**

Puis le chiffre qui compte, calculé en croisant `rapprochement.csv` avec la
colonne `Priorité ICP` si elle existe :

> Parmi tes priorités A : **tant sont nouveaux pour toi.**

Si une clé n'a pas pu servir parce que l'export ne contenait pas la colonne,
dis-le, et dis ce que ça coûte : sans téléphone ni SIRET dans l'export, presque
tout sort en « à vérifier » ou en « non », et le chiffre des nouveaux est
gonflé.

**Arrêt.** Montre les lignes `à vérifier` en tableau (nom dans le fichier, nom
dans le CRM, ville, propriétaire) et demande de trancher. C'est une liste
courte. Reporte chaque réponse : `oui` ou `non`.

Écris ensuite dans le fichier, en retrouvant chaque ligne par son `ID Scalon`
et chaque colonne par son en-tête : `Dans le CRM`, `Clé de rapprochement`,
`ID CRM`, `Propriétaire CRM`. Crée les colonnes à droite si `/terrain-setup` ne
les a pas posées. En mode CSV, écris dans `etablissements-travail.csv`.

## Phase 4 · quoi faire des nouveaux

Ne propose pas d'importer tout le fichier. Propose le choix :

> Trois façons de continuer :
> 1. **Ne rien importer pour l'instant.** Tu appelles depuis le fichier, et
>    seuls les établissements qui répondent positivement entrent dans le CRM.
>    C'est ce qu'on fait chez nous : le CRM reste propre.
> 2. **Importer les priorités A absentes du CRM**, pour que toute l'équipe les
>    voie.
> 3. **Enrichir les fiches déjà présentes** avec ce que le fichier sait d'elles
>    (statut, type d'établissement, enseigne), sans en créer de nouvelles.

**Arrêt, pour les options 2 et 3.** Annonce le nombre exact de fiches créées
ou modifiées et les champs concernés. Attends un oui explicite.

- CRM branché : crée ou mets à jour par lots de 20, en commençant par 5 fiches
  que tu fais relire dans le CRM avant de continuer.
- Sinon : produis `<dossier_travail>/import-crm.csv`, avec les colonnes que son
  CRM attend à l'import, et laisse-le importer lui-même.

Dans les deux cas, ne pousse jamais une ligne `Hors cible` ni une ligne
`Indéterminé`.

**Pas de CRM du tout.** Dis-le simplement : un CRM complet se construit dans
Notion en un prompt, celui du premier blueprint :
https://github.com/morterolvalentin-ctrl/outbound-blueprint/blob/main/prompts/08-construire-le-crm-notion.md

Termine en rappelant la file d'appels : `Priorité ICP` = A, `Dans le CRM` =
non, triée par score décroissant.
