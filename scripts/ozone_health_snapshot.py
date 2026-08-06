#!/usr/bin/env python3
"""Ozone & air-quality health snapshot (research) for Casey/Clark County + sample cities."""
from __future__ import annotations

import json
import math
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SITES = [
    {"id": "casey_il", "name": "Casey, IL (Clark County)", "lat": 39.299, "lon": -87.992},
    {"id": "chicago_il", "name": "Chicago, IL", "lat": 41.88, "lon": -87.63},
    {"id": "stlouis_mo", "name": "St. Louis, MO", "lat": 38.63, "lon": -90.20},
    {"id": "indianapolis_in", "name": "Indianapolis, IN", "lat": 39.77, "lon": -86.16},
]


def fetch_aq(lat, lon):
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        "&current=us_aqi,pm2_5,ozone,nitrogen_dioxide,uv_index"
        "&hourly=ozone,uv_index,pm2_5,us_aqi"
        "&timezone=auto&forecast_days=2"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-Ozone/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def o3_ug_to_ppb(ug):
    if ug is None:
        return None
    # rough STP conversion for display context
    return round(float(ug) * 0.5, 1)


def ozone_band(ug):
    """Research-oriented outdoor guidance bands from O3 µg/m³."""
    if ug is None:
        return "unknown", "Ozone data unavailable"
    # Approximate alignment with common outdoor messaging
    if ug < 60:
        return "good", "Low ozone — generally comfortable for outdoor activity (research screen)."
    if ug < 100:
        return "moderate", "Moderate ozone — sensitive groups may notice irritation with prolonged outdoor time."
    if ug < 140:
        return "unhealthy_sensitive", "Elevated ozone — limit prolonged outdoor exertion if you are sensitive."
    if ug < 180:
        return "unhealthy", "High ozone — reduce outdoor exertion; prefer morning/evening if possible."
    return "very_high", "Very high ozone — outdoor activity not advised for extended periods (research screen)."


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    sites_out = []
    for site in SITES:
        try:
            raw = fetch_aq(site["lat"], site["lon"])
            cur = raw.get("current") or {}
            o3 = cur.get("ozone")
            band, meaning = ozone_band(o3)
            sites_out.append({
                "id": site["id"],
                "name": site["name"],
                "lat": site["lat"],
                "lon": site["lon"],
                "ok": True,
                "ozone_ug_m3": o3,
                "ozone_ppb_approx": o3_ug_to_ppb(o3),
                "us_aqi": cur.get("us_aqi"),
                "pm2_5": cur.get("pm2_5"),
                "no2": cur.get("nitrogen_dioxide"),
                "uv_index": cur.get("uv_index"),
                "band": band,
                "health_meaning": meaning,
                "time_local": cur.get("time"),
                "hourly": {
                    "time": (raw.get("hourly") or {}).get("time", [])[:24],
                    "ozone": (raw.get("hourly") or {}).get("ozone", [])[:24],
                },
            })
        except Exception as e:
            sites_out.append({"id": site["id"], "name": site["name"], "ok": False, "error": str(e)})

    primary = next((s for s in sites_out if s.get("id") == "casey_il" and s.get("ok")), sites_out[0] if sites_out else {})

    # Chart for Casey ozone hourly
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        if primary.get("ok") and primary.get("hourly", {}).get("ozone"):
            times = [t[-5:] if "T" in t else t for t in primary["hourly"]["time"]]
            vals = [v if v is not None else 0 for v in primary["hourly"]["ozone"]]
            fig, ax = plt.subplots(figsize=(10, 3.8))
            fig.patch.set_facecolor("#0a1628")
            ax.set_facecolor("#0a1628")
            ax.plot(range(len(vals)), vals, color="#4ade80", linewidth=2)
            ax.fill_between(range(len(vals)), vals, alpha=0.2, color="#4ade80")
            ax.axhline(100, color="#feca57", linestyle="--", alpha=0.7)
            ax.axhline(140, color="#ff6b6b", linestyle="--", alpha=0.7)
            ax.set_title(f"Casey IL surface ozone (µg/m³) — {date}", color="#e8f4ff")
            ax.set_ylabel("O₃ µg/m³", color="#e8f4ff")
            ax.tick_params(colors="#b8c9d9")
            ax.grid(True, alpha=0.25, color="#1a3050")
            if len(times) > 8:
                step = max(1, len(times) // 8)
                ax.set_xticks(list(range(0, len(times), step)))
                ax.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=45, ha="right")
            fig.tight_layout()
            for d in [Path("visuals/latest"), Path(f"visuals/{date}")]:
                d.mkdir(parents=True, exist_ok=True)
                fig.savefig(d / "ozone-casey-trend.png", dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
    except Exception as e:
        print("chart skip", e)

    payload = {
        "schema": "uogw.ozone_health.v1",
        "ok": True,
        "date_utc": date,
        "generated_at_utc": now_s,
        "disclaimer": (
            "Research air-quality snapshot from Open-Meteo model fields. "
            "Not an EPA AirNow or NWS health advisory. For official AQI use airnow.gov."
        ),
        "primary_site": primary,
        "sites": sites_out,
        "chart": "visuals/latest/ozone-casey-trend.png",
        "curator": "Midwest Stratospheric Data Systems",
    }

    for p in [
        Path(f"data/entries/{date}/ozone-health.json"),
        Path("data/latest/ozone-health.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/ozone-health.json").write_text(
        json.dumps({"ok": True, "date": date, "generated_at_utc": now_s, "casey_band": primary.get("band")}, indent=2)
        + "\n"
    )
    print(json.dumps({"ok": True, "sites": len(sites_out), "casey_o3": primary.get("ozone_ug_m3")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
