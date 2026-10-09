#!/usr/bin/env python3
"""Build UOGW daily research summary + science package (stdlib only)."""
from __future__ import annotations

import glob
import json
import os
import statistics
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone


def load(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def safe_mean(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(statistics.mean(vals), 3) if vals else None


def safe_minmax(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    if not vals:
        return None, None
    return min(vals), max(vals)


def main() -> int:
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    os.makedirs(f"data/entries/{date}", exist_ok=True)
    os.makedirs("data/latest", exist_ok=True)
    os.makedirs("status", exist_ok=True)
    os.makedirs(f"snapshots/{date}", exist_ok=True)
    os.makedirs("layers/research", exist_ok=True)

    cities = load("data/latest/global-cities.json") or load("layers/ground/samples/cities-latest.json") or {}
    ndbc = load("data/latest/ndbc-realtime.json") or load("layers/marine/ndbc/realtime-latest.json") or {}
    casey = load("data/latest/casey-hourly.json") or load("layers/ground/casey/latest.json") or {}
    igra_status = load("status/igra.json") or {}
    ndbc_status = load("status/ndbc.json") or {}
    samples_status = load("status/global-samples.json") or {}
    ground_status = load("status/msds-ground.json") or {}
    intl_status = load("status/international.json") or {}
    ghcn = load("layers/ground/ghcn/stations-index-latest.json") or {}
    intl = load("layers/ground/international/sources-latest.json") or {}
    catalog = load("catalog/catalog.json") or {}

    research_cities = [
        ("casey_il", 39.2992, -87.9925, "America/Chicago"),
        ("chicago_il", 41.8781, -87.6298, "America/Chicago"),
        ("london_uk", 51.5074, -0.1278, "Europe/London"),
        ("tokyo_jp", 35.6762, 139.6503, "Asia/Tokyo"),
        ("sydney_au", -33.8688, 151.2093, "Australia/Sydney"),
        ("nairobi_ke", -1.2921, 36.8219, "Africa/Nairobi"),
        ("sao_paulo_br", -23.5505, -46.6333, "America/Sao_Paulo"),
        ("berlin_de", 52.52, 13.405, "Europe/Berlin"),
        ("mumbai_in", 19.076, 72.8777, "Asia/Kolkata"),
        ("reykjavik_is", 64.1466, -21.9426, "Atlantic/Reykjavik"),
    ]
    daily_climate = []
    for cid, lat, lon, tz in research_cities:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={yesterday}&end_date={yesterday}"
            "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,"
            "windspeed_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration"
            f"&timezone={urllib.parse.quote(tz)}&windspeed_unit=ms"
        )
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Midwest-Stratospheric/UOGW-research"}),
                timeout=60,
            ) as resp:
                data = json.loads(resp.read().decode())
            d = data.get("daily") or {}
            daily_climate.append({
                "id": cid, "lat": lat, "lon": lon, "date": yesterday, "ok": True,
                "temperature_max_c": (d.get("temperature_2m_max") or [None])[0],
                "temperature_min_c": (d.get("temperature_2m_min") or [None])[0],
                "temperature_mean_c": (d.get("temperature_2m_mean") or [None])[0],
                "precipitation_mm": (d.get("precipitation_sum") or [None])[0],
                "wind_max_ms": (d.get("windspeed_10m_max") or [None])[0],
                "shortwave_radiation_mj_m2": (d.get("shortwave_radiation_sum") or [None])[0],
                "et0_mm": (d.get("et0_fao_evapotranspiration") or [None])[0],
            })
        except Exception as e:
            daily_climate.append({"id": cid, "lat": lat, "lon": lon, "date": yesterday, "ok": False, "error": str(e)[:160]})

    city_list = cities.get("cities") or []
    temps = [c.get("observation", {}).get("temperature_c") or (c.get("current") or {}).get("temperature_2m") for c in city_list]
    hums = [c.get("observation", {}).get("relative_humidity_pct") or (c.get("current") or {}).get("relative_humidity_2m") for c in city_list]
    press = [c.get("observation", {}).get("pressure_msl_hpa") or (c.get("current") or {}).get("pressure_msl") for c in city_list]
    winds = [c.get("observation", {}).get("wind_speed_ms") or (c.get("current") or {}).get("wind_speed_10m") for c in city_list]
    tmin, tmax = safe_minmax(temps)

    ndbc_obs = ndbc.get("observations") or {}
    wave_hs, water_ts, air_ts = [], [], []
    for _sid, block in ndbc_obs.items():
        lo = block.get("latest_observation") or {}
        if lo.get("wave_height_m") is not None:
            wave_hs.append(lo["wave_height_m"])
        if lo.get("water_temp_c") is not None:
            water_ts.append(lo["water_temp_c"])
        if lo.get("air_temp_c") is not None:
            air_ts.append(lo["air_temp_c"])

    casey_obs = casey.get("observations") or []
    casey_temps = [o.get("temperature_c") for o in casey_obs]
    casey_tmin, casey_tmax = safe_minmax(casey_temps)

    layer_files = []
    for root, _, files in os.walk("layers"):
        for fn in files:
            if fn.endswith(".json"):
                layer_files.append(os.path.join(root, fn).replace("\\", "/"))
    entry_files = sorted(glob.glob(f"data/entries/{date}/*.json"))

    summary = {
        "schema": "uogw.research_summary.v1",
        "date_utc": date,
        "generated_at_utc": now_s,
        "curator": "Midwest Stratospheric Data Systems",
        "repository": "https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather",
        "data_hub": "https://www.midwestsds.com/portal.html",
        "purpose": "Daily multi-layer atmospheric research package.",
        "catalog": {
            "dataset_count": len((catalog.get("datasets") or [])),
            "layers": list((catalog.get("layer_summary") or {}).keys()) or ["ground", "marine", "upper-air", "stratospheric", "satellite", "flight"],
        },
        "indexes": {
            "igra_stations": igra_status.get("station_count"),
            "igra_y2d_files": igra_status.get("file_count"),
            "ndbc_stations": ndbc_status.get("station_count") or (ndbc.get("station_count") if isinstance(ndbc, dict) else None),
            "ghcn_stations": ghcn.get("station_count"),
            "ghcn_countries": ghcn.get("country_count"),
            "foreign_open_sources": intl.get("source_count") or intl_status.get("foreign_source_count"),
            "global_city_samples": samples_status.get("city_count") or cities.get("city_count"),
            "global_city_ok": samples_status.get("ok_count") or cities.get("ok_count"),
        },
        "observations_today": {
            "global_cities_ok": cities.get("ok_count") or samples_status.get("ok_count"),
            "ndbc_realtime_stations": len(ndbc_obs) or ndbc_status.get("realtime_observation_count"),
            "casey_hourly_count": casey.get("observation_count") or len(casey_obs) or ground_status.get("observation_count"),
            "research_daily_climate_cities": sum(1 for x in daily_climate if x.get("ok")),
        },
        "derived_surface_stats": {
            "global_city_temperature_c": {"mean": safe_mean(temps), "min": tmin, "max": tmax},
            "global_city_humidity_pct": {"mean": safe_mean(hums)},
            "global_city_pressure_hpa": {"mean": safe_mean(press)},
            "global_city_wind_ms": {"mean": safe_mean(winds)},
            "casey_temperature_c": {"min": casey_tmin, "max": casey_tmax, "mean": safe_mean(casey_temps)},
            "ndbc_wave_height_m": {"mean": safe_mean(wave_hs), "n": len(wave_hs)},
            "ndbc_water_temp_c": {"mean": safe_mean(water_ts), "n": len(water_ts)},
            "ndbc_air_temp_c": {"mean": safe_mean(air_ts), "n": len(air_ts)},
        },
        "files": {"layer_json_count": len(layer_files), "entry_files": [p.replace("\\", "/") for p in entry_files]},
        "science_notes": [
            "Surface city samples use Open-Meteo (CC BY 4.0).",
            "Marine realtime from NOAA NDBC public feeds.",
            "Casey hourly is MSDS-curated Open-Meteo extract.",
            "IGRA/GHCN/NDBC counts are discovery indexes.",
        ],
        "status_sources": {
            "igra": igra_status, "ndbc": ndbc_status, "global_samples": samples_status,
            "msds_ground": ground_status, "international": intl_status,
        },
    }

    science_package = {
        "schema": "uogw.science_package.v1",
        "date_utc": date,
        "generated_at_utc": now_s,
        "curator": "Midwest Stratospheric Data Systems",
        "summary": summary,
        "daily_climate_research_cities": daily_climate,
        "global_city_observations": city_list,
        "ndbc_latest_observations": {sid: (block.get("latest_observation") or {}) for sid, block in ndbc_obs.items()},
        "casey_site": casey.get("site"),
        "casey_daily": casey.get("daily"),
        "casey_observation_count": len(casey_obs),
        "attribution": {
            "open_meteo": "CC BY 4.0 — https://open-meteo.com/",
            "ndbc": "NOAA NDBC",
            "igra": "NOAA NCEI IGRA",
            "ghcn": "NOAA NCEI GHCNd",
            "msds": "Midwest Stratospheric Data Systems",
        },
    }

    climate_doc = {"date": yesterday, "generated_at_utc": now_s, "cities": daily_climate, "data_kind": "observations"}
    paths = {
        f"data/entries/{date}/research-summary.json": summary,
        f"data/entries/{date}/science-package.json": science_package,
        f"data/entries/{date}/daily-climate.json": climate_doc,
        "data/latest/research-summary.json": summary,
        "data/latest/science-package.json": science_package,
        "data/latest/daily-climate.json": climate_doc,
        f"layers/research/summary-{date}.json": summary,
        "layers/research/summary-latest.json": summary,
        f"snapshots/{date}/research-summary.json": summary,
    }
    for p, doc in paths.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            json.dump(doc, f, indent=2)

    sp = f"data/entries/{date}/summary.json"
    base = load(sp) or {"date": date, "entries": {}}
    base["date"] = date
    base["generated_at_utc"] = now_s
    base.setdefault("entries", {})
    base["entries"]["research-summary"] = {
        "ok": True, "file": f"data/entries/{date}/research-summary.json",
        "dataset_count": summary["catalog"]["dataset_count"],
        "global_cities_ok": summary["observations_today"]["global_cities_ok"],
        "ndbc_realtime_stations": summary["observations_today"]["ndbc_realtime_stations"],
        "casey_hourly_count": summary["observations_today"]["casey_hourly_count"],
        "daily_climate_cities": summary["observations_today"]["research_daily_climate_cities"],
    }
    base["entries"]["science-package"] = {"ok": True, "file": f"data/entries/{date}/science-package.json"}
    base["entries"]["daily-climate"] = {
        "ok": summary["observations_today"]["research_daily_climate_cities"] > 0,
        "observation_count": summary["observations_today"]["research_daily_climate_cities"],
        "file": f"data/entries/{date}/daily-climate.json",
    }
    base["indexes"] = summary["indexes"]
    base["derived_surface_stats"] = summary["derived_surface_stats"]
    with open(sp, "w") as f:
        json.dump(base, f, indent=2)
    with open("data/latest/summary.json", "w") as f:
        json.dump(base, f, indent=2)
    with open("status/research-package.json", "w") as f:
        json.dump({
            "source": "uogw-research-package", "ok": True, "date": date,
            "data_entry": f"data/entries/{date}/science-package.json",
            "research_summary": f"data/entries/{date}/research-summary.json",
            "generated_at_utc": now_s,
        }, f, indent=2)

    print("RESEARCH PACKAGE OK", date,
          "cities", summary["observations_today"]["global_cities_ok"],
          "ndbc", summary["observations_today"]["ndbc_realtime_stations"],
          "casey", summary["observations_today"]["casey_hourly_count"],
          "climate", summary["observations_today"]["research_daily_climate_cities"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
