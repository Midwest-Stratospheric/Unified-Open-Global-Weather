# API and Status

## Public catalog (MSDS site)

| Resource | URL |
|----------|-----|
| Catalog | https://midwestsds.com/data/v1/catalog.json |
| Data Hub | https://www.midwestsds.com/portal.html |
| API docs | https://www.midwestsds.com/api.html |

## GitHub raw endpoints (this repo)

| Resource | Path |
|----------|------|
| Machine catalog | `catalog/catalog.json` |
| Source registry | `sources/registry.json` |
| Status rollup | `status/last_update.json` |
| Per-source status | `status/*.json` |
| City samples | `layers/ground/samples/cities-latest.json` |
| IGRA latest | `layers/upper-air/igra/*-latest.json` |
| NDBC latest | `layers/marine/ndbc/*-latest.json` |
| GHCN index | `layers/ground/ghcn/stations-index-latest.json` |
| International sources | `layers/ground/international/sources-latest.json` |

Raw base:

`https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/`

## Status rollup fields

`status/last_update.json` typically includes:

- `generated_at_utc`
- `catalog_datasets`
- `layer_json_files`
- `sources` (per-indexer ok / counts / timestamps)
- `repository`, `data_hub`, `curator`
