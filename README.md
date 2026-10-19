# Assistant islamique — Apprendre l'Islam

Assistant islamique hors ligne, pensé pour apprendre le Coran, les hadiths et les fondements de l'islam à partir d'une base locale.

> ⚠️ Outil d'apprentissage, pas une source d'autorité religieuse. Les citations sont tirées de la base locale, jamais inventées.

---

## Objectif du projet

Le projet vise à offrir un compagnon d'étude islamique fiable, en français, avec :

- lecture et recherche du Coran
- consultation de hadiths par livre ou au hasard
- plan d'apprentissage personnalisé
- quiz de révision
- services utiles en ligne : date hijri, prières, qibla, tafsir

---

## Fonctionnalités

| Commande | Description |
| --- | --- |
| `coran <ref>` | Lire un verset ou une plage de versets |
| `coran chercher "<mot>"` | Rechercher un terme dans le Coran |
| `hadith hasard` | Hadith au hasard |
| `hadith chercher "<mot>"` | Rechercher un thème dans les hadiths |
| `hadith hadith <livre> <n°>` | Consulter un hadith précis |
| `apprendre` | Voir le plan d'apprentissage |
| `apprendre lecon <id>` | Suivre une leçon |
| `quiz` | Générer un quiz de révision |
| `hijri` | Date hijri et événement islamique |
| `prieres <ville|lat lon>` | Horaires de prière |
| `qibla <lat lon>` | Direction de la qibla |
| `tafsir <ref>` | Tafsir abrégé |
| `aide` / `quitter` | Aide et sortie |

---

## Installation

Prérequis : Linux, Python 3.12+, `curl`, `zstd`.

```bash
./setup.sh
```

Le script crée un environnement virtuel, installe les dépendances, télécharge les données et construit la base SQLite locale.

---

## Interface graphique web

Une interface web locale complète est disponible, en plus de la ligne de commande.

```bash
source .venv/bin/activate
python webapp.py
```

Puis ouvrir <http://127.0.0.1:5000>.

Options utiles :

```bash
python webapp.py --port 8080        # changer le port
python webapp.py --host 0.0.0.0     # rendre accessible sur le réseau local
python webapp.py --debug            # mode développement Flask
```

L'interface propose :

- **Accueil** : progression, verset du jour, hadith du jour, accès rapide
- **Coran** : lecture par sourate ou plage de versets, recherche française/arabe, tafsir à la demande
- **Hadiths** : recherche thématique, consultation par recueil et numéro, hadith au hasard
- **Apprendre** : plan par modules, leçons, références Coran/hadiths, validation de la progression
- **Quiz** : quiz Coran, hadiths ou mixte, correction et explication immédiates
- **Outils** : date hijri, horaires de prière, qibla et tafsir (connexion Internet requise)

Le rendu est responsive (mobile et bureau) et propose un thème clair/sombre. Le serveur Flask est prévu pour un usage local ; pour un déploiement public, utilisez un serveur WSGI de production.

---

## Utilisation

### Mode interactif

```bash
source .venv/bin/activate
python apprendre_islam.py
```

### Commande unique

```bash
source .venv/bin/activate
python apprendre_islam.py coran 2:255
python apprendre_islam.py hadith hadith bukhari 1
python apprendre_islam.py quiz coran 10
python apprendre_islam.py prieres Dakar Senegal
python apprendre_islam.py tafsir 2:255
```

---

## Architecture

```text
apprendre_islam.py      Point d'entrée CLI
webapp.py               Point d'entrée de l'interface web
templates/              Templates Jinja2 de l'interface web
static/                 CSS et JavaScript de l'interface web
agent/
  __init__.py           Version et package du projet
  __main__.py           Exécution via python -m agent
  cli.py                Interface de commandes et REPL
  web.py                Application Flask et routes de l'interface
  db.py                 Base SQLite + recherche FTS5
  ingest.py             Téléchargement des données et construction de la base
  quran.py              Lecture et recherche du Coran
  hadith.py             Recherche et consultation des hadiths
  api.py                API islamique externe (hijri, prière, qibla, tafsir)
  curriculum.py         Plan d'apprentissage
  quiz.py               Générateur de quiz
  llm.py                Client Ollama local

data/
  raw/                  Données sources brutes
  agent.db              Base locale SQLite
  progress.json         Progression de l'utilisateur

setup.sh                Installation du projet
scripts/install_ollama.sh  Script d'installation utile au besoin
requirements.txt        Dépendances Python
pyproject.toml          Packaging Python du projet
tests/                  Vérifications unitaires du système
```

---

## Sources de données

- Coran : `risan/quran-json` v3.1.2
- Hadiths : `AhmedBaset/hadith-json` v1.2.0

Les données sont téléchargées une fois puis exploitées localement depuis SQLite.

---

## Qualité et tests

```bash
python -m unittest discover -s tests -v
```

Le projet possède une suite de tests couvrant les commandes, la base SQLite, les validations et la logique de progression.

---

## État de production

Cette version est pensée comme une base stable et claire pour un assistant islamique autonome, sans modules annexes, avec une organisation plus propre et un point d’entrée standardisé.
