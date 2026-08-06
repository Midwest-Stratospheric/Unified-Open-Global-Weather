#!/usr/bin/env python3
"""Clark County, IL pre-tornado RESEARCH condition tracker.

NOT an official NWS product. Computes a transparent 0–100 research score from
Open-Meteo CAPE, CIN, lifted index, dewpoint, wind, and pressure tendency for
the Casey / Clark County area. Publishes JSON + trend PNG for the Data Hub.
"""
from __future__ import annotations

import json
import math
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]

# Casey, IL / Clark County approximate centroid
LAT, LON = 39.299, -87.992
SITE = {
    "name": "Clark County, Illinois (Casey area)",
    "county": "Clark",
    "state": "IL",
    "lat": LAT,
    "lon": LON,
    "timezone": "America/Chicago",
}


def fetch_open_meteo() -> dict:
    params = (
        f"latitude={LAT}&longitude={LON}"
        "&hourly=temperature_2m,relative_humidity_2m,dewpoint_2m,pressure_msl,"
        "surface_pressure,wind_speed_10m,wind_gusts_10m,wind_direction_10m,"
        "precipitation,weather_code,cape,convective_inhibition,lifted_index,cloud_cover"
        "&current=temperature_2m,relative_humidity_2m,dewpoint_2m,pressure_msl,"
        "wind_speed_10m,wind_gusts_10m,wind_direction_10m,precipitation,weather_code,cape"
        "&timezone=America%2FChicago&forecast_days=2"
    )
    url = "https://api.open-meteo.com/v1/forecast?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-PreTornado/1.0 (midwestsds.com)"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def c_to_f(c):
    if c is None:
        return None
    return round(float(c) * 9 / 5 + 32, 1)


