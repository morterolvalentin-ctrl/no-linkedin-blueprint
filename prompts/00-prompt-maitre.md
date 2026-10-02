# 00 · Le prompt maître

Pour Claude sur le web ou l'application de bureau, sans terminal et sans
installation. Tu joins tes fichiers à la conversation, tu colles le prompt.

**Avant de coller :**

1. Fais ta copie du fichier exemple (lien dans
   [`references/fichier-demo.md`](../references/fichier-demo.md)), ou ouvre ton
   propre fichier d'établissements.
2. Télécharge le fichier en Excel (Fichier → Télécharger → Microsoft Excel),
   ou deux onglets en CSV : **Établissements** et **Légende**.
3. Si tu as un CRM, exporte tes **entreprises** en CSV. Sinon, saute cette
   étape, le prompt s'en passe.
4. Joins les fichiers à la conversation, puis colle ce qui suit.

```text
Tu vas m'aider à prospecter des établissements locaux à partir d'un fichier
qualifié. Je te joins : le fichier des établissements avec sa légende (un
classeur Excel, ou deux CSV), et
(si je l'ai) un export CSV des entreprises de mon CRM.

Règles, valables pour toute la conversation :
- Les colonnes d'origine du fichier sont en lecture seule. Tu ajoutes des
  colonnes à droite, tu n'en modifies aucune.
- Tu désignes une colonne par son en-tête et une ligne par son identifiant
  (colonne « ID Scalon »), jamais par une lettre ou un numéro de ligne.
- Tu n'inventes rien sur un établissement. Si tu ne sais pas, tu l'écris.
- Tu t'arrêtes à chaque étape marquée ARRÊT et tu attends ma réponse.
- Tu calcules avec du code sur les fichiers joints, tu ne comptes pas de tête.

ÉTAPE 1 · Lire. Lis la légende en entier, puis le fichier. Rends-moi en dix
lignes : le nombre de lignes, la répartition du verdict (colonne « Statut »),
la répartition du type d'établissement parmi les qualifiés, la médiane du
score par verdict, le taux de remplissage du téléphone, et trois exemples de
« Raison du statut » cités mot pour mot, un par verdict.

ÉTAPE 2 · Mon ICP. Pose-moi ces questions une par une, en attendant chaque
réponse : ce que je vends et à qui ; ce que mes trois meilleurs clients ont en
commun ; quel type d'établissement j'appelle pour rien ; si l'appartenance à
un réseau ou à une enseigne change quelque chose ; s'il y a une taille
minimale ou maximale ; ma zone. Puis écris ma fiche ICP en n'utilisant que des
colonnes qui existent dans le fichier, avec quatre niveaux : A, B, C, Hors
cible, plus « À vérifier » pour les lignes indéterminées qui ont un téléphone.
Donne le nombre de lignes de chaque niveau.
ARRÊT : je valide la fiche.

ÉTAPE 3 · Prioriser. Ajoute « Priorité ICP » (A, B, C, À vérifier, Hors cible)
et « Raison priorité » (une phrase qui cite le critère décisif, dans les mots
du fichier). Une ligne « Non qualifié » est toujours Hors cible. Une ligne
« Indéterminé » n'est jamais A, B ou C. Montre-moi d'abord 50 lignes
qualifiées en tableau.
ARRÊT : je valide les 50, puis tu appliques à tout le fichier.

ÉTAPE 4 · Dédoublonner. Si j'ai joint un export CRM, rapproche-le du fichier
avec ces clés, dans cet ordre, en t'arrêtant à la première qui répond :
1) SIRET exact, 14 chiffres ;
2) téléphone, après l'avoir ramené au format international des deux côtés
   (02 54 55 22 22, +33 2 54 55 22 22 et 0033254552222 sont le même numéro) ;
3) domaine du site, seulement si ce domaine n'apparaît que sur une ligne du
   fichier (un domaine partagé est celui d'un réseau) ;
4) nom nettoyé + code postal, qui ne donne jamais « oui » mais « à vérifier ».
Ajoute « Dans le CRM » (oui, non, à vérifier), « Clé de rapprochement »,
« ID CRM », « Propriétaire CRM ». Rends-moi le compte : déjà dans le CRM,
à vérifier, absents, et combien de mes priorités A sont absentes du CRM.
Si je n'ai pas joint d'export, mets « Dans le CRM » à vide et dis-le.
ARRÊT : je tranche les « à vérifier ».

ÉTAPE 5 · Suivi. Ajoute « Appelé » (FALSE partout), « Statut d'appel »
(« À appeler » sur les A, B et C), « Nb appels » (0), « Dernier appel »,
« Prochaine action », « Notes ».

ÉTAPE 6 · Rendre. Donne-moi le fichier complet en CSV à télécharger, et ma
file d'appels du jour : les priorités A absentes du CRM, par score décroissant,
30 lignes, avec pour chacune le nom, la ville, le téléphone et la raison
d'appeler.
```

**Après :** dans ton Google Sheet, Fichier → Importer → Importer, puis
« Remplacer la feuille actuelle ». Sélectionne la colonne `Appelé`, Insertion →
Case à cocher. Tu peux appeler.

Le soir, télécharge de nouveau l'onglet en CSV et utilise le prompt
[04](04-traiter-une-session-dappels.md).
