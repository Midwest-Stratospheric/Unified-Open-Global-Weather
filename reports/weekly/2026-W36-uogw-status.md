# UOGW Weekly Status Report — 2026-W36

**Generated:** 2026-08-31 10:04 UTC
**Curator:** Midwest Stratospheric Data Systems (Aerostratospheric)
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **25** |
| Global city samples (OK) | **32 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,936** |
| GHCN stations indexed | **132,501** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **7** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **1** (0 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **31 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 54.7 °F → **97.3 °F**
  Mean ≈ 70.8 °F · Median ≈ 68.0 °F
- Hottest sample: **Dubai, AE** (97.3 °F)
- Coldest sample: **Buenos Aires, AR** (54.7 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Jakarta, ID | 93.9 | 42 | **98.0** | extreme_caution |
| Singapore, SG | 89.1 | 60 | **97.6** | extreme_caution |
| Dubai, AE | 97.3 | 26 | **96.2** | extreme_caution |
| Bangkok, TH | 85.6 | 69 | **93.7** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 64.8 – 90.5 °F (mean 76.3 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 31 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 0 |
| Watch | 1 |
| Info | 0 |

Top flags:
- **Watch** — Dubai, AE: High heat: T>=35C (example: 36.2C mid-latitude hot day)

Full details: `data/latest/anomaly-report.json` · `docs/ANOMALY_METHODS.md`

---

## System Health

- Overall health: **OK**
- Checks: 11/11 passed

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW).
> https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always cite upstream providers (Open-Meteo, NOAA NDBC / NCEI, NASA, etc.).

---

*Open atmosphere. Open archives. Midwest-made flight data for everyone.*
