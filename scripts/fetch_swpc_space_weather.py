#!/usr/bin/env python3
"""NOAA SWPC space weather -> layers/space-weather/ (public domain, US Government)."""
from __future__ import annotations
import sys
from _uogw_fetch import ROOT, get, get_json, now_utc, write_csv, write_json

B = "https://services.swpc.noaa.gov"
L = ROOT / "layers" / "space-weather"


def main() -> int:
    t = now_utc(); day = t.strftime("%Y-%m-%d"); stamp = t.strftime("%Y-%m-%dT%H:%M:%SZ")
    fails = []
    jobs = {}
    # Kp (3-hourly planetary index, last ~7 days)
    def kp():
        rows = get_json(f"{B}/products/noaa-planetary-k-index.json")
        if rows and isinstance(rows[0], list):
            hdr = rows[0]; rows = [dict(zip(hdr, r)) for r in rows[1:]]
        return rows
    jobs["kp-index"] = kp
    def wind():
        p = get_json(f"{B}/json/rtsw/rtsw_wind_1m.json"); m = get_json(f"{B}/json/rtsw/rtsw_mag_1m.json")
        mag = {r["time_tag"]: r for r in m if r.get("active")}
        out = []
        for r in p:
            if not r.get("active"):
                continue
            g = mag.get(r["time_tag"], {})
            out.append({"time_tag": r["time_tag"], "source": r.get("source"), "proton_speed_km_s": r.get("proton_speed"),
                        "proton_density_cm3": r.get("proton_density"), "proton_temperature_K": r.get("proton_temperature"),
                        "bt_nT": g.get("bt"), "bz_gsm_nT": g.get("bz_gsm"), "by_gsm_nT": g.get("by_gsm")})
        return sorted(out, key=lambda r: r["time_tag"])
    jobs["solar-wind"] = wind
    def xray():
        rows = get_json(f"{B}/json/goes/primary/xrays-1-day.json")
        return [{"time_tag": r.get("time_tag"), "satellite": r.get("satellite"), "energy": r.get("energy"),
                 "flux_W_m2": r.get("flux")} for r in rows]
    jobs["xray-flux"] = xray
    def f107():
        rows = get_json(f"{B}/json/f107_cm_flux.json")
        return sorted([{"time_tag": r.get("time_tag"), "flux_sfu": r.get("flux"), "frequency_MHz": r.get("frequency"),
                        "reporting_schedule": r.get("reporting_schedule")} for r in rows], key=lambda r: r["time_tag"] or "")
    jobs["f107-solar-flux"] = f107
    for name, fn in jobs.items():
        try:
            rows = fn()
            n = write_csv(L / name / f"{day}.csv", rows)
            write_csv(L / name / "latest.csv", rows)
            print(f"{name}: {n} rows")
        except Exception as e:  # keep other sources going
            fails.append(f"{name}: {e}")
    # Geomagnetic / aurora summary: NOAA scales (R/S/G) + 3-day forecast text
    try:
        scales = get_json(f"{B}/products/noaa-scales.json")
        fc = get(f"{B}/text/3-day-forecast.txt").decode("utf-8", "replace")
        g = L / "geomagnetic-summary"
        write_json(g / f"{day}.json", {"retrieved_utc": stamp, "source": f"{B}/products/noaa-scales.json", "noaa_scales": scales})
        write_json(g / "latest.json", {"retrieved_utc": stamp, "noaa_scales": scales})
        (g / f"3-day-forecast-{day}.txt").write_text(fc)
        print("geomagnetic-summary: ok")
    except Exception as e:
        fails.append(f"geomagnetic-summary: {e}")
    for f in fails:
        print("FAIL", f, file=sys.stderr)
    return 1 if len(fails) == len(jobs) + 1 else 0


if __name__ == "__main__":
    sys.exit(main())
