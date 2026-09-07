"""Interface interactive en ligne de commande."""
from __future__ import annotations

import sys

from agent import db, hadith, llm, quran, quiz, curriculum

HELP = """\
━━━ Agent IA — Apprendre l'Islam (niveau intermédiaire) ━━━

📖 CORAN
  coran 2                     → sourate 2 (aperçu)
  coran 2:255                 → verset précis
  coran 18 1-10               → plage de versets
  coran chercher <terme>      → recherche dans la traduction française
  coran list                  → liste des 114 sourates
  expliquer 2:255             → explication pédagogique du verset par l'IA

🌙 HADITH
  hadith hasard               → hadith au hasard
  hadith hasard bukhari       → hadith au hasard dans un livre
  hadith chercher <terme>     → recherche parmi les hadiths
  hadith chercher <terme> livre bukhari
  hadith livre bukhari        → fiche d'un livre
  hadith hadith bukhari 1     → hadith précis (livre + n°)
  hadith livres               → liste des livres

🎓 APPRENTISSAGE
  apprendre                   → plan et progression
  apprendre lecon <id>        → suivre une leçon (ex : apprendre lecon fiq2)
  apprendre terminer <id>     → valider une leçon

❓ QUIZ
  quiz                        → quiz mixte (5 questions)
  quiz coran / quiz hadith    → quiz ciblé
  quiz coran 10               → 10 questions

📚 CONNAISSANCES ISLAMIQUES
  noms <n>                    → noms d'Allah (ex : noms 1-10, noms rahman)
  piliers                     → les 5 piliers de l'islam
  foi                         → les 6 piliers de la foi
  prophètes                   → liste des prophètes mentionnés dans le Coran
  sourates importantes        → les sourates majeures

🇸🇳 WOLOF
  wolof coran 1:1             → traduire le verset 1:1 en wolof
  wolof hadith bukhari 1      → traduire le hadith bukhari n°1 en wolof
  wolof <texte>               → traduire un texte libre en wolof

🗣️ IA
  demander <question>         → réponse appuyée sur la base locale
  demander explique le verset du Trône
  demander qu'est-ce que la taqwa ?
  demander quel est le jeûne du Ramadan ?
  demander traduis ce verset en wolof

❌ quitter / exit
"""


def resolve_book_input(user_input: str) -> str | None:
    """Résout un nom de livre tapé par l'utilisateur vers un slug de la BD."""
    raw = user_input.strip().lower()
    if not raw:
        return None
    row = db.resolve_book(raw)
    if row:
        return row["slug"]
    books = db.list_books()
    for b in books:
        if raw in b["name_en"].lower() or raw in b["name_ar"]:
            return b["slug"]
    for b in books:
        if b["slug"].startswith(raw) or raw.startswith(b["slug"]):
            return b["slug"]
    return None


def _grounding_context(question: str, limit: int = 8) -> str:
    """Recherche contextuelle enrichie pour répondre aux questions."""
    parts = []
    
    # Recherche dans le Coran
    quran_rows = db.search_quran(question, limit=limit)
    for row in quran_rows[:4]:
        meta = db.get_surah_meta(row["surah"])
        parts.append(
            f"[Coran {row['surah']}:{row['ayah']} — {meta['transliteration']}]\n"
            f"{row['text_ar']}\n{row['text_fr']}"
        )
    
    # Recherche dans les hadiths
    hadith_rows = db.search_hadith(question, limit=limit)
    for row in hadith_rows[:4]:
        parts.append(
            f"[Hadith — {row['book_name']} n°{row['hadith_number']}]\n{row['text_en'][:400]}"
        )
    
    # Recherche par mots-clés supplémentaires pour les questions générales
    keywords = question.lower().split()
    extended_terms = []
    
    # Ajouter des termes associés pour améliorer la recherche
    word_map = {
        "prière": ["salat", "prier", "prieres"],
        "prières": ["salat", "prier"],
        "jeûne": ["ramadan", "sawm"],
        "jeune": ["ramadan", "sawm"],
        "aumône": ["zakat", "donner"],
        "zakat": ["zakat", "aumone"],
        "pèlerinage": ["hajj", "mecque"],
        "hajj": ["hajj", "pelerinage"],
        "pardon": ["tawbah", "repentir"],
        "repentir": ["tawbah", "pardon"],
        "patience": ["sabr", "patient"],
        "gratitude": ["shukr", "remercier"],
        "miséricorde": ["rahma", "rahman", "rahim"],
        "pitié": ["rahma", "misericorde"],
        "sagesse": ["hikma", "sage"],
        "science": ["ilm", "savoir"],
        "connaissance": ["ilm", "savoir"],
        "foi": ["iman", "croyance"],
        "croyance": ["iman", "foi"],
        "islam": ["soumission", "paix"],
        "prophète": ["rasul", "messager"],
        "messager": ["rasul", "prophete"],
        "allah": ["dieu", "seigneur"],
        "dieu": ["allah", "seigneur"],
        "paradis": ["jannah", "eden"],
        "enfer": ["jahannam", "gehenne"],
        "anges": ["malak", "ange"],
        "diable": ["shaytan", "iblis"],
        "satan": ["shaytan", "iblis"],
    }
    
    for word in keywords:
        if word in word_map:
            extended_terms.extend(word_map[word])
    
    if extended_terms:
        extended_query = " ".join(extended_terms[:3])
        extra_quran = db.search_quran(extended_query, limit=3)
        for row in extra_quran[:2]:
            if row not in quran_rows:
                meta = db.get_surah_meta(row["surah"])
                parts.append(
                    f"[Coran {row['surah']}:{row['ayah']} — {meta['transliteration']}]\n"
                    f"{row['text_ar']}\n{row['text_fr']}"
                )
        
        extra_hadith = db.search_hadith(extended_query, limit=3)
        for row in extra_hadith[:2]:
            if row not in hadith_rows:
                parts.append(
                    f"[Hadith — {row['book_name']} n°{row['hadith_number']}]\n{row['text_en'][:400]}"
                )
    
    return "\n\n".join(parts)


