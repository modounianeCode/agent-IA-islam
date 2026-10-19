"""Interface graphique web locale (Flask) de l'assistant islamique.

Lancement :
    python webapp.py
    # ou
    python -m agent.web

L'application ne contacte Internet que pour les outils en ligne
(hijri, prières, qibla, tafsir). Coran, hadiths, leçons et quiz
fonctionnent entièrement hors-ligne depuis data/agent.db.
"""
from __future__ import annotations

import os
from datetime import date
from functools import lru_cache
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from agent import api, curriculum, db, quran, quiz

BASE_DIR = Path(__file__).resolve().parent.parent

PRAYER_LABELS = {
    "imsak": "Imsak",
    "fajr": "Aube (Fajr)",
    "sunrise": "Lever du soleil",
    "dhuhr": "Midi (Dhuhr)",
    "asr": "Après-midi (Asr)",
    "maghrib": "Coucher du soleil (Maghrib)",
    "isha": "Nuit (Isha)",
}

DAILY_AYAHS = [
    (2, 255),
    (3, 8),
    (13, 28),
    (39, 53),
    (94, 5),
    (65, 3),
    (2, 286),
    (24, 35),
    (49, 13),
    (17, 80),
    (20, 114),
    (40, 60),
]


@lru_cache(maxsize=1)
def _stats() -> dict:
    return db.stats()


def _row_to_dict(row) -> dict | None:
    return dict(row) if row is not None else None


def _surah_dict(surah_id: int) -> dict | None:
    return _row_to_dict(db.get_surah_meta(surah_id))


def _hadith_dict(row) -> dict | None:
    """Convertit une ligne hadith + jointure livre en dict prêt pour le template."""
    if row is None:
        return None
    data = dict(row)
    data.setdefault("book_name", data.get("book_slug", "Hadith"))
    return data


def _daily_ayah() -> dict:
    today = date.today()
    surah_id, ayah_id = DAILY_AYAHS[today.toordinal() % len(DAILY_AYAHS)]
    row = db.get_ayah(surah_id, ayah_id)
    return {
        "row": _row_to_dict(row),
        "meta": _surah_dict(surah_id),
        "surah": surah_id,
        "ayah": ayah_id,
    }


def _daily_hadith() -> dict | None:
    with db.connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM hadiths").fetchone()[0]
        if not total:
            return None
        offset = date.today().toordinal() % total
        row = conn.execute(
            "SELECT h.*, b.slug AS book_slug, b.name_en AS book_name"
            " FROM hadiths h JOIN hadith_books b ON b.id = h.book_id"
            " ORDER BY h.id LIMIT 1 OFFSET ?",
            (offset,),
        ).fetchone()
    return _hadith_dict(row)


def _progress_data() -> dict:
    progress = curriculum.load_progress()
    done = set(progress.get("completed", []))
    total = len(curriculum.LESSONS)
    return {
        "completed": done,
        "count": len(done),
        "total": total,
        "percent": round(len(done) / total * 100) if total else 0,
        "next": curriculum.next_lesson(progress),
        "last": progress.get("last"),
    }


def _lesson_references(lesson: dict) -> tuple[list[dict], list[dict]]:
    quran_refs: list[dict] = []
    for ref in lesson.get("quran", []):
        try:
            surah_id, ayah_id, _ = quran.parse_ref(str(ref.get("ref", "")))
            if ayah_id is None:
                ayah_id = 1
            row = db.get_ayah(surah_id, ayah_id)
        except (ValueError, TypeError):
            row = None
            surah_id, ayah_id = None, None
        quran_refs.append(
            {
                "ref": ref.get("ref", ""),
                "note": ref.get("note", ""),
                "row": _row_to_dict(row),
                "meta": _surah_dict(surah_id) if surah_id else None,
            }
        )

    hadith_refs: list[dict] = []
    for ref in lesson.get("hadith", []):
        row = None
        book = ref.get("book")
        number = ref.get("number")
        if book and number:
            row = db.get_hadith(book, number)
        if row is None and ref.get("term"):
            rows = db.search_hadith(str(ref["term"]), book=book, limit=1)
            row = rows[0] if rows else None
        hadith_refs.append(
            {
                "book": book,
                "number": number,
                "note": ref.get("note", ""),
                "row": _hadith_dict(row),
            }
        )
    return quran_refs, hadith_refs


