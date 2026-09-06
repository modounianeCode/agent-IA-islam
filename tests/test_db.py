"""Tests unitaires de l'agent : base locale, recherche, curriculum, quiz."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import cli, curriculum, db, quiz


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = db.stats()

    def test_compteurs(self):
        self.assertEqual(self.stats["surahs"], 114)
        self.assertEqual(self.stats["ayahs"], 6236)
        self.assertEqual(self.stats["books"], 17)
        self.assertGreater(self.stats["hadiths"], 50_000)

    def test_surah_meta(self):
        meta = db.get_surah_meta(2)
        self.assertIsNotNone(meta)
        self.assertEqual(meta["total_verses"], 286)

    def test_get_ayah(self):
        ayah = db.get_ayah(2, 255)
        self.assertIsNotNone(ayah)
        self.assertTrue(ayah["text_ar"])
        self.assertTrue(ayah["text_fr"])

    def test_get_hadith(self):
        h = db.get_hadith("bukhari", 1)
        self.assertIsNotNone(h)
        self.assertEqual(h["hadith_number"], 1)
        self.assertIn("intention", h["text_en"].lower())

    def test_get_hadith_introuvable(self):
        self.assertIsNone(db.get_hadith("bukhari", 999_999))

    def test_resolve_book(self):
        self.assertEqual(db.resolve_book("muslim")["slug"], "muslim")


class TestRecherche(unittest.TestCase):
    def test_search_quran_fr(self):
        rows = db.search_quran("miséricorde", limit=5)
        self.assertGreaterEqual(len(rows), 1)
        self.assertIn("miséricorde", rows[0]["text_fr"].lower())

    def test_search_quran_ar(self):
        rows = db.search_quran("الرحمن")
        self.assertTrue(rows)

    def test_search_hadith(self):
        rows = db.search_hadith("Paradise", book="bukhari", limit=5)
        self.assertTrue(rows)
        self.assertEqual(rows[0]["book_slug"], "bukhari")

    def test_resolution_aliases(self):
        self.assertEqual(cli.resolve_book_input("sahih muslim"), "muslim")
        self.assertEqual(cli.resolve_book_input("jardin des vertueux"), "riyad_assalihin")


class TestCurriculum(unittest.TestCase):
    def test_nb_lecons(self):
        self.assertGreater(len(curriculum.LESSONS), 20)

    def test_references_hadith_verifiees(self):
        checks = [
            ("bukhari", 1), ("bukhari", 50), ("bukhari", 13), ("bukhari", 52),
            ("muslim", 457), ("muslim", 1367), ("muslim", 6430),
            ("abudawud", 60), ("abudawud", 1047), ("abudawud", 4912),
            ("nasai", 2216), ("riyad_assalihin", 364),
            ("nawawi40", 2), ("mishkat_almasabih", 1259),
        ]
        for book, number in checks:
            self.assertIsNotNone(
                db.get_hadith(book, number),
                f"{book} n°{number} absent de la base",
            )

    def test_refs_vers_coran_valides(self):
        for lesson in curriculum.LESSONS:
            for ref in lesson.get("quran", []):
                surah, _, ayah = ref["ref"].partition(":")
                row = db.get_ayah(int(surah), int(ayah))
                self.assertIsNotNone(
                    row, f"Référence Coran invalide : {ref['ref']} ({lesson['id']})"
                )


class TestQuiz(unittest.TestCase):
    def test_quiz_mixte(self):
        qs = quiz.build_quiz("mixte", n=4)
        self.assertEqual(len(qs), 4)
        for q in qs:
            self.assertIn("question", q)
            self.assertGreaterEqual(len(q["options"]), 4)
            self.assertIn("answer", q)
            self.assertIn("explain", q)

    def test_quiz_coran(self):
        qs = quiz.build_quiz("coran", n=3)
        self.assertTrue(qs)
        self.assertTrue(all(q["kind"] in ("traduction", "sourate") for q in qs))

    def test_quiz_hadith(self):
        qs = quiz.build_quiz("hadith", n=3)
        self.assertTrue(qs)


class TestCli(unittest.TestCase):
    def test_coran_one_shot(self):
        out = cli.dispatch(["coran", "2:255"])
        self.assertIn("Al-Baqarah", out)
        self.assertIn("255.", out)

    def test_coran_lire_surah(self):
        out = cli.dispatch(["coran", "18", "1-3"])
        self.assertIn("Al-Kahf", out)

    def test_coran_chercher(self):
        out = cli.dispatch(["coran", "chercher", "miséricorde"])
        self.assertIn("verset(s)", out)

    def test_hadith_lookup(self):
        out = cli.dispatch(["hadith", "hadith", "bukhari", "1"])
        self.assertIn("Bukhari", out)
        self.assertIn("intention", out.lower())

    def test_hadith_livres(self):
        out = cli.dispatch(["hadith", "livres"])
        self.assertIn("17", out)

    def test_apprendre_plan(self):
        out = cli.dispatch(["apprendre"])
        self.assertIn("Module 1", out)
        self.assertIn("Progression", out)

    def test_apprendre_lecon(self):
        out = cli.dispatch(["apprendre", "lecon", "fiq2"])
        self.assertIn("La prière (salat)", out)
        self.assertIn("Mishkat al-Masabih", out)

    def test_apprendre_terminer(self):
        out = cli.dispatch(["apprendre", "terminer", "aq1"])
        self.assertIn("validée", out)


if __name__ == "__main__":
    unittest.main()