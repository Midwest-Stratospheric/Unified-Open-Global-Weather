#!/usr/bin/env python3
"""UV index forecast (NOAA CPC / EPA, ZIP-level) + modeled surface ozone (Open-Meteo / CAMS) for Casey, IL -> layers/atmosphere/."""
from __future__ import annotations
import sys
from datetime import datetime
from _uogw_fetch import ROOT, SITES, get_json, now_utc, write_csv

L = ROOT / "layers" / "atmosphere"


def main() -> int:
    day = now_utc().strftime("%Y-%m-%d"); ok = 0
    try:
        rows = get_json("https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/ZIP/62420/JSON")
        out = [{"local_time": datetime.strptime(r["DATE_TIME"], "%b/%d/%Y %I %p").strftime("%Y-%m-%dT%H:00"),
                "city": r.get("CITY"), "state": r.get("STATE"), "uv_index": r.get("UV_VALUE")} for r in rows]
        out.sort(key=lambda r: r["local_time"])
        write_csv(L / "uv-index" / "casey" / f"{day}.csv", out); write_csv(L / "uv-index" / "casey" / "latest.csv", out)
        print(f"uv-index: {len(out)} hours"); ok += 1
    except Exception as e:
        print(f"FAIL uv-index: {e}", file=sys.stderr)
    for key, (lat, lon, _) in SITES.items():
        try:
            d = get_json(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=ozone,nitrogen_dioxide,pm2_5,uv_index,uv_index_clear_sky&past_days=2&forecast_days=3&timezone=America%2FChicago")
            h = d["hourly"]; u = d["hourly_units"]
            rows = [{(f"{c} ({u[c]})" if c != "time" else "local_time"): h[c][i] for c in h} for i in range(len(h["time"]))]
            write_csv(L / "ozone" / key / f"{day}.csv", rows); write_csv(L / "ozone" / key / "latest.csv", rows)
            print(f"ozone {key}: {len(rows)} hours"); ok += 1
        except Exception as e:
            print(f"FAIL ozone {key}: {e}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
