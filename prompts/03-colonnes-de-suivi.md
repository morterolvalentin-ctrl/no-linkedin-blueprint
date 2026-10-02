# 03 · Ajouter les colonnes de suivi

À utiliser avec Claude branché sur ton Google Sheet. Sans connexion, le
[prompt maître](00-prompt-maitre.md) pose les mêmes colonnes dans le CSV.

Le détail des colonnes, des statuts et des règles :
[`references/colonnes-de-suivi.md`](../references/colonnes-de-suivi.md).

```text
Dans mon Google Sheet [URL DE TA COPIE], onglet « Établissements », ajoute ces
colonnes à droite des colonnes existantes, dans cet ordre, sans modifier ni
déplacer aucune colonne d'origine :

Priorité ICP · Raison priorité · Dans le CRM · Clé de rapprochement · ID CRM ·
Propriétaire CRM · Appelé · Statut d'appel · Nb appels · Dernier appel ·
Prochaine action · Notes

N'ajoute pas une colonne qui existe déjà : relis la ligne d'en-tête d'abord.

Puis :
- « Appelé » : cases à cocher, toutes décochées.
- « Statut d'appel » : liste déroulante avec À appeler, Rappeler, Réponse
  positive, Réponse négative, Rappel programmé, Ne pas contacter. Mets
  « À appeler » sur les lignes dont la « Priorité ICP » vaut A, B ou C.
- « Priorité ICP » : liste déroulante avec A, B, C, À vérifier, Hors cible.
- « Dans le CRM » : liste déroulante avec oui, non, à vérifier.
- « Nb appels » : 0 sur les lignes A, B et C.
- « Dernier appel » : format date AAAA-MM-JJ.
- Fige la ligne d'en-tête et les deux premières colonnes.
- Pose un filtre sur la ligne d'en-tête.
- Vérifie que « Téléphone » et « SIRET » sont en texte brut.

Désigne toujours une colonne par son en-tête, jamais par sa lettre. Si une
mise en forme n'est pas à ta portée, dis laquelle et donne-moi le geste à
faire à la main.
```

Ta vue d'appel, à enregistrer comme vue filtrée : `Priorité ICP` = A,
`Dans le CRM` = non, `Statut d'appel` = À appeler ou Rappeler, tri par
`Score Ciblage Scalon` décroissant.
