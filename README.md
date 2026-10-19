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
agent/
  __init__.py           Version et package du projet
  __main__.py           Exécution via python -m agent
  cli.py                Interface de commandes et REPL
  db.py                 Base SQLite + recherche FTS5
  ingest.py             Téléchargement des données et construction de la base
  quran.py              Lecture et recherche du Coran
  hadith.py             Recherche et consultation des hadiths
  api.py                API islamique externe (hijri, prière, qibla, tafsir)
  curriculum.py         Plan d'apprentissage
  quiz.py               Générateur de quiz

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
