# Brancher les outils à Claude

**Rien n'est obligatoire pour tester.** Le blueprint tourne sans aucune
connexion : tu télécharges le fichier en `.csv`, Claude travaille dessus en
local et te rend un fichier à réimporter. C'est le chemin le plus court pour
voir si ça te sert.

Les connexions ci-dessous servent ensuite, quand tu veux que Claude écrive
directement dans ton Sheet, dans ton CRM et dans ton téléphone.

Toutes les commandes se lancent dans un terminal, pas dans Claude.

| Outil | Rôle | Sans lui | Coût |
|---|---|---|---|
| [Google Sheets](#1-google-sheets--le-fichier) | Claude lit et écrit ton fichier en direct | export et réimport CSV à la main | 0 € |
| [Ton CRM](#2-ton-crm--le-dédoublonnage) | Lire tes comptes, pousser les établissements qualifiés | export CSV du CRM | selon ton CRM |
| [Notion](#3-notion--le-crm-si-tu-nen-as-pas) | Le CRM, si tu n'en as pas | pas de CRM | 10 €/mois |
| [Allo](#4-allo--le-téléphone) | La file d'appels et le nom affiché au rappel | tu composes à la main | dès 18 $/mois |

---

## 1. Google Sheets · le fichier

```bash
claude mcp add google-sheets \
  --env CREDENTIALS_PATH=/chemin/vers/credentials.json \
  --env TOKEN_PATH=/chemin/vers/token.json \
  -- uvx --with "mcp<2" --from mcp-google-sheets@latest mcp-google-sheets
```

Il te faut des identifiants OAuth Google. C'est l'étape la plus longue de tout
le blueprint, compte quinze minutes :

1. Va sur [console.cloud.google.com](https://console.cloud.google.com) et crée
   un projet.
2. Active l'**API Google Sheets** et l'**API Google Drive**.
3. Écran de consentement OAuth : type « Externe », ajoute ton adresse Google
   comme utilisateur de test.
4. Identifiants → Créer → ID client OAuth → **Application de bureau**.
   Télécharge le JSON : c'est ton `credentials.json`.
5. Lance la commande ci-dessus avec le chemin de ce fichier. Le `token.json` se
   crée tout seul à la première connexion, Claude t'ouvre une page Google.

`uvx` vient avec [uv](https://docs.astral.sh/uv/). S'il manque :
`curl -LsSf https://astral.sh/uv/install.sh | sh`.

Sur Claude web ou l'application de bureau, Google Drive s'active depuis les
réglages de connecteurs, sans terminal.

## 2. Ton CRM · le dédoublonnage

**L'export CSV marche avec tous les CRM et ne demande aucune connexion.** C'est
le chemin par défaut du blueprint, voir
[`references/cles-de-dedoublonnage.md`](../references/cles-de-dedoublonnage.md).

Si tu veux que Claude lise et écrive dans ton CRM directement, HubSpot publie
un serveur MCP hébergé :

```bash
claude mcp add hubspot --transport http https://mcp.hubspot.com
```

Authentification par OAuth dans le navigateur. La procédure à jour est dans la
[documentation HubSpot](https://developers.hubspot.com/docs/build-with-ai/remote-mcp-server).

Pour Salesforce, Pipedrive, Zoho et les autres, cherche le connecteur officiel
de ton CRM dans les réglages de connecteurs de Claude, ou reste sur l'export
CSV.

## 3. Notion · le CRM, si tu n'en as pas

```bash
claude mcp add notion --transport http https://mcp.notion.com/mcp
```

OAuth. Autorise l'accès à l'espace où vivra le CRM, pas à tout ton Notion. Le
CRM lui-même se construit avec un seul prompt :
[08 · Construire le CRM dans Notion](https://github.com/morterolvalentin-ctrl/outbound-blueprint/blob/main/prompts/08-construire-le-crm-notion.md).

## 4. Allo · le téléphone

[withallo.com](https://withallo.com) · à partir de 18 $ par mois.

```bash
claude mcp add allo --transport http https://mcp.withallo.com/mcp \
  --header "Authorization: TA_CLE_API"
```

La clé se récupère dans Allo, **Settings → API**.

Deux choses changent une fois Allo branché. Claude pousse tes lignes
prioritaires dans la file d'appels, tu n'as plus qu'à enchaîner. Et quand un
garagiste te rappelle deux heures plus tard, son nom s'affiche : après
quarante appels dans la matinée, tu ne reconnais aucun numéro.

---

## Vérifier que tout répond

```bash
claude mcp list
```

Chaque ligne doit afficher `✔ Connected`. Une ligne `! Needs authentication`
veut dire que l'OAuth n'a pas été fait : lance `claude`, tape `/mcp`, choisis
le serveur.

## Où vivent les clés

Dans ta configuration MCP et dans ton environnement shell. Jamais dans un
fichier du projet, jamais collées dans une conversation.
