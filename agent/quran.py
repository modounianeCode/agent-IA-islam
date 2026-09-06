"""Lecture et recherche du Coran."""
from __future__ import annotations

import sqlite3

from agent import db


def parse_ref(ref: str) -> tuple[int, int | None, int | None]:
    """Parse '2', '2:255', '18 1-10', '2 : 255'."""
    ref = ref.strip().strip("'\"")
    if ":" in ref:
        surah, _, rest = ref.partition(":")
        ayah = int(rest.strip())
        return int(surah.strip()), ayah, ayah
    parts = ref.split()
    surah = int(parts[0])
    if len(parts) == 1:
        return surah, None, None
    if len(parts) == 2 and "-" in parts[1]:
        a, b = parts[1].split("-")
        return surah, int(a), int(b)
    if len(parts) == 2:
        return surah, int(parts[1]), int(parts[1])
    raise ValueError(f"Référence incomprise : {ref!r}")


def format_ayah(row, with_meta: bool = True) -> str:
    meta = db.get_surah_meta(row["surah"])
    name = meta["transliteration"] if meta else f"Sourate {row['surah']}"
    lines = [f"📖 {name} {row['surah']}:{row['ayah']}"]
    lines.append(row["text_ar"])
    if row["text_fr"]:
        lines.append(f"— {row['text_fr']}")
    return "\n".join(lines)


def lire(surah: int, start: int | None = None, end: int | None = None) -> str:
    meta = db.get_surah_meta(surah)
    if not meta:
        return f"Sourate {surah} introuvable (1–114)."
    title = f"🌸 Sourate {meta['transliteration']} ({meta['name_ar']}) — {meta['name_fr']}"
    title += f" · {meta['type']} · {meta['total_verses']} versets"
    if start is None:
        rows = db.get_surah(surah)
    else:
        rows = db.get_ayah_range(surah, start, end or start)
    if not rows:
        return f"Aucun verset trouvé pour la référence."
    out = [title, "=" * 60]
    if start is None:
        out.append(f"\n1. {rows[0]['text_ar']}\n— {rows[0]['text_fr']}\n")
        out.append(f"{len(rows)}. {rows[-1]['text_ar']}\n— {rows[-1]['text_fr']}\n")
        out.append(f"(… {len(rows) - 2} versets intermédiaires — utilise 'coran {surah} {start}-{end}' pour les afficher)")
    else:
        for row in rows:
            out.append(f"{row['ayah']}. {row['text_ar']}")
            if row["text_fr"]:
                out.append(f"   {row['text_fr']}")
    return "\n".join(out)


def chercher(terms: str) -> str:
    rows = db.search_quran(terms)
    if not rows:
        return f"Aucun verset contenant « {terms} »."
    out = [f"🔎 {len(rows)} verset(s) contenant « {terms} » :", "=" * 60]
    for i, row in enumerate(rows[:12], 1):
        out.append(f"{i}. {format_ayah(row)}")
    return "\n\n".join(out)


def list_surahs() -> str:
    surahs = db.quran_meta()
    out = ["📑 Les 114 sourates :", "=" * 60]
    for s in surahs:
        out.append(f"{s['id']:>3}. {s['transliteration']:<20} ({s['name_fr']})")
    return "\n".join(out)