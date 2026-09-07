"""Schéma SQLite, remplissage et recherche (FTS5) pour le Coran et les hadiths."""
from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "agent.db"

_ACRONYME = re.compile(r"[^\w\s]", re.UNICODE)

ALIASES = {
    "sahih al-bukhari": "bukhari",
    "bukhari": "bukhari",
    "sahih muslim": "muslim",
    "muslim": "muslim",
    "abu dawud": "abudawud",
    "abou dawoud": "abudawud",
    "tirmidhi": "tirmidhi",
    "tirmizi": "tirmidhi",
    "nasai": "nasai",
    "nasa-i": "nasai",
    "ibn majah": "ibnmajah",
    "malik": "malik",
    "muwatta": "malik",
    "ahmad": "ahmed",
    "ahmed": "ahmed",
    "darimi": "darimi",
    "riyad": "riyad_assalihin",
    "riyad as-salihin": "riyad_assalihin",
    "jardin des vertueux": "riyad_assalihin",
    "shamail": "shamail_muhammadiyah",
    "bulugh": "bulugh_almaram",
    "adab": "aladab_almufrad",
    "adab almufrad": "aladab_almufrad",
    "mishkat": "mishkat_almasabih",
    "nawawi40": "nawawi40",
    "40 nawawi": "nawawi40",
    "an-nawawi": "nawawi40",
    "qudsi": "qudsi40",
    "shah waliullah": "shahwaliullah40",
}


