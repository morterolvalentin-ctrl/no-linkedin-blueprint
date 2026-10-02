#!/usr/bin/env bash
# No LinkedIn Blueprint · installation
# Copie trois skills dans ~/.claude/skills/ et les références dans ~/.claude/terrain/.
# Ne touche à aucun de tes fichiers existants sans te le dire, n'installe aucune clé.

set -euo pipefail

REPO="https://github.com/morterolvalentin-ctrl/no-linkedin-blueprint.git"
SKILLS_DIR="${HOME}/.claude/skills"
CONF_DIR="${HOME}/.claude/terrain"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

bold "No LinkedIn Blueprint · installation"
echo

command -v git >/dev/null || { echo "git est requis."; exit 1; }

git clone --depth 1 -q "${REPO}" "${TMP}/repo"
ok "dépôt récupéré"

mkdir -p "${SKILLS_DIR}" "${CONF_DIR}"

for s in terrain-setup terrain-dedup terrain-appels; do
  if [ -d "${SKILLS_DIR}/${s}" ]; then
    backup="${SKILLS_DIR}/${s}.backup-$(date +%Y%m%d-%H%M%S)"
    mv "${SKILLS_DIR}/${s}" "${backup}"
    warn "${s} existait déjà, sauvegardée dans $(basename "${backup}")"
  fi
  cp -R "${TMP}/repo/skills/${s}" "${SKILLS_DIR}/${s}"
  ok "skill ${s} installée"
done

# Les références, les prompts et le script sont écrasés à chaque install : ce
# sont des copies du dépôt. Ton config.json et ta fiche icp.md ne sont pas
# touchés.
for pair in \
  "references/fichier-demo.md:fichier-demo.md" \
  "references/colonnes-de-suivi.md:colonnes-de-suivi.md" \
  "references/cles-de-dedoublonnage.md:cles-de-dedoublonnage.md" \
  "mcp/README.md:mcp.md"; do
  src="${TMP}/repo/${pair%%:*}"
  dst="${CONF_DIR}/${pair##*:}"
  if [ -f "${src}" ]; then
    cp "${src}" "${dst}"
  else
    warn "${pair%%:*} absent du dépôt, ignoré"
  fi
done

for d in prompts scripts; do
  rm -rf "${CONF_DIR:?}/${d}"
  cp -R "${TMP}/repo/${d}" "${CONF_DIR}/${d}"
done
ok "références, guide de connexion, script et $(find "${CONF_DIR}/prompts" -name '*.md' | wc -l | tr -d ' ') prompts copiés dans ~/.claude/terrain/"

if command -v python3 >/dev/null; then
  ok "python3 trouvé, le script de dédoublonnage est prêt"
else
  warn "python3 introuvable : le dédoublonnage par script ne tournera pas, le prompt 02 le remplace"
fi

echo
bold "C'est installé. La suite :"
echo
echo "    1. Fais ta copie du fichier de démonstration (un clic) :"
echo "       https://docs.google.com/spreadsheets/d/1B3-JFoqKLBg3WmGM3EKy5pjQ0Q6-nPBeKiDvNFQWbDE/copy"
echo
echo "    2. Lance Claude, puis la skill :"
echo "       claude"
echo "       /terrain-setup"
echo
echo "Aucune connexion n'est nécessaire pour tester : la skill sait travailler"
echo "sur un simple export CSV. Elle te proposera de brancher Google Sheets"
echo "ensuite, si tu veux qu'elle écrive directement dans ton fichier."
echo
