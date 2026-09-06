# Aide - Agent IA Apprendre l'Islam

Guide de reference de toutes les commandes disponibles.

## Lancement

```bash
# Mode interactif (REPL)
python apprendre_islam.py

# Mode one-shot (une seule commande)
python apprendre_islam.py <commande> [arguments]
```

## Commandes Coran

| Commande | Description |
|---|---|
| `coran <sourate>` | Vue d'ensemble d'une sourate |
| `coran <sourate>:<verset>` | Verset precis (ex: `coran 2:255`) |
| `coran <sourate> <debut>-<fin>` | Plage de versets (ex: `coran 18 1-10`) |
| `coran chercher <terme>` | Rechercher dans la traduction francaise |
| `coran list` | Lister les 114 sourates |

## Commandes Hadith

| Commande | Description |
|---|---|
| `hadith hasard` | Hadith aleatoire |
| `hadith hasard <livre>` | Hadith aleatoire dans un livre precis |
| `hadith hadith <livre> <n>` | Hadith precis (ex: `hadith hadith bukhari 1`) |
| `hadith chercher <terme>` | Rechercher dans les hadiths |
| `hadith chercher <terme> livre <livre>` | Rechercher dans un livre precis |
| `hadith livre <slug>` | Fiche d'information sur un livre |
| `hadith livres` | Lister tous les livres de hadiths |

En mode interactif, une traduction/explication IA est proposee pour chaque hadith consulte.

## Commandes Apprentissage

| Commande | Alias | Description |
|---|---|---|
| `apprendre` | `learn` | Afficher le plan d'apprentissage et la progression |
| `apprendre lecon <id>` | | Suivre une lecon (ex: `apprendre lecon fiq2`) |
| `apprendre terminer <id>` | | Valider une lecon terminee |

## Commandes Quiz

| Commande | Description |
|---|---|
| `quiz` | Quiz melange, 5 questions |
| `quiz coran` | Quiz Coran, 5 questions |
| `quiz hadith` | Quiz Hadith, 5 questions |
| `quiz mixte` | Quiz melange, 5 questions |
| `quiz <nombre>` | Quiz melange avec N questions (ex: `quiz 10`) |
| `quiz coran <nombre>` | Quiz Coran avec N questions |
| `quiz hadith <nombre>` | Quiz Hadith avec N questions |

Un score est affiche a la fin du quiz avec un retour base sur la performance.

## Commandes IA (assistant intelligent)

| Commande | Alias | Description |
|---|---|---|
| `demander <question>` | `demande`, `ask` | Poser une question sur le corpus islamique |
| `expliquer <sourate:verset>` | | Explication pedagogique d'un verset par l'IA |

Ces commandes necessitent le serveur Ollama avec le modele `qwen2.5:7b`.

## Commandes Wolof

| Commande | Description |
|---|---|
| `wolof coran <ref>` | Traduire un verset en wolof (ex: `wolof coran 1:1`) |
| `wolof hadith <livre> <n>` | Traduire un hadith en wolof (ex: `wolof hadith bukhari 1`) |
| `wolof <texte>` | Traduire un texte libre en wolof |
| `wolof aide` | Aide wolof |

En mode interactif, apres avoir consulte un hadith, vous pouvez choisir une traduction en francais (f) ou en wolof (w).

Ces traductions sont pedagogiques et produites par l'IA locale. Le wolof est la langue du Senegal.

## Commandes systeme

| Commande | Alias | Description |
|---|---|---|
| `aide` | `help`, `?` | Afficher l'aide |
| `quitter` | `exit`, `quit` | Quitter le programme |

## Depuis le terminal

```bash
# Executer une seule commande
python apprendre_islam.py coran 2:255
python apprendre_islam.py hadith hadith bukhari 1
python apprendre_islam.py apprendre lecon aq1
python apprendre_islam.py demander "quelle est la place de la sincerite en islam ?"
python apprendre_islam.py quiz coran 10
python apprendre_islam.py expliquer 2:255
python apprendre_islam.py wolof coran 1:1
python apprendre_islam.py wolof hadith bukhari 1
```