def dispatch(args: list[str], interactive: bool = False) -> str | int:
    if not args:
        return HELP
    cmd = args[0].lower()

    # ── CORAN ──────────────────────────────────────────────
    if cmd == "coran":
        if len(args) < 2:
            return "Usage : coran <ref> | coran chercher <terme> | coran list"
        sub = args[1].lower()
        if sub == "list":
            return quran.list_surahs()
        if sub == "chercher":
            return quran.chercher(" ".join(args[2:]))
        try:
            s, a, b = quran.parse_ref(" ".join(args[1:]))
            return quran.lire(s, a, b) if a is not None else quran.lire(s)
        except ValueError:
            return quran.chercher(" ".join(args[1:]))

    if cmd == "expliquer":
        if len(args) < 2:
            return "Usage : expliquer <sourate:verset> (ex : expliquer 2:255)"
        try:
            surah, start, end = quran.parse_ref(" ".join(args[1:]))
        except ValueError:
            return "Référence incomprise. Exemple : expliquer 2:255"
        meta = db.get_surah_meta(surah)
        if not meta:
            return f"Sourate {surah} introuvable."
        rows = db.get_ayah_range(surah, max(1, start - 2), min(meta["total_verses"], end + 2))
        ctx_lines = []
        for row in rows:
            marker = "" if row["ayah"] == start else " "
            ctx_lines.append(
                f"[v{row['ayah']}]{marker} {row['text_ar']}\n   {row['text_fr']}"
            )
        context = "\n".join(ctx_lines)
        if not llm.is_available():
            return (
                "Ollama (modèle qwen2.5:7b) n'est pas lancé. Lance d'abord le serveur "
                "(voir setup.sh), puis réessaie. Voici le verset sans explication :\n"
                + quran.lire(surah, start, end)
            )
        print(
            f"🤖 Explication du verset Coran {surah}:{start} — "
            f"{meta['transliteration']} (l'IA génère, ça peut prendre un moment)…\n"
        )
        prompt = (
            f"Explique-moi pédagogiquement le verset Coran {surah}:{start} pour un étudiant de niveau intermédiaire :\n"
            "1) sens du verset, 2) contexte (si connu), 3) 2–3 leçons pratiques, 4) références croisées Coran/Sunna solides.\n"
            "RÈGLE ABSOLUE : ne cite que le verset {surah}:{start} fourni ci-dessous. "
            "Tu ne dois JAMAIS écrire un nom de livre ni un numéro de hadith (ex. « Bukhari n°6648 »). "
            "À la place de tout hadith, écris exactement : « hadith authentique (référence à vérifier) ». "
            "Réponds en français."
        )
        msgs = llm.teacher_messages(prompt, context)
        llm.chat(msgs, strict=True)
        return ""

    # ── HADITH ─────────────────────────────────────────────
    if cmd == "hadith":
        if len(args) < 2:
            return "Usage : hadith hasard [livre] | hadith chercher ... | hadith hadith <livre> <n> | hadith livres"
        sub = args[1].lower()
        if sub == "livres" or sub == "liste":
            return hadith.book_list()
        if sub == "hasard":
            book = resolve_book_input(args[2]) if len(args) > 2 else None
            if len(args) > 2 and book is None:
                return f"Livre inconnu : « {args[2]} ». Voir 'hadith livres'."
            res = hadith.random_hadith(book)
            if interactive:
                print(res)
                a = input("\nVeux-tu une explication/traduction en français (f), en wolof (w) ou rien (n) ? ").strip().lower()
                row = db.random_hadith(book)
                if a in ("o", "oui", "f", "fr"):
                    return _explain_hadith_from_row(row)
                if a in ("w", "wolof"):
                    return _translate_to_wolof(
                        f"Narrateur : {row['narrator_en'] or '?'}\n{row['text_en']}\n{row['arabic'] or ''}",
                        f"Hadith — {row['book_name']} n°{row['hadith_number']}",
                    )
            return res
        if sub == "chercher":
            if len(args) < 3:
                return "Usage : hadith chercher <terme> [livre <slug>]"
            book = None
            terms = args[2:]
            if "livre" in terms:
                i = terms.index("livre")
                book = resolve_book_input(terms[i + 1]) if len(terms) > i + 1 else None
                if len(terms) > i + 1 and book is None:
                    return f"Livre inconnu : « {terms[i+1]} »."
                terms = terms[:i]
            return hadith.search(" ".join(terms), book=book)
        if sub == "hadith":
            if len(args) < 4:
                return "Usage : hadith hadith <livre> <n°> (ex : hadith hadith bukhari 1)"
            book = resolve_book_input(args[2])
            if not book:
                return f"Livre inconnu : « {args[2]} »."
            try:
                n = int(args[3])
            except ValueError:
                return "Le n° doit être un entier."
            res = hadith.lookup(book, n)
            if interactive:
                print(res)
                a = input("\nVeux-tu une explication/traduction en français (f), en wolof (w) ou rien (n) ? ").strip().lower()
                row = db.get_hadith(book, n)
                if a in ("o", "oui", "f", "fr") and row:
                    return _explain_hadith_from_row(row)
                if a in ("w", "wolof") and row:
                    return _translate_to_wolof(
                        f"Narrateur : {row['narrator_en'] or '?'}\n{row['text_en']}\n{row['arabic'] or ''}",
                        f"Hadith — {row['book_name']} n°{row['hadith_number']}",
                    )
            return res
        if sub == "livre":
            if len(args) < 3:
                return "Usage : hadith livre <slug> — ex : hadith livre riyad_assalihin"
            book = resolve_book_input(args[2])
            if not book:
                return f"Livre inconnu : « {args[2]} ». Voir 'hadith livres'."
            row = db.resolve_book(book)
            count = db.connect().execute(
                "SELECT COUNT(*) FROM hadiths WHERE book_id=?", (row["id"],)
            ).fetchone()[0]
            sample = db.connect().execute(
                "SELECT h.*, b.name_en AS book_name FROM hadiths h"
                " JOIN hadith_books b ON b.id=h.book_id WHERE h.book_id=? LIMIT 3",
                (row["id"],),
            ).fetchall()
            out = [f"📚 {row['name_en']} ({row['name_ar']}) — {count} hadiths", "=" * 60]
            for h in sample:
                out.append(f"- n°{h['hadith_number']} : {h['text_en'][:120]}…")
            return "\n".join(out)
        return "Sous-commande hadith inconnue. Tape 'aide'."

    # ── APPRENTISSAGE ──────────────────────────────────────
    if cmd == "apprendre" or cmd == "learn":
        if len(args) >= 3 and args[1].lower() == "lecon":
            return curriculum.show_lesson(args[2])
        if len(args) >= 3 and args[1].lower() == "terminer":
            if args[2] not in [l["id"] for l in curriculum.LESSONS]:
                return f"Leçon « {args[2]} » introuvable."
            progress = curriculum.complete(args[2])
            nxt = curriculum.next_lesson(progress)
            lines = [f"✅ Leçon « {args[2]} » validée. Bravo !"]
            if nxt:
                lines.append(f"\nProchaine leçon proposée : {nxt['id']} — {nxt['title']}")
                lines.append("('apprendre lecon " + nxt['id'] + "')")
            return "\n".join(lines)
        return curriculum.overview()

    # ── QUIZ ───────────────────────────────────────────────
    if cmd == "quiz":
        kind = "mixte"
        n = 5
        if len(args) > 1:
            arg = args[1].lower()
            if arg in ("coran", "hadith", "mixte"):
                kind = arg
                if len(args) > 2 and args[2].isdigit():
                    n = int(args[2])
            elif arg.isdigit():
                n = int(arg)
        if not interactive:
            # mode non interactif : afficher uniquement la première question
            qs = quiz.build_quiz(kind, n)
            if not qs:
                return "Impossible de générer un quiz (base vide ?)."
            q = qs[0]
            out = [f"❓ {q['question']}", ""]
            out += [f"   {chr(97 + i)}. {opt}" for i, opt in enumerate(q["options"])]
            out += ["", f"✔ {q['explain']}"]
            return "\n".join(out)
        return _run_quiz(kind, n)

    # ── CONNAISSANCES ISLAMIQUES ──────────────────────────────
    if cmd == "noms":
        return _list_names(args[1:])
    
    if cmd == "piliers":
        return _list_pillars()
    
    if cmd == "foi":
        return _list_faith_pillars()
    
    if cmd == "prophètes" or cmd == "prophetes":
        return _list_prophets()
    
    if cmd == "sourates" or cmd == "sourates importantes":
        return _list_important_surahs()
    
    # ── WOLOF (traductions IA) ──────────────────────────────
    if cmd == "wolof":
        return _wolof_dispatch(args[1:])
    
    # ── DEMANDER (IA) ──────────────────────────────────────
    if cmd in ("demander", "demande", "ask"):
        if len(args) < 2:
            return "Usage : demander <votre question> (ex : demander qu'est-ce que la taqwa ?)"
        question = " ".join(args[1:])
        return ask_llm(question)

    if cmd in ("aide", "help", "?"):
        return HELP
    if cmd in ("quitter", "exit", "quit"):
        return "__EXIT__"
    return f"Commande inconnue : {cmd!r}. Tape 'aide'."


