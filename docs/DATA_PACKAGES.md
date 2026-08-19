# UOGW Data Packages

Overview of the **daily science and layer packages** produced by Unified Open Global Weather automations. All content is open / redistributable with upstream attribution.

## Primary machine-readable packages (`data/latest/`)

| File | Role |
|------|------|
| `science-package.json` | Combined daily observations + summary |
| `science-analytics.json` | Extremes, coverage, research flags |
| `anomaly-report.json` | Multi-method anomaly screening (research only) |
| `hub-endpoints.json` | Map of stable endpoints for the Data Hub |

## Layer packages (`layers/`)

| Layer | Examples |
|-------|----------|
| **Ground** | Casey IL daily, global city samples, GHCN index |
| **Marine** | NDBC station indexes + samples |
| **Upper-air** | IGRA station list + year indexes |
| **Stratospheric / space** | Catalog links + space-weather snapshots |
| **Satellite / model** | Open catalog + research field snapshots |
| **Flight** | Pointers to MSDS / X2Griffon products (`msds-data`) |

## Status & health

| Path | Role |
|------|------|
| `status/last_update.json` | Last successful update markers |
| Health-monitor workflow | Alerts / self-heal of latest pointers |

## Reports & visuals

| Path | Role |
|------|------|
| `reports/weekly/` | Weekly status reports (Actions) |
| `visuals/latest/` | °F chart PNGs + markdown gallery |

## Related GIR package

Hazard / geospatial open-tier briefing products (NWS, USGS, EONET, CISA KEV, etc.) live in the sibling repository:

**[aerostratospheric-defense-gir](https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir)** — daily executive summaries under `reports/`.

## How to consume

- Start with `data/latest/science-package.json` and `hub-endpoints.json`.
- Clone or use raw.githubusercontent.com paths for individual files.
- Always cite upstream providers listed in `catalog/` and docs.

## What is excluded

Proprietary bulk archives, restricted or non-redistributable products, and classified material.