def normalize_fr(text: str) -> str:
    """Enlève les accents/casse pour une recherche insensible aux accents."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return " ".join(_ACRONYME.sub("", nfkd).lower().split())


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
    text = text.replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", text).strip()


def normalize_ar(text: str) -> str:
    """Enlève les voyelles/tanwin/sourates arabes pour une recherche robuste."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    for ch in (
        "\u064b", "\u064c", "\u064d", "\u064e", "\u064f",
        "\u0650", "\u0651", "\u0652", "\u0670", "\u0655",
    ):
        text = text.replace(ch, "")
    for code in range(0x06D6, 0x06EE):  # signes coraniques (ۖ…ۭ) : retirer
        text = text.replace(chr(code), "")
    text = text.replace("آ", "ا").replace("أ", "ا").replace("إ", "ا")
    text = text.replace("\u0671", "ا")
    text = text.replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي")
    text = text.replace("ة", "ه")
    text = text.replace("\u0640", "")
    return " ".join(text.split())


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS surahs (
            id INTEGER PRIMARY KEY,
            name_ar TEXT NOT NULL,
            transliteration TEXT NOT NULL,
            name_fr TEXT,
            type TEXT NOT NULL,
            total_verses INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ayahs (
            idx INTEGER PRIMARY KEY,
            surah INTEGER NOT NULL,
            ayah INTEGER NOT NULL,
            text_ar TEXT NOT NULL,
            text_fr TEXT,
            text_en TEXT,
            norm_fr TEXT,
            norm_ar TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah, ayah);

        CREATE VIRTUAL TABLE IF NOT EXISTS ayahs_fts USING fts5(
            norm_fr, norm_ar, content='', tokenize='unicode61'
        );

        CREATE TABLE IF NOT EXISTS hadith_books (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            name_en TEXT NOT NULL,
            name_ar TEXT
        );

        CREATE TABLE IF NOT EXISTS hadiths (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL REFERENCES hadith_books(id),
            chapter_id INTEGER,
            chapter_en TEXT,
            hadith_number INTEGER,
            arabic TEXT,
            narrator_en TEXT,
            text_en TEXT,
            reference TEXT,
            norm_en TEXT,
            norm_ar TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_hadiths_book ON hadiths(book_id, hadith_number);

        CREATE VIRTUAL TABLE IF NOT EXISTS hadiths_fts USING fts5(
            norm_en, norm_ar, content='', tokenize='unicode61'
        );
        """
    )
    conn.commit()


def _parse_quran_file(path: Path, field: str) -> dict[tuple[int, int], str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for surah in data:
        for verse in surah["verses"]:
            out[(surah["id"], verse["id"])] = verse.get(field, "")
    return out


def build_database() -> None:
    conn = connect()
    for table in ("hadiths_fts", "hadiths", "hadith_books", "ayahs_fts", "ayahs", "surahs"):
        conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    create_schema(conn)

    quran = json.loads((RAW_DIR / "quran_fr.json").read_text(encoding="utf-8"))
    en_map = _parse_quran_file(RAW_DIR / "quran_en.json", "translation")
    global_idx = 0

    for surah in quran:
        conn.execute(
            "INSERT INTO surahs (id, name_ar, transliteration, name_fr, type, total_verses)"
            " VALUES (?,?,?,?,?,?)",
            (
                surah["id"],
                surah["name"],
                surah["transliteration"],
                surah.get("translation", ""),
                surah["type"],
                surah["total_verses"],
            ),
        )
        for verse in surah["verses"]:
            global_idx += 1
            text_fr = verse.get("translation", "")
            text_en = en_map.get((surah["id"], verse["id"]), "")
            conn.execute(
                "INSERT INTO ayahs (idx, surah, ayah, text_ar, text_fr, text_en, norm_fr, norm_ar)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (
                    global_idx,
                    surah["id"],
                    verse["id"],
                    verse["text"],
                    text_fr,
                    text_en,
                    normalize_fr(text_fr),
                    normalize_ar(verse["text"]),
                ),
            )
            conn.execute(
                "INSERT INTO ayahs_fts (rowid, norm_fr, norm_ar) VALUES (?,?,?)",
                (global_idx, normalize_fr(text_fr), normalize_ar(verse["text"])),
            )

    book_files = sorted(RAW_DIR.glob("*.json"))
    book_slugs = [
        "bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah",
        "malik", "ahmed", "darimi",
        "riyad_assalihin", "shamail_muhammadiyah", "bulugh_almaram",
        "aladab_almufrad", "mishkat_almasabih", "nawawi40", "qudsi40",
        "shahwaliullah40",
    ]
    names_en = {
        "bukhari": "Sahih al-Bukhari",
        "muslim": "Sahih Muslim",
        "abudawud": "Sunan Abi Dawud",
        "tirmidhi": "Jami at-Tirmidhi",
        "nasai": "Sunan an-Nasai",
        "ibnmajah": "Sunan Ibn Majah",
        "malik": "Muwatta Malik",
        "ahmed": "Musnad Ahmad",
        "darimi": "Sunan ad-Darimi",
        "riyad_assalihin": "Riyad as-Salihin",
        "shamail_muhammadiyah": "Shamail al-Muhammadiyah",
        "bulugh_almaram": "Bulugh al-Maram",
        "aladab_almufrad": "Al-Adab Al-Mufrad",
        "mishkat_almasabih": "Mishkat al-Masabih",
        "nawawi40": "The Forty Hadith of an-Nawawi",
        "qudsi40": "The Forty Hadith Qudsi",
        "shahwaliullah40": "The Forty Hadith of Shah Waliullah",
    }
    names_ar = {
        "bukhari": "صحيح البخاري",
        "muslim": "صحيح مسلم",
        "abudawud": "سنن أبي داود",
        "tirmidhi": "جامع الترمذي",
        "nasai": "سنن النسائي",
        "ibnmajah": "سنن ابن ماجه",
        "malik": "موطأ مالك",
        "ahmed": "مسند أحمد",
        "darimi": "سنن الدارمي",
        "riyad_assalihin": "رياض الصالحين",
        "shamail_muhammadiyah": "الشمائل المحمدية",
        "bulugh_almaram": "بلوغ المرام",
        "aladab_almufrad": "الأدب المفرد",
        "mishkat_almasabih": "مشكاة المصابيح",
        "nawawi40": "الأربعون النووية",
        "qudsi40": "الأربعون القدسية",
        "shahwaliullah40": "أربعون الشاه ولي الله",
    }

    for i, slug in enumerate(book_slugs, start=1):
        conn.execute(
            "INSERT INTO hadith_books (id, slug, name_en, name_ar) VALUES (?,?,?,?)",
            (i, slug, names_en[slug], names_ar[slug]),
        )

    hid = 0
    for slug in book_slugs:
        path = RAW_DIR / f"{slug}.json"
        if not path.exists():
            continue
        book_id = book_slugs.index(slug) + 1
        data = json.loads(path.read_text(encoding="utf-8"))
        hadith_items = data.get("hadiths", data if isinstance(data, list) else [])
        chapters = {
            c.get("id"): strip_html(c.get("english", ""))
            for c in data.get("chapters", [])
        }
        for item in hadith_items:
            hid += 1
            english = item.get("english") or {}
            arabic = item.get("arabic") or ""
            text_en = strip_html(english.get("text", "")) if isinstance(english, dict) else ""
            narrator = strip_html(english.get("narrator", "")) if isinstance(english, dict) else ""
            norm_en = f"{narrator} {text_en}"
            conn.execute(
                "INSERT INTO hadiths (id, book_id, chapter_id, chapter_en, hadith_number, arabic,"
                " narrator_en, text_en, reference, norm_en, norm_ar)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    hid,
                    book_id,
                    item.get("chapterId"),
                    chapters.get(item.get("chapterId"), ""),
                    item.get("idInBook"),
                    arabic,
                    narrator,
                    text_en,
                    "",
                    normalize_fr(norm_en),
                    normalize_ar(arabic),
                ),
            )
            conn.execute(
                "INSERT INTO hadiths_fts (rowid, norm_en, norm_ar) VALUES (?,?,?)",
                (hid, normalize_fr(norm_en), normalize_ar(arabic)),
            )

    conn.commit()
    conn.close()


def stats() -> dict:
    with connect() as conn:
        surahs = conn.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]
        ayahs = conn.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
        books = conn.execute("SELECT COUNT(*) FROM hadith_books").fetchone()[0]
        hadiths = conn.execute("SELECT COUNT(*) FROM hadiths").fetchone()[0]
    return {"surahs": surahs, "ayahs": ayahs, "books": books, "hadiths": hadiths}


def list_books() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT id, slug, name_en, name_ar,"
            " (SELECT COUNT(*) FROM hadiths h WHERE h.book_id = hadith_books.id) AS count"
            " FROM hadith_books ORDER BY id"
        ).fetchall()


def resolve_book(slug_or_name: str) -> sqlite3.Row | None:
    raw = slug_or_name.strip().lower()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM hadith_books WHERE slug = ?", (raw,)
        ).fetchone()
        if row:
            return row
        if raw in ALIASES:
            return conn.execute(
                "SELECT * FROM hadith_books WHERE slug = ?", (ALIASES[raw],)
            ).fetchone()
        for candidate in conn.execute(
            "SELECT * FROM hadith_books WHERE LOWER(name_en) = ?",
            (raw,),
        ).fetchall():
            return candidate
    return None


def quran_meta() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM surahs ORDER BY id").fetchall()


def get_ayah(surah: int, ayah: int) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM ayahs WHERE surah = ? AND ayah = ?", (surah, ayah)
        ).fetchone()


def get_ayah_range(surah: int, start: int, end: int) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM ayahs WHERE surah = ? AND ayah BETWEEN ? AND ?"
            " ORDER BY ayah",
            (surah, start, end),
        ).fetchall()


def get_surah(surah: int) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM ayahs WHERE surah = ? ORDER BY ayah", (surah,)
        ).fetchall()


def get_surah_meta(surah: int) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM surahs WHERE id = ?", (surah,)
        ).fetchone()


def _fts_query(terms: str) -> str:
    tokens = re.findall(r"[\w]+", terms)
    if not tokens:
        return ""
    return " AND ".join(f'"{t}"*' for t in tokens)


def search_quran(terms: str, limit: int = 12) -> list[sqlite3.Row]:
    q_norm = normalize_fr(terms)
    q_ar = normalize_ar(terms)
    with connect() as conn:
        if q_norm:
            rows = conn.execute(
                "SELECT rowid AS idx FROM ayahs_fts WHERE ayahs_fts MATCH ? LIMIT ?",
                (_fts_query(q_norm), limit),
            ).fetchall()
        else:
            rows = []
        if not rows and q_ar:
            rows = conn.execute(
                "SELECT rowid AS idx FROM ayahs_fts WHERE ayahs_fts MATCH ? LIMIT ?",
                (_fts_query(q_ar), limit),
            ).fetchall()
        ids = [r["idx"] for r in rows]
        if ids:
            placeholders = ",".join("?" for _ in ids)
            return conn.execute(
                f"SELECT * FROM ayahs WHERE idx IN ({placeholders})",
                ids,
            ).fetchall()
        return []


def search_hadith(terms: str, book: str | None = None, limit: int = 10) -> list[sqlite3.Row]:
    q_norm = normalize_fr(terms)
    q_ar = normalize_ar(terms)
    with connect() as conn:
        base = "SELECT h.*, b.slug AS book_slug, b.name_en AS book_name FROM hadiths h"
        base += " JOIN hadith_books b ON b.id = h.book_id"
        if book:
            base += " WHERE b.slug = ?"
        rows = []
        if q_norm:
            sql = "SELECT rowid FROM hadiths_fts WHERE hadiths_fts MATCH ?"
            if book:
                sql += " AND rowid IN (SELECT id FROM hadiths WHERE book_id = (SELECT id FROM hadith_books WHERE slug = ?))"
            rows = conn.execute(sql + " LIMIT ?", (_fts_query(q_norm), *((book,) if book else ()), limit)).fetchall()
        elif q_ar:
            sql = "SELECT rowid FROM hadiths_fts WHERE hadiths_fts MATCH ?"
            if book:
                sql += " AND rowid IN (SELECT id FROM hadiths WHERE book_id = (SELECT id FROM hadith_books WHERE slug = ?))"
            rows = conn.execute(sql + " LIMIT ?", (_fts_query(q_ar), *((book,) if book else ()), limit)).fetchall()
        ids = [r["rowid"] for r in rows]
        if ids:
            placeholders = ",".join("?" for _ in ids)
            sql = (
                f"SELECT h.*, b.slug AS book_slug, b.name_en AS book_name"
                f" FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
                f" WHERE h.id IN ({placeholders})"
            )
            return conn.execute(sql, ids).fetchall()
        return []


def get_hadith(book: str, number: int) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(
            "SELECT h.*, b.slug AS book_slug, b.name_en AS book_name"
            " FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
            " WHERE b.slug = ? AND h.hadith_number = ?",
            (book, number),
        ).fetchone()


def ayah_exists(surah: int, ayah: int) -> bool:
    """Vérifie qu'un verset (sourate:verset) existe réellement dans la base."""
    with connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM ayahs WHERE surah = ? AND ayah = ?",
            (surah, ayah),
        ).fetchone()
    return row is not None


def surah_total_verses(surah: int) -> int | None:
    """Retourne le nombre de versets d'une sourate, ou None si inexistante."""
    with connect() as conn:
        row = conn.execute(
            "SELECT total_verses FROM surahs WHERE id = ?", (surah,)
        ).fetchone()
    return row["total_verses"] if row else None


def hadith_exists(book: str, number: int) -> bool:
    """Vérifie qu'un hadith (livre + n°) existe réellement dans la base."""
    with connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
            " WHERE b.slug = ? AND h.hadith_number = ?",
            (book, number),
        ).fetchone()
    return row is not None


def random_hadith(book: str | None = None) -> sqlite3.Row:
    import random

    with connect() as conn:
        if book:
            return conn.execute(
                "SELECT h.*, b.slug AS book_slug, b.name_en AS book_name"
                " FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
                " WHERE b.slug = ? ORDER BY RANDOM() LIMIT 1",
                (book,),
            ).fetchone()
        return conn.execute(
            "SELECT h.*, b.slug AS book_slug, b.name_en AS book_name"
            " FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
            " ORDER BY RANDOM() LIMIT 1"
        ).fetchone()