def _run_quiz(kind: str, n: int) -> str:
    questions = quiz.build_quiz(kind, n)
    if not questions:
        return "Impossible de générer un quiz (base vide ?)."
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}/{len(questions)}")
        print(q["question"])
        letters = "abcd"
        for j, opt in enumerate(q["options"]):
            print(f"   {letters[j]}. {opt}")
        while True:
            rep = input("Ta réponse (a/b/c/d) : ").strip().lower()
            if rep in letters:
                break
            print("Réponds par a, b, c ou d.")
        idx = letters.index(rep)
        if idx == q["answer"]:
            print("✅ Bonne réponse !")
            score += 1
        else:
            good = letters[q["answer"]]
            print(f"❌ Mauvaise réponse. La bonne était {good}.")
        print(f"ℹ {q['explain']}")
    print(f"\n━━━ Score : {score}/{len(questions)} ━━━")
    if score / len(questions) >= 0.8:
        print("Excellent ! Les révisions portent leurs fruits.")
    elif score / len(questions) >= 0.5:
        print("Bon résultat. Relis les leçons 'apprendre' et retente.")
    else:
        print("Continue ! Suis le plan 'apprendre' puis refais ce quiz.")
    return ""


def _explain_hadith_from_row(row) -> str:
    if not llm.is_available():
        return (
            "\n(Ollama n'est pas lancé — impossible de traduire maintenant. "
            "Lance le serveur puis tape 'demander explique ce hadith'.)"
        )
    print("\n🤖 Traduction/Explication en français (IA locale)…\n")
    context = (
        f"[Hadith — {row['book_name']} n°{row['hadith_number']}]\n"
        f"Narrateur : {row['narrator_en'] or '?'}\n{row['arabic'] or ''}\n{row['text_en']}"
    )
    prompt = (
        "Traduis en français ce hadith de façon fidèle puis, en 3 points, ce qu'on en retient "
        "pratiquement pour aujourd'hui. Cite le livre et le n°."
    )
    llm.chat(llm.teacher_messages(prompt, context), strict=True)
    return ""


