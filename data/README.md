# UOGW Actual Data

This directory holds **real observation payloads**, not just indexes.

## Layout

```
data/
  entries/YYYY-MM-DD/     # One folder per automation day
    summary.json          # Counts + what was written
    global-cities.json    # Live surface obs for 30+ worldwide cities
    ndbc-realtime.json    # Parsed buoy/met observations
    casey-hourly.json     # Full hourly + daily for Casey, IL
  latest/                 # Pointers to most recent entry files
```

Layer indexes still live under `layers/`.  
**If you want numbers to plot or analyze, start here in `data/entries/`.**

## Update cadence

Written automatically by GitHub Actions (see `.github/workflows/`).  
Each successful run commits at least one new or updated entry for that UTC date.
