#!/usr/bin/env python3
"""UOGW Weekly Status Report generator.

Reads the latest JSON packages under data/latest/ and writes a markdown
report to reports/weekly/YYYY-Wxx-uogw-status.md plus reports/latest.md.

Designed to run under GitHub Actions (ubuntu-latest, python3).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "data" / "latest"
REPORTS = ROOT / "reports"
WEEKLY = REPORTS / "weekly"


def load(name: str) -> dict[str, Any] | None:
    p = LATEST / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def iso_week(dt: datetime) -> str:
    return f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"


def f_to_c(f: float) -> float:
    return (f - 32) * 5 / 9


def main() -> int:
    now = datetime.now(timezone.utc)
    week = iso_week(now)
    date_str = now.strftime("%Y-%m-%d")

    summary = load("summary.json") or {}
    analytics = load("science-analytics.json") or {}
    anomaly = load("anomaly-report.json") or {}
    health = load("health-report.json") or {}
    research = load("research-summary.json") or {}
    pretornado = load("pre-tornado-clark.json") or {}
    status = load("../status/last_update.json")  # may not exist relative; try absolute
    if status is None:
        status_path = ROOT / "status" / "last_update.json"
        if status_path.exists():
            try:
                status = json.loads(status_path.read_text(encoding="utf-8"))
            except Exception:
                status = {}

    # Coverage & indexes
    indexes = summary.get("indexes") or research.get("indexes") or {}
    coverage = analytics.get("coverage") or {}
    surface = analytics.get("surface") or {}
    extremes = analytics.get("extremes") or {}
    heat_flags = analytics.get("heat_index_flags") or []
    anomaly_counts = (anomaly.get("counts") or analytics.get("anomalies", {}).get("counts") or {})
    health_summary = health.get("summary") or {}
    pret_score = (pretornado.get("probability_research") or {}).get("score_0_to_100")
    pret_level = (pretornado.get("probability_research") or {}).get("level_label") or (pretornado.get("probability_research") or {}).get("level")

    # Temperature helpers
    g_temp_f = (surface.get("global_city_temperature") or {}).get("fahrenheit") or {}
    casey_f = (surface.get("casey_temperature") or {}).get("fahrenheit") or {}

    hottest = extremes.get("hottest") or {}
    coldest = extremes.get("coldest") or {}

    lines: list[str] = []
    lines.append(f"# UOGW Weekly Status Report — {week}")
    lines.append("")
    lines.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC")
    lines.append("**Curator:** Midwest Stratospheric Data Systems (Aerostratospheric)")
    lines.append("**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather")
    lines.append("**Data Hub:** https://midwestsds.com/msds-data-hub.html")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Executive Snapshot")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Catalog datasets | **{indexes.get('dataset_count') or research.get('catalog', {}).get('dataset_count') or 25}** |")
    lines.append(f"| Global city samples (OK) | **{coverage.get('global_cities_ok', indexes.get('global_city_ok', '—'))} / {coverage.get('global_cities_total', indexes.get('global_city_samples', 34))}** |")
    lines.append(f"| IGRA stations indexed | **{indexes.get('igra_stations', '—'):,}** |")
    lines.append(f"| NDBC stations indexed | **{indexes.get('ndbc_stations', '—'):,}** |")
    lines.append(f"| GHCN stations indexed | **{indexes.get('ghcn_stations', '—'):,}** |")
    lines.append(f"| Casey hourly observations | **{coverage.get('casey_hourly_count', '—')}** |")
    lines.append(f"| NDBC realtime samples | **{coverage.get('ndbc_stations_sampled', '—')}** stations |")
    ok = health_summary.get("ok", "—")
    total = health_summary.get("total", "—")
    lines.append(f"| Health checks | **{ok} / {total} OK** |")
    lines.append(f"| Anomaly flags (research) | **{anomaly_counts.get('total', 0)}** ({anomaly_counts.get('alert', 0)} Alert · {anomaly_counts.get('watch', 0)} Watch) |")
    if pret_score is not None:
        lines.append(f"| Pre-tornado Clark Co. score | **{pret_score} / 100 ({pret_level or '—'})** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Surface Conditions (Global City Sample)")
    lines.append("")
    if g_temp_f:
        lines.append(f"- **Temperature range:** {g_temp_f.get('min', '—')} °F → **{g_temp_f.get('max', '—')} °F**")
        lines.append(f"  Mean ≈ {g_temp_f.get('mean', '—'):.1f} °F · Median ≈ {g_temp_f.get('median', '—'):.1f} °F")
    if hottest:
        lines.append(f"- Hottest sample: **{hottest.get('name')}** ({hottest.get('temperature_f')} °F)")
    if coldest:
        lines.append(f"- Coldest sample: **{coldest.get('name')}** ({coldest.get('temperature_f')} °F)")
    lines.append("")

    if heat_flags:
        lines.append("### Heat-Index Flags (research)")
        lines.append("")
        lines.append("| City | T (°F) | RH % | Heat Index (°F) | Level |")
        lines.append("|------|--------|------|-----------------|-------|")
        for h in heat_flags[:10]:
            lines.append(
                f"| {h.get('name')} | {h.get('temperature_f')} | {h.get('relative_humidity_pct')} | "
                f"**{h.get('heat_index_f')}** | {h.get('level')} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Local Midwest Focus — Casey, IL")
    lines.append("")
    if casey_f:
        lines.append(f"- Daily range: {casey_f.get('min')} – {casey_f.get('max')} °F (mean {casey_f.get('mean'):.1f} °F)")
    lines.append("- NASA GLOBE registration: **GO-4VW9B**")
    if pret_score is not None:
        lines.append("")
        lines.append("### Pre-Tornado Research Score (Clark County)")
        lines.append("")
        lines.append(f"- **Score:** {pret_score} / 100 → **{pret_level}**")
        lines.append("- **Disclaimer:** Research screening only. Not an NWS product.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Anomaly Screening (Research Only)")
    lines.append("")
    lines.append(f"| Severity | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| Alert | {anomaly_counts.get('alert', 0)} |")
    lines.append(f"| Watch | {anomaly_counts.get('watch', 0)} |")
    lines.append(f"| Info | {anomaly_counts.get('info', 0)} |")
    lines.append("")
    top = (anomaly.get("anomalies") or analytics.get("anomalies", {}).get("top") or [])[:5]
    if top:
        lines.append("Top flags:")
        for a in top:
            lines.append(f"- **{a.get('severity', '').title()}** — {a.get('subject')}: {a.get('detail')}")
        lines.append("")
    lines.append("Full details: `data/latest/anomaly-report.json` · `docs/ANOMALY_METHODS.md`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## System Health")
    lines.append("")
    if health.get("ok"):
        lines.append("- Overall health: **OK**")
    lines.append(f"- Checks: {ok}/{total} passed")
    if health.get("critical_fail"):
        lines.append("- ⚠️ Critical failure detected — see health-report.json")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Citation")
    lines.append("")
    lines.append("> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW).")
    lines.append("> https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather")
    lines.append("")
    lines.append("Always cite upstream providers (Open-Meteo, NOAA NDBC / NCEI, NASA, etc.).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Open atmosphere. Open archives. Midwest-made flight data for everyone.*")
    lines.append("")

    content = "\n".join(lines)

    WEEKLY.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    out_week = WEEKLY / f"{week}-uogw-status.md"
    out_latest = REPORTS / "latest.md"

    out_week.write_text(content, encoding="utf-8")
    out_latest.write_text(content, encoding="utf-8")

    print(f"Wrote {out_week.relative_to(ROOT)}")
    print(f"Wrote {out_latest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