def _list_names(args: list[str]) -> str:
    """Affiche les noms d'Allah."""
    names = [
        ("Ar-Rahman", "Le Tout Miséricordieux"),
        ("Ar-Rahim", "Le Très Miséricordieux"),
        ("Al-Malik", "Le Roi"),
        ("Al-Quddus", "Le Saint"),
        ("As-Salam", "La Paix"),
        ("Al-Mu'min", "Le Grant de sécurité"),
        ("Al-Muhaymin", "Le Protecteur"),
        ("Al-Aziz", "Le Tout Puissant"),
        ("Al-Jabbar", "Le Redresseur"),
        ("Al-Mutakabbir", "Le Suprême"),
        ("Al-Khaliq", "Le Créateur"),
        ("Al-Bari", "Le Fabricateur"),
        ("Al-Musawwir", "Le Façonneur"),
        ("Al-Ghaffar", "Le Pardonneur"),
        ("Al-Qahhar", "Le Dominateur"),
        ("Al-Wahhab", "Le Donateur"),
        ("Ar-Razzaq", "Le Pourvoyeur"),
        ("Al-Fattah", "L'Ouvreur"),
        ("Al-Alim", "L'Omniscient"),
        ("Al-Qabid", "Le Constricteur"),
        ("Al-Basit", "Le Dilatateur"),
        ("Al-Khafid", "L'Abaissant"),
        ("Ar-Rafi'", "L'Élévateur"),
        ("Al-Mu'izz", "Le Honoreur"),
        ("Al-Mudhill", "L'Avilisseur"),
        ("As-Sami'", "L'Oudiant"),
        ("Al-Basir", "Le Voyant"),
        ("Al-Hakam", "Le Juge"),
        ("Al-Adl", "Le Juste"),
        ("Al-Latif", "Le Délicat"),
        ("Al-Khabir", "Le Très Connaisseur"),
        ("Al-Halim", "Le Doux"),
        ("Al-Azim", "Le Grand"),
        ("Al-Ghafur", "Le Pardonneur"),
        ("Ash-Shakur", "Le Reconnaissant"),
        ("Al-Ali", "Le Très Haut"),
        ("Al-Kabir", "Le Grand"),
        ("Al-Hafiz", "Le Gardien"),
        ("Al-Muqit", "Le Protecteur"),
        ("Al-Hasib", "Le Dénombreur"),
        ("Al-Jalil", "Le Glorieux"),
        ("Al-Karim", "Le Généreux"),
        ("Ar-Raqib", "Le Vigilant"),
        ("Al-Mujib", "L'Exauçant"),
        ("Al-Wasi'", "L'Immense"),
        ("Al-Hakim", "Le Sage"),
        ("Al-Wadud", "Le Bien-Aimant"),
        ("Al-Majid", "Le Glorieux"),
        ("Al-Ba'ith", "Le Résurrecteur"),
        ("Ash-Shahid", "Le Témoin"),
        ("Al-Haqq", "Le Véridique"),
        ("Al-Wakil", "Le Mandataire"),
        ("Al-Qawiyy", "Le Fort"),
        ("Al-Matin", "Le Ferme"),
        ("Al-Waliyy", "Le Protecteur"),
        ("Al-Hamid", "Le Loué"),
        ("Al-Muhsi", "Le Nombreur"),
        ("Al-Mubdi'", "Le Créateur"),
        ("Al-Mu'iid", "Le Restitueur"),
        ("Al-Muhyi", "Le Vivifiant"),
        ("Al-Mumit", "Le Donateur de mort"),
        ("Al-Hayy", "Le Vivant"),
        ("Al-Qayyum", "Le Subsistant"),
        ("Al-Wajid", "L'Existant"),
        ("Al-Majid", "Le Sublime"),
        ("Al-Wahid", "L'Unic"),
        ("As-Samad", "L'Éternel"),
        ("Al-Qadir", "Le Puissant"),
        ("Al-Muqtadir", "Le Tout Puissant"),
        ("Al-Muqaddim", "Le Précédent"),
        ("Al-Mu'akhkhir", "Le Retardateur"),
        ("Al-Awwal", "Le Premier"),
        ("Al-Akhir", "Le Dernier"),
        ("Az-Zahir", "L'Apparent"),
        ("Al-Batin", "Le Caché"),
        ("Al-Wali", "Le Proche"),
        ("Al-Muta'ali", "Le Très Élevé"),
        ("Al-Barr", "Le Bienfaisant"),
        ("At-Tawwab", "Le Retournant"),
        ("Al-Muntaqim", "Le Vengeur"),
        ("Al-Afu", "Le Pardonneur"),
        ("Al-Ra'uf", "Le Compatissant"),
        ("Malik al-Mulk", "Le Possesseur de la royauté"),
        ("Dhu al-Jalal wa al-Ikram", "Le Majestueux et le Généreux"),
        ("Al-Muqsit", "L'Équitable"),
        ("Al-Jami'", "Le Rassembleur"),
        ("Al-Ghaniyy", "Le Riche"),
        ("Al-Mughniyy", "L'Enrichisseur"),
        ("Al-Mani'", "Le Répresseur"),
        ("Ad-Darr", "Le Nuisible"),
        ("An-Nafi'", "L'Utile"),
        ("An-Nur", "La Lumière"),
        ("Al-Hadi", "Le Guide"),
        ("Al-Badi'", "L'Incomparable"),
        ("Al-Baqi", "L'Éternel"),
        ("Al-Warith", "L'Héritier"),
        ("Ar-Rashid", "Le Bien Guidé"),
        ("As-Sabur", "Le Patient"),
    ]
    
    # Déterminer quels noms afficher
    if not args:
        # Afficher tous les noms
        display_names = names
        title = "Les 99 noms d'Allah (al-Asma al-Husna)"
    else:
        # Filtrer par critère
        filter_term = args[0].lower()
        display_names = []
        
        # Gérer les plages comme "1-10"
        if "-" in filter_term:
            try:
                start_str, end_str = filter_term.split("-")
                start = int(start_str) - 1  # Convertir en index 0-based
                end = int(end_str)
                display_names = names[start:end]
                title = f"Noms d'Allah {start+1} à {end}"
            except (ValueError, IndexError):
                return "Format invalide. Utilisez : noms <début>-<fin> (ex: noms 1-10)"
        elif filter_term.isdigit():
            n = int(filter_term)
            start = max(0, n - 1)
            end = min(len(names), n + 9)  # Afficher 10 noms
            display_names = names[start:end]
            title = f"Noms d'Allah {start+1} à {end}"
        else:
            # Filtrer par mot-clé (insensible aux accents et aux formes)
            import unicodedata
            def strip_accents(s):
                return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
            
            filter_normalized = strip_accents(filter_term.lower())
            for name, desc in names:
                name_normalized = strip_accents(name.lower())
                desc_normalized = strip_accents(desc.lower())
                # Recherche flexible par racine commune (min 4 caractères)
                if (filter_normalized in name_normalized or 
                    filter_normalized in desc_normalized or
                    any(word.startswith(filter_normalized) for word in desc_normalized.split()) or
                    any(filter_normalized.startswith(word.rstrip('eieuxiour')) for word in desc_normalized.split() if len(word) > 4)):
                    display_names.append((name, desc))
            title = f"Noms d'Allah contenant « {filter_term} »"
    
    if not display_names:
        return f"Aucun nom trouvé pour « {filter_term} »."
    
    out = [f"🌸 {title}", "=" * 60]
    for i, (name, desc) in enumerate(display_names, 1):
        out.append(f"{i:2}. {name:<20} — {desc}")
    
    if len(args) == 0:
        out.append("\nUtilisation : noms <numéro> ou noms <début>-<fin>")
        out.append("Exemples : noms 1-10, noms rahman, noms miséricorde")
    
    return "\n".join(out)


