# 02 · Dédoublonner avec son CRM

Deux façons. Le script est exact et gratuit, le prompt marche sans terminal.

## Avec le script (recommandé)

```bash
python3 ~/.claude/terrain/scripts/dedup.py \
  --fichier etablissements.csv \
  --crm export-crm.csv \
  --sortie dedup
```

Il écrit `dedup/rapport.txt` (le compte) et `dedup/rapprochement.csv` (le
verdict ligne par ligne). Python standard, rien à installer. Les exports par
CRM et les options sont dans
[`references/cles-de-dedoublonnage.md`](../references/cles-de-dedoublonnage.md).

## Avec un prompt

Joins le CSV des établissements et l'export CSV des **entreprises** de ton CRM.

```text
Je te joins un fichier d'établissements et un export de mon CRM. Dis-moi
lesquels j'ai déjà. Calcule avec du code, ne compare rien de tête.

Commence par me montrer les en-têtes des deux fichiers et les colonnes que tu
comptes utiliser comme SIRET, téléphone, site web, nom, code postal,
identifiant de fiche et propriétaire. Attends que je confirme.

Puis rapproche, dans cet ordre, en t'arrêtant à la première clé qui répond :
1. SIRET : 14 chiffres, exact.
2. Téléphone : ramène d'abord les deux côtés au format international sans
   espace ni ponctuation. 02 54 55 22 22, +33 2 54 55 22 22, 0033254552222 et
   +33 (0)2 54 55 22 22 sont le même numéro.
3. Domaine du site : sans http, sans www, sans chemin. N'utilise un domaine
   que s'il n'apparaît que sur une seule ligne du fichier : un domaine partagé
   par plusieurs établissements est celui de leur réseau.
4. Nom + code postal : nom en minuscules, sans accents, sans forme juridique
   (SARL, SAS, EURL, Ets…). Cette clé ne donne jamais « oui », seulement
   « à vérifier ».

Ajoute quatre colonnes à droite du fichier, sans toucher aux autres :
« Dans le CRM » (oui, non, à vérifier), « Clé de rapprochement », « ID CRM »,
« Propriétaire CRM ».

Rends-moi :
- le compte : déjà dans le CRM (par clé), à vérifier, absents ;
- si le fichier a une colonne « Priorité ICP », combien de A sont absents ;
- le tableau des « à vérifier », pour que je tranche à l'œil ;
- le fichier complet en CSV.

N'importe rien dans mon CRM. Si une clé n'a pas pu servir parce que la colonne
manquait dans mon export, dis-le et dis ce que ça change au résultat.
```

## Lire le résultat

- **Absents** : ta liste d'appels.
- **Déjà dans le CRM** : ne les réimporte pas. Regarde ce que le fichier sait
  d'eux et que ta fiche ignore.
- **À vérifier** : dix minutes à l'œil.

Si le rapport annonce presque 100 % d'absents, méfie-toi avant de te réjouir :
c'est en général que l'export ne contenait ni téléphone ni SIRET.
