# Agent IA — Apprendre l'Islam

Agent conversationnel en ligne de commande (CLI), en français, **100 % hors-ligne** une fois la base construite. Il repose sur une base SQLite locale (Coran + 17 recueils de hadiths) et un modèle de langage local via [Ollama](https://ollama.com) — aucune clé API, aucune requête envoyée à un service externe.

> ⚠️ **Avertissement** : les réponses de l'IA sont un outil d'apprentissage, pas une source d'autorité religieuse. Les citations du Coran et des hadiths affichées proviennent **de la base locale**, jamais inventées.

---

## Fonctionnalités

| Commande                                  | Description                                                        |
| ----------------------------------------- | ------------------------------------------------------------------ |
| `coran <ref>`                             | Lire un verset avec traduction française (ex. `coran 2:255`)       |
| `coran <sourate> [debut fin]`             | Lire une plage de versets en arabe + français (ex. `coran 18 1-3`) |
| `coran chercher "<mot>"`                  | Recherche plein-texte (ex. `coran chercher "miséricorde"`)         |
| `hadith hadith <livre> <n°>`              | Lire un hadith précis (ex. `hadith hadith bukhari 1`)              |
| `hadith chercher "<mot>" [livre <livre>]` | Recherche plein-texte dans les hadiths                             |
| `hadith livres`                           | Liste des 17 recueils et leur nombre de hadiths                    |
| `hadith hasard`                           | Hadith du jour au hasard                                           |
| `apprendre`                               | Plan d'apprentissage personnalisé (8 modules, ~22 leçons)          |
| `apprendre lecon <id>`                    | Afficher une leçon avec ses références authentiques                |
| `apprendre terminer <id>`                 | Marquer une leçon comme validée (progression persistée)            |
| `quiz`                                    | QCM de révision basés sur la base locale                           |
| `demander <question>`                     | Poser une question à l'IA locale (citée sur la base)               |
| `expliquer <ref>`                         | Explication détaillée d'un verset par l'IA                         |
| `wolof coran <ref>`                       | Traduction en wolof d'un verset (ex. `wolof coran 1:1`)            |
| `wolof hadith <livre> <n°>`               | Traduction en wolof d'un hadith (ex. `wolof hadith bukhari 1`)     |
| `wolof <texte>`                           | Traduction en wolof d'un texte libre                               |
| `aide` / `quitter`                        | Aide / sortie                                                      |

Lancer sans argument ouvre un **REPL interactif** ; en passant une commande en argument, le script s'exécute en une fois.

---

## Installation

Prérequis : Linux, `python3 >= 3.12`, `curl`, `zstd`, ~7 Go d'espace libre.

```bash
./setup.sh
```

Ce script :

1. crée un environnement virtuel `.venv` et installe `requirements.txt` ;
2. télécharge les données (Coran en 3 langues + 17 recueils de hadiths) ;
3. construit `data/agent.db` (114 sourates, 6 236 versets, 50 884 hadiths) ;
4. installe le serveur **Ollama** dans `~/.local/lib/ollama` (sans sudo).

### Modèle local (génération des réponses)

Le grand modèle est **optionnel** : tout le contenu factuel (Coran, hadiths, plan, quiz) fonctionne sans lui.

```bash
~/.local/lib/ollama/bin/ollama serve &   # une fois, en arrière-plan
~/.local/lib/ollama/bin/ollama pull qwen2.5:7b   # ~4,7 Go
```

---

## Utilisation rapide

```bash
source .venv/bin/activate

python apprendre_islam.py coran 2:255
python apprendre_islam.py hadith hadith bukhari 1
python apprendre_islam.py apprendre lecon aq1
python apprendre_islam.py demander "quelle est la place de la sincérité en islam ?"
python apprendre_islam.py quiz
```

---

## Tests

```bash
python -m unittest discover -s tests -v
```

---

## Sources de données

- Coran : [`risan/quran-json`](https://github.com/risan/quran-json) v3.1.2 — texte arabe, traduction française de Muhammad Hamidullah, traduction anglaise de Saheeh International, liste des sourates en français.
- Hadiths : [`AhmedBaset/hadith-json`](https://github.com/AhmedBaset/hadith-json) v1.2.0 — 17 recueils (Sahih al-Bukhari, Sahih Muslim, Sunan Abi Dawud, Jami at-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah, Muwatta Malik, Musnad Ahmad, Sunan ad-Darimi, Riyad as-Salihin, Shamail al-Muhammadiyah, Bulugh al-Maram, Al-Adab Al-Mufrad, Mishkat al-Masabih, Les 40 hadiths d'an-Nawawi, Les 40 hadiths Qudsi, Les 40 hadiths de Shah Waliullah).

Le téléchargement a lieu **une seule fois** à l'installation ; ensuite tout est lu depuis SQLite.

---

## Architecture

```
apprendre_islam.py      Point d'entrée CLI (REPL + une commande)
app.py                  Application de facturation (Recus + Bons de livraison)
agent/
  ingest.py             Téléchargement des datasets + construction de la base
  db.py                 Schéma SQLite, normalisation, recherche FTS5
  quran.py              Lecture/recherche du Coran
  hadith.py             Lecture/recherche des hadiths
  llm.py                Client Ollama (urllib, streaming SSE) + prompt enseignant
  curriculum.py         Plan d'apprentissage (références vérifiées dans la BD)
  quiz.py               Générateur de QCM
  cli.py                Dispatcher des commandes
data/                   Données brutes téléchargées + base SQLite + progression
scripts/install_ollama.sh   Installation d'Ollama sans sudo
setup.sh                Installation complète
tests/                  Tests unitaires (base, recherche, quiz)
```

---

## Application de facturation (Recus + Bons de livraison)

Gestionnaire de reçus/quittances et bons de livraison avec export PDF et CSV. Interface web Flask, données stockées en JSON.

### Demarrage

```bash
# 1. Installer les dependances (une seule fois)
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 2. Lancer l'application
./venv/bin/python app.py
```

L'application est ensuite accessible a **http://127.0.0.1:5000**

### Fonctionnalites

- Creation de recus / quittances et bons de livraison
- Generation de documents PDF (pages A4 avec signatures)
- Export des donnees en CSV
- Consultation et suppression des documents

### Stockage

- Les donnees sont stockees dans `data/*.json`
- Les PDF generes sont dans `data/pdf/`