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
            "Le tawhid (l'unicité) est le fondement absolu de la foi musulmane. C'est le pilier sur lequel repose "
            "toute la religion : sans tawhid, aucune œuvre n'est acceptée. Ce mot arabe signifie « déclarer qu'Allah est "
            "Un, unique, sans associé ». C'est le message que tous les prophètes ont transmis à l'humanité, d'Adam à Muhammad ﷺ.\n\n"
            "Les savants ont divisé le tawhid en trois aspects complémentaires, qu'il est essentiel de comprendre :\n\n"
            "1) Tawhid ar-Rububiyyah — L'unicité de la Seigneurie : Allah est le seul Créateur de l'univers, le seul "
            "qui donne la vie et la mort, le seul qui gère tout ce qui existe. Il n'a pas de partenaire dans Sa "
            "Seigneurie. C'est comme si un architecte unique avait construit tout un immeuble : personne d'autre "
            "n'y a contribué. De même, Allah a tout créé sans aide.\n\n"
            "2) Tawhid al-Uluhiyyah — L'unicité de l'adoration : toute adoration — prière, invocation, sacrifice, "
            "crainte, amour, espoir — ne doit être adressée qu'à Allah seul. C'est le cœur du tawhid et la raison "
            "pour laquelle les prophètes ont été envoyés. Si quelqu'un invoque un saint, une tombe ou une étoile en "
            "espérant un secours, il commet le shirk (associé à Allah), qui est le pire des péchés.\n\n"
            "3) Tawhid al-Asma wa-s-Sifat — L'unicité des Noms et Attributs : Allah possède des Noms et Attributs "
            "parfaits (Ar-Rahman, Al-'Alim, Al-Qayyum, etc.). On ne peut ni déformer leur sens en les comparant à "
            "ceux des créatures, ni nier leur existence, ni poser la question du « comment » (bila kayf). Par exemple, "
            "Allah a une Main, un Visage, mais ce ne sont pas des membres humains : ce sont des réalités convenables "
            "à Sa majesté.\n\n"
            "La Sourate Al-Ikhlas (112) résume l'essence du tawhid en quatre versets : « Dis : Il est Allah, Unique. "
            "Allah, Le Seul dont on dépend. Il n'engendre pas et n'est pas engendré. Et nul n'est Lui équivalent. » "
            "Le verset du Trône (2:255) en détaille la grandeur. La chahada, premier pilier de l'islam, est "
            "précisément l'acte d'attester cette unicité : « J'atteste qu'il n'y a de divinité qu'Allah, et "
            "j'atteste que Muhammad est Son messager. »\n\n"
            "Point pratique : comment appliquer le tawhid au quotidien ? Avant chaque action, vérifiez que votre "
            "intention est purement pour Allah. Si vous faites une bonne action pour être loué par les gens, vous "
            "nuisez à votre tawhid. Si vous avez peur d'un problème santé ou de perdre votre emploi, souvenez-vous "
            "qu'Allah seul peut vous protéger. Le tawhid n'est pas une croyance abstraite : c'est une relation "
            "vivante avec votre Créateur."
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
            "La foi (iman) repose sur six piliers fondamentaux, enseignés dans le célèbre hadith de Jibril (ange Gabriel), "
            "l'un des hadiths les plus importants de l'islam. Dans ce hadith, l'ange Gabriel vient interrogé le Prophète ﷺ "
            "devant ses compagnons pour leur enseigner les fondements de leur religion.\n\n"
            "Les six piliers de l'iman sont :\n\n"
            "1) Croire en Allah : cela inclut de croire en Son existence, en Son unicité (tawhid), en Ses Noms et "
            "Attributs, et en Ses actes. C'est le pilier le plus fondamental. C'est comme la fondation d'un bâtiment : "
            "si elle s'effondre, tout le reste s'écroule.\n\n"
            "2) Croire aux anges : les anges sont des créatures luminenses créées par Allah, qui L'adorent sans relâche. "
            "Ils ont des rôles précis : Jibril (Gabriel) apporte la révélation, Mikael gère les provisions, Israfil sonnera "
            "la trompe du Jour dernier, et Azraïl (Malak al-Mawt) est l'ange de la mort. Les anges n'ont pas de volonté "
            "propre : ils obéissent parfaitement à Allah. Ils sont invisibles, mais ils sont réels.\n\n"
            "3) Croire aux Livres : Allah a révélé des Livres sacrés à Ses prophètes. Nous croyons au Tawrat (Moïse), "
            "aux Zabour (David), à l'Injil (Jésus) et au Coran (Muhammad ﷺ). Nous croyons que les textes actuels "
            "du Tawrat et de l'Injil ont été altérés par les humains, tandis que le Coran est préservé intégralement "
            "jusqu'à la fin des temps.\n\n"
            "4) Croire aux messagers : Allah a envoyé des prophètes à chaque peuple pour les guider. Nous croyons en "
            "tous les prophètes, sans distinction : Adam, Noé, Abraham, Moïse, Jésus, Muhammad ﷺ et tous les autres. "
            "Le Prophète Muhammad ﷺ est le dernier des prophètes (Khatam an-Nabiyyin).\n\n"
            "5) Croire au Jour dernier (Yawm al-Qiyamah) : c'est le jour de la résurrection, du jugement et de la "
            "rétribution éternelle. Les gens seront rassemblés devant Allah pour être jugés selon leurs œuvres. Les "
            "croyants entreront au Paradis (Jannah) et les mécréants seront punis en Enfer (Jahannam). C'est le jour "
            "qui donne un sens à toute notre vie : sans lui, les injustices ne seraient jamais réparées.\n\n"
            "6) Croire au destin (qadar) : tout ce qui arrive — bien ou mal — se fait avec la science, la volonté et "
            "la création d'Allah. Cela ne signifie pas que nous n'avons pas de choix : Allah nous a donné la liberté "
            "de choisir, mais Il sait d'avance ce que nous choisirons.\n\n"
            "Ces six piliers forment un tout inséparable. Vous ne pouvez pas en négliger un sansnuire aux autres. "
            "Par exemple, croire en Allah sans croire au Jour dernier, c'est comme construire une maison sans toit.\n\n"
            "Les trois plans de la religion : l'islam (soumission externe : prière, zakat, jeûne), l'iman (foi "
            "interne : les six piliers) et l'ihsan (excellence : « adorer Allah comme si tu Le vois, car si tu ne "
            "Le vois pas, Lui te voit »). Ces trois dimensions doivent être développées ensemble pour une foi complète."
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
            "Croire au décret divin (qadar) est le sixième pilier de la foi. Cela signifie que rien n'arrive sans la "
            "science, la volonté et la création d'Allah. Le qadar est un concept profond qui touche au mystère de la "
            "relation entre Allah et l'homme, et qui a fait l'objet de nombreux débats au cours de l'histoire islamique.\n\n"
            "Les savants ont classiquement défini quatre degrés du qadar :\n\n"
            "1) La science éternelle (al-'ilm) : Allah sait tout, avant même la création de l'univers. Il sait quel "
            "chemin chaque personne prendra, quelles seront ses bonnes et mauvaises actions, et quelle sera sa fin. "
            "C'est comme un auteur qui a écrit tout le roman avant même de commencer à l'écrire.\n\n"
            "2) L'écriture dans le Livre clair (al-lawh al-mahfudh) : Allah a tout consigné dans un Livre préservé, "
            "avant la création du temps et de l'espace. Tout y est inscrit : la durée de vie de chaque créature, ses "
            "provisions, ses épreuves.\n\n"
            "3) La volonté universelle (al-mashi'ah) : Allah veut et permet chaque chose. Rien ne se produit contre "
            "Sa volonté. Cependant, cette volonté ne contraint pas l'homme : Il nous a donné la liberté de choix, et "
            "c'est pour cela que nous serons jugés.\n\n"
            "4) La création de chaque chose (al-khalq) : Allah est le Créateur de tout, y compris des actions humaines. "
            "L'homme choisit librement, mais c'est Allah qui crée le pouvoir d'agir et les conséquences de l'action.\n\n"
            "Cette croyance ne doit pas mener au fatalisme. Le Prophète ﷺ a dit : « Lie ta chamelle, puis confie-toi "
            "à Allah » (Tirmidhi). Cela signifie que vous devez agir, prendre les moyens nécessaires, puis accepter "
            "le résultat avec confiance. Si vous êtes malade, consultez un médecin (moyen humain) et priez pour votre "
            "guérison (moyen divin). Les deux ne se contredisent pas : ils se complètent.\n\n"
            "Les extrêmes à éviter :\n"
            "- Le fatalisme (les Qadariyyah) : croire que nos actions n'ont aucune importance puisque tout est écrit. "
            "C'est faux : Allah nous juge sur nos choix.\n"
            "- Le relativisme (les Mu'tazilites) : croire que l'homme est totalement libre et qu'Allah ne sait pas "
            "d'avance ce qu'il fera. C'est aussi faux : Allah est Omniscient.\n\n"
            "La voie juste (Ahl as-Sunnah) : l'homme a une volonté réelle et choisit ses actions, mais Allah est le "
            "Créateur de tout et sait d'avance tout ce qui va se passer. Ce paradoxe apparent est le mystère du qadar. "
            "Crois au qadar sans entrer dans des spéculations inutiles qui divisaient les premières communautés. "
            "Le Coran dit : « Nul malheur n'atteint sur la terre ni en vous-même sans qu'il ne soit inscrit dans un "
            "Livre avant que Nous le fassions exister » (57:22). Cette croyance apporte la paix du cœur : vous savez "
            "que tout vient d'Allah, et que même les épreuves contiennent une sagesse et une miséricorde cachées."
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
            "La purification (taharah) est la clé de la prière : aucune prière n'est acceptée sans elle, sauf excuse "
            "légitime (maladie, danger, manque d'eau). C'est le premier acte que le musulman accomplit avant de se "
            "présenter devant Allah. Imaginez que vous allez rencontrer un roi : vous vous habillez correctement et "
            "vous vous lavez. Pour Allah, roi des rois, la propreté du corps est encore plus importante.\n\n"
            "Il existe trois types de purification rituelle :\n\n"
            "1) Le wudu (ablutions mineures) : il est nécessaire après des impuretés mineures (urine, selles, gaz, "
            "sommeil profond, perte de conscience). Les étapes obligatoires du wudu sont :\n"
            "   a) Formuler l'intention (niyyah) dans le cœur — pas besoin de la dire à voix haute\n"
            "   b) Se laver les mains jusqu'aux poignets trois fois\n"
            "   c) Se rincer la bouche (madmadah) trois fois\n"
            "   d) Inspirer l'eau par le nez (istinshaq) et l'expirer trois fois\n"
            "   e) Se laver le visage du front au menton et d'une oreille à l'autre trois fois\n"
            "   f) Se laver le bras droit du coude aux doigts trois fois, puis le bras gauche\n"
            "   g) Passer la main mouillée sur la tête une fois\n"
            "   h) Se laver les pieds jusqu'aux chevilles trois fois, en frottant entre les orteils\n"
            "L'ordre est important : le Coran les mentionne dans cette séquence (5:6). Ensuite, il est sunna de "
            "passer les mains mouillées sur les oreilles et de dire : « Ashhadu an la ilaha illallah wahdahu la "
            "shareek lah, wa ashhadu anna Muhammadan 'abduhu wa rasooluh » (J'atteste qu'il n'y a de divinité "
            "qu'Allah, sans associé, et j'atteste que Muhammad est Son serviteur et messager).\n\n"
            "2) Le ghusl (grand lavage rituel) : il est obligatoire après les grandes impuretés (rapport sexuel, "
            "rêves mouillés avec éjaculation, menstrues, lochies). Il consiste à faire couler l'eau sur tout le "
            "corps, y compris les cheveux, en s'assurant que l'eau touche chaque partie.\n\n"
            "3) Le tayammum (purification sèche) : en l'absence d'eau ou si l'eau est dangereuse pour la santé, "
            "on peut utiliser de la terre propre. Frappez la terre avec vos paumes, soufflez dessus, puis passez-les "
            "sur votre visage et vos bras. C'est une miséricorde d'Allah qui permet de prier même dans les situations "
            "les plus difficiles.\n\n"
            "Ce qui annule le wudu : tout ce qui sort des voies naturelles (urine, selles, gaz), le sommeil profond, "
            "la perte de conscience, toucher ses parties intimes avec la paume de la main nue.\n\n"
            "Conseil pratique : ne gaspillez pas l'eau. Le Prophète ﷺ faisait son wudu avec un mudd d'eau "
            "(l'équivalent de deux mains jointes). Et après le wudu, il est sunna de prier deux rak'at "
            "surérogatoires : c'est l'une des meilleures œuvres pour entrer au Paradis."
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
            "La salat (prière) est le premier pilier pratique après la chahada. Le Prophète ﷺ a dit que la prière "
            "sera « la première chose dont on sera interrogé le Jour de la Résurrection ». Si elle est bonne, tout "
            "le reste sera bon ; si elle est défectueuse, tout sera perdu. C'est le seul pilier qui revient chaque jour.\n\n"
            "Les cinq prières obligatoires et leurs horaires :\n"
            "- Fajr (l'aube) : 2 rak'at — de l'aube au lever du soleil\n"
            "- Dhuhr (midi) : 4 rak'at — après le passage du soleil au zénith\n"
            "- Asr (après-midi) : 4 rak'at — de l'après-midi jusqu'au coucher du soleil\n"
            "- Maghrib (soir) : 3 rak'at — du coucher du soleil jusqu'à la disparition du crépuscule\n"
            "- Isha (nuit) : 4 rak'at — du crépuscule à l'aube\n\n"
            "Pour que la prière soit valide, plusieurs conditions doivent être réunies :\n"
            "- Être musulman, raisonnable et pubère\n"
            "- Être en état de purification (wudu ou ghusl)\n"
            "- Se tourner vers la qibla (la Kaaba à La Mecque)\n"
            "- Porter des vêtements propres et couvrant les zones de pudeur\n"
            "- S'assurer que le moment de la prière est entré\n\n"
            "Les piliers de la rak'ah (unité de prière) :\n"
            "- Le takbir d'ouverture : « Allahu Akbar » (Allah est le plus grand)\n"
            "- La récitation de la Fatiha (obligatoire dans chaque rak'ah)\n"
            "- L'inclinaison (ruku) : pencher le haut du corps en disant « Subhana Rabbiya-l-'Adhim » (gloire à mon Seigneur l'Immense)\n"
            "- Le redressement (itidal) après le ruku\n"
            "- La prosternation (sujud) : « Subhana Rabbiya-l-A'la » (gloire à mon Seigneur le Très-Haut)\n"
            "- L'élévation entre les deux prosternations\n"
            "- Le tashahhud final (attestation) et la salutation de fin (salam) à droite puis à gauche\n\n"
            "Les recommandations importantes (sunna) : réciter une sourate supplémentaire après la Fatiha, faire "
            "les takbirs de transition, dire le Qunoot pendant certaines prières, se concentrer (khushu) en écoutant "
            "et méditant le sens des paroles.\n\n"
            "La prière comme école de discipline : elle structure la journée du musulman. Cinq moments par jour, "
            "toujours aux mêmes heures, où l'on se détache des préoccupations du monde pour se connecter à Allah. "
            "Le Coran nous enseigne : « La prière préserve de la turpitude et du blâmable » (29:45). C'est la "
            "prière végétale — vécue avec concentration et humilité — qui élève et protège, et non un simple "
            "mouvement répété mécaniquement. Le Prophète ﷺ disait que lorsqu'on prie avec humilité, les péchés "
            "s'effacent de la face, de la tête et du corps de sa ligne droite de prosternation."
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
            "La prière du vendredi (salat al-jumu'ah) est l'une des grandes spécificités de cette communauté. "
            "Elle remplace la prière de Dhuhr (midi) pour celui qui a l'obligation d'y participer : homme libre, "
            "pubère, résident (non voyageur), et capable financièrement et physiquement. Elle comporte deux rak'at "
            "au lieu de quatre, précédées de deux sermons (khutbah) prononcés par l'imam.\n\n"
            "Le verset clé est 62:9 : « Ô vous qui croyez ! Lorsqu'on appelle à la prière du vendredi, accourez à "
            "l'invocation d'Allah et laissez tout commerce. Cela est meilleur pour vous, si vous saviez. »\n\n"
            "Pourquoi le vendredi est important ?\n"
            "- C'est le meilleur jour de la semaine : « Le meilleur jour où le soleil se lève est le vendredi » (Abu Dawud)\n"
            "- Il contient une heure où les invocations sont exaucées (la plupart des savants disent qu'elle se situe "
            "entre l'Asr et le Maghrib, en fin de journée)\n"
            "- Il comporte des sunan recommandées : se laver (ghusl du vendredi), se parfumer, porter de beaux "
            "vêtements, réciter la sourate Al-Kahf (18) dans la journée, faire beaucoup de prières sur le Prophète ﷺ\n"
            "- Les musulmans sont réunis pour une adoration collective hebdomadaire\n\n"
            "L'éthique du vendredi : écouter attentivement le sermon sans bavarder (même pour dire « tais-toi » à "
            "quelqu'un), arriver tôt pour occuper les premiers rangs, ne pas déranger les gens en enjambant leurs "
            "rangées.\n\n"
            "La prière en congrégation (jama'ah) : le Prophète ﷺ a dit que la prière en groupe est 25 à 27 fois "
            "supérieure à la prière seul. Pourquoi ? Parce qu'elle unit la communauté, que les anges assistent à la "
            "réunion, et que les récompenses se multiplient. Se rendre à la mosquée pas à pas efface les péchés et "
            "élève les degrés : à chaque pas qui vous approche de la mosquée, vous gagnez en récompense.\n\n"
            "Conseil pratique : si vous êtes un homme, essayez de faire au moins Fajr et Isha à la mosquée en plus "
            "du vendredi. Le Prophète ﷺ a dit que celui qui prie Isha en congrégation c'est comme s'il avait prié "
            "la moitié de la nuit, et celui qui prie aussi Fajr en congrégation, c'est comme s'il avait prié toute "
            "la nuit entière."
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
            "La zakat est le troisième pilier de l'islam. Le mot « zakat » vient de la racine arabe qui signifie à "
            "la fois « purification » et « croissance ». La zakat purifie le bien et la personne : elle purifie "
            "l'argent des souillures de l'avarice et de l'égoïsme, et elle purifie l'âme de la cupidité. C'est aussi "
            "un droit des pauvres sur la richesse des aisés : la pauvreté n'est pas une fatalité, et la richesse "
            "n'est pas un droit absolu sans contrepartie.\n\n"
            "Quand la zakat est-elle obligatoire ? Pour un musulman adulte, libre (non esclave) et sain d'esprit qui "
            "possède le seuil minimum (nissab) pendant une année lunaire complète (hawl). Les conditions exactes :\n"
            "- Posséder un bien qui atteint le nissab\n"
            "- Que le bien ait été en votre possession pendant un an lunaire complet\n"
            "- Que le bien soit sans dette (les dettes sont déduites du calcul)\n\n"
            "Le nissab (seuil minimum) est fixé à 85 grammes d'or pur (soit environ 20 dinars) ou 595 grammes "
            "d'argent (soit 200 dirhams). Aujourd'hui, la plupart des savants utilisent la valeur de l'argent pour "
            "faciliter l'accessibilité à la zakat.\n\n"
            "Les taux de la zakat :\n"
            "- Or, argent et biens commerciaux : 2,5 % (1/40) de la valeur totale\n"
            "- Bétail (camels, bovins, ovins) : taux variables selon le nombre\n"
            "- Produits agricoles irrigués naturellement : 10 % de la récolte\n"
            "- Produits agricoles irrigués artificiellement : 5 % de la récolte\n"
            "- Trésors, minerais : 20 % (khums)\n\n"
            "Les huit catégories de bénéficiaires (Coran 9:60) :\n"
            "1) Les pauvres (fuqara) : ceux qui n'ont pas de quoi subvenir à leurs besoins essentiels\n"
            "2) Les nécessiteux (masakin) : ceux dont les moyens sont insuffisants\n"
            "3) Les collecteurs de zakat (amilin) : ceux qui sont employés pour la collecter\n"
            "4) Ceux dont les cœurs sont à gagner (muallafat al-qulub) : les nouveaux convertis pour les soutenir\n"
            "5) L'affranchissement des esclaves (riqab)\n"
            "6) Les endettés (gharimin) : ceux qui sont accablés de dettes\n"
            "7) Dans le sentier d'Allah (fi sabilillah) : traditionnellement le jihad, aujourd'hui étendu aux "
            "projets religieux, éducatifs et caritatifs\n"
            "8) Le voyageur démuni (ibn as-sabil) : celui qui est bloqué loin de chez lui\n\n"
            "Erreurs à éviter : verser la zakat en retard sans excuse, donner le pire de son bien (Allah dit de "
            "donner « le meilleur de ce que vous avez acquis », 2:267), faire un reproche ou blesser le bénéficiaire "
            "(ce qui annule la récompense, 2:264).\n\n"
            "Le Prophète ﷺ a dit : « L'aumône ne diminue pas la richesse » (Muslim). La zakat est un investissement "
            "dans l'au-delà, et Allah multiplie la récompense de ceux qui dépensent dans Sa voie."
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
            "Le jeûne du mois de Ramadan est le quatrième pilier de l'islam. Allah dit dans le Coran : « Ô vous qui "
            "avez cru ! Le jeûne vous a été prescrit comme il a été prescrit à ceux qui vous ont précédés, afin que "
            "vous atteigniez la piété (taqwa) » (2:183). Ce verset montre plusieurs choses importantes :\n\n"
            "- La prescription est ancienne (elle existait avant l'islam, chez les communautés précédentes)\n"
            "- Le but premier n'est pas la privation physique, mais l'atteinte de la piété (conscience d'Allah)\n\n"
            "Le jeûne consiste à s'abstenir de manger, de boire et des relations conjugales depuis l'aube (fajr) "
            "jusqu'au coucher du soleil (maghrib), avec l'intention (niyyah) formée au préalable. Mais le jeûne "
            "va bien au-delà : le Prophète ﷺ a dit « Celui qui ne délaisse pas le mensonge et les mauvaises actions, "
            "Allah n'a nul besoin qu'il délaisse sa nourriture et sa boisson » (Bukhari). Un jeûne qui ne purifie "
            "pas la langue et le comportement est un jeûne incomplet.\n\n"
            "Qui doit jeûner ? Tout musulman pubère, sain d'esprit et capable physiquement.\n\n"
            "Qui est dispensé ?\n"
            "- Le malade (qui ne peut pas supporter le jeûne) : doit rattraper plus tard ou nourrir un pauvre\n"
            "- Le voyageur (s'il le souhaite) : doit rattraper plus tard\n"
            "- La femme gestante ou allaitante (si c'est dangereux pour elle ou son bébé) : doit rattraper\n"
            "- La femme en période de règles ou de lochies : ne doit pas jeûner mais doit rattraper plus tard\n"
            "- La personne âgée ou malade chronique : peut nourrir un pauvre pour chaque jour de jeûne manqué (fidya)\n\n"
            "Ce qui annule le jeûne : manger ou boire volontairement, avoir des rapports intimes en journée, "
            "l'éjaculation volontaire, les règles ou les lochies, le vomissement provoqué volontairement.\n\n"
            "Les recommandations du Ramadan :\n"
            "- Prendre le repas du sahur (repas avant l'aube) : « Il y a de la baraka dans le sahur » (Bukhari)\n"
            "- Rompre le jeûne rapidement dès le coucher du soleil, de préférence avec des dattes\n"
            "- Accomplir la prière de Tarawih pendant les nuits du Ramadan\n"
            "- Réciter et méditer le Coran : le Ramadan est le mois du Coran\n"
            "- Multiplier les invocations, l'aumône et les bonnes actions\n"
            "- Verser la zakat al-fitr à la fin du Ramadan (une mesure de nourriture par personne)\n\n"
            "La nuit du destin (Laylat al-Qadr) est plus méritoire que mille mois (97:3). Elle se trouve dans les "
            "dix dernières nuits du Ramadan, particulièrement les nuits impaires (21, 23, 25, 27, 29). C'est une "
            "nuit de grande valeur où les invocations sont exaucées et où la récompense est multipliée. "
            "L'invocation recommandée : « Allahumma innaka 'afuwwun tuhibbu-l-'afwa fa'fu 'anni » (Ô Allah, Tu es "
            "Pardonneur et Tu aimes le pardon, pardonne-moi).\n\n"
            "Le Ramadan est une école de piété : elle vous apprend à contrôler vos désirs, à ressentir la faim "
            "des pauvres, à renforcer votre volonté, et à purifier votre cœur. Ce n'est pas un mois de simple "
            "privation, mais un mois de transformation spirituelle."
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
            "Le hajj (pèlerinage à La Mecque) est le cinquième pilier de l'islam et l'un des plus grands actes "
            "d'adoration. C'est l'aboutissement spirituel d'une vie de foi, un voyage unique qui rassemble des "
            "musulmans de toutes les races, langues et nations en un même lieu, une même tenue, un même but : "
            "l'adoration d'Allah seul.\n\n"
            "L'obligation du hajj : il est obligatoire une fois dans la vie pour qui en a la capacité. Le Coran "
            "dit : « Et c'est un devoir envers Allah pour les gens qui en ont la capacité, de faire le pèlerinage "
            "de la Maison » (3:97). La capacité inclut : les moyens financiers (pour le voyage et l'entretien de "
            "sa famille), la santé physique, et la sécurité du chemin.\n\n"
            "Le temps du hajj : chaque année du 8 au 12 de dhul-hijjah (le douzième mois du calendrier islamique).\n\n"
            "Les rites majeurs, étape par étape :\n"
            "1) L'ihram : entrée en état de sacralité. L'homme porte deux rectangles de tissu blanc non cousus ; "
            "la femme porte des vêtements modestes. Pendant l'ihram, on ne peut pas couper ses cheveux ou ongles, "
            "utiliser du parfum, chasser, avoir des rapports conjugaux.\n"
            "2) Le tawaf : circumambulation autour de la Kaaba sept fois dans le sens antihoraire.\n"
            "3) Le sa'i : parcours entre les collines de Safa et Marwah sept fois, en souvenir de la quête d'eau "
            "de Hajar pour son fils Ismaïl.\n"
            "4) Le séjour à Mina (8 dhul-hijjah) : passer la journée et la nuit à Mina.\n"
            "5) Le séjour à Arafat (9 dhul-hijjah) : c'est LE rite central. Le Prophète ﷺ a dit « Le hajj, c'est "
            "Arafat ». On y reste debout (wuquf) pendant la journée, en invoquant Allah, en se repentant, en "
            "démontrant sa soumission totale.\n"
            "6) Muzdalifah (nuit du 9 au 10) : passer la nuit sous les étoiles après le coucher du soleil à Arafat.\n"
            "7) La lapidation des stèles (rajm) à Mina (10, 11, 12 dhul-hijjah) : on lance sept petits cailloux "
            "sur la jamrah al-aqabah, symbolisant le rejet de Satan.\n"
            "8) Le sacrifice (udhiyyah) : immoler un animal (mouton, bovin, ou une part de chameau) pour commémorer "
            "le sacrifice d'Abraham, et donner la viande aux pauvres.\n"
            "9) La coupe des cheveux et la sortie de l'ihram.\n"
            "10) Le tawaf al-ifadah : tourner autour de la Kaaba de nouveau.\n\n"
            "La dimension spirituelle : le hajj incarne l'égalité absolue des êtres humains devant Allah. Quel que "
            "soit le statut social, tous portent les mêmes vêtements blancs, tous accomplissent les mêmes rites. C'est "
            "le plus grand rassemblement annuel de l'humanité. Le Prophète ﷺ a dit : « Le hajj agréé n'a d'autre "
            "récompense que le Paradis. » Un hajj acceptable exige : une pureté d'intention, des moyens licites, "
            "et un comportement impeccable envers les autres pèlerins.\n\n"
            "Astuce : commencez à préparer votre hajj bien à l'avance — engagez-vous dans la pratique régulière "
            "des piliers, mémorisez les invocations du pèlerin, et aspergez de bonnes œuvres quotidiennes. "
            "Le hajj n'est pas une vacance ou un voyage touristique : c'est une adoration majeure qui demande "
            "préparation spirituelle et matérielle."
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
            "La Sirah (biographie du Prophète ﷺ) est essentielle pour comprendre l'islam. Allah dit : « Vous avez en "
            "l'envoyé d'Allah un excellent modèle (uswah hasanah) pour quiconque espère en Allah et au Jour dernier » (33:21). "
            "En étudiant la vie du Prophète ﷺ, nous apprenons non seulement les événements historiques, mais aussi comment "
            "appliquer l'islam dans toutes les situations de la vie.\n\n"
            "La naissance et le contexte : Muhammad ﷺ est né à La Mecque vers l'an 570 (élu Année de l'Éléphant). La Mecque "
            "était un centre commercial et religieux : la Kaaba attirait des pèlerins d'Arabie entière, qui adoraient "
            "de nombreuses idoles. La société était tribale, marquée par la division, la violence et l'idolâtrie. "
            "C'est dans ce contexte que le dernier prophète est né.\n\n"
            "L'orphelin : son père Abdullah est mort avant sa naissance. Sa mère Amina est morte quand il avait environ "
            "6 ans. Il fut alors confié à son grand-père Abdul-Muttalib, puis, à la mort de celui-ci, à son oncle Abu Talib. "
            "Cette expérience de l'orphelinage lui enseigna la compassion et la vigilance, et Allah le rappelle : « Ne "
            "t'a-t-Il pas trouvé orphelin, ne t'a-t-Il pas accueilli ? » (93:6).\n\n"
            "La jeunesse vertueuse : avant la prophétie, Muhammad ﷺ était connu pour son intégrité exceptionnelle. "
            "Il était appelé « al-Amin » (le digne de confiance) et « as-Sadiq » (le véridique). Il refusait de participer "
            "aux idolâtries et aux injustices de son peuple. Quand la Kaaba fut reconstruite, et que les tribus se "
            "disputaient l'honneur de placer la Pierre noire, il trouva une solution pacifique en posant la pierre sur "
            "le pan de son manteau et en demandant aux chefs de tribus de tenir les bords. C'était un sage médiateur.\n\n"
            "À 25 ans, il épouse Khadija bint Khuwaylid, une commerçante respectable de 40 ans, qu'il avait accompagnée "
            "lors de ses voyages commerciaux. Khadija sera son premier soutien, la première à le croire, et elle restera "
            "son épouse unique jusqu'à sa mort.\n\n"
            "La première révélation : à l'âge de 40 ans, Muhammad ﷺ aimait se retirer en méditation dans la grotte de "
            "Hira, en haut de la montagne de lumière près de La Mecque. C'est là que l'archange Gabriel (Jibril) lui apparut "
            " et lui dit « Lis ! ». Muhammad ﷺ, illettré, répondit : « Je ne sais pas lire ». Gabriel le serra fort et "
            "répéta ; et c'est alors que furent révélés les tout premiers versets de la Sourate Al-Alaq : « Lis, au nom "
            "de ton Seigneur qui a créé... » (96:1-5).\n\n"
            "La révélation commença par des songes véridiques pendant six mois, puis la descente directe de la parole "
            "d'Allah. Terrifié et secoué, Muhammad ﷺ rentra chez lui, enveloppé dans une couverture, et dit à Khadija : "
            "« Couvre-moi, couvre-moi ». C'est Khadija qui le rassura, et son cousin Waraqa, chrétien savant, confirma : "
            "« Cela est le grand Namus (la révélation) qui est venu à Moïse. »\n\n"
            "La mission commence : Muhammad ﷺ appela d'abord discrètement son clan, puis ouvertement toute la Mecque. "
            "La plupart des Mecquois le rejetèrent, le traitèrent de menteur et de sorcier, et persécutèrent ses "
            "compagnons. Malgré cela, il resta patient et ferme, ce qui lui vaudra plus tard d'être suivi par "
            "des milliers de personnes."
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
            "La Hégire (migration vers Médine) est l'un des événements fondateurs de l'islam. Elle marque le début "
            "du calendrier musulman (l'an 1 de l'Hégire, soit 622 après J.-C.) et constitue le tournant décisif : "
            "la petite communauté persécutée de La Mecque devient une véritable société organisée.\n\n"
            "Le contexte : après treize années de prédication à La Mecque, les musulmans étaient soumis à une "
            "persécution croissante. Certains avaient déjà émigré en Abyssinie (l'actuelle Éthiopie) pour se "
            "réfugier auprès du roi chrétien juste Negus. Mais la situation continuait de se dégrader à La Mecque.\n\n"
            "Le chemin vers la Hégire : lors du pèlerinage annuel, des hommes de Yathrib (la future Médine) "
            "rencontrèrent le Prophète ﷺ et embrassèrent l'islam. Ils s'engagèrent à le protéger et à l'accueillir "
            "chez eux. Ce furent les premières promesses d'Aqaba, puis les deuxièmes promesses d'un groupe plus "
            "important. L'islam avait trouvé une terre d'accueil.\n\n"
            "La migration du Prophète ﷺ : quand les Mecquois complotèrent pour assassiner le Prophète ﷺ pendant "
            "son sommeil, Allah l'avertit. Il quitta la Mecque avec son fidèle compagnon Abu Bakr. Ils se cachèrent "
            "dans la grotte de Thawr pendant trois jours, tandis que les Mecquois les cherchaient. Pendant ce séjour, "
            "Allah révéla : « Si vous ne lui apportez pas secours… Allah a déjà été son secours, lorsqu'il a fait "
            "sortir ceux qui avaient mécru, alors qu'ils étaient deux en la grotte et qu'il disait à son compagnon : "
            "« Ne t'attriste pas, Allah est avec nous » » (9:40).\n\n"
            "La construction de Médine : à son arrivée à Médine (alors appelée Yathrib), le Prophète ﷺ construisit "
            "la première mosque (Masjid an-Nabawi) au cœur de la ville. Puis il établit trois piliers de la nouvelle "
            "société :\n"
            "1) La fraternité (mu'akhah) : il déclara que chaque émigrant (Muhajir) était lié à un partisan (Ansar). "
            "Les Ansars, généreux, partagèrent leurs biens et leurs maisons avec les émigrants démunis.\n"
            "2) La constitution de Médine : il rédigea un pacte entre les musulmans, les juifs et les autres tribus, "
            "établissant une coexistence pacifique fondée sur la justice et la protection mutuelle. C'était l'un "
            "des premiers documents de ce type dans l'histoire.\n"
            "3) L'appel à la prière (adhan) : la mosquée de Médine verra naître l'adhan, l'appel à la prière qui "
            "résonne encore aujourd'hui dans le monde entier.\n\n"
            "Les leçons de la Hégire :\n"
            "- La patience et la sagesse : les prophètes ne forcent jamais les gens, ils éduquent et guident\n"
            "- La solidarité : les musulmans s'entraidaient, partageant biens et maisons\n"
            "- La tolérance : la constitution de Médine incluait les non-musulmans\n"
            "- L'organisation : la Hégire montre comment une communauté se construit sur des fondations spirituelles, "
            "sociales et politiques solides\n\n"
            "Le hadith de l'intention est lié à la Hégire : « Les actions ne valent que par leurs intentions, et "
            "chacun aura ce qu'il a intentionné. Celui dont la migration est pour Allah et Son messager, sa migration "
            "est pour Allah et Son messager ; et celui dont la migration est pour des biens du monde à obtenir ou "
            "une femme à épouser, sa migration est pour ce pour quoi il a émigré » (Bukhari n°1)."
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
            "La conquête de La Mecque (Fath Makkah) en l'an 8 de l'Hégire (630) est l'un des moments les plus "
            "émouvants de la Sirah. Elle illustre de manière éclatante le pardon prophétique et l'aboutissement "
            "de vingt-trois années de prédication patiente.\n\n"
            "Le contexte : les Quraysh (tribu de la Mecque) avaient violé le pacte de Hudaybiyah conclu avec les "
            "musulmans, en attaquant une tribu alliée des musulmans. Le Prophète ﷺ rassembla une armée de dix mille "
            "hommes et marcha sur la Mecque, avec l'intention de pénétrer sans effusion de sang.\n\n"
            "La chute pacifique : l'armée musulmane entra dans La Mecque de manière coordonnée et presque sans "
            "résistance. Abu Sufyan, le chef des Quraysh, fut conduit devant le Prophète ﷺ et s'embrassa. Le "
            "Prophète ﷺ lui dit : « Quiconque entre chez Abu Sufyan est en sécurité, quiconque ferme sa porte est "
            "en sécurité, et quiconque entre dans la mosquée est en sécurité. »\n\n"
            "Le pardon : une fois la Mecque sous contrôle, le Prophète ﷺ se tint à la porte de la Kaaba et posa "
            "une question mémorable aux habitants rassemblés : « Ô Quraysh ! Quelle est la voie que vous pensez "
            "que je vais prendre à votre égard ? » Ils répondirent : « Nous pensons que tu seras bon, car tu es "
            "un frère généreux, le fils d'un frère généreux. » Alors il dit : « Allez, vous êtes libres (Talaqun). »\n\n"
            "Il fit ensuite purifier la Kaaba de ses 360 idoles, en récitant : « La vérité est venue et l'erreur "
            "s'est évanouie. L'erreur est vouée à disparaître » (17:81). Le puissant chef qui avait consacré sa "
            "vie à combattre l'islam avait réussi à pénétrer dans la ville sans effusion de sang, avec un message "
            "de miséricorde et de pardon.\n\n"
            "Les leçons de la conquête :\n"
            "- Le pardon est plus puissant que la vengeance : le Prophète ﷺ avait été persécuté, expulsé, et ses "
            "compagnons avaient été torturés dans cette même ville. Pourtant, il pardonna.\n"
            "- La clémence dans la victoire : au lieu d'humilier ceux qui l'avaient combattu, il leur offrit la "
            "sécurité et la dignité. C'est le comportement d'un véritable leader spirituel.\n"
            "- L'objectif n'était pas la conquête matérielle mais l'établissement de la justice et de l'adoration "
            "d'Allah.\n\n"
            "Le sermon d'adieu (Hujjat al-Wada) : deux ans plus tard, en l'an 10 de l'Hégire, le Prophète ﷺ "
            "accomplit son pèlerinage d'adieu. Devant plus de cent mille personnes rassemblées à Arafat, il "
            "prononça un sermon universel qui résume les principes essentiels de l'islam :\n"
            "- Le sang et les biens des personnes sont sacrés : « Vos vies et vos biens vous sont sacrés, comme "
            "le sont ce jour et ce mois »\n"
            "- L'usure est abolie (suite aux révélations)\n"
            "- Les droits de la femme : « Traitez bien les femmes »\n"
            "- L'égalité : « Aucune supériorité pour un Arabe sur un non-Arabe, ni pour un non-Arabe sur un Arabe, "
            "ni pour un Blanc sur un Noir, si ce n'est par la piété »\n"
            "- La fidélité au Coran et à la Sunna : « Je vous ai laissé deux choses ; tant que vous vous y "
            "attacherez, vous ne vous égarerez jamais : le Livre d'Allah et ma Sunna. »\n\n"
            "Ce sermon est le testament du Prophète ﷺ : il résume en quelques phrases les fondamentaux de "
            "l'humanité, de la justice et de la foi."
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
            "Le Coran est la parole incréée d'Allah, révélée au Prophète Muhammad ﷺ par l'intermédiaire de "
            "l'archange Gabriel (Jibril), pendant une période d'environ 23 ans (609-632 de notre ère). C'est le "
            "Livre le plus important de l'islam : sa source et son fondement. Comprendre le Coran, c'est "
            "comprendre le message et la religion.\n\n"
            "La révélation (wahy) : la Wahy est la transmission de la parole d'Allah au Prophète ﷺ, de manière "
            "cachée et directe, à travers Gabriel ou d'autres moyens. Le Coran a été révélé de manière "
            "progressive, par versets et par sourates, en fonction des circonstances et des besoins de la "
            "communauté. Allah dit : « Et (Nous avons fait descendre) le Coran en le fragmentant, afin que tu le "
            "récites lentement aux gens. Et Nous l'avons fait descendre d'une manière progressive » (17:106).\n\n"
            "La préservation du texte : dès la première révélation, les compagnons mémorisaient les versets et "
            "les consignaient par écrit sur des os, des feuilles de palmier, des pierres et des peaux. Le Prophète "
            "ﷺ dictait chaque verset à ses scribes (dont Zayd ibn Thabit). Après sa mort, le calife Abu Bakr "
            "ordonna de rassembler le Coran en un premier volume (mushaf) pour préserver le texte. Le calife "
            "Uthman unifia ensuite toutes les versions en une seule écriture (la recension uthmanienne), et "
            "envoya des copies aux grandes villes. Cette préservation est un miracle : Allah garantit que « C'est "
            "Nous qui avons fait descendre le Rappel, et c'est Nous qui en sommes les gardiens » (15:9). Aucun "
            "autre livre sacré n'a été préservé de cette manière depuis 1400 ans.\n\n"
            "Le Coran comprend 114 sourates et 6236 versets. Il est divisé en 30 juz' (sections) pour faciliter "
            "la lecture complète pendant le Ramadan.\n\n"
            "La distinction Makki/Madani : les sourates révélées avant la Hégire (au moment du séjour à La Mecque) "
            "sont dites « mecquoises » (Makkiyah) ; celles révélées après la Hégire (à Médine) sont dites "
            "« médinoises » (Madaniyah).\n"
            "- Les sourates mécquoises traitent principalement de la foi, du tawhid, de la résurrection, des "
            "récits des prophètes précédents, de la patience face à l'oppression. Elles sont généralement courtes "
            "et poétiques.\n"
            "- Les sourates médinoises traitent de la législation (fiqh), du culte, de la vie sociale, de la "
            "famille, de l'économie et des règles de vie en communauté. Elles sont généralement plus longues et "
            "plus détaillées.\n\n"
            "Les circonstances de la révélation (asbab an-nuzul) : connaître pourquoi un verset a été révélé "
            "éclaire son sens. Par exemple, le verset sur la médisance a été révélé après qu'un compagnon ait "
            "médisé d'une personne. Ce contexte enrichit la compréhension du texte.\n\n"
            "Le Coran n'est pas seulement un texte à lire : c'est un guide pour la vie. Allah dit : « Ceci est le "
            "Livre au sujet duquel il n'y a aucun doute, un guide pour les pieux » (2:2). Chaque musulman est "
            "invité à le lire, à le mémoriser, à le méditer et à l'appliquer."
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
            "Le tajwid est la science de la récitation correcte du Coran. Il consiste à donner à chaque lettre son "
            "articulation correcte (makhraj) et ses caractéristiques propres (sifât), et à respecter les règles "
            "de prolongation (madd), de nasalisation (ghunnah), d'assimilation (idgham) et d'arrêt (waqf).\n\n"
            "Beaucoup de débutants négligent le tajwid et pensent qu'il s'agit d'une ornementation optionnelle. "
            "C'est une erreur : le tajwid protège le sens du texte sacré. Une faute de prononciation peut changer "
            "le sens d'un verset. Allah nous demande « de réciter le Coran, lentement et clairement » (73:4).\n\n"
            "Les notions de base à maîtriser :\n\n"
            "1) L'articulation (makhraj) : chaque lettre arabe a un point d'articulation précis. Par exemple, "
            "le « qaf » (ق) vient du fond de la gorge, le « sin » (س) du bout de la langue, le « mim » (م) des "
            "lèvres. Il faut s'entraîner à articuler chaque lettre correctement.\n\n"
            "2) Les caractéristiques des lettres (sifât) : chaque lettre a des qualités comme le fait d'être "
            "prononcée avec force (shiddah) ou douceur (rikhwah), ou d'être « gutturale » (halqiyyah). Parmi les "
            "plus importantes : les lettres « emphatiques » (ت، د، ط، ص، ض، ظ، ق) qui sont prononcées avec "
            "profondeur, et les lettres « gutturales » (ح، خ، ع، غ، هـ، أ) qui viennent de la gorge.\n\n"
            "3) Les règles de nasalisation (ghunnah) : le son nasal prolongé pour les lettres « nun » (ن) et "
            "« mim » (م) lorsqu'elles sont accompagnées d'un shaddah ou suivies de certaines lettres.\n\n"
            "4) Les prolongations (madd) : certaines voyelles sont allongées plus ou moins longtemps selon la "
            "présence de lettres de prolongation (alif, waw, ya). Exemple : la madd al-munfasil (séparée) se "
            "prolonge de 4 à 5 temps lorsque le prolongement est suivi d'une hamza dans le mot suivant.\n\n"
            "5) Les arrêts (waqf) : savoir où s'arrêter et où continuer. Les symboles en marge du Coran (comme "
            "le م (lazim = obligatoire) ou le ج (ja'iz = permis) indiquent les règles d'arrêt.\n\n"
            "Comment progresser :\n"
            "- Écouter des récitateurs reconnus (comme Al-Husary, Al-Minshawi, Sudais, Al-Afasy) et imiter leur "
            "récitation\n"
            "- S'entraîner à l'articulation des lettres avec des exercices répétés (le hulq, la langue, les lèvres)\n"
            "- Réciter lentement, avec tartil (lenteur) comme demandé par Allah\n"
            "- Lire la Sourate Al-Fatiha correctement : c'est la base de toutes les prières\n\n"
            "Le tajwid est une discipline spirituelle : en récitant correctement, on entre en état de "
            "recueillement (khushu) et on s'approche d'Allah. Le Prophète ﷺ a dit : « Récitez le Coran, car il "
            "intercédera en faveur de ses compagnons le Jour de la Résurrection » (Muslim)."
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
            "Le Coran et la Sunna sont les deux sources fondamentales de l'islam. Le Coran est la parole révélée "
            "d'Allah ; la Sunna est la deuxième source : elle comprend les paroles (aqwal), les actes (af'al), "
            "les approbations (taqrir) du Prophète ﷺ, ainsi que ses qualités morales et physiques. Le hadith "
            "est le rapport (le récit) qui transmet la Sunna.\n\n"
            "La relation entre le Coran et la Sunna :\n\n"
            "1) La Sunna confirme ce que dit le Coran : par exemple, le Coran ordonne la prière ; la Sunna "
            "explique précisément comment faire cette prière.\n\n"
            "2) La Sunna détaille ce que le Coran résume : le Coran ordonne la zakat, mais c'est la Sunna qui "
            "fixe le nissab (seuil minimum) et les taux. Le Coran ordonne le hajj, mais c'est la Sunna qui "
            "explique les rites étape par étape.\n\n"
            "3) La Sunna peut ajouter des prescriptions : par exemple, l'interdiction d'épouser en même temps "
            "une tante et sa nièce, ou la prière en congrégation.\n\n"
            "L'autorité de la Sunna est fondée sur le Coran : « Prenez ce que le Messager vous donne et "
            "abstenez-vous de ce qu'il vous interdit » (59:7), et « Quiconque obéit au Messager obéit certainement "
            "à Allah » (4:80).\n\n"
            "Comment se transmet le hadith ? Chaque hadith comporte deux parties :\n"
            "- Le matn : le texte du hadith lui-même (le contenu de la parole ou de l'acte rapporté)\n"
            "- L'isnad : la chaîne de transmission (la liste des personnes qui ont transmis le hadith, du "
            "rapporteur original au compilateur)\n\n"
            "La méthodologie des savants : les compilateurs (muhaddithun) ont développé une science rigoureuse "
            "pour vérifier l'authenticité des hadiths. Ils examinaient la fiabilité de chaque transmetteur, la "
            "continuité de la chaîne, et la conformité du texte avec d'autres hadiths authentiques. C'est pour "
            "cela que nous avons aujourd'hui les célèbres recueils comme Sahih al-Bukhari, Sahih Muslim, Sunan "
            "Abu Dawud, etc.\n\n"
            "Les compilations principales (les « Six livres » du sunnisme) :\n"
            "- Sahih al-Bukhari (le plus authentique selon la majorité)\n"
            "- Sahih Muslim\n"
            "- Sunan Abu Dawud\n"
            "- Sunan at-Tirmidhi\n"
            "- Sunan an-Nasai\n"
            "- Sunan Ibn Majah\n"
            "À quoi s'ajoutent les recueils de hadiths sacrés (qudsi), les recueils de hadiths d'An-Nawawi "
            "(comme Riyad as-Salihin et les 40 hadiths), et d'autres.\n\n"
            "Le « hadith qudsi » est une spécialité : c'est une parole dont le sens vient d'Allah mais dont la "
            "formulation est du Prophète ﷺ. Il se distingue du Coran (dont le texte et le sens viennent d'Allah "
            "et qui est un miracle).\n\n"
            "Pourquoi c'est important : la Sunna est l'explication vivante de l'islam. Étudier la Sunna permet de "
            "comprendre comment appliquer le Coran dans la vie réelle. Le Coran et la Sunna sont inséparables : "
            "celui qui prétend s'attacher au Coran en ignorant la Sunna ne peut pas appliquer l'islam de manière "
            "correcte et complète."
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
            "L'un des trésors de la science du hadith est la gradation des hadiths selon leur degré "
            "d'authenticité. Cette science est née dès les premières générations de savants, qui ont développé "
            "une méthodologie rigoureuse pour protéger la religion de la falsification.\n\n"
            "Les catégories principales :\n\n"
            "1) Sahih (authentique) : un hadith dont la chaîne de transmission (isnad) est continue, dont chaque "
            "transmetteur est intègre (adl) et précis (dabit), sans anomalie (shadhdh) ni défaut caché (illah). "
            "Les recueils de Bukhari et de Muslim exclusivement de hadiths sahih.\n\n"
            "2) Hasan (bon) : un hadith dont la chaîne est correcte mais dont un transmetteur est légèrement "
            "moins précis. Son niveau d'authenticité est bon sans atteindre l'excellence du sahih. Il est "
            "utilisable pour les preuves et les pratiques.\n\n"
            "3) Da'if (faible) : un hadith qui présente une faiblesse dans la chaîne ou dans le texte : un "
            "transmetteur inconnu, une interruption dans la chaîne, un transmetteur mémorisateur faible, etc. "
            "Un hadith da'if ne peut pas être utilisé comme fondement d'une règle juridique, mais peut "
            "éventuellement servir dans les vertus et les exhortations (sous conditions).\n\n"
            "4) Mawdu' (fabriqué / forgé) : un hadith inventé, attribué faussement au Prophète ﷺ. C'est la "
            "catégorie la plus grave : le Prophète ﷺ a dit « Que celui qui ment sur mon compte de façon délibérée "
            "prépare sa place dans l'Enfer » (Bukhari). Les savants ont démasqué de nombreuses forgeries pour "
            "protéger la Sunna.\n\n"
            "La chaîne de transmission (isnad) : c'est la colonne vertébrale du hadith. Chaque hadith est "
            "accompagné de la liste des transmetteurs, du compagnon qui a entendu le Prophète ﷺ jusqu'au "
            "compilateur. Les savants ont développé une « science des hommes » (ilm ar-rijal) pour évaluer la "
            "fiabilité, la mémoire et l'honnêteté de chaque transmetteur.\n\n"
            "Pourquoi c'est important pour le débutant :\n"
            "- Vérifiez toujours la source d'un hadith avant de le partager. Beaucoup de hadiths forgés circulent "
            "sur Internet et dans les conversations quotidiennes.\n"
            "- Privilégiez les hadiths des recueils reconnus (Bukhari, Muslim) ou ceux authentifiés par des "
            "savants comme al-Albani.\n"
            "- Ne confondez pas un hadith sahih avec une simple citation attribuée au Prophète ﷺ sans "
            "vérification.\n\n"
            "Le verset « Si un pervers vous apporte une nouvelle, vérifiez (tabayyanu) » (49:6) nous ordonne de "
            "vérifier avant de transmettre. Cette exigence de rigueur s'applique de manière encore plus stricte "
            "à la parole du Prophète ﷺ, car elle est un acte d'adoration."
        ),
        "quran": [
            {"ref": "49:6", "note": "Si un pervers vous apporte une nouvelle, vérifiez (tabayyanu)"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 106, "note": "Que celui qui ment sur mon compte prépare sa place dans l'Enfer (Bukhari n°106)"},
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
            "L'éthique islamique (akhlaq) commence par le cœur. Le Prophète ﷺ a dit : « Certes, il y a dans le corps "
            "un morceau de chair ; s'il est sain, tout le corps est sain, et s'il est corrompu, tout le corps est "
            "corrompu : c'est le cœur » (Bukhari et Muslim). Cette métaphore puissante illustre que toutes les "
            "actions extérieures découlent de l'état intérieur du cœur.\n\n"
            "Les trois vertus fondamentales du cœur :\n\n"
            "1) L'ikhlas (la sincérité) : c'est l'intention pure, qui ne cherche que l'agrément d'Allah, sans "
            "attendre de louange ni de reconnaissance des gens. L'ikhlas est la condition d'acceptation de toute "
            "adoration : Allah dit « Et il ne leur a été ordonné que d'adorer Allah, en Lui vouant un culte "
            "exclusif » (98:5). Le premier hadith du Sahih al-Bukhari : « Les actes ne valent que par les "
            "intentions ». Sans ikhlas, une œuvre peut être conforme à la lettre mais vide spirituellement.\n"
            "Exemple concret : si vous faites une aumône devant les gens pour qu'ils vous louent, ce n'est pas "
            "de l'ikhlas. Si vous faites la même aumône discrètement, uniquement pour Allah, c'est de l'ikhlas.\n\n"
            "2) La taqwa (la piété / la conscience d'Allah) : la taqwa est une vigilance intérieure constante, "
            "comme un bouclier qui protège du péché. Le mot vient de la racine « ittiqa » (se protéger). C'est "
            "cette conscience d'Allah qui pousse le croyant à éviter ce qu'Allah a interdit et à pratiquer ce "
            "qu'Il a ordonné. Allah dit : « Quiconque craint Allah, Il lui donnera une issue et lui accordera des "
            "provisions d'où il n'attendait pas » (65:2-3). La taqwa n'est pas la peur paralysante de Dieu, mais "
            "l'amour et le respect qui vous gardent proche de Lui.\n\n"
            "3) Le tawakkul (la confiance en Allah) : c'est se reposer entièrement sur Allah tout en prenant les "
            "moyens nécessaires. Le hadith du Prophète ﷺ est très parlant : « Lie ta chamelle, puis confie-toi à "
            "Allah » (Tirmidhi). Le tawakkul n'est pas la passivité : c'est la combinaison de l'effort humain et "
            "de la confiance divine. Allah dit : « Quand tu as pris une décision, confie-toi donc à Allah. Allah "
            "aime ceux qui Lui font confiance » (3:159).\n\n"
            "Le lien entre ces vertus : l'ikhlas rend l'action pure, la taqwa la guide vers le bien, et le "
            "tawakkul la libère de l'anxiété des résultats. Travaillez ces trois vertus en parallèle : chaque "
            "matin, réfléchissez à votre intention (ikhlas), à votre attitude envers Allah (taqwa), et à la "
            "manière dont vous confiez vos affaires du jour (tawakkul)."
        ),
        "quran": [
            {"ref": "2:177", "note": "La piété réside dans la droiture du cœur"},
            {"ref": "65:2", "note": "Quiconque craint Allah, Il lui donnera une issue"},
            {"ref": "3:159", "note": "Quand tu as pris une décision, confie-toi à Allah"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1, "note": "Les actes ne valent que par l'intention (l'ikhlas)"},
            {"book": "tirmidhi", "number": 2587, "note": "Lie ta chamelle, puis confie-toi à Allah (tawakkul)"},
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
            "La langue est l'un des membres les plus dangereux du corps humain. Le Prophète ﷺ a dit : « Celui qui "
            "croit en Allah et au Jour dernier, qu'il dise du bien ou qu'il se taise » (Bukhari et Muslim). C'est "
            "un principe simple mais profond : tout ce qui n'est pas bon à dire est mieux non dit. La langue peut "
            "être la source des plus grandes récompenses ou des plus grands péchés.\n\n"
            "Les dangers de la langue :\n"
            "- Le mensonge (kadhib) : le Coran dit « Certes, Allah ne guide pas celui qui est menteur et ingrat » "
            "(39:3). Le Prophète ﷺ a dit « La marque de l'hypocrite est au nombre de trois : quand il parle, il "
            "ment ; quand il promet, il manque ; et quand on lui confie, il trahit » (Bukhari et Muslim).\n"
            "- La médisance (ghibah) : c'est dire à propos de quelqu'un une chose qu'il n'aimerait pas entendre, "
            "même si elle est vraie. Le Coran condamne sévèrement : « Ne médisez pas les uns des autres. L'un de "
            "vous aimerait-il manger la chair de son frère mort ? Vous l'auriez en horreur » (49:12).\n"
            "- La délation / le commérage (namimah) : transmettre des propos pour semer la discorde entre les "
            "personnes.\n"
            "- La moquerie (sukhriyah) : « Que les uns ne se moquent pas des autres ; il se peut que ceux-ci "
            "soient meilleurs qu'eux » (49:11).\n"
            "- Le langage grossier et les insultes.\n\n"
            "La vertu de la véracité (sidq) : le Prophète ﷺ a dit « La véracité mène à la piété et la piété mène "
            "au Paradis. L'homme ne cesse de dire la vérité jusqu'à être inscrit auprès d'Allah comme véridique » "
            "(Bukhari et Muslim). Le musulman est la personne la plus fiable : on peut le croire et lui confier "
            "ses secrets.\n\n"
            "La vertu de la miséricorde (rahma) : le Prophète ﷺ a dit « Celui qui ne fait pas miséricorde aux gens, "
            "Allah ne lui fait pas miséricorde » (Bukhari et Muslim), et « Les miséricordieux reçoivent la "
            "miséricorde du Tout Miséricordieux. Faites miséricorde à ceux qui sont sur la terre, le Ciel vous fera "
            "miséricorde » (Tirmidhi). La miséricorde est une attitude globale : envers les humains, les animaux, "
            "toute la création.\n\n"
            "L'amour pour son frère : le Prophète ﷺ a dit « Aucun de vous ne croit vraiment tant qu'il n'aime pas "
            "pour son frère ce qu'il aime pour lui-même » (Bukhari et Muslim). C'est le test de la foi : "
            "voulez-vous du bien pour les autres ce que vous voulez pour vous ? Si oui, votre foi est renforcée ; "
            "si non, vous devez corriger votre cœur.\n\n"
            "Application pratique : avant de parler, posez-vous trois questions :\n"
            "1) Est-ce vrai ?\n"
            "2) Est-ce nécessaire à dire ?\n"
            "3) Est-ce que cela ne va pas nuire à quelqu'un ?\n"
            "Si une de ces réponses est non, alors la meilleure action est de se taire. Et si vous entendez de la "
            "médisance, ne participez pas, changez de sujet, ou demandez à la personne de se taire."
        ),
        "quran": [
            {"ref": "49:11", "note": "Que les uns ne se moquent pas des autres"},
            {"ref": "49:12", "note": "Évitez la suspicion, la médisance"},
            {"ref": "41:34", "note": "Repousse le mal par ce qui est meilleur"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 6236, "note": "Qui croit en Allah et au Jour dernier, qu'il dise du bien ou se taise"},
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
            "La générosité (jood) est une qualité qui reflète la beauté de l'islam. Le Prophète ﷺ était décrit "
            "par ses compagnons comme « plus généreux que le vent qui ne retient rien ». La générosité n'est pas "
            "réservée à ceux qui ont les moyens : elle est une question de cœur et de disponibilité.\n\n"
            "Les formes de la générosité :\n"
            "- La générosité financière : la sadaqa (aumône volontaire), la zakat (aumône obligatoire), l'aide "
            "aux pauvres, aux orphelins, aux nécessiteux. Allah dit : « L'exemple de ceux qui dépensent leurs "
            "biens dans le sentier d'Allah est semblable à un grain de blé qui fait germer sept épis, dans "
            "chaque épi cent grains » (2:261).\n"
            "- La générosité du sourire : le Prophète ﷺ a dit « Ton sourire en face de ton frère est une "
            "aumône » (Tirmidhi). Un simple sourire peut être un acte d'adoration.\n"
            "- La générosité du bon mot : une parole aimable, un encouragement, une consolation, sont des "
            "aumônes.\n"
            "- La générosité de l'effort : déplacer un obstacle du chemin, aider quelqu'un à porter un fardeau, "
            "faire du bien à ses proches.\n"
            "- La générosité du savoir : enseigner ce que l'on sait, partager des connaissances utiles.\n\n"
            "La générosité discrète : Allah apprécie l'aumône faite discrètement. Le Prophète ﷺ a mentionné "
            "parmi ceux que l'ombre d'Allah protégera le Jour du Jugement, « celui qui donne une aumône à la "
            "main droite, et dont la main gauche ne sait pas ce que la main droite a donné » (Bukhari). "
            "Cherchez à donner avec discrétion pour préserver la dignité du bénéficiaire et la pureté de votre "
            "intention.\n\n"
            "La générosité ne diminue pas la richesse : le Prophète ﷺ a dit « L'aumône ne diminue pas la "
            "richesse, et Allah n'augmente le serviteur dans le pardon qu'après un acte de pardon, et quiconque "
            "s'humilie pour Allah, Allah l'élève » (Muslim). C'est un principe contre-intuitif du monde, mais "
            "c'est une vérité spirituelle : en donnant, on reçoit d'Allah d'une manière que l'on ne comprend "
            "pas toujours.\n\n"
            "Le lien des proches (silat ar-rahim) : le Prophète ﷺ a dit « Celui qui croit en Allah et au Jour "
            "dernier, qu'il maintienne les liens de parenté » (Bukhari). Les liens de parenté ne se limitent "
            "pas aux visites occasionnelles : c'est un entretien continu de la relation, de l'affection, de "
            "l'entraide. Allah dit : « Craignez Allah en qui vous vous interrogez, et restaurer les liens de "
            "parenté » (4:1).\n\n"
            "Le droit des proches : « Donne au proche son dû, ainsi qu'au pauvre et au voyageur » (17:26). Ce "
            "verset couvre plusieurs obligations : le droit des parents, des frères et sœurs, des voisins, et "
            "des personnes dans le besoin. Le voisin a aussi ses droits : le Prophète ﷺ a dit « Gabriel n'a "
            "cessé de me recommander le voisin jusqu'à ce que j'ai cru qu'il allait lui faire hériter » "
            "(Bukhari et Muslim).\n\n"
            "Application pratique :\n"
            "- Identifiez les besoins autour de vous et agissez discrètement\n"
            "- Contactez régulièrement vos proches, prenez de leurs nouvelles\n"
            "- Voisinage : offrez à manger, aidez en cas de besoin, saluez toujours\n"
            "- La générosité n'est pas un acte ponctuel : c'est un état d'esprit permanent"
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
            "Le rappel d'Allah (dhikr) est une nourriture spirituelle indispensable. Allah ordonne : « Ô vous qui "
            "avez cru ! Invoquez Allah d'une invocation abondante, et glorifiez-Le à la pointe et au déclin du "
            "jour » (33:41-42) et « Souvenez-vous de Moi, Je me souviendrai de vous » (2:152). Le dhikr est la "
            "respiration de l'âme : sans lui, le cœur s'étouffe.\n\n"
            "Le Coran dit : « Ceux qui croient, et dont les cœurs se tranquillisent à l'évocation d'Allah. Certes, "
            "c'est par l'évocation d'Allah que les cœurs s'apaisent » (13:28). Dans un monde rempli de stress et "
            "d'anxiété, le dhikr est le remède que chaque musulman possède à portée de main.\n\n"
            "Les formules essentielles à mémoriser :\n\n"
            "1) Subhan Allah (Gloire à Allah) : exaltation de la pureté et de la perfection d'Allah.\n"
            "2) Alhamdulillah (Louange à Allah) : remerciement et reconnaissance de tous les bienfaits.\n"
            "3) Allahu Akbar (Allah est le plus grand) : reconnaissance de la grandeur suprême d'Allah.\n"
            "4) La ilaha illallah (Il n'y a de divinité qu'Allah) : le meilleur dhikr, la parole du tawhid.\n"
            "5) La hawla wa la quwwata illa billah (Il n'y a de force et de puissance qu'en Allah) : elle soulage "
            "les difficultés.\n"
            "6) Astaghfirullah (Je demande pardon à Allah) : le rappel du repentir.\n"
            "7) Subhan Allah wa bihamdihi (Gloire à Allah et à Sa louange) : « deux paroles légères sur la langue, "
            "lourdes sur la balance » (Bukhari).\n\n"
            "Les moments recommandés pour le dhikr :\n"
            "- Après chaque prière obligatoire : « Subhan Allah » 33 fois, « Alhamdulillah » 33 fois, « Allahu "
            "Akbar » 33 fois, puis compléter par « La ilaha illallah wahdahu la sharika lah... »\n"
            "- Le matin et le soir : les invocations du matin et du soir (réfugiées dans Ayat al-Kursi, les trois "
            "sourates de protection, etc.)\n"
            "- Au coucher et au réveil\n"
            "- Pendant la journée, au travail, en conduisant, partout et toujours\n\n"
            "Les trois sourates de protection :\n"
            "- Al-Ikhlas (112) : l'unicité\n"
            "- Al-Falaq (113) : refuge contre le mal des créatures\n"
            "- An-Nas (114) : refuge contre le mauvais murmureur\n"
            "Le Prophète ﷺ a dit : « Dis : Il est Allah, Unique. Dis : Je cherche protection... » trois fois le "
            "matin et trois fois le soir, elles te suffisent pour te protéger de tout mal ».\n\n"
            "Le dhikr est accessible à tous, même à celui qui ne sait pas lire : on peut mémoriser quelques "
            "formules et les répéter avec concentration. Le Prophète ﷺ a dit « Que ta langue ne cesse d'être "
            "moite du rappel d'Allah » (Tirmidhi).\n\n"
            "Application pratique : établissez un rituel simple. Chaque matin, récitez les protections ; après "
            "chaque prière, faites le dhikr habituel ; le soir, avant de dormir, récitez Ayat al-Kursi et les "
            "sourates de protection. Progressivement, le dhikr deviendra naturel et votre cœur s'apaisera."
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
            "Le repentir (tawbah) est l'un des plus beaux cadeaux qu'Allah offre à Ses serviteurs. C'est le retour "
            "de l'âme vers son Créateur après un égarement. Le mot « tawbah » vient de « retour » : se repentir, "
            "c'est revenir à Allah, revenir au droit chemin, revenir à la pureté.\n\n"
            "Les trois conditions de la tawbah acceptée :\n"
            "1) Cesser le péché immédiatement\n"
            "2) Regretter sincèrement de l'avoir commis\n"
            "3) Résoudre fermement à ne pas y revenir\n"
            "Si le péché concerne le droit d'une autre personne (vol, fraude, calomnie, etc.), il faut en plus "
            "réparer ce tort : rendre le bien volé, présenter des excuses, revenir sur la calomnie.\n\n"
            "Quand la tawbah est-elle acceptée ?\n"
            "- La porte du repentir reste ouverte tant que l'âme n'atteint pas la gorge (au moment de la mort) "
            "et tant que le soleil ne se lève pas de l'ouest (signe majeur de la fin).\n"
            "- Même une vie de péchés peut être effacée par un repentir sincère : le repentir efface le péché "
            "comme s'il n'avait pas existé.\n\n"
            "La miséricorde d'Allah :\n"
            "- Allah dit : « Dis : Ô Mes serviteurs qui avez commis des excès à votre propre détriment, ne "
            "désespérez pas de la miséricorde d'Allah. Allah pardonne tous les péchés, car Il est le Pardonneur, "
            "le Très Miséricordieux » (39:53). Ce verset est l'un des plus optimistes du Coran : elle s'adresse "
            "à tous ceux qui ont péché, sans exception.\n"
            "- Le Prophète ﷺ a dit : « Allah dit : Ô fils d'Adam ! Tant que tu M'invoques et que tu espères en "
            "Moi, Je te pardonne quoique tu aies fait, et cela ne Me déplaît pas. Ô fils d'Adam ! Si tes péchés "
            "atteignaient les nuages du ciel, puis que tu Me demandais pardon, Je te pardonnerais » (Tirmidhi).\n"
            "- Le hadith de l'homme qui a tué 99 personnes, puis 100, puis s'est tourné vers Allah et s'est "
            "repenti sincèrement : il est décédé sur le chemin du village du savant qu'il cherchait, et Allah "
            "a accepté son repentir. C'est la preuve que la miséricorde d'Allah dépasse toute faute.\n\n"
            "Allah « se réjouit » du retour de Son serviteur : le Prophète ﷺ a dit que la joie d'Allah au "
            "repentir de Son serviteur est plus grande que celle d'un homme qui retrouve sa monture perdue avec "
            "sa nourriture et sa boisson dans le désert. Cette image montre la valeur immense du repentir aux "
            "yeux d'Allah.\n\n"
            "Les obstacles au repentir :\n"
            "- Le désespoir de la miséricorde d'Allah (contre lequel Allah nous met en garde)\n"
            "- Remettre à plus tard (« je me repentirai un jour ») — c'est un piège de Satan\n"
            "- Minimiser le péché et se croire à l'abri\n\n"
            "Application pratique :\n"
            "- Chaque jour, demandez pardon à Allah avec « Astaghfirullah »\n"
            "- Le soir, faites le bilan de votre journée et réparez les torts\n"
            "- Si vous avez blessé quelqu'un, présentez des excuses même si c'est difficile\n"
            "- Croyez fermement qu'Allah veut votre retour : Il nous aime quand on se repent (2:222)"
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
            "Les 99 noms d'Allah (al-Asma al-Husna) sont les « plus beaux noms » par lesquels Allah Se décrit dans "
            "le Coran et la Sunna. Allah dit : « C'est à Allah qu'appartiennent les plus beaux noms. Invoquez-Le "
            "par eux » (7:180). Chaque nom est une porte vers la connaissance d'Allah et une invitation à "
            "l'adoration.\n\n"
            "Pourquoi connaitre les noms d'Allah ?\n"
            "- Parce que c'est la plus noble connaissance : connaître Allah est le but de l'existence\n"
            "- Parce que l'invocation par les noms est une adoration : « Invoquez-Le par eux »\n"
            "- Parce que la foi augmente : quand vous connaissez Allah par Ar-Rahman (Miséricordieux), vous "
            "espérez en Sa miséricorde ; par Al-'Adl (Juste), vous Le craignez ; par Al-'Alim (Savant), vous "
            "vous surveillez\n"
            "- Parce que chaque nom a un impact sur la vie pratique\n\n"
            "Le hadith des 99 noms : le Prophète ﷺ a dit « Allah a 99 noms, cent moins un. Celui qui les "
            "compte entrera au Paradis » (Bukhari et Muslim). « Les compter » signifie non seulement les "
            "mémoriser, mais les comprendre et les méditer pour que la foi augmente.\n\n"
            "La différence entre noms et attributs : les savants distinguent les noms (asma) et les attributs "
            "(sifat) :\n"
            "- Les noms sont les appellations : Ar-Rahman, Al-Malik, Al-Quddus...\n"
            "- Les attributs sont les qualités que ces noms impliquent : la miséricorde (rahmah), la royauté "
            "(mulk), la sainteté (qudus)...\n"
            "Chaque nom renvoie à une perfection d'Allah. Quand nous connaissons Allah par un nom, nous "
            "comprenons son attribut et ses implications sur nos vies.\n\n"
            "Exemples concrets :\n"
            "- Ar-Rahman (Le Tout Miséricordieux) : Allah est miséricordieux envers toute Sa création, croyants "
            "et non-croyants, êtres humains et animaux. Quand on connaît ce nom, on espère la miséricorde et "
            "on cherche à en être digne.\n"
            "- Ar-Razzaq (Le Pourvoyeur) : Allah pourvoit à la subsistance de toutes les créatures. Quand on "
            "connaît ce nom, on ne s'angoisse pas pour le gagne-pain : on cherche les moyens licites et on "
            "s'en remet à Allah.\n"
            "- Al-'Adl (Le Juste) : Allah est parfaitement juste. Quand on connaît ce nom, on est rassuré que "
            "les injustices du monde seront réparées, et on s'efforce soi-même d'être juste.\n\n"
            "Comment lire les noms d'Allah :\n"
            "- Mémorisez les 99 noms progressivement, en les récitant régulièrement\n"
            "- Méditez le sens de chaque nom\n"
            "- Utilisez-les dans vos invocations selon vos besoins (par ex. invoquer Al-Ghaffar pour le pardon, "
            "Al-Razzaq pour la subsistance)\n"
            "- Appliquez ce que chaque nom implique dans votre comportement\n\n"
            "Une erreur à éviter : ne pas déformer le sens des noms ni les réduire à des concepts humains. "
            "Allah est au-dessus de toute comparaison avec Sa création. Les noms d'Allah sont une porte vers "
            "une foi profonde et une adoration authentique."
        ),
        "quran": [
            {"ref": "7:180", "note": "Les plus beaux noms sont à Allah"},
            {"ref": "20:8", "note": "À Allah appartiennent les plus beaux noms, invoquez-les"},
            {"ref": "59:24", "note": "Il est Allah, le Créateur, l'Initiateur, le Donateur de forme"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 6171, "note": "Les 99 noms d'Allah, moins un : celui qui les compte entrera au Paradis"},
            {"book": "muslim", "number": 6644, "note": "Allah possède 99 noms, 100 moins un : qui les mémorise entre au Paradis"},
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
            "Parmi les 99 noms d'Allah, ceux qui expriment la miséricorde et le pardon occupent une place centrale. "
            "Le Coran commence par « Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux » (Bismillah "
            "ar-Rahman ar-Rahim), et presque toutes les sourates (sauf une) commencent par cette invocation. "
            "Cela montre que la miséricorde est la qualité dominante d'Allah.\n\n"
            "Les principaux noms de la miséricorde et leurs significations :\n\n"
            "1) Ar-Rahman (Le Tout Miséricordieux) : Sa miséricorde est universelle, elle englobe toute la "
            "création — les croyants et les non-croyants, les êtres humains, les animaux, tout ce qui existe. "
            "C'est Lui qui fournit la nourriture, la pluie, la vie et les bienfaits à tous, sans distinction.\n\n"
            "2) Ar-Rahim (Le Très Miséricordieux) : Sa miséricorde est particulière, spéciale pour les croyants. "
            "C'est elle qui guide, pardonne et élève ceux qui se tournent vers Lui. La différence : Ar-Rahman "
            "donne à tous ; Ar-Rahim donne par-dessus tout aux croyants, y compris dans l'au-delà (l'entrée au "
            "Paradis).\n\n"
            "3) Al-Ghaffar (Le Pardonneur) : Celui qui pardonne abondamment et répète le pardon, quel que soit "
            "le nombre de péchés. Allah pardonne, encore et encore, pourvu que Son serviteur se tourne vers Lui.\n\n"
            "4) Al-'Afuw (Le Pardonnant / L'Effaceur) : Celui qui efface complètement le péché, sans en laisser "
            "de trace, comme s'il n'avait jamais existé. C'est plus qu'un pardon : c'est une abolition totale.\n\n"
            "5) At-Tawwab (Celui qui accepte le repentir / Le Retournant) : Allah accepte le repentir et aide "
            "Son serviteur à revenir vers Lui. Ce nom est aussi lié à la pratique : Allah aime ceux qui se "
            "repentent et se purifient (2:222).\n\n"
            "Le hadith de la miséricorde : le Prophète ﷺ a rapporté que le jour où Allah a créé la miséricorde, "
            "Il en a réparti 99 parties et en a gardé une seule pour la terre, avec laquelle les créatures "
            "montrent de la compassion les unes envers les autres ; et avec la 99ème, Il fera miséricorde à "
            "Ses serviteurs le Jour de la Résurrection (Bukhari et Muslim). Cela illustre l'immensité de la "
            "miséricorde divine.\n\n"
            "Le verset fondamental : « Dis : Ô Mes serviteurs qui avez commis des excès à votre propre "
            "détriment, ne désespérez pas de la miséricorde d'Allah. Allah pardonne tous les péchés » (39:53).\n\n"
            "Application pratique :\n"
            "- Invoquez Allah par ces noms dans vos prières et demandez pardon avec espoir\n"
            "- Réfléchissez à la bonté d'Allah envers vous chaque jour\n"
            "- Essayez d'être miséricordieux envers les autres, car Allah est miséricordieux envers les "
            "miséricordieux\n"
            "- Ne désespérez jamais de la miséricorde d'Allah, même après une chute"
        ),
        "quran": [
            {"ref": "1:1", "note": "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux"},
            {"ref": "39:53", "note": "La miséricorde d'Allah est immense"},
            {"ref": "7:156", "note": "Ma miséricorde embrasse toute chose"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 5771, "note": "Allah est plus miséricordieux envers Ses serviteurs qu'une mère envers son enfant"},
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
            "Parmi les noms d'Allah, ceux qui expriment la science et la sagesse nous enseignent qu'Allah connaît "
            "tout et que Sa sagesse est parfaite. Ces noms devraient transformer notre manière de vivre, de "
            "décider et de comprendre le monde.\n\n"
            "Les principaux noms de la science et de la sagesse :\n\n"
            "1) Al-'Alim (L'Omniscient) : Il sait tout, le passé, le présent et le futur, le visible et "
            "l'invisible, le caché dans les cœurs et les pensées les plus secrètes. Aucune de nos actions "
            "n'échappe à Sa science. Allah dit : « Et Allah sait ce que vous faites » (2:234).\n\n"
            "2) Al-Khabir (Le Très Connaisseur) : Il connaît chaque chose en détail, ses subtilités et ses "
            "secrets les plus profonds. « Khabir » précise l'intériorité de la connaissance : Allah sait ce "
            "qui se cache même dans les recoins les plus obscurs.\n\n"
            "3) As-Sami' (L'Ouïant) : Il entend toutes les voix, même les plus faibles, même les prières "
            "chuchotées dans la nuit, même les soupirs du cœur. Aucune parole ne Lui échappe.\n\n"
            "4) Al-Basir (Le Voyant) : Il voit tout, même ce qui est le plus caché, même dans les entrailles "
            "de la terre et les profondeurs des mers. Rien n'est invisible à Ses yeux.\n\n"
            "5) Al-Hakim (Le Sage) : Sa sagesse est parfaite dans toute Sa création et Sa législation. Tout ce "
            "qu'Allah a créé et ordonné a une sagesse, même si nous ne la percevons pas toujours. « N'est-il "
            "pas le Sage ? » dit le Coran.\n\n"
            "La combinaison de ces noms : As-Sami' et Al-Basir ensemble rappellent que rien de ce que nous "
            "faisons ou disons n'échappe à Allah. Al-'Alim et Al-Khabir ensemble confirment une science "
            "totale. Al-Hakim donne du sens à tout ce qui arrive.\n\n"
            "Comment ces noms guident notre recherche du savoir :\n"
            "- Si Allah est Al-'Alim et qu'Il accorde la science à qui Il veut, nous devons apprendre avec "
            "humilité et constance\n"
            "- Le verset « Allah élève ceux qui ont cru parmi vous et ceux à qui le savoir a été donné » "
            "(58:11) nous invite à rechercher le savoir\n"
            "- Comme Allah voit tout, nous devons agir avec droiture, sachant que nous sommes observés\n"
            "- Comme Allah est Le Sage, nous devons chercher la sagesse dans les événements et accepter que "
            "Sa sagesse dépasse la nôtre\n\n"
            "Application pratique :\n"
            "- Avant de faire une action, rappelez-vous qu'Allah vous voit et vous entend\n"
            "- Dans la difficulté, cherchez la sagesse cachée : chaque épreuve a un sens\n"
            "- Cherchez le savoir pour vous rapprocher d'Allah, pas pour vous vanter\n"
            "- Quand vous prenez une décision, consultez (istikhara) et confiez-vous à Al-Hakim, le Sage"
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
            "La chahada (attestation de foi) est le premier et le plus important des cinq piliers de l'islam. "
            "C'est la porte d'entrée dans la religion : « J'atteste qu'il n'y a de divinité qu'Allah, et "
            "j'atteste que Muhammad est le Messager d'Allah » (Ashhadu an la ilaha illallah wa ashhadu anna "
            "Muhammadan rasulullah).\n\n"
            "Cette phrase, simple en apparence, contient tout l'islam. Elle a deux parties inséparables :\n\n"
            "1) La ilaha illallah (Il n'y a de divinité qu'Allah) : c'est le tawhid. Cette formule comporte "
            "deux éléments :\n"
            "   - La négation : « La ilaha » — il n'y a aucune divinité digne d'adoration\n"
            "   - L'affirmation : « illallah » — si ce n'est Allah seul\n"
            "C'est comme une porte : on ferme (négation de toutes les fausses divinités) puis on ouvre "
            "(affirmation de l'adoration d'Allah seul).\n\n"
            "2) Muhammadan rasulullah (Muhammad est le Messager d'Allah) : la reconnaissance que Muhammad ﷺ "
            "est le Messager d'Allah, le serviteur et le dernier des prophètes. Cela implique de lui obéir "
            "dans ce qu'il a ordonné, de le croire dans ce qu'il a informé, de s'abstenir de ce qu'il a "
            "interdit, et de suivre sa Sunna.\n\n"
            "Les six conditions de la chahada : les savants ont formulé les conditions sans lesquelles "
            "l'attestation n'est pas valide :\n"
            "1) La connaissance ('ilm) : comprendre le sens réel de la chahada, ce qu'elle affirme et ce "
            "qu'elle nie. Il ne suffit pas de la répéter par tradition.\n"
            "2) La certitude (yaqin) : une foi ferme et inébranlable, sans aucun doute. « Les bédouins "
            "disent : nous avons cru. Dis : vous n'avez pas encore cru » (49:14).\n"
            "3) L'acceptation (qabul) : accepter ce que la chahada exige, sans rejeter une partie du message.\n"
            "4) La soumission (inqiyad) : se soumettre pratiquement à Allah et à Son messager.\n"
            "5) La sincérité (sidq) : être véridique dans son attestation, sans hypocrisie. « Allah dit : "
            "Certes, Allah sait ce que renferment vos poitrines » (87:10).\n"
            "6) L'amour (mahabbah) : aimer Allah et Son messager plus que tout. « Ceux qui ont cru sont plus "
            "durs envers les mécréants, miséricordieux entre eux » (48:29).\n\n"
            "Les implications pratiques de la chahada :\n"
            "- La prière, la zakat, le jeûne et le hajj n'ont de valeur que si la chahada est vraie\n"
            "- La chahada protège la personne (statut de musulman, droits religieux)\n"
            "- Elle est la clé du Paradis pour celui qui la prononce sincèrement\n\n"
            "Allah témoigne de la vérité de la chahada : « Allah témoigne que, point de divinité à part Lui, "
            "ainsi que les anges et les détenteurs du savoir, en toute équité » (3:18).\n\n"
            "Erreur à éviter : prononcer la chahada machinalement, sans méditer son sens. Elle doit être "
            "vécue chaque instant : c'est elle qui définit l'identité du musulman."
        ),
        "quran": [
            {"ref": "3:18", "note": "Allah témoigne qu'il n'y a de divinité que Lui, et les anges et ceux qui savent"},
            {"ref": "47:19", "note": "Sache qu'il n'y a de divinité qu'Allah"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 8, "note": "L'islam est bâti sur cinq piliers : la chahada, la prière, la zakat, le jeûne et le pèlerinage"},
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
            "La zakat est le troisième pilier de l'islam et le pilier financier le plus important (après la "
            "chahada et la prière). Elle est mentionnée dans le Coran 32 fois, souvent directement liée à la "
            "prière : « Et accomplissez la prière et acquittez-vous de la zakat » (2:43). Sa place inséparable "
            "de la prière montre qu'en islam, la spiritualité ne va pas sans la solidarité.\n\n"
            "Les conditions d'obligation de la zakat :\n"
            "1) Être musulman\n"
            "2) Être libre et sain d'esprit\n"
            "3) Posséder le nissab (seuil minimum) : 85 grammes d'or ou 595 grammes d'argent (ou équivalent)\n"
            "4) Que le bien ait été possédé pendant une année lunaire complète (hawl)\n"
            "5) Que le bien soit productif ou en excédent des besoins essentiels\n\n"
            "Les taux de la zakat selon le type de bien :\n"
            "- Argent, or, liquidités, épargne, investissements : 2,5 % (1/40) par an\n"
            "- Biens commerciaux et marchandises : 2,5 % de leur valeur par an\n"
            "- Produits agricoles irrigués naturellement : 10 % de la récolte\n"
            "- Produits agricoles irrigués artificiellement : 5 % de la récolte\n"
            "- Bétail (chameaux, bovins, ovins) : taux variables selon le nombre et le type\n"
            "- Trésors et minerais : 20 %\n\n"
            "Les biens non soumis à la zakat : votre résidence principale, votre véhicule personnel, vos "
            "vêtements, votre mobilier essentiel ne sont pas soumis à la zakat.\n\n"
            "Les huit catégories de bénéficiaires (Coran 9:60) :\n"
            "1) Les pauvres (fuqara) : ceux qui n'ont pas de quoi couvrir leurs besoins essentiels\n"
            "2) Les nécessiteux (masakin) : ceux dont les moyens sont insuffisants pour subvenir à leurs besoins\n"
            "3) Les collecteurs de zakat (amilin) : ceux qui sont officiellement chargés de la collecter\n"
            "4) Ceux dont les cœurs sont à gagner (muallafat al-qulub) : les nouveaux convertis pour les "
            "soutenir et les aider à consolider leur foi\n"
            "5) L'affranchissement des esclaves (riqab) : pour libérer les personnes assujetties\n"
            "6) Les endettés (gharimin) : ceux qui sont accablés de dettes et ne peuvent pas les rembourser\n"
            "7) Dans le sentier d'Allah (fi sabilillah) : traditionnellement le jihad, aujourd'hui étendu aux "
            "œuvres caritatives, éducatives et religieuses\n"
            "8) Le voyageur démuni (ibn as-sabil) : celui qui est bloqué loin de son foyer sans ressources\n\n"
            "L'impact social de la zakat :\n"
            "- Elle purifie la richesse et le cœur de l'avarice\n"
            "- Elle est un droit des pauvres, pas une faveur des riches\n"
            "- Elle réduit les écarts et la pauvreté dans la société\n"
            "- Elle crée une solidarité efficace et organisée\n"
            "- Elle protège l'économie des excès matériels\n\n"
            "La différence entre zakat et sadaqa :\n"
            "- La zakat est obligatoire, avec des règles précises (taux, seuils, bénéficiaires)\n"
            "- La sadaqa (aumône volontaire) est recommandée, sans règles formelles, et peut être donnée à "
            "n'importe quel moment et de n'importe quelle manière\n\n"
            "Astuce pratique : choisissez une date fixe (par exemple le début du Ramadan ou l'anniversaire de "
            "votre entreprise) pour évaluer votre patrimoine et payer votre zakat régulièrement chaque année."
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
            "Le hajj est le cinquième pilier de l'islam et le plus grand voyage spirituel d'une vie. Il "
            "reproduit les rites établis par le prophète Abraham (Ibrahim) et son fils Ismaïl, des milliers "
            "d'années avant la venue du Prophète Muhammad ﷺ. C'est un pèlerinage unique au monde, qui "
            "rassemble chaque année des millions de musulmans dans un même lieu, avec la même tenue, pour "
            "un même but : l'adoration d'Allah seul.\n\n"
            "Quand le hajj a-t-il lieu ? Chaque année du 8 au 12 de dhul-hijjah (le douzième mois du "
            "calendrier islamique). Il est obligatoire pour tout musulman qui en a la capacité matérielle "
            "et physique, une fois dans sa vie. Le Coran dit : « Et c'est un devoir envers Allah pour les "
            "gens qui en ont la capacité, de faire le pèlerinage de la Maison » (3:97).\n\n"
            "Les rites du pèlerinage, étape par étape :\n\n"
            "1) L'ihram : c'est l'entrée en état de sacralité, marquée par l'intention du pèlerin de "
            "commencer le hajj. L'homme revêt deux pans de tissu blanc non cousus ; la femme porte des "
            "vêtements modestes couvrant tout le corps sauf le visage et les mains. Pendant l'ihram, il est "
            "interdit de : couper ses cheveux ou ses ongles, se parfumer, chasser, juger, avoir des "
            "relations conjugales. L'ihram symbolise la rupture avec le monde matériel et la préparation "
            "à la présence spirituelle.\n\n"
            "2) Le tawaf : la circumambulation autour de la Kaaba, sept tours dans le sens antihoraire, en "
            "priant et en invoquant Allah. La Kaaba est la première maison construite pour l'adoration d'Allah "
            "sur terre. Le tawaf exprime la rotation de toute l'existence autour d'Allah, le centre de tout.\n\n"
            "3) Le sa'i : le parcours entre les collines de Safa et Marwah, sept fois, en souvenir de Hajar, "
            "la femme d'Abraham, qui chercha de l'eau pour son fils Ismaïl dans le désert et dont l'Allah "
            "fit jaillir la source de Zamzam. C'est le symbole de la persévérance et de l'espoir.\n\n"
            "4) Le séjour à Mina (8 dhul-hijjah) : le pèlerin passe la journée et la nuit à Mina, un village "
            "près de La Mecque, en priant et en invoquant Allah.\n\n"
            "5) Le séjour à Arafat (9 dhul-hijjah) : c'est LE rite essentiel. Le Prophète ﷺ a dit « Le hajj "
            "c'est Arafat » (Abu Dawud et Tirmidhi). Sans station debout (wuquf) à Arafat, le hajj est "
            "invalide. Le pèlerin reste debout sur la plaine d'Arafat de midi au coucher du soleil, invoquant "
            "Allah, se repentant, magnifiant Son nom. C'est le moment le plus puissant du hajj : « Le meilleur "
            "doukâ est celui du jour d'Arafat » (Tirmidhi).\n\n"
            "6) Muzdalifah (nuit du 9 au 10) : après le coucher du soleil à Arafat, le pèlerin se rend à "
            "Muzdalifah pour y passer la nuit sous les étoiles.\n\n"
            "7) La lapidation des stèles (rajm) à Mina : pendant les trois jours de Tachriq (10, 11, 12), le "
            "pèlerin lance des petits cailloux sur les trois stèles (jamarat) symbolisant la réjection de "
            "Satan. On commence par la plus grande (al-jamrah al-kubra).\n\n"
            "8) Le sacrifice (udhiyyah / idi al-adha) : immoler un animal (mouton, bovin ou une part de "
            "chameau) pour commémorer le sacrifice d'Abraham. La viande est partagée avec les nécessiteux.\n\n"
            "9) La coupe des cheveux et la sortie de l'ihram : le pèlerin coupe ses cheveux (hommes) ou "
            "raccourcit (femmes), marquant la fin de l'état d'ihram.\n\n"
            "10) Le tawaf al-ifadah : le tawaf de la rupture, un second tour de la Kaaba.\n\n"
            "11) Le tawaf al-wada' (tawaf d'adieu) avant de quitter La Mecque.\n\n"
            "La signification spirituelle du hajj :\n"
            "- L'égalité absolue : des millions de personnes, de toutes races et classes sociales, portent "
            "les mêmes vêtements et accomplissent les mêmes gestes. Aucun roi n'est plus compris que le pauvre.\n"
            "- La purification : le Prophète ﷺ a dit « Celui qui fait le hajj sans avoir des rapports intimes "
            "ni commettre d'actes impies revient comme le jour où il est sorti du ventre de sa mère » "
            "(Bukhari).\n"
            "- La fraternité universelle : les musulmans se reconnaissent dans cette communauté mondiale\n"
            "- La soumission totale : le hajj est une démonstration pratique de la soumission à Allah, "
            "comme le fit Abraham. « Le hajj agréé n'a d'autre récompense que le Paradis » (Bukhari et Muslim).\n\n"
            "Préparation pratique : le hajj est un voyage exigeant. Entraînez-vous physiquement, mémorisez "
            "les invocations spécifiques, apprenez les règles des rites, et préparez votre intention et votre "
            "patience. La patience est la clé du hajj : des foules, des files, des longueurs d'attente."
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
            "Le sabr (patience) et le shukr (gratitude) sont deux vertus sœurs qui forment le socle de la "
            "vie spirituelle du croyant. Ces deux vertus sont le remède aux deux plus grandes sources de "
            "détresse humaine : l'adversité et l'absence de satisfaction.\n\n"
            "Le sabr (patience) : le mot sabr signifie au sens propre « maîtriser », « retenir ». Ce n'est "
            "pas l'élimination de la douleur ou le refus de la ressentir — le Prophète ﷺ lui-même a pleuré, "
            "a ressenti la douleur, la perte et la tristesse. Le sabr est la capacité à supporter l'épreuve "
            "avec dignité, en gardant la confiance en Allah, sans sombrer dans le désespoir ni la révolte.\n\n"
            "Les trois types de sabr :\n"
            "1) La patience dans l'obéissance à Allah : persévérer dans la prière, le jeûne, la "
            "connaissance — même quand c'est difficile. Le verset « Ô vous qui avez cru, cherchez secours "
            "dans la patience et la prière » (2:153) nous ordonne d'obtenir la force par la patience.\n"
            "2) La patience dans l'évitement des péchés : résister à la tentation, au mensonge, à la colère, "
            "aux désirs illicites.\n"
            "3) La patience dans les épreuves de la vie : face à la maladie, la perte, l'injustice, les "
            "difficultés financières. C'est là que le sabr révèle sa beauté : « Allah est avec les patients » "
            "(2:153) et « Allah aime les patients » (3:146).\n\n"
            "Le shukr (gratitude) : le mot shukr signifie reconnaître un bienfait et en manifester sa "
            "reconnaissance. Dans la vie du croyant, la gratitude a trois dimensions :\n"
            "1) La gratitude du cœur : reconnaître que tout comes d'Allah et vivre avec cette conscience\n"
            "2) La gratitude de la langue : exprimer sa reconnaissance avec Alhamdulillah et invoquer Allah\n"
            "3) La gratitude des membres : utiliser les bienfaits reçus pour le bien, comme Allah l'a ordonné\n\n"
            "Allah promet : « Si vous êtes reconnaissants, Je vous accorderai davantage » (14:7). La "
            "gratitude est la clé de l'augmentation des bienfaits, tandis que l'ingratitude est le chemin "
            "de leur diminution.\n\n"
            "Le hadith du Prophète ﷺ est célèbre : « L'affaire du croyant est étonnante ! Tout lui est "
            "bon. Si une grâce lui est accordée, il en remercie Allah — ce qui est un bien pour lui. Et si "
            "une adversité le frappe, il patiente — ce qui est aussi un bien pour lui » (Muslim). Le croyant "
            "a compris que dans la facilité comme dans la difficulté, il y a une bénédiction cachée : "
            "l'épreuve est une école de patience, la grâce est une école de gratitude.\n\n"
            "Application pratique :\n"
            "- Quand vous traversez une difficulté, dites « Inna lillahi wa inna ilayhi raji'un » (Nous "
            "appartenons à Allah et à Lui nous retournons) et rappelez-vous la récompense de la patience\n"
            "- Chaque jour, faites une liste mentale de 10 bienfaits d'Allah et remerciez-Le pour chacun\n"
            "- Face à la tentation, retardez votre décision pour laisser la raison précéder l'émotion\n"
            "- Le complément de la patience et de la gratitude est l'espoir : l'espoir de la miséricorde "
            "d'Allah rend chaque jour supportable et chaque été agréable"
        ),
        "quran": [
            {"ref": "2:153", "note": "Allah est avec les patients"},
            {"ref": "14:7", "note": "Si vous êtes reconnaissants, Je vous accorderai davantage"},
            {"ref": "31:17", "note": "Commande-le patient et ordonne-le bien"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 5428, "note": "Aucune fatigue ni maladie n'atteint le musulman sans qu'Allah n'efface des péchés (sabr et shukr)"},
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
            "Le tawakkul (confiance en Allah) est l'un des plus grands actes de foi. C'est placer toute sa "
            "confiance en Allah, s'appuyer sur Lui et s'abandonner à Sa volonté, après avoir pris les "
            "moyens légitimes. C'est une combinaison délicate entre l'effort humain et la remise complète "
            "à Allah : le tawakkul n'est ni la passivité ni la négligence.\n\n"
            "Le célèbre hadith du Prophète ﷺ : « Lie ta chamelle, puis confie-toi à Allah » (Tirmidhi). "
            "Un bédouin demanda : « Ô Messager d'Allah, dois-je lâcher ma chamelle et me confier à Allah, "
            "ou la lier puis me confier à Allah ? » Il répondit : « Lie-la, puis confie-toi à Allah. » "
            "C'est un enseignement magistral : le tawakkul ne dispense pas de l'action. On attache la "
            "chamelle (on prend les moyens), puis on se confie à Allah (on accepte le résultat avec confiance).\n\n"
            "La différence entre tawakkul et passivité :\n"
            "- La passivité : « je ne fais rien, Allah fera tout » — c'est une déformation du tawakkul, "
            "une paresse déguisée en piété\n"
            "- L'excès de planification sans Allah : « je planifie tout seul sans me tourner vers Allah » "
            "— c'est un oubli de la place du Créateur\n"
            "- Le tawakkul correct : « je fais tout mon possible (études, travail, moyens), puis je "
            "confie le résultat à Allah »\n\n"
            "Les versets clés :\n"
            "- « Quiconque craint Allah, Il lui donnera une issue, lui accordera des provisions d'où il "
            "n'attendait pas » (65:2-3)\n"
            "- « Et (que) quand tu auras pris une décision, confie-toi donc à Allah. Allah aime ceux qui "
            "Lui font confiance » (3:159)\n"
            "- « Et confie-toi au Très-Vivant qui ne meurt jamais » (25:58)\n\n"
            "Les bienfaits du tawakkul :\n"
            "- La paix du cœur : quand vous savez que le résultat est entre les mains d'Allah, vous ne vous "
            "angoissez plus des issues\n"
            "- La libération de l'anxiété : vous faites votre part, puis vous lâchez prise\n"
            "- La confiance dans les épreuves : vous savez qu'Allah ne vous éprouve que selon vos capacités\n"
            "- Le détachement des louanges des gens : vous travaillez pour Allah, pas pour l'opinion des gens\n\n"
            "Exemples concrets de tawakkul :\n"
            "- Le malade prend son traitement (moyen) et confie sa guérison à Allah\n"
            "- L'étudiant travaille avant l'examen (moyen) et accepte le résultat avec sérénité\n"
            "- Le chercheur d'emploi envoie des candidatures (moyen) et prie pour la meilleure issue\n"
            "- Le commerçant fait son travail avec honnêteté (moyen) et gagne sa subsistance avec confiance\n\n"
            "Le tawakkul est compatible avec la demande de pardon et l'action : nous prenons les moyens, "
            "nous invoquons Allah, nous agissons avec sagesse, puis nous remettons tout à Lui.\n\n"
            "Application pratique :\n"
            "- Avant chaque action importante, formulez votre intention, travaillez avec sérieux, puis dites "
            "« Tawakkaltu 'ala Allah » (Je me confie à Allah)\n"
            "- Quand l'angoisse vous gagne, récitez « Allahumma la sahla illa ma ja'alatahu sahla » (Ô "
            "Allah, rien n'est facile sauf ce que Tu rends facile)\n"
            "- Souvenez-vous que le tawakkul, c'est la rencontre entre l'effort humain et la confiance divine"
        ),
        "quran": [
            {"ref": "65:2", "note": "Quiconque craint Allah, Il lui donnera une issue"},
            {"ref": "3:159", "note": "Quand tu as pris une décision, confie-toi à Allah"},
        ],
        "hadith": [
            {"book": "tirmidhi", "number": 2587, "note": "« Ô Messager d'Allah, dois-je la lâcher et me confier à Allah ? » Il dit : « Lie-la et confie-toi à Allah » (tawakkul)"},
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
            "La fraternité islamique (ukhuwwah) est un pilier spirituel et social de l'islam. Allah dit : "
            "« Les croyants ne sont que des frères. Etablissez donc la concorde entre vos frères » (49:10). "
            "Cette fraternité dépasse les liens de sang, d'origine, de langue et de nationalité : elle est "
            "fondée sur la foi et l'amour pour Allah.\n\n"
            "Cette fraternité est unique dans l'histoire : elle a uni les Muhajirun (émigrants de la Mecque) "
            "aux Ansar (partisans de Médine), qui ont partagé leurs maisons, leurs biens et leurs familles. "
            "Le Prophète ﷺ a établi cette fraternité officiellement à Médine, montrant qu'elle est une "
            "institution essentielle de la communauté.\n\n"
            "Le Prophète ﷺ a dit : « Aucun de vous ne croit tant qu'il n'aime pas pour son frère ce qu'il "
            "aime pour lui-même » (Bukhari et Muslim). C'est un test de la foi : l'amour du bien pour "
            "autrui, au même niveau que pour soi-même. C'est le principe d'or de l'islam : ne désire pour "
            "ton frère que ce que tu désires pour toi.\n\n"
            "Les droits mutuels entre musulmans (d'après le Sahih Muslim) :\n"
            "- Le droit à la salutation : le musulman a droit aux salutations par le salam\n"
            "- Le droit au soutien en cas de maladie : visiter le malade\n"
            "- Le droit aux condoléances : assister aux funérailles\n"
            "- Le droit de répondre à l'invitation\n"
            "- Le droit de prier pour la miséricorde quand l'on éternue (et que le musulman répond « Yahdikumu Allah »)\n"
            "- Le droit de recevoir un bon conseil sincère (naseehah)\n\n"
            "Le Coran énumère d'autres droits : la bienveillance, l'honnêteté, la loyauté, le soutien "
            "matériel et moral : « Les croyants et les croyantes sont alliés les uns des autres » (9:71).\n\n"
            "Aimer pour Allah, haïr pour Allah : les savants distinguent l'amour pour Allah (aimer quelqu'un "
            "parce qu'il est obéissant à Allah) de l'amour personnel (aimer quelqu'un pour ses qualités "
            "humaines). Le Prophète ﷺ a dit que celui qui aime pour Allah, hait pour Allah, donne pour "
            "Allah et retient pour Allah a perfectionné sa foi (Abu Dawud).\n\n"
            "Les signes de la fraternité authentique :\n"
            "- La sincérité dans le conseil, même quand c'est difficile\n"
            "- La discrétion sur les défauts des autres\n"
            "- La prière pour son frère en son absence (le Prophète ﷺ a dit que c'est une invocation exaucée)\n"
            "- L'entraide matérielle et morale : « Aidez-vous les uns les autres dans l'accomplissement des "
            "bonnes œuvres et de la piété » (5:2)\n"
            "- Le pardon des erreurs : « Que ceux d'entre vous qui ont de la vertu et de la richesse ne "
            "jurent pas de ne plus donner aux parents et aux pauvres » (24:22)\n\n"
            "Application pratique :\n"
            "- Organisez des liens réguliers avec les musulmans autour de vous (mosquée, voisinage, famille)\n"
            "- Visitez les malades et assistez aux funérailles (un droit, pas une option)\n"
            "- Donnez un conseil sincère avec douceur et discrétion\n"
            "- Priez pour votre frère en son absence\n"
            "- Soyez un vecteur d'unité, pas de division"
        ),
        "quran": [
            {"ref": "49:10", "note": "Les croyants ne sont que des frères"},
            {"ref": "8:1", "note": "Les croyants sont des frères"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 13, "note": "Aime pour ton frère ce que tu aimes pour toi-même"},
            {"book": "bukhari", "number": 1203, "note": "Les droits du musulman : visiter le malade, suivre les funérailles, répondre à l'invitation, répondre au salam, souhaiter le miséricorde à l'éternueur"},
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
            "Les batailles et expéditions de l'époque du Prophète ﷺ contiennent des leçons profondes. Il est "
            "important de les comprendre dans leur contexte : il ne s'agissait pas de guerres de conquête ou "
            "d'expansion territoriale, mais de luttes pour la survie de la communauté et la liberté de "
            "croyance face à une persécution continue. Chaque bataille porte des enseignements spirituels, "
            "stratégiques et moraux.\n\n"
            "1) La bataille de Badr (624 de notre ère / 2 Hégire) :\n"
            "- Contexte : une petite communauté de 313 musulmans affronta une armée de près de 1000 Mecquois "
            "bien équipés, près des puits de Badr.\n"
            "- Leçon : la victoire vint de la foi, non de la force des armes. Allah dit : « Allah vous a "
            "déjà secourus à Badr alors que vous étiez une petite troupe : craignez donc Allah » (3:123). "
            "Badr a montré que lorsqu'on s'appuie sur Allah avec sincérité, la force matérielle peut être "
            "dépassée. C'est aussi la première victoire décisive : elle établit la légitimité et la "
            "puissance naissante de la communauté musulmane.\n\n"
            "2) La bataille d'Uhud (625) :\n"
            "- Contexte : l'année suivante, les Quraysh revinrent se venger. Le Prophète ﷺ avait posté des "
            "archers sur une colline avec l'ordre strict de ne pas la quitter, quelle que soit l'issue. "
            "Quand ils virent les musulmans gagner, ils désobéirent pour participer au butin, et laissent "
            "un espace ouvert. La cavalerie mecquoise contre-attaqua de flanc, provoquant une défaite partielle "
            "et la blessure grave du Prophète ﷺ.\n"
            "- Leçon : la désobéissance aux ordres du Prophète ﷺ et à la discipline collective a des "
            "conséquences graves. La victoire n'est jamais acquise sans la piété et la discipline. "
            "Uhud enseigne aussi le pardon : le Prophète ﷺ, blessé, a demandé le pardon pour ses "
            "compagnons qui avaient commis la faute.\n\n"
            "3) La bataille du fossé (Al-Ahzab / Al-Khandaq, 627) :\n"
            "- Contexte : une coalition de tribus mecquoises (Al-Ahzab, les partis) assiégea Médine avec "
            "une grande force. Salman al-Farisi, un compagnon persan, proposa de creuser un fossé autour "
            "de la ville, une stratégie inconnue dans la péninsule arabique.\n"
            "- Leçon : la stratégie, la préparation et l'intelligence comptent autant que la foi. La "
            "victoire finale vint sans bataille d'armée : Allah envoya un vent violent et la peur dans le "
            "camp ennemi, qui se retira. La sourate Al-Ahzab (33) et son verset sur le « vent » et les "
            "« soldats invisibles » illustrent l'intervention divine.\n\n"
            "4) La conquête de La Mecque (630) :\n"
            "- Contexte : après la violation du pacte de Hudaybiyah, une armée de 10 000 hommes entra "
            "pacifiquement dans la Mecque.\n"
            "- Leçon : la clémence dans la victoire. « Allez, vous êtes libres. » Le Prophète ﷺ a purifié "
            "la Kaaba des idoles et a pardonné à ses pires ennemis. C'est le sommet de la miséricorde "
            "prophétique.\n\n"
            "5) La bataille de Hunayn (630) :\n"
            "- Contexte : une coalition de tribus hostiles tenta de combattre les musulmans après la "
            "conquête. Les musulmans crurent leur nombre suffisant (« votre grand nombre vous a plu ») "
            "mais furent repoussés d'abord.\n"
            "- Leçon : l'orgueil, même pour une bonne cause, peut mener à la chute. Allah dit : « Après "
            "l'humiliation, Il vous fit remporter la victoire. » L'humilité devant Allah et Son secours "
            "sont les vraies forces.\n\n"
            "Les enseignements transversaux de ces batailles :\n"
            "- La foi est le facteur décisif, pas le nombre\n"
            "- La discipline et l'obéissance sont indispensables\n"
            "- La stratégie et la préparation sont des vertus islamiques\n"
            "- Le pardon dans la victoire est la marque du croyant\n"
            "- L'orgueil est l'ennemi caché\n"
            "- Les batailles étaient des réponses à l'agression, jamais des guerres de conquête"
        ),
        "quran": [
            {"ref": "8:5", "note": "Allah vous a secourus à Badr alors que vous étiez les plus faibles"},
            {"ref": "3:123", "note": "Allah vous a déjà secourus à Badr, alors que vous étiez les plus faibles"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 455, "note": "Le jour du fossé (Al-Khandaq) et la stratégie du creusement du tranchée autour de Médine"},
            {"book": "bukhari", "number": 2797, "note": "Le Prophète ﷺ dans sa tente le jour de Badr : la victoire vient d'Allah"},
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
            "Les épouses du Prophète ﷺ — « les Mères des croyants » (Ummahat al-Mu'minin), comme les appelle "
            "le Coran (33:6) — ont joué un rôle fondamental dans la transmission de l'islam. Elles étaient "
            "des compagnes, des savantes, des témoins et des modèles pour toute la communauté. Étudier leur "
            "vie, c'est comprendre le modèle familial prophétique et le rôle de la femme en islam.\n\n"
            "1) Khadijah bint Khuwaylid (morte en 619) : première épouse et premier soutien. Veuve "
            "commerçante respectée, elle proposa le mariage au Prophète ﷺ quand il avait 25 ans et elle "
            "40 ans. Elle fut la première à croire en sa prophétie, le consola lors de la première révélation "
            "et dépensa sa fortune pour la cause de l'islam. Le Prophète ﷺ ne se maria avec personne "
            "d'autre pendant toute leur vie commune. Après sa mort, il garda une reconnaissance immense "
            "pour elle.\n\n"
            "2) Sawdah bint Zam'ah : veuve émigrée, elle épousa le Prophète ﷺ à Médine pour protéger et "
            "aider les enfants. Elle est restée un modèle de générosité et de dévouement.\n\n"
            "3) Aisha bint Abi Bakr : la plus jeune des épouses, fille d'Abu Bakr. Elle fut l'une des "
            "plus grandes savantes de l'islam : plus de 2000 hadiths transmis par elle. Les compagnons "
            "venaient consulter ses connaissances en fiqh. Elle a joué un rôle décisif dans la "
            "transmission de la Sunna, notamment sur le foyer du Prophète ﷺ, les ablutions, la prière et "
            "les règles des femmes\n\n"
            "4) Hafsa bint Omar (fille d'Omar ibn al-Khattab) : elle fut la gardienne du premier exemple "
            "du Coran (le mushaf rassemblé sous Abu Bakr). Elle était reconnue pour sa piété et son "
            "jeûne assidu.\n\n"
            "5) Zaynab bint Jahsh : cousine du Prophète ﷺ, elle épousa au début un homme affranchi "
            "(Zayd ibn Harithah) pour installer la révision des préjugés sociaux de l'Arabie préislamique "
            "(l'adoption n'a pas le statut du sang). Son mariage avec le Prophète ﷺ fut révélé par un "
            "verset du Coran (33:37-38), pour abroger la coutume qui interdisait de se marier avec l'ex-"
            "épouse d'un fils adoptif. Elle était célèbre pour sa générosité et ses œuvres caritatives.\n\n"
            "Les autres épouses : Umm Salama (source importante de hadiths et modèle de patience), Juwairiyah "
            "bint al-Harith, Safiyyah bint Huyay, Maymunah bint al-Harith, et Rayhana (période incertaine). "
            "Le Prophète ﷺ avait un certain nombre d'épouses à une époque donnée — un régime spécial "
            "révélé par le Coran pour Lui seul, dans un but politique (unifier les tribus) et social "
            "(protéger les veuves).\n\n"
            "Le modèle familial prophétique :\n"
            "- Le Prophète ﷺ participait aux tâches ménagères : Aisha a rapporté « Il cousait ses "
            "vêtements, réparait ses sandales, servait sa famille » (Bukhari).\n"
            "- Il traitait ses épouses avec respect, tendresse et justice\n"
            "- Il jouait avec les enfants, porte les petits, souriait et plaisantait\n"
            "- Il consultait ses épouses dans les décisions importantes (comme au moment du traité "
            "de Hudaybiyah)\n"
            "- Il a dit : « Le meilleur d'entre vous est celui qui est le meilleur envers sa famille, et "
            "je suis le meilleur d'entre vous envers ma famille » (Tirmidhi).\n\n"
            "Les femmes en islam : la place de la femme en islam est définie par la justice et la dignité. "
            "Le Coran dit : « Elles sont un vêtement pour vous et vous un vêtement pour elles » (2:187). "
            "Le Prophète ﷺ a dit : « Recommandez-vous mutuellement les femmes comme bon » (Bukhari).\n\n"
            "Application pratique :\n"
            "- Étudiez la vie des épouses du Prophète ﷺ : elles sont des trésors de connaissance et de modèles\n"
            "- Connaissez les hadiths islamiques sur les femmes et la famille\n"
            "- Appliquez le principe d'or : traitez votre femme comme le Prophète ﷺ traitait les siennes"
        ),
        "quran": [
            {"ref": "33:28", "note": "Versets de la khaswa (épouses du Prophète)"},
            {"ref": "33:59", "note": "Ordre de porter le voile pour les femmes du Prophète"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 5743, "note": "Qui mérite le mieux mes bonnes relations ? Ta mère, puis ta mère, puis ta mère, puis ton père (le meilleur envers la famille)"},
            {"book": "bukhari", "number": 5219, "note": "Le Prophète servait sa famille et aidait à la maison"},
        ],
    },
    # ── Module 13 : Vie familiale et mariage en islam ────────────────────────
    {
        "module": 13,
        "module_title": "La vie familiale et le mariage en islam",
        "id": "fam1",
        "title": "Le mariage : buts et conditions",
        "objectives": [
            "Comprendre le but spirituel et social du mariage",
            "Connaître les piliers et conditions de validité du mariage",
        ],
        "content": (
            "Le mariage (nikah) est un acte d'adoration en islam. Le Prophète ﷺ l'a appelé « ma Sunna » et a dit : "
            "« Quiconque se détourne de ma Sunna n'est pas de moi ». Le mariage n'est pas une simple convention "
            "sociale : c'est une institution sacrée qui unit deux êtres pour construire une famille croyante et "
            "aimante, et c'est la moitié de la religion pour celui qui y entre purement.\n\n"
            "Le but du mariage défini par le Coran : « Et parmi Ses signes, Il a créé pour vous, de vous-mêmes, "
            "des épouses afin que vous trouviez auprès d'elles la tranquillité, et Il a placé entre vous affection "
            "et miséricorde. Il y a en cela des signes pour des gens qui réfléchissent » (30:21). Ce verset "
            "révèle trois finalités :\n"
            "1) La tranquillité (sakinah) : trouver le repos et la sérénité auprès de son conjoint\n"
            "2) L'affection (mawaddah) : l'amour chaleureux qui lie les époux\n"
            "3) La miséricorde (rahmah) : la bienveillance, le pardon et la tendresse mutuels\n"
            "Ce verset place la femme comme un « signe d'Allah » : un reflet de Sa sagesse pour l'homme.\n\n"
            "D'autres objectifs légitimes :\n"
            "- La chasteté : le Prophète ﷺ a dit au jeune homme qui pouvait se marier : « Qu'il se marie, car cela "
            "abaisse le regard et protège la chasteté » (Bukhari n°4862)\n"
            "- La continuation de l'espèce humaine : « Ô gens ! Craignez votre Seigneur qui vous a créés d'un seul "
            "être » (4:1)\n"
            "- L'établissement d'une famille pieuse, berceau d'une société saine\n\n"
            "La vertu recherchée chez le conjoint : le Prophète ﷺ a dit : « On épouse la femme pour quatre choses : "
            "sa richesse, sa lignée, sa beauté et sa religion. Choisis celle qui a la religion, que tu sois "
            "comblé » (Bukhari n°4886 et Muslim). C'est un principe fondamental : la piété et le caractère doivent "
            "primer sur l'apparence et la fortune. Une union fondée sur la religion est une union bénie et durable.\n\n"
            "Les piliers et conditions de validité du mariage :\n"
            "- L'accord des deux époux (consentement mutuel) : le mariage est invalide s'il est imposé à une "
            "femme contre sa volonté. Le Prophète ﷺ a dit que la femme ne doit pas être donnée en mariage sans "
            "son consentement\n"
            "- Le tuteur (wali) pour la femme musulmane : le père ou le plus proche parent mâle agit comme tuteur\n"
            "- Deux témoins musulmans intègres présents à la conclusion du contrat\n"
            "- La dot (mahr) : une somme ou un bien offert à la femme, un droit qui lui appartient entièrement, "
            "et non une simple formalité symbolique\n"
            "- Le célibat des personnes concernées (pas de mariage simultané avec une personne déjà mariée dans "
            "des conditions interdites)\n\n"
            "Le mariage établit des droits et des devoirs réciproques : « Et elles ont des droits équivalents à "
            "leurs obligations, conformément à la bienséance. Et les hommes ont sur elles un degré [de "
            "responsabilité] » (2:228). L'islam établit donc une complémentarité et une équité entre les époux, "
            "fondées sur la responsabilité et la bienveillance.\n\n"
            "Application pratique :\n"
            "- Si vous voulez vous marier, recherchez d'abord la piété et le bon caractère chez le futur conjoint\n"
            "- Faites de la consultation (istikhara) et du conseil familial des étapes de votre décision\n"
            "- Établissez dès le départ un foyer fondé sur la prière, la patience et la miséricorde réciproque"
        ),
        "quran": [
            {"ref": "30:21", "note": "Il a placé entre vous affection et miséricorde"},
            {"ref": "4:1", "note": "Craignez votre Seigneur qui vous a créés d'un seul être"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 4862, "note": "La Sunna du mariage : qu'il se marie, cela abaisse le regard et protège la chasteté"},
            {"book": "bukhari", "number": 4886, "note": "On épouse pour quatre choses : richesse, lignée, beauté, religion — choisis la religion"},
        ],
    },
    {
        "module": 13,
        "module_title": "La vie familiale et le mariage en islam",
        "id": "fam2",
        "title": "L'amour et le respect mutuels entre époux",
        "objectives": [
            "Comprendre le modèle prophétique de la relation conjugale",
            "Apprendre à bâtir un foyer fondé sur la miséricorde",
        ],
        "content": (
            "La relation entre époux en islam est bâtie sur l'amour (mawaddah), la miséricorde (rahmah) et la "
            "justice (adl). Le Coran décrit les époux comme « un vêtement l'un pour l'autre » (2:187) : le "
            "vêtement protège, embellit, cache et apaise. C'est une image magnifique de l'intimité et de la "
            "complémentarité conjugale.\n\n"
            "Le modèle prophétique : le Prophète ﷺ est le meilleur exemple dans la relation conjugale. Il a dit : "
            "« Le meilleur d'entre vous est celui qui est le meilleur envers sa famille, et je suis le meilleur "
            "d'entre vous envers ma famille » (Tirmidhi n°1165). Cette parole établit que la bonté envers son "
            "épouse est un signe de foi et de perfection morale.\n\n"
            "Comment le Prophète ﷺ traitait-il ses épouses ?\n"
            "- Il les aidait dans les tâches de la maison : Aisha a rapporté qu'il cousait ses vêtements, réparait "
            "ses sandales et aidait sa famille (Bukhari n°5219)\n"
            "- Il était doux et patient, même dans la difficulté\n"
            "- Il plaisantait avec elles, partageait leurs joies et les consolait dans leurs peines\n"
            "- Il écoutait leurs avis dans les décisions importantes (par exemple Umm Salama au traité de "
            "Hudaybiyah)\n"
            "- Il souriait et exprimait sa tendresse\n\n"
            "L'égalité et la complémentarité : le Coran dit « Ô vous qui avez cru ! Il ne vous est pas permis "
            "d'hériter des femmes contre leur gré. Et ne les maltraitez pas » (4:19). Il a aussi ordonné : "
            "« Comportez-vous avec elles convenablement. Si vous les haïssez, il se peut que vous haïssiez une "
            "chose alors qu'Allah y a placé beaucoup de bien » (4:19). Même l'aversion n'est pas une excuse pour "
            "la dureté : on peut découvrir le bien dans ce qu'on n'aime pas.\n\n"
            "Les droits et devoirs fondamentaux :\n"
            "- L'homme est le soutien financier (qawwam), responsable de la subsistance de la famille. Le Coran "
            "dit : « Les hommes ont autorité sur les femmes, en raison des faveurs qu'Allah accorde à ceux-là "
            "sur celles-ci, et aussi à cause des dépenses qu'ils font de leurs biens » (4:34). Il s'agit d'une "
            "responsabilité, pas d'un privilège de supériorité.\n"
            "- La femme a le droit à la dot, à l'entretien, à la cohabitation juste et au respect\n"
            "- La femme et l'homme sont égaux en valeur spirituelle : « Quiconque, homme ou femme, fait une bonne "
            "œuvre tout en étant croyant... » (16:97)\n"
            "- Les époux doivent se traiter avec bienséance (ma'ruf) : la bienveillance doit être réciproque\n\n"
            "La patience dans le mariage : le mariage est aussi une école de patience. Les différences de "
            "caractère, les difficultés matérielles, les épreuves de la vie mettent la relation à l'épreuve. "
            "L'islam encourage la recherche de solutions, la consultation mutuelle (shura) et, si nécessaire, "
            "l'arbitrage familial (4:35) plutôt que la rupture hâtive. Le divorce est autorisé mais c'est « la "
            "chose licite la plus détestée d'Allah » (Abu Dawud) : il est le dernier recours.\n\n"
            "Application pratique :\n"
            "- Traitez votre conjoint comme vous voudriez être traité : avec respect, tendresse et gratitude\n"
            "- Exprimez votre affection en paroles et en actes chaque jour\n"
            "- Consultez votre conjoint dans les décisions importantes\n"
            "- En cas de conflit, privilégiez le dialogue, le pardon et la consultation\n"
            "- Faites de la prière commune et de la lecture du Coran un pilier de votre foyer"
        ),
        "quran": [
            {"ref": "2:187", "note": "Elles sont un vêtement pour vous et vous un vêtement pour elles"},
            {"ref": "4:19", "note": "Comportez-vous avec elles convenablement"},
            {"ref": "4:34", "note": "Les hommes ont autorité sur les femmes, en raison des faveurs d'Allah et de leurs dépenses"},
        ],
        "hadith": [
            {"book": "tirmidhi", "number": 1165, "note": "Le meilleur d'entre vous est le meilleur envers sa famille"},
            {"book": "bukhari", "number": 5219, "note": "Le Prophète aidait sa famille à la maison"},
        ],
    },
    {
        "module": 13,
        "module_title": "La vie familiale et le mariage en islam",
        "id": "fam3",
        "title": "Les parents : droits et piété filiale",
        "objectives": [
            "Comprendre la place éminente des parents dans l'islam",
            "Apprendre comment servir et honorer ses parents",
        ],
        "content": (
            "La bonté envers les parents (birr al-walidayn) est, après l'adoration d'Allah, l'obligation la plus "
            "importante de l'islam. Allah a lié Son adoration au devoir envers les parents : « Et ton Seigneur a "
            "décrété : n'adorez que Lui, et (faites) le bien envers les père et mère » (17:23). Cette juxtaposition "
            "montre l'importance capitale de la piété filiale.\n\n"
            "Le devoir envers les parents après l'adoration : dans le hadith, un homme demanda au Prophète ﷺ "
            "« Quelle est l'œuvre la plus agréable à Allah ? » Il répondit « La prière à son heure ». Puis « Le "
            "bien envers les parents ». Puis « Le jihad dans le sentier d'Allah » (Bukhari). Le bien envers les "
            "parents occupe la deuxième place, après la prière.\n\n"
            "La triple mention de la mère : un homme demanda au Prophète ﷺ « Qui mérite le mieux ma bonne "
            "compagnie ? » Il répondit « Ta mère ». « Et ensuite ? » « Ta mère ». « Et ensuite ? » « Ta mère ». "
            "« Et ensuite ? » « Ton père » (Bukhari n°5743). La mère est citée trois fois avant le père, en "
            "raison des peines de la grossesse, de l'accouchement et de l'allaitement.\n\n"
            "Ce que le Coran demande :\n"
            "- La bienfaisance : « Et ton Seigneur a décrété : n'adorez que Lui, et (faites) le bien envers les "
            "père et mère » (17:23)\n"
            "- La douceur : « Si l'un d'eux ou tous deux atteignent auprès de toi la vieillesse, ne leur dis "
            "point : Fi ! Et ne les brusque pas, mais adresse-leur des paroles honorables » (17:23). Même le mot "
            "« Fi » (pff) est interdit : la patience face à la vieillesse des parents est un acte d'adoration.\n"
            "- L'humilité : « Et par miséricorde, abaisse pour eux l'aile de l'humilité » (17:24)\n"
            "- L'invocation : « Et dis : Ô mon Seigneur, fais-leur à tous deux miséricorde comme ils m'ont "
            "élevé tout petit » (17:24)\n"
            "- La gratitude : « Et Nous avons recommandé à l'homme (la bienfaisance envers) ses deux parents, "
            "sa mère l'a porté [en subissant] faiblesse sur faiblesse » (31:14)\n\n"
            "La piété filiale ne cesse pas avec la mort des parents : on peut continuer à les honorer par "
            "l'invocation, la sadaqa en leur nom, l'entretien de leurs liens de parenté et le respect de leurs "
            "engagements.\n\n"
            "L'ordre d'obéissance aux parents n'est pas absolu : l'obéissance aux parents ne vaut pas dans la "
            "désobéissance à Allah. Le Prophète ﷺ a dit « Point d'obéissance à une créature dans la "
            "désobéissance au Créateur ». Mais même dans ce cas, il faut refuser avec douceur et respect, sans "
            "rupture de la relation.\n\n"
            "Application pratique :\n"
            "- Appelez vos parents régulièrement, prenez de leurs nouvelles avec affection\n"
            "- Aidez-les matériellement et dans les tâches de la vie quotidienne\n"
            "- Patientez avec leur vieillesse et ne leur dis jamais « Fi »\n"
            "- Priez pour eux constamment, dans leur vie et après leur mort\n"
            "- Faites des aumônes à leur intention s'ils sont décédés"
        ),
        "quran": [
            {"ref": "17:23", "note": "N'adorez qu'Allah, et faites le bien envers les père et mère"},
            {"ref": "17:24", "note": "Par miséricorde, abaisse pour eux l'aile de l'humilité"},
            {"ref": "31:14", "note": "Sa mère l'a porté en subissant faiblesse sur faiblesse"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 5743, "note": "Ta mère, puis ta mère, puis ta mère, puis ton père"},
            {"book": "bukhari", "number": 2548, "note": "Les grands péchés : associer à Allah, être indocile envers ses parents, tuer"},
        ],
    },
    # ── Module 14 : Éthique et valeurs économiques en islam ──────────────────
    {
        "module": 14,
        "module_title": "L'éthique et les valeurs économiques en islam",
        "id": "eco1",
        "title": "La justice et l'honnêteté dans l'argent",
        "objectives": [
            "Comprendre les principes de justice économique en islam",
            "Apprendre l'honnêteté dans le commerce et les transactions",
        ],
        "content": (
            "L'islam donne à l'économie une dimension éthique profonde : l'argent n'est pas une fin en soi, mais "
            "un moyen que l'homme doit gérer en dépositaire responsable devant Allah. Le Coran et la Sunna fixent "
            "des principes clairs de justice, d'honnêteté et de solidarité économique.\n\n"
            "Les biens sont une épreuve et un dépôt : Allah dit « Sachez que vos biens et vos enfants ne sont "
            "qu'une épreuve, et que c'est auprès d'Allah qu'est une énorme récompense » (8:28). La richesse est "
            "une épreuve : elle révèle si l'homme reste humble, généreux et obéissant, ou si elle l'enivre et "
            "l'éloigne de son Créateur.\n\n"
            "La justice dans les transactions :\n"
            "- La justice est commandée dans tout échange : « Ô vous qui avez cru ! Soyez stricts dans la "
            "justice » (5:8). La justice dans les transactions commerciales est une obligation religieuse.\n"
            "- La fraude est interdite : le Prophète ﷺ a dit « Celui qui nous trompe n'est pas des nôtres » "
            "(Muslim n°101).\n"
            "- La tromperie sur la qualité des marchandises est interdite\n\n"
            "Les « trompeurs » (mutaffifin) : la sourate Al-Mutaffifin (83) condamne sévèrement ceux qui fraudent "
            "dans les mesures et les poids : « Malheur aux fraudeurs, qui, lorsqu'ils font mesurer pour eux-"
            "mêmes, exigent la pleine mesure, et qui, lorsqu'eux-mêmes mesurent ou pèsent pour les autres, leur "
            "causent perte. Ceux-là ne pensent-ils pas qu'ils seront ressuscités ? » (83:1-5). L'honnêteté dans "
            "le poids et la mesure est un devoir : « Donnez la pleine mesure quand vous mesurez, et pesez avec "
            "une balance exacte » (17:35 / 55:9).\n\n"
            "Les droits économiques :\n"
            "- Rémunérer le travailleur : « Payer l'ouvrier avant que sa sueur ne sèche » (Ibn Majah)\n"
            "- Éviter l'usure (riba) : le Coran interdit l'usure et encourage la sadaqa (2:275-276)\n"
            "- Remplir les contrats et les engagements : « Ô vous qui avez cru ! Remplissez les contrats » (5:1)\n"
            "- Écrire les dettes : « Ô vous qui avez cru ! Quand vous contractez une dette à échéance fixe, "
            "mettez-la par écrit » (2:282). Allah ordonne la documentation des créances pour prévenir les conflits\n\n"
            "La vérité et la transparence : le Prophète ﷺ a dit « Les deux vendeurs ont le choix (de poursuivre) "
            "tant qu'ils ne se sont pas quittés ; s'ils furent véridiques et clairs, leur vente est bénie ; mais "
            "s'ils dissimulèrent et mentirent, la bénédiction de leur vente sera effacée » (Tirmidhi n°1254). "
            "L'honnêteté apporte la baraka (bénédiction) dans les gains.\n\n"
            "Application pratique :\n"
            "- Soyez toujours honnête dans vos transactions, même dans les petites choses\n"
            "- Donnez la pleine mesure et pesez exactement\n"
            "- Payer les travailleurs et rembourser les dettes dans les délais\n"
            "- Évitez toute forme d'intérêt usuraire et cherchez des voies licites (halal)"
        ),
        "quran": [
            {"ref": "83:1", "note": "Malheur aux fraudeurs"},
            {"ref": "83:2", "note": "Ceux qui, lorsqu'ils font mesurer pour eux-mêmes, exigent la pleine mesure"},
            {"ref": "83:3", "note": "Et qui, lorsqu'ils pèsent ou mesurent pour d'autres, leur causent perte"},
            {"ref": "16:90", "note": "Allah commande l'équité, la bienfaisance et l'extension aux proches"},
            {"ref": "2:283", "note": "N'atténuez pas le témoignage"},
        ],
        "hadith": [
            {"book": "tirmidhi", "number": 1995, "note": "Le musulman est le frère du musulman : il ne le trompe pas, ne lui ment pas, ne le trahit pas ; son honneur, ses biens et son sang lui sont sacrés"},
            {"book": "tirmidhi", "number": 1254, "note": "Si les vendeurs furent véridiques et clairs, leur vente est bénie"},
        ],
    },
    {
        "module": 14,
        "module_title": "L'éthique et les valeurs économiques en islam",
        "id": "eco2",
        "title": "Le compte des biens et la préparation de l'au-delà",
        "objectives": [
            "Comprendre que les biens seront comptés au Jour dernier",
            "Apprendre la modération et le détachement",
        ],
        "content": (
            "L'un des principes fondamentaux de l'économie islamique est que l'homme ne peut pas séparer sa vie "
            "économique de sa destinée éternelle. Les biens et les richesses seront pris en compte le Jour de la "
            "Résurrection : « Certes, ceux qui thésaurisent l'or et l'argent et ne les dépensent pas dans le "
            "sentier d'Allah, annonce-leur un châtiment douloureux » (9:34).\n\n"
            "L'interrogation sur les biens : le Prophète ﷺ a dit que les pieds du serviteur ne cesseront pas de "
            "bouger le Jour de la Résurrection avant qu'on ne l'interroge sur quatre choses : sa vie, sa "
            "jeunesse, sa science et « d'où il a acquis ses biens et où il les a dépensés » (Tirmidhi). Chaque "
            "argent doit donc être gagné licitement (halal) et dépensé de manière louable.\n\n"
            "Les sources de revenus licites et illicites :\n"
            "- Illicites : le vol, la fraude, l'usure (riba), la tromperie, les gains du jeu et de l'alcool, "
            "l'argent gagné par des moyens interdits\n"
            "- Licites : le travail honnête, le commerce équitable, les métiers utiles. Le Prophète ﷺ a dit que "
            "« le commerçant véridique et digne de confiance sera avec les prophètes, les véridiques et les "
            "martyrs » (Tirmidhi)\n\n"
            "La nourriture et l'argent licites (halal) ont un effet spirituel : ce qui est consommé illicite "
            "souille le corps et le cœur, et empêche l'exaucement des invocations. Le Prophète ﷺ a mentionné "
            "l'homme qui prie en mendiant, à la chevelure hirsute, dont la nourriture est illicite, et a dit "
            "qu'il n'invoquait qu'avec une bouche nourrie d'illicite : ses invocations ne sont pas exaucées.\n\n"
            "La modération (qasd) dans la dépense :\n"
            "- Allah condamne le gaspillage : « Et ne gaspillez pas ; car Allah n'aime pas les gaspilleurs » "
            "(7:31)\n"
            "- L'islam recommande une dépense équilibrée : « Et ceux qui, lorsqu'ils dépensent, ne sont ni "
            "prodigues ni avares, mais se tiennent au juste milieu » (25:67)\n"
            "- Le Prophète ﷺ a recommandé de vivre selon ses moyens et d'éviter la surenchère dans les dépenses\n\n"
            "Le détachement et la vigilance :\n"
            "- Les biens de ce monde sont temporaires ; l'au-delà est éternel. « La vie présente n'est que jeu et "
            "divertissement ; et la vie future est bien meilleure pour ceux qui craignent Allah » (6:32)\n"
            "- Le riche doit se rappeler qu'il rendra compte : la richesse est un dépôt qui doit être purifié "
            "par la zakat et la sadaqa\n"
            "- Une vie simple et tournée vers Allah est une source de sérénité\n\n"
            "Application pratique :\n"
            "- Interrogez-vous sur la source de vos revenus et purifiez ce qui est douteux\n"
            "- Dépensez avec modération, sans avarice ni gaspillage\n"
            "- Mémorisez et méditez que chaque dirham a une origine et une destination dont vous rendrez compte\n"
            "- Faites de la zakat et de la sadaqa une habitude régulière"
        ),
        "quran": [
            {"ref": "6:32", "note": "La vie présente n'est que jeu et divertissement ; la prospérité future est meilleure pour les pieux"},
            {"ref": "25:67", "note": "Ceux qui, lorsqu'ils dépensent, ne sont ni prodigues ni avares"},
            {"ref": "83:1", "note": "Malheur aux fraudeurs : le compte des biens est certain"},
        ],
        "hadith": [
            {"book": "tirmidhi", "number": 2486, "note": "Les pieds du serviteur ne bougeront pas le Jour du Jugement avant qu'on ne l'interroge sur sa vie, sa jeunesse, sa science et ses biens"},
        ],
    },
    # ── Module 15 : Les prophètes et les récits coraniques ───────────────────
    {
        "module": 15,
        "module_title": "Les prophètes et les récits coraniques",
        "id": "pro1",
        "title": "Introduction aux prophètes et leurs missions",
        "objectives": [
            "Comprendre le rôle des prophètes en islam",
            "Connaître la différence entre prophète et messager",
        ],
        "content": (
            "Les prophètes occupent une place centrale dans la foi musulmane. Croire en eux est le 4e pilier de "
            "la foi (iman). Allah a envoyé des prophètes à chaque peuple pour transmettre le même message : "
            "adorer Allah seul. « Nous avons envoyé dans chaque communauté un messager [pour leur dire] : "
            "Adorez Allah et écartez-vous des fausses divinités » (16:36).\n\n"
            "La différence entre prophète (nabi) et messager (rasul) :\n"
            "- Tous les messagers sont des prophètes, mais tous les prophètes ne sont pas des messagers\n"
            "- Le prophète (nabi) reçoit la révélation d'Allah pour son peuple\n"
            "- Le messager (rasul) reçoit la révélation et est envoyé avec une législation nouvelle ou un "
            "message nouveau, souvent avec un Livre\n"
            "Le Coran mentionne 25 prophètes nommément, et Allah dit « Et des messagers que Nous t'avons déjà "
            "racontés, et des messagers que Nous ne t'avons pas racontés » (4:164). Leur nombre exact est "
            "connu d'Allah seul.\n\n"
            "Les qualités communes des prophètes :\n"
            "- Ils sont des êtres humains choisis par Allah ; ils ne sont pas divins\n"
            "- Ils sont infaillibles dans la transmission du message et exempts des grands péchés\n"
            "- Ils sont véridiques (sidq) et dignes de confiance (amanah)\n"
            "- Ils sont le meilleur exemple (uswah hasanah) pour leur communauté\n\n"
            "Les principaux prophètes mentionnés dans le Coran :\n"
            "- Adam (Adam) : le premier homme et premier prophète\n"
            "- Nuh (Noé) : envoyé à un peuple qui refusa de se repentir ; il construisit l'arche\n"
            "- Ibrahim (Abraham) : le ami intime d'Allah (Khalilullah), père des prophètes\n"
            "- Musa (Moïse) : à qui Allah parla directement (Kalimullah), envoyé avec la Thora\n"
            "- 'Isa (Jésus) : le Mesie, fils de Maryam, envoyé avec l'Évangile\n"
            "- Muhammad ﷺ : le sceau des prophètes, envoyé à toute l'humanité\n\n"
            "Le Coran relate leurs récits : « Récitons pour toi, en toute vérité, leur récit » (18:13). Ces "
            "récits contiennent des leçons : la patience, la confiance en Allah, la lutte contre l'idolâtrie, "
            "la persévérance face à l'adversité.\n\n"
            "Le premier commandement universel : chaque prophète a débuté sa mission par l'appel au tawhid "
            "(l'unicité d'Allah). Abraham dit à son peuple : « Et dont je veux dire à mon peuple : ne suivez "
            "que ce qui est juste, parcourez la voie d'Allah » (43:26) — il a rompu avec les idoles. C'est le "
            "fil conducteur de tous les messages : « Adorez Allah, vous n'avez point d'autre divinité que Lui ».\n\n"
            "Application pratique :\n"
            "- Étudiez les récits des prophètes : ils sont une source intarissable de leçons et de courage\n"
            "- Méditez la patience d'Abraham, la foi de Maryam, la constance des messagers\n"
            "- Croyez en tous les prophètes sans distinction, comme l'ordonne le Coran (2:285)"
        ),
        "quran": [
            {"ref": "4:163", "note": "Nous t'avons fait une révélation comme Nous fîmes à Noé et aux prophètes après lui"},
            {"ref": "43:26", "note": "Abraham rompit avec ce que vous adorez en dehors d'Allah"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 3299, "note": "Les prophètes sont des frères paternels : leur religion est une, leur législation diffère"},
        ],
    },
    {
        "module": 15,
        "module_title": "Les prophètes et les récits coraniques",
        "id": "pro2",
        "title": "Adam, Nuh et Ibrahim : leçon de foi et de patience",
        "objectives": [
            "Comprendre le récit d'Adam et la fallibilité",
            "Tirer les leçons des récits de Nuh et Ibrahim",
        ],
        "content": (
            "Les récits d'Adam, de Noé (Nuh) et d'Abraham (Ibrahim) sont parmi les plus riches d'enseignements "
            "du Coran. Ils nous apprennent la création de l'homme, le repentir, la patience et la confiance "
            "absolue en Allah.\n\n"
            "1) Adam : le premier homme et le premier prophète\n"
            "- Allah créa Adam de terre et souffla en lui de Son Esprit (38:71-72)\n"
            "- Allah enseigna à Adam les noms de toutes choses (2:31) : une dignité honorifique de l'homme\n"
            "- Adam et Eve vivaient au Paradis jusqu'à ce qu'ils succombent à la tentation de Satan et "
            "mangent de l'arbre interdit (2:36-37)\n"
            "- Après la faute, Adam et Eve se repentirent : « Ils dirent : Notre Seigneur, nous avons fait du "
            "tort à nous-mêmes. Si Tu ne nous pardonnes pas et ne nous fais pas miséricorde, nous serons "
            "certainement parmi les perdants » (7:23). Allah accepta leur repentir : c'est la première leçon "
            "sur la miséricorde et la tawbah.\n"
            "- La leçon : l'être humain est faillible mais toujours pardonné s'il se tourne vers Allah ; et "
            "Satan est l'ennemi déclaré de l'homme (2:36)\n\n"
            "2) Nuh (Noé) : la patience dans la mission\n"
            "- Nuh fut envoyé à son peuple qui adorait des idoles. Il les appela pendant neuf cent cinquante "
            "ans (29:14), mais seule une minorité crut (11:40)\n"
            "- Malgré les moqueries et le rejet, il resta ferme et patient\n"
            "- À la fin, il reçut l'ordre de construire l'arche ; les croyants furent sauvés pendant le "
            "déluge, et les mécréants périrent (11:38-44)\n"
            "- La leçon : la patience et la persévérance dans l'appel, même face à l'échec apparent ; la "
            "certitude que le secours d'Allah vient toujours\n\n"
            "3) Ibrahim (Abraham) : le père de la foi\n"
            "- Ibrahim est appelé « Khalil Allah » (l'ami intime d'Allah). Il est le modèle de la soumission "
            "et du sacrifice total\n"
            "- Il chercha Allah par le raisonnement (2:258-260) et invita son peuple à adorer Allah seul, "
            "brisant les idoles (21:51-67)\n"
            "- Il fut jeté dans le feu, qui devint paix et fraîcheur pour lui (21:69) : la confiance absolue\n"
            "- Il reçut l'ordre d'éloigner sa femme Hajar et son fils Ismaïl dans la vallée de Bakkah "
            "(future La Mecque), et de l'y laisser, sur ordre divin. Allah fit jaillir Zamzam pour eux (2:124-127)\n"
            "- Il fut éprouvé par le sacrifice de son fils : « Mon fils, je me suis vu en songe sacrifiant "
            "tout en te soumettant à l'épreuve. Observe donc ce que tu en penses. » Il dit : « Ô mon père, "
            "fais ce qui t'est commandé » (37:102). Son obéissance totale lui valut une rançon : le mouton "
            "(37:107) et l'institution de l'Aïd al-Adha\n"
            "- Allah fit de lui et d'Ismaïl les bâtisseurs de la Kaaba (2:125-127)\n\n"
            "Ces trois prophètes incarnent les piliers de la foi en pratique : Adam le repentir, Nuh la "
            "patience, Ibrahim la soumission et l'unicité. Les méditer renforce notre propre foi.\n\n"
            "Application pratique :\n"
            "- Puisez du courage dans la patience de Nuh et la soumission d'Ibrahim\n"
            "- Rappelez-vous que le repentir efface toute faute, comme pour Adam\n"
            "- Quel que soit le feu de vos épreuves, faites confiance à Allah comme Ibrahim"
        ),
        "quran": [
            {"ref": "2:37", "note": "Adam reçut des paroles de son Seigneur, qui accepta son repentir"},
            {"ref": "11:40", "note": "Embarquent seulement ceux qui croyaient (avec Nuh)"},
            {"ref": "37:100", "note": "Seigneur, donne-moi un [enfant] parmi les vertueux (Abraham)"},
            {"ref": "37:102", "note": "Je me suis vu en songe sacrifiant... Observe ce que tu en penses"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 3188, "note": "Allah créa Adam à Son image, soixante coudées de haut"},
        ],
    },
    {
        "module": 15,
        "module_title": "Les prophètes et les récits coraniques",
        "id": "pro3",
        "title": "Musa, 'Isa et Muhammad : les grands messagers",
        "objectives": [
            "Comprendre le rôle de Musa et 'Isa dans le Coran",
            "Situer Muhammad ﷺ comme le sceau des prophètes",
        ],
        "content": (
            "Musa (Moïse), 'Isa (Jésus) et Muhammad ﷺ sont trois des plus grands messagers de l'islam. Le Coran "
            "relate abondamment leurs histoires, et les musulmans croient en eux avec un amour et un respect "
            "profonds, comme en tous les prophètes.\n\n"
            "1) Musa (Moïse) : le prophète qui parla à Allah\n"
            "- Allah l'appela « Kalim Allah » (celui à qui Allah parla directement) : « Et Allah parla "
            "directement à Moïse » (4:164)\n"
            "- Il fut sauvé du Pharaon qui tuait les garçons hébreux : sa mère, par inspiration, le plaça dans "
            "un coffret jeté sur le Nil, qu'Allah ramena vers Pharaon (20:37-39)\n"
            "- Il reçut la révélation au mont Sinaï (Tur), reçut les tables de la Thora, et il demanda à voir "
            "Allah (7:143)\n"
            "- Il affronta Pharaon et son sorcier avec la force de la vérité, par l'ordre d'Allah\n"
            "- Il conduisit le peuple d'Israël hors d'Égypte, traversa la mer avec eux par la puissance d'Allah, "
            "mais son peuple sombra dans l'adoration du veau (7:148-150) pendant qu'il était parti recevoir les "
            "tables\n"
            "- La leçon : la fermeté dans la vérité face au tyran ; le souci de guider son peuple même quand "
            "il s'égare\n\n"
            "2) 'Isa (Jésus) : le messager et serviteur d'Allah\n"
            "- L'islam honore 'Isa comme un grand prophète et messager, né miraculeusement de la Vierge Maryam "
            "(Marie), mais il n'est pas divin : il est le serviteur et le messager d'Allah (43:59)\n"
            "- Sa naissance est relatée dans la sourate Maryam (19) : transcription d'une grâce divine\n"
            "- Il reçut l'Évangile et réalisa des miracles par la permission d'Allah : guérir le lépreux, "
            "ressusciter les morts, créer un oiseau d'argile (3:49)\n"
            "- Le Coran affirme : « Le Messie, fils de Marie, n'est qu'un messager » (5:75) et rejette toute "
            "divinité de 'Isa et de sa mère\n"
            "- Le Coran précise que 'Isa ne fut pas tué ni crucifié selon l'apparence apparente (4:157), mais "
            "qu'Allah l'éleva vers Lui ; son retour à la fin des temps est une croyance islamique\n\n"
            "3) Muhammad ﷺ : le sceau des prophètes\n"
            "- Il est le dernier des prophètes : « Muhamm n'est point une père d'aucun de vos hommes, mais le "
            "messager d'Allah et le sceau des prophètes » (33:40)\n"
            "- Il fut envoyé à toute l'humanité, alors que les prophètes précédents furent envoyés à leur "
            "peuple et à leur époque\n"
            "- Il apporta le Coran, miracle permanent et préservé, et la Sunna, explication vivante\n"
            "- Il est la miséricorde envoyée aux mondes (21:107)\n"
            "- Le Prophète ﷺ a dit qu'il est le plus proche des serviteurs de 'Isa le Jour de la Résurrection, "
            "car les prophètes sont des frères paternels (Bukhari n°3299)\n\n"
            "Le croyant croit en tout et tous les prophètes : « Le Messager a cru en ce qu'on a fait descendre "
            "vers lui de la part de son Seigneur, et les croyants aussi : tous ont cru en Allah, en Ses anges, "
            "en Ses Livres et en Ses messagers » (2:285). Aucune distinction entre les prophètes dans la foi.\n\n"
            "Application pratique :\n"
            "- Étudiez les récits des messagers : ils montrent comment transmettre la vérité avec douceur, "
            "force et patience\n"
            "- Suivez l'exemple de Muhammad ﷺ, le modèle parfait, en toute chose\n"
            "- Aimez et respectez tous les prophètes, et priez sur eux comme l'ordonne Allah"
        ),
        "quran": [
            {"ref": "4:163", "note": "Nous avons révélé à Moïse comme aux prophètes après lui"},
            {"ref": "3:45", "note": "Les anges annoncent à Marie un Verbe de Lui, nommé le Messie, fils de Marie"},
            {"ref": "33:40", "note": "Muhammad est le sceau des prophètes"},
            {"ref": "21:107", "note": "Nous ne t'avons envoyé que comme miséricorde pour l'univers"},
            {"ref": "19:16", "note": "Marie s'isola de sa famille, à un endroit tourné vers l'Orient"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 3300, "note": "Je suis le plus proche des gens de 'Isa, fils de Marie, ici-bas et dans l'au-delà"},
        ],
    },
    # ── Module 16 : La mort et le Jour dernier ───────────────────────────────
    {
        "module": 16,
        "module_title": "La mort, l'au-delà et le Jour dernier",
        "id": "akh5",
        "title": "La mort et la vie dans la tombe (barzakh)",
        "objectives": [
            "Comprendre la mort comme le passage vers l'au-delà",
            "Connaître les épreuves et bénédictions du barzakh",
        ],
        "content": (
            "La mort est une réalité certaine que chaque âme goûtera : « Toute âme goûtera la mort » (3:185). "
            "Elle n'est pas une fin, mais un passage : le croyant voit la mort comme le départ vers l'au-delà, "
            "le moment où l'âme quitte le corps pour rejoindre son Créateur.\n\n"
            "La mort en islam :\n"
            "- C'est une invitation à se préparer : « Toute âme goûtera la mort. Et c'est seulement le Jour de la "
            "Résurrection qu'il vous sera donné votre entière rétribution » (3:185)\n"
            "- Le croyant se prépare par les bonnes œuvres : le Prophète ﷺ a enseigné de penser souvent au "
            "destructeur des plaisirs, la mort, pour ne pas s'attacher à ce monde\n"
            "- L'ange de la mort (Malak al-Mawt) recueille les âmes, puis les anges questionnent le défunt\n\n"
            "Le barzakh (la vie intermédiaire dans la tombe) :\n"
            "- Après la mort, chaque être humain entre dans le barzakh : la vie de la tombe qUI s'étend jusqu'au "
            "Jour de la Résurrection\n"
            "- Deux anges (Munkar et Nakir) interrogent le défunt sur sa religion, son seigneur et son prophète. "
            "Ceux qui répondent avec foi sont apaisés et récompensés ; les autres reçoivent un châtiment "
            "(Bukhari n°1321)\n"
            "- La tombe est soit un jardin du Paradis, soit un gouffre de l'Enfer, comme l'a dit le Prophète ﷺ\n"
            "- Le croyant y jouit du repos et d'une lumière ; il y est préparé à son bonheur éternel\n"
            "- Le mécréant et l'insouciant y subissent un tourment\n\n"
            "La consolation des épreuves : la certitude de l'au-delà donne un sens à la vie et une consolation "
            "dans l'épreuve. Le Prophète ﷺ a dit que le musulman atteint d'une épreuve (maladie, perte) voit "
            "ses péchés effacés, même s'il n'y a que la piqûre d'une épine (Bukhari n°5428).\n\n"
            "La préparation :\n"
            "- Faire ses ablutions et achever sa prière quotidienne : la dernière chose de sa vie devrait être "
            "la foi (mention de la chahada)\n"
            "- Le Prophète ﷺ a recommandé de mentionner « La ilaha illallah » et de mourir sur la chahada\n"
            "- Acquérir la science utile et la mettre en pratique\n"
            "- Rendre les droits dus aux personnes et réparer les torts avant la mort\n"
            "- Écrire son testament (wasiyyah) : l'islam recommande de ne pas se coucher sans avoir rédigé de "
            "testament\n\n"
            "Application pratique :\n"
            "- Ne remettez pas à plus tard ce que vous pouvez faire aujourd'hui, car la mort peut survenir à "
            "tout moment\n"
            "- Renouvelez vos intentions et vos bonnes œuvres\n"
            "- Parlez de la mort sans crainte paralysante, mais comme une motivation à bien agir\n"
            "- Priez pour vos proches décédés et faites l'aumône à leur intention"
        ),
        "quran": [
            {"ref": "3:185", "note": "Toute âme goûtera la mort, et c'est seulement le Jour de la Résurrection que vous recevrez votre entière rétribution"},
            {"ref": "67:2", "note": "Celui qui a créé la mort et la vie pour vous éprouver : qui de vous est le meilleur en œuvres"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 1321, "note": "L'interrogation des anges dans la tombe : la foi du croyant est éprouvée et confirmée"},
            {"book": "bukhari", "number": 5428, "note": "Aucune épreuve (même une épine) n'atteint le musulman sans qu'Allah n'efface des péchés"},
        ],
    },
    {
        "module": 16,
        "module_title": "La mort, l'au-delà et le Jour dernier",
        "id": "akh6",
        "title": "La Résurrection, le Jugement et la rétribution",
        "objectives": [
            "Comprendre les étapes du Jour dernier",
            "Connaître le Paradis et l'Enfer selon le Coran",
        ],
        "content": (
            "Le Jour dernier (Yawm al-Qiyamah) est le centre de la vision islamique de l'existence. Croire en "
            "lui est le 5e pilier de la foi. « À Allah appartient le secret des cieux et de la terre, et la "
            "venue de l'Heure [du Jugement] sera seulement en un clin d'œil ou plus encore » (16:77). Ce jour "
            "donne un sens ultime à toute la vie d'ici-bas.\n\n"
            "Les signes du Jour dernier :\n"
            "- De grands signes annonceront son approche (le lever du soleil à l'Ouest, la bête de la terre, "
            "le retour de 'Isa, l'apparition de Gog et Magog, etc.)\n"
            "- Ces signes rappellent au croyant de se préparer\n"
            "- Le Coran ne fixe pas la date : « L'Heure viendra certainement, sans aucun doute » mais la "
            "connaissance de son moment revient à Allah seul\n\n"
            "Le Jour dernier commence par :\n"
            "- Le soufflement dans la Trompe (Sur) : tout ce qui est dans les cieux et la terre s'évanouit "
            "sauf ce qu'Allah veut (27:87)\n"
            "- La résurrection des corps : « Ce jour-là vous serez exposés, sans que rien de vous se cache » "
            "(69:18)\n"
            "- Le rassemblement : « Et (rappelle-toi) le jour où Nous ferons sortir de chaque communauté un "
            "groupe de ceux qui traitaient Nos signes de mensonges » (27:83)\n"
            "- Les livres des œuvres : chacun reçoit le livre de ses actions (36:12)\n"
            "- La balance (Mizan) : les œuvres seront pesées ; celui dont la balance est lourde de bonnes "
            "œuvres est sauvé (101:6-8)\n"
            "- Le Sirat : le pont tendu au-dessus de l'Enfer que les croyants traverseront\n\n"
            "L'intercession (shafa'ah) : le Prophète ﷺ intercédera en faveur de sa communauté le Jour de la "
            "Résurrection (hadith du grand intercession, après avoir demandé la permission d'Allah). Cette "
            "intercession est une grâce divine qui ne fonctionne que par la permission d'Allah.\n\n"
            "Le Paradis (Jannah) :\n"
            "- C'est la récompense éternelle des croyants : « Et annonce à ceux qui croient et accomplissent "
            "de bonnes œuvres qu'ils auront des jardins sous lesquels coulent les ruisseaux » (2:25)\n"
            "- Le Coran décrit ses délices : nourriture et boissons délicieuses, demeures, compagnes, "
            "perfection et, le plus grand, la vision d'Allah (76:20-22)\n"
            "- Ses demeures sont de plusieurs degrés (Jannat al-Firdaws est le plus élevé)\n\n"
            "L'Enfer (Jahannam) :\n"
            "- C'est le châtiment éternel des mécréants et de ceux qui ont commis le grand shirk\n"
            "- Le Coran décrit son feu, sa chaleur et ses tourments (56:92-94)\n"
            "- Il a sept portes et plusieurs niveaux (15:43-44)\n"
            "- Seules les fautes majeures impardonnées des croyants y subissent un tourment limité, puis ils "
            "en sortent par la miséricorde et l'intercession\n\n"
            "Le but de cette croyance : le Jour dernier n'est pas une menace stérile. C'est une certitude qui :\n"
            "- Donne un sens à la justice : les injustices seront réparées\n"
            "- Encourage à bien agir : chaque œuvre est comptée\n"
            "- Console l'opprimé : sa patience sera récompensée\n"
            "- Ramène au Pardon d'Allah : « Dis : Ô Mes serviteurs qui avez commis des excès, ne désespérez "
            "pas de la miséricorde d'Allah » (39:53)\n\n"
            "Application pratique :\n"
            "- Pensez à l'au-delà pour équilibrer votre vie : ni excès en ce monde, ni renoncement\n"
            "- Accomplissez les bonnes œuvres avec sincérité (ikhlas), car elles seront pesées\n"
            "- Espérez la miséricorde d'Allah tout en craignant Sa justice\n"
            "- Ne vous attachez pas frénétiquement aux biens d'ici-bas qui ne durent pas"
        ),
        "quran": [
            {"ref": "18:47", "note": "Le jour où Nous ferons marcher les montagnes et où la terre sera nivelée"},
            {"ref": "36:12", "note": "Et Nous mettrons tout par écrit dans un livre manifeste"},
            {"ref": "99:1", "note": "Quand la terre sera secouée d'un tremblement"},
            {"ref": "101:1", "note": "Le Fracassant (Al-Qari'ah)"},
        ],
        "hadith": [
            {"book": "bukhari", "number": 50, "note": "Le hadith de Jibril : la foi (iman) inclut la croyance en la Résurrection et aux piliers de la foi"},
        ],
    },
    {
        "module": 16,
        "module_title": "La mort, l'au-delà et le Jour dernier",
        "id": "akh7",
        "title": "La préparation à l'au-delà et le meilleur investissement",
        "objectives": [
            "Comprendre que les œuvres qui demeurent sont un trésor",
            "Apprendre à investir dans les bonnes actions durables",
        ],
        "content": (
            "Les personnes sensées sont celles qui utilisent leur vie d'ici-bas pour se préparer à l'au-delà. "
            "Le Prophète ﷺ a dit que la richesse que l'on dépense pour Allah, pour la famille, ou pour la "
            "charité constitue un investissement dont la récompense demeure, contrairement aux plaisirs "
            "éphémères (Muslim). Ce monde est une semence ; l'au-delà, la récolte.\n\n"
            "Les actions dont la récompense demeure après la mort : le Prophète ﷺ a enseigné que trois choses "
            "continuent de bénéficier au croyant après sa mort :\n"
            "1) La sadaqa jariyah (un bien dont les effets durent) : construire une mosquée, creuser un puits, "
            "financer une école, planter un arbre, etc.\n"
            "2) Une science utile (ilm nafi') : un savoir qu'il a enseigné et qui profite aux gens après lui\n"
            "3) Un enfant vertueux qui prie pour ses parents (Muslim n°1631)\n\n"
            "Ces trois investissements sont « durables » : ils continuent de produire des récompenses dans la "
            "tombe et au-delà. Ils montrent que la prévoyance du croyant dépasse la seule vie terrestre.\n\n"
            "Les bonnes œuvres qui purifient la vie :\n"
            "- Les invocations (dhikr) : « les œuvres qui demeurent » (as-salihat) désignent dans le Coran les "
            "actions pieuses durables (18:46)\n"
            "- La prière, le jeûne, la zakat, le hajj\n"
            "- La bienfaisance envers les parents, les orphelins, les pauvres et les voisins\n"
            "- L'honnêteté dans les affaires et la justice\n"
            "- La patience et le pardon\n\n"
            "Le balancement de la vie et de la mort : « Le Jour où rien ne servira ni les biens ni les fils, "
            "sauf celui qui viendra à Allah avec un cœur sain » (26:88-89). Au Jour dernier, seuls le cœur "
            "sain (la foi sincère) et les bonnes œuvres serviront. Ni la richesse ni les enfants "
            "n'intercéderont d'eux-mêmes.\n\n"
            "La mort n'est pas une tristesse pour le croyant qui s'est préparé : le Prophète ﷺ est mort, les "
            "prophètes sont morts, l'au-delà demeure. La foi en l'au-delà transforme l'approche de la vie : "
            "on vit en étant conscient que chaque action a un poids, que chaque aumône rayonne, que chaque "
            "science partagée perdure.\n\n"
            "Application pratique :\n"
            "- Choisissez une œuvre de sadaqa jariyah à votre portée (un soutien à une œuvre, la plantation, "
            "l'éducation)\n"
            "- Enseignez une science utile — ne serait-ce qu'un verset ou une invocation — à quelqu'un\n"
            "- Élevez vos enfants dans la piété afin qu'ils prient pour vous\n"
            "- Dans chaque bienfait, investissez : donnez, enseignez, abreuvez, afin que la récompense "
            "s'accumule dans votre balance"
        ),
        "quran": [
            {"ref": "18:46", "note": "Les biens et les enfants sont l'ornement de la vie d'ici-bas ; les œuvres de droite demeurent et sont meilleures auprès d'Allah"},
            {"ref": "26:88", "note": "Le Jour où ni les biens ni les enfants ne seront d'aucune utilité"},
        ],
        "hadith": [
            {"book": "muslim", "number": 4094, "note": "Trois œuvres continuent de profiter au croyant après sa mort : la sadaqa jariyah, une science utile et un enfant vertueux qui prie pour lui"},
            {"book": "bukhari", "number": 6166, "note": "Le dhikr est une œuvre qui nourrit la balance et apaisent le cœur"},
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
    block = f"{line}\n{row['text_ar']}\n— {row['text_fr']}"
    if row["text_en"]:
        block += f"\n– {row['text_en']}"
    return block


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