#!/usr/bin/env python3
"""Publish a single hub-endpoints.json map for the MSDS Data Hub."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main"


def main() -> int:
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    bundle = {
        "schema": "uogw.hub_endpoints.v1",
        "date_utc": date,
        "generated_at_utc": now_s,
        "data_hub": "https://midwestsds.com/msds-data-hub.html",
        "repository": "https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather",
        "raw_base": RAW,
        "endpoints": {
            "science_package": f"{RAW}/data/latest/science-package.json",
            "research_summary": f"{RAW}/data/latest/research-summary.json",
            "science_analytics": f"{RAW}/data/latest/science-analytics.json",
            "anomaly_report": f"{RAW}/data/latest/anomaly-report.json",
            "global_cities": f"{RAW}/data/latest/global-cities.json",
            "casey_hourly": f"{RAW}/data/latest/casey-hourly.json",
            "ndbc_realtime": f"{RAW}/data/latest/ndbc-realtime.json",
            "rolling_baseline": f"{RAW}/data/latest/rolling-baseline.json",
            "charts_status": f"{RAW}/status/charts.json",
            "charts_markdown": f"{RAW}/visuals/latest/CHARTS.md",
            "anomaly_methods": f"{RAW}/docs/ANOMALY_METHODS.md",
            "catalog": f"{RAW}/catalog/catalog.json",
        },
        "charts": {
            "base": f"{RAW}/visuals/latest/",
            "files": [
                "global-city-temperatures.png",
                "global-city-temp-map.png",
                "casey-hourly-temperature.png",
                "research-cities-tminmax.png",
                "ndbc-marine-samples.png",
                "anomaly-severity.png",
                "global-city-humidity.png",
                "daily-summary-card.png",
            ],
            "temperature_display_unit": "fahrenheit",
        },
        "anomaly_guide": {
            "alert": "Strong outlier vs thresholds or baseline (research only — not an NWS warning).",
            "watch": "Elevated interest: heat/cold, wind, pressure, or |z| >= 2.5 vs recent baseline.",
            "info": "Notable lower-urgency conditions (e.g. dry-hot, strong high, warm water).",
            "methods_doc": f"{RAW}/docs/ANOMALY_METHODS.md",
        },
    }

    for p in [
        ROOT / f"data/entries/{date}/hub-endpoints.json",
        ROOT / "data/latest/hub-endpoints.json",
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(bundle, indent=2) + "\n")

    status = ROOT / "status" / "hub-endpoints.json"
    status.parent.mkdir(parents=True, exist_ok=True)
    status.write_text(
        json.dumps({"ok": True, "date": date, "generated_at_utc": now_s}, indent=2) + "\n"
    )
    print("hub-endpoints written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
