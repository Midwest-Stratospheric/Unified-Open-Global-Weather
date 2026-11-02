#!/usr/bin/env python3
"""NOAA NCEI IGRA v2.2 radiosonde soundings, Lincoln IL (ILX, USM00074560) -> layers/upper-air/ilx-soundings/ (public domain)."""
from __future__ import annotations
import sys
from _uogw_fetch import ROOT, get, unzip_first, write_csv, write_json, now_utc

STATION = "USM00074560"
URL = f"https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-y2d/{STATION}-data-beg2026.txt.zip"
L = ROOT / "layers" / "upper-air" / "ilx-soundings"
KEEP = 28  # most recent soundings kept as CSV (about two weeks at 00Z/12Z)


def num(s, scale=1.0, missing=(-9999, -8888)):
    try:
        v = int(s)
    except ValueError:
        return None
    return None if v in missing else round(v / scale, 2)


def main() -> int:
    txt = unzip_first(get(URL, timeout=120))
    sounds, cur = [], None
    for line in txt.splitlines():
        if line.startswith("#"):
            cur = {"id": line[1:12], "time": f"{line[13:17]}-{line[18:20]}-{line[21:23]}T{line[24:26]}:00Z", "levels": []}
            sounds.append(cur)
        elif cur is not None and len(line) >= 51:
            cur["levels"].append({
                "level_type": line[0:2].strip(), "pressure_hPa": num(line[9:15], 100),
                "geopotential_height_m": num(line[16:21]), "temperature_C": num(line[22:27], 10),
                "relative_humidity_pct": num(line[28:33], 10), "dewpoint_depression_C": num(line[34:39], 10),
                "wind_direction_deg": num(line[40:45]), "wind_speed_m_s": num(line[46:51], 10)})
    recent = sounds[-KEEP:]
    rows = [{"sounding_time_utc": s["time"], **lv} for s in recent for lv in s["levels"]]
    write_csv(L / "recent-soundings.csv", rows)
    write_json(L / "index.json", {"station": STATION, "name": "Lincoln, IL (NWS ILX)", "retrieved_utc": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                  "source": URL, "soundings_in_file": len(sounds), "soundings_kept": [s["time"] for s in recent]})
    print(f"ILX: {len(sounds)} soundings in archive, kept {len(recent)} ({len(rows)} levels)")
    return 0 if recent else 1


if __name__ == "__main__":
    sys.exit(main())
