#!/usr/bin/env python3
"""UOGW self-heal: keep data/latest pointers in sync with layer latests and entries."""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# source -> destinations (copy if dest missing or source newer)
SYNC_MAP = [
    ("layers/ground/samples/cities-latest.json", ["data/latest/global-cities.json"]),
    ("layers/ground/casey/latest.json", ["data/latest/casey-hourly.json"]),
    ("layers/marine/ndbc/realtime-latest.json", ["data/latest/ndbc-realtime.json"]),
    ("layers/research/summary-latest.json", ["data/latest/research-summary.json"]),
    ("layers/analytics/anomalies-latest.json", ["data/latest/anomaly-report.json"]),
    ("layers/analytics/baseline-latest.json", ["data/latest/rolling-baseline.json"]),
    ("layers/satellite/radiance-index-latest.json", ["data/latest/satellite-radiance-index.json"]),
]


def load(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def mtime(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except Exception:
        return 0.0


def copy_file(src: Path, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return {"copied": str(src.relative_to(ROOT)), "to": str(dest.relative_to(ROOT))}


def rebuild_science_package() -> dict | None:
    """If science-package missing, build a minimal one from available latest files."""
    dest = ROOT / "data/latest/science-package.json"
    summary = load(ROOT / "data/latest/research-summary.json") or load(
        ROOT / "layers/research/summary-latest.json"
    )
    cities = load(ROOT / "data/latest/global-cities.json") or load(
        ROOT / "layers/ground/samples/cities-latest.json"
    )
    ndbc = load(ROOT / "data/latest/ndbc-realtime.json")
    casey = load(ROOT / "data/latest/casey-hourly.json")
    climate = load(ROOT / "data/latest/daily-climate.json")
    if not summary and not cities and not casey:
        return None
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ndbc_obs = (ndbc or {}).get("observations") or {}
    pkg = {
        "schema": "uogw.science_package.v1",
        "date_utc": (summary or {}).get("date_utc") or date,
        "generated_at_utc": now,
        "curator": "Midwest Stratospheric Data Systems",
        "rebuilt_by": "scripts/heal_latest.py",
        "summary": summary or {"note": "summary missing; partial rebuild"},
        "daily_climate_research_cities": (climate or {}).get("cities") or [],
        "global_city_observations": (cities or {}).get("cities") or [],
        "ndbc_latest_observations": {
            sid: (block.get("latest_observation") or {}) for sid, block in ndbc_obs.items()
        },
        "casey_site": (casey or {}).get("site"),
        "casey_daily": (casey or {}).get("daily"),
        "casey_observation_count": (casey or {}).get("observation_count")
        or len((casey or {}).get("observations") or []),
        "attribution": {
            "open_meteo": "CC BY 4.0 — https://open-meteo.com/",
            "ndbc": "NOAA NDBC",
            "msds": "Midwest Stratospheric Data Systems",
        },
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(pkg, indent=2))
    # also date entry
    entry = ROOT / f"data/entries/{date}/science-package.json"
    entry.parent.mkdir(parents=True, exist_ok=True)
    entry.write_text(json.dumps(pkg, indent=2))
    return {"rebuilt": "data/latest/science-package.json"}


def snapshot_latest_for_rollback() -> str | None:
    """Copy current data/latest into snapshots/rollback-point for emergency restore."""
    latest = ROOT / "data/latest"
    if not latest.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    dest = ROOT / "snapshots" / "rollback-points" / stamp
    dest.mkdir(parents=True, exist_ok=True)
    for p in latest.glob("*"):
        if p.is_file():
            shutil.copy2(p, dest / p.name)
    meta = {
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": sorted([p.name for p in dest.glob("*")]),
    }
    (dest / "_rollback_meta.json").write_text(json.dumps(meta, indent=2))
    # keep pointer to last rollback point
    pointer = ROOT / "snapshots" / "rollback-points" / "LATEST"
    pointer.write_text(stamp + "\n")
    return stamp


def main():
    os.chdir(ROOT)
    actions = []
    # pre-heal snapshot (best-effort)
    try:
        stamp = snapshot_latest_for_rollback()
        if stamp:
            actions.append({"rollback_point": stamp})
    except Exception as e:
        actions.append({"snapshot_error": str(e)[:200]})

    for src_rel, dests in SYNC_MAP:
        src = ROOT / src_rel
        if not src.exists():
            continue
        for dest_rel in dests:
            dest = ROOT / dest_rel
            if (not dest.exists()) or (mtime(src) > mtime(dest) + 1):
                actions.append(copy_file(src, dest))

    # research summary dual path
    rs = ROOT / "data/latest/research-summary.json"
    if not rs.exists():
        rebuilt = rebuild_science_package()
        # try layers again
        layer = ROOT / "layers/research/summary-latest.json"
        if layer.exists():
            actions.append(copy_file(layer, rs))

    if not (ROOT / "data/latest/science-package.json").exists():
        r = rebuild_science_package()
        if r:
            actions.append(r)

    report = {
        "schema": "uogw.heal_actions.v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actions": actions,
    }
    out = ROOT / "status" / "heal.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
