# Les colonnes de suivi

Le fichier livré décrit les établissements. Il ne sait rien de tes appels. On
lui ajoute douze colonnes, **à droite**, sans toucher à une seule colonne
d'origine.

Ce sont les colonnes qu'on utilise tous les jours chez Scalon pour notre propre
prospection, réduites à ce qui sert.

## Ta priorité

| Colonne | Contenu |
|---|---|
| `Priorité ICP` | **Liste fermée** : `A` · `B` · `C` · `À vérifier` · `Hors cible` |
| `Raison priorité` | Une phrase : le critère de ton ICP qui a décidé |

`Score Ciblage Scalon` répond à « est-ce bien un garage ? ». `Priorité ICP`
répond à « est-ce **mon** client ? ». Les deux ne se remplacent pas : la
première vient du fichier, la seconde vient de toi.

## Le rapprochement CRM

| Colonne | Contenu |
|---|---|
| `Dans le CRM` | `oui` · `non` · `à vérifier` |
| `Clé de rapprochement` | La clé qui a répondu |
| `ID CRM` | L'identifiant de la fiche trouvée |
| `Propriétaire CRM` | Le commercial qui porte déjà le compte |

## Le suivi d'appel

| Colonne | Contenu |
|---|---|
| `Appelé` | **Case à cocher.** Tu la coches quand tu viens d'appeler. C'est le seul geste demandé pendant la session, avec la note |
| `Statut d'appel` | **Liste fermée** : `À appeler` · `Rappeler` · `Réponse positive` · `Réponse négative` · `Rappel programmé` · `Ne pas contacter` |
| `Nb appels` | Tentatives réelles. Jamais incrémenté pour un mail |
| `Dernier appel` | Date du dernier appel, `AAAA-MM-JJ` |
| `Prochaine action` | Une action concrète, avec une date |
| `Notes` | Ce qui s'est passé, en langage libre. **La colonne la plus importante** : c'est elle qui alimente le classement et ton CRM |

### Les six statuts

| Statut | Quand |
|---|---|
| `À appeler` | Jamais appelé. C'est l'état de départ |
| `Rappeler` | Personne n'a décroché, ou le patron était sous une voiture. Au moins un appel réel |
| `Réponse positive` | Il a dit oui : rendez-vous pris, ou il demande lui-même un devis, une démo, un passage |
| `Réponse négative` | Il a décroché et c'est non |
| `Rappel programmé` | Il demande à être rappelé à une date précise. `Prochaine action` porte la date |
| `Ne pas contacter` | Fermé, vendu, hors cible constaté au téléphone, ou il l'a demandé |

## Comment la case `Appelé` fonctionne

1. Pendant ta session : tu appelles, tu coches `Appelé`, tu écris ta note. Cinq
   secondes.
2. Le soir : `/terrain-appels` lit **les lignes cochées**, classe chacune
   depuis sa note, ajoute 1 à `Nb appels`, écrit `Dernier appel`, propose
   `Prochaine action`, puis **décoche la case**.
3. Le lendemain, les cases sont vides. Une case cochée veut toujours dire
   « appelé depuis le dernier traitement ».

## Les règles d'écriture

Elles viennent toutes d'une erreur réelle.

**1. Une colonne se désigne par son en-tête, jamais par sa lettre.**
Tu vas déplacer des colonnes à la main. Une écriture « en colonne F » finit un
jour dans la mauvaise colonne, sans rien signaler.

**2. On n'écrit jamais à un numéro de ligne.**
On écrit à un `ID Scalon`, après avoir relu le `Nom` de la ligne. Tu tries et
tu filtres ce fichier pendant tes sessions : une ligne bouge entre la lecture
et l'écriture.

**3. Les colonnes d'origine sont en lecture seule.**
`Statut`, `Raison du statut`, `Score Ciblage Scalon` et les autres ne se
modifient pas. Si tu contestes un verdict, tu l'écris dans `Notes` et dans ta
`Priorité ICP`.

**4. `Notes` s'ajoute, ne s'écrase jamais.**
On concatène avec ` | `, la date devant. L'historique d'un établissement tient
dans cette cellule.

**5. Jamais `Rappeler` sur une ligne à zéro appel.**
Sinon tu ne distingues plus les lignes vierges des relances.

## Les mises en forme à poser une fois

- figer la ligne d'en-tête et les deux premières colonnes (`ID Scalon`, `Nom`) ;
- validation des données (liste déroulante) sur `Priorité ICP`, `Dans le CRM`
  et `Statut d'appel` ;
- case à cocher sur `Appelé` ;
- format date `AAAA-MM-JJ` sur `Dernier appel` ;
- format texte brut sur `Téléphone` et `SIRET`, sinon le tableur mange le `+`
  et transforme le SIRET en notation scientifique ;
- un filtre sur la ligne d'en-tête.

## La vue d'appel

Un filtre, toujours le même :

`Priorité ICP` = A, `Dans le CRM` = non, `Statut d'appel` = À appeler ou
Rappeler, trié par `Score Ciblage Scalon` décroissant.

C'est ta file du jour. Quand elle est vide, tu passes aux B.
