#!/usr/bin/env bash
# Installe le serveur Ollama sans sudo dans ~/.local/lib/ollama
set -euo pipefail

INSTALL_DIR="${HOME}/.local/lib/ollama"
BIN_DIR="${INSTALL_DIR}/bin"
mkdir -p /tmp/ollama-install

echo "  * Détection de la version d'Ollama"
LATEST_URL=$(curl -fsSL https://api.github.com/repos/ollama/ollama/releases/latest \
    | grep -oP '"browser_download_url":\s*"\Khttps://[^"]+linux-amd64\.tar\.zst' | head -1)
if [ -z "${LATEST_URL}" ]; then
    echo "Erreur : impossible de déterminer le binaire Ollama (connexion requise)."
    exit 1
fi
echo "  * Téléchargement : ${LATEST_URL}"
curl -fL --progress-bar "${LATEST_URL}" -o /tmp/ollama-install/ollama.tar.zst

mkdir -p "${INSTALL_DIR}"
tar --zstd -xf /tmp/ollama-install/ollama.tar.zst -C "${INSTALL_DIR}"

if "${BIN_DIR}/ollama" --version >/dev/null 2>&1; then
    echo "  * Ollama installé : $("${BIN_DIR}/ollama" --version)"
else
    echo "Erreur : l'installation d'Ollama a échoué."
    exit 1
fi

echo ""
echo "  Pour lancer le serveur (à faire une fois par session) :"
echo "    ${BIN_DIR}/ollama serve"
echo "  Puis charger le modèle (téléchargement ~4,7 Go) :"
echo "    ${BIN_DIR}/ollama pull qwen2.5:7b"