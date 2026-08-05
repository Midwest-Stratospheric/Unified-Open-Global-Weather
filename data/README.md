# UOGW Actual Data (Research-Ready)

This directory is the **science-facing data surface** of Unified Open Global Weather.

Indexes under `layers/` help discovery. **Numbers for analysis live here.**

## Daily layout

```
data/
  entries/YYYY-MM-DD/
    summary.json              # What landed that day (all sources)
    global-cities.json        # Live surface obs — 30+ worldwide cities
    ndbc-realtime.json        # Parsed buoy/met observations
    casey-hourly.json         # Full hourly series for Casey, IL
    igra-index.json           # Upper-air station + Y2D research stats
    daily-climate.json        # Max/min/mean temp, precip, wind, radiation, ET0
    research-summary.json     # Generalized multi-source daily summary
    science-package.json      # Combined research package (summary + obs)
  latest/                     # Always the newest of each product
```

## Updated every day (UTC)

| Workflow | Cron (UTC) | Writes |
|----------|------------|--------|
| MSDS Ground Daily | 01:15 | `casey-hourly.json` |
| Global Samples Daily | 05:00 | `global-cities.json` |
| International Indexes | 05:30 | GHCN + foreign registry |
| IGRA Index Daily | 06:30 | `igra-index.json` |
| NDBC Marine Daily | 07:45 | `ndbc-realtime.json` |
| Catalog Rebuild | 08:00 | status rollup |
| **Daily Research Package** | **09:00** | **research-summary + science-package + daily-climate** |

All workflows also support **manual Run workflow** from the Actions tab.

## Why this helps research

- Multi-layer: ground + marine + upper-air indexes + local HAB support site
- International city samples, not US-only
- Derived daily stats (means/mins/maxes) for quick comparison
- Stable paths under `data/latest/` for scripts and notebooks
- Full attribution chains to NOAA, Open-Meteo, and MSDS

## Quick start for analysis

```text
https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/science-package.json
https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/research-summary.json
https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/global-cities.json
https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/ndbc-realtime.json
https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/casey-hourly.json
```

Curator: Midwest Stratospheric Data Systems · https://www.midwestsds.com
