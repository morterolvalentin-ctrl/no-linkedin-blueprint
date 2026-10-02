# No LinkedIn Blueprint

Prospecter les entreprises qui ne sont pas sur LinkedIn : garages, restaurants,
commerces, artisans, salons, cabinets. Avec Claude, un fichier
d'établissements qualifiés, ton CRM et un téléphone.

C'est la version publique de la façon dont on travaille chez
[Scalon](https://scalon.fr), livrée avec **un vrai fichier de 999
établissements** pour tester.

👉 **[Copier le fichier de démonstration](https://docs.google.com/spreadsheets/d/1B3-JFoqKLBg3WmGM3EKy5pjQ0Q6-nPBeKiDvNFQWbDE/copy)** · Google Sheets, un clic
👉 **[Demander un échantillon sur ton marché](https://cal.com/valentin-morterol-ezc5qn/30min)** · 30 minutes avec Valentin

---

## Le problème

Aucun outil de prospection LinkedIn ne trouve un garagiste, un restaurateur ou
un artisan. Il reste deux façons de faire, et les deux coûtent cher.

- **Une base légale dans le CRM.** Elle part des codes d'activité, elle n'est
  jamais à jour, et la plus grande part de ses lignes est hors cible.
- **Les commerciaux qui cherchent un par un sur une carte.** Ils qualifient au
  lieu de vendre, alors qu'ils sont payés et commissionnés pour vendre.

Ce dépôt montre la troisième : un fichier où chaque établissement porte déjà
son verdict et la raison de ce verdict, que Claude trie pour toi, rapproche de
ton CRM et transforme en file d'appels.

## Tester en dix minutes, sans rien brancher

**Avec Claude Code**

```bash
curl -fsSL https://raw.githubusercontent.com/morterolvalentin-ctrl/no-linkedin-blueprint/main/install.sh | bash
```

Puis, dans Claude Code :

```
/terrain-setup
```

La skill te donne le lien du fichier, te demande à qui tu vends, et monte le
reste. Elle sait travailler sur un simple export CSV : **aucune connexion n'est
nécessaire pour un premier essai.**

**Sans terminal**, sur Claude web ou l'application de bureau : télécharge deux
onglets du fichier en CSV, joins-les à la conversation et colle le
[prompt maître](prompts/00-prompt-maitre.md).

<br>

> Tu préfères voir ce que fait le script avant de le lancer ?
> [`install.sh`](install.sh) clone ce dépôt dans un dossier temporaire, copie
> trois skills dans `~/.claude/skills/` en sauvegardant ce qui existait, et
> dépose les références dans `~/.claude/terrain/`. Il ne touche à rien d'autre
> et n'installe aucune clé.

## Le fichier de démonstration

999 établissements du Loir-et-Cher (41), relevés le 28/09/2026. C'est un test
réel, produit pour une entreprise qui vend aux **garages indépendants**, ceux
que le métier appelle les MRA.

| | |
|---|---|
| Établissements passés au crible | 999 |
| **Qualifiés** : garage en activité, atelier ouvert au public | **229** |
| Non qualifiés, avec le motif écrit | 298 |
| Indéterminés : rien de public ne confirme l'activité | 472 |
| Garages indépendants (MRA) parmi les qualifiés | 164, dont 92 sans enseigne |

Chaque ligne porte un `Statut`, une `Raison du statut`, un
`Score Ciblage Scalon` de 0 à 100, un `Type d'établissement` et son
`Réseau ou marque`. Le détail, et ce que ces chiffres disent des codes
d'activité, est dans [`references/fichier-demo.md`](references/fichier-demo.md).

Ta cible n'est pas le garage ? Le fichier te sert à monter la machine. Pour la
faire tourner sur ton marché, il te faut un fichier sur ton marché :
[30 minutes avec Valentin](https://cal.com/valentin-morterol-ezc5qn/30min),
l'échantillon est gratuit.

## Les trois skills

| Skill | Quand | Ce qu'elle fait |
|---|---|---|
| [`/terrain-setup`](skills/terrain-setup/SKILL.md) | Une fois par fichier | Lit le fichier et sa légende, t'interroge sur ton client idéal, écrit `Priorité ICP` et sa raison sur chaque ligne, ajoute les colonnes de suivi. Deux arrêts où tu valides |
| [`/terrain-dedup`](skills/terrain-dedup/SKILL.md) | Avant d'appeler | Rapproche le fichier de ton CRM sur quatre clés, te dit combien d'établissements tu n'avais pas, n'importe rien sans ton accord. Sait fabriquer un CRM de démonstration si tu n'en as pas |
| [`/terrain-appels`](skills/terrain-appels/SKILL.md) | Avant et après chaque session | Sort la file du jour, puis lit les cases `Appelé` cochées et tes notes, classe, met à jour, et pousse les réponses positives dans le CRM |

## Les prompts, si tu préfères sans skill

| # | Étape | Fichier |
|---|---|---|
| 00 | Tout en un prompt, sans terminal | [`00-prompt-maitre.md`](prompts/00-prompt-maitre.md) |
| 01 | Définir son ICP et prioriser le fichier | [`01-definir-son-icp-et-prioriser.md`](prompts/01-definir-son-icp-et-prioriser.md) |
| 02 | Dédoublonner avec son CRM | [`02-dedoublonner-avec-son-crm.md`](prompts/02-dedoublonner-avec-son-crm.md) |
| 03 | Ajouter les colonnes de suivi | [`03-colonnes-de-suivi.md`](prompts/03-colonnes-de-suivi.md) |
| 04 | Traiter une session d'appels | [`04-traiter-une-session-dappels.md`](prompts/04-traiter-une-session-dappels.md) |

## Le script de dédoublonnage

[`scripts/dedup.py`](scripts/dedup.py) rapproche le fichier d'un export CSV de
n'importe quel CRM. Python standard, rien à installer.

```bash
python3 ~/.claude/terrain/scripts/dedup.py --fichier etablissements.csv --crm export-crm.csv
```

Quatre clés, dans l'ordre : SIRET, téléphone ramené au format international,
domaine du site quand il est propre à l'établissement, puis nom + code postal,
qui ne donne jamais mieux que « à vérifier ».

## Les outils

Aucun n'est nécessaire pour tester. Les commandes sont dans
[`mcp/README.md`](mcp/README.md).

| Outil | Rôle | Coût par mois |
|---|---|---|
| Claude | Le moteur | 20 € |
| [Google Sheets](mcp/README.md#1-google-sheets--le-fichier) | Le fichier, lu et écrit en direct | 0 € |
| [Ton CRM](mcp/README.md#2-ton-crm--le-dédoublonnage) | HubSpot, Salesforce, Pipedrive… un export CSV suffit | ce que tu paies déjà |
| [Notion](mcp/README.md#3-notion--le-crm-si-tu-nen-as-pas) | Le CRM, si tu n'en as pas | 10 € |
| [Allo](mcp/README.md#4-allo--le-téléphone) | La file d'appels, le nom affiché au rappel | dès 18 $ |

## Les références

| Fichier | Contenu |
|---|---|
| [`references/fichier-demo.md`](references/fichier-demo.md) | Ce que contient le fichier : verdicts, score, types, enseignes |
| [`references/colonnes-de-suivi.md`](references/colonnes-de-suivi.md) | Les douze colonnes à ajouter, les six statuts, les cinq règles d'écriture |
| [`references/cles-de-dedoublonnage.md`](references/cles-de-dedoublonnage.md) | Les quatre clés, les trois pièges, l'export par CRM |

## Désinstaller

```bash
rm -rf ~/.claude/skills/terrain-setup ~/.claude/skills/terrain-dedup \
       ~/.claude/skills/terrain-appels ~/.claude/terrain
```

Tes connexions restent branchées, ton Sheet et ton CRM restent à toi. Ton
dossier de travail `~/terrain/` (configuration, fiche ICP, exports) n'est pas
supprimé.

## Le blueprint précédent

Celui-ci traite des entreprises qui **ne sont pas** sur LinkedIn. Pour celles
qui y sont, avec le script de cold call et le CRM Notion :
[outbound-blueprint](https://github.com/morterolvalentin-ctrl/outbound-blueprint).

## Qui a écrit ça

<img src="https://scalon.fr/img/asset-84dc076345.webp" alt="Valentin Morterol" width="96" height="96" align="left" hspace="16">

**Valentin Morterol**, cofondateur et CEO de [Scalon](https://scalon.fr).

On qualifie des marchés entiers pour les entreprises qui prospectent des
établissements locaux : garages, restaurants, bars, commerces. Pour chaque
établissement, ce qu'il fait vraiment et ce qui en fait un client.

[LinkedIn](https://www.linkedin.com/in/valentin-morterol/) · [valentin@scalon.fr](mailto:valentin@scalon.fr) · [Prendre 30 minutes](https://cal.com/valentin-morterol-ezc5qn/30min)

<br clear="left">

## Licence

MIT pour les skills, les prompts et le script. Le fichier de démonstration
reste la propriété de Scalon : tu peux le copier pour tester ce blueprint, pas
le revendre ni le republier.
