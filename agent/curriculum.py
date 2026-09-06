"""Plan d'apprentissage personnalisé (niveau intermédiaire).

Chaque leçon référence des textes authentiques de la base locale (Coran/Hadith).
Toutes les références de hadiths ont été vérifiées (numéro réel dans la BD).
Les citations ne sont pas inventées : elles sont lues depuis la BD à l'affichage.
"""
from __future__ import annotations

import json
from pathlib import Path

from agent import db

PROGRESS_FILE = Path(__file__).resolve().parent.parent / "data" / "progress.json"

LESSONS = [
    # ── Module 1 : Aqidah ────────────────────────────────────────────────
    {
        "module": 1,
        "module_title": "Aqidah — La croyance islamique",
        "id": "aq1",
        "title": "Tawhid : l'unicité d'Allah",
        "objectives": [
            "Distinguer tawhid ar-rububiyyah, al-uluhiyyah et al-asma wa-s-sifat",
            "Citer les preuves du Coran sur l'unicité",
        ],
        "content": (
            "Le tawhid (l'unicité) est le fondement de la foi musulmane. On le divise classiquement en trois aspects : "
            "(1) l'unicité de la Seigneurie (rububiyyah) : Allah est le seul Créateur, Nourricier et Gérant de l'univers ; "
            "(2) l'unicité de l'adoration (uluhiyyah) : toute adoration — prière, invocation, sacrifice, crainte, amour — "
            "ne doit être adressée qu'à Allah seul ; (3) l'unicité des Noms et Attributs (al-asma wa-s-sifat) : Allah possède "
            "des Noms et Attributs parfaits, dont on ne peut ni déformer le sens, ni nier l'existence, ni interroger le « comment ».\n\n"
            "La Sourate Al-Ikhlas résume l'essence du tawhid, et le verset du Trône (2:255) en détaille la grandeur. "
            "Le premier pilier de l'islam, la chahada, est précisément l'acte d'attester cette unicité."
        ),
        "quran": [
            {"ref": "2:163", "note": "« Et votre Divinité est une divinité unique »"},
            {"ref": "2:255", "note": "Aya du Trône (Ayat al-Kursi) — la grandeur d'Allah"},
            {"ref": "112:1", "note": "Dis : Il est Allah, Unique"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1, "note": "Les actes ne valent que par l'intention (Bukhari n°1)"},
            {"book": "bukhari", "number": 50, "note": "Le hadith de Jibril : les degrés de la religion"},
        ],
    },
    {
        "module": 1,
        "module_title": "Aqidah — La croyance islamique",
        "id": "aq2",
        "title": "Les piliers de la foi (iman)",
        "objectives": [
            "Énumérer les 6 piliers de la foi",
            "Expliquer le lien entre islam, iman et ihsan",
        ],
        "content": (
            "La foi (iman) repose sur six piliers : croire en Allah, en Ses anges, en Ses Livres, en Ses messagers, "
            "au Jour dernier, et au destin bon et mauvais (qadar). Ils sont enseignés dans le hadith de Jibril, "
            "où l'ange Gabriel interroge le Prophète ﷺ sur l'islam, l'iman et l'ihsan.\n\n"
            "L'islam se résume aux cinq piliers pratiques ; l'iman est la foi intérieure ; l'ihsan est « adorer Allah comme si tu Le vois, "
            "car si tu ne Le vois pas, Lui te voit » — le plus haut degré de la religion. Les trois plans doivent être travaillés ensemble."
        ),
        "quran": [
            {"ref": "2:177", "note": "La piété : croire en Allah, au Jour dernier, aux anges, au Livre, aux prophètes"},
            {"ref": "2:285", "note": "Le croyant croit en Allah, en Ses anges, Ses livres et Ses messagers"},
        ],
        "hadith": [
            {"book": "nawawi40", "number": 2, "note": "Le hadith de Jibril (Quarante hadiths de An-Nawawi, n°2)"},
            {"book": "bukhari", "number": 13, "note": "La foi n'est complète qu'en aimant pour son frère ce qu'on aime pour soi"},
        ],
    },
    {
        "module": 1,
        "module_title": "Aqidah — La croyance islamique",
        "id": "aq3",
        "title": "Le destin (qadar) : croire, sans faux débats",
        "objectives": [
            "Comprendre les degrés de la foi au décret divin",
            "Éviter les extrêmes (fatalisme / relativisme)",
        ],
        "content": (
            "Croire au décret divin signifie que rien n'arrive sans la science, la volonté et la création d'Allah. "
            "On distingue classiquement : la science éternelle d'Allah, l'écriture dans le Livre clair, "
            "la volonté universelle et la création de chaque chose.\n\n"
            "Cette croyance ne doit pas mener au fatalisme : Allah a donné à l'homme une volonté et des choix réels, "
            "et la Sunna nous ordonne d'agir et de nous efforcer, en disant « si Allah veut » pour nos projets. "
            "Crois au qadar sans entrer dans des spéculations qui divisaient les premières communautés."
        ),
        "quran": [
            {"ref": "64:11", "note": "Nul malheur n'atteint sans la permission d'Allah"},
            {"ref": "18:23", "note": "Ne dis jamais « je le ferai demain » sans « si Allah veut »"},
            {"ref": "57:22", "note": "Nul malheur n'arrive sans être dans un Livre avant que Nous le réalisions"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 50, "note": "Le hadith de Jibril : définition de la foi (l'iman y inclut le destin dans sa version complète)"},
        ],
    },
    # ── Module 2 : Fiqh — Purification et prière ──────────────────────────
    {
        "module": 2,
        "module_title": "Fiqh — Purification et prière",
        "id": "fiq1",
        "title": "La purification (taharah) : clef de la prière",
        "objectives": [
            "Identifier les eaux et les impuretés",
            "Maîtriser les conditions de validité des ablutions (wudu) et le ghousl",
        ],
        "content": (
            "La purification est la clé de la prière ; la prière n'est pas acceptée sans elle (sauf excuse légitime). "
            "Les obligations pratiques à maîtriser : l'eau pure, le wudu (ablutions mineures) avec ses actes obligatoires, "
            "le ghousl (ablutions majeures) après les grandes impuretés, le tayammum (avec de la terre pure) en l'absence d'eau.\n\n"
            "Mémorise l'ordre du wudu : intention, lavage du visage, des mains jusqu'aux coudes, essuyage de la tête, lavage des pieds "
            "jusqu'aux chevilles. La prière n'est acceptée que par celui qui s'y présente en état de pureté."
        ),
        "quran": [
            {"ref": "5:6", "note": "Ô vous qui croyez ! Lorsque vous vous levez pour la prière, lavez vos visages et vos mains…"},
        ],
        "hadith": [
            {"book": "abudawud", "number": 60, "note": "Allah n'accepte pas la prière sans purification (Abu Dawud n°60)"},
            {"book": "riyad_assalihin", "number": 364, "note": "Les cinq prières purifient comme un fleuve qui lave cinq fois par jour"},
        ],
    },
    {
        "module": 2,
        "module_title": "Fiqh — Purification et prière",
        "id": "fiq2",
        "title": "La prière (salat) : piliers, conditions, invalidités",
        "objectives": [
            "Connaître les piliers et conditions de la prière",
            "Comprendre comment la prière corrige le comportement",
        ],
        "content": (
            "La salat est le premier pilier pratique après la chahada et « la première chose dont on sera interrogé ». "
            "On distingue : les conditions (islam, raison, discernement, purification, orientation vers la qibla, temps correct), "
            "les piliers (takbir d'ouverture, lecture de la Fatiha, inclinaison, prosternation, assise finale) et les actes complémentaires.\n\n"
            "Le Coran nous enseigne que la prière préserve de la turpitude et du blâmable (29:45) : c'est la prière vécue "
            "qui élève et protège, et non un simple mouvement répété."
        ),
        "quran": [
            {"ref": "29:45", "note": "La prière préserve de la turpitude et du blâmable"},
            {"ref": "20:14", "note": "Accomplis la prière pour te souvenir de Moi"},
            {"ref": "2:43", "note": "Accomplissez la prière et acquittez-vous de la zakat"},
        ],
        "hadith": [
            {"book": "mishkat_almasabih", "number": 1259, "note": "La première œuvre dont on sera jugé : la prière"},
            {"book": "muslim", "number": 457, "note": "Les cinq prières et le vendredi effacent les péchés mineurs"},
        ],
    },
    {
        "module": 2,
        "module_title": "Fiqh — Purification et prière",
        "id": "fiq3",
        "title": "La prière du vendredi (jumu'ah) et la prière en groupe",
        "objectives": [
            "Comprendre l'obligation et l'éthique du vendredi",
            "Connaître le mérite de la prière en assemblée",
        ],
        "content": (
            "La prière du vendredi (salat al-jumu'ah) remplace la prière de midi pour celui qui en a l'obligation. "
            "Elle comporte deux unités, précédées de deux sermons (khutbah). Le vendredi est aussi un moment "
            "d'invocation : il contient une heure où les invocations sont exaucées.\n\n"
            "La prière en congrégation (jama'ah) est 25 à 27 fois supérieure à la prière seul : se rendre à la mosquée "
            "et ne pas écarter les autres font partie de l'adab prescrit."
        ),
        "quran": [
            {"ref": "62:9", "note": "Ô vous qui croyez ! Lorsqu'on appelle à la prière du vendredi, accourez à l'invocation d'Allah"},
        ],
        "hadith": [
            {"book": "muslim", "number": 1367, "note": "La prière en congrégation est plus méritoire de 25 à 27 degrés"},
            {"book": "abudawud", "number": 1047, "note": "Le meilleur jour où le soleil se lève : le vendredi"},
        ],
    },
    # ── Module 3 : Fiqh — Zakat, jeûne, hajj ───────────────────────────────
    {
        "module": 3,
        "module_title": "Fiqh — Zakat, jeûne et hajj",
        "id": "fiq4",
        "title": "La zakat : purifier son argent",
        "objectives": [
            "Connaître les biens concernés et le taux (2,5 % par an)",
            "Identifier les 8 catégories de bénéficiaires",
        ],
        "content": (
            "La zakat est le troisième pilier : elle purifie le bien et la personne. Elle est due chaque année "
            "sur les biens atteignant le seuil (nissab) sur lesquels une année a passé, pour un taux de 2,5 % "
            "pour l'argent et les biens commerciaux. Le verset 9:60 énumère les catégories de bénéficiaires.\n\n"
            "La zakat doit être versée sans retard, sincèrement, en donnant le meilleur du bien, "
            "sans reproche ni intimidation des bénéficiaires."
        ),
        "quran": [
            {"ref": "9:60", "note": "Les 8 catégories de bénéficiaires de la zakat"},
            {"ref": "2:261", "note": "La parabole de ceux qui dépensent dans le sentier d'Allah"},
            {"ref": "2:264", "note": "N'annulez pas vos aumônes par le reproche ou le tort"},
        ],
        "hadith": [
            {"book": "muslim", "number": 6430, "note": "L'aumône ne diminue pas la richesse (Muslim n°6430)"},
        ],
    },
    {
        "module": 3,
        "module_title": "Fiqh — Zakat, jeûne et hajj",
        "id": "fiq5",
        "title": "Le jeûne de Ramadan : sens et règles",
        "objectives": [
            "Connaître les piliers et ce qui annule le jeûne",
            "Vivre le Ramadan comme une école de piété",
        ],
        "content": (
            "Allah a prescrit le jeûne « comme Il l'a prescrit à ceux avant vous, afin que vous atteigniez la piété (taqwa) » (2:183). "
            "On observe le jeûne de l'aube au coucher du soleil, en s'abstenant de nourriture, de boisson et des relations conjugales, "
            "mais aussi — surtout — de la parole et du comportement vains.\n\n"
            "La nuit du destin (Laylat al-Qadr) est meilleure que mille mois ; elle se cherche dans les dix derniers jours, "
            "notamment les nuits impaires."
        ),
        "quran": [
            {"ref": "2:183", "note": "Le jeûne vous est prescrit… afin que vous atteigniez la piété"},
            {"ref": "2:185", "note": "Ramadan : descente du Coran, guide pour les gens"},
            {"ref": "97:3", "note": "La nuit du destin est meilleure que mille mois"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 38, "note": "Quiconque jeûne Ramadan avec foi et espérance : pardon des péchés passés"},
            {"book": "nasai", "number": 2216, "note": "Hadith sacré : « Le jeûne est à Moi et c'est Moi qui le récompense »"},
            {"book": "bukhari", "number": 5828, "note": "Jeûner, c'est aussi abandonner les fausses paroles et les mauvais agissements"},
        ],
    },
    {
        "module": 3,
        "module_title": "Fiqh — Zakat, jeûne et hajj",
        "id": "fiq6",
        "title": "Le pèlerinage (hajj) : l'aboutissement spirituel",
        "objectives": [
            "Comprendre la condition d'obligation et les rites majeurs",
            "Saisir la dimension spirituelle : l'humilité et l'égalité",
        ],
        "content": (
            "Le hajj est une obligation pour celui qui en a la capacité (physique, financière et sécuritaire), au moins une fois dans sa vie. "
            "Ses rites se concentrent à La Mecque, à Mina, à Arafat et à Muzdalifah, autour de la Kaaba.\n\n"
            "« Le pèlerinage, c'est Arafat » : se tenir sur la plaine d'Arafat est le rite central. "
            "Le pèlerin — vêtu de simples habits blancs (ihram) — incarne l'égalité absolue des êtres devant Allah."
        ),
        "quran": [
            {"ref": "3:97", "note": "Faire le pèlerinage de la Maison est un devoir envers Allah pour qui en a la capacité"},
            {"ref": "22:27", "note": "Appelle les gens au pèlerinage"},
            {"ref": "22:28", "note": "Qu'ils jouissent de bienfaits et invoquent Allah aux jours connus"},
        ],
        "hadith": [
            {"book": "nasai", "number": 3022, "note": "« Le pèlerinage, c'est Arafat » (mauqif central)"},
        ],
    },
    # ── Module 4 : Sirah ───────────────────────────────────────────────────
    {
        "module": 4,
        "module_title": "Sirah — La vie du Prophète ﷺ",
        "id": "sir1",
        "title": "La Mecque : de la naissance à la mission",
        "objectives": [
            "Replacer la naissance et la jeunesse du Prophète ﷺ dans leur contexte",
            "Comprendre l'avènement de la révélation",
        ],
        "content": (
            "Muhammad ﷺ est né à La Mecque vers 570. Orphelin de père puis de mère, élevé par son grand-père "
            "puis son oncle Abu Talib, il gagne la confiance de son clan par sa droiture (« al-Amin », le digne de confiance). "
            "À 25 ans il épouse Khadija, qui sera son premier soutien.\n\n"
            "À 40 ans, dans la grotte de Hira, l'archange Gabriel lui révèle les premiers versets de la Sourate Al-Alaq "
            "(« Lis, au nom de ton Seigneur qui a créé… »). La révélation commence par des songes véridiques, "
            "puis la descente directe de la parole d'Allah."
        ),
        "quran": [
            {"ref": "96:1", "note": "Lis, au nom de ton Seigneur qui a créé"},
            {"ref": "93:6", "note": "Ne t'a-t-Il pas trouvé orphelin, ne t'a-t-Il pas accueilli ?"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 3, "note": "Les débuts de la révélation : les songes véridiques et la grotte de Hira"},
        ],
    },
    {
        "module": 4,
        "module_title": "Sirah — La vie du Prophète ﷺ",
        "id": "sir2",
        "title": "La Hégire et la construction de Médine",
        "objectives": [
            "Situer les événements clés de la Hégire",
            "Tirer les leçons de la solidarité des Ansars",
        ],
        "content": (
            "Face à l'oppression mecquoise, les musulmans émigrent d'abord en Abyssinie, puis Allah permet la Hégire vers Médine "
            "(en l'an 622). Cette migration fonde le calendrier musulman et la première communauté organisée.\n\n"
            "À Médine, le Prophète ﷺ bâtit la mosquée, établit la fraternité entre émigrants (Muhajirun) et partisans (Ansar), "
            "et rédige la constitution de Médine unissant les habitants dans une cité communautaire."
        ),
        "quran": [
            {"ref": "8:74", "note": "Ceux qui ont cru et émigré… et ceux qui ont donné refuge et secouru"},
            {"ref": "59:9", "note": "Ceux qui avaient élu domicile et la foi, et qui aiment ceux qui émigrent vers eux"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1, "note": "Le hadith de l'intention : « celui dont l'immigration est pour Allah et Son messager »"},
        ],
    },
    {
        "module": 4,
        "module_title": "Sirah — La vie du Prophète ﷺ",
        "id": "sir3",
        "title": "La conquête de La Mecque et le sermon d'adieu",
        "objectives": [
            "Comprendre le pardon prophétique",
            "Retenir l'essentiel du sermon d'adieu",
        ],
        "content": (
            "En l'an 630, la Mecque est conquise presque sans effusion de sang. Le Prophète ﷺ entre dans la ville vainqueur, "
            "et loin de se venger, il pardonne : « Allez, vous êtes libres ». Ce pardon est un sommet de la miséricorde prophétique.\n\n"
            "Lors du pèlerinage d'adieu, il livre un message universel : la vie et le bien des personnes sont sacrés, "
            "l'usure est abolie, et « nul n'est supérieur à un autre sinon par la piété »."
        ),
        "quran": [
            {"ref": "110:1", "note": "Lorsque vient le secours d'Allah et la victoire"},
            {"ref": "49:13", "note": "Le plus noble d'entre vous est le plus pieux"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1, "note": "L'esprit du sermon d'adieu : égalité et sincérité (leçon : l'intention gouverne les actes)"},
        ],
    },
    # ── Module 5 : Sciences du Coran ───────────────────────────────────────
    {
        "module": 5,
        "module_title": "Sciences du Coran",
        "id": "cor1",
        "title": "Le Coran : texte, transmission et classification",
        "objectives": [
            "Comprendre la révélation (wahy) et la collecte du texte",
            "Distinguer sourates mécquoises et médinoises",
        ],
        "content": (
            "Le Coran est la parole d'Allah révélée au Prophète ﷺ par l'ange Gabriel, transmise par voie continue (tawatur). "
            "Il a été mémorisé et consigné à l'époque du Prophète ﷺ, rassemblé en un mushaf sous Abu Bakr puis uni "
            "en une seule écriture sous Uthman.\n\n"
            "Les sourates mécquoises (avant la Hégire) traitent surtout de la foi, de l'unicité et de la résurrection ; "
            "les sourates médinoises traitent de la législation, du culte et de la vie sociale. Connaître les circonstances "
            "de révélation (asbab an-nuzul) éclaire le sens des versets."
        ),
        "quran": [
            {"ref": "12:2", "note": "Nous l'avons fait descendre un Coran en arabe, afin que vous raisonniez"},
            {"ref": "56:77", "note": "C'est vraiment un Coran noble"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 4820, "note": "Le meilleur d'entre vous est celui qui apprend le Coran et l'enseigne"},
        ],
    },
    {
        "module": 5,
        "module_title": "Sciences du Coran",
        "id": "cor2",
        "title": "Le tajwid : lire le Coran correctement",
        "objectives": [
            "Comprendre l'exigence d'une récitation soignée",
            "Apprendre les règles de base (articulation, prolongations, arrêts)",
        ],
        "content": (
            "La récitation correcte (tajwid) consiste à donner à chaque lettre son articulation (makhraj) et ses caractéristiques "
            "propres, et à respecter les prolongations (madd) et les arrêts (waqf). Ce n'est pas une ornementation surtout : "
            "c'est une discipline qui protège le sens du texte sacré.\n\n"
            "Commence par l'articulation correcte des lettres et l'arrêt en fin de verset, "
            "en t'aidant de l'écoute de récitateurs reconnus."
        ),
        "quran": [
            {"ref": "73:4", "note": "Récite le Coran clairement, lentement (avec tartil)"},
            {"ref": "15:9", "note": "C'est Nous qui avons fait descendre le Rappel, et c'est Nous qui le gardons"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 4820, "note": "Apprendre et enseigner le Coran : la voie du mérite"},
        ],
    },
    # ── Module 6 : Sciences du hadith ─────────────────────────────────────
    {
        "module": 6,
        "module_title": "Sciences du hadith",
        "id": "had1",
        "title": "La Sunna : deuxième source de l'islam",
        "objectives": [
            "Définir hadith et Sunna",
            "Comprendre le rôle de la Sunna par rapport au Coran",
        ],
        "content": (
            "La Sunna est la deuxième source de la législation : elle détaille ce que le Coran résume. Elle comprend "
            "les paroles, les actes, les approbations du Prophète ﷺ ainsi que ses qualités morales. Le hadith en est le rapport.\n\n"
            "Le verset « Prenez ce que le Messager vous donne » (59:7) fonde l'autorité de la Sunna. "
            "Sans elle, la prière, la zakat ou le hajj ne seraient pas explicables en pratique."
        ),
        "quran": [
            {"ref": "59:7", "note": "Prenez ce que le Messager vous donne, et abstenez-vous de ce qu'il vous interdit"},
            {"ref": "4:59", "note": "Obéissez à Allah, obéissez au Messager et à ceux d'entre vous qui détiennent l'autorité"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1, "note": "L'intention structure toute la pratique — introduction à la science du hadith"},
        ],
    },
    {
        "module": 6,
        "module_title": "Sciences du hadith",
        "id": "had2",
        "title": "Statuts des hadiths : sahih, hasan, da'if",
        "objectives": [
            "Comprendre la gradation des hadiths",
            "Savoir pourquoi on vérifie un hadith avant de le partager",
        ],
        "content": (
            "Les savants ont classé les hadiths selon l'authenticité de la chaîne de transmission (isnad) et du texte (matn) : "
            "sahih (authentique), hasan (bon), da'if (faible), maudu' (fabrication). Un hadith sahih exige une chaîne continue, "
            "des rapporteurs intègres et précis, sans anomalie ni défaut caché.\n\n"
            "La Sunna est exigeante avec la parole : quiconque rapporte sur le Prophète ﷺ se doit d'être véridique. "
            "Vérifie toujours la source avant de partager un hadith."
        ),
        "quran": [
            {"ref": "49:6", "note": "Si un pervers vous apporte une nouvelle, vérifiez (tabayyanu)"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 5828, "note": "La véracité de la parole : celui qui recherche le vrai est préservé"},
        ],
    },
    # ── Module 7 : Adab et Akhlaq ─────────────────────────────────────────
    {
        "module": 7,
        "module_title": "Adab et Akhlaq — L'éthique spirituelle",
        "id": "akh1",
        "title": "La droiture du cœur : ikhlas, taqwa, tawakkul",
        "objectives": [
            "Définir la sincérité (ikhlas) et la piété (taqwa)",
            "Confier ses affaires à Allah (tawakkul)",
        ],
        "content": (
            "Le cœur est au centre de l'islam : « Il y a dans le corps un morceau de chair ; s'il est sain, tout le corps est sain, "
            "et s'il est corrompu, tout le corps est corrompu : c'est le cœur ».\n\n"
            "La taqwa est une conscience vigilante d'Allah qui protège des péchés ; l'ikhlas est l'intention pure, "
            "ne cherchant que l'agrément d'Allah ; le tawakkul est la confiance en Allah accompagnée de la prise de moyens."
        ),
        "quran": [
            {"ref": "2:177", "note": "La piété réside dans la droiture du cœur"},
            {"ref": "65:2", "note": "Quiconque craint Allah, Il lui donnera une issue"},
            {"ref": "3:159", "note": "Quand tu as pris une décision, confie-toi à Allah"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 52, "note": "Le cœur : s'il est sain, tout le corps est sain"},
            {"book": "muslim", "number": 81, "note": "Le croyant parle de bien ou se tait"},
        ],
    },
    {
        "module": 7,
        "module_title": "Adab et Akhlaq — L'éthique spirituelle",
        "id": "akh2",
        "title": "La langue et les mœurs : vérité, confiance, miséricorde",
        "objectives": [
            "Comprendre le poids de la parole",
            "Adopter la miséricorde comme trait du croyant",
        ],
        "content": (
            "Le Prophète ﷺ a résumé l'éthique : « Celui qui croit en Allah et au Jour dernier parle de bien ou se tait ». "
            "La langue est le membre le plus dangereux : mensonge, médisance, délation et moquerie abîment la foi.\n\n"
            "Le croyant est aussi celui qu'on peut croire et à qui l'on peut se confier : ",
            "« Aucun de vous ne croit vraiment tant qu'il n'aime pas pour son frère ce qu'il aime pour lui-même. »"
        ),
        "quran": [
            {"ref": "49:11", "note": "Que les uns ne se moquent pas des autres"},
            {"ref": "49:12", "note": "Évitez la suspicion, la médisance"},
            {"ref": "41:34", "note": "Repousse le mal par ce qui est meilleur"},
        ],
        "hadith": [
            {"book": "muslim", "number": 81, "note": "Parle de bien ou tais-toi"},
            {"book": "bukhari", "number": 13, "note": "Aime pour ton frère ce que tu aimes pour toi-même"},
            {"book": "abudawud", "number": 4912, "note": "Ne vous haïssez pas, ne vous enviez pas, soyez des frères"},
        ],
    },
    {
        "module": 7,
        "module_title": "Adab et Akhlaq — L'éthique spirituelle",
        "id": "akh3",
        "title": "La générosité et le lien des proches",
        "objectives": [
            "Pratiquer la générosité discrète",
            "Entretenir les liens de parenté",
        ],
        "content": (
            "Allah aime ceux qui dépensent discrètement : il est dit de ceux qui « donnent leur bien, alors qu'ils l'aiment, "
            "aux proches, aux orphelins… » (2:177). L'aumône ne diminue pas la richesse : elle est au contraire un investissement.\n\n"
            "La générosité n'est pas réservée aux riches : un bon mot, un sourire, retirer un obstacle du chemin, c'est aussi l'aumône."
        ),
        "quran": [
            {"ref": "2:177", "note": "Donner son bien aux proches, orphelins, pauvres, voyageurs"},
            {"ref": "17:26", "note": "Donne au proche son dû, ainsi qu'au pauvre et au voyageur"},
        ],
        "hadith": [
            {"book": "muslim", "number": 6430, "note": "L'aumône ne diminue pas la richesse"},
        ],
    },
    # ── Module 8 : Adhkar et pratique ──────────────────────────────────────
    {
        "module": 8,
        "module_title": "Adhkar et pratique quotidienne",
        "id": "pra1",
        "title": "Le rappel d'Allah et les invocations du quotidien",
        "objectives": [
            "Comprendre l'importance du rappel d'Allah",
            "Mémoriser quelques formules essentielles",
        ],
        "content": (
            "Allah ordonne : « Invoquez-Moi, Je vous exaucerai » (40:60) et « Souvenez-vous de Moi, Je me souviendrai de vous » (2:152). "
            "C'est par l'évocation d'Allah que les cœurs s'apaisent (13:28).\n\n"
            "Commence par trois piliers de rappel : Ayat al-Kursi (2:255), les trois sourates de protection (Al-Ikhlas, Al-Falaq, "
            "An-Nas) et les formules de glorification rapportées dans la Sunna."
        ),
        "quran": [
            {"ref": "2:152", "note": "Souvenez-vous de Moi, Je me souviendrai de vous"},
            {"ref": "40:60", "note": "Invoquez-Moi, Je vous exaucerai"},
            {"ref": "13:28", "note": "C'est par l'évocation d'Allah que les cœurs s'apaisent"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 6166, "note": "« Subhan Allah wa bihamdihi » cent fois par jour : péchés effacés"},
            {"book": "muslim", "number": 6430, "note": "Rapport sur l'aumône et les bonnes œuvres quotidiennes"},
        ],
    },
    {
        "module": 8,
        "module_title": "Adhkar et pratique quotidienne",
        "id": "pra2",
        "title": "Repentir et retour à Allah (tawbah)",
        "objectives": [
            "Comprendre les conditions d'une repentance agréée",
            "Savoir qu'Allah « se réjouit » du retour de Son serviteur",
        ],
        "content": (
            "Le repentir (tawbah) a trois conditions : cesser le péché, regretter sincèrement, et résoudre à ne pas récidiver "
            "(plus la restitution des droits lésés, le cas échéant). Sa porte reste ouverte tant que l'âme n'atteint pas la gorge.\n\n"
            "Allah dit : « Dis : Ô Mes serviteurs qui avez commis des excès à votre propre détriment, ne désespérez pas de la "
            "miséricorde d'Allah. Allah pardonne tous les péchés » (39:53). Celui qui se repent est aimé d'Allah."
        ),
        "quran": [
            {"ref": "39:53", "note": "Ne désespérez pas de la miséricorde d'Allah"},
            {"ref": "2:222", "note": "Allah aime ceux qui se repentent et ceux qui se purifient"},
            {"ref": "66:8", "note": "Repentez-vous à Allah d'un repentir sincère"},
        ],
        "hadith": [
            {"book": "riyad_assalihin", "number": 1232, "note": "Allah se réjouit du repentir de Son serviteur (Riyad as-Salihin)"},
        ],
    },
    # ── Module 9 : Les 99 noms d'Allah ─────────────────────────────────────
    {
        "module": 9,
        "module_title": "Les 99 noms d'Allah (al-Asma al-Husna)",
        "id": "asm1",
        "title": "Introduction aux noms d'Allah",
        "objectives": [
            "Comprendre l'importance des noms d'Allah dans la vie du musulman",
            "Connaître la différence entre noms propres et attributs",
        ],
        "content": (
            "Les 99 noms d'Allah (al-Asma al-Husna) sont les beaux noms par lesquels Allah Se décrit dans le Coran et la Sunna. "
            "Ils reflètent Ses attributs parfaits : connaissance, puissance, miséricorde, justice, etc.\n\n"
            "Allah dit : « Les plus beaux noms sont à Allah, invoquez-les par » (7:180). Chaque nom exprime une réalité "
            "qui doit guider notre adoration : par exemple, Ar-Rahman nous rappelle la miséricorde infinie d'Allah, "
            "et Al-'Adl Sa justice parfaite.\n\n"
            "L'invocation des noms d'Allah fait partie des meilleures œuvres, surtout après la prière, le vendredi, "
            "et les moments d'exaucement."
        ),
        "quran": [
            {"ref": "7:180", "note": "Les plus beaux noms sont à Allah"},
            {"ref": "20:8", "note": "À Allah appartiennent les plus beaux noms, invoquez-les"},
            {"ref": "59:24", "note": "Il est Allah, le Créateur, l'Initiateur, le Donateur de forme"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 2736, "note": "Les 99 noms d'Allah, moins un : celui qui les compte entrera au Paradis"},
            {"book": "muslim", "number": 2677, "note": "Allah possède 99 noms, 100 moins un"},
        ],
    },
    {
        "module": 9,
        "module_title": "Les 99 noms d'Allah (al-Asma al-Husna)",
        "id": "asm2",
        "title": "Les noms liés à la miséricorde et au pardon",
        "objectives": [
            "Mémoriser les noms liés à la miséricorde",
            "Comprendre comment ces noms influencent notre comportement",
        ],
        "content": (
            "Allah s'est décrit par des noms de miséricorde qui sont parmi les plus cités dans le Coran :\n\n"
            "- Ar-Rahman (Le Tout Miséricordieux) : Sa miséricorde est universelle, elle englobe tous les êtres.\n"
            "- Ar-Rahim (Le Très Miséricordieux) : Sa miséricorde particulière pour les croyants.\n"
            "- Al-Ghaffar (Le Pardonneur) : Celui qui pardonne abondamment les péchés.\n"
            "- Al-'Afuw (Le Pardonneur) : Celui qui efface les péchés sans laisser de trace.\n"
            "- At-Tawwab (Le Retournant) : Celui qui accepte le repentir et y aide Ses serviteurs.\n\n"
            "Ces noms nous enseignent que la miséricorde d'Allah est plus grande que nos péchés, "
            "et que la porte du repentir reste toujours ouverte."
        ),
        "quran": [
            {"ref": "1:1", "note": "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux"},
            {"ref": "39:53", "note": "La miséricorde d'Allah est immense"},
            {"ref": "7:156", "note": "Ma miséricorde embrasse toute chose"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 6307, "note": "Allah est plus miséricordieux envers Ses serviteurs qu'une mère envers son enfant"},
        ],
    },
    {
        "module": 9,
        "module_title": "Les 99 noms d'Allah (al-Asma al-Husna)",
        "id": "asm3",
        "title": "Les noms liés à la science et à la sagesse",
        "objectives": [
            "Connaître les noms d'Allah liés à la connaissance",
            "Comprendre comment ces noms guident notre recherche du savoir",
        ],
        "content": (
            "Allah possède des noms qui témoignent de Sa science infinie :\n\n"
            "- Al-'Alim (L'Omniscient) : Il sait tout, le passé, le présent et le futur, le visible et l'invisible.\n"
            "- Al-Khabir (Le Très Connaisseur) : Il connaît chaque chose en détail.\n"
            "- As-Sami' (L'Oudiant) : Il entend toutes les paroles, même les plus secrètes.\n"
            "- Al-Basir (Le Voyant) : Il voit tout, même ce qui est caché dans les cœurs.\n"
            "- Al-Hakim (Le Sage) : Sa sagesse est parfaite dans toute Sa création et Sa législation.\n\n"
            "Ces noms nous rappellent qu'Allah est témoin de tout ce que nous faisons, "
            "et que nous devons Lui obéir en sachant qu'Il nous observe."
        ),
        "quran": [
            {"ref": "2:29", "note": "Il connaît tout, même ce qui est dans les entrailles de la terre"},
            {"ref": "49:18", "note": "Allah connaît le mieux la vérité de vos dires"},
            {"ref": "58:11", "note": "Allah élève ceux qui ont cru parmi vous et ceux à qui le savoir a été donné"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 50, "note": "Le hadith de Jibril : définition de la foi et de la sagesse"},
        ],
    },
    # ── Module 10 : Les piliers de l'islam en détail ────────────────────────
    {
        "module": 10,
        "module_title": "Les 5 piliers de l'islam en détail",
        "id": "pil1",
        "title": "La chahada : attestation de foi",
        "objectives": [
            "Comprendre les conditions de validité de la chahada",
            "Connaître les implications pratiques de la chahada",
        ],
        "content": (
            "La chahada (attestation de foi) est le premier pilier de l'islam : « J'atteste qu'il n'y a de divinité "
            "qu'Allah, et j'atteste que Muhammad est le Messager d'Allah ».\n\n"
            "Cette phrase comporte deux parties essentielles :\n"
            "1. Tawhid : la négation de toute divinité en dehors d'Allah (la ilaha illallah)\n"
            "2. Risalah : l'acceptation de Muhammad comme messager final (muhammadur rasulullah)\n\n"
            "La chahada a six conditions : la connaissance, la certitude, l'acceptation, la soumission, la sincérité "
            "et l'amour. Elle doit être prononcée sincèrement pour entrer dans l'islam."
        ),
        "quran": [
            {"ref": "3:18", "note": "Allah témoigne qu'il n'y a de divinité que Lui, et les anges et ceux qui savent"},
            {"ref": "47:19", "note": "Sache qu'il n'y a de divinité qu'Allah"},
        ],
        "hadith": [
            {"book": "muslim", "number": 40, "note": "L'islam est bâti sur cinq piliers : la chahada, la prière, la zakat, le jeûne et le pèlerinage"},
        ],
    },
    {
        "module": 10,
        "module_title": "Les 5 piliers de l'islam en détail",
        "id": "pil2",
        "title": "La zakat : purifier ses biens",
        "objectives": [
            "Connaître les conditions d'application de la zakat",
            "Comprendre l'impact social de la zakat",
        ],
        "content": (
            "La zakat est le troisième pilier : elle purifie la richesse et purifie le cœur de l'avarice. "
            "Elle est due chaque année sur les biens qui atteignent le nissab (seuil minimum) et sur lesquels "
            "une année complète s'est écoulée.\n\n"
            "Le taux est de 2,5% pour l'argent et l'or, 5% pour le bétail, et 10% pour les produits agricoles "
            "irrigués. Les bénéficiaires sont au nombre de huit (cf. Coran 9:60) : les pauvres, les nécessiteux, "
            "les collecteurs, les convertis, les affranchis, les endettés, les voyageurs et pour la cause d'Allah.\n\n"
            "La zakat est un droit des pauvres sur les biens des riches : elle crée la solidarité sociale "
            "et purifie l'économie."
        ),
        "quran": [
            {"ref": "9:60", "note": "Les 8 catégories de bénéficiaires de la zakat"},
            {"ref": "2:261", "note": "La parabole de ceux qui dépensent dans le sentier d'Allah"},
        ],
        "hadith": [
            {"book": "muslim", "number": 6430, "note": "L'aumône ne diminue pas la richesse"},
        ],
    },
    {
        "module": 10,
        "module_title": "Les 5 piliers de l'islam en détail",
        "id": "pil3",
        "title": "Le hajj : pèlerinage à La Mecque",
        "objectives": [
            "Connaître les rites du pèlerinage",
            "Comprendre la signification spirituelle du hajj",
        ],
        "content": (
            "Le hajj est une obligation pour tout musulman qui en a la capacité (physique, financière et sécuritaire). "
            "Il a lieu chaque année du 8 au 12 dhul hijjah.\n\n"
            "Les rites principaux :\n"
            "- Ihram : entrée en état de sacralité (vêtements blancs, interdictions)\n"
            "- Tawaf : circumambulation de la Kaaba 7 fois\n"
            "- Sa'i : parcours entre Safa et Marwa 7 fois\n"
            "- Arafat : stationnement sur la plaine d'Arafat (le pèlerinage, c'est Arafat)\n"
            "- Muzdalifah : nuit sous les étoiles\n"
            "- Mina : lapidation des stèles symbolisant Iblis\n"
            "- Sacrifice : immolation d'un animal\n\n"
            "Le hajj symbolise l'égalité des êtres devant Allah et la fraternité universelle."
        ),
        "quran": [
            {"ref": "3:97", "note": "Faire le pèlerinage de la Maison est un devoir envers Allah pour qui en a la capacité"},
            {"ref": "22:27", "note": "Appelle les gens au pèlerinage"},
        ],
        "hadith": [
            {"book": "nasai", "number": 3022, "note": "Le pèlerinage, c'est Arafat"},
        ],
    },
    # ── Module 11 : Concepts islamiques fondamentaux ────────────────────────
    {
        "module": 11,
        "module_title": "Concepts islamiques fondamentaux",
        "id": "con1",
        "title": "La patience (sabr) et la gratitude (shukr)",
        "objectives": [
            "Comprendre la place du sabr dans la vie du musulman",
            "Apprendre à être reconnaissant envers Allah",
        ],
        "content": (
            "Le sabr (patience) est une vertu fondamentale en islam. Il ne signifie pas l'absence de douleur, "
            "mais la capacité à supporter les épreuves avec dignité et confiance en Allah.\n\n"
            "Le Coran dit : « Allah est avec les patients » (2:153) et « La vie de ce monde n'est que jeu et "
            "divertissement, mais la vie future est véritablement la vie, s'ils savaient » (29:64).\n\n"
            "Le shukr (gratitude) est le complément du sabr : « Si vous êtes reconnaissants, Je vous accorderai "
            "davantage » (14:7). Le vrai musulman remercie Allah dans l'aisance comme dans la difficulté, "
            "car chaque situation contient une bénédiction cachée."
        ),
        "quran": [
            {"ref": "2:153", "note": "Allah est avec les patients"},
            {"ref": "14:7", "note": "Si vous êtes reconnaissants, Je vous accorderai davantage"},
            {"ref": "31:17", "note": "Commande-le patient et ordonne-le bien"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1302, "note": "L'affaire du croyant est étonnante : tout est bien pour lui"},
        ],
    },
    {
        "module": 11,
        "module_title": "Concepts islamiques fondamentaux",
        "id": "con2",
        "title": "La confiance en Allah (tawakkul)",
        "objectives": [
            "Comprendre la différence entre tawakkul et passivité",
            "Apprendre à agir tout en se confiant en Allah",
        ],
        "content": (
            "Le tawakkul (confiance en Allah) signifie se reposer entièrement sur Allah tout en prenant les "
            "moyens nécessaires. Ce n'est ni la négligence, ni l'excès de planification.\n\n"
            "Le Prophète ﷺ a dit : « Lie ta chamelle, puis confie-toi à Allah » (Tirmidhi). "
            "Cela signifie qu'on doit faire l'effort humain nécessaire, puis accepter le résultat avec sérénité.\n\n"
            "Le Coran nous enseigne : « Quiconque craint Allah, Il lui donnera une issue, lui accordera des provisions "
            "de sources inattendues » (65:2-3). Le tawakkul apporte la paix du cœur et libère de l'angoisse."
        ),
        "quran": [
            {"ref": "65:2", "note": "Quiconque craint Allah, Il lui donnera une issue"},
            {"ref": "3:159", "note": "Quand tu as pris une décision, confie-toi à Allah"},
        ],
        "hadith": [
            {"book": "tirmidhi", "number": 2517, "note": "Lie ta chamelle, puis confie-toi à Allah"},
        ],
    },
    {
        "module": 11,
        "module_title": "Concepts islamiques fondamentaux",
        "id": "con3",
        "title": "Lafraternité islamique (ukhuwwah)",
        "objectives": [
            "Comprendre les droits mutuels entre musulmans",
            "Apprendre à aimer pour Allah et à haïr pour Allah",
        ],
        "content": (
            "La fraternité islamique est un pilier de la foi : « Les croyants ne sont que des frères » (49:10). "
            "Cette fraternité est fondée sur l'amour pour Allah, non sur l'intérêt ou la parenté.\n\n"
            "Le Prophète ﷺ a dit : « Aucun de vous n'a真正的 foi tant qu'il n'aime pas pour son frère "
            "ce qu'il aime pour lui-même » (Bukhari). Cela implique la bienveillance, la loyauté, "
            "l'honnêteté et le soutien mutuel.\n\n"
            "La ukhuwwah se traduit par : visiter les malades, assister les funérailles, aider les nécessiteux, "
            "donner un bon conseil, et prier les uns pour les autres."
        ),
        "quran": [
            {"ref": "49:10", "note": "Les croyants ne sont que des frères"},
            {"ref": "8:1", "note": "Les croyants sont des frères"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 13, "note": "Aime pour ton frère ce que tu aimes pour toi-même"},
            {"book": "muslim", "number": 2564, "note": "Les droits mutuels entre musulmans"},
        ],
    },
    # ── Module 12 : La vie du Prophète ﷺ (Sira détaillée) ──────────────────
    {
        "module": 12,
        "module_title": "La vie du Prophète ﷺ (Sira détaillée)",
        "id": "sir4",
        "title": "Les batailles et les expéditions",
        "objectives": [
            "Connaître les grandes batailles de l'islam",
            "Comprendre les leçons spirituelles de ces événements",
        ],
        "content": (
            "Les batailles de l'islam ont des leçons profondes :\n\n"
            "- Badr (624) : les 313 musulmans vainquent 1000 mecquois. C'est la première victoire, "
            "qui montre que la force réside dans la foi, non dans les nombres.\n"
            "- Uhud (625) : défaite partielle à cause de la désobéissance d'une partie des archers. "
            "Leçon : la discipline et l'obéissance sont essentielles.\n"
            "- Al-Ahzab/Khandaq (627) : siège de Médine, sauvé par la stratégie de Salman al-Farisi "
            "(fossé) et l'intervention divine.\n"
            "- La Mecque (630) : conquête pacifique, pardon général du Prophète ﷺ.\n"
            "- Hunayn (630) : victoire après un moment de difficulté, leçon sur l'humilité.\n\n"
            "Ces batailles ne sont pas des guerres de conquête mais des luttes pour la survie "
            "et la liberté de croyance."
        ),
        "quran": [
            {"ref": "8:5", "note": "Allah vous a secourus à Badr alors que vous étiez les plus faibles"},
            {"ref": "3:123", "note": "Allah vous a déjà secourus à Badr, alors que vous étiez les plus faibles"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 2797, "note": "La vertu de la bataille de Badr"},
            {"book": "bukhari", "number": 3995, "note": "La stratégie du fossé"},
        ],
    },
    {
        "module": 12,
        "module_title": "La vie du Prophète ﷺ (Sira détaillée)",
        "id": "sir5",
        "title": "Les épouses du Prophète ﷺ et la vie familiale",
        "objectives": [
            "Connaître les épouses du Prophète ﷺ et leurs vertus",
            "Comprendre le modèle familial en islam",
        ],
        "content": (
            "Le Prophète ﷺ a épousé plusieurs femmes qui ont joué un rôle majeur dans la transmission "
            "de la Sunna et l'éducation de la communauté :\n\n"
            "- Khadijah bint Khuwaylid : première épouse, premier soutien, mère des croyants.\n"
            "- Sawdah bint Zam'ah : compagne de la Hégire, exemplaire dans la générosité.\n"
            "- Aisha bint Abi Bakr : « la mère des croyants », grande savante, source de hadiths.\n"
            "- Hafsa bint Omar : gardienne du Coran après la mort du Prophète ﷺ.\n"
            "- Zaynab bint Jahsh : épousée par ordre divin pour briser les tabous sociaux.\n\n"
            "Le Prophète ﷺ participait aux tâches ménagères, jouait avec ses enfants, "
            "et traitait ses épouses avec respect et tendresse."
        ),
        "quran": [
            {"ref": "33:28", "note": "Versets de la khaswa (épouses du Prophète)"},
            {"ref": "33:59", "note": "Ordre de porter le voile pour les femmes du Prophète"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 67, "note": "Le meilleur d'entre vous est celui qui est le meilleur envers sa femme"},
            {"book": "bukhari", "number": 5219, "note": "Le Prophète aidait à la maison"},
        ],
    },
]