def _list_pillars() -> str:
    """Affiche les 5 piliers de l'islam."""
    out = [
        "🕌 Les 5 piliers de l'islam",
        "=" * 60,
        "",
        "1. LA CHAHADA (Attestation de foi)",
        "   « J'atteste qu'il n'y a de divinité qu'Allah,",
        "    et j'atteste que Muhammad est le Messager d'Allah »",
        "",
        "2. LA SALAT (Prières quotidiennes)",
        "   5 prières obligatoires : Fajr, Dhuhr, Asr, Maghrib, Isha",
        "   Condition de validité : purification (wudu), direction (qibla), temps",
        "",
        "3. LA ZAKAT (Aumône obligatoire)",
        "   2,5% des biens atteignant le nissab pendant un an",
        "   Bénéficiaires : pauvres, nécessiteux, voyageurs, etc. (9:60)",
        "",
        "4. LE SAWM (Jeûne du Ramadan)",
        "   Du lever au coucher du soleil pendant le mois de Ramadan",
        "   But : atteindre la piété (taqwa) - Coran 2:183",
        "",
        "5. LE HAJJ (Pèlerinage à La Mecque)",
        "   Obligatoire une fois dans la vie pour qui en a la capacité",
        "   Rites : tawaf, sa'i, Arafat, sacrifice",
        "",
        "📖 Référence : Sahih Muslim 16 hadith n°40",
        "   Le Prophète ﷺ a dit : « L'islam est bâti sur cinq piliers... »",
    ]
    return "\n".join(out)


