#!/usr/bin/env python3
"""Generate UOGW PNG charts + CHARTS.md. Temperatures displayed in Fahrenheit."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def c_to_f(c):
    if c is None:
        return None
    try:
        return round(float(c) * 9.0 / 5.0 + 32.0, 1)
    except (TypeError, ValueError):
        return None


def load(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def city_temp_c(c: dict):
    obs = c.get("observation") or {}
    t = obs.get("temperature_c")
    if t is not None:
        return t
    cur = c.get("current") or {}
    t = cur.get("temperature_2m")
    if t is not None:
        return t
    return cur.get("temperature_c")


def main() -> int:
    os.chdir(ROOT)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cities = load(Path("data/latest/global-cities.json")) or load(
        Path("layers/ground/samples/cities-latest.json")
    ) or {}
    ndbc = load(Path("data/latest/ndbc-realtime.json")) or {}
    casey = load(Path("data/latest/casey-hourly.json")) or load(
        Path("layers/ground/casey/latest.json")
    ) or {}
    anomaly = load(Path("data/latest/anomaly-report.json")) or {}
    climate = load(Path("data/latest/daily-climate.json")) or {}
    science = load(Path("data/latest/science-package.json")) or {}

    out_dirs = [Path(f"visuals/{date}"), Path("visuals/latest")]
    written: list[str] = []

    def save(fig, name: str):
        for d in out_dirs:
            d.mkdir(parents=True, exist_ok=True)
            path = d / name
            fig.savefig(path, dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
            written.append(str(path))
        plt.close(fig)

    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.facecolor": "#0a1628",
            "figure.facecolor": "#0a1628",
            "axes.edgecolor": "#00d4ff",
            "axes.labelcolor": "#e8f4ff",
            "xtick.color": "#b8c9d9",
            "ytick.color": "#b8c9d9",
            "text.color": "#e8f4ff",
            "grid.color": "#1a3050",
        }
    )
    CYAN, ORANGE, RED, YELLOW = "#00d4ff", "#ff9f43", "#ff6b6b", "#feca57"

    city_rows = []
    for c in cities.get("cities") or []:
        if not c.get("ok"):
            continue
        t_c = city_temp_c(c)
        t_f = c_to_f(t_c)
        if t_f is None:
            continue
        city_rows.append((c.get("name") or c.get("id"), t_f, c.get("lat"), c.get("lon"), t_c))
    city_rows.sort(key=lambda x: x[1])

    if city_rows:
        fig, ax = plt.subplots(figsize=(10, max(4, 0.28 * len(city_rows))))
        names = [r[0] for r in city_rows]
        temps_f = [r[1] for r in city_rows]
        colors = [RED if t >= 95 else ORANGE if t >= 86 else CYAN if t >= 32 else "#74b9ff" for t in temps_f]
        ax.barh(names, temps_f, color=colors)
        ax.set_xlabel("Temperature (°F)")
        ax.set_title(f"UOGW Global City Temperatures (°F) — {date}")
        ax.grid(True, axis="x", alpha=0.4)
        save(fig, "global-city-temperatures.png")

        fig, ax = plt.subplots(figsize=(11, 5.5))
        sc = ax.scatter([r[3] for r in city_rows], [r[2] for r in city_rows], c=[r[1] for r in city_rows], cmap="coolwarm", s=60, edgecolors="white", linewidths=0.4)
        cb = plt.colorbar(sc, ax=ax, fraction=0.03)
        cb.set_label("°F")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title(f"UOGW City Temperature Map (°F) — {date}")
        ax.set_xlim(-180, 180)
        ax.set_ylim(-60, 75)
        ax.grid(True, alpha=0.35)
        save(fig, "global-city-temp-map.png")

    cob = casey.get("observations") or []
    if not cob and isinstance(casey.get("hourly"), dict):
        times = casey["hourly"].get("time") or []
        temps = casey["hourly"].get("temperature_2m") or []
        cob = [{"time": t, "temperature_c": temps[i] if i < len(temps) else None} for i, t in enumerate(times)]
    if cob:
        times = [str(o.get("time", ""))[-5:] for o in cob]
        vals_f = [c_to_f(o.get("temperature_c")) for o in cob]
        fig, ax1 = plt.subplots(figsize=(11, 4.2))
        ax1.plot(times, vals_f, color=CYAN, marker="o", markersize=3)
        ax1.set_ylabel("Temperature (°F)")
        ax1.set_xlabel("Local time")
        ax1.set_title(f"Casey, IL Hourly Temperature (°F) — {casey.get('date', date)}")
        ax1.grid(True, alpha=0.35)
        if len(times) > 12:
            step = max(1, len(times) // 12)
            ax1.set_xticks(list(range(0, len(times), step)))
            ax1.set_xticklabels([times[i] for i in range(0, len(times), step)], rotation=45, ha="right")
        save(fig, "casey-hourly-temperature.png")

    ndbc_obs = ndbc.get("observations") or {}
    if ndbc_obs:
        sids = list(ndbc_obs.keys())
        waves = [(ndbc_obs[s].get("latest_observation") or {}).get("wave_height_m") for s in sids]
        wtemps_f = [c_to_f((ndbc_obs[s].get("latest_observation") or {}).get("water_temp_c")) for s in sids]
        atemps_f = [c_to_f((ndbc_obs[s].get("latest_observation") or {}).get("air_temp_c")) for s in sids]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        x = np.arange(len(sids))
        axes[0].bar(x, [w if w is not None else 0 for w in waves], color=CYAN)
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(sids, rotation=45, ha="right")
        axes[0].set_ylabel("Wave height (m)")
        axes[0].set_title("NDBC Wave Height")
        axes[0].grid(True, axis="y", alpha=0.35)
        axes[1].plot(x, wtemps_f, "o-", color=CYAN, label="Water °F")
        axes[1].plot(x, atemps_f, "s--", color=ORANGE, label="Air °F")
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(sids, rotation=45, ha="right")
        axes[1].set_ylabel("Temperature (°F)")
        axes[1].set_title("NDBC Water / Air Temp (°F)")
        axes[1].legend()
        axes[1].grid(True, alpha=0.35)
        fig.suptitle(f"UOGW Marine Samples — {date}", color="#e8f4ff")
        fig.tight_layout()
        save(fig, "ndbc-marine-samples.png")

    hum_rows = []
    for c in cities.get("cities") or []:
        if not c.get("ok"):
            continue
        obs = c.get("observation") or {}
        cur = c.get("current") or {}
        h = obs.get("relative_humidity_pct", cur.get("relative_humidity_2m"))
        if not isinstance(h, (int, float)):
            continue
        hum_rows.append((c.get("name") or c.get("id"), float(h)))
    hum_rows.sort(key=lambda x: x[1])
    if hum_rows:
        fig, ax = plt.subplots(figsize=(10, max(4, 0.28 * len(hum_rows))))
        ax.barh([r[0] for r in hum_rows], [r[1] for r in hum_rows], color=CYAN)
        ax.set_xlabel("Relative humidity (%)")
        ax.set_title(f"UOGW Global City Relative Humidity — {date}")
        ax.grid(True, axis="x", alpha=0.4)
        save(fig, "global-city-humidity.png")

    counts = anomaly.get("counts") or {}
    if counts:
        labels = ["alert", "watch", "info"]
        vals = [counts.get(k, 0) for k in labels]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(labels, vals, color=[RED, ORANGE, YELLOW])
        ax.set_title(f"Anomaly Flags — {date} (total={counts.get('total', sum(vals))})")
        ax.grid(True, axis="y", alpha=0.35)
        save(fig, "anomaly-severity.png")

    clim_rows = []
    for c in climate.get("cities") or []:
        if not c.get("ok"):
            continue
        tmax = c_to_f(c.get("temperature_max_c"))
        tmin = c_to_f(c.get("temperature_min_c"))
        if tmax is None and tmin is None:
            continue
        clim_rows.append({"id": c.get("id") or c.get("name") or "?", "tmax_f": tmax, "tmin_f": tmin})
    if not clim_rows:
        for c in science.get("daily_climate_research_cities") or []:
            if not isinstance(c, dict) or c.get("ok") is False:
                continue
            tmax = c_to_f(c.get("temperature_max_c") or c.get("tmax_c"))
            tmin = c_to_f(c.get("temperature_min_c") or c.get("tmin_c"))
            if tmax is None and tmin is None:
                continue
            clim_rows.append({"id": c.get("id") or c.get("name") or "?", "tmax_f": tmax, "tmin_f": tmin})
    if not clim_rows and city_rows:
        for name, tf, _lat, _lon, _tc in city_rows[-10:]:
            clim_rows.append({"id": str(name).split(",")[0][:12], "tmax_f": tf, "tmin_f": tf})

    if clim_rows:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        labels = [r["id"] for r in clim_rows]
        x = np.arange(len(labels))
        ax.bar(x - 0.2, [r["tmax_f"] or 0 for r in clim_rows], width=0.4, color=ORANGE, label="Tmax °F")
        ax.bar(x + 0.2, [r["tmin_f"] or 0 for r in clim_rows], width=0.4, color=CYAN, label="Tmin °F")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel("Temperature (°F)")
        ax.legend()
        ax.grid(True, axis="y", alpha=0.35)
        ax.set_title(f"Research Cities Daily Tmin / Tmax (°F) — {climate.get('date') or science.get('date_utc') or date}")
        save(fig, "research-cities-tminmax.png")
    else:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.axis("off")
        ax.text(0.5, 0.5, "Research cities Tmin/Tmax unavailable", ha="center", va="center", color="#e8f4ff")
        save(fig, "research-cities-tminmax.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    lines = [
        "UOGW Daily Visual Summary (°F)",
        f"Date (UTC): {date}",
        f"Cities plotted: {len(city_rows)}",
        f"City T min/max: {(city_rows[0][1] if city_rows else 'n/a')} / {(city_rows[-1][1] if city_rows else 'n/a')} °F",
        f"Casey hours: {len(cob)}",
        f"NDBC stations: {len(ndbc_obs)}",
        f"Humidity cities: {len(hum_rows)}",
        f"Anomaly total: {(counts or {}).get('total', 'n/a')}",
        "Midwest Stratospheric Data Systems",
    ]
    y = 0.92
    for i, line in enumerate(lines):
        ax.text(0.05, y, line, transform=ax.transAxes, fontsize=15 if i == 0 else 11, fontweight="bold" if i == 0 else "normal", color=CYAN if i == 0 else "#e8f4ff", family="monospace")
        y -= 0.09
    save(fig, "daily-summary-card.png")

    md = [
        f"# UOGW Charts — {date}",
        "",
        "Temperatures shown in **Fahrenheit (°F)**. Generated automatically from repository data.",
        "",
        f"_Generated at {now} UTC · Midwest Stratospheric Data Systems_",
        "",
        "## PNG charts",
        "",
    ]
    chart_specs = [
        ("Global city temperatures (°F)", "global-city-temperatures.png",
         "Horizontal bar chart of current surface air temperature for each successful global city sample. Bars sorted cold→hot; warmer colors mark heat (≥86°F / ≥95°F)."),
        ("City temperature map (°F)", "global-city-temp-map.png",
         "Scatter map of city samples by longitude/latitude, colored by temperature (°F). Shows geographic pattern of the daily open sample set."),
        ("Casey hourly temperature (°F)", "casey-hourly-temperature.png",
         "24-hour temperature trace for Casey, Illinois (MSDS home site). Useful for diurnal range and local extremes that feed anomaly rules."),
        ("NDBC marine samples", "ndbc-marine-samples.png",
         "NOAA NDBC buoy sample panel: wave height (meters) plus water and air temperature (°F) for stations in today's marine pull."),
        ("Global city relative humidity (%)", "global-city-humidity.png",
         "Relative humidity (%) for the global city sample network. Dry+hot combinations can contribute to compound research flags."),
        ("Anomaly severity", "anomaly-severity.png",
         "Count of UOGW research anomaly flags by severity (alert / watch / info). Not an NWS warning product."),
        ("Research cities Tmin/Tmax (°F)", "research-cities-tminmax.png",
         "Daily minimum and maximum temperatures for the research climate city set. Compares day-range width across selected locations."),
        ("Daily summary card", "daily-summary-card.png",
         "One-page snapshot of today's visual package: city count, temperature span, Casey hours, NDBC samples, and anomaly total."),
    ]
    for title, fn, desc in chart_specs:
        md += [f"### {title}", "", f"![{title}](./{fn})", "", f"*{desc}*", ""]
        if fn == "anomaly-severity.png":
            a = counts.get("alert", 0) if counts else 0
            w = counts.get("watch", 0) if counts else 0
            info = counts.get("info", 0) if counts else 0
            tot = counts.get("total", 0) if counts else 0
            md += [
                "#### Anomaly detection guide (what this graph means)",
                "",
                "UOGW counts **research flags** for the daily sample set — **not** National Weather Service warnings.",
                "",
                "| Severity | Meaning |",
                "|----------|---------|",
                "| **Alert** | Strong outlier vs thresholds or baseline (extreme heat/cold, |z| >= 3, very high waves). |",
                "| **Watch** | Elevated interest — heat/cold, wind, low pressure, or |z| >= 2.5 vs the 7-day baseline. |",
                "| **Info** | Lower urgency (hot + very dry, strong high, warm water sample). |",
                "",
                f"Today: **alert {a}** · **watch {w}** · **info {info}** · total **{tot}**",
                "",
                "Full methods: [docs/ANOMALY_METHODS.md](../../docs/ANOMALY_METHODS.md) · "
                "[ANOMALY_GUIDE.md](../ANOMALY_GUIDE.md) · [CHART_DESCRIPTIONS.md](../CHART_DESCRIPTIONS.md)",
                "",
            ]

    if counts:
        md += ["## Anomaly severity (Mermaid)", "", "```mermaid", "pie showData", f"  title Anomaly flags {date}"]
        for k in ("alert", "watch", "info"):
            md.append(f'  "{k}" : {int(counts.get(k, 0))}')
        md += ["```", ""]

    md += ["## Snapshot table (°F)", "", "| Metric | Value |", "|--------|-------|", f"| Date UTC | {date} |", f"| Cities OK | {len(city_rows)} |"]
    if city_rows:
        md.append(f"| City T min/max °F | {city_rows[0][1]} / {city_rows[-1][1]} |")
    md += [f"| Anomaly total | {counts.get('total', 'n/a') if counts else 'n/a'} |", ""]

    md_text = "\n".join(md) + "\n"
    for d in out_dirs:
        d.mkdir(parents=True, exist_ok=True)
        (d / "CHARTS.md").write_text(md_text)
        written.append(str(d / "CHARTS.md"))

    Path("visuals/README.md").write_text(
        "# UOGW Visuals\n\n**[latest/CHARTS.md](./latest/CHARTS.md)** · **[CHART_DESCRIPTIONS.md](./CHART_DESCRIPTIONS.md)** · **[ANOMALY_GUIDE.md](./ANOMALY_GUIDE.md)**\n"
    )

    for p in [
        Path(f"visuals/{date}/manifest.json"),
        Path("visuals/latest/manifest.json"),
        Path(f"data/entries/{date}/visuals-manifest.json"),
        Path("data/latest/visuals-manifest.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"schema": "uogw.visuals_manifest.v2", "date_utc": date, "generated_at_utc": now, "temperature_display_unit": "fahrenheit", "charts_md": "visuals/latest/CHARTS.md", "automated": True}, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/charts.json").write_text(json.dumps({"source": "uogw-charts", "ok": True, "date": date, "generated_at_utc": now}, indent=2) + "\n")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("hub_bundle", Path("scripts/hub_bundle.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    except Exception as e:
        print("hub_bundle skip", e)

    print(f"charts written={len(written)} cities={len(city_rows)} climate_rows={len(clim_rows)} unit=F")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
