#!/usr/bin/env python3
"""Illinois radiosonde activity: 3-day launch count + devices-likely-aloft estimate.

Primary NWS upper-air site in Illinois: Lincoln (ILX / KILX).
Source: Iowa Environmental Mesonet computed RAOB parameters API.
"""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Illinois primary radiosonde site (+ optional near-border context stations)
STATIONS = [
    {
        "id": "KILX",
        "name": "Lincoln, IL (ILX)",
        "state": "IL",
        "role": "primary",
        "wmo": "74560",
        "lat": 40.15,
        "lon": -89.337,
    },
]

# Typical radiosonde flight duration used for "likely aloft" estimate
ALOFT_HOURS = 2.0


def fetch_year(station: str, year: int) -> list:
    url = f"https://mesonet.agron.iastate.edu/api/1/raobs_by_year.json?station={station}&year={year}"
    req = urllib.request.Request(url, headers={"User-Agent": "UOGW-IL-Radiosonde/1.0 (midwestsds.com)"})
    with urllib.request.urlopen(req, timeout=90) as r:
        j = json.loads(r.read().decode())
    return j.get("data") or []


def parse_valid(v: str):
    if not v:
        return None
    try:
        if v.endswith("Z"):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def main() -> int:
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    window_start = now - timedelta(days=3)

    station_reports = []
    all_launches = []
    aloft = []

    years = {now.year}
    if window_start.year != now.year:
        years.add(window_start.year)

    for st in STATIONS:
        rows = []
        for y in sorted(years):
            try:
                rows.extend(fetch_year(st["id"], y))
            except Exception as e:
                station_reports.append({
                    "station": st["id"],
                    "name": st["name"],
                    "ok": False,
                    "error": str(e),
                })
                continue

        launches_3d = []
        for row in rows:
            dt = parse_valid(row.get("valid") or "")
            if not dt:
                continue
            if dt < window_start or dt > now + timedelta(hours=1):
                continue
            entry = {
                "station": st["id"],
                "name": st["name"],
                "valid_utc": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "release_time": row.get("release_time"),
                "sbcape_jkg": row.get("sbcape_jkg"),
                "pwater_mm": row.get("pwater_mm"),
                "shear_sfc_6km_smps": row.get("shear_sfc_6km_smps"),
            }
            launches_3d.append(entry)
            all_launches.append(entry)
            age_h = (now - dt).total_seconds() / 3600.0
            if 0 <= age_h <= ALOFT_HOURS:
                aloft.append({**entry, "estimated_age_hours": round(age_h, 2)})

        launches_3d.sort(key=lambda x: x["valid_utc"])
        station_reports.append({
            "station": st["id"],
            "name": st["name"],
            "state": st["state"],
            "role": st["role"],
            "ok": True,
            "launches_3_days": len(launches_3d),
            "launches": launches_3d,
        })

    all_launches.sort(key=lambda x: x["valid_utc"])

    payload = {
        "schema": "uogw.illinois_radiosonde_count.v1",
        "ok": True,
        "date_utc": date,
        "generated_at_utc": now_s,
        "region": {
            "name": "Illinois",
            "focus": "NWS radiosonde / rawinsonde launches",
            "primary_station": "KILX (Lincoln, IL)",
            "note": (
                "Illinois' operational NWS upper-air site is Lincoln (ILX). "
                "Synoptic launches are typically 00Z and 12Z daily."
            ),
        },
        "window": {
            "hours": 72,
            "start_utc": window_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_utc": now_s,
        },
        "counts": {
            "launches_3_days": len(all_launches),
            "devices_likely_aloft": len(aloft),
            "aloft_window_hours": ALOFT_HOURS,
            "stations_reporting": sum(1 for s in station_reports if s.get("ok")),
        },
        "devices_likely_aloft": aloft,
        "launches_3_days": all_launches,
        "stations": station_reports,
        "source": {
            "name": "Iowa Environmental Mesonet RAOB by year",
            "url": "https://mesonet.agron.iastate.edu/api/1/raobs_by_year.json",
            "attribution": "Iowa State University IEM",
        },
        "disclaimer": (
            "Launch times are synoptic schedule timestamps from public RAOB archives. "
            "'Devices likely aloft' is an estimate (flight within last "
            f"{ALOFT_HOURS:.0f} hours), not radar tracking of each balloon."
        ),
        "curator": "Midwest Stratospheric Data Systems",
        "hub": "https://midwestsds.com/msds-data-hub.html#il-radiosondes",
    }

    for p in [
        Path(f"data/entries/{date}/illinois-radiosonde-count.json"),
        Path("data/latest/illinois-radiosonde-count.json"),
        Path("layers/upper-air/illinois-radiosonde-count-latest.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2) + "\n")

    Path("status").mkdir(parents=True, exist_ok=True)
    Path("status/illinois-radiosonde-count.json").write_text(
        json.dumps(
            {
                "ok": True,
                "generated_at_utc": now_s,
                "launches_3_days": len(all_launches),
                "devices_likely_aloft": len(aloft),
            },
            indent=2,
        )
        + "\n"
    )

    print(
        json.dumps(
            {
                "ok": True,
                "launches_3_days": len(all_launches),
                "devices_likely_aloft": len(aloft),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
