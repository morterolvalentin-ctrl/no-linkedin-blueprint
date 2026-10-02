# 04 · Traiter une session d'appels

Pendant la session tu ne fais que deux gestes par appel : cocher `Appelé`,
écrire ta note. Le soir, ce prompt fait le reste.

Avec Claude branché sur ton Sheet, donne l'URL. Sinon, télécharge l'onglet en
CSV et joins-le.

```text
Je viens de finir une session d'appels sur mon fichier [URL DU SHEET, OU CSV
JOINT]. Traite-la.

1. Prends toutes les lignes où « Appelé » est coché, et seulement celles-là.
   Dis-moi combien il y en a.

2. Classe chacune depuis sa colonne « Notes », avec six valeurs et six
   seulement dans « Statut d'appel » :
   - Rappeler : personne n'a décroché, répondeur, patron absent ou occupé
   - Réponse positive : il a dit oui (rendez-vous, devis, démo, passage)
   - Réponse négative : il a décroché et c'est non
   - Rappel programmé : il demande à être rappelé à une date précise
   - Ne pas contacter : fermé, vendu, numéro faux, hors cible, ou il l'a demandé
   Une ligne cochée sans note : ne devine pas, liste-la et demande-moi.

3. Pour chaque ligne classée : « Nb appels » +1, « Dernier appel » = la date
   du jour au format AAAA-MM-JJ, « Prochaine action » = une action et une
   date (vide pour un non ou un « ne pas contacter »), puis décoche « Appelé ».
   Dans « Notes », ajoute la date devant ma note si elle n'y est pas. N'écrase
   jamais une note existante, ajoute avec « | ».

4. Retrouve chaque ligne par son « ID Scalon » et relis son « Nom » avant
   d'écrire. Retrouve chaque colonne par son en-tête. Ne modifie aucune colonne
   d'origine du fichier.

5. Rends-moi : le nombre d'appels, de décrochés, de réponses positives, de
   rappels programmés ; la liste des réponses positives avec leur prochaine
   action ; et tout motif de refus qui revient plus de trois fois.

6. Ne crée rien dans mon CRM sans me le demander. Propose-moi seulement d'y
   créer les réponses positives.
```

**Pourquoi seules les réponses positives entrent dans le CRM.** Un CRM rempli
de 1 000 établissements jamais joints est un CRM que personne n'ouvre. Le
fichier est l'endroit où tu travailles, le CRM est l'endroit où vivent les
gens qui t'ont répondu.
