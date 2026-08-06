#!/usr/bin/env python3
"""Space weather + NOAA GFS research snapshot for UOGW hub.

Sources:
- NOAA SWPC planetary K-index and GOES X-ray flux (near-real-time space environment)
- Open-Meteo GFS model fields for Casey, IL (model forecast — not balloon telemetry)
- NOMADS GFS product directory presence check
"""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASEY = {"lat": 39.299, "lon": -87.992, "name": "Casey, IL"}


def get_json(url: str, timeout: int = 45):
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-SpaceGFS/1.0 (midwestsds.com)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def get_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-SpaceGFS/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(2000).decode("utf-8", "replace")


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Space weather (SWPC) ---
    space = {"ok": False}
    try:
        kp_rows = get_json("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json")
        xray_rows = get_json("https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json")
        kp_latest = kp_rows[-1] if kp_rows else {}
        # soft X-ray band often last entries; take last
        xray_latest = xray_rows[-1] if xray_rows else {}
        kp_series = [
            {
                "time": r.get("time_tag"),
                "kp": r.get("kp_index", r.get("estimated_kp")),
            }
            for r in kp_rows[-48:]
        ]
        xray_series = [
            {"time": r.get("time_tag"), "flux": r.get("flux"), "energy": r.get("energy")}
            for r in xray_rows[-60:]
            if r.get("flux") is not None
        ]
        space = {
            "ok": True,
            "source": "NOAA SWPC",
            "data_class": "near_real_time_space_environment",
            "not_telemetry": (
                "These are space-environment monitors (ground/satellite instruments), "
                "not MSDS balloon payload telemetry and not radiosonde tracks."
            ),
            "kp_latest": kp_latest,
            "xray_latest": xray_latest,
            "kp_series": kp_series,
            "xray_series_tail": xray_series[-30:],
        }
    except Exception as e:
        space = {"ok": False, "error": str(e)}

    # --- GFS via Open-Meteo ---
    gfs = {"ok": False}
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={CASEY['lat']}&longitude={CASEY['lon']}"
            "&models=gfs_seamless"
            "&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_gusts_10m,weather_code"
            "&hourly=temperature_2m,pressure_msl,wind_speed_10m,cape,precipitation"
            "&forecast_days=2&timezone=America%2FChicago"
        )
        raw = get_json(url)
        cur = raw.get("current") or {}
        hourly = raw.get("hourly") or {}
        gfs = {
            "ok": True,
            "model": "NOAA GFS (via Open-Meteo gfs_seamless)",
            "data_class": "numerical_weather_prediction_model",
            "not_telemetry": (
                "GFS is a forecast model grid, not observations from a balloon, radiosonde, or live tracker."
            ),
            "site": CASEY,
            "current": cur,
            "hourly": {
                "time": (hourly.get("time") or [])[:36],
                "temperature_2m": (hourly.get("temperature_2m") or [])[:36],
                "cape": (hourly.get("cape") or [])[:36],
                "pressure_msl": (hourly.get("pressure_msl") or [])[:36],
            },
            "upstream_noaa_nomads": "https://nomads.ncep.noaa.gov/",
        }
    except Exception as e:
        gfs = {"ok": False, "error": str(e)}

    # --- NOMADS availability check ---
    nomads = {"ok": False}
    try:
        html = get_text("https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/")
        nomads = {
            "ok": "gfs." in html or "Index of" in html,
            "url": "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/",
            "filter_ui": "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl",
            "note": "NCEP NOMADS serves full GFS GRIB2 cycles; Open-Meteo provides a convenient subset for hub charts.",
            "data_class": "model_file_archive_distribution",
        }
    except Exception as e:
        nomads = {"ok": False, "error": str(e)}

    # --- Charts ---
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        Path("visuals/latest").mkdir(parents=True, exist_ok=True)

        def style(ax):
            ax.set_facecolor("#0a1628")
            ax.tick_params(colors="#b8c9d9")
            ax.grid(True, alpha=0.25, color="#1a3050")

        if space.get("ok") and space.get("kp_series"):
            fig, ax = plt.subplots(figsize=(10, 3.4))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            ys = [float(p["kp"] or 0) for p in space["kp_series"]]
            ax.plot(range(len(ys)), ys, color="#a78bfa", linewidth=1.8)
            ax.fill_between(range(len(ys)), ys, alpha=0.25, color="#a78bfa")
            ax.set_ylim(0, max(9, max(ys) + 1 if ys else 5))
            ax.set_title(f"Planetary K-index (NOAA SWPC) — {date}", color="#e8f4ff")
            ax.set_ylabel("Kp", color="#e8f4ff")
            fig.tight_layout()
            fig.savefig("visuals/latest/space-kp-index.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if space.get("ok") and space.get("xray_series_tail"):
            fig, ax = plt.subplots(figsize=(10, 3.4))
            fig.patch.set_facecolor("#0a1628")
            style(ax)
            ys = [float(p["flux"]) for p in space["xray_series_tail"]]
            ax.semilogy(range(len(ys)), ys, color="#f472b6", linewidth=1.5)
            ax.set_title(f"GOES X-ray flux (NOAA SWPC) — {date}", color="#e8f4ff")
            ax.set_ylabel("Flux", color="#e8f4ff")
            fig.tight_layout()
            fig.savefig("visuals/latest/space-goes-xray.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)

        if gfs.get("ok") and gfs.get("hourly", {}).get("temperature_2m"):
            fig, axes = plt.subplots(2, 1, figsize=(10, 5.2), sharex=True)
            fig.patch.set_facecolor("#0a1628")
            times = gfs["hourly"]["time"]
            labels = [t[-5:] if "T" in t else t for t in times]
            for ax in axes:
                style(ax)
            temps_f = [round(t * 9 / 5 + 32, 1) if t is not None else None for t in gfs["hourly"]["temperature_2m"]]
            axes[0].plot(range(len(temps_f)), temps_f, color="#00d4ff", linewidth=2)
            axes[0].set_ylabel("°F", color="#e8f4ff")
            axes[0].set_title(f"GFS seamless · Casey IL temperature (°F) — {date}", color="#e8f4ff")
            cape = [c if c is not None else 0 for c in (gfs["hourly"].get("cape") or [])]
            axes[1].bar(range(len(cape)), cape, color="#fbbf24", alpha=0.85)
            axes[1].set_ylabel("CAPE J/kg", color="#e8f4ff")
            if len(labels) > 10:
                step = max(1, len(labels) // 10)
                axes[1].set_xticks(list(range(0, len(labels), step)))
                axes[1].set_xticklabels([labels[i] for i in range(0, len(labels), step)], rotation=45, ha="right")
            fig.tight_layout()
            fig.savefig("visuals/latest/gfs-casey-forecast.png", dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close(fig)
    except Exception as e:
        print("charts", e)

    payload = {
        "schema": "uogw.space_gfs_snapshot.v1",
        "ok": True,
        "date_utc": date,
        "generated_at_utc": now_s,
        "data_vs_telemetry": {
            "live_telemetry": (
                "Serial/APRS/WSPR/GPS packets from an MSDS payload or a radiosonde while it is transmitting in flight."
            ),
            "near_real_time_products": (
                "SWPC Kp and GOES X-rays update frequently from operational sensors — still not MSDS flight telemetry."
            ),
            "model_forecast": (
                "NOAA GFS (and Open-Meteo GFS seamless) are predicted grids, not measured balloon or radiosonde paths."
            ),
            "archive_counts": (
                "Illinois radiosonde 3-day counts come from public RAOB archives (launch schedule times), "
                "not live trackers on each balloon."
            ),
        },
        "space": space,
        "gfs": gfs,
        "nomads": nomads,
        "charts": {
            "kp": "visuals/latest/space-kp-index.png",
            "xray": "visuals/latest/space-goes-xray.png",
            "gfs_casey": "visuals/latest/gfs-casey-forecast.png",
        },
        "curator": "Midwest Stratospheric Data Systems",
        "hub": "https://midwestsds.com/msds-data-hub.html#space-data",
    }

    for p in [
        Path(f"data/entries/{date}/space-gfs-snapshot.json"),
        Path("data/latest/space-gfs-snapshot.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/space-gfs.json").write_text(
        json.dumps(
            {
                "ok": True,
                "generated_at_utc": now_s,
                "space_ok": bool(space.get("ok")),
                "gfs_ok": bool(gfs.get("ok")),
                "nomads_ok": bool(nomads.get("ok")),
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps({"ok": True, "space": space.get("ok"), "gfs": gfs.get("ok"), "nomads": nomads.get("ok")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
