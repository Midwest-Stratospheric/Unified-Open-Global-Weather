#!/usr/bin/env python3
"""Download the UOGW trainer from Hugging Face, patch fragile stratified splits, and run the daily retrain."""
from __future__ import annotations

import os
import re
import runpy
import urllib.request
from pathlib import Path

REPO = os.environ.get("HF_REPO", "aerostratospheric/uogw-scientific-suite")
TOKEN = os.environ.get("HF_TOKEN", "")
URL = f"https://huggingface.co/{REPO}/resolve/main/train_hf_models.py"


def patch_trainer(src: str) -> str:
    """Make stratified train_test_split safe when a class has <2 samples."""
    # Anomaly severity head
    src = re.sub(
        r"strat = y if len\(set\(y\)\) > 1 else None\n\s*Xtr, Xte, ytr, yte = train_test_split\(X, y, test_size=0\.25, random_state=rng, stratify=strat\)",
        "counts = Counter(y)\n    strat = y if len(set(y)) > 1 and min(counts.values()) >= 2 else None\n    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=rng, stratify=strat)",
        src,
        count=1,
    )
    # Thermal comfort head (second stratified split)
    src = re.sub(
        r"Xtr, Xte, ytr, yte = train_test_split\(AX, ay, test_size=0\.2, random_state=rng, stratify=ay\)",
        "counts = Counter(ay)\n    strat = ay if len(set(ay)) > 1 and min(counts.values()) >= 2 else None\n    Xtr, Xte, ytr, yte = train_test_split(AX, ay, test_size=0.2, random_state=rng, stratify=strat)",
        src,
        count=1,
    )
    return src


def main() -> int:
    dest = Path("/tmp/train_hf_models.py")
    req = urllib.request.Request(URL)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
    patched = patch_trainer(raw)
    dest.write_text(patched, encoding="utf-8")
    print("downloaded + patched trainer", dest, "from", URL)
    # Also push the fixed trainer back to HF so future runs get the permanent fix
    if TOKEN:
        try:
            from huggingface_hub import HfApi
            api = HfApi(token=TOKEN)
            api.upload_file(
                path_or_fileobj=str(dest),
                path_in_repo="train_hf_models.py",
                repo_id=REPO,
                repo_type="model",
                commit_message="fix: harden stratified splits (min class count >= 2)",
            )
            print("uploaded fixed trainer to", REPO)
        except Exception as e:
            print("note: could not upload fixed trainer:", e)
    runpy.run_path(str(dest), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
