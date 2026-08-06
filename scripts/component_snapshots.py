#!/usr/bin/env python3
"""UOGW component snapshots: ozone health, heat-humidity, pressure-wind, marine.

Publishes JSON + PNG charts for the Data Hub. Ozone uses Open-Meteo air-quality
near Casey / Clark County. Other panels derive from existing UOGW latest files.
"""
from __future__ import annotations

import json
import math
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAT, LON = 39.299, -87.992


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
        return round(float(c) * 9 / 5 + 32, 1)
    except (TypeError, ValueError):
        return None


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-Snapshots/1.0 (midwestsds.com)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def ozone_category_ugm3(o3: float | None) -> tuple[str, str]:
    """Rough outdoor guidance from concentration (µg/m³). Not medical advice."""
    if o3 is None:
        return "unknown", "Ozone reading unavailable"
    # Approximate bands aligned with moderate outdoor exposure messaging
    if o3 < 50:
        return "good", "Low ozone — generally comfortable for outdoor activity"
    if o3 < 100:
        return "moderate", "Moderate ozone — sensitive individuals may notice irritation"
    if o3 < 150:
        return "unhealthy_sensitive", "Elevated ozone — limit prolonged outdoor exertion if sensitive"
    if o3 < 200:
        return "unhealthy", "High ozone — reduce outdoor exertion; follow local AQI guidance"
    return "very_high", "Very high ozone — avoid prolonged outdoor activity; check AirNow"


def us_aqi_label(aqi: float | None) -> str:
    if aqi is None:
        return "—"
    aqi = float(aqi)
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for sensitive groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very unhealthy"
    return "Hazardous"


def build_ozone() -> dict:
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={LAT}&longitude={LON}"
        "&current=european_aqi,us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,"
        "sulphur_dioxide,ozone,uv_index"
        "&hourly=ozone,pm2_5,us_aqi"
        "&timezone=America%2FChicago&forecast_days=2"
    )
    raw = fetch_json(url)
    cur = raw.get("current") or {}
    hourly = raw.get("hourly") or {}
    o3 = cur.get("ozone")
    cat, msg = ozone_category_ugm3(o3 if o3 is None else float(o3))
    return {
        "schema": "uogw.ozone_health.v1",
        "ok": True,
        "site": {"name": "Clark County IL (Casey)", "lat": LAT, "lon": LON},
        "disclaimer": (
            "Air-quality model fields for research/education. Not medical advice. "
            "For official AQI and health guidance use AirNow.gov and local agencies."
        ),
        "current": {
            "ozone_ug_m3": o3,
            "category": cat,
            "message": msg,
            "us_aqi": cur.get("us_aqi"),
            "us_aqi_label": us_aqi_label(cur.get("us_aqi")),
            "pm2_5_ug_m3": cur.get("pm2_5"),
            "no2_ug_m3": cur.get("nitrogen_dioxide"),
            "uv_index": cur.get("uv_index"),
            "time_local": cur.get("time"),
        },
        "hourly": {
            "time": (hourly.get("time") or [])[:48],
            "ozone_ug_m3": (hourly.get("ozone") or [])[:48],
            "us_aqi": (hourly.get("us_aqi") or [])[:48],
            "pm2_5": (hourly.get("pm2_5") or [])[:48],
        },
        "official": ["https://www.airnow.gov/", "https://www.epa.gov/ozone-pollution"],
    }


def build_heat_humidity(cities_doc: dict, casey: dict) -> dict:
    rows = []
    for c in cities_doc.get("cities") or []:
        if not c.get("ok"):
            continue
        obs = c.get("observation") or {}
        cur = c.get("current") or {}
        t = obs.get("temperature_c", cur.get("temperature_2m", cur.get("temperature_c")))
        h = obs.get("relative_humidity_pct", cur.get("relative_humidity_2m"))
        if t is None:
            continue
        rows.append({
            "name": c.get("name") or c.get("id"),
            "temp_c": t,
            "temp_f": c_to_f(t),
            "rh": h,
        })
    rows.sort(key=lambda r: r["temp_f"] or -999)
    casey_obs = casey.get("observations") or []
    casey_t = [o.get("temperature_c") for o in casey_obs if isinstance(o.get("temperature_c"), (int, float))]
    casey_h = [o.get("relative_humidity_pct") for o in casey_obs if isinstance(o.get("relative_humidity_pct"), (int, float))]
    return {
        "schema": "uogw.heat_humidity.v1",
        "ok": True,
        "cities": rows,
        "hottest": rows[-1] if rows else None,
        "coldest": rows[0] if rows else None,
        "casey": {
            "temp_f_min": c_to_f(min(casey_t)) if casey_t else None,
            "temp_f_max": c_to_f(max(casey_t)) if casey_t else None,
            "rh_mean": round(sum(casey_h) / len(casey_h), 1) if casey_h else None,
            "hours": len(casey_obs),
        },
    }


def build_pressure_wind(cities_doc: dict) -> dict:
    rows = []
    for c in cities_doc.get("cities") or []:
        if not c.get("ok"):
            continue
        obs = c.get("observation") or {}
        cur = c.get("current") or {}
        p = obs.get("pressure_msl_hpa", cur.get("pressure_msl"))
        w = obs.get("wind_speed_ms", cur.get("wind_speed_10m"))
        rows.append({
            "name": c.get("name") or c.get("id"),
            "pressure_hpa": p,
            "wind_ms": w,
            "wind_mph": round(float(w) * 2.23694, 1) if isinstance(w, (int, float)) else None,
        })
    return {"schema": "uogw.pressure_wind.v1", "ok": True, "cities": rows}


