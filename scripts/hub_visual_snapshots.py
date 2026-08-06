#!/usr/bin/env python3
"""Build three hub visual snapshots from existing UOGW latest products."""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(p):
    path = ROOT / p
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def c_to_f(c):
    if c is None:
        return None
    try:
        return round(float(c) * 9 / 5 + 32, 1)
    except Exception:
        return None


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    analytics = load("data/latest/science-analytics.json") or {}
    ndbc = load("data/latest/ndbc-realtime.json") or {}
    casey = load("data/latest/casey-hourly.json") or {}
    cities = load("data/latest/global-cities.json") or {}

    surface = analytics.get("surface") or {}
    heat = {
        "title": "Heat & humidity snapshot",
        "global_temp_f": ((surface.get("global_city_temperature") or {}).get("fahrenheit") or {}),
        "global_rh": surface.get("global_city_humidity_pct") or {},
        "casey_temp_f": ((surface.get("casey_temperature") or {}).get("fahrenheit") or {}),
        "heat_index_flags": (analytics.get("heat_index_flags") or [])[:5],
        "extremes": analytics.get("extremes") or {},
    }

    obs = ndbc.get("observations") or {}
    marine_rows = []
    for sid, block in list(obs.items())[:8]:
        lo = block.get("latest_observation") or {}
        marine_rows.append({
            "station": sid,
            "wave_height_m": lo.get("wave_height_m"),
            "water_temp_f": c_to_f(lo.get("water_temp_c")),
            "air_temp_f": c_to_f(lo.get("air_temp_c")),
        })
    marine = {"title": "Marine NDBC snapshot", "station_count": len(obs), "rows": marine_rows}

    cob = casey.get("observations") or []
    temps_f = [c_to_f(o.get("temperature_c")) for o in cob if o.get("temperature_c") is not None]
    casey_snap = {
        "title": "Casey local conditions",
        "date": casey.get("date") or date,
        "observation_count": len(cob) or casey.get("observation_count"),
        "temp_f_min": min(temps_f) if temps_f else None,
        "temp_f_max": max(temps_f) if temps_f else None,
        "temp_f_mean": round(sum(temps_f) / len(temps_f), 1) if temps_f else None,
        "hourly": [
            {"time": o.get("time"), "temperature_f": c_to_f(o.get("temperature_c")), "humidity": o.get("relative_humidity_pct")}
            for o in cob[-12:]
        ],
    }

    Path("visuals/latest").mkdir(parents=True, exist_ok=True)
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        def style(ax):
            ax.set_facecolor("#0a1628")
            ax.tick_params(colors="#b8c9d9")
            ax.grid(True, alpha=0.25, color="#1a3050")

        city_list = [c for c in (cities.get("cities") or []) if c.get("ok")]
        rows = []
        press_rows = []
        for c in city_list:
            obs_c = c.get("observation") or {}
            cur = c.get("current") or {}
            t = obs_c.get("temperature_c", cur.get("temperature_2m", cur.get("temperature_c")))
            if t is not None:
                rows.append((c.get("name") or c.get("id"), c_to_f(t)))
            p = obs_c.get("pressure_msl_hpa", cur.get("pressure_msl"))
            w = obs_c.get("wind_speed_ms", cur.get("wind_speed_10m"))
            if p is not None:
                press_rows.append((c.get("name") or c.get("id"), p, w))
        rows.sort(key=lambda x: x[1], reverse=True)
        top = rows[:12]
        if top:
            fig, ax = plt.subplots(figsize=(9, 4.2))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            ax.barh([r[0] for r in reversed(top)], [r[1] for r in reversed(top)], color="#ff9f43")
            ax.set_xlabel("°F", color="#e8f4ff")
            ax.set_title(f"Warmest sample cities (°F) — {date}", color="#e8f4ff")
            fig.tight_layout()
            for name in ("hub-heat-cities.png", "heat-humidity-cities.png"):
                fig.savefig(f"visuals/latest/{name}", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if press_rows:
            press_rows.sort(key=lambda x: x[1])
            sample = press_rows[:12]
            fig, ax = plt.subplots(figsize=(9, 4))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            ax.barh([r[0] for r in reversed(sample)], [r[1] for r in reversed(sample)], color="#38bdf8")
            ax.set_xlabel("hPa", color="#e8f4ff")
            ax.set_title(f"Sample city MSLP (hPa) — {date}", color="#e8f4ff")
            fig.tight_layout()
            fig.savefig("visuals/latest/pressure-wind-sample.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if marine_rows:
            fig, ax = plt.subplots(figsize=(9, 3.8))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            ax.bar([r["station"] for r in marine_rows], [r["wave_height_m"] or 0 for r in marine_rows], color="#00d4ff")
            ax.set_ylabel("Wave height (m)", color="#e8f4ff")
            ax.set_title(f"NDBC sample wave heights — {date}", color="#e8f4ff")
            fig.tight_layout()
            for name in ("hub-marine-waves.png",):
                fig.savefig(f"visuals/latest/{name}", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if casey_snap["hourly"]:
            fig, ax = plt.subplots(figsize=(9, 3.6))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            hs = casey_snap["hourly"]
            ax.plot(range(len(hs)), [h["temperature_f"] for h in hs], color="#00d4ff", marker="o", markersize=3)
            ax.set_ylabel("°F", color="#e8f4ff")
            ax.set_title(f"Casey recent hourly temperature (°F) — {date}", color="#e8f4ff")
            fig.tight_layout()
            fig.savefig("visuals/latest/hub-casey-recent.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
    except Exception as e:
        print("charts", e)

    payload = {
        "schema": "uogw.hub_visual_snapshots.v1",
        "ok": True,
        "date_utc": date,
        "generated_at_utc": now_s,
        "heat": heat,
        "marine": marine,
        "casey": casey_snap,
        "charts": {
            "heat": "visuals/latest/hub-heat-cities.png",
            "pressure": "visuals/latest/pressure-wind-sample.png",
            "marine": "visuals/latest/hub-marine-waves.png",
            "casey": "visuals/latest/hub-casey-recent.png",
        },
    }
    for p in [
        Path(f"data/entries/{date}/hub-visual-snapshots.json"),
        Path("data/latest/hub-visual-snapshots.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
