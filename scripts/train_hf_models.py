#!/usr/bin/env python3
"""Download the UOGW trainer from Hugging Face and run the daily retrain."""
from __future__ import annotations

import os
import runpy
import urllib.request
from pathlib import Path

REPO = os.environ.get("HF_REPO", "aerostratospheric/uogw-scientific-suite")
TOKEN = os.environ.get("HF_TOKEN", "")
URL = f"https://huggingface.co/{REPO}/resolve/main/train_hf_models.py"


def main() -> int:
    dest = Path("/tmp/train_hf_models.py")
    req = urllib.request.Request(URL)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())
    print("downloaded trainer", dest, "from", URL)
    runpy.run_path(str(dest), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
