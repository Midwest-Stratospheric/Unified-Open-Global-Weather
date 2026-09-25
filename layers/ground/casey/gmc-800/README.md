# Casey GMC-800 — fixed ground radiation station

First-party **surface ionizing-radiation** observations from a GQ Electronics **GMC-800** at Casey, Illinois.

## Ingest policy (always)

Every GMC-800 export is committed comprehensively:

1. Full **hourly** series for the whole window (`hourly_START_END.csv`) — every hour, min/mean/max/median CPM and µSv/h
2. **Daily** rollup + window stats in `latest.json` and a dated pointer
3. **Minute** CSVs under `minutes/YYYY-MM-DD.csv` when the export is attached
4. IGDR snapshot for the ingest date

Do not replace a comprehensive commit with a short latest-only window.

## Location

`MSDS-GMC800-CASEY` · 39.2974 N, 87.9818 W · America/Chicago · fixed · GQ GMC-800 · `cpm`, `usv_h`

## Current files

| File | Role |
|------|------|
| `station.json` | Site metadata |
| `latest.json` | Window stats + daily rollup |
| `hourly_2026-09-16_2026-09-25.csv` | All 214 hours |
| `minutes/YYYY-MM-DD.csv` | Native 1-minute rows |
| `2026-09-16.json` / `2026-09-25.json` | Dated pointers |

## Windows

- First: 2026-09-15 12:40 – 2026-09-16 09:40 · 1,233 min · mean 15.12 CPM / 0.098 µSv/h
- Second: 2026-09-16 10:01 – 2026-09-25 07:52 · 12,832 min · 214 hours · mean 15.12 CPM / 0.098 µSv/h (min 3 / max 33 CPM)

Source: GQ Data Viewer 2.75. CC BY 4.0 with GQ Electronics attribution.
