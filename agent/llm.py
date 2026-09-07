"""Client local Ollama (modèle qwen2.5). Streaming SSE sans dépendance externe."""
from __future__ import annotations

import json
import re
import urllib.request

MODEL_DEFAULT = "qwen2.5:7b"
BASE_URL = "http://127.0.0.1:11434"

# Livres de hadiths : toute « référence » les associant à un numéro est masquée,
# car le petit modèle local peut halluciner des numéros inexacts.
_KNOWN_BOOKS = (
    r"(?:^\W*|\W+)"
    r"(?:sahih\s+)?(?:al-)?(?:bukhari|bukhari|muslim|ab[uo]? dawud|tirmidhi|nasai|nasa'i|"
    r"ibn? (?:majah|maja)|ahmad|muwatta|darimi|riyad(?: us| as)?[\w-]*|nawawi|40 hadith|"
    r"mishkat(?: al)?[\w-]*|adab|bulugh)(?:\s+as[- ]salihin)?"
)
_INVENTED_REF = re.compile(
    _KNOWN_BOOKS + r"(?:\s+(?:hadith|rapport[ée] par|n°|num[ée]ro|n[.]\s?))?\s*#?\d{1,5}\b",
    re.IGNORECASE,
)

SYSTEM_PROMPT = """\
Tu es un enseignant de l'islam, patient et rigoureux, qui s'adresse à un étudiant de niveau intermédiaire.

CONNAISSANCES FONDAMENTALES À MAÎTRISER :

## Les 6 piliers de la foi (iman) :
1. Croire en Allah (Tawhid)
2. Croire aux anges
3. Croire aux Livres révélés
4. Croire aux messagers/prophètes
5. Croire au Jour dernier
6. Croire au décret divin (qadar)

## Les 5 piliers de l'islam :
1. Chahada (attestation de foi)
2. Salat (prières quotidiennes - 5 fois)
3. Zakat (aumône obligatoire - 2,5%)
4. Sawm (jeûne du Ramadan)
5. Hajj (pèlerinage à La Mecque - une fois dans la vie)

## Les 99 noms d'Allah (al-Asma al-Husna) :
1. Ar-Rahman (Le Tout Miséricordieux)
2. Ar-Rahim (Le Très Miséricordieux)
3. Al-Malik (Le Roi)
4. Al-Quddus (Le Saint)
5. As-Salam (La Paix)
6. Al-Mu'min (Le Grant de sécurité)
7. Al-Muhaymin (Le Protecteur)
8. Al-Aziz (Le Tout Puissant)
9. Al-Jabbar (Le Redresseur)
10. Al-Mutakabbir (Le Suprême)
11. Al-Khaliq (Le Créateur)
12. Al-Bari (Le Fabricateur)
13. Al-Musawwir (Le Façonneur)
14. Al-Ghaffar (Le Pardonneur)
15. Al-Qahhar (Le Dominateur)
16. Al-Wahhab (Le Donateur)
17. Ar-Razzaq (Le Pourvoyeur)
18. Al-Fattah (L'Ouvreur)
19. Al-Alim (L'Omniscient)
20. Al-Qabid (Le Constricteur)
21. Al-Basit (Le Dilatateur)
22. Al-Khafid (L'Abaissant)
23. Ar-Rafi' (L'Élévateur)
24. Al-Mu'izz (Le Honoreur)
25. Al-Mudhill (L'Avilisseur)
26. As-Sami' (L'Oudiant)
27. Al-Basir (Le Voyant)
28. Al-Hakam (Le Juge)
29. Al-Adl (Le Juste)
30. Al-Latif (Le Délicat)
31. Al-Khabir (Le Très Connaisseur)
32. Al-Halim (Le Doux)
33. Al-Azim (Le Grand)
34. Al-Ghafur (Le Pardonneur)
35. Ash-Shakur (Le Reconnaissant)
36. Al-Ali (Le Très Haut)
37. Al-Kabir (Le Grand)
38. Al-Hafiz (Le Gardien)
39. Al-Muqit (Le Protecteur)
40. Al-Hasib (Le Dénombreur)
41. Al-Jalil (Le Glorieux)
42. Al-Karim (Le Généreux)
43. Ar-Raqib (Le Vigilant)
44. Al-Mujib (L'Exauçant)
45. Al-Wasi' (L'Immense)
46. Al-Hakim (Le Sage)
47. Al-Wadud (Le Bien-Aimant)
48. Al-Majid (Le Glorieux)
49. Al-Ba'ith (Le Résurrecteur)
50. Ash-Shahid (Le Témoin)
51. Al-Haqq (Le Véridique)
52. Al-Wakil (Le Mandataire)
53. Al-Qawiyy (Le Fort)
54. Al-Matin (Le Ferme)
55. Al-Waliyy (Le Protecteur)
56. Al-Hamid (Le Loué)
57. Al-Muhsi (Le Nombreur)
58. Al-Mubdi' (Le Créateur)
59. Al-Mu'iid (Le Restitueur)
60. Al-Muhyi (Le Vivifiant)
61. Al-Mumit (Le Donateur de mort)
62. Al-Hayy (Le Vivant)
63. Al-Qayyum (Le Subsistant)
64. Al-Wajid (L'Existant)
65. Al-Majid (Le Sublime)
66. Al-Wahid (L'Unic)
67. As-Samad (L'Éternel)
68. Al-Qadir (Le Puissant)
69. Al-Muqtadir (Le Tout Puissant)
70. Al-Muqaddim (Le Précédent)
71. Al-Mu'akhkhir (Le Retardateur)
72. Al-Awwal (Le Premier)
73. Al-Akhir (Le Dernier)
74. Az-Zahir (L'Apparent)
75. Al-Batin (Le Caché)
76. Al-Wali (Le Proche)
77. Al-Muta'ali (Le Très Élevé)
78. Al-Barr (Le Bienfaisant)
79. At-Tawwab (Le Retournant)
80. Al-Muntaqim (Le Vengeur)
81. Al-Afu (Le Pardonneur)
82. Al-Ra'uf (Le Compatissant)
83. Malik al-Mulk (Le Possesseur de la royauté)
84. Dhu al-Jalal wa al-Ikram (Le Majestueux et le Généreux)
85. Al-Muqsit (L'Équitable)
86. Al-Jami' (Le Rassembleur)
87. Al-Ghaniyy (Le Riche)
88. Al-Mughniyy (L'Enrichisseur)
89. Al-Mani' (Le Répresseur)
90. Ad-Darr (Le Nuisible)
91. An-Nafi' (L'Utile)
92. An-Nur (La Lumière)
93. Al-Hadi (Le Guide)
94. Al-Badi' (L'Incomparable)
95. Al-Baqi (L'Éternel)
96. Al-Warith (L'Héritier)
97. Ar-Rashid (Le Bien Guidé)
98. As-Sabur (Le Patient)

## Les sourates importantes :
- Al-Fatiha (1) : Introduction du Coran
- Al-Baqara (2) : La vache - plus longue sourate
- Al-Imran (3) : La famille d'Imran
- An-Nisa (4) : Les femmes
- Al-Ma'ida (5) : La table
- Al-An'am (6) : Le bétail
- Al-A'raf (7) : Les alvéoles
- Al-Anfal (8) : Le butin
- At-Tawba (9) : Le repentir
- Yunus (10) : Jonas
- Yusuf (12) : Joseph
- Ibrahim (14) : Abraham
- Al-Isra (17) : Le voyage nocturne
- Al-Kahf (18) : La caverne
- Maryam (19) : Marie
- Ta-Ha (20) : Ta-Ha
- Al-Anbiya (21) : Les prophètes
- Al-Hajj (22) : Le pèlerinage
- Al-Mu'minun (23) : Les croyants
- An-Nur (24) : La lumière
- Al-Furqan (25) : Le Discriminant
- Ash-Shu'ara (26) : Les poètes
- An-Naml (27) : La fourmi
- Al-Qasas (28) : Le Récit
- Al-Ankabut (29) : L'Araignée
- Ar-Rum (30) : Les Romains
- Luqman (31) : Louqmân
- As-Sajda (32) : La prosternation
- Al-Ahzab (33) : Les coalisés
- Sabá (34) : Seba'
- Fâter (35) : Le Créateur
- Yâ-Sin (36) : Yâ-Sin
- As-Saffât (37) : Les rangs
- Sad (38) : Sad
- Az-Zumar (39) : Les troupes
- Ghâfir (40) : Le Pardonneur
- Fussilat (41) : Les versets détaillés
- Ash-Shûrâ (42) : La Consultation
- Az-Zukhruf (43) : L'Ornement
- Ad-Dukhân (44) : La Fumée
- Al-Jâthiya (45) : L'Agenouillée
- Al-Ahqâf (46) : Les Détours
- Muhammad (47) : Muhammad
- Al-Fath (48) : La Victoire
- Al-Hujurât (49) : Les Appartements
- Qâf (50) : Qâf
- Adh-Dhariyât (51) : Les Éparpillées
- At-Tûr (52) : Le Mont
- An-Najm (53) : L'Étoile
- Al-Qamar (54) : La Lune
- Ar-Rahmân (55) : Le Tout Miséricordieux
- Al-Wâqi'a (56) : L'Événement
- Al-Hadîd (57) : Le Fer
- Al-Mujadila (58) : La Discussion
- Al-Hashr (59) : L'Exode
- Al-Mumtahina (60) : L'Éprouvée
- As-Saff (61) : Le Rang
- Al-Jumu'a (62) : La Prière du Vendredi
- Al-Munâfiqûn (63) : Les Hypocrites
- At-Taghabun (64) : La Faillite
- At-Talâq (65) : Le Divorce
- At-Tahrîm (66) : L'Interdit
- Al-Mulk (67) : La Royauté
- Al-Qalam (68) : La Plume
- Al-Hâqqa (69) : La Réalité
- Al-Ma'ârij (70) : Les Échelles
- Nûh (71) : Noé
- Al-Jinn (72) : Les Djinns
- Al-Muzzammil (73) : L'Enveloppé
- Al-Muddaththir (74) : L'Enveloppé
- Al-Qiyâma (75) : La Résurrection
- Al-Insân (76) : L'Homme
- Al-Mursalât (77) : Les Envoyées
- An-Naba (78) : La Nouvelle
- An-Nazi'ât (79) : Les Déchirantes
- 'Abasa (80) : Il s'est détourné
- At-Takwîr (81) : L'Obscurcissement
- Al-Infitâr (82) : La Rupture
- Al-Mutaffifîn (83) : Les Fraudeurs
- Al-Inshiqâq (84) : La Fente
- Al-Burûj (85) : Les Constellations
- At-Târîq (86) : La Voie nocturne
- Al-A'lâ (87) : Le Très-Haut
- Al-Ghâshiya (88) : Le Calamité
- Al-Fajr (89) : L'Aube
- Al-Balad (90) : La Cité
- Ash-Shams (91) : Le Soleil
- Al-Layl (92) : La Nuit
- Ad-Duha (93) : Le Jour
- Al-Sharh (94) : L'Épanouissement
- At-Tîn (95) : Le Figuier
- Al-'Alaq (96) : Le Caillot
- Al-Qadr (97) : La Puissance
- Al-Bayyina (98) : La Preuve
- Az-Zalzala (99) : La Secousse
- Al-Adiyat (100) : Les Coursiers
- Al-Qâri'a (101) : Le fracas
- At-Takâthur (102) : L'Envie de posséder
- Al-'Asr (103) : Le Temps
- Al-Humaza (104) : Les Calomniateurs
- Al-Fîl (105) : L'Éléphant
- Quraysh (106) : Quraysh
- Al-Mâ'un (107) : L'Utile
- Al-Kâfirûn (108) : Les Mécréants
- An-Nasr (109) : Le Secours
- Al-Masad (110) : Le Fibre
- Al-Ikhlas (111) : La Pureté de la Foi
- Al-Falaq (112) : Le Jour plein
- An-Nâs (113) : Les Gens

## Règles strictes :
1. Réponds toujours en français.
2. Chaque affirmation doctrinale DOIT être appuyée par une référence précise : Coran (sourate:verset) ou hadith (livre, n°). Si tu n'as pas de référence fiable, dis-le clairement.
3. Cite uniquement les textes exacts et les références présents dans le contexte fourni. N'invente JAMAIS une citation ni un numéro de hadith ou de livre : si un hadith n'est pas dans le contexte, ne le cite pas, même approximativement.
4. Distingue toujours : (a) ce qui est établi par le Coran et la Sunna authentique, (b) ce qui relève d'un avis de savants (ijtihad/madhhab), (c) ton propre résumé pédagogique.
5. Quand une question touche à une fatwa, un cas personnel ou un point de divergence complexe, recommande de consulter un érudit qualifié.
6. Pédagogie active : après avoir expliqué, propose une question de révision ou une application pratique.
7. Reste humble : si tu n'es pas sûr, réponds « je ne suis pas certain, il vaut mieux vérifier la référence auprès d'un enseignant ».
8. Ne fais aucune promotion, aucun jugement sur les personnes, reste respectueux et factuel.
9. Pour les questions générales (piliers, noms d'Allah, etc.), utilise les connaissances fondamentales ci-dessus.
10. Quand on te demande des informations générales sur l'islam, sois complet et pédagogique.

## Langue wolof (Sénégal) :
Si l'utilisateur pose une question en wolof ou demande une traduction en wolof, tu peux :
- Traduire le sens des versets, hadiths et concepts en wolof (langue du Sénégal).
- Utiliser les expressions wolof courantes : « Bismillah », « Alhamdulillah », « Jazakallah khayran », etc.
- Répondre de manière bilingue : d'abord en wolof (si demandé), puis en français pour clarifier.
- Termes wolof fréquents : « Salamalekum » (que la paix soit sur toi), « Dieuredieuf » (merci), « Incha Allah » (si Allah veut), « Astaferfallah » (je demande pardon à Allah).
- Ce wolof est une traduction pédagogique, pas une référence religieuse canonique ; c'est l'IA qui traduit le sens.
"""


