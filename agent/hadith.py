"""Lecture, recherche et hadiths aléatoires."""
from __future__ import annotations

import sqlite3

from agent import db


def _book_display(book) -> str:
    return f"{book['name_en']} ({book['name_ar']})" if book["name_ar"] else book["name_en"]


def _format(h, fr_text: str | None = None) -> str:
    lines = [f"🕌 Hadith (n°{h['hadith_number']}) — {_book_display(db.resolve_book(h['book_slug']))}"]
    if h["reference"]:
        lines.append(f"Réf. : {h['reference']}")
    if h["arabic"]:
        lines.append("")
        lines.append(h["arabic"])
    if h["text_en"]:
        lines.append("")
        if h["narrator_en"]:
            lines.append(f"📖 Narrateur : {h['narrator_en']}")
        lines.append(h["text_en"])
    if fr_text:
        lines.append("")
        lines.append(f"🇫🇷 {fr_text}")
    return "\n".join(lines)


def random_hadith(book: str | None = None) -> str:
    row = db.random_hadith(book)
    if not row:
        return "Aucun hadith trouvé." + (
            f" (livre « {book} » inconnu ?)" if book else ""
        )
    return _format(row) + "\n\n(la traduction française est proposée par l'IA locale — commande : 'expliquer hadith' dans le chat)"

def search(terms: str, book: str | None = None) -> str:
    rows = db.search_hadith(terms, book=book)
    if not rows:
        return f"Aucun hadith contenant « {terms} »."
    out = [f"🔎 {len(rows)} hadith(s) contenant « {terms} » :", "=" * 60]
    for i, row in enumerate(rows[:10], 1):
        out.append(f"{i}. (n°{row['hadith_number']}) {_book_display(db.resolve_book(row['book_slug']))}")
        out.append(row["text_en"][:300])
        out.append("")
    return "\n".join(out)


def book_list() -> str:
    books = db.list_books()
    out = ["📚 Livres de hadiths disponibles :", "=" * 60]
    for b in books:
        out.append(
            f"- {b['slug']:<24} {b['name_en']} — {b['count']} hadiths"
        )
    out.append("\nRecherche par livre : 'hadith chercher <terme> livre <slug>'")
    return "\n".join(out)


def lookup(book: str, number: int) -> str:
    row = db.get_hadith(book, number)
    if not row:
        return f"Hadith n°{number} du livre « {book} » introuvable."
    return _format(row)