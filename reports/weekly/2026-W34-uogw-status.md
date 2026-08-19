# UOGW Weekly Status Report — 2026-W34

**Period:** 2026-08-13 → 2026-08-19  
**Generated:** 2026-08-19 (UTC)  
**Curator:** Midwest Stratospheric Data Systems (Aerostratospheric)  
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather  
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **25** |
| Global city samples (OK) | **31 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,936** |
| GHCN stations indexed | **132,501** (219 countries) |
| Casey hourly observations | **24** |
| NDBC realtime samples | **7** stations |
| Health checks | **11 / 11 OK** (no critical fails) |
| Anomaly flags (research) | **3** (2 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **68 / 100 (High research concern)** |

All core daily pipelines (global samples, MSDS ground, NDBC, research package, anomaly detection, charts, health monitor) completed successfully.

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 45.0 °F (Buenos Aires) → **105.3 °F (Dubai)**  
  Mean ≈ 71.2 °F · Median ≈ 67.8 °F
- **Humidity:** mean 70.9 % (range 28–92 %)
- **Pressure:** mean 1013.2 hPa
- **Wind:** mean 2.7 m/s

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 105.3 | 28 | **110.5** | Danger |
| Bangkok, TH | 89.6 | 58 | 97.7 | Extreme Caution |
| Singapore, SG | 87.6 | 66 | 97.1 | Extreme Caution |
| Jakarta, ID | 87.8 | 59 | 94.3 | Extreme Caution |
| Beijing, CN | 87.3 | 57 | 92.4 | Extreme Caution |
| Seoul, KR | 86.0 | 62 | 91.8 | Extreme Caution |
| Tokyo, JP | 89.4 | 45 | 91.5 | Extreme Caution |
| Mumbai, IN | 82.8 | 79 | 90.5 | Extreme Caution |

---

## Local Midwest Focus — Casey, IL (MSDS Home Site)

- **Daily range (2026-08-18):** 62.1 – 82.4 °F (mean 72.4 °F)
- Humidity mean ≈ 77 %
- NASA GLOBE registration: **GO-4VW9B**
- 24 hourly observations present and healthy

### Pre-Tornado Research Score (Clark County)

- **Score:** 68 / 100 → **High research concern**
- Key drivers: CAPE ≈ 1050 J/kg, Lifted Index −5.7, rich low-level moisture, falling pressure
- **Disclaimer:** Research screening only. Not an NWS product. Follow official NWS / SPC guidance.

---

## Anomaly Screening (Research Only)

| Severity | Count | Notable |
|----------|-------|---------|
| Alert | 2 | Dubai extreme heat (40.7 °C); Lima robust MAD z-score cold outlier |
| Watch | 1 | São Paulo elevated MAD z-score |
| Info | 0 | — |

Methods: absolute thresholds + multi-method z-scores (population, sample, MAD). Full details in `data/latest/anomaly-report.json` and `docs/ANOMALY_METHODS.md`.

---

## System Health & Coverage

- **Health report:** All 11 monitored endpoints OK (global-cities, casey-hourly, ndbc-realtime, science-package, research-summary, anomaly, baseline, satellite, fair-metadata, charts, catalog).
- **Self-heal / rollback points** available.
- **Automations active:** 21 GitHub Actions workflows (daily + on-demand).
- Layer coverage remains complete across Ground · Marine · Upper-air · Stratospheric · Satellite · Flight.

---

## Notable Indexes

| Index | Count |
|-------|-------|
| IGRA radiosonde stations | 2,931 |
| NDBC marine stations | 1,936 |
| GHCN daily stations | 132,501 |
| Foreign open sources | 18 |
| Satellite radiance products | 6 |

---

## Outlook & Notes

- Daily science packages, charts (°F), and analytics continue on schedule.
- X2Griffon / MSDS flight products remain planned (maiden public launch window September 2026).
- This weekly report series is now automated (see `.github/workflows/weekly-report.yml`).

**Citation**  
> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always cite upstream providers (Open-Meteo, NOAA NDBC / NCEI, NASA, etc.).

---

*Open atmosphere. Open archives. Midwest-made flight data for everyone.*
