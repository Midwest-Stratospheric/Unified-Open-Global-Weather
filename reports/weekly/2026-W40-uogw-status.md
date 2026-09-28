# UOGW Weekly Status Report — 2026-W40

**Generated:** 2026-09-28 17:57 UTC
**Curator:** Midwest Stratospheric Data Systems (Aerostratospheric)
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **26** |
| Global city samples (OK) | **32 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,940** |
| GHCN stations indexed | **132,503** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **7** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **4** (3 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **19 / 100 (Quiet)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 40.6 °F → **97.3 °F**
  Mean ≈ 68.2 °F · Median ≈ 68.6 °F
- Hottest sample: **Dubai, AE** (97.3 °F)
- Coldest sample: **Anchorage, AK, US** (40.6 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 97.3 | 53 | **113.5** | danger |
| Mumbai, IN | 85.6 | 66 | **92.5** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 49.6 – 76.1 °F (mean 62.4 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 19 / 100 → **Quiet**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 3 |
| Watch | 1 |
| Info | 0 |

Top flags:
- **Watch** — Dubai, AE: High heat: T>=35C (example: 36.2C mid-latitude hot day)
- **Alert** — Mexico City, MX: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Berlin, DE: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Madrid, ES: Robust MAD z-score |z|>=5 (outlier-resistant)

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
