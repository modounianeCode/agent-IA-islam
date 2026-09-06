# Améliorations futures — Agent IA « Apprendre l'Islam »

Liste de pistes d'amélioration (non classées par ordre de priorité). Ce fichier sert de
référence pour les prochaines itérations du projet.

---

## 1. Fiabilité du contenu (le plus important)

- **Anti-hallucination complète** : le modèle local `qwen2.5:7b` invente encore du *contenu*
  de hadith (il paraphrase, attribue des récits au Prophète ﷺ). Le filtre actuel (`strict=True`)
  masque « livre + numéro » mais pas le contenu. Piste : vérification post-génération par
  recherche FTS des citations produites, ou refus automatique si aucune source locale ne
  correspond.
- **Détection de citations non fournies** : bien que le prompt l'interdise, le modèle peut
  citer un verset non présent dans le contexte (ex. « Coran 2:117 »). Amélioration : valider
  chaque référence `sourate:verset` citée dans la réponse contre `data/agent.db`.
- **Ajout d'une traduction française des hadiths** : la BD ne contient que l'arabe et
  l'anglais. L'IA traduit oralement mais la traduction est aléatoire. Deux options :
  1. ajouter une traduction françaises officielle (usage restreint/licence), ou
  2. pré-générer les traductions IA hors-ligne et les stocker en cache.

## 2. Fonctionnalités pédagogiques

- **Quiz intelligents** : questions côté contexte/leçon (`apprendre lecon X` → quiz sur X),
  plus de types (vrai/faux, association), scores persistés.
- **Évaluation de la progression** : grille de niveau, révisions espacées (leitner) selon
  les leçons validées dans `data/progress.json`.
- **Vocabulaire arabe** : mémoriser + interroger le vocabulaire du Coran (radicaux, sens),
  conjugaison des termes.
- **Tafsir** : ajouter un résumé de tafsir (lignée de Ma'arif/Al-Muyassar) pour chaque sourate.
- **Histoires des prophètes, noms d'Allah (99)**, adhkar du matin/soir avec rappels
  programmables.
- **Mode « répétition »** : lecture audio (TTS) ou timer de révision.

## 3. Expérience utilisateur

- **Interface TUI** (ex. `rich`, `textual`, ou simple coloration ANSI) pour l'affichage des
  versets et hadiths (l'interface est actuellement en texte brut).
- **Export** : PDF/HTML d'un module ou du plan complet pour impression.
- **Raccourcis clavier** dans le REPL (flèches/historique via `readline`), autocomplétion
  des commandes.
- **Multilingue** : bascule francais/anglais de l'interface (le contenu Coran FR/EN existe déjà).
- **Veille de la progression** : barre de progression visuelle dans `apprendre`.

## 4. Performance et modèle

- **Modèle plus léger** (`qwen2.5:3b` ou `gemma3:4b`) en fallback quand CPU lent —
  évaluation de la vitesse (actuellement ~3-10 s/34 tokens, 100 % CPU).
- **GPU/CUDA** : détection de GPU pour accélérer la génération.
- **Longueur des réponses** : limiter `num_predict` / température pour des réponses plus
  courtes et fiables.
- **Indexation** : ajouter un index `bm25` ou précharger le contexte pour un grounding
  plus précis.

## 5. Données

- **Compléter la BD** : tafsir, asbab an-nuzul, biographie des rapporteurs, hadiths en
  français (voir §1).
- **Chapitre arabe des recueils** : `chapter_en` existe ; ajouter la traduction FR des
  chapitres pour contextiser.
- **Nettoyage** : certains `idInBook` des livres (ex. Musnad Ahmad, 1374 hadiths) semblent
  incomplets/variables — à auditer.
- **Mise à jour des datasets** : scripts de re-téléchargement versionnés (jsDelivr cache).

## 6. Qualité et tests

- **CI** : GitHub Actions exécutant `python -m unittest discover -s tests` avec une BD
  d'exemple réduite.
- **Tests du LLM** : fixtures de réponses, test de non-hallucination (recherche des
  références citées dans la BD).
- **Lint/typage** : `ruff`, `mypy`, pré-commit.
- **Couverture** : augmenter la couverture des modules `ingest`, `llm`, `cli` (actuellement
  tests sur db/curriculum/quiz).

## 7. Installation et distribution

- **Packaging** : `pyproject.toml` + `pip install .`, console entry point `islam`.
- **Installer système** : uniqement via `~/.local` ; proposer un paquet apt/flatpak ? Non
  prioritaire (doit rester hors-ligne, sans dépendance réseau à l'exécution).
- **`make`** : cibles `setup`, `build`, `test`, `run`.

---

## Problèmes connus à traiter en priorité

| Problème | Impact | Suggestion |
|---|---|---|
| Hallucination du contenu hadith par l'IA | Fiabilité | Vérification FTS post-génération (§1) |
| Références « Coran x:y » non fournies | Fiabilité | Validation contre la BD |
| Musnad Ahmad : seulement 1374 hadiths | Données | Auditer la source / idInBook |
| Pas de traduction FR des hadiths | UX | Cache de traductions IA (§1) |
| Génération lente sur CPU | UX | Fallback modèle 3B ou GPU (§4) |