def _list_faith_pillars() -> str:
    """Affiche les 6 piliers de la foi."""
    out = [
        "📚 Les 6 piliers de la foi (iman)",
        "=" * 60,
        "",
        "1. CROIRE EN ALLAH (Tawhid)",
        "   L'unicité d'Allah dans Sa seigneurie, Son adoration et Ses attributs",
        "",
        "2. CROIRE AUX ANGES",
        "   Êtres de lumière créés par Allah, chargés de missions spécifiques",
        "   Exemples : Jibril (révélation), Mikail (provision), Israfil (trompette)",
        "",
        "3. CROIRE AUX LIVRES RÉVÉLÉS",
        "   Coran, Torah, Psautier, Évangile, etc.",
        "   « Nous avons fait descendre le Rappel, et Nous le garderons » (15:9)",
        "",
        "4. CROIRE AUX MESSAGERS/PROPHÈTES",
        "   Adam, Noé, Abraham, Moïse, Jésus, Muhammad ﷺ, etc.",
        "   « Nous n'envoyons aucun messager avant toi » (3:161)",
        "",
        "5. CROIRE AU JOUR DERNIER",
        "   Résurrection, jugement, Paradis et Enfer",
        "   « Ce monde n'est que jeu et divertissement » (29:64)",
        "",
        "6. CROIRE AU DÉCRET DIVIN (Qadar)",
        "   Tout vient d'Allah : science, volonté, création",
        "   « Allah est le Créateur de toute chose » (39:62)",
        "",
        "📖 Référence : Hadith de Jibril (Sahih Muslim n°8)",
    ]
    return "\n".join(out)


