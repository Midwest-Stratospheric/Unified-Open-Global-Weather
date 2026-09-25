# Casey GMC-800 — fixed ground radiation station

First-party **surface ionizing-radiation** observations from a GQ Electronics **GMC-800** Geiger–Müller counter at the Aerostratospheric / MSDS Casey, Illinois site.

This product is **not** a balloon flight profile and **not** a mobile track. It is a **fixed weather-and-radiation station**: the same coordinates are applied to every sample.

## Why radiation is in UOGW

UOGW already publishes surface meteorology at Casey. The GMC-800 adds a co-located **background radiation** layer so researchers can compare local dose rate with weather, space-weather, and (after recovery) near-space flight profiles.

Typical uses:
- local background CPM / µSv/h baseline for the Casey launch site
- context for why surface radiation is tracked on UOGW alongside temperature and humidity
- comparison of ground dose rate before and after HAB flights

This is a **research / citizen-science** series. It is **not** a regulatory health product and is **not** an emergency alert feed.

## Fixed location

| Field | Value |
|-------|-------|
| Station id | `MSDS-GMC800-CASEY` |
| Latitude | **39.2974 N** |
| Longitude | **87.9818 W** (−87.9818) |
| Timezone | America/Chicago |
| Location mode | **fixed** |
| Instrument | GQ Electronics GMC-800 |
| Variables | `cpm` (counts per minute), `usv_h` (µSv/h) |

Do not relocate samples. If the unit is moved, open a new station id.

## What the files contain

| File | Role |
|------|------|
| `station.json` | Immutable site metadata (lat/lon, instrument, variables) |
| `latest.json` | Current ingest: daily CPM / µSv/h rollup plus last 24 hours hourly |
| `2026-09-16.json` | Dated pointer for the first ingest (2026-09-15 12:40 – 2026-09-16 09:40) |
| `2026-09-25.json` | Dated pointer for the second ingest (2026-09-16 10:01 – 2026-09-25 07:52) |

Native logger interval from Data Viewer is **1 minute** (`Every Second` save type aggregated to CPM / µSv/h per minute). Daily products average those minutes.

## Radiation quantities

| Field | Meaning |
|-------|---------|
| `cpm` | Tube counts per minute (instantaneous minute total from the export) |
| `usv_h` | Dose-rate indication in microsieverts per hour, as reported by the GMC-800 / Data Viewer |

The GMC-800 registers beta, gamma, and X-ray. Values here are **as exported**; they are not independently recailbrated in this repo.

First ingest (2026-09-15 12:40 – 2026-09-16 09:40 America/Chicago): 1,233 minute samples, mean **15.12 CPM** / **0.098 µSv/h**.

Second ingest (2026-09-16 10:01 – 2026-09-25 07:52 America/Chicago): 12,832 minute samples, 214 consecutive hours, mean **15.12 CPM** / **0.098 µSv/h** (min 3 / max 33 CPM). Continues immediately after the first ingest with no multi-hour gaps.

## Source

GQ Geiger Counter Data Viewer 2.75 history export (`20260916_09_40_54.csv` first window; `20260925_07_47_18.csv` second window). Curated by Aerostratospheric. License for the curated package: CC BY 4.0 with instrument attribution to GQ Electronics.

Sibling copy: [IGDR station](https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository/blob/main/stations/msds-gmc800-casey.json) and [IGDR snapshot](https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository/blob/main/snapshots/2026-09-25/gmc-800-casey.json).
