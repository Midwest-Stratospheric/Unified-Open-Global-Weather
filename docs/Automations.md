# Automations

All schedules run on **GitHub Actions** inside this repository. They do not depend on midwestsds.com being online.

| Workflow | Schedule (UTC) | Output |
|----------|----------------|--------|
| `msds-ground-daily.yml` | Daily | Casey ground → msds-data + `layers/ground/casey/` |
| `igra-index-daily.yml` | Daily | IGRA station + Y2D index → `layers/upper-air/igra/` |
| `ndbc-marine-daily.yml` | Daily | NDBC stations → `layers/marine/ndbc/` |
| `global-samples-daily.yml` | ~05:00 | Worldwide city samples → `layers/ground/samples/` |
| `international-indexes-daily.yml` | ~05:30 | GHCN + foreign registry → `layers/ground/ghcn/` + `international/` |
| `catalog-rebuild.yml` | ~08:00 + on data pushes | `status/last_update.json` |

## Secrets

| Secret | Purpose |
|--------|---------|
| `MSDS_DATA_TOKEN` | Optional PAT with write access to `msds-data` for cross-repo ground commits |

## Concurrency

Workflows use concurrency groups and rebase/retry on push to avoid race failures when multiple indexers commit close together.

## Manual runs

Repository → **Actions** → select workflow → **Run workflow**.

https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/actions