def _parse_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def _tools_result(action: str, form) -> tuple[dict | None, str | None]:
    """Exécute un outil en ligne et retourne (résultat, erreur)."""
    if action == "hijri":
        try:
            data = api.hijri()
        except api.ApiError as exc:
            return None, str(exc)
        events = None
        try:
            events = api.islamic_events()
        except api.ApiError:
            pass
        return {"kind": "hijri", "data": data, "events": events}, None

    if action == "prieres":
        lat = _parse_float(form.get("lat"))
        lon = _parse_float(form.get("lon"))
        place = None
        timezone = (form.get("timezone") or "").strip() or None
        if lat is not None and lon is not None:
            place = f"{lat:g}, {lon:g}"
        else:
            city = (form.get("city") or "").strip()
            country = (form.get("country") or "").strip() or None
            if not city:
                return None, "Indique une ville ou des coordonnées (latitude, longitude)."
            try:
                info = api.geocode(city, country)
            except api.ApiError as exc:
                return None, str(exc)
            if not info:
                return None, f"Ville « {city} » introuvable (géocodage Open-Meteo)."
            lat, lon = info["latitude"], info["longitude"]
            timezone = timezone or info.get("timezone")
            place = f"{info.get('name', city)} ({info.get('country', '')})".strip(" ()")
        try:
            data = api.prayer_times(lat, lon, timezone=timezone)
        except api.ApiError as exc:
            return None, str(exc)
        times = data.get("prayer_times", {})
        ordered = [
            (label, times[key]) for key, label in PRAYER_LABELS.items() if key in times
        ]
        return {
            "kind": "prieres",
            "place": place,
            "data": data,
            "times": ordered,
        }, None

    if action == "qibla":
        lat = _parse_float(form.get("lat"))
        lon = _parse_float(form.get("lon"))
        if lat is None or lon is None:
            return None, "Indique une latitude et une longitude (ex : 14.69 / -17.44)."
        try:
            data = api.qibla(lat, lon)
        except api.ApiError as exc:
            return None, str(exc)
        return {"kind": "qibla", "data": data}, None

    if action == "tafsir":
        raw_ref = (form.get("ref") or "").strip()
        if not raw_ref:
            return None, "Indique une référence (ex : 2:255 ou 1)."
        try:
            surah_id, ayah_id, _ = quran.parse_ref(raw_ref)
        except ValueError:
            return None, "Référence incomprise. Exemples : 2:255, 1, 18 1-10."
        if ayah_id is None:
            ayah_id = 1
        meta = db.get_surah_meta(surah_id)
        if not meta:
            return None, f"Sourate {surah_id} introuvable (1–114)."
        if not 1 <= ayah_id <= meta["total_verses"]:
            return (
                None,
                f"Le verset {surah_id}:{ayah_id} n'existe pas "
                f"(la sourate a {meta['total_verses']} versets).",
            )
        try:
            data = api.tafsir(surah_id, ayah_id)
        except api.ApiError as exc:
            return None, str(exc)
        text = ((data or {}).get("tafsir") or {}).get("text", "").strip()
        return {
            "kind": "tafsir",
            "surah": surah_id,
            "ayah": ayah_id,
            "meta": dict(meta),
            "row": _row_to_dict(db.get_ayah(surah_id, ayah_id)),
            "text": text,
        }, None

    return None, None


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config["SECRET_KEY"] = os.environ.get(
        "AGENT_IA_SECRET_KEY", "agent-ia-islam-local"
    )

    @app.context_processor
    def inject_globals():
        return {
            "global_stats": _stats(),
            "current_year": date.today().year,
            "sidebar_progress": _progress_data(),
        }

    # ── Accueil ────────────────────────────────────────────────
    @app.route("/")
    def index():
        progress = _progress_data()
        return render_template(
            "index.html",
            progress=progress,
            daily_ayah=_daily_ayah(),
            daily_hadith=_daily_hadith(),
            active="index",
        )

    # ── Coran ──────────────────────────────────────────────────
    @app.route("/coran")
    def coran():
        query = (request.args.get("q") or "").strip()
        surah_id = request.args.get("sourate", type=int) or 1
        start = request.args.get("debut", type=int)
        end = request.args.get("fin", type=int)

        surahs = [dict(s) for s in db.quran_meta()]
        search_results: list[dict] | None = None
        selected = None
        verses: list[dict] = []
        error = None

        if query:
            rows = db.search_quran(query, limit=30)
            search_results = []
            for row in rows:
                item = dict(row)
                item["meta"] = _surah_dict(item["surah"])
                search_results.append(item)
        else:
            meta = db.get_surah_meta(surah_id)
            if not meta:
                abort(404)
            selected = dict(meta)
            if start is not None:
                if end is None:
                    end = start
                start = max(1, min(start, selected["total_verses"]))
                end = max(start, min(end, selected["total_verses"]))
                verses = [dict(r) for r in db.get_ayah_range(surah_id, start, end)]
            else:
                verses = [dict(r) for r in db.get_surah(surah_id)]

        return render_template(
            "coran.html",
            active="coran",
            surahs=surahs,
            selected=selected,
            verses=verses,
            query=query,
            search_results=search_results,
            start=start,
            end=end,
            error=error,
        )

    # ── Hadiths ────────────────────────────────────────────────
    @app.route("/hadiths")
    def hadiths():
        books = [dict(b) for b in db.list_books()]
        query = (request.args.get("q") or "").strip()
        book = (request.args.get("livre") or "").strip()
        number = (request.args.get("numero") or "").strip()
        random_flag = request.args.get("hasard")
        error = None
        results: list[dict] = []
        single = None

        if book:
            resolved = db.resolve_book(book)
            book = resolved["slug"] if resolved else ""
            if not book:
                error = f"Livre inconnu : « {request.args.get('livre')} »."

        if number and not error:
            if not book:
                book = "bukhari"
            try:
                wanted = int(number)
            except ValueError:
                error = "Le numéro du hadith doit être un entier."
            else:
                single = _hadith_dict(db.get_hadith(book, wanted))
                if single is None:
                    error = f"Hadith n°{wanted} introuvable dans « {book} »."
        elif query and not error:
            rows = db.search_hadith(query, book=book or None, limit=25)
            results = [d for d in (_hadith_dict(r) for r in rows) if d]
            if not results:
                error = f"Aucun hadith trouvé pour « {query} »."
        elif random_flag and not error:
            single = _hadith_dict(db.random_hadith(book or None))
            if single is None:
                error = "Aucun hadith trouvé."

        return render_template(
            "hadiths.html",
            active="hadiths",
            books=books,
            query=query,
            book=book,
            number=number,
            results=results,
            single=single,
            error=error,
        )

    # ── Apprentissage ──────────────────────────────────────────
    @app.route("/apprendre")
    def apprendre():
        progress = _progress_data()
        modules: list[dict] = []
        current = None
        for lesson in curriculum.LESSONS:
            if current is None or current["number"] != lesson["module"]:
                current = {
                    "number": lesson["module"],
                    "title": lesson["module_title"],
                    "lessons": [],
                }
                modules.append(current)
            current["lessons"].append(
                {
                    **lesson,
                    "done": lesson["id"] in progress["completed"],
                }
            )
        for module in modules:
            module["done"] = sum(1 for l in module["lessons"] if l["done"])
            module["total"] = len(module["lessons"])
            module["percent"] = round(module["done"] / module["total"] * 100)
        return render_template(
            "apprendre.html",
            active="apprendre",
            modules=modules,
            progress=progress,
        )

    @app.route("/apprendre/<lesson_id>")
    def lecon(lesson_id: str):
        lesson = curriculum.lesson_by_id(lesson_id)
        if not lesson:
            abort(404)
        progress = _progress_data()
        quran_refs, hadith_refs = _lesson_references(lesson)
        index = next(
            (i for i, item in enumerate(curriculum.LESSONS) if item["id"] == lesson_id),
            0,
        )
        previous_lesson = curriculum.LESSONS[index - 1] if index > 0 else None
        following_lesson = (
            curriculum.LESSONS[index + 1]
            if index + 1 < len(curriculum.LESSONS)
            else None
        )
        return render_template(
            "lecon.html",
            active="apprendre",
            lesson=lesson,
            done=lesson_id in progress["completed"],
            progress=progress,
            quran_refs=quran_refs,
            hadith_refs=hadith_refs,
            previous_lesson=previous_lesson,
            following_lesson=following_lesson,
        )

    @app.route("/apprendre/<lesson_id>/terminer", methods=["POST"])
    def terminer_lecon(lesson_id: str):
        if not curriculum.lesson_by_id(lesson_id):
            abort(404)
        progress = curriculum.complete(lesson_id)
        following = curriculum.next_lesson(progress)
        flash(f"Leçon « {lesson_id} » validée. Bravo !", "success")
        if following:
            return redirect(url_for("lecon", lesson_id=following["id"]))
        return redirect(url_for("apprendre"))

    # ── Quiz ───────────────────────────────────────────────────
    @app.route("/quiz")
    def quiz_page():
        return render_template(
            "quiz.html",
            active="quiz",
            progress=_progress_data(),
        )

    @app.route("/api/quiz")
    def api_quiz():
        kind = (request.args.get("type") or "mixte").lower()
        if kind not in ("coran", "hadith", "mixte"):
            kind = "mixte"
        try:
            count = int(request.args.get("n", 5))
        except ValueError:
            count = 5
        count = max(1, min(count, 20))
        questions = quiz.build_quiz(kind, count)
        if not questions:
            return jsonify({"error": "Impossible de générer un quiz (base vide ?)."}), 500
        return jsonify({"questions": questions})

    # ── Outils en ligne ────────────────────────────────────────
    @app.route("/outils", methods=["GET", "POST"])
    def outils():
        action = (
            request.form.get("action") or request.args.get("action") or ""
        ).strip()
        result = None
        error = None
        if action:
            result, error = _tools_result(action, request.form)
        return render_template(
            "outils.html",
            active="outils",
            action=action,
            result=result,
            error=error,
        )

    # ── Erreurs ────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(_exc):
        return (
            render_template(
                "404.html",
                active="",
            ),
            404,
        )

    @app.errorhandler(500)
    def server_error(_exc):
        return (
            render_template(
                "500.html",
                active="",
            ),
            500,
        )

    return app


app = create_app()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Interface web de l'assistant islamique")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
