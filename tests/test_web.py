"""Tests de l'interface web locale (Flask test client).

Aucun réseau : les appels aux API islamiques sont simulés.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import api, curriculum
from agent.web import app


HIJRI_DATA = {
    "data": {
        "gregorian": {"formatted": "Monday, September 07, 2026"},
        "hijri": {
            "formatted": "25 ربيع الأول 1448 AH",
            "month_name_arabic": "رَبِيع الْأَوَّل",
            "month_name": "Rabi' al-awwal",
            "era": "AH (After Hijra)",
        },
        "islamic_info": {"note": "dates may vary"},
    }
}
EVENTS_DATA = {
    "data": {"next_event": {"name": "Isra and Mi'raj", "hijri_date": "27 Rajab 1448 AH"}}
}
PRAYER_DATA = {
    "data": {
        "date": "2026-09-07",
        "calculation_method": "MuslimWorldLeague",
        "madhab": "Shafi",
        "prayer_times": {
            "imsak": "05:36", "fajr": "05:46", "sunrise": "06:58",
            "dhuhr": "13:09", "asr": "16:24", "maghrib": "19:17", "isha": "20:25",
        },
        "current_status": {
            "current_prayer": "maghrib",
            "next_prayer": "isha",
            "time_until_next": "38 minutes",
        },
    }
}
GEO_RESULT = {
    "results": [
        {
            "name": "Dakar",
            "latitude": 14.6937,
            "longitude": -17.44406,
            "timezone": "Africa/Dakar",
            "country": "Sénégal",
            "country_code": "SN",
        }
    ]
}
QIBLA_DATA = {
    "data": {
        "qibla_direction": 73.93,
        "compass_bearing": "ENE",
        "location": {"latitude": 14.69, "longitude": -17.44},
        "distance_km": 6069.18,
        "distance_miles": 3771.21,
    }
}
TAFSIR_DATA = {
    "data": {
        "tafsir": {
            "text": "The Virtue of Ayat Al-Kursi. This is the greatest Ayah in the Book of Allah."
        }
    }
}


class TestPagesHorsLigne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def assert_ok(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, url)
        self.assertIn(b"Apprendre l'Islam", response.data)

    def test_accueil(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Verset du jour", response.data)
        self.assertIn(b"Hadith du jour", response.data)

    def test_coran_lecture(self):
        self.assert_ok("/coran")
        response = self.client.get("/coran?sourate=2&debut=255&fin=255")
        self.assertIn("Point de divinité".encode("utf-8"), response.data)
        self.assertIn(b'id="v-2-255"', response.data)

    def test_coran_recherche(self):
        response = self.client.get("/coran?q=miséricorde")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"verset(s)", response.data)

    def test_hadiths_liste(self):
        response = self.client.get("/hadiths")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sahih al-Bukhari", response.data)

    def test_hadith_fiche(self):
        response = self.client.get("/hadiths?livre=bukhari&numero=1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("intentions".encode("utf-8"), response.data)

    def test_hadith_recherche(self):
        response = self.client.get("/hadiths?q=patience")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"hadith(s)", response.data)

    def test_apprendre(self):
        response = self.client.get("/apprendre")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Plan d'apprentissage", response.data)
        response = self.client.get("/apprendre/aq1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tawhid", response.data)

    def test_quiz_page(self):
        self.assert_ok("/quiz")

    def test_outils_page(self):
        self.assert_ok("/outils")

    def test_404(self):
        response = self.client.get("/page-inexistante")
        self.assertEqual(response.status_code, 404)


class TestQuizApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_quiz_json(self):
        response = self.client.get("/api/quiz?type=coran&n=3")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(len(payload["questions"]), 3)
        question = payload["questions"][0]
        for key in ("question", "options", "answer", "explain"):
            self.assertIn(key, question)
        self.assertIn(question["answer"], range(len(question["options"])))

    def test_quiz_type_invalide_retombe_sur_mixte(self):
        response = self.client.get("/api/quiz?type=inconnu&n=2")
        self.assertEqual(response.status_code, 200)


class TestCompletionWeb(unittest.TestCase):
    def test_terminer_lecon(self):
        with tempfile.TemporaryDirectory() as tmp:
            progress_file = Path(tmp) / "progress.json"
            progress_file.write_text(
                json.dumps({"completed": [], "last": None}), encoding="utf-8"
            )
            with mock.patch.object(curriculum, "PROGRESS_FILE", progress_file):
                client = app.test_client()
                response = client.post(
                    "/apprendre/aq1/terminer", follow_redirects=True
                )
                self.assertEqual(response.status_code, 200)
                saved = json.loads(progress_file.read_text(encoding="utf-8"))
                self.assertIn("aq1", saved["completed"])


class TestOutilsEnLigne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_hijri(self):
        def fake_ummah(path):
            return EVENTS_DATA if path.startswith("/api/islamic-events") else HIJRI_DATA

        with mock.patch.object(api, "_ummah", side_effect=fake_ummah):
            response = self.client.post("/outils", data={"action": "hijri"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("25 ربيع الأول 1448 AH".encode("utf-8"), response.data)
        self.assertIn(b"Isra and Mi&#39;raj", response.data)

    def test_prieres(self):
        with mock.patch.object(api, "_http_json", return_value=GEO_RESULT), mock.patch.object(
            api, "_ummah", return_value=PRAYER_DATA
        ):
            response = self.client.post(
                "/outils", data={"action": "prieres", "city": "Dakar", "country": "Senegal"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Aube (Fajr)", response.data)
        self.assertIn(b"05:46", response.data)

    def test_qibla(self):
        with mock.patch.object(api, "_ummah", return_value=QIBLA_DATA):
            response = self.client.post(
                "/outils", data={"action": "qibla", "lat": "14.69", "lon": "-17.44"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"73.93", response.data)
        self.assertIn(b"ENE", response.data)

    def test_tafsir(self):
        with mock.patch.object(api, "_ummah", return_value=TAFSIR_DATA):
            response = self.client.post("/outils", data={"action": "tafsir", "ref": "2:255"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Virtue of Ayat Al-Kursi", response.data)

    def test_tafsir_ref_invalide(self):
        response = self.client.post("/outils", data={"action": "tafsir", "ref": "2:999999"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"n&#39;existe pas", response.data)


if __name__ == "__main__":
    unittest.main()