def _list_prophets() -> str:
    """Affiche les prophètes mentionnés dans le Coran."""
    out = [
        "🕊️ Les prophètes mentionnés dans le Coran",
        "=" * 60,
        "",
        "Les prophètes principaux (ulul-azm) :",
        "1. Nuh (Noé) - Coran 71",
        "2. Ibrahim (Abraham) - Coran 14, 21, 26",
        "3. Musa (Moïse) - Coran 2, 7, 10, 20, 28",
        "4. Isa (Jésus) - Coran 3, 4, 5, 19",
        "5. Muhammad ﷺ - Coran 33, 47, 48",
        "",
        "Autres prophètes mentionnés :",
        "- Adam (2:31, 3:33)",
        "- Idris (19:56, 21:85)",
        "- Hud (7:65, 11:50)",
        "- Salih (7:73, 11:61)",
        "- Lut (7:80, 11:77)",
        "- Ismail (2:125, 19:54)",
        "- Ishaq (2:133, 19:49)",
        "- Yaqub (2:132, 11:71)",
        "- Yusuf (12:4, 6:84)",
        "- Ayyub (21:83, 38:41)",
        "- Dhul-Kifl (21:85, 38:48)",
        "- Yunus (10:98, 21:87)",
        "- Dawud (27:15, 38:17)",
        "- Sulayman (27:15, 38:30)",
        "- Ilyas (6:85, 37:123)",
        "- Al-Yasa (6:86, 38:48)",
        "- Zakariya (3:37, 19:2)",
        "- Yahya (3:38, 19:12)",
        "",
        "📖 Coran 4:163 : « Nous avons inspiré Noé et les prophètes après lui »",
    ]
    return "\n".join(out)


def _list_important_surahs() -> str:
    """Affiche les sourates importantes du Coran."""
    out = [
        "🌸 Les sourates importantes du Coran",
        "=" * 60,
        "",
        "Sourates de protection (Mu'awwidhat) :",
        "- Al-Falaq (112) : refuge contre les maux",
        "- An-Nas (113) : refuge contre les insufflations",
        "- Al-Ikhlas (111) : pureté de la foi",
        "",
        "Sourates fréquemment récitées :",
        "- Al-Fatiha (1) : l'ouverture, récitation quotidienne en prière",
        "- Al-Baqara (2:255) : Ayat al-Kursi (verset du Trône)",
        "- Ya-Sin (36) : cœur du Coran",
        "- Ar-Rahman (55) : les bienfaits d'Allah",
        "- Al-Mulk (67) : la royauté divine",
        "- Al-Qadr (97) : la nuit du Destin",
        "- Al-Asr (103) : le temps et la perte",
        "- At-Tin (95) : le figuier et l'olivier",
        "",
        "Sourates narratives importantes :",
        "- Yusuf (12) : histoire de Joseph",
        "- Al-Kahf (18) : la caverne et les récits",
        "- Maryam (19) : Marie et Jésus",
        "- Ibrahim (14) : Abraham et son père",
        "- Nuh (71) : Noé et son peuple",
        "",
        "Sourates législatives :",
        "- An-Nisa (4) : les femmes",
        "- Al-Ma'ida (5) : la table",
        "- Al-Baqara (2) : la vache (plus longue sourate)",
        "",
        "📖 Référence : Coran 15:9 : « Nous avons fait descendre le Rappel, et Nous le garderons »",
    ]
    return "\n".join(out)


def _translate_to_wolof(text: str, reference: str) -> str:
    """Traduit un texte (verset ou hadith) en wolof via l'IA locale."""
    if not llm.is_available():
        return (
            "⚠️ Ollama (modèle qwen2.5:7b) ne tourne pas ou le modèle n'est pas tiré.\n"
            "Lance : ./setup.sh  puis réessaie."
        )
    print("🤖 Traduction en wolof (IA locale)…\n")
    context = f"[{reference}]\n{text}"
    prompt = (
        "Traduis ce texte en WOLOF (langue du Sénégal), en t'efforçant d'être fidèle au sens.\n"
        "Règles :\n"
        "1. Traduis le sens en wolof de manière claire et naturelle.\n"
        "2. Garde les termes religieux arabes courants (Allah, etc.) tels quels.\n"
        "3. Donne ensuite une traduction française de référence en dessous.\n"
        "4. Réponds d'abord en wolof, puis en français.\n"
        "RÈGLE ABSOLUE : ne cite que le texte fourni ci-dessous. "
        "N'invente AUCUNE citation ni numéro de hadith."
    )
    msgs = llm.teacher_messages(prompt, context)
    text = llm.chat(msgs, stream=False, strict=True)
    print(text, flush=True)
    return ""