def safe(v):
    if v is None:
        return None
    try:
        if isinstance(v, float) and math.isnan(v):
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def score_components(cur: dict, hourly: dict, idx: int) -> dict:
    """Transparent research scoring. Weights sum conceptually toward 0–100."""
    cape = safe(cur.get("cape"))
    if cape is None and hourly.get("cape"):
        cape = safe(hourly["cape"][idx] if idx < len(hourly["cape"]) else None)

    cin = None
    if hourly.get("convective_inhibition") and idx < len(hourly["convective_inhibition"]):
        cin = safe(hourly["convective_inhibition"][idx])

    li = None
    if hourly.get("lifted_index") and idx < len(hourly["lifted_index"]):
        li = safe(hourly["lifted_index"][idx])

    dew = safe(cur.get("dewpoint_2m"))
    if dew is None and hourly.get("dewpoint_2m"):
        dew = safe(hourly["dewpoint_2m"][idx])

    rh = safe(cur.get("relative_humidity_2m"))
    gust = safe(cur.get("wind_gusts_10m"))
    if gust is None and hourly.get("wind_gusts_10m"):
        gust = safe(hourly["wind_gusts_10m"][idx])
    wind = safe(cur.get("wind_speed_10m"))

    # Pressure tendency: last 3 hours vs now (hourly)
    p_now = safe(cur.get("pressure_msl"))
    p_tend = None
    if hourly.get("pressure_msl") and idx >= 3:
        p3 = safe(hourly["pressure_msl"][idx - 3])
        p0 = safe(hourly["pressure_msl"][idx])
        if p3 is not None and p0 is not None:
            p_tend = round(p0 - p3, 2)  # negative = falling

    parts = {}

    # CAPE (0–30): weak <500, mod 500–1000, strong 1000–2500, extreme >2500
    if cape is None:
        parts["cape"] = {"points": 0, "value": None, "note": "CAPE unavailable"}
    elif cape < 250:
        parts["cape"] = {"points": 2, "value": cape, "note": "Very low CAPE"}
    elif cape < 500:
        parts["cape"] = {"points": 6, "value": cape, "note": "Low CAPE"}
    elif cape < 1000:
        parts["cape"] = {"points": 12, "value": cape, "note": "Moderate CAPE"}
    elif cape < 2000:
        parts["cape"] = {"points": 20, "value": cape, "note": "Strong CAPE"}
    elif cape < 3000:
        parts["cape"] = {"points": 26, "value": cape, "note": "Very strong CAPE"}
    else:
        parts["cape"] = {"points": 30, "value": cape, "note": "Extreme CAPE"}

    # Lifted index (0–15): more negative = more unstable
    if li is None:
        parts["lifted_index"] = {"points": 0, "value": None, "note": "LI unavailable"}
    elif li > 0:
        parts["lifted_index"] = {"points": 1, "value": li, "note": "Stable LI"}
    elif li > -2:
        parts["lifted_index"] = {"points": 4, "value": li, "note": "Marginal LI"}
    elif li > -4:
        parts["lifted_index"] = {"points": 8, "value": li, "note": "Moderately unstable"}
    elif li > -6:
        parts["lifted_index"] = {"points": 12, "value": li, "note": "Unstable"}
    else:
        parts["lifted_index"] = {"points": 15, "value": li, "note": "Strongly unstable LI"}

    # CIN (0–10): low CIN favors surface-based storms
    if cin is None:
        parts["cin"] = {"points": 3, "value": None, "note": "CIN unavailable (neutral)"}
    elif cin > 100:
        parts["cin"] = {"points": 1, "value": cin, "note": "Strong inhibition"}
    elif cin > 50:
        parts["cin"] = {"points": 3, "value": cin, "note": "Moderate inhibition"}
    elif cin > 25:
        parts["cin"] = {"points": 6, "value": cin, "note": "Weak inhibition"}
    else:
        parts["cin"] = {"points": 10, "value": cin, "note": "Little inhibition"}

    # Moisture via dewpoint °C (0–15): IL summer dewpoints
    if dew is None:
        parts["moisture"] = {"points": 0, "value": None, "note": "Dewpoint unavailable"}
    elif dew < 10:
        parts["moisture"] = {"points": 2, "value": dew, "note": "Dry"}
    elif dew < 15:
        parts["moisture"] = {"points": 5, "value": dew, "note": "Modest moisture"}
    elif dew < 18:
        parts["moisture"] = {"points": 9, "value": dew, "note": "Adequate moisture"}
    elif dew < 21:
        parts["moisture"] = {"points": 12, "value": dew, "note": "Rich moisture"}
    else:
        parts["moisture"] = {"points": 15, "value": dew, "note": "Very moist boundary layer"}

    # Wind / gust proxy for organization (0–15) — not true deep-layer shear
    g = gust if gust is not None else wind
    if g is None:
        parts["wind"] = {"points": 0, "value": None, "note": "Wind unavailable"}
    elif g < 15:
        parts["wind"] = {"points": 3, "value": g, "note": "Light wind/gusts"}
    elif g < 25:
        parts["wind"] = {"points": 7, "value": g, "note": "Moderate gusts"}
    elif g < 40:
        parts["wind"] = {"points": 11, "value": g, "note": "Strong gusts"}
    else:
        parts["wind"] = {"points": 15, "value": g, "note": "Very strong gusts"}

    # Pressure fall last 3h (0–10)
    if p_tend is None:
        parts["pressure_tendency"] = {"points": 2, "value": None, "note": "Tendency unavailable"}
    elif p_tend <= -3:
        parts["pressure_tendency"] = {"points": 10, "value": p_tend, "note": "Rapid pressure fall"}
    elif p_tend <= -1.5:
        parts["pressure_tendency"] = {"points": 7, "value": p_tend, "note": "Falling pressure"}
    elif p_tend <= 0:
        parts["pressure_tendency"] = {"points": 4, "value": p_tend, "note": "Slight fall/steady"}
    else:
        parts["pressure_tendency"] = {"points": 1, "value": p_tend, "note": "Rising pressure"}

    total = sum(p["points"] for p in parts.values())
    total = max(0, min(100, int(round(total))))

    if total < 25:
        level, label = "quiet", "Quiet"
    elif total < 45:
        level, label = "elevated", "Elevated"
    elif total < 65:
        level, label = "watch", "Watch conditions"
    else:
        level, label = "high", "High research concern"

    return {
        "score": total,
        "level": level,
        "level_label": label,
        "components": parts,
        "inputs": {
            "cape_jkg": cape,
            "cin_jkg": cin,
            "lifted_index": li,
            "dewpoint_c": dew,
            "dewpoint_f": c_to_f(dew),
            "relative_humidity_pct": rh,
            "wind_speed_kmh": wind,
            "wind_gusts_kmh": gust,
            "pressure_msl_hpa": p_now,
            "pressure_tendency_3h_hpa": p_tend,
            "temperature_c": safe(cur.get("temperature_2m")),
            "temperature_f": c_to_f(safe(cur.get("temperature_2m"))),
        },
    }


