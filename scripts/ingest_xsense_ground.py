#!/usr/bin/env python3
"""Ingest X-Sense thermo-hygrometer email-export CSVs into UOGW ground layer.

Expected raw path:
  layers/ground/casey/xsense/raw/YYYY-MM-DD.csv

CSV columns (X-Sense export):
  Time,Temperature_Fahrenheit,Relative Humidity_Percent
  2026/09/13 23:59,75.2,49.7

Times are treated as America/Chicago local (Casey ground station).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "layers" / "ground" / "casey" / "xsense" / "raw"
OUT_DIR = ROOT / "layers" / "ground" / "casey" / "xsense"
ENTRIES = ROOT / "data" / "entries"
LATEST = ROOT / "data" / "latest"
STATUS = ROOT / "status"

SITE = {
    "name": "Casey, Illinois \u2014 MSDS ground station",
    "latitude": 39.2992,
    "longitude": -87.9925,
    "elevation_m": 200,
    "timezone": "America/Chicago",
    "instrument": "X-Sense thermo-hygrometer",
}
TZ = ZoneInfo("America/Chicago")
DATE_RE = re.compile(r"(20\d{2})[-_/]?(\d{2})[-_/]?(\d{2})")


def f_to_c(f: float) -> float:
    return round((f - 32.0) * 5.0 / 9.0, 2)


def parse_stamp(raw: str):
    raw = (raw or "").strip()
    for fmt in (
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
    ):
        try:
            return datetime.strptime(raw[:19], fmt).replace(tzinfo=TZ)
        except ValueError:
            continue
    return None


def date_from_name(path: Path):
    m = DATE_RE.search(path.stem.replace(" ", ""))
    if not m:
        m = DATE_RE.search(path.name)
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def load_rows(path: Path):
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(text.splitlines(), dialect=dialect)
    rows = []
    for rec in reader:
        norm = {re.sub(r"[^a-z0-9]+", "_", (k or "").strip().lower()).strip("_"): v for k, v in rec.items()}
        tkey = next((k for k in ("time", "timestamp", "datetime", "date_time") if k in norm), None)
        fkey = next((k for k in norm if "temp" in k and ("f" in k or "fahr" in k)), None)
        ckey = next((k for k in norm if "temp" in k and ("c" in k or "cels" in k)), None)
        hkey = next((k for k in norm if "humid" in k or k.endswith("_percent") or k == "rh"), None)
        if not tkey:
            continue
        ts = parse_stamp(str(norm.get(tkey) or ""))
        if ts is None:
            continue
        temp_f = None
        temp_c = None
        try:
            if fkey and str(norm.get(fkey) or "").strip() not in ("", "None", "nan"):
                temp_f = float(str(norm[fkey]).strip())
                temp_c = f_to_c(temp_f)
            elif ckey and str(norm.get(ckey) or "").strip() not in ("", "None", "nan"):
                temp_c = float(str(norm[ckey]).strip())
                temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 2)
        except ValueError:
            pass
        rh = None
        try:
            if hkey and str(norm.get(hkey) or "").strip() not in ("", "None", "nan"):
                rh = float(str(norm[hkey]).strip())
        except ValueError:
            pass
        if temp_f is None and rh is None:
            continue
        rows.append(
            {
                "time_local": ts.strftime("%Y-%m-%dT%H:%M:%S"),
                "time": ts.isoformat(),
                "date": ts.date().isoformat(),
                "hour": ts.strftime("%Y-%m-%dT%H:00:00"),
                "temperature_f": temp_f,
                "temperature_c": temp_c,
                "relative_humidity_pct": rh,
            }
        )
    rows.sort(key=lambda r: r["time"])
    return rows


def hourly_rollup(rows):
    buckets = defaultdict(list)
    for r in rows:
        buckets[r["hour"]].append(r)
    out = []
    for hour in sorted(buckets):
        chunk = buckets[hour]
        tf = [x["temperature_f"] for x in chunk if x["temperature_f"] is not None]
        tc = [x["temperature_c"] for x in chunk if x["temperature_c"] is not None]
        rh = [x["relative_humidity_pct"] for x in chunk if x["relative_humidity_pct"] is not None]
        out.append(
            {
                "time": hour,
                "sample_count": len(chunk),
                "temperature_f": round(mean(tf), 2) if tf else None,
                "temperature_c": round(mean(tc), 2) if tc else None,
                "temperature_f_min": round(min(tf), 2) if tf else None,
                "temperature_f_max": round(max(tf), 2) if tf else None,
                "relative_humidity_pct": round(mean(rh), 1) if rh else None,
                "relative_humidity_pct_min": round(min(rh), 1) if rh else None,
                "relative_humidity_pct_max": round(max(rh), 1) if rh else None,
            }
        )
    return out


def stats(rows):
    tf = [x["temperature_f"] for x in rows if x["temperature_f"] is not None]
    tc = [x["temperature_c"] for x in rows if x["temperature_c"] is not None]
    rh = [x["relative_humidity_pct"] for x in rows if x["relative_humidity_pct"] is not None]
    return {
        "temperature_c_min": round(min(tc), 2) if tc else None,
        "temperature_c_max": round(max(tc), 2) if tc else None,
        "temperature_c_mean": round(mean(tc), 2) if tc else None,
        "temperature_f_min": round(min(tf), 2) if tf else None,
        "temperature_f_max": round(max(tf), 2) if tf else None,
        "temperature_f_mean": round(mean(tf), 2) if tf else None,
        "relative_humidity_pct_min": round(min(rh), 1) if rh else None,
        "relative_humidity_pct_max": round(max(rh), 1) if rh else None,
        "relative_humidity_pct_mean": round(mean(rh), 1) if rh else None,
    }


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def process_file(path: Path):
    rows = load_rows(path)
    if not rows:
        print(f"no rows: {path}")
        return None
    dates = sorted({r["date"] for r in rows})
    date = date_from_name(path) or dates[-1]
    day_rows = [r for r in rows if r["date"] == date] or rows
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    hourly = hourly_rollup(day_rows)
    payload = {
        "date": date,
        "site": SITE,
        "source": {
            "provider": "X-Sense",
            "kind": "in-situ ground station email export",
            "email_from": "support@x-sense-iot.com",
            "filename": path.name,
            "raw_file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "retrieved_at_utc": now,
            "curator": "Midwest Stratospheric Data Systems",
        },
        "data_kind": "in_situ_observations",
        "native_interval": "1min",
        "product_interval": "hourly",
        "observation_count": len(hourly),
        "native_sample_count": len(day_rows),
        "stats": stats(day_rows),
        "observations": hourly,
        "meta": {"generator": "uogw/ingest_xsense_ground.py", "uogw": True, "native_dates": dates},
    }
    write_json(OUT_DIR / f"{date}.json", payload)
    write_json(OUT_DIR / "latest.json", payload)
    write_json(ENTRIES / date / "casey-xsense.json", payload)
    write_json(LATEST / "casey-xsense.json", payload)
    summary_path = ENTRIES / date / "summary.json"
    summary = {}
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            summary = {}
    summary.setdefault("date", date)
    summary.setdefault("generated_at_utc", now)
    summary.setdefault("entries", {})
    summary["entries"]["casey-xsense"] = {
        "ok": True,
        "observation_count": len(hourly),
        "native_sample_count": len(day_rows),
        "file": f"data/entries/{date}/casey-xsense.json",
        "source": "X-Sense in-situ",
    }
    write_json(summary_path, summary)
    write_json(LATEST / "summary-xsense.json", summary)
    write_json(
        STATUS / "msds-xsense.json",
        {
            "source": "msds-casey-xsense",
            "ok": True,
            "date": date,
            "observation_count": len(hourly),
            "native_sample_count": len(day_rows),
            "data_entry": f"data/entries/{date}/casey-xsense.json",
            "generated_at_utc": now,
        },
    )
    print(f"ingested {path.name}: {len(day_rows)} native samples -> {len(hourly)} hourly obs for {date}")
    return payload


def main(argv):
    if argv:
        targets = [Path(a) for a in argv]
    else:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        targets = sorted(p for p in RAW_DIR.iterdir() if p.suffix.lower() in {".csv", ".txt"})
    if not targets:
        print("no raw X-Sense CSVs found")
        return 0
    n = 0
    for path in targets:
        if process_file(path):
            n += 1
    print(f"processed {n} file(s)")
    return 0 if n else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
