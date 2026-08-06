#!/usr/bin/env python3
"""Build UOGW science analytics summary for research + Data Hub UI."""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median, pstdev

ROOT = Path(__file__).resolve().parents[1]


def load(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def c_to_f(c):
    if c is None:
        return None
    try:
        return round(float(c) * 9.0 / 5.0 + 32.0, 1)
    except (TypeError, ValueError):
        return None


def stats(vals):
    vals = [float(v) for v in vals if isinstance(v, (int, float)) and not math.isnan(float(v))]
    if not vals:
        return None
    out = {
        "n": len(vals),
        "min": round(min(vals), 3),
        "max": round(max(vals), 3),
        "mean": round(mean(vals), 3),
        "median": round(median(vals), 3),
    }
    if len(vals) >= 2:
        try:
            out["pstdev"] = round(pstdev(vals), 3)
        except Exception:
            pass
    return out


def dual_temp_stats(vals_c):
    s_c = stats(vals_c)
    if not s_c:
        return None
    vals_f = [c_to_f(v) for v in vals_c if isinstance(v, (int, float))]
    s_f = stats(vals_f)
    return {"celsius": s_c, "fahrenheit": s_f}


def city_temp_c(c: dict):
    obs = c.get("observation") or {}
    if obs.get("temperature_c") is not None:
        return obs.get("temperature_c")
    cur = c.get("current") or {}
    return cur.get("temperature_2m", cur.get("temperature_c"))


def city_field(c: dict, *keys):
    obs = c.get("observation") or {}
    cur = c.get("current") or {}
    for k in keys:
        if obs.get(k) is not None:
            return obs.get(k)
        if cur.get(k) is not None:
            return cur.get(k)
    return None


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    cities_doc = load(Path("data/latest/global-cities.json")) or load(
        Path("layers/ground/samples/cities-latest.json")
    ) or {}
    casey = load(Path("data/latest/casey-hourly.json")) or {}
    ndbc = load(Path("data/latest/ndbc-realtime.json")) or {}
    anomaly = load(Path("data/latest/anomaly-report.json")) or {}
    research = load(Path("data/latest/research-summary.json")) or {}
    baseline = load(Path("data/latest/rolling-baseline.json")) or {}
    climate = load(Path("data/latest/daily-climate.json")) or {}

    city_list = [c for c in (cities_doc.get("cities") or []) if c.get("ok")]
    temps_c = []
    rh = []
    pres = []
    wind = []
    extremes = {"hottest": None, "coldest": None}

    for c in city_list:
        name = c.get("name") or c.get("id")
        t = city_temp_c(c)
        if isinstance(t, (int, float)):
            temps_c.append(t)
            row = {"name": name, "id": c.get("id"), "temperature_c": t, "temperature_f": c_to_f(t),
                   "lat": c.get("lat"), "lon": c.get("lon"), "country": c.get("country")}
            if extremes["hottest"] is None or t > extremes["hottest"]["temperature_c"]:
                extremes["hottest"] = row
            if extremes["coldest"] is None or t < extremes["coldest"]["temperature_c"]:
                extremes["coldest"] = row
        h = city_field(c, "relative_humidity_pct", "relative_humidity_2m")
        if isinstance(h, (int, float)):
            rh.append(h)
        p = city_field(c, "pressure_msl_hpa", "pressure_msl")
        if isinstance(p, (int, float)):
            pres.append(p)
        w = city_field(c, "wind_speed_ms", "wind_speed_10m")
        if isinstance(w, (int, float)):
            wind.append(w)

    casey_obs = casey.get("observations") or []
    casey_t = [o.get("temperature_c") for o in casey_obs if isinstance(o.get("temperature_c"), (int, float))]
    casey_rh = [o.get("relative_humidity_pct") for o in casey_obs if isinstance(o.get("relative_humidity_pct"), (int, float))]

    ndbc_obs = ndbc.get("observations") or {}
    wave, water_t, air_t = [], [], []
    for sid, block in ndbc_obs.items():
        lo = block.get("latest_observation") or {}
        if isinstance(lo.get("wave_height_m"), (int, float)):
            wave.append(lo["wave_height_m"])
        if isinstance(lo.get("water_temp_c"), (int, float)):
            water_t.append(lo["water_temp_c"])
        if isinstance(lo.get("air_temp_c"), (int, float)):
            air_t.append(lo["air_temp_c"])

    # Simple heat index proxy (Rothfusz regression) for cities with T+RH — research only
    heat_flags = []
    for c in city_list:
        t = city_temp_c(c)
        h = city_field(c, "relative_humidity_pct", "relative_humidity_2m")
        if not isinstance(t, (int, float)) or not isinstance(h, (int, float)):
            continue
        tf = c_to_f(t)
        if tf is None or tf < 80:
            continue
        # NOAA heat index approximation (°F)
        HI = (-42.379 + 2.04901523 * tf + 10.14333127 * h
              - 0.22475541 * tf * h - 6.83783e-3 * tf ** 2
              - 5.481717e-2 * h ** 2 + 1.22874e-3 * tf ** 2 * h
              + 8.5282e-4 * tf * h ** 2 - 1.99e-6 * tf ** 2 * h ** 2)
        if HI >= 90:
            heat_flags.append({
                "name": c.get("name") or c.get("id"),
                "temperature_f": tf,
                "relative_humidity_pct": h,
                "heat_index_f": round(HI, 1),
                "level": "danger" if HI >= 105 else "extreme_caution" if HI >= 90 else "caution",
            })
    heat_flags.sort(key=lambda x: x["heat_index_f"], reverse=True)

    anom_counts = anomaly.get("counts") or {}
    top_anomalies = (anomaly.get("anomalies") or [])[:8]

    coverage = {
        "global_cities_ok": len(city_list),
        "global_cities_total": cities_doc.get("city_count") or len(cities_doc.get("cities") or []),
        "casey_hourly_count": len(casey_obs) or casey.get("observation_count"),
        "ndbc_stations_sampled": len(ndbc_obs),
        "research_climate_cities": len([c for c in (climate.get("cities") or []) if c.get("ok")]),
        "anomaly_events": anom_counts.get("total"),
        "baseline_present": bool(baseline),
        "research_summary_present": bool(research),
    }

    # Hub-ready highlight cards
    highlights = []
    if extremes["hottest"]:
        highlights.append({
            "id": "hottest_city",
            "label": "Hottest sample city",
            "value": f"{extremes['hottest']['temperature_f']} °F",
            "detail": extremes["hottest"]["name"],
        })
    if extremes["coldest"]:
        highlights.append({
            "id": "coldest_city",
            "label": "Coldest sample city",
            "value": f"{extremes['coldest']['temperature_f']} °F",
            "detail": extremes["coldest"]["name"],
        })
    if casey_t:
        highlights.append({
            "id": "casey_range",
            "label": "Casey daily range",
            "value": f"{c_to_f(min(casey_t))}–{c_to_f(max(casey_t))} °F",
            "detail": casey.get("date") or date,
        })
    highlights.append({
        "id": "anomalies",
        "label": "Anomaly flags",
        "value": str(anom_counts.get("total", 0)),
        "detail": f"alert {anom_counts.get('alert', 0)} · watch {anom_counts.get('watch', 0)} · info {anom_counts.get('info', 0)}",
    })
    if heat_flags:
        highlights.append({
            "id": "heat_index",
            "label": "Elevated heat index",
            "value": f"{heat_flags[0]['heat_index_f']} °F",
            "detail": heat_flags[0]["name"],
        })

    analytics = {
        "schema": "uogw.science_analytics.v1",
        "date_utc": date,
        "generated_at_utc": now_s,
        "curator": "Midwest Stratospheric Data Systems",
        "display_preference": {
            "hub_temperature_unit": "fahrenheit",
            "science_storage_unit": "celsius",
        },
        "coverage": coverage,
        "surface": {
            "global_city_temperature": dual_temp_stats(temps_c),
            "global_city_humidity_pct": stats(rh),
            "global_city_pressure_hpa": stats(pres),
            "global_city_wind_ms": stats(wind),
            "casey_temperature": dual_temp_stats(casey_t),
            "casey_humidity_pct": stats(casey_rh),
        },
        "marine": {
            "wave_height_m": stats(wave),
            "water_temperature": dual_temp_stats(water_t),
            "air_temperature": dual_temp_stats(air_t),
        },
        "extremes": extremes,
        "heat_index_flags": heat_flags[:10],
        "anomalies": {
            "counts": anom_counts,
            "top": top_anomalies,
            "disclaimer": anomaly.get("disclaimer") or "Research screening only",
        },
        "highlights": highlights,
        "inputs": {
            "global_cities": bool(cities_doc),
            "casey": bool(casey),
            "ndbc": bool(ndbc),
            "anomaly": bool(anomaly),
            "baseline": bool(baseline),
            "climate": bool(climate),
        },
        "hub": {
            "data_hub_url": "https://midwestsds.com/msds-data-hub.html",
            "charts_url": "https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/blob/main/visuals/latest/CHARTS.md",
            "science_package": "data/latest/science-package.json",
        },
    }

    targets = [
        Path(f"data/entries/{date}/science-analytics.json"),
        Path("data/latest/science-analytics.json"),
        Path(f"layers/analytics/science-analytics-{date}.json"),
        Path("layers/analytics/science-analytics-latest.json"),
        Path(f"snapshots/{date}/science-analytics.json"),
    ]
    for p in targets:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(analytics, indent=2) + "\n")

    # merge into summary.json entry index
    sp = Path(f"data/entries/{date}/summary.json")
    summary = load(sp) or {"date": date, "entries": {}}
    summary.setdefault("entries", {})
    summary["entries"]["science-analytics"] = {
        "ok": True,
        "file": f"data/entries/{date}/science-analytics.json",
        "highlights": len(highlights),
        "anomaly_total": anom_counts.get("total"),
    }
    summary["generated_at_utc"] = now_s
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(summary, indent=2) + "\n")
    Path("data/latest/summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/science-analytics.json").write_text(
        json.dumps(
            {
                "source": "uogw-science-analytics",
                "ok": True,
                "date": date,
                "generated_at_utc": now_s,
                "data_entry": f"data/entries/{date}/science-analytics.json",
                "highlight_count": len(highlights),
            },
            indent=2,
        )
        + "\n"
    )

    print(json.dumps({"ok": True, "highlights": len(highlights), "cities": len(city_list)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
