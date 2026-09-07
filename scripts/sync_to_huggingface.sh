#!/usr/bin/env bash
# Mirror UOGW JSON/Markdown packages to Hugging Face (separate from GIR).
set -euo pipefail

HF_TOKEN="${HF_TOKEN:-}"
HF_REPO="${HF_REPO:-aerostratospheric/uogw}"
HF_USER="${HF_USER:-aerostratospheric}"

if [[ -z "${HF_TOKEN}" ]]; then
  echo "HF_TOKEN is not set. Add it as a GitHub Actions secret named HF_TOKEN."
  exit 1
fi

WORKDIR="$(pwd)"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

clone_url="https://${HF_USER}:${HF_TOKEN}@huggingface.co/datasets/${HF_REPO}"
git clone --depth 1 "${clone_url}" "${TMP}/hf"
cd "${TMP}/hf"

copy_tree() {
  local src="$1" dest="$2"
  if [[ -d "${WORKDIR}/${src}" ]]; then
    rm -rf "${dest}"
    mkdir -p "${dest}"
    # Text / JSON packages only — HF git rejects raw PNG/binaries without Xet/LFS.
    find "${WORKDIR}/${src}" -type f \
      ! -iname '*.png' ! -iname '*.jpg' ! -iname '*.jpeg' ! -iname '*.gif' \
      ! -iname '*.webp' ! -iname '*.zip' ! -iname '*.gz' ! -iname '*.bin' \
      -print0 | while IFS= read -r -d '' f; do
        rel="${f#${WORKDIR}/${src}/}"
        mkdir -p "${dest}/$(dirname "${rel}")"
        cp -a "$f" "${dest}/${rel}"
      done
  fi
}

copy_tree data/latest data/latest
copy_tree catalog catalog
copy_tree reports reports
copy_tree visuals visuals

mkdir -p data
cat > sync-status.json << JSON
{
  "source": "https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather",
  "hf_repo": "https://huggingface.co/datasets/${HF_REPO}",
  "synced_utc": "${STAMP}",
  "github_commit": "${COMMIT}"
}
JSON

git config user.name "UOGW HF mirror"
git config user.email "launchcontrol@midwestsds.com"
git add -A
if git diff --staged --quiet; then
  echo "No Hugging Face changes for UOGW."
  exit 0
fi
git commit -m "data(uogw): daily sync ${STAMP}"
git push origin HEAD:main
echo "Pushed UOGW snapshot to https://huggingface.co/datasets/${HF_REPO}"
