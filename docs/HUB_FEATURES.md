# MSDS Data Hub features (mirror of midwestsds.com/msds-data-hub.html)

Public hub: https://midwestsds.com/msds-data-hub.html  
Main repository: https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

## Core UOGW products

| Hub section | Product / path | Script / workflow |
|-------------|----------------|-------------------|
| Unified Open Global Weather | `catalog/catalog.json`, `data/latest/*` | daily pipelines |
| Live chart gallery | `visuals/latest/*.png` | `scripts/generate_charts.py`, `charts-daily.yml` |
| Anomaly research alert | `data/latest/anomaly-report.json` | anomaly pipeline |
| Science analytics | `data/latest/science-analytics.json` | `science-analytics-daily.yml` |
| Pre-tornado Clark County | `data/latest/pre-tornado-clark.json` | `scripts/pre_tornado_clark.py` |
| Illinois radiosonde count | `data/latest/illinois-radiosonde-count.json` | `scripts/illinois_radiosonde_count.py` |
| Ozone health snapshot | `data/latest/ozone-health.json` | `scripts/ozone_health_snapshot.py` |
| Space weather + GFS | `data/latest/space-gfs-snapshot.json` | `scripts/space_gfs_snapshot.py` |
| Hub visual snapshots | `data/latest/hub-visual-snapshots.json` | `scripts/hub_visual_snapshots.py` |
| Casey ground | msds-data + UOGW casey-hourly | ground daily |
| NDBC marine | `data/latest/ndbc-realtime.json` | marine daily |

## Interactive hub-only tools (client-side)

These run in the browser against public APIs; results are not written back to GitHub unless noted.

| Tool | Behavior |
|------|----------|
| ZIP pre-tornado score | Zippopotam geocode + Open-Meteo scoring |
| Address conditions report | Extracts **city + state** from free-form address → Open-Meteo report (printable) |
| Live Kp / X-ray / GFS canvases | NOAA SWPC + Open-Meteo when PNG charts missing |
| GLOBE feed panel | NASA GLOBE observation queries |

## Source folders

- [data/latest](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/tree/main/data/latest)
- [visuals/latest](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/tree/main/visuals/latest)
- [scripts](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/tree/main/scripts)
- [workflows](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/tree/main/.github/workflows)
- [docs](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/tree/main/docs)

## Related repositories

- [msds-data](https://github.com/Midwest-Stratospheric/msds-data) — Casey ground / MSDS flight products
- [International-Ground-Data-Repository](https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository) — IGDR upper-air index

## Data vs live telemetry

See [DATA_VS_TELEMETRY.md](./DATA_VS_TELEMETRY.md).
