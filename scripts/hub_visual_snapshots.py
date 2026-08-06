#!/usr/bin/env python3
"""Build three hub visual snapshots from existing UOGW latest products."""
from __future__ import annotations

import json
import os
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

    # 1) Heat & humidity snapshot
    surface = (analytics.get("surface") or {})
    heat = {
        "title": "Heat & humidity snapshot",
        "global_temp_f": ((surface.get("global_city_temperature") or {}).get("fahrenheit") or {}),
        "global_rh": surface.get("global_city_humidity_pct") or {},
        "casey_temp_f": ((surface.get("casey_temperature") or {}).get("fahrenheit") or {}),
        "heat_index_flags": (analytics.get("heat_index_flags") or [])[:5],
        "extremes": analytics.get("extremes") or {},
    }

    # 2) Marine snapshot
    obs = ndbc.get("observations") or {}
    marine_rows = []
    for sid, block in list(obs.items())[:8]:
        lo = block.get("latest_observation") or {}
        marine_rows.append({
            "station": sid,
            "wave_height_m": lo.get("wave_height_m"),
            "water_temp_f": c_to_f(lo.get("water_temp_c")),
            "air_temp_f": c_to_f(lo.get("air_temp_c")),
            "wind_speed": lo.get("wind_speed_ms"),
        })
    marine = {
        "title": "Marine NDBC snapshot",
        "station_count": len(obs),
        "rows": marine_rows,
        "wave_stats": ((analytics.get("marine") or {}).get("wave_height_m") or {}),
    }

    # 3) Casey local series snapshot
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
            {
                "time": o.get("time"),
                "temperature_f": c_to_f(o.get("temperature_c")),
                "humidity": o.get("relative_humidity_pct"),
            }
            for o in cob[-12:]
        ],
    }

    # Charts
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        def style(ax):
            ax.set_facecolor("#0a1628")
            ax.tick_params(colors="#b8c9d9")
            ax.grid(True, alpha=0.25, color="#1a3050")
            for s in ax.spines.values():
                s.set_color("#00d4ff")

        # Heat: simple bar of hottest cities from analytics extremes or cities file
        city_list = [c for c in (cities.get("cities") or []) if c.get("ok")]
        rows = []
        for c in city_list:
            obs_c = c.get("observation") or {}
            cur = c.get("current") or {}
            t = obs_c.get("temperature_c", cur.get("temperature_2m", cur.get("temperature_c")))
            if t is None:
                continue
            rows.append((c.get("name") or c.get("id"), c_to_f(t)))
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
            Path("visuals/latest").mkdir(parents=True, exist_ok=True)
            fig.savefig("visuals/latest/hub-heat-cities.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if marine_rows:
            fig, ax = plt.subplots(figsize=(9, 3.8))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            labels = [r["station"] for r in marine_rows]
            waves = [r["wave_height_m"] or 0 for r in marine_rows]
            ax.bar(labels, waves, color="#00d4ff")
            ax.set_ylabel("Wave height (m)", color="#e8f4ff")
            ax.set_title(f"NDBC sample wave heights — {date}", color="#e8f4ff")
            fig.tight_layout()
            fig.savefig("visuals/latest/hub-marine-waves.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if casey_snap["hourly"]:
            fig, ax = plt.subplots(figsize=(9, 3.6))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            hs = casey_snap["hourly"]
            ax.plot(range(len(hs)), [h["temperature_f"] for h in hs], color="#00d4ff", marker="o", markersize=3)
            ax.set_ylabel("°F", color="#e8f4ff")
            ax.set_title(f"Casey recent hourly temperature (°F) — {date}", color="#e8f4ff")
            ax.set_xticks(range(len(hs)))
            ax.set_xticklabels([str(h.get("time") or "")[-5:] for h in hs], rotation=45, ha="right")
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
    print(json.dumps({"ok": True, "marine_stations": len(marine_rows), "casey_hours": len(cob)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