def build_marine(ndbc: dict) -> dict:
    obs = ndbc.get("observations") or {}
    stations = []
    for sid, block in obs.items():
        lo = block.get("latest_observation") or {}
        stations.append({
            "id": sid,
            "wave_height_m": lo.get("wave_height_m"),
            "water_temp_c": lo.get("water_temp_c"),
            "water_temp_f": c_to_f(lo.get("water_temp_c")),
            "air_temp_c": lo.get("air_temp_c"),
            "air_temp_f": c_to_f(lo.get("air_temp_c")),
        })
    return {"schema": "uogw.marine_snapshot.v1", "ok": True, "stations": stations}


def charts(ozone: dict, heat: dict, pressure: dict, marine: dict, date: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def style(ax):
        ax.set_facecolor("#0a1628")
        ax.tick_params(colors="#b8c9d9")
        for s in ("bottom", "left"):
            ax.spines[s].set_color("#00d4ff")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(True, alpha=0.25, color="#1a3050")

    out_dirs = [ROOT / "visuals/latest", ROOT / f"visuals/{date}"]

    def save(fig, name):
        for d in out_dirs:
            d.mkdir(parents=True, exist_ok=True)
            fig.savefig(d / name, dpi=140, bbox_inches="tight", facecolor="#0a1628")
        plt.close(fig)

    # Ozone trend
    h = ozone.get("hourly") or {}
    times = [t[-5:] if "T" in t else t for t in (h.get("time") or [])[:36]]
    o3 = (h.get("ozone_ug_m3") or [])[:36]
    if times and o3:
        fig, ax = plt.subplots(figsize=(10, 3.8))
        fig.patch.set_facecolor("#0a1628")
        style(ax)
        ax.fill_between(range(len(o3)), o3, color="#22d3ee", alpha=0.3)
        ax.plot(range(len(o3)), o3, color="#22d3ee", lw=2)
        ax.set_title(f"Ozone (µg/m³) · Casey / Clark County — {date}", color="#e8f4ff")
        ax.set_ylabel("µg/m³", color="#e8f4ff")
        step = max(1, len(times) // 10)
        ax.set_xticks(list(range(0, len(times), step)))
        ax.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=45, ha="right")
        save(fig, "ozone-health-trend.png")

    # Heat humidity bars
    cities = (heat.get("cities") or [])[-12:]
    if cities:
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#0a1628")
        style(ax)
        names = [c["name"].split(",")[0][:14] for c in cities]
        vals = [c["temp_f"] or 0 for c in cities]
        ax.barh(names, vals, color="#fb923c")
        ax.set_xlabel("°F", color="#e8f4ff")
        ax.set_title(f"Global sample temperatures (°F) — {date}", color="#e8f4ff")
        save(fig, "heat-humidity-cities.png")

    # Pressure scatter-ish bar
    prow = [c for c in (pressure.get("cities") or []) if c.get("pressure_hpa") is not None][:15]
    if prow:
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#0a1628")
        style(ax)
        ax.bar([c["name"].split(",")[0][:10] for c in prow], [c["pressure_hpa"] for c in prow], color="#00d4ff")
        ax.set_ylabel("hPa", color="#e8f4ff")
        ax.set_title(f"MSL pressure sample (hPa) — {date}", color="#e8f4ff")
        plt.xticks(rotation=45, ha="right")
        save(fig, "pressure-wind-sample.png")

    # Marine
    st = marine.get("stations") or []
    if st:
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
        fig.patch.set_facecolor("#0a1628")
        for ax in axes:
            style(ax)
        ids = [s["id"] for s in st]
        waves = [s.get("wave_height_m") or 0 for s in st]
        wtf = [s.get("water_temp_f") or 0 for s in st]
        axes[0].bar(ids, waves, color="#00d4ff")
        axes[0].set_title("NDBC wave height (m)", color="#e8f4ff")
        axes[1].bar(ids, wtf, color="#38bdf8")
        axes[1].set_title("NDBC water temp (°F)", color="#e8f4ff")
        fig.suptitle(f"Marine snapshot — {date}", color="#e8f4ff")
        fig.tight_layout()
        save(fig, "marine-component.png")


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    cities = load(Path("data/latest/global-cities.json")) or {}
    casey = load(Path("data/latest/casey-hourly.json")) or {}
    ndbc = load(Path("data/latest/ndbc-realtime.json")) or {}

    try:
        ozone = build_ozone()
    except Exception as e:
        ozone = {"schema": "uogw.ozone_health.v1", "ok": False, "error": str(e)}

    heat = build_heat_humidity(cities, casey)
    pressure = build_pressure_wind(cities)
    marine = build_marine(ndbc)

    for name, payload in [
        ("ozone-health.json", ozone),
        ("heat-humidity.json", heat),
        ("pressure-wind.json", pressure),
        ("marine-snapshot.json", marine),
    ]:
        payload["generated_at_utc"] = now_s
        payload["date_utc"] = date
        payload["curator"] = "Midwest Stratospheric Data Systems"
        for p in [
            Path(f"data/entries/{date}/{name}"),
            Path(f"data/latest/{name}"),
        ]:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(payload, indent=2) + "\n")

    try:
        if ozone.get("ok"):
            charts(ozone, heat, pressure, marine, date)
    except Exception as e:
        print("chart error", e)

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/component-snapshots.json").write_text(
        json.dumps({"ok": True, "date": date, "generated_at_utc": now_s}, indent=2) + "\n"
    )
    print(json.dumps({"ok": True, "ozone": ozone.get("ok"), "cities": len(heat.get("cities") or [])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
