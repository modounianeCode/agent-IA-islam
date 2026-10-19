"""Tests des commandes en ligne (API islamiques) — réseau simulé.

Ces tests ne font AUCUN appel réseau : les fonctions HTTP de agent.api
sont simulées (unittest.mock) pour que la suite reste 100 % hors-ligne.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import api, cli

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
    "data": {
        "next_event": {"name": "Isra and Mi'raj", "hijri_date": "27 Rajab 1448 AH"}
    }
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
        "current_status": {"current_prayer": "maghrib", "next_prayer": "isha", "time_until_next": "38 minutes"},
    }
}

GEO_RESULT = {
    "results": [
        {
            "name": "Dakar", "latitude": 14.6937, "longitude": -17.44406,
            "timezone": "Africa/Dakar", "country": "Sénégal", "country_code": "SN",
        }
    ]
}

QIBLA_DATA = {
    "data": {
        "qibla_direction": 73.93, "compass_bearing": "ENE",
        "location": {"latitude": 14.69, "longitude": -17.44},
        "distance_km": 6069.18, "distance_miles": 3771.21,
    }
}

TAFSIR_DATA = {
    "data": {
        "verse_key": "2:255",
        "tafsir": {
            "key": "ibn_kathir", "name": "Ibn Kathir (Abridged)",
            "language": "english", "author": "Hafiz Ibn Kathir",
            "text": "The Virtue of Ayat Al-Kursi. This is the greatest Ayah in the Book of Allah.",
        },
    }
}


class TestHijri(unittest.TestCase):
    def test_hijri_format(self):
        def fake_ummah(path):
            if path.startswith("/api/islamic-events"):
                return EVENTS_DATA
            return HIJRI_DATA

        with mock.patch.object(api, "_ummah", side_effect=fake_ummah):
            out = cli._hijri()
        self.assertIn("📅 Date islamique", out)
        self.assertIn("25 ربيع الأول 1448 AH", out)
        self.assertIn("Isra and Mi'raj", out)


class TestPrayerTimes(unittest.TestCase):
    def test_prayer_times_ville(self):
        with mock.patch.object(api, "_http_json", return_value=GEO_RESULT), mock.patch.object(
            api, "_ummah", return_value=PRAYER_DATA
        ):
            out = cli._prayer_times(["Dakar", "Senegal"])
        self.assertIn("🕌 Horaires de prière", out)
        self.assertIn("Dakar (Sénégal)", out)
        self.assertIn("Aube (Fajr)", out)
        self.assertIn("05:46", out)
        self.assertIn("isha", out)

    def test_prayer_times_coordonnees(self):
        with mock.patch.object(api, "_ummah", return_value=PRAYER_DATA):
            out = cli._prayer_times(["14.69", "-17.44"])
        self.assertIn("Horaires de prière", out)
        self.assertIn("Midi (Dhuhr)", out)

    def test_prayer_times_ville_introuvable(self):
        with mock.patch.object(api, "_http_json", return_value={"results": []}):
            out = cli._prayer_times(["Atlantide"])
        self.assertIn("introuvable", out)

    def test_prayer_times_sans_args(self):
        out = cli._prayer_times([])
        self.assertIn("Usage", out)


class TestQibla(unittest.TestCase):
    def test_qibla_format(self):
        with mock.patch.object(api, "_ummah", return_value=QIBLA_DATA):
            out = cli._qibla(["14.69", "-17.44"])
        self.assertIn("🧭 Direction de la Qibla", out)
        self.assertIn("73.93", out)
        self.assertIn("ENE", out)

    def test_qibla_mauvaise_usage(self):
        out = cli._qibla([])
        self.assertIn("Usage", out)
        out2 = cli._qibla(["bonjour"])
        self.assertIn("Usage", out2)


class TestTafsir(unittest.TestCase):
    def test_tafsir_format(self):
        with mock.patch.object(api, "_ummah", return_value=TAFSIR_DATA):
            out = cli._tafsir(["2:255"])
        self.assertIn("Tafsir Ibn Kathir", out)
        self.assertIn("Virtue of Ayat Al-Kursi", out)

    def test_tafsir_sourate_seule(self):
        with mock.patch.object(api, "_ummah", return_value=TAFSIR_DATA):
            out = cli._tafsir(["2"])
        self.assertIn("Coran 2:1", out)

    def test_tafsir_ref_invalide(self):
        out = cli._tafsir(["2:999999"])
        self.assertIn("n'existe pas", out)
        out2 = cli._tafsir(["abc"])
        self.assertIn("Référence incomprise", out2)

    def test_tafsir_sans_args(self):
        out = cli._tafsir([])
        self.assertIn("Usage", out)


class TestErreurReseau(unittest.TestCase):
    def test_erreur_api_tres_transmise(self):
        with mock.patch.object(api, "_ummah", side_effect=api.ApiError("réseau coupé")):
            out = cli._qibla(["14.69", "-17.44"])
        self.assertIn("réseau coupé", out)


class TestDispatchEnLigne(unittest.TestCase):
    def test_dispatch_commande_inconnue(self):
        def fake_ummah(path):
            if path.startswith("/api/qibla"):
                return QIBLA_DATA
            if path.startswith("/api/prayer-times"):
                return PRAYER_DATA
            return HIJRI_DATA

        with mock.patch.object(api, "_ummah", side_effect=fake_ummah), mock.patch.object(
            api, "_http_json", return_value=GEO_RESULT
        ):
            self.assertIsInstance(cli.dispatch(["hijri"]), str)
            self.assertIsInstance(cli.dispatch(["qibla", "10", "10"]), str)
            self.assertIsInstance(cli.dispatch(["prieres", "Dakar"]), str)
            self.assertNotIn("inconnue", cli.dispatch(["hijri"]).lower())


if __name__ == "__main__":
    unittest.main()