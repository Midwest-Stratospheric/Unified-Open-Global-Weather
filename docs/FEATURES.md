# UOGW feature catalog

See the full hub ↔ GitHub map in [HUB_FEATURES.md](./HUB_FEATURES.md) and package map in [DATA_PACKAGES.md](./DATA_PACKAGES.md).

## Layers

1. **Ground** — surface stations, Casey daily, GLOBE, global city samples, GHCN index
2. **Marine** — NDBC samples and indexes
3. **Upper-air** — IGRA index, Illinois radiosonde counts
4. **Stratospheric / space** — SWPC Kp, GOES X-rays (via space-gfs snapshot), catalog links
5. **Satellite / model** — GFS seamless fields for research charts, open catalog pointers
6. **Flight** — MSDS X2Griffon products (`msds-data`)

## Research modules

- Multi-method anomaly detection (threshold + z-score / MAD family)
- Pre-tornado condition score (Clark County IL)
- Ozone health snapshot
- Science analytics digest (`science-analytics.json`)
- Daily science package (`science-package.json`)
- Self-healing latest pointers (`heal_latest.py`)
- Health-monitor PR automation
- **Weekly status report** (`scripts/weekly_report.py` → `reports/weekly/`)
- FAIR metadata daily refresh
- Rolling baseline daily

## Automations

All under `.github/workflows/` — schedule + `workflow_dispatch`.

- Daily data + analytics pipelines (ground, marine, IGRA, global samples, charts, anomaly, science analytics, …)
- **Weekly Status Report** — Mondays 10:00 UTC (`weekly-report.yml`)
- Health monitor, rollback, auto-rerun-failures
- Catalog rebuild, component snapshots, satellite radiance, space-GFS, pre-tornado Clark, ozone visuals

## Repository hygiene

- `CONTRIBUTING.md` — how to propose open/redistributable improvements
- `SECURITY.md` — vulnerability reporting
- `docs/DATA_PACKAGES.md` — consumer-facing package map
- Catalog + source registry under `catalog/` and `sources/`

## Sibling geospatial package

Open hazard / defense-adjacent geospatial briefing products:
[aerostratospheric-defense-gir](https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir)