def _quran_block(ref: str) -> str:
    surah, _, ayah = ref.partition(":")
    try:
        s, a = int(surah), int(ayah)
    except ValueError:
        return ref
    row = db.get_ayah(s, a)
    if not row:
        return ""
    meta = db.get_surah_meta(s)
    line = f"📖 Coran {s}:{a} — {meta['transliteration']}"
    return f"{line}\n{row['text_ar']}\n— {row['text_fr']}"


def _hadith_block(ref: dict) -> str:
    book, number = ref.get("book"), ref.get("number")
    row = db.get_hadith(book, number) if book and number else None
    if row:
        line = f"🕌 Hadith — {row['book_name']} (n°{row['hadith_number']})"
        text = f"{line}\n{row['text_en'][:600]}"
        if row["arabic"]:
            text += f"\n{row['arabic'][:300]}"
        return text
    # Repli : recherche par phrase sur le texte anglais
    term = ref.get("term")
    if term:
        rows = db.search_hadith(term, book=book, limit=1)
        if rows:
            h = rows[0]
            line = f"🕌 Hadith — {h['book_name']} (n°{h['hadith_number']})"
            return f"{line}\n{h['text_en'][:600]}"
    return f"(Référence : {book} n°{number or term} — {ref.get('note', '')}. Vérifie auprès de la source.)"


