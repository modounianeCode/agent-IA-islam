#!/usr/bin/env bash
# =============================================================
#  Assistant islamique — Apprendre l'Islam
#  Installe les dépendances, télécharge les données et construit
#  la base locale locale.
# =============================================================
set -euo pipefail

cd "$(dirname "$0")"

echo "==> [1/5] Vérification de Python 3.12+"
command -v python3 >/dev/null 2>&1 || { echo "Erreur : python3 est requis."; exit 1; }
python3 - <<'PY'
import sys
if sys.version_info < (3, 12):
    sys.exit(f"Python 3.12+ requis (version trouvée : {sys.version})")
PY

echo "==> [2/5] Création de l'environnement virtuel"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "==> [3/5] Téléchargement des données (Coran + 17 recueils de hadiths)"
python -m agent.ingest --download

echo "==> [4/5] Construction de la base locale (data/agent.db)"
python -m agent.ingest --build

echo ""
echo "=========================================="
echo "  Installation terminée."
echo "  Lancer l'assistant :"
echo "    Interface web    : source .venv/bin/activate && python webapp.py"
echo "    Ligne de commande: source .venv/bin/activate && python apprendre_islam.py"
echo "=========================================="