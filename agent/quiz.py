"""Quiz (QCM) générés à partir des textes authentiques de la base locale.

Chaque question est vérifiable : les bonnes réponses proviennent de la BD,
les distracteurs sont d'autres textes réels. Rien n'est « halluciné ».
"""
from __future__ import annotations

import random

from agent import db


def _sample_verses(n: int) -> list:
    import sqlite3

    with db.connect() as conn:
        rows = conn.execute(
            "SELECT a.*, s.transliteration AS st FROM ayahs a"
            " JOIN surahs s ON s.id = a.surah"
            " WHERE a.text_fr IS NOT NULL AND a.text_fr != '' ORDER BY RANDOM() LIMIT ?",
            (n,),
        ).fetchall()
    return rows


def _sample_hadiths(n: int) -> list:
    with db.connect() as conn:
        rows = conn.execute(
            "SELECT h.*, b.name_en AS book_name, b.slug AS book_slug FROM hadiths h"
            " JOIN hadith_books b ON b.id = h.book_id"
            " WHERE h.text_en IS NOT NULL AND h.text_en != ''"
            " ORDER BY RANDOM() LIMIT ?",
            (n,),
        ).fetchall()
    return rows


def build_coran_quiz(n: int = 4) -> list[dict]:
    verses = _sample_verses(n + 3 * n)
    questions = []
    for i in range(n):
        verse = verses[i]
        wrong = [v for v in verses if v["idx"] != verse["idx"]]
        random.shuffle(wrong)
        type_q = random.choice(["traduction", "sourate"])
        if type_q == "traduction" and verse["text_fr"]:
            options = [verse["text_fr"][:120]]
            for w in wrong[:3]:
                options.append(w["text_fr"][:120] if w["text_fr"] else "")
            random.shuffle(options)
            questions.append({
                "kind": "traduction",
                "question": f'{verse["text_ar"]}\n\nComment ce verset est-il traduit (Hamidullah) ?',
                "options": [o or "—" for o in options],
                "answer": options.index(verse["text_fr"][:120]),
                "explain": (f"Coran {verse['surah']}:{verse['ayah']} ({verse['st']}) — "
                            f"{verse['text_fr']}"),
            })
        else:
            other_surahs = db.quran_meta()
            names = [s["transliteration"] for s in other_surahs]
            placeholder = [s["transliteration"] for s in other_surahs if s["id"] == verse["surah"]]
            if not placeholder:
                continue
            correct = placeholder[0]
            wrong_names = [x for x in names if x != correct]
            random.shuffle(wrong_names)
            options = [correct] + wrong_names[:3]
            random.shuffle(options)
            questions.append({
                "kind": "sourate",
                "question": f'{verse["text_fr"]}\n\nDans quelle sourate se trouve ce verset ?',
                "options": options,
                "answer": options.index(correct),
                "explain": f"Coran {verse['surah']}:{verse['ayah']} ({verse['st']})",
            })
    return questions


def build_hadith_quiz(n: int = 4) -> list[dict]:
    hadiths = _sample_hadiths(n + 2 * n)
    questions = []
    for i in range(n):
        h = hadiths[i]
        books = db.list_books()
        correct_book = next((b for b in books if b["slug"] == h["book_slug"]), None)
        if not correct_book:
            continue
        wrong = [b for b in books if b["slug"] != h["book_slug"]]
        random.shuffle(wrong)
        options = [correct_book["name_en"]] + [w["name_en"] for w in wrong[:3]]
        random.shuffle(options)
        snippet = h["text_en"][:180]
        questions.append({
            "kind": "livre",
            "question": f'« …{snippet}… »\n\nDe quel recueil de hadiths provient cet extrait ?',
            "options": options,
            "answer": options.index(correct_book["name_en"]),
            "explain": (f"{h['book_name']} (n°{h['hadith_number']}) — "
                        f"{build_ref_hadith(h)}"),
        })
    return questions


def build_ref_hadith(h) -> str:
    parts = []
    if h["narrator_en"]:
        parts.append(f"Narrateur : {h['narrator_en']}")
    if h["reference"]:
        parts.append(h["reference"])
    return " ; ".join(parts)


def build_quiz(kind: str = "mixte", n: int = 5) -> list[dict]:
    """kind : 'coran' | 'hadith' | 'mixte'"""
    if kind == "coran":
        return build_coran_quiz(n)
    if kind == "hadith":
        return build_hadith_quiz(n)
    half = max(2, n // 2)
    half2 = n - half
    qs = build_coran_quiz(half) + build_hadith_quiz(half2)
    random.shuffle(qs)
    return qs[:n]