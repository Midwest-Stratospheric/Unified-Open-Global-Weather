# UOGW Weekly Status Report — 2026-W38

**Generated:** 2026-09-14 16:07 UTC
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
| NDBC stations indexed | **1,938** |
| GHCN stations indexed | **132,501** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **7** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **4** (0 Alert · 4 Watch) |
| Pre-tornado Clark Co. score | **30 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 43.0 °F → **100.8 °F**
  Mean ≈ 69.2 °F · Median ≈ 69.8 °F
- Hottest sample: **Dubai, AE** (100.8 °F)
- Coldest sample: **Buenos Aires, AR** (43.0 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 100.8 | 40 | **111.1** | danger |
| Cairo, EG | 94.1 | 35 | **95.0** | extreme_caution |
| Jakarta, ID | 90.1 | 41 | **91.2** | extreme_caution |
| Mumbai, IN | 83.3 | 77 | **91.1** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 63.9 – 86.7 °F (mean 74.0 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 30 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 0 |
| Watch | 4 |
| Info | 0 |

Top flags:
- **Watch** — Dubai, AE: High heat: T>=35C (example: 36.2C mid-latitude hot day)
- **Watch** — Chicago, IL, US: Robust MAD z-score |z|>=3.5
- **Watch** — Mexico City, MX: Robust MAD z-score |z|>=3.5
- **Watch** — Sydney, AU: Robust MAD z-score |z|>=3.5

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
