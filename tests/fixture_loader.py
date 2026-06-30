"""Single Felisa fixture: WindSeriesV1 (pollutants + ERA5 ws/wd)."""
from __future__ import annotations

import json
from pathlib import Path

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "felisa_munarriz.json"


def load_wind_series() -> dict:
    if not FIXTURE_PATH.is_file():
        raise FileNotFoundError(f"Missing {FIXTURE_PATH}")
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def load_series_v1() -> dict:
    """Pollutant-only view for prepare → plot tools (drops ws/wd)."""
    data = load_wind_series()
    out: dict = {"timestamps": data["timestamps"], "series": data["series"]}
    if data.get("meta"):
        out["meta"] = data["meta"]
    return out
