"""Tests de la validation anti-hallucination des réponses IA.

Ces validations vérifient que les citations (Coran : sourate:verset,
Hadith : livre + n°) pointent bien vers des éléments réellement présents
dans la base locale, et signalent toute référence inventée.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import db, llm


class TestValidationCoran(unittest.TestCase):
    def test_verset_valide_inchange(self):
        text = "« Allah, point de divinité à part Lui » (Coran 2:255)"
        out = llm.validate_quran_refs(text)
        self.assertNotIn("⚠️", out)
        self.assertEqual(out, text)

    def test_verset_inexistant_signale(self):
        text = "Citation inventée (Coran 2:999)"
        out = llm.validate_quran_refs(text)
        self.assertIn("⚠️", out)
        self.assertIn("2:999", out)

    def test_sourate_inexistante_signale(self):
        text = "Réf (Coran 115:1)"
        out = llm.validate_quran_refs(text)
        self.assertIn("⚠️", out)
        self.assertIn("115", out)

    def test_verset_hors_limite_signale(self):
        # Al-Baqarah (2) a 286 versets ; 2000 est hors limite
        out = llm.validate_quran_refs("(Coran 2:2000)")
        self.assertIn("⚠️", out)

    def test_plusieurs_refs_valides(self):
        text = "Versets 1:1 et 18:10 sont valides."
        out = llm.validate_quran_refs(text)
        self.assertNotIn("⚠️", out)


class TestValidationHadith(unittest.TestCase):
    def test_hadith_valide_inchange(self):
        text = "Rapporté par al-Bukhari n°1"
        out = llm.validate_hadith_refs(text)
        self.assertNotIn("⚠️", out)

    def test_hadith_inexistant_signale(self):
        text = "Rapporté par Bukhari n°999999"
        out = llm.validate_hadith_refs(text)
        self.assertIn("⚠️", out)

    def test_aucune_ref_inchange(self):
        text = "Il faut être sincère dans son intention."
        out = llm.validate_hadith_refs(text)
        self.assertEqual(out, text)

    def test_numero_seul_masque(self):
        # Un numéro isolé sans livre n'est pas traité par la validation livre/n°
        out = llm.validate_hadith_refs("Quelques versets comme 2:255")
        self.assertNotIn("hadith à vérifier", out)


class TestValidationGlobale(unittest.TestCase):
    def test_mix_valide(self):
        text = "Coran 2:255 et rapporté par Muslim n°1."
        out = llm.validate_generated(text)
        self.assertNotIn("⚠️", out)

    def test_mix_invalide(self):
        text = "Coran 2:999 et rapporté par Bukhari n°999999."
        out = llm.validate_generated(text)
        self.assertIn("⚠️", out)

    def test_fonctions_db_existence(self):
        self.assertTrue(db.ayah_exists(2, 255))
        self.assertFalse(db.ayah_exists(2, 999))
        self.assertTrue(db.hadith_exists("bukhari", 1))
        self.assertFalse(db.hadith_exists("bukhari", 999999))
        self.assertEqual(db.surah_total_verses(2), 286)
        self.assertIsNone(db.surah_total_verses(999))


if __name__ == "__main__":
    unittest.main()