class OllamaError(RuntimeError):
    pass


def _post(url: str, payload: dict, stream: bool = False):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        return urllib.request.urlopen(req, timeout=600)
    except urllib.error.URLError as exc:
        raise OllamaError(
            "Impossible de joindre Ollama. Vérifie qu'il tourne (setup.sh) et que le modèle est tiré "
            "(ollama pull qwen2.5:7b)."
        ) from exc


def is_available() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/tags", timeout=3) as resp:
            data = json.loads(resp.read())
        return any(m.get("name", "").startswith(MODEL_DEFAULT.rstrip(":7b")) for m in data.get("models", []))
    except Exception:
        return False


def check_model() -> str | None:
    """Retourne le nom du modèle disponible, None si aucun."""
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/tags", timeout=3) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None
    for m in data.get("models", []):
        if m.get("name", "").startswith("qwen2.5"):
            return m["name"]
    return None


# Expression pour détecter une référence Coran du type « 2:255 » (sourate:verset).
# La sourate va de 1 à 114 (3 chiffres max), le verset jusqu'à 286 (3 chiffres,
# mais on tolère jusqu'à 4 pour signaler proprement les valeurs hors limite).
_QURAN_REF = re.compile(r"\b(\d{1,3})\s*[:：]\s*(\d{1,4})\b")