def _wolof_dispatch(args: list[str]) -> str:
    """Dispatch des commandes wolof."""
    if not args:
        return HELP_WOLOF
    sub = args[0].lower()
    
    if sub == "aide" or sub == "help":
        return HELP_WOLOF
    
    # wolof coran <ref>
    if sub == "coran":
        if len(args) < 2:
            return "Usage : wolof coran <sourate:verset> (ex : wolof coran 1:1)"
        try:
            surah, start, end = quran.parse_ref(" ".join(args[1:]))
        except ValueError:
            return "Référence incomprise. Exemple : wolof coran 1:1"
        meta = db.get_surah_meta(surah)
        if not meta:
            return f"Sourate {surah} introuvable."
        row = db.get_ayah(surah, start)
        if not row:
            return f"Verset {surah}:{start} introuvable."
        text = f"{row['text_ar']}\n{row['text_fr']}"
        ref = f"Coran {surah}:{start} — {meta['transliteration']}"
        return _translate_to_wolof(text, ref)
    
    # wolof hadith <livre> <n>
    if sub == "hadith":
        if len(args) < 3:
            return "Usage : wolof hadith <livre> <n°> (ex : wolof hadith bukhari 1)"
        book = resolve_book_input(args[1])
        if not book:
            return f"Livre inconnu : « {args[1]} ». Voir 'hadith livres'."
        try:
            n = int(args[2])
        except ValueError:
            return "Le n° doit être un entier."
        row = db.get_hadith(book, n)
        if not row:
            return f"Hadith n°{n} du livre « {book} » introuvable."
        text = f"Narrateur : {row['narrator_en'] or '?'}\n{row['text_en']}\n{row['arabic'] or ''}"
        ref = f"Hadith — {row['book_name']} n°{row['hadith_number']}"
        return _translate_to_wolof(text, ref)
    
    # wolof <texte libre> → on traduit la question / demande en wolof
    return _translate_to_wolof(" ".join(args), "texte fourni")


HELP_WOLOF = """\
🇸🇳 WOLOF — Traduction en wolof (Sénégal)

  wolof coran <ref>              → traduire un verset en wolof (ex : wolof coran 1:1)
  wolof hadith <livre> <n>       → traduire un hadith en wolof (ex : wolof hadith bukhari 1)
  wolof <texte>                  → traduire un texte libre en wolof
  wolof aide                     → cette aide

Exemple : wolof coran 2:255  (Ayat al-Kursi en wolof)
          wolof hadith bukhari 1  (premier hadith en wolof)

Note : ces traductions sont pédagogiques, produites par l'IA locale.
"""


def ask_llm(question: str) -> str:
    if not llm.is_available():
        return (
            "⚠️ Ollama (modèle qwen2.5:7b) ne tourne pas ou le modèle n'est pas tiré.\n"
            "Lance : ./setup.sh  puis réessaie."
        )
    print("🔎 Recherche dans le corpus local…")
    context = _grounding_context(question)
    print("🤖 L'IA réfléchit…\n")
    msgs = llm.teacher_messages(question, context)
    llm.chat(msgs, strict=True)
    return ""


def repl() -> None:
    print(HELP)
    first = True
    while True:
        try:
            if first:
                print("\nCommencer ? 'apprendre' pour le plan, 'quiz' pour tester, 'demander' pour poser une question.\n")
                first = False
            line = input("🕌 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nÀ bientôt. Barakallahu fik !")
            break
        if not line:
            continue
        args = line.split()
        if args[0].lower() in ("quit", "exit", "quitter"):
            print("À bientôt. Barakallahu fik !")
            break
        try:
            result = dispatch(args, interactive=True)
        except Exception as exc:
            print(f"Erreur : {exc}")
            continue
        if result and isinstance(result, str) and result != "__EXIT__":
            print(result)


def main(argv: list[str]) -> int:
    if not argv:
        repl()
        return 0
    if argv[0] in ("start", "--start") :
        repl()
        return 0
    result = dispatch(argv)
    if result == "__EXIT__":
        return 0
    if isinstance(result, str) and result:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))