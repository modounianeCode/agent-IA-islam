"""Téléchargement des données et construction de la base SQLite (une seule fois).

Usage :
    python -m agent.ingest [--download] [--build]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

from agent import db

QURAN_BASE = "https://cdn.jsdelivr.net/npm/quran-json@3.1.2/dist"
HADITH_BASE = "https://cdn.jsdelivr.net/gh/AhmedBaset/hadith-json@v1.2.0/db/by_book"

QURAN_FILES = {
    "quran_fr.json": f"{QURAN_BASE}/quran_fr.json",
    "quran_en.json": f"{QURAN_BASE}/quran_en.json",
    "chapters_fr.json": f"{QURAN_BASE}/chapters/index.json",
}

THE_9 = ["abudawud", "bukhari", "darimi", "ibnmajah", "malik", "muslim", "nasai", "tirmidhi", "ahmed"]
FORTIES = ["nawawi40", "qudsi40", "shahwaliullah40"]
OTHER = ["aladab_almufrad", "bulugh_almaram", "mishkat_almasabih", "riyad_assalihin", "shamail_muhammadiyah"]

HADITH_FILES: dict[str, str] = {}
for _slug in THE_9:
    HADITH_FILES[f"{_slug}.json"] = f"{HADITH_BASE}/the_9_books/{_slug}.json"
for _slug in FORTIES:
    HADITH_FILES[f"{_slug}.json"] = f"{HADITH_BASE}/forties/{_slug}.json"
for _slug in OTHER:
    HADITH_FILES[f"{_slug}.json"] = f"{HADITH_BASE}/other_books/{_slug}.json"


def download_all() -> None:
    db.RAW_DIR.mkdir(parents=True, exist_ok=True)
    files = {**QURAN_FILES, **HADITH_FILES}
    for name, url in files.items():
        dest = db.RAW_DIR / name
        if dest.exists():
            print(f"  [OK] {name} (déjà présent)")
            continue
        print(f"  [↓] {name}")
        with urllib.request.urlopen(url, timeout=120) as resp:
            dest.write_bytes(resp.read())
    # Vérification minimale
    for name in ("quran_fr.json", "quran_en.json"):
        data = json.loads((db.RAW_DIR / name).read_text(encoding="utf-8"))
        assert len(data) == 114, f"{name} incomplet"
    print("Téléchargement des données terminé.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingestion des données islamiques")
    parser.add_argument("--download", action="store_true", help="Télécharger les JSON")
    parser.add_argument("--build", action="store_true", help="Construire la base SQLite")
    args = parser.parse_args()

    if args.download:
        download_all()
    if args.build:
        print("Construction de la base SQLite…")
        db.build_database()
        print("Statistiques :", db.stats())
    if not args.download and not args.build:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())