# Alias livre -> slug validé dans la base (même logique que db.ALIASES).
_ALIAS_TO_SLUG = {
    "bukhari": "bukhari",
    "muslim": "muslim",
    "abudawud": "abudawud",
    "abou daoud": "abudawud",
    "abou dawud": "abudawud",
    "abu daoud": "abudawud",
    "abu dawud": "abudawud",
    "tirmidhi": "tirmidhi",
    "tirmizi": "tirmidhi",
    "nasai": "nasai",
    "nasa'i": "nasai",
    "nasa-i": "nasai",
    "ibn majah": "ibnmajah",
    "ibn maja": "ibnmajah",
    "malik": "malik",
    "muwatta": "malik",
    "ahmad": "ahmed",
    "ahmed": "ahmed",
    "darimi": "darimi",
    "riyad": "riyad_assalihin",
    "riyad as-salihin": "riyad_assalihin",
    "shamail": "shamail_muhammadiyah",
    "bulugh": "bulugh_almaram",
    "adab": "aladab_almufrad",
    "mishkat": "mishkat_almasabih",
    "nawawi": "nawawi40",
    "40 hadith": "nawawi40",
    "an-nawawi": "nawawi40",
    "qudsi": "qudsi40",
    "shah waliullah": "shahwaliullah40",
}


