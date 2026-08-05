#!/usr/bin/env python3
"""Generate UOGW PNG charts + GitHub-native CHARTS.md from data/latest."""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


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
        obs = c.get("observation") or {}
        t = obs.get("temperature_c")
        if t is None and isinstance(c.get("current"), dict):
            t = c["current"].get("temperature_2m")
        if t is None:
            continue
        city_rows.append((c.get("name") or c.get("id"), float(t), c.get("lat"), c.get("lon")))
    city_rows.sort(key=lambda x: x[1])

    if city_rows:
        fig, ax = plt.subplots(figsize=(10, max(4, 0.28 * len(city_rows))))
        names = [r[0] for r in city_rows]
        temps = [r[1] for r in city_rows]
        colors = [
            RED if t >= 35 else ORANGE if t >= 30 else CYAN if t >= 0 else "#74b9ff" for t in temps
        ]
        ax.barh(names, temps, color=colors)
        ax.set_xlabel("Temperature (C)")
        ax.set_title(f"UOGW Global City Temperatures - {date}")
        ax.grid(True, axis="x", alpha=0.4)
        save(fig, "global-city-temperatures.png")

        fig, ax = plt.subplots(figsize=(11, 5.5))
        sc = ax.scatter(
            [r[3] for r in city_rows],
            [r[2] for r in city_rows],
            c=[r[1] for r in city_rows],
            cmap="coolwarm",
            s=60,
            edgecolors="white",
            linewidths=0.4,
        )
        cb = plt.colorbar(sc, ax=ax, fraction=0.03)
        cb.set_label("C")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title(f"UOGW City Temperature Map - {date}")
        ax.set_xlim(-180, 180)
        ax.set_ylim(-60, 75)
        ax.grid(True, alpha=0.35)
        save(fig, "global-city-temp-map.png")

    cob = casey.get("observations") or []
    if not cob and isinstance(casey.get("hourly"), dict):
        times = casey["hourly"].get("time") or []
        temps = casey["hourly"].get("temperature_2m") or []
        cob = [
            {"time": t, "temperature_c": temps[i] if i < len(temps) else None}
            for i, t in enumerate(times)
        ]
    if cob:
        times = [str(o.get("time", ""))[-5:] for o in cob]
        vals = [o.get("temperature_c") for o in cob]
        fig, ax1 = plt.subplots(figsize=(11, 4.2))
        ax1.plot(times, vals, color=CYAN, marker="o", markersize=3)
        ax1.set_ylabel("Temperature (C)")
        ax1.set_xlabel("Local time")
        ax1.set_title(f"Casey IL Hourly Temperature - {casey.get('date', date)}")
        ax1.grid(True, alpha=0.35)
        if len(times) > 12:
            step = max(1, len(times) // 12)
            ax1.set_xticks(list(range(0, len(times), step)))
            ax1.set_xticklabels(
                [times[i] for i in range(0, len(times), step)], rotation=45, ha="right"
            )
        save(fig, "casey-hourly-temperature.png")

    ndbc_obs = ndbc.get("observations") or {}
    if ndbc_obs:
        sids = list(ndbc_obs.keys())
        waves = [(ndbc_obs[s].get("latest_observation") or {}).get("wave_height_m") for s in sids]
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(sids, [w if w is not None else 0 for w in waves], color=CYAN)
        ax.set_ylabel("Wave height (m)")
        ax.set_title(f"NDBC Wave Height - {date}")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, axis="y", alpha=0.35)
        save(fig, "ndbc-marine-samples.png")

    counts = anomaly.get("counts") or {}
    if counts:
        labels = ["alert", "watch", "info"]
        vals = [counts.get(k, 0) for k in labels]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(labels, vals, color=[RED, ORANGE, YELLOW])
        ax.set_title(f"Anomaly Flags - {date} total={counts.get('total', sum(vals))}")
        ax.grid(True, axis="y", alpha=0.35)
        save(fig, "anomaly-severity.png")

    clim_ok = [c for c in (climate.get("cities") or []) if c.get("ok")]
    if clim_ok:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        labels = [c.get("id") for c in clim_ok]
        x = np.arange(len(labels))
        ax.bar(
            x - 0.2,
            [c.get("temperature_max_c") for c in clim_ok],
            width=0.4,
            color=ORANGE,
            label="Tmax",
        )
        ax.bar(
            x + 0.2,
            [c.get("temperature_min_c") for c in clim_ok],
            width=0.4,
            color=CYAN,
            label="Tmin",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel("C")
        ax.legend()
        ax.grid(True, axis="y", alpha=0.35)
        ax.set_title(f"Research Cities Daily Tmin Tmax - {climate.get('date', date)}")
        save(fig, "research-cities-tminmax.png")

    # summary card
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    lines = [
        "UOGW Daily Visual Summary",
        f"Date (UTC): {date}",
        f"Cities plotted: {len(city_rows)}",
        f"Casey hours: {len(cob)}",
        f"NDBC stations: {len(ndbc_obs)}",
        f"Anomaly total: {(counts or {}).get('total', 'n/a')}",
        "Midwest Stratospheric Data Systems",
    ]
    y = 0.9
    for i, line in enumerate(lines):
        ax.text(
            0.05,
            y,
            line,
            transform=ax.transAxes,
            fontsize=16 if i == 0 else 11,
            fontweight="bold" if i == 0 else "normal",
            color=CYAN if i == 0 else "#e8f4ff",
            family="monospace",
        )
        y -= 0.1
    save(fig, "daily-summary-card.png")

    def esc(s):
        return str(s).replace('"', "'").replace("[", "(").replace("]", ")")[:36]

    md = [
        f"# UOGW Charts - {date}",
        "",
        "Generated automatically from repository data. View on GitHub.",
        "",
        f"_Generated at {now} UTC · Midwest Stratospheric Data Systems_",
        "",
        "## PNG charts",
        "",
    ]
    for title, fn in [
        ("Global city temperatures", "global-city-temperatures.png"),
        ("City temperature map", "global-city-temp-map.png"),
        ("Casey hourly temperature", "casey-hourly-temperature.png"),
        ("NDBC marine samples", "ndbc-marine-samples.png"),
        ("Anomaly severity", "anomaly-severity.png"),
        ("Research cities Tmin/Tmax", "research-cities-tminmax.png"),
        ("Daily summary card", "daily-summary-card.png"),
    ]:
        md += [f"### {title}", "", f"![{title}](./{fn})", ""]

    if counts:
        md += [
            "## Anomaly severity (Mermaid)",
            "",
            "```mermaid",
            "pie showData",
            f"  title Anomaly flags {date}",
        ]
        for k in ("alert", "watch", "info"):
            md.append(f'  "{k}" : {int(counts.get(k, 0))}')
        md += ["```", ""]

    if city_rows:
        sample = city_rows[-12:] if len(city_rows) > 12 else city_rows
        labels = ", ".join('"' + esc(r[0].split(",")[0]) + '"' for r in sample)
        vals = ", ".join(str(round(r[1], 1)) for r in sample)
        md += [
            "## City temperatures (Mermaid xychart)",
            "",
            "```mermaid",
            "xychart-beta",
            f'  title "City temperatures C - {date}"',
            f"  x-axis [{labels}]",
            '  y-axis "Temp C"',
            f"  bar [{vals}]",
            "```",
            "",
        ]

    md += [
        "## Snapshot table",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Date UTC | {date} |",
        f"| Cities OK | {len(city_rows)} |",
    ]
    if city_rows:
        md.append(f"| City T min/max C | {city_rows[0][1]} / {city_rows[-1][1]} |")
    md += [
        f"| Anomaly total | {counts.get('total', 'n/a') if counts else 'n/a'} |",
        f"| Casey hours | {len(cob) or 'n/a'} |",
        f"| NDBC samples | {len(ndbc_obs) or 'n/a'} |",
        "",
        "Also embedded in the repository [README](../../README.md).",
        "",
    ]

    md_text = "\n".join(md) + "\n"
    for d in out_dirs:
        d.mkdir(parents=True, exist_ok=True)
        (d / "CHARTS.md").write_text(md_text)
        written.append(str(d / "CHARTS.md"))

    Path("visuals/README.md").write_text(
        "\n".join(
            [
                "# UOGW Visuals",
                "",
                "Charts are generated **automatically** by `charts-daily.yml`.",
                "",
                "- Schedule: 11:00 UTC daily",
                "- Also runs after key data workflows complete",
                "- Script: `scripts/generate_charts.py`",
                "",
                "**[latest/CHARTS.md](./latest/CHARTS.md)**",
                "",
                "![Global city temperatures](./latest/global-city-temperatures.png)",
                "",
            ]
        )
        + "\n"
    )

    manifest = {
        "schema": "uogw.visuals_manifest.v2",
        "date_utc": date,
        "generated_at_utc": now,
        "charts_md": "visuals/latest/CHARTS.md",
        "png_count": sum(1 for w in written if w.endswith(".png")),
        "automated": True,
        "curator": "Midwest Stratospheric Data Systems",
    }
    for p in [
        Path(f"visuals/{date}/manifest.json"),
        Path("visuals/latest/manifest.json"),
        Path(f"data/entries/{date}/visuals-manifest.json"),
        Path("data/latest/visuals-manifest.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(manifest, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/charts.json").write_text(
        json.dumps(
            {
                "source": "uogw-charts",
                "ok": True,
                "automated": True,
                "date": date,
                "png_files": len([w for w in written if w.endswith(".png")]),
                "markdown": "visuals/latest/CHARTS.md",
                "generated_at_utc": now,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"charts written: {len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