def build_hourly_series(hourly: dict) -> list:
    times = hourly.get("time") or []
    series = []
    for i, t in enumerate(times):
        # synthetic current-like dict from hourly row
        row = {
            "cape": (hourly.get("cape") or [None])[i] if i < len(hourly.get("cape") or []) else None,
            "dewpoint_2m": (hourly.get("dewpoint_2m") or [None])[i] if i < len(hourly.get("dewpoint_2m") or []) else None,
            "relative_humidity_2m": (hourly.get("relative_humidity_2m") or [None])[i] if i < len(hourly.get("relative_humidity_2m") or []) else None,
            "wind_gusts_10m": (hourly.get("wind_gusts_10m") or [None])[i] if i < len(hourly.get("wind_gusts_10m") or []) else None,
            "wind_speed_10m": (hourly.get("wind_speed_10m") or [None])[i] if i < len(hourly.get("wind_speed_10m") or []) else None,
            "pressure_msl": (hourly.get("pressure_msl") or [None])[i] if i < len(hourly.get("pressure_msl") or []) else None,
            "temperature_2m": (hourly.get("temperature_2m") or [None])[i] if i < len(hourly.get("temperature_2m") or []) else None,
        }
        sc = score_components(row, hourly, i)
        series.append({
            "time": t,
            "score": sc["score"],
            "level": sc["level"],
            "cape_jkg": sc["inputs"]["cape_jkg"],
            "dewpoint_f": sc["inputs"]["dewpoint_f"],
            "pressure_msl_hpa": sc["inputs"]["pressure_msl_hpa"],
        })
    return series


