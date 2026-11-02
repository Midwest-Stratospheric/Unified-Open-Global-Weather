#!/usr/bin/env python3
"""NOAA/NWS ASOS observations near Casey, IL -> layers/ground/regional/nws/ (public domain)."""
from __future__ import annotations
import sys
from _uogw_fetch import ROOT, get_json, now_utc, write_csv

STATIONS = {"KMTO": "Mattoon/Charleston, IL", "KLWV": "Lawrenceville, IL", "KHUF": "Terre Haute, IN"}
L = ROOT / "layers" / "ground" / "regional" / "nws"
FIELDS = [("temperature", "temperature_C"), ("dewpoint", "dewpoint_C"), ("relativeHumidity", "relative_humidity_pct"),
          ("windDirection", "wind_direction_deg"), ("windSpeed", "wind_speed_km_h"), ("windGust", "wind_gust_km_h"),
          ("barometricPressure", "pressure_Pa"), ("seaLevelPressure", "sea_level_pressure_Pa"),
          ("visibility", "visibility_m"), ("precipitationLastHour", "precip_last_hour_mm")]


def main() -> int:
    day = now_utc().strftime("%Y-%m-%d"); ok = 0
    for sid, name in STATIONS.items():
        try:
            d = get_json(f"https://api.weather.gov/stations/{sid}/observations?limit=100")
            rows = []
            for f in d.get("features", []):
                p = f["properties"]
                r = {"station": sid, "timestamp_utc": p.get("timestamp"), "text": p.get("textDescription")}
                for k, col in FIELDS:
                    r[col] = (p.get(k) or {}).get("value")
                rows.append(r)
            rows.sort(key=lambda r: r["timestamp_utc"] or "")
            write_csv(L / sid / f"{day}.csv", rows); write_csv(L / sid / "latest.csv", rows)
            print(f"{sid}: {len(rows)} obs"); ok += 1
        except Exception as e:
            print(f"FAIL {sid}: {e}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
