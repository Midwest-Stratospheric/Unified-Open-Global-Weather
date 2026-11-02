"""Shared helpers for UOGW open-source fetchers (stdlib only)."""
from __future__ import annotations
import csv, io, json, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "UOGW-OpenSources/1.0 (midwestsds.com; Aerostratospheric)"
SITES = {"casey": (39.299, -87.992, "Casey, IL"), "birds": (38.840, -87.667, "Birds, IL")}


def get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/geo+json, application/json, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url: str):
    return json.loads(get(url).decode("utf-8"))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def unzip_first(data: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return z.read(z.namelist()[0]).decode("utf-8", "replace")