def make_chart(series: list, date: str, score_now: int, level: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # next 24–36 points from now-ish: use all or last 48
    use = series[:48] if len(series) > 48 else series
    times = [s["time"][-5:] if "T" in s["time"] else s["time"] for s in use]
    scores = [s["score"] for s in use]
    capes = [s["cape_jkg"] if s["cape_jkg"] is not None else 0 for s in use]

    fig, axes = plt.subplots(2, 1, figsize=(11, 6.2), sharex=True)
    fig.patch.set_facecolor("#0a1628")
    for ax in axes:
        ax.set_facecolor("#0a1628")
        ax.tick_params(colors="#b8c9d9")
        ax.spines["bottom"].set_color("#00d4ff")
        ax.spines["left"].set_color("#00d4ff")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(True, alpha=0.25, color="#1a3050")

    axes[0].fill_between(range(len(scores)), scores, alpha=0.25, color="#ff6b6b")
    axes[0].plot(range(len(scores)), scores, color="#ff6b6b", linewidth=2)
    axes[0].axhline(45, color="#feca57", linestyle="--", linewidth=1, alpha=0.8)
    axes[0].axhline(65, color="#ff6b6b", linestyle="--", linewidth=1, alpha=0.8)
    axes[0].set_ylabel("Research score", color="#e8f4ff")
    axes[0].set_ylim(0, 100)
    axes[0].set_title(
        f"Clark County IL · Pre-tornado research score (now {score_now} · {level}) — {date}",
        color="#e8f4ff",
        fontsize=11,
    )

    axes[1].bar(range(len(capes)), capes, color="#00d4ff", alpha=0.85)
    axes[1].set_ylabel("CAPE (J/kg)", color="#e8f4ff")
    axes[1].set_xlabel("Local time", color="#e8f4ff")
    if len(times) > 12:
        step = max(1, len(times) // 12)
        axes[1].set_xticks(list(range(0, len(times), step)))
        axes[1].set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=45, ha="right")
    else:
        axes[1].set_xticks(list(range(len(times))))
        axes[1].set_xticklabels(times, rotation=45, ha="right")

    fig.tight_layout()
    for d in [ROOT / "visuals/latest", ROOT / f"visuals/{date}"]:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / "pre-tornado-clark-trend.png", dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        raw = fetch_open_meteo()
    except Exception as e:
        err = {
            "schema": "uogw.pre_tornado_clark.v1",
            "ok": False,
            "error": str(e),
            "generated_at_utc": now_s,
            "site": SITE,
            "disclaimer": "Research only — not an NWS warning product.",
        }
        Path("data/latest").mkdir(parents=True, exist_ok=True)
        Path("data/latest/pre-tornado-clark.json").write_text(json.dumps(err, indent=2) + "\n")
        print(json.dumps(err))
        return 1

    hourly = raw.get("hourly") or {}
    current = raw.get("current") or {}
    times = hourly.get("time") or []
    # match current hour index
    idx = 0
    cur_t = current.get("time")
    if cur_t and times:
        if cur_t in times:
            idx = times.index(cur_t)
        else:
            # nearest
            for i, t in enumerate(times):
                if t <= cur_t:
                    idx = i

    scored = score_components(current, hourly, idx)
    series = build_hourly_series(hourly)
    make_chart(series, date, scored["score"], scored["level"])

    meaning = {
        "quiet": "Background conditions. No elevated pre-tornado research signals for Clark County in this automated screen.",
        "elevated": "Some instability/moisture/wind factors are rising. Stay weather-aware; this is not an official watch.",
        "watch": "Multiple research factors concurrent (instability, moisture, and/or wind/pressure signals). Monitor NWS/SPC products closely.",
        "high": "Strong stacked research signals. Treat as heightened awareness only — official warnings come solely from NWS.",
    }

    payload = {
        "schema": "uogw.pre_tornado_clark.v1",
        "ok": True,
        "date_utc": date,
        "generated_at_utc": now_s,
        "site": SITE,
        "disclaimer": (
            "RESEARCH SCREENING ONLY. This is NOT a National Weather Service watch, warning, or forecast. "
            "Tornadoes can occur with little notice. Always follow NWS, local emergency management, and NOAA Weather Radio."
        ),
        "probability_research": {
            "score_0_to_100": scored["score"],
            "level": scored["level"],
            "level_label": scored["level_label"],
            "meaning": meaning[scored["level"]],
            "method": (
                "Weighted composite of CAPE, lifted index, CIN, dewpoint moisture, wind gust proxy, "
                "and 3-hour pressure tendency from Open-Meteo near Casey, IL. Not calibrated storm probability."
            ),
        },
        "components": scored["components"],
        "observations": scored["inputs"],
        "trend_hourly": series[:36],
        "chart": "visuals/latest/pre-tornado-clark-trend.png",
        "hub": "https://midwestsds.com/msds-data-hub.html#pre-tornado",
        "official_sources": [
            "https://www.weather.gov/",
            "https://www.spc.noaa.gov/",
            "https://alerts.weather.gov/",
        ],
        "curator": "Midwest Stratospheric Data Systems",
    }

    for p in [
        Path(f"data/entries/{date}/pre-tornado-clark.json"),
        Path("data/latest/pre-tornado-clark.json"),
        Path(f"layers/hazards/pre-tornado-clark-{date}.json"),
        Path("layers/hazards/pre-tornado-clark-latest.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/pre-tornado-clark.json").write_text(
        json.dumps(
            {
                "ok": True,
                "date": date,
                "generated_at_utc": now_s,
                "score": scored["score"],
                "level": scored["level"],
            },
            indent=2,
        )
        + "\n"
    )

    print(json.dumps({"ok": True, "score": scored["score"], "level": scored["level"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