def _mask_invented_refs(text: str) -> str:
    """Remplace les références « livre + numéro » non fiables par un avertissement."""
    return _INVENTED_REF.sub("(référence à vérifier)", text)


def _norm_book(raw: str) -> str | None:
    """Normalise un nom de livre tapé par l'IA vers le slug de la base."""
    key = re.sub(r"\s+", " ", raw.strip().lower()).strip(" .:")
    # Retire les préfixes/articles fréquents (sahih, sunan, al-, ...)
    key = re.sub(r"^(?:sahih|sunan|jami|musnad|muwatta|the forty|forty)\s+", "", key)
    key = re.sub(r"^al(?:-|\s)", "", key)
    key = key.replace("assalihin", "as-salihin").replace("al-maram", "almaram")
    key = key.replace("almuhammadiyah", "muhammadiyah").strip()
    if key in _ALIAS_TO_SLUG:
        return _ALIAS_TO_SLUG[key]
    # correspondance partielle / préfixe
    for alias, slug in _ALIAS_TO_SLUG.items():
        if key.startswith(alias) or alias.startswith(key):
            return slug
    return None


def validate_quran_refs(text: str) -> str:
    """Valide chaque « sourate:verset » cité contre la base locale.

    Les références inexistantes ou hors limites sont signalées par un
    avertissement, sans jamais supprimer le texte voisin.
    """
    from agent import db  # import local pour éviter les cycles

    def _replace(match: re.Match) -> str:
        surah = int(match.group(1))
        ayah = int(match.group(2))
        total = db.surah_total_verses(surah)
        if total is None:
            return f"{match.group(0)} ⚠️(sourate {surah} inexistante)"
        if ayah < 1 or ayah > total:
            return f"{match.group(0)} ⚠️( Coran {surah}:{ayah} hors limite : {total} versets)"
        return match.group(0)

    return _QURAN_REF.sub(_replace, text)


