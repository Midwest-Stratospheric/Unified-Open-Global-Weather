#!/usr/bin/env python3
"""UOGW scientific feature suite (4 modules).

1. Quality scorecard — observation completeness + package integrity
2. Change detection — deltas vs previous research summary / scorecard
3. Layer coverage report — six-layer observing system inventory
4. FAIR package card — research-ready citation / reuse metadata

Outputs under data/latest/ and reports/scientific/.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "data" / "latest"
STATUS = ROOT / "status"
REPORTS = ROOT / "reports" / "scientific"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    return (dt or now_utc()).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def feature_1_scorecard(research: dict, anomaly: dict, analytics: dict, now: datetime) -> dict:
    obs = research.get("observations_today") or {}
    idx = research.get("indexes") or {}
    checks = []

    def add(name: str, ok: bool, detail: Any = None) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    cities = obs.get("global_cities_ok") or 0
    add("global_city_samples", cities and cities > 0, cities)
    add("ndbc_realtime", (obs.get("ndbc_realtime_stations") or 0) > 0, obs.get("ndbc_realtime_stations"))
    add("casey_hourly", (obs.get("casey_hourly_count") or 0) > 0, obs.get("casey_hourly_count"))
    add("research_climate_cities", (obs.get("research_daily_climate_cities") or 0) > 0, obs.get("research_daily_climate_cities"))
    add("igra_index", (idx.get("igra_stations") or 0) > 0, idx.get("igra_stations"))
    add("science_package_present", (LATEST / "science-package.json").exists())
    add("research_summary_present", (LATEST / "research-summary.json").exists())

    ok_n = sum(1 for c in checks if c["ok"])
    total = len(checks)
    completeness = round(100.0 * ok_n / total, 1) if total else 0.0

    counts = anomaly.get("counts") or (analytics.get("anomalies") or {}).get("counts") or {}
    anomaly_total = counts.get("total", 0)

    # integrity: presence of key latest files
    key_files = [
        "science-package.json",
        "research-summary.json",
        "summary.json",
        "anomaly-report.json",
    ]
    present = sum(1 for f in key_files if (LATEST / f).exists())
    integrity = round(100.0 * present / len(key_files), 1)

    composite = round(0.55 * completeness + 0.25 * integrity + 0.20 * min(100.0, 50 + (cities or 0)), 1)
    # soften city influence: already in completeness
    composite = round(0.60 * completeness + 0.40 * integrity, 1)

    if composite >= 90:
        grade = "A"
    elif composite >= 80:
        grade = "B"
    elif composite >= 70:
        grade = "C"
    elif composite >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "schema": "uogw.scientific_scorecard.v1",
        "generated_at_utc": iso(now),
        "completeness_pct": completeness,
        "checks_ok": ok_n,
        "checks_total": total,
        "checks": checks,
        "integrity_pct": integrity,
        "composite_score": composite,
        "grade": grade,
        "anomaly_flags_total": anomaly_total,
        "indexes": {
            "igra_stations": idx.get("igra_stations"),
            "ndbc_stations": idx.get("ndbc_stations"),
            "ghcn_stations": idx.get("ghcn_stations"),
        },
        "notes": [
            "Composite = 0.60·completeness + 0.40·integrity",
            "Research screening only — not an NWS product",
        ],
    }


def feature_2_change_detection(scorecard: dict, research: dict, now: datetime) -> dict:
    prev = load_json(LATEST / "scientific_scorecard_previous.json") or {}
    prev_research = load_json(LATEST / "research-summary_previous.json") or {}

    out = {
        "schema": "uogw.change_detection.v1",
        "generated_at_utc": iso(now),
        "compared_to": prev.get("generated_at_utc") or prev_research.get("generated_at_utc"),
        "score_delta": None,
        "observation_deltas": [],
        "summary": [],
    }

    if prev:
        out["score_delta"] = round(
            float(scorecard.get("composite_score", 0)) - float(prev.get("composite_score", 0)), 1
        )

    prev_obs = (prev_research.get("observations_today") or {})
    cur_obs = (research.get("observations_today") or {})
    for key in sorted(set(list(prev_obs.keys()) + list(cur_obs.keys()))):
        a, b = prev_obs.get(key), cur_obs.get(key)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a != b:
            out["observation_deltas"].append({"field": key, "from": a, "to": b, "delta": b - a})

    if out["score_delta"] is not None:
        out["summary"].append(f"Composite score Δ {out['score_delta']}")
    out["summary"].append(f"Observation field deltas: {len(out['observation_deltas'])}")
    if not prev and not prev_research:
        out["summary"].append("First scientific baseline established")
    return out


def feature_3_layer_coverage(research: dict, now: datetime) -> dict:
    layers_def = [
        ("ground", ["global_cities_ok", "casey_hourly_count"]),
        ("marine", ["ndbc_realtime_stations"]),
        ("upper-air", ["igra_stations"]),
        ("stratospheric_space", []),
        ("satellite_model", []),
        ("flight", []),
    ]
    obs = research.get("observations_today") or {}
    idx = research.get("indexes") or {}

    layers = []
    for name, keys in layers_def:
        signals = []
        ok_signals = 0
        for k in keys:
            val = obs.get(k)
            if val is None:
                val = idx.get(k)
            signals.append({"key": k, "value": val})
            if isinstance(val, (int, float)) and val > 0:
                ok_signals += 1
        # structural presence
        if name == "ground":
            path_ok = (ROOT / "layers" / "ground").exists()
        elif name == "marine":
            path_ok = (ROOT / "layers" / "marine").exists()
        elif name == "upper-air":
            path_ok = (ROOT / "layers" / "upper-air").exists() or (idx.get("igra_stations") or 0) > 0
        elif name == "stratospheric_space":
            path_ok = (ROOT / "layers").exists()
        elif name == "satellite_model":
            path_ok = (LATEST / "science-package.json").exists()
        else:
            path_ok = True
        layers.append(
            {
                "layer": name,
                "path_present": path_ok,
                "signals": signals,
                "signals_ok": ok_signals,
                "active": path_ok and (ok_signals > 0 or not keys),
            }
        )

    active = sum(1 for L in layers if L.get("active"))
    return {
        "schema": "uogw.layer_coverage.v1",
        "generated_at_utc": iso(now),
        "layers": layers,
        "layers_active": active,
        "layers_total": len(layers),
        "coverage_pct": round(100.0 * active / len(layers), 1) if layers else 0.0,
        "notes": [
            "Layer activity is heuristic from indexes/observations + directory presence",
            "Flight layer expands when MSDS HAB packages are published",
        ],
    }


def feature_4_fair_card(scorecard: dict, coverage: dict, now: datetime) -> dict:
    return {
        "schema": "uogw.fair_package_card.v1",
        "generated_at_utc": iso(now),
        "title": "Unified Open Global Weather daily science package",
        "version_hint": "See GitHub Releases (vMAJOR.MINOR)",
        "repository": "https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather",
        "data_hub": "https://midwestsds.com/msds-data-hub.html",
        "license_note": "Derived products often CC BY 4.0; always retain upstream terms",
        "findable": {
            "identifiers": [
                "data/latest/science-package.json",
                "data/latest/research-summary.json",
                "catalog/catalog.json",
            ],
            "keywords": [
                "atmospheric science",
                "open data",
                "multi-layer",
                "anomaly detection",
                "Midwest Stratospheric",
            ],
        },
        "accessible": {
            "access": "public git + Data Hub",
            "formats": ["JSON", "PNG charts", "Markdown"],
        },
        "interoperable": {
            "layers": ["ground", "marine", "upper-air", "stratospheric", "satellite", "flight"],
            "related": ["aerostratospheric-defense-gir", "msds-data"],
        },
        "reusable": {
            "citation": "Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW).",
            "intended_use": "Open research, education, cross-layer atmospheric analysis",
            "not_for": "Sole operational warning service",
        },
        "quality_snapshot": {
            "grade": scorecard.get("grade"),
            "composite_score": scorecard.get("composite_score"),
            "completeness_pct": scorecard.get("completeness_pct"),
        },
        "coverage_snapshot": {
            "layers_active": coverage.get("layers_active"),
            "layers_total": coverage.get("layers_total"),
            "coverage_pct": coverage.get("coverage_pct"),
        },
    }


def write_markdown(scorecard: dict, changes: dict, coverage: dict, fair: dict, now: datetime) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# UOGW Scientific Features Digest — {now.strftime('%Y-%m-%d')}",
        "",
        f"Generated: {iso(now)}",
        "",
        "## 1. Quality scorecard",
        "",
        f"- Grade: **{scorecard.get('grade')}** (composite {scorecard.get('composite_score')})",
        f"- Completeness: {scorecard.get('completeness_pct')}% "
        f"({scorecard.get('checks_ok')}/{scorecard.get('checks_total')})",
        f"- Integrity: {scorecard.get('integrity_pct')}%",
        f"- Anomaly flags (research): {scorecard.get('anomaly_flags_total')}",
        "",
        "## 2. Change detection",
        "",
    ]
    for s in changes.get("summary") or []:
        lines.append(f"- {s}")
    for d in (changes.get("observation_deltas") or [])[:12]:
        lines.append(f"- `{d.get('field')}`: {d.get('from')} → {d.get('to')} (Δ {d.get('delta')})")
    lines += ["", "## 3. Layer coverage", ""]
    for L in coverage.get("layers") or []:
        lines.append(
            f"- **{L.get('layer')}**: active={L.get('active')} signals_ok={L.get('signals_ok')}"
        )
    lines += [
        "",
        f"Overall layer coverage: {coverage.get('coverage_pct')}%",
        "",
        "## 4. FAIR package card",
        "",
        f"- {fair.get('title')}",
        f"- {fair.get('repository')}",
        "",
        "---",
        "*Open atmospheric research features — not an official warning product.*",
        "",
    ]
    text = "\n".join(lines)
    (REPORTS / "latest.md").write_text(text, encoding="utf-8")
    (REPORTS / f"{now.strftime('%Y-%m-%d')}-scientific.md").write_text(text, encoding="utf-8")


def main() -> int:
    now = now_utc()
    LATEST.mkdir(parents=True, exist_ok=True)

    research = load_json(LATEST / "research-summary.json") or {}
    anomaly = load_json(LATEST / "anomaly-report.json") or {}
    analytics = load_json(LATEST / "science-analytics.json") or {}

    # rotate previous
    for name in ("scientific_scorecard_latest.json", "research-summary.json"):
        src = LATEST / name
        if src.exists():
            if name == "scientific_scorecard_latest.json":
                dest = LATEST / "scientific_scorecard_previous.json"
            else:
                dest = LATEST / "research-summary_previous.json"
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    scorecard = feature_1_scorecard(research, anomaly, analytics, now)
    changes = feature_2_change_detection(scorecard, research, now)
    coverage = feature_3_layer_coverage(research, now)
    fair = feature_4_fair_card(scorecard, coverage, now)

    write_json(LATEST / "scientific_scorecard_latest.json", scorecard)
    write_json(LATEST / "change_detection_latest.json", changes)
    write_json(LATEST / "layer_coverage_latest.json", coverage)
    write_json(LATEST / "fair_package_card_latest.json", fair)
    write_markdown(scorecard, changes, coverage, fair, now)

    print("UOGW scientific features OK", scorecard.get("grade"), scorecard.get("composite_score"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
