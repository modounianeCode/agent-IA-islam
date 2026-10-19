"""Interface interactive en ligne de commande."""
from __future__ import annotations

import sys

from agent import db, hadith, quran, quiz, curriculum

_conversation_history: list[dict] = []

HELP = """\
━━━ Assistant islamique — Apprendre l'Islam ━━━
💡 La touche TAB complète automatiquement la commande en cours de frappe.

📖 CORAN
  coran 2                     → sourate 2 (aperçu)
  coran 2:255                 → verset précis
  coran 18 1-10               → plage de versets
  coran chercher <terme>      → recherche dans la traduction française
  coran list                  → liste des 114 sourates

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
  histoires <nom>             → histoire d'un prophète (ex : histoires yusuf)
  sourates importantes        → les sourates majeures

🌐 EN LIGNE (API — nécessite Internet)
  hijri                       → date hijri du jour et prochain événement
  prieres <ville> [pays]      → horaires de prière (ex : prieres Dakar Senegal)
  prieres <lat> <lon>         → horaires de prière par coordonnées
  qibla <lat> <lon>           → direction de la Qibla (ex : qibla 14.69 -17.44)
  tafsir <s>[:<v>]            → tafsir Ibn Kathir d'un verset (ex : tafsir 2:255)

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
            f"{row['text_ar']}\n{row['text_fr']}\n{row['text_en']}"
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
                    f"{row['text_ar']}\n{row['text_fr']}\n{row['text_en']}"
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
            return hadith.random_hadith(book)
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
                a = input("\nVeux-tu une explication/traduction en français (f) ou rien (n) ? ").strip().lower()
                row = db.get_hadith(book, n)
                if a in ("o", "oui", "f", "fr") and row:
                    return _explain_hadith_from_row(row)
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
    
    if cmd in ("histoires", "histoire", "récits", "recits", "stories"):
        return _stories_dispatch(args[1:])
    
    if cmd == "sourates" or cmd == "sourates importantes":
        return _list_important_surahs()

    # ── EN LIGNE (API islamiques) ──────────────────────────
    if cmd == "hijri":
        return _hijri()
    if cmd in ("prieres", "prière", "priere"):
        return _prayer_times(args[1:])
    if cmd == "qibla":
        return _qibla(args[1:])
    if cmd == "tafsir":
        return _tafsir(args[1:])

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


# ── HISTOIRES DES PROPHÈTES ───────────────────────────────────────
PROPHET_STORIES = {
    "adam": {
        "name": "Adam",
        "title": "Le premier homme et le premier prophète",
        "story": (
            "Adam est le premier être humain et le premier prophète. Allah le créa de terre, l'honora en "
            "lui enseignant les noms de toutes choses (2:31), et lui demanda de prostrer les anges par respect "
            "pour lui. Adam et sa femme vécurent au Paradis, jusqu'à ce que Satan les tente et qu'ils "
            "mangent de l'arbre interdit (2:36). Ils se repentirent aussitôt : « Notre Seigneur, nous avons fait "
            "du tort à nous-mêmes… » (7:23) et Allah accepta leur repentir. Adam est le père de l'humanité et "
            "l'exemple du repentir sincère : l'homme est faillible, mais la miséricorde d'Allah est plus grande "
            "que toute faute."
        ),
        "verses": [
            ("2:31", "Allah enseigna à Adam les noms de toutes choses"),
            ("2:36", "Satan les fit sortir du Paradis : il est l'ennemi déclaré de l'homme"),
            ("7:23", "Adam et sa femme se repentent : « …Si Tu ne nous pardonnes pas… nous serons perdants »"),
        ],
        "lesson": "Quelle que soit la faute, le repentir sincère vers Allah est toujours accepté.",
    },
    "idris": {
        "name": "Idris (Énoch)",
        "title": "Le prophète élevé en haut lieu",
        "story": (
            "Idris est un prophète ancien, ancêtre de Nuh (Noé). Allah le loue dans le Coran comme « un homme "
            "véridique et un prophète » (19:56). Il est connu pour sa persévérance et sa patience. Le Coran "
            "dit qu'Allah « l'éleva en un lieu très haut » (19:57) : une marque d'honneur et de proximité avec "
            "Allah. On rapporte qu'il fut le premier à écrire avec le calame et à coudre des vêtements."
        ),
        "verses": [
            ("19:56", "Idris était un véridique et un prophète"),
            ("19:57", "Allah l'éleva en un lieu très haut"),
            ("21:85", "Il fut parmi les endurants"),
        ],
        "lesson": "La véracité et la persévérance élèvent le serviteur auprès d'Allah.",
    },
    "nuh": {
        "name": "Nuh (Noé)",
        "title": "La patience dans l'appel, neuf cent cinquante ans",
        "story": (
            "Nuh fut envoyé à un peuple qui adorait des idoles. Il les appela à l'unicité d'Allah pendant neuf "
            "cent cinquante ans (29:14), mais seuls quelques-uns crurent. Il construisit l'arche sur ordre "
            "d'Allah, malgré les moqueries des mécréants. Quand le déluge vint, il embarqua les croyants et un "
            "couple de chaque espèce (11:40). Son fils, qui s'était écarté de la foi, refusa et périt (11:42-43). "
            "Le récit de Nuh est une leçon immense de patience et de certitude : le secours d'Allah vient "
            "toujours, même quand tout semble perdu."
        ),
        "verses": [
            ("29:14", "Nuh demeura parmi son peuple neuf cent cinquante ans"),
            ("11:40", "Embarquèrent seulement ceux qui avaient cru"),
            ("71:1", "Nous avons envoyé Nuh à son peuple : avertis-les avant qu'un châtiment douloureux ne les frappe"),
        ],
        "lesson": "La patience dans l'appel, même face au rejet, est la voie des prophètes.",
    },
    "hud": {
        "name": "Hud (Héber)",
        "title": "Envoyé aux 'Ad, peuple des colonnes",
        "story": (
            "Hud fut envoyé au peuple des 'Ad, qui habitait de vastes demeures et adorait des idoles. Il les "
            "appela à adorer Allah seul et refusa tout salaire pour cela (11:51). Les 'Ad, pleins d'orgueil "
            "pour leur puissance, le traitèrent de menteur et le raillèrent. Malgré ses avertissements, ils "
            "persistèrent dans l'erreur et furent détruits par un vent glacial. Allah sauva Hud et ceux qui "
            "avaient cru avec lui (11:58)."
        ),
        "verses": [
            ("7:65", "Nous avons envoyé Hud aux 'Ad, leur frère : Adorez Allah, vous n'avez point de divinité en dehors de Lui"),
            ("11:50", "Hud appela son peuple à l'unicité d'Allah"),
            ("11:58", "Notre ordre vint : Nous sauvâmes Hud et ceux qui crurent avec lui"),
        ],
        "lesson": "L'orgueil et la puissance matérielle ne protègent jamais de la justice d'Allah.",
    },
    "salih": {
        "name": "Salih (Salé)",
        "title": "Envoyé aux Thamud, peuple du rocher",
        "story": (
            "Salih fut envoyé aux Thamud, un peuple qui sculptait des maisons dans la roche. Il les appela à "
            "adorer Allah seul. Comme signe, Allah leur donna la chamelle et leur demanda de la laisser boire "
            "et de ne pas lui faire de mal (7:73). Mais ils tuèrent la chamelle et défièrent Salih. Le châtiment "
            "les frappa par un grand cri, et Allah sauva Salih et les croyants. Le récit montre que les signes "
            "d'Allah exigent la foi et non le défi."
        ),
        "verses": [
            ("7:73", "Voici la chamelle d'Allah, signe pour vous : laissez-la paître, ne lui faites pas de mal"),
            ("11:61", "Salih appela son peuple à Lui demander pardon et à se repentir"),
            ("11:68", "Les Thamud furent détruits pour avoir démenti les signes de leur Seigneur"),
        ],
        "lesson": "Les signes d'Allah demandent humilité et obéissance, jamais provocation.",
    },
    "ibrahim": {
        "name": "Ibrahim (Abraham)",
        "title": "Le père des prophètes, l'ami intime d'Allah",
        "story": (
            "Ibrahim est l'ami intime d'Allah (Khalilullah) et le père spirituel des prophètes. Jeune, il "
            "chercha son Seigneur par le raisonnement et invita son peuple à l'unicité. Il brisa les idoles "
            "que son peuple adorait (21:51-57) et fut jeté dans le feu, qui devint pour lui paix et fraîcheur "
            "(21:69). Il émigra avec sa famille, laissa Ismaïl et Hajar dans la vallée de Bakkah (future La "
            "Mecque), où Allah fit jaillir la source de Zamzam. Eprouvé par l'ordre de sacrifier son fils, "
            "son obéissance totale fut récompensée par un grand sacrifice (37:102-107). Avec Ismaïl, il "
            "construisit la Kaaba (2:127). Le Coran en fait le modèle de la soumission pure."
        ),
        "verses": [
            ("21:51", "Nous avions auparavant donné à Ibrahim la bonne direction"),
            ("21:69", "Ô feu, sois pour Ibrahim un fraîcheur et une paix"),
            ("37:102", "Je me suis vu en songe sacrifiant tout en te soumettant à l'épreuve : Observe ce que tu en penses"),
            ("2:127", "Ibrahim et Ismaïl élevèrent les fondements de la Maison"),
        ],
        "lesson": "La soumission totale à Allah, même dans l'épreuve la plus dure, est la foi véritable.",
    },
    "lut": {
        "name": "Lut (Lot)",
        "title": "Envoyé à un peuple perverti",
        "story": (
            "Lut, neveu d'Ibrahim, fut envoyé à un peuple qui commit un péché abominable : les hommes "
            "s'approchaient des hommes au lieu des femmes (7:80-81). Il les appela à la pureté, mais ils "
            "le menacèrent d'expulsion et vinrent même vers ses hôtes (les anges). Ceux-ci se révélèrent et "
            "annoncèrent le châtiment. Allah sauva Lut et sa famille, sauf sa femme qui partageait le rejet. "
            "Le peuple de Lut fut renversé : une leçon sur l'abandon des interdits d'Allah."
        ),
        "verses": [
            ("7:80", "Vous approchez-vous des hommes au lieu des femmes ? Vous êtes un peuple transgresseur"),
            ("11:77", "Les envoyés arrivèrent chez Lut, qui en fut effrayé"),
            ("7:84", "Nous fîmes pleuvoir sur eux une pluie : vois la fin des criminels"),
        ],
        "lesson": "La pureté et la pudeur sont des valeurs qu'on ne sacrifie jamais.",
    },
    "ismail": {
        "name": "Ismaïl (Ismaël)",
        "title": "Le fils du sacrifice et le bâtisseur de la Kaaba",
        "story": (
            "Ismaïl, fils d'Ibrahim et de Hajar, grandit dans la vallée de La Mecque. Il est connu pour sa "
            "droiture et sa patience. Lorsque son père lui fit part du songe lui demandant de le sacrifier, il "
            "répondit avec une obéissance admirable : « Ô mon père, fais ce qui t'est commandé ; tu me "
            "trouveras patient, s'il plaît à Allah » (37:102). Sa soumission fut le fondement de l'Aïd al-Adha. "
            "Avec son père, il construisit la Kaaba, et Allah le loue dans le Coran comme « d'une promesse "
            "véridique » (19:54)."
        ),
        "verses": [
            ("37:102", "Ô mon père, fais ce qui t'est commandé : tu me trouveras patient"),
            ("2:125", "Nous fîmes de la Maison un lieu de rassemblement pour les gens"),
            ("19:54", "Ismaïl était d'une promesse véridique, et il fut un messager et un prophète"),
        ],
        "lesson": "L'obéissance confiante à Allah, même dans l'épreuve, élève le serviteur.",
    },
    "ishaq": {
        "name": "Ishaq (Isaac)",
        "title": "Le fils promis de la miséricorde",
        "story": (
            "Ishaq est le fils d'Ibrahim et de Sarah, dont la naissance fut annoncée comme une bonne nouvelle "
            "en dépit de leur vieillesse (11:71 ; 51:29-30). Il est le père de Yaqub (Jacob) et l'ancêtre de "
            "nombreux prophètes. Allah le bénit ainsi que sa descendance, et le Coran le cite parmi les "
            "prophètes élus et guidés (6:84). Son histoire rappelle que rien n'est impossible à Allah."
        ),
        "verses": [
            ("11:71", "Sa femme rit, et Nous lui annonçâmes la bonne nouvelle d'Ishaq, et après lui de Yaqub"),
            ("19:49", "Nous lui fîmes don d'Ishaq et de Yaqub, et nous en fîmes tous deux des prophètes"),
            ("6:84", "Nous lui donnâmes Ishaq et Yaqub : Nous les guidâmes tous"),
        ],
        "lesson": "Les promesses d'Allah s'accomplissent, même lorsque tout paraît impossible.",
    },
    "yaqub": {
        "name": "Yaqub (Jacob)",
        "title": "Le père patient des douze tribus",
        "story": (
            "Yaqub, fils d'Ishaq et père de Yusuf, est un prophète patient. Il subit la perte de son fils bien-"
            "aimé Yusuf avec une dignité profonde : « Belle patience ! Allah est mon secours contre ce que "
            "vous avancez » (12:18). Il refusa de désespérer et garda confiance en Allah pendant de longues "
            "années. Allah lui rendit finalement Yusuf et le consola (12:96). Sur son lit, il recommanda à ses "
            "fils la religion de leurs pères : la soumission à Allah, seul (2:132)."
        ),
        "verses": [
            ("12:18", "Belle patience ! Allah est mon secours contre ce que vous avancez"),
            ("12:96", "L'annonceur arriva avec la tunique de Yusuf : la vue de Yaqub revint"),
            ("2:132", "Yaqub recommanda à ses fils : ô mes fils, Allah a choisi pour vous la religion"),
        ],
        "lesson": "La patience dans l'épreuve et la confiance en Allah portent toujours leurs fruits.",
    },
    "yusuf": {
        "name": "Yusuf (Joseph)",
        "title": "De la fosse au trône d'Égypte",
        "story": (
            "Yusuf fut jeté par ses frères, par jalousie, dans le fond d'un puits (12:10), puis vendu en Égypte "
            "où il grandit dans la maison d'un notable. Il refusa la tentation avec piété et fut injustement "
            "emprisonné. En prison, il interpréta les rêves et sa droiture fut reconnue. Appelé auprès du roi, "
            "il expliqua le songe des sept vaches (12:43-49) et devint intendant des greniers d'Égypte. Des "
            "années plus tard, ses frères vinrent et se reconnurent ; Yusuf leur pardonna avec noblesse "
            "(12:92). La sourate Yusuf (12) est appelée « la plus belle des histoires » (12:3)."
        ),
        "verses": [
            ("12:10", "Jetez-le dans le fond du puits : le recueilleront des voyageurs"),
            ("12:92", "Point de reproche pour vous aujourd'hui : Allah vous pardonne"),
            ("12:3", "Nous te racontons la plus belle des histoires par ce que Nous te révélons"),
        ],
        "lesson": "La pureté, la patience et le pardon transforment les plus dures épreuves en victoires.",
    },
    "ayyub": {
        "name": "Ayyub (Job)",
        "title": "L'exemple parfait de la patience dans la maladie",
        "story": (
            "Ayyub fut comblé de biens, d'enfants et de santé, puis éprouvé par la perte de tout cela et une "
            "longue maladie. Il ne cessa jamais d'invoquer Allah et garda une patience exemplaire. Il dit : "
            "« Le mal m'a touché, et Tu es le plus miséricordieux des miséricordieux » (21:83). Allah lui "
            "répondit, lui rendit la santé et lui rendit sa famille en plus grand nombre (21:84). La légende "
            "pousserait à se plaindre ; Ayyub est la preuve que l'épreuve est une école de foi."
        ),
        "verses": [
            ("21:83", "Le mal m'a touché, et Tu es le plus miséricordieux des miséricordieux"),
            ("21:84", "Nous lui répondîmes, écartâmes le mal et lui rendîmes sa famille"),
            ("38:41", "Rappelle-toi Ayyub, qui invoqua son Seigneur : le diable m'a touché de peine et de tourment"),
        ],
        "lesson": "Dans la douleur comme dans l'aisance, on glorifie et invoque Allah, jamais on ne désespère.",
    },
    "shuayb": {
        "name": "Shuayb (Jethro)",
        "title": "Le défenseur de l'équité dans le commerce",
        "story": (
            "Shuayb fut envoyé au peuple de Madian, qui tricheait dans les poids et mesures et dépouillait les "
            "gens. Il leur ordonna la justice, l'équité dans le commerce et l'adoration d'Allah seul (11:84-85). "
            "Rebuté, il fut menacé d'expulsion. Allah détruisit les mécréants par le tremblement et sauva "
            "Shuayb et les croyants. C'est le prophète patron de l'honnêteté commerciale, une leçon toujours "
            "actuelle."
        ),
        "verses": [
            ("7:85", "Remplissez la mesure et le poids avec équité, ne frustrez pas les gens de leurs biens"),
            ("11:84", "Nous envoyâmes Shuayb aux Madian, leur frère : adorez Allah, vous n'avez point de divinité en dehors de Lui"),
            ("7:87", "Si une partie de vous a cru au message et l'autre non, patientez jusqu'à ce qu'Allah juge"),
        ],
        "lesson": "L'argent et le commerce doivent être purs, honnêtes et justes envers tous.",
    },
    "musa": {
        "name": "Musa (Moïse)",
        "title": "Le prophète à qui Allah parla, sauveur de son peuple",
        "story": (
            "Musa est appelé Kalimullah, « celui à qui Allah parla ». Né sous le règne du Pharaon qui tuait les "
            "garçons hébreux, il fut placé dans un coffret jeté sur le Nil et recueilli, par la volonté d'Allah, "
            "dans la maison du Pharaon (28:4-8). Devenu adulte, Allah lui parla au mont Sinay (le Tur) et lui "
            "donna la Thora (7:143-145). Il affronta Pharaon avec son frère Harun, fit traverser la mer à son "
            "peuple par la puissance d'Allah, et reçut les tables de la Loi. Mais son peuple se mit à adorer le "
            "veau en son absence (7:148). Musa reste le symbole de la fermeté face au tyran et de la douceur "
            "envers son peuple."
        ),
        "verses": [
            ("28:4", "Pharaon s'éleva dans le pays et sema la division parmi ses habitants"),
            ("28:7", "Nous inspirâmes à la mère de Musa : allaitez-le, et quand tu craindras, jette-le dans le fleuve"),
            ("7:143", "Musa vint au rendez-vous, et son Seigneur lui parla"),
            ("4:164", "Allah parla à Musa directement"),
        ],
        "lesson": "La vérité, portée avec foi, triomphe des tyrans les plus puissants.",
    },
    "harun": {
        "name": "Harun (Aaron)",
        "title": "Le frère et soutien de Musa",
        "story": (
            "Harun fut le frère de Musa et son soutien dans la mission. Allah exauça la prière de Musa qui "
            "demandait son frère comme appui (20:29-32). Harun l'accompagna auprès du Pharaon et partagea "
            "la difficile conduite du peuple d'Israël. Quand une partie du peuple adora le veau, Harun les "
            "avertit et les dissuada (20:90), mais ils n'écoutèrent pas. Le Coran le cite parmi les prophètes "
            "élus (19:53)."
        ),
        "verses": [
            ("20:92", "Musa dit à Harun : qu'est-ce qui t'a empêché, quand tu les as vus s'égarer, de me suivre ?"),
            ("19:53", "Nous lui fîmes don de son frère Harun, de par Notre miséricorde"),
            ("7:142", "Nous donnâmes à Musa ses rendez-vous, et Nous lui désignâmes son frère Harun comme soutien"),
        ],
        "lesson": "La solidarité fraternelle dans le bien est un pilier de la mission.",
    },
    "dawud": {
        "name": "Dawud (David)",
        "title": "Le roi-prophète au jugement juste",
        "story": (
            "Dawud tua Goliath (Jalut) avec la permission d'Allah, et Allah lui donna la royauté et la sagesse "
            "(2:251). Il reçut le Zabur (Psaumes), et la montagne comme les oiseaux glorifiaient Allah avec lui "
            "(21:79). Prophète-roi, il fut éprouvé par une affaire de deux plaideurs et se repentit (38:21-25). "
            "Allah lui ordonna de juger avec équité et de ne pas suivre la passion (38:26). Dawud montre que la "
            "force et le pouvoir doivent être au service de la justice."
        ),
        "verses": [
            ("2:251", "Allah donna à Dawud la royauté et la sagesse, et Lui enseigna ce qu'Il voulut"),
            ("38:26", "Ô Dawud, Nous t'avons fait calife sur la terre : juge donc en toute équité"),
            ("21:79", "Nous soumîmes les montagnes et les oiseaux qui glorifiaient avec lui"),
        ],
        "lesson": "Le pouvoir est une charge qui exige justice, humilité et repentir.",
    },
    "sulayman": {
        "name": "Sulayman (Salomon)",
        "title": "Le roi auquel Allah soumit les djinns et le vent",
        "story": (
            "Sulayman, fils de Dawud, reçut d'Allah un royaume sans égal : le vent, les djinns et le langage "
            "des oiseaux furent soumis à son service (27:15-17). Il jugea avec sagesse, comme le montre "
            "l'histoire de la reine de Saba (Bilqis), qu'il invita à adorer Allah seul et qui s'y soumit "
            "(27:38-44). Sa lettre commençait par la basmala, « Au nom d'Allah, le Tout Miséricordieux, le Très "
            "Miséricordieux » (27:30). Le prophète souligna que les bienfaits d'Allah appellent la gratitude "
            ": « Ceci est une faveur de mon Seigneur pour m'éprouver » (27:40)."
        ),
        "verses": [
            ("27:15", "Nous donnâmes à Dawud et à Sulayman la science, et ils dirent : louange à Allah"),
            ("27:30", "Elle vient de Sulayman : Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux"),
            ("27:40", "Ceci est une faveur de mon Seigneur pour m'éprouver : serai-je reconnaissant ou ingrat ?"),
        ],
        "lesson": "La puissance et les dons sont une épreuve : on les met au service d'Allah, avec gratitude.",
    },
    "ilyas": {
        "name": "Ilyas (Élie)",
        "title": "Le défenseur du monothéisme",
        "story": (
            "Ilyas fut envoyé au peuple d'Israël qui adorait l'idole Baal. Il les appela à craindre Allah et à "
            "abandonner cette fausse divinité (37:124-126). Le Coran le loue et lui rend hommage : « Que la paix "
            "soit sur Ilyas » (37:130). Comme beaucoup de prophètes, il fut démenti par la majorité de son "
            "peuple, mais sa mission rappelle que le tawhid ne supporte aucun compromis. Il est cité avec "
            "Zakariya et Yahya parmi les plus pieux (6:85)."
        ),
        "verses": [
            ("37:123", "Ilyas fut, lui aussi, du nombre des envoyés"),
            ("37:130", "Que la paix soit sur Ilyas"),
            ("6:85", "Zakariya, Yahya, Isa et Ilyas furent tous du nombre des vertueux"),
        ],
        "lesson": "Le monothéisme se défend sans compromis, avec douceur et constance.",
    },
    "al_yasa": {
        "name": "Al-Yasa (Élisée)",
        "title": "Le successeur du message",
        "story": (
            "Al-Yasa (Élisée) est cité dans le Coran parmi les prophètes élus, aux côtés d'Ismaïl, d'Ilyas et "
            "de Dhul-Kifl, comme un homme du nombre des meilleurs (38:48). Peu d'éléments de son récit sont "
            "détaillés dans le Coran, mais sa mention enseigne que le message prophétique se transmet de "
            "génération en génération, avec la même mission : rappeler l'adoration d'Allah seul."
        ),
        "verses": [
            ("38:48", "Rappelle-toi Al-Yasa et Dhul-Kifl : tous sont du nombre des meilleurs"),
            ("6:86", "Ismaïl, Al-Yasa, Yunus et Lut : Nous les préférâmes aux mondes"),
        ],
        "lesson": "Chaque génération a besoin d'un rappel, et chacun peut porter la lumière.",
    },
    "yunus": {
        "name": "Yunus (Jonas)",
        "title": "L'invocation dans l'obscurité de la mer",
        "story": (
            "Yunus fut envoyé à son peuple, qui ne crut qu'au moment où le châtiment était imminent et fut ainsi "
            "épargné (10:98). Las, il partit sans attendre l'ordre d'Allah et fut englouti par une grande baleine "
            "(37:140-142). Dans les ténèbres, il invoqua : « Point de divinité à part Toi ! Gloire à Toi ! J'étais "
            "parmi les injustes » (21:87). Allah exauça son invocation et le fit sortir (21:88). Cette invocation "
            "est devenue une grande invocation du pardon."
        ),
        "verses": [
            ("21:87", "Point de divinité à part Toi ! Gloire à Toi ! J'étais parmi les injustes"),
            ("21:88", "Nous lui répondîmes et le sauvâmes de l'anxiété"),
            ("10:98", "Y a-t-il une cité qui crut au moment fatal et tira profit de sa foi, sinon le peuple de Yunus ?"),
        ],
        "lesson": "La sincérité de l'invocation, même au fond de la détresse, fait descendre le secours d'Allah.",
    },
    "zakariya": {
        "name": "Zakariya (Zacharie)",
        "title": "L'invocation d'un cœur pour un enfant",
        "story": (
            "Zakariya, chargé de la garde de Maryam auprès de laquelle il voyait des dons d'Allah (3:37), "
            "demanda à son Seigneur, en secret et avec ferveur, un enfant qui poursuivrait le message (3:38 ; "
            "19:2-6). Allah lui annonça la naissance de Yahya, alors que lui et sa femme étaient vieux (19:7-9). "
            "Les anges lui dirent : « Allah t'annonce la bonne nouvelle de Yahya, qui confirmera une parole "
            "d'Allah » (3:39). L'histoire de Zakariya est la preuve que la prière sincère transforme l'impossible."
        ),
        "verses": [
            ("3:37", "Chaque fois que Zakariya entrait auprès de Maryam, il trouvait chez elle une nourriture"),
            ("3:39", "Allah t'annonce la bonne nouvelle de Yahya, qui confirmera une parole d'Allah"),
            ("19:2", "C'est le récit de la miséricorde de ton Seigneur envers Son serviteur Zakariya"),
        ],
        "lesson": "Nul ne doit désespérer de la miséricorde d'Allah : Sa réponse peut venir à tout âge.",
    },
    "yahya": {
        "name": "Yahya (Jean-Baptiste)",
        "title": "Le prophète de la pureté",
        "story": (
            "Yahya naquit par un don d'Allah à Zakariya, et Allah le dota dès l'enfance de sagesse et de "
            "jugement (19:12). Il incarnait la chasteté, la pureté et la piété, et Allah l'éleva au rang des "
            "meilleurs : « Et un être pur, pieux et tendre, qui craignait Allah » (19:13-14). Il annonça et "
            "prépara la venue du Messager 'Isa. Sa vie courte fut marquée par le courage de dire la vérité "
            "jusqu'au bout. Dieu lui donne la paix : « La paix était sur lui le jour de sa naissance, de sa mort "
            "et le jour où il sera ressuscité vivant » (19:15)."
        ),
        "verses": [
            ("19:12", "Ô Yahya, tiens fermement le Livre ! Nous lui donnâmes la sagesse dès l'enfance"),
            ("3:39", "Il sera noble et chaste et prophète parmi les vertueux"),
            ("19:15", "Que la paix soit sur lui le jour de sa naissance, de sa mort et de sa résurrection"),
        ],
        "lesson": "La pureté et le courage de la vérité sont des héritages précieux transmis aux nouvelles générations.",
    },
    "isa": {
        "name": "'Isa (Jésus)",
        "title": "Le serviteur et messager d'Allah, né de Maryam",
        "story": (
            "'Isa, fils de Maryam, naquit miraculeusement sans père, par la volonté d'Allah (3:45-47 ; 19:20-21). "
            "Il parla au berceau pour défendre sa mère pieuse (19:29-33) et reçut l'Évangile. Par la permission "
            "d'Allah, il ressuscitait les morts, guérissait le lépreux et l'aveugle, et créait un oiseau d'argile "
            "(3:49). Il n'est pas une divinité, mais un serviteur d'Allah (43:59). Allah le mit à l'abri des "
            "machinations et l'éleva vers Lui (4:157-158) ; l'islam attend son retour à la fin des temps. "
            "Croyant en 'Isa, c'est croire à la puissance d'Allah et à Son unicité."
        ),
        "verses": [
            ("3:45", "Les anges dirent : ô Marie, Allah t'annonce un Verbe de Sa part : nommé le Messie, 'Isa, fils de Marie"),
            ("3:49", "Je crée pour vous, d'argile, une forme d'oiseau ; j'y souffle et elle devient oiseau par la permission d'Allah"),
            ("43:59", "'Isa n'est qu'un serviteur que Nous avons comblé de grâces"),
            ("4:157", "Ils ne l'ont ni tué ni crucifié, mais cela leur fit voir une apparence"),
        ],
        "lesson": "Les miracles sont la preuve de la puissance d'Allah, jamais une raison d'adorer autrui que Lui.",
    },
    "dhul_kifl": {
        "name": "Dhul-Kifl (Ézéchiel)",
        "title": "Le serviteur endurant",
        "story": (
            "Dhul-Kifl est cité dans le Coran parmi les prophètes doués d'endurance et élevés en dignité, "
            "aux côtés d'Ayyub et d'Ismaïl (38:48 ; 21:85). Son nom signifie « celui qui a reçu une part "
            "doublée » de récompense. Peu de détails sont donnés dans le Coran, mais sa mention enseigne la "
            "constance dans le service d'Allah. Il rappelle que la piété ne se mesure pas à la célébrité mais "
            "à l'endurance."
        ),
        "verses": [
            ("21:85", "Ismaïl, Idris et Dhul-Kifl furent tous des endurants"),
            ("38:48", "Rappelle-toi Al-Yasa et Dhul-Kifl : tous sont du nombre des meilleurs"),
        ],
        "lesson": "La constance discrète dans l'obéissance est pleinement récompensée par Allah.",
    },
    "muhammad": {
        "name": "Muhammad ﷺ",
        "title": "Le sceau des prophètes, miséricorde pour l'univers",
        "story": (
            "Muhammad ﷺ est le dernier des prophètes et des messagers (33:40). Il fut envoyé à toute l'humanité, "
            "alors que les prophètes précédents étaient envoyés à leur peuple et leur époque. Il reçut le Coran, "
            "le miracle permanent et préservé, et Allah lui dit : « Nous ne t'avons envoyé que comme miséricorde "
            "pour l'univers » (21:107). Il est le modèle parfait : véridique, digne de confiance, d'une immense "
            "bonté. Croire en lui engage à l'aimer, à suivre sa Sunna et à le défendre avec douceur et sagesse. "
            "Il demeure l'exemple suprême à imiter dans toutes les dimensions de la vie."
        ),
        "verses": [
            ("33:40", "Muhammad n'est le père d'aucun de vos hommes, mais le messager d'Allah et le sceau des prophètes"),
            ("21:107", "Nous ne t'avons envoyé que comme miséricorde pour l'univers"),
            ("2:285", "Le Messager a cru en ce qu'on a fait descendre vers lui, et les croyants aussi"),
            ("68:4", "Tu es d'une moralité éminente"),
        ],
        "lesson": "Aimer et suivre Muhammad ﷺ, c'est le prendre pour modèle en tout, jusqu'au retour d'Allah.",
    },
}

PROPHET_STORY_ALIASES = {
    "noe": "nuh", "noah": "nuh", "abraham": "ibrahim", "abrahim": "ibrahim",
    "lot": "lut", "ismael": "ismail", "isaac": "ishaq", "jacob": "yaqub",
    "joseph": "yusuf", "job": "ayyub", "jethro": "shuayb", "shuayb": "shuayb",
    "moise": "musa", "moses": "musa", "aaron": "harun", "haroun": "harun",
    "david": "dawud", "salomon": "sulayman", "souleymane": "sulayman", "sulaiman": "sulayman",
    "elie": "ilyas", "ilyes": "ilyas", "elisee": "al_yasa", "yasa": "al_yasa",
    "jonas": "yunus", "zacharie": "zakariya", "zakaria": "zakariya",
    "jean-baptiste": "yahya", "jean baptiste": "yahya", "yahia": "yahya",
    "jesus": "isa", "issa": "isa", "issah": "isa", "ezechiel": "dhul_kifl",
    "adam": "adam", "idris": "idris", "hud": "hud", "salih": "salih", "lut": "lut",
    "yusuf": "yusuf", "harun": "harun", "ilyas": "ilyas", "al-yasa": "al_yasa",
    "al yasa": "al_yasa", "dhul-kifl": "dhul_kifl", "dhul kifl": "dhul_kifl",
    "muhammad": "muhammad", "mohammed": "muhammad", "mahomet": "muhammad",
}


def _prophet_key(name: str) -> str | None:
    raw = name.strip().lower().replace("'", "")
    if raw in PROPHET_STORIES:
        return raw
    if raw in PROPHET_STORY_ALIASES:
        return PROPHET_STORY_ALIASES[raw]
    normalized = raw.replace("-", " ").replace("_", " ").strip()
    for key in PROPHET_STORIES:
        if normalized == key.replace("_", " "):
            return key
    return None


def _story_verse(ref: str, note: str) -> str:
    surah, _, ayah = ref.partition(":")
    try:
        s, a = int(surah), int(ayah)
    except ValueError:
        return f"(Référence à vérifier : {ref})"
    row = db.get_ayah(s, a)
    if not row:
        return f"(Référence à vérifier : {ref})"
    return f"{quran.format_ayah(row)}\n*{note}*"


def _show_story(key: str) -> str:
    p = PROPHET_STORIES[key]
    lines = [f"🕊️ Histoire de {p['name']} — {p['title']}", "=" * 60, "", p["story"], "", "📖 Versets clés :"]
    for ref, note in p["verses"]:
        lines.append("\n" + _story_verse(ref, note))
    lines.append("\n💡 Leçon à retenir : " + p["lesson"])
    return "\n".join(lines)


def _list_stories() -> str:
    out = [
        "🕊️ Les histoires des prophètes (25)",
        "=" * 60,
        "Tape : histoires <nom>  pour lire une histoire.",
        "",
    ]
    for i, key in enumerate(PROPHET_STORIES, 1):
        out.append(f"{i:>2}. {PROPHET_STORIES[key]['name']}")
    out.append("\nExemple : histoires yusuf, histoires musa, histoires muhammad")
    return "\n".join(out)


def _stories_dispatch(args: list[str]) -> str:
    if not args or args[0].lower() in ("aide", "help", "liste", "list"):
        return _list_stories()
    key = _prophet_key(args[0])
    if not key:
        return f"Prophète inconnu : « {args[0]} ». Tape 'histoires' pour la liste."
    return _show_story(key)


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


PRAYER_LABELS = {
    "imsak": "Imsak",
    "fajr": "Aube (Fajr)",
    "sunrise": "Lever du soleil",
    "dhuhr": "Midi (Dhuhr)",
    "asr": "Après-midi (Asr)",
    "maghrib": "Coucher du soleil (Maghrib)",
    "isha": "Nuit (Isha)",
}


def _parse_latlon(args: list[str]) -> tuple[float, float, str | None] | None:
    """Parse ['lat', 'lon', 'timezone'] → triplette, ou None si invalide."""
    if len(args) < 2:
        return None
    try:
        lat, lng = float(args[0]), float(args[1])
    except ValueError:
        return None
    tz = " ".join(args[2:]).strip() or None
    return lat, lng, tz


def _hijri() -> str:
    from agent import api

    try:
        data = api.hijri()
        hij, greg = data["hijri"], data["gregorian"]
    except api.ApiError as exc:
        return str(exc)
    lines = [
        "📅 Date islamique (hijri)",
        "=" * 60,
        f"{hij['formatted']}  ·  {hij['month_name_arabic']} ({hij['month_name']})",
        f"Géorgien : {greg['formatted']}",
        f"Ère : {hij['era']}",
    ]
    try:
        events = api.islamic_events()
        next_event = events.get("next_event")
        if next_event:
            lines.append("")
            lines.append(f"⏳ Prochain événement : {next_event['name']} — {next_event['hijri_date']}")
    except api.ApiError:
        pass
    lines.append("")
    lines.append("ℹ Les dates peuvent varier de 1 à 2 jours selon l'observation de la lune.")
    return "\n".join(lines)


def _prayer_times(args: list[str]) -> str:
    from agent import api

    if not args:
        return (
            "Usage : prieres <ville> [pays] | prieres <lat> <lon> [timezone]\n"
            "Exemples : prieres Dakar | prieres Dakar Senegal | prieres 14.69 -17.44"
        )
    coords = _parse_latlon(args)
    if coords:
        lat, lng, tz = coords
        place = f"{lat}, {lng}"
    else:
        city = args[0]
        country = " ".join(args[1:]) if len(args) > 1 else None
        try:
            place_info = api.geocode(city, country)
        except api.ApiError as exc:
            return str(exc)
        if not place_info:
            return f"Ville « {city} » introuvable (géocodage Open-Meteo)."
        lat, lng = place_info["latitude"], place_info["longitude"]
        tz = place_info.get("timezone")
        place = f"{place_info['name']} ({place_info.get('country', '')})"
    try:
        data = api.prayer_times(lat, lng, timezone=tz)
    except api.ApiError as exc:
        return str(exc)
    lines = [
        f"🕌 Horaires de prière — {place}",
        "=" * 60,
        f"Date : {data['date']}   ·   Méthode : {data.get('calculation_method')}   ·   Madhhab : {data.get('madhab')}",
        "",
    ]
    times = data.get("prayer_times", {})
    for key, label in PRAYER_LABELS.items():
        if key in times:
            lines.append(f"  ·  {label:<30} {times[key]}")
    status = data.get("current_status") or {}
    if status.get("next_prayer"):
        lines.append("")
        lines.append(
            f"⏱ Actuellement : {status.get('current_prayer', '?')} → prochaine prière : "
            f"{status['next_prayer']} ({status.get('time_until_next', '?')})"
        )
    lines.append("")
    lines.append("ℹ Calcul astronomique — les horaires des mosquées locales peuvent varier légèrement.")
    return "\n".join(lines)


def _qibla(args: list[str]) -> str:
    from agent import api

    coords = _parse_latlon(args)
    if not coords:
        return "Usage : qibla <latitude> <longitude>\nExemple : qibla 14.69 -17.44 (Dakar)"
    lat, lng, _ = coords
    try:
        data = api.qibla(lat, lng)
    except api.ApiError as exc:
        return str(exc)
    lines = [
        "🧭 Direction de la Qibla",
        "=" * 60,
        f"Position : {data['location']['latitude']}, {data['location']['longitude']}",
        f"Direction : {data['qibla_direction']}° ({data.get('compass_bearing', '')})",
        f"Distance de la Kaaba : {data.get('distance_km', 0):.0f} km ({data.get('distance_miles', 0):.0f} mi)",
        "",
        "ℹ Angle par rapport au nord géographique (vrai nord), pas le nord magnétique.",
    ]
    return "\n".join(lines)


def _tafsir(args: list[str]) -> str:
    from agent import api

    if not args:
        return "Usage : tafsir <sourate>[:<verset>]\nExemples : tafsir 2:255, tafsir 1"
    try:
        surah, ayah, _ = quran.parse_ref(" ".join(args))
    except ValueError:
        return "Référence incomprise. Exemples : tafsir 2:255, tafsir 1"
    if ayah is None:
        ayah = 1
    meta = db.get_surah_meta(surah)
    if not meta:
        return f"Sourate {surah} introuvable (1–114)."
    if not 1 <= ayah <= meta["total_verses"]:
        return f"Le verset {surah}:{ayah} n'existe pas (la sourate a {meta['total_verses']} versets)."
    try:
        data = api.tafsir(surah, ayah)
    except api.ApiError as exc:
        return str(exc)
    row = db.get_ayah(surah, ayah)
    lines = [f"📜 Tafsir Ibn Kathir — Coran {surah}:{ayah} ({meta['transliteration']})", "=" * 60]
    if row:
        lines += ["", row["text_ar"], f"  — {row['text_fr']}", f"  – {row['text_en']}", ""]
    text = (data.get("tafsir") or {}).get("text", "").strip()
    if not text:
        return "\n".join(lines) + "\n(Tafsir non disponible pour ce verset.)"
    if len(text) > 2200:
        text = text[:2200] + "\n…"
    lines.append(text)
    lines.append("")
    lines.append("ℹ Tafsir Ibn Kathir (abrégé, en anglais) via l'API UmmahAPI.")
    return "\n".join(lines)


# ── Complétion par TAB (readline) ────────────────────────────
_ALL_COMMANDS = [
    "aide", "apprendre", "coran", "foi",
    "hadith", "hijri", "histoires", "noms", "piliers", "prieres",
    "prophètes", "qibla", "quiz", "sourates", "tafsir", "quitter",
]

_ALL_ALIASES = [
    "exit", "help", "histoire", "learn", "priere",
    "prophetes", "quit", "récits", "recits", "stories", "?",
]

_SUBCOMMANDS = {
    "coran": ["chercher", "list"],
    "hadith": ["hasard", "chercher", "livres", "liste", "livre", "hadith"],
    "apprendre": ["lecon", "terminer"],
    "quiz": ["coran", "hadith", "mixte"],
    "sourates": ["importantes"],
    "histoires": ["aide", "liste"],
}


def _complete_candidates(line: str, text: str) -> list[str]:
    """Propose des complétions pour la ligne saisie (insensible à la casse)."""

    def books() -> list[str]:
        return [b["slug"] for b in db.list_books()]

    def prophets() -> list[str]:
        return sorted(set(PROPHET_STORIES) | set(PROPHET_STORY_ALIASES))

    def lessons() -> list[str]:
        return sorted({l["id"] for l in curriculum.LESSONS})

    tokens = line.split()
    trailing_space = line.endswith((" ", "\t"))
    if trailing_space or not tokens:
        completed, current = tokens, text
    else:
        completed, current = tokens[:-1], tokens[-1]
    lower = current.strip().lower()

    if not completed:
        names = {c.lower(): c for c in _ALL_COMMANDS + _ALL_ALIASES}
        return sorted(n for n in names if n.startswith(lower))

    cmd = completed[0].lower()
    n_after = len(completed) - 1

    # Premier mot d'argument : sous-commandes (ou entités propres à la commande)
    if n_after == 0:
        subs = list(_SUBCOMMANDS.get(cmd, ()))
        if cmd == "apprendre":
            subs += lessons()
        if cmd == "histoires":
            subs += prophets()
        return sorted(s for s in set(subs) if s.lower().startswith(lower))

    second = completed[1].lower()

    if cmd == "apprendre" and second in ("lecon", "terminer"):
        return sorted(i for i in lessons() if i.startswith(lower))

    if cmd == "histoires":
        return sorted(p for p in prophets() if p.startswith(lower))

    if cmd == "hadith":
        later = [c.lower() for c in completed[1:]]
        if "livre" in later:
            return sorted(b for b in books() if b.startswith(lower))
        if second in ("hasard", "livre", "hadith") and n_after == 1:
            return sorted(b for b in books() if b.startswith(lower))

    return []


def _completer(text: str, state: int) -> str | None:
    import readline

    options = _complete_candidates(readline.get_line_buffer(), text)
    return options[state] if state < len(options) else None


def _enable_tab_completion() -> None:
    import readline

    readline.set_completer(_completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set show-all-if-ambiguous on")


def repl() -> None:
    _enable_tab_completion()
    print(HELP)
    first = True
    while True:
        try:
            if first:
                print("\nCommencer ? 'apprendre' pour le plan, 'quiz' pour tester, ou 'aide' pour voir les commandes.\n")
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