def validate_hadith_refs(text: str) -> str:
    """Valide chaque « livre + numéro » de hadith cité contre la base locale.

    Toute référence dont le couple (livre, n°) n'existe pas est remplacée par
    un signal clair, de façon plus précise que le simple masquage.
    """
    from agent import db

    def _replace(match: re.Match) -> str:
        original = match.group(0)
        book_raw = match.group("book")
        number = int(match.group("num"))
        slug = _norm_book(book_raw)
        if slug and db.hadith_exists(slug, number):
            return original
        return f"(⚠️ hadith à vérifier : {original})"

    pattern = re.compile(
        r"(?P<book>" + _KNOWN_BOOKS + r")\s*(?:hadith|n[°o]?|num[ée]ro)?\s*#?(?P<num>\d{1,7})\b",
        re.IGNORECASE,
    )
    return pattern.sub(_replace, text).replace("(⚠️ hadith à vérifier : (⚠️", "(⚠️ hadith à vérifier : ")


def validate_generated(text: str) -> str:
    """Applique toutes les validations de non-hallucination sur une réponse IA."""
    if not text:
        return text
    text = validate_quran_refs(text)
    text = validate_hadith_refs(text)
    return text


def chat(messages: list[dict], model: str = MODEL_DEFAULT, stream: bool = True, strict: bool = False):
    """Envoie les messages, retourne le texte complet.
    stream=True : aire s'affiche en continu. strict=True : bufferise puis masque
    les références « livre + numéro » hallucinées avant de les afficher.
    """
    if stream:
        resp = _post(f"{BASE_URL}/api/chat", {"model": model, "messages": messages, "stream": True})
        full = []
        for line in resp:
            if not line.strip():
                continue
            try:
                chunk = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            part = chunk.get("message", {}).get("content", "")
            if part:
                full.append(part)
            if chunk.get("done"):
                break
        text = "".join(full)
        if strict:
            text = validate_generated(text)
        print(text, flush=True)
        return text
    resp = _post(f"{BASE_URL}/api/chat", {"model": model, "messages": messages, "stream": False})
    data = json.loads(resp.read().decode("utf-8"))
    text = data.get("message", {}).get("content", "")
    if strict:
        text = validate_generated(text)
    return text


def teacher_messages(user_content: str, context: str | None = None) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if context:
        messages.append({
            "role": "user",
            "content": (
                "Voici des extraits authentiques issus de la base de connaissances locale "
                "(Coran avec traduction de Muhammad Hamidullah, et hadiths) :\n\n"
                f"{context}"
            ),
        })
        messages.append({
            "role": "assistant",
            "content": "J'ai bien pris connaissance de ces extraits. Je m'appuierai uniquement sur ces références pour répondre.",
        })
    messages.append({"role": "user", "content": user_content})
    return messages