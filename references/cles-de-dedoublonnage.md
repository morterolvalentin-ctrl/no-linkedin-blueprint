# Les clés de dédoublonnage

Rapprocher un fichier d'établissements de ton CRM, c'est répondre à une seule
question par ligne : **est-ce que je l'ai déjà ?** Tout dépend de la clé que tu
compares.

## L'ordre des clés

On les essaie dans cet ordre, et on s'arrête à la première qui répond.

| # | Clé | Verdict | Pourquoi cet ordre |
|---|---|---|---|
| 1 | **SIRET** | `oui` | Identifiant légal de l'établissement. Quand ton CRM l'a, il n'y a pas de discussion |
| 2 | **Téléphone** | `oui` | La clé la plus répandue dans un CRM de terrain. À normaliser avant de comparer |
| 3 | **Domaine du site** | `oui` | Fiable seulement quand le domaine est propre à l'établissement |
| 4 | **Nom + code postal** | `à vérifier` | Jamais une preuve. Deux « Garage du Centre » peuvent partager un code postal |

## Les trois pièges

**1. Le téléphone ne se compare pas tel quel.**
`02 54 55 22 22`, `+33 2 54 55 22 22`, `0033254552222` et `+33 (0)2 54 55 22 22`
sont le même numéro. Comparés en texte brut, ce sont quatre établissements
différents, et ton rapport annonce 100 % de nouveautés. Tout se ramène au format
international avant de comparer.

**2. Le domaine d'un réseau n'est pas le domaine d'un établissement.**
Un garage sous enseigne a souvent pour site une page du site de son réseau.
Tous les garages de l'enseigne partagent alors le même domaine. Une clé
« domaine » naïve les fusionne tous en un seul. La règle : un domaine qui
apparaît sur plus d'une ligne ne sert pas de clé.

**3. Le nom seul n'est jamais une clé.**
Le nom légal et le nom affiché sur la devanture diffèrent souvent.
Le nom, même avec le code postal, ne donne qu'un `à vérifier` : c'est toi qui
tranches, à l'œil, sur une liste courte.

## Ce qu'on écrit dans le fichier

Quatre colonnes ajoutées à droite, jamais à la place d'une colonne existante.

| Colonne | Valeurs |
|---|---|
| `Dans le CRM` | `oui` · `non` · `à vérifier` |
| `Clé de rapprochement` | `SIRET` · `Téléphone` · `Domaine du site` · `Nom + code postal` |
| `ID CRM` | L'identifiant de la fiche trouvée |
| `Propriétaire CRM` | Le commercial qui porte déjà le compte |

`Propriétaire CRM` évite l'erreur la plus coûteuse en équipe : appeler le
client d'un collègue.

## Exporter depuis ton CRM

Un export CSV suffit, et il marche avec tous les CRM. Exporte les
**entreprises** (ou les comptes), pas les contacts, avec au minimum : le nom,
le téléphone, le code postal, l'identifiant de fiche, le propriétaire. Ajoute
le SIRET et le site web si tu les as.

| CRM | Où |
|---|---|
| HubSpot | CRM → Entreprises → Exporter (en haut à droite du tableau) |
| Salesforce | Rapports → nouveau rapport sur les Comptes → Exporter, format CSV |
| Pipedrive | Organisations → ⋯ → Exporter les résultats du filtre |
| Zoho CRM | Configuration → Administration des données → Exporter |
| Un tableur | Fichier → Télécharger → CSV |

Le script reconnaît seul les en-têtes français et anglais des exports courants.
Si ta colonne porte un nom maison, tu la désignes :

```bash
python3 ~/.claude/terrain/scripts/dedup.py \
  --fichier etablissements.csv --crm export-crm.csv \
  --crm-telephone "Tél. standard" --crm-id "N° compte"
```

## Si ton CRM est branché à Claude

HubSpot, Salesforce et d'autres ont un serveur MCP ou un connecteur Claude.
Dans ce cas tu peux sauter l'export : `/terrain-dedup` demande à Claude de lire
les entreprises du CRM, puis applique exactement les mêmes clés. Sur une grosse
base, l'export CSV reste plus rapide et ne coûte rien.

## Après le rapprochement

- `non` : c'est ta liste d'appels. Ce sont les établissements que ton CRM
  n'avait pas.
- `oui` : tu ne les réimportes pas. Tu regardes ce que le fichier sait d'eux et
  que ta fiche ne sait pas (le statut, le type, l'enseigne), et tu enrichis.
- `à vérifier` : une liste courte, dix minutes à l'œil.

N'importe rien dans ton CRM avant d'avoir relu le rapport. Un import se défait
mal.
