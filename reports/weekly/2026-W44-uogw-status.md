# UOGW Weekly Status Report — 2026-W44

**Generated:** 2026-10-26 16:25 UTC
**Curator:** Aerostratospheric
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **28** |
| Global city samples (OK) | **33 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,940** |
| GHCN stations indexed | **133,039** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **1** (0 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **22 / 100 (Quiet)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 39.6 °F → **93.4 °F**
  Mean ≈ 63.9 °F · Median ≈ 61.0 °F
- Hottest sample: **Mumbai, IN** (93.4 °F)
- Coldest sample: **Reykjavik, IS** (39.6 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 88.9 | 67 | **100.9** | extreme_caution |
| Mumbai, IN | 93.4 | 41 | **96.6** | extreme_caution |
| Lagos, NG | 84.2 | 76 | **93.0** | extreme_caution |
| Bangkok, TH | 84.0 | 72 | **91.1** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 44.1 – 75.9 °F (mean 58.0 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 22 / 100 → **Quiet**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 0 |
| Watch | 1 |
| Info | 0 |

Top flags:
- **Watch** — Jakarta, ID: Robust MAD z-score |z|>=3.5

Full details: `data/latest/anomaly-report.json` · `docs/ANOMALY_METHODS.md`

---

## System Health

- Overall health: **OK**
- Checks: 11/11 passed

---

## Citation

> Aerostratospheric (2026). Unified Open Global Weather (UOGW).
> https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always cite upstream providers (Open-Meteo, NOAA NDBC / NCEI, NASA, etc.).

---

*Open atmosphere. Open archives. Midwest-made flight data for everyone.*
