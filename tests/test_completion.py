"""Tests de la complétion par TAB (readline).

On teste directement la fonction pure `_complete_candidates` (pas de
readline, pas de réseau).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import cli


class TestCompletionsCommande(unittest.TestCase):
    def test_premier_mot(self):
        self.assertIn("hijri", cli._complete_candidates("", "hi"))
        self.assertIn("hadith", cli._complete_candidates("", "ha"))
        self.assertIn("coran", cli._complete_candidates("", "c"))
        self.assertNotIn("qibla", cli._complete_candidates("", "hi"))

    def test_insensible_a_la_casse(self):
        self.assertIn("coran", cli._complete_candidates("", "C"))


class TestCompletionsSousCommandes(unittest.TestCase):
    def test_coran(self):
        res = cli._complete_candidates("coran ", "")
        self.assertIn("chercher", res)
        self.assertIn("list", res)

    def test_hadith(self):
        res = cli._complete_candidates("hadith ", "")
        for sub in ("hasard", "chercher", "livre", "livres"):
            self.assertIn(sub, res)
        self.assertEqual(cli._complete_candidates("hadith ha", "ha"), ["hadith", "hasard"])

    def test_quiz(self):
        res = cli._complete_candidates("quiz c", "c")
        self.assertEqual(res, ["coran"])

    def test_sourates(self):
        res = cli._complete_candidates("sourates i", "i")
        self.assertEqual(res, ["importantes"])


class TestCompletionsEntites(unittest.TestCase):
    def test_lecons(self):
        res = cli._complete_candidates("apprendre lecon ", "")
        self.assertIn("fiq1", res)
        self.assertIn("akh7", res)
        res2 = cli._complete_candidates("apprendre lecon fi", "fi")
        self.assertTrue(all(x.startswith("fi") for x in res2))
        self.assertTrue(res2)

    def test_prophetes(self):
        res = cli._complete_candidates("histoires yu", "yu")
        self.assertIn("yusuf", res)
        res2 = cli._complete_candidates("histoires mo", "mo")
        self.assertNotEqual(res2, [])

    def test_livres_hadith(self):
        res = cli._complete_candidates("hadith hasard bu", "bu")
        self.assertIn("bukhari", res)
        res2 = cli._complete_candidates("hadith chercher misericorde livre ", "")
        self.assertIn("muslim", res2)
        res3 = cli._complete_candidates("hadith hadith tirm", "tirm")
        self.assertIn("tirmidhi", res3)


class TestCompletionsLibre(unittest.TestCase):
    def test_texte_libre_sans_suggestion(self):
        # demander / expliquer / prieres : aucun mot-clé à proposer
        self.assertEqual(cli._complete_candidates("demander bonjour", "bonjour"), [])
        self.assertEqual(cli._complete_candidates("prieres Dakar", "Dakar"), [])


if __name__ == "__main__":
    unittest.main()