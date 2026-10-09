# Casey GMC-800 — fixed ground radiation station

First-party **surface ionizing-radiation** observations from a GQ Electronics **GMC-800** at Casey, Illinois.

## Ingest policy (always)

Every GMC-800 export is committed comprehensively:

1. Full **hourly** series for the whole window (`hourly_START_END.csv`) — every hour, min/mean/max/median CPM and µSv/h
2. **Daily** rollup + window stats in `latest.json` and a dated pointer
3. **Minute** CSVs under `minutes/YYYY-MM-DD.csv` when the export is attached (none are published yet; see below)
4. IGDR snapshot for the ingest date

Do not replace a comprehensive commit with a short latest-only window.

## Location

`MSDS-GMC800-CASEY` · 39.2974 N, 87.9818 W · America/Chicago · fixed · GQ GMC-800 · `cpm`, `usv_h`

## Current files

| File | Role |
|------|------|
| `station.json` | Site metadata |
| `latest.json` | Current window stats + daily rollup (2026-10-09 ingest) |
| `hourly_2026-09-16_2026-09-19.csv` | 86 hours (2026-09-25 ingest, part 1) |
| `hourly_2026-09-20_2026-09-25.csv` | 128 hours (2026-09-25 ingest, part 2) |
| `hourly_2026-09-25_2026-10-09.csv` | All 338 hours of the 2026-10-09 ingest |
| `hourly_2026-09-25_2026-09-30.csv` / `hourly_2026-10-01_2026-10-09.csv` | Same 338 hours split into two parts (136 + 202); duplicates of the combined file |
| `2026-09-16.json` / `2026-09-25.json` / `2026-10-09.json` | Dated pointers for each ingest |
| `compilation/` | Daily compilation CSV/JSON (one row per day plus one window summary row) |

Native 1-minute rows are **not published** in this folder. The hourly files summarize them (`n` = minutes in each hour).

## Ingest history

| Ingest | Window (Casey local time) | Minute readings | Hourly rows |
|---|---|---|---|
| 2026-09-16 | 2026-09-15 12:40 – 2026-09-16 09:40 | 1,233 | not in current hourly files (count recorded in `2026-09-16.json`) |
| 2026-09-25 | 2026-09-16 10:01 – 2026-09-25 07:52 | 12,832 | 214 |
| 2026-10-09 | 2026-09-25 08:05 – 2026-10-09 09:30 | 20,244 | 338 |

Hourly coverage: **2026-09-16 10:00 to 2026-10-09 09:30 CT**, 552 unique hours, 33,076 minute readings, with no missing hours.

Window stats:

- 2026-09-25 ingest: mean 15.12 CPM / 0.098 µSv/h (min 3 / max 33 CPM)
- 2026-10-09 ingest: mean 15.00 CPM / 0.097 µSv/h (min 3 / max 32 CPM; 0.020–0.208 µSv/h)

## Units

CPM is counts per minute. µSv/h (microsieverts per hour) is the dose-rate estimate reported by the device export.

## Update cadence

Updates are **manual exports** from the counter using GQ Data Viewer 2.75, committed when an export is made (so far on 2026-09-16, 2026-09-25 and 2026-10-09). This folder is not a real-time feed.

Source: GQ Data Viewer 2.75. CC BY 4.0 with GQ Electronics attribution.
