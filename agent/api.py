"""
Accès en ligne aux API islamiques (UmmahAPI + géocodage Open-Meteo).
Ces commandes nécessitent une connexion Internet. Le reste de l'agent
reste 100 % hors-ligne (base locale SQLite).

"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

UMMAHAPI = "https://ummahapi.com"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
TIMEOUT = 20


class ApiError(RuntimeError):
    """Erreur réseau, HTTP ou réponse invalide de l'API."""


def _http_json(url: str) -> Any:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
            raw = resp.read()
    except Exception as exc:
        raise ApiError(
            f"Impossible de contacter l'API ({exc.__class__.__name__}). "
            "Vérifie ta connexion Internet et réessaie."
        ) from exc
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ApiError("Réponse de l'API illisible.") from exc


def _ummah(path: str) -> dict[str, Any]:
    payload = _http_json(f"{UMMAHAPI}{path}")
    if not payload.get("success", True):
        raise ApiError(payload.get("message") or payload.get("error") or "Erreur de l'API UmmahAPI.")
    return payload


def hijri() -> dict[str, Any]:
    """Date hijri du jour : {hijri, gregorian, islamic_info}."""
    return _ummah("/api/today-hijri")["data"]


def islamic_events() -> dict[str, Any]:
    """Événements islamiques : {current_hijri_date, next_event, events[]}."""
    return _ummah("/api/islamic-events")["data"]


def qibla(lat: float, lng: float) -> dict[str, Any]:
    """Direction de la Qibla pour une position (lat, lng)."""
    return _ummah(f"/api/qibla?lat={lat}&lng={lng}")["data"]


def prayer_times(lat: float, lng: float, timezone: str | None = None) -> dict[str, Any]:
    """Horaires de prière : {prayer_times, current_status, date, method…}."""
    query = urllib.parse.urlencode({"lat": lat, "lng": lng})
    if timezone:
        query += "&" + urllib.parse.urlencode({"timezone": timezone})
    return _ummah(f"/api/prayer-times?{query}")["data"]


def tafsir(surah: int, ayah: int) -> dict[str, Any]:
    """Tafsir Ibn Kathir (abrégé, en anglais) d'un verset."""
    return _ummah(f"/api/tafsir/ibn_kathir/surah/{surah}/ayah/{ayah}")["data"]


def geocode(city: str, country: str | None = None) -> dict[str, Any] | None:
    """Géocode une ville (Open-Meteo) → dict avec latitude/longitude/timezone."""
    query = urllib.parse.urlencode(
        {"name": city, "count": 5, "language": "fr", "format": "json"}
    )
    payload = _http_json(f"{GEOCODE_URL}?{query}")
    results = payload.get("results")
    if not results:
        return None
    if country:
        c = country.strip().lower()
        for result in results:
            if (
                str(result.get("country", "")).lower() == c
                or str(result.get("country_code", "")).lower() == c
            ):
                return result
    return results[0]
