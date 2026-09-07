# Hugging Face daily mirror (UOGW)

UOGW and GIR publish to **separate** Hugging Face datasets.

| Dataset | URL |
|---------|-----|
| **UOGW** | https://huggingface.co/datasets/aerostratospheric/uogw |
| GIR (sibling) | https://huggingface.co/datasets/aerostratospheric/gir |

## Automation

GitHub Action: [`.github/workflows/huggingface-daily.yml`](../.github/workflows/huggingface-daily.yml)

- Schedule: **11:00 UTC daily** (after the 09:00 research package)
- Manual: Actions → *Daily Hugging Face sync (UOGW)* → Run workflow
- Script: [`scripts/sync_to_huggingface.sh`](../scripts/sync_to_huggingface.sh)

Synced paths: `data/latest/`, `catalog/`, `reports/`, text files under `visuals/`.
PNG charts stay on GitHub (HF git rejects raw binaries without Xet).

## Required secret

Add a repository secret named **`HF_TOKEN`** (Hugging Face write token):

https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/settings/secrets/actions

Do not commit the token.
