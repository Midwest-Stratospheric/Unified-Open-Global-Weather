#!/usr/bin/env python3
"""Open-Meteo historical archive (ERA5-based) for Casey and Birds, IL -> layers/ground/regional/open-meteo/ (CC BY 4.0)."""
from __future__ import annotations
import sys
from datetime import timedelta
from _uogw_fetch import ROOT, SITES, get_json, now_utc, write_csv

L = ROOT / "layers" / "ground" / "regional" / "open-meteo"
DAILY = "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration"


def main() -> int:
    t = now_utc().date(); end = t - timedelta(days=6); start = end - timedelta(days=59); ok = 0
    for key, (lat, lon, name) in SITES.items():
        try:
            d = get_json(f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily={DAILY}&timezone=America%2FChicago")
            dd = d["daily"]; units = d["daily_units"]; cols = list(dd.keys())
            rows = [{f"{c} ({units[c]})" if c != "time" else "date": dd[c][i] for c in cols} for i in range(len(dd["time"]))]
            write_csv(L / key / "daily-last-60d.csv", rows)
            print(f"{key}: {len(rows)} days {start}..{end}"); ok += 1
        except Exception as e:
            print(f"FAIL {key}: {e}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
