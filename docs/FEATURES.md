# UOGW Feature Catalog

Current capabilities of the Unified Open Global Weather repository.

## Core data products

| Feature | Path | Notes |
|---------|------|-------|
| Science package | `data/latest/science-package.json` | Combined daily research payload |
| Research summary | `data/latest/research-summary.json` | Index + derived stats |
| Science analytics | `data/latest/science-analytics.json` | Hub highlights, extremes, heat index |
| Global city samples | `data/latest/global-cities.json` | International surface samples |
| Casey hourly | `data/latest/casey-hourly.json` | MSDS local series |
| NDBC realtime | `data/latest/ndbc-realtime.json` | Parsed buoy observations |
| Anomaly report | `data/latest/anomaly-report.json` | Research flags + z-scores |
| Rolling baseline | `data/latest/rolling-baseline.json` | 7-day context |
| Satellite radiance index | `data/latest/satellite-radiance-index.json` | Open product discovery |
| FAIR + citation | `data/latest/fair-metadata.json` | Daily metadata bundle |
| Hub endpoints | `data/latest/hub-endpoints.json` | Single map for Data Hub UI |

## Visuals

| Feature | Path |
|---------|------|
| Chart gallery + anomaly guide | `visuals/latest/CHARTS.md` |
| PNG charts (°F) | `visuals/latest/*.png` |
| README embeds | root `README.md` |

## Analytics & science

- Absolute threshold anomaly screens  
- Multi-method z-scores (population, sample, MAD)  
- Heat-index research flags (°F)  
- Hottest/coldest sample cities  
- Coverage + surface/marine summary stats (°C and °F)  

## Operations

- Health Monitor (self-heal, re-dispatch, alert PR)  
- Rollback workflow + `docs/ROLLBACK.md`  
- Charts auto-run after data workflows  
- Science analytics auto-run after research/anomaly/charts  

## Data Hub

https://midwestsds.com/msds-data-hub.html — loads charts + science analytics + anomaly guide.