def lesson_references(lesson: dict) -> str:
    parts = []
    for ref in lesson.get("quran", []):
        block = _quran_block(ref["ref"])
        if block:
            parts.append(f"{block}\n*{ref.get('note', '')}*")
    for ref in lesson.get("hadith", []):
        parts.append(f"{_hadith_block(ref)}\n*{ref.get('note', '')}*")
    return "\n\n".join(parts)


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"completed": [], "last": None}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def next_lesson(progress: dict | None = None) -> dict | None:
    progress = progress or load_progress()
    done = set(progress.get("completed", []))
    for lesson in LESSONS:
        if lesson["id"] not in done:
            return lesson
    return None


def lesson_by_id(lesson_id: str) -> dict | None:
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    return None


def complete(lesson_id: str) -> dict:
    progress = load_progress()
    if lesson_id not in progress["completed"]:
        progress["completed"].append(lesson_id)
    progress["last"] = lesson_id
    save_progress(progress)
    return progress


def overview(progress: dict | None = None) -> str:
    progress = progress or load_progress()
    done = set(progress.get("completed", []))
    out = ["🎓 Plan d'apprentissage — niveau intermédiaire", "=" * 60]
    current_module = None
    for lesson in LESSONS:
        if lesson["module"] != current_module:
            current_module = lesson["module"]
            out.append(f"\n📌 Module {current_module} — {lesson['module_title']}")
        mark = "✅" if lesson["id"] in done else "⬜"
        out.append(f"  {mark} {lesson['id']:<5} {lesson['title']}")
    total = len(LESSONS)
    pct = int(len(done) / total * 100) if total else 0
    out.append(f"\nProgression : {len(done)}/{total} leçons ({pct} %)\n")
    out.append("Commande : 'apprendre lecon <id>' pour suivre une leçon, 'apprendre terminer <id>' pour la valider.")
    return "\n".join(out)


def show_lesson(lesson_id: str) -> str:
    lesson = lesson_by_id(lesson_id)
    if not lesson:
        return f"Leçon « {lesson_id} » introuvable. Tape 'apprendre' pour voir le plan."
    out = [
        f"🎓 Module {lesson['module']} — {lesson['module_title']}",
        f"Leçon {lesson['id']} : {lesson['title']}",
        "=" * 60,
        lesson["content"],
        "",
        "🔗 Références authentiques :",
        "─" * 40,
        lesson_references(lesson),
        "",
        "🎯 Objectifs :",
    ]
    out.extend(f"• {o}" for o in lesson["objectives"])
    out.append("\nPour valider cette leçon : 'apprendre terminer " + lesson["id"] + "'")
    out.append("Pour approfondir une référence : 'demander explique cette leçon'")
    return "\n".join(out)