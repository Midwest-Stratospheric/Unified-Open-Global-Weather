# Hugging Face daily mirror (UOGW)

Published by **[Aerostratospheric](https://www.midwestsds.com/)**.  
Midwest Stratospheric Data Systems operates as a limited partnership under Aerostratospheric.

UOGW and GIR publish to **separate** Hugging Face datasets and model suites under [`aerostratospheric`](https://huggingface.co/aerostratospheric).

| Artifact | URL |
|---------|-----|
| **UOGW dataset** | https://huggingface.co/datasets/aerostratospheric/uogw |
| **UOGW models** | https://huggingface.co/aerostratospheric/uogw-scientific-suite |
| GIR dataset (sibling) | https://huggingface.co/datasets/aerostratospheric/gir |
| GIR models (sibling) | https://huggingface.co/aerostratospheric/gir-open-tier-suite |
| Hub card | https://huggingface.co/aerostratospheric/msds-open-models |

## Aerostratospheric

| Resource | Link |
|----------|------|
| Home | https://www.midwestsds.com/ |
| About | https://midwestsds.com/about.html |
| xDataHub | https://midwestsds.com/msds-data-hub.html |
| Defense GIR | https://midwestsds.com/aerostratospheric-defense-gir.html |
| Contact | https://midwestsds.com/contact/ |
| GitHub | https://github.com/Midwest-Stratospheric |
| Hugging Face | https://huggingface.co/aerostratospheric |

Casey, Illinois · NASA GLOBE **GO-4VW9B** · Ham **KE9CFY** · launchcontrol@midwestsds.com

## Data automation

GitHub Action: [`.github/workflows/huggingface-daily.yml`](../.github/workflows/huggingface-daily.yml)

- Schedule: **11:00 UTC daily** (after the 09:00 research package)
- Manual: Actions → *Daily Hugging Face sync (UOGW)* → Run workflow
- Script: [`scripts/sync_to_huggingface.sh`](../scripts/sync_to_huggingface.sh)

Synced paths: `data/latest/`, `catalog/`, `reports/`, text files under `visuals/`.
PNG charts stay on GitHub (HF git rejects raw binaries without Xet).

## Model automation (daily retrain)

GitHub Action: [`.github/workflows/huggingface-models-daily.yml`](../.github/workflows/huggingface-models-daily.yml)

- Schedule: **12:00 UTC daily**
- Also runs after a successful *Daily Hugging Face sync (UOGW)*
- Manual: Actions → *Daily Hugging Face model retrain (UOGW)* → Run workflow
- Script: [`scripts/train_hf_models.py`](../scripts/train_hf_models.py)
- Also checks out GIR so the anomaly head can use the historical UOGW screens archived there

Pushes a new commit to `aerostratospheric/uogw-scientific-suite` (`metrics.json` records the train time).

## Required secret

Add a repository secret named **`HF_TOKEN`** (Hugging Face write token):

https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/settings/secrets/actions

Do not commit the token.
