# UOGW Weekly Status Report — 2026-W43

**Generated:** 2026-10-19 16:45 UTC
**Curator:** Aerostratospheric
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
| GHCN stations indexed | **133,039** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **1** (1 Alert · 0 Watch) |
| Pre-tornado Clark Co. score | **19 / 100 (Quiet)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 37.0 °F → **91.9 °F**
  Mean ≈ 61.6 °F · Median ≈ 58.2 °F
- Hottest sample: **Mumbai, IN** (91.9 °F)
- Coldest sample: **Casey, IL, US** (37.0 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Mumbai, IN | 91.9 | 61 | **105.1** | danger |
| Lagos, NG | 86.2 | 73 | **96.9** | extreme_caution |
| Jakarta, ID | 87.6 | 62 | **95.2** | extreme_caution |
| Singapore, SG | 85.3 | 68 | **92.6** | extreme_caution |
| Bangkok, TH | 82.2 | 83 | **90.1** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 34.0 – 65.3 °F (mean 48.2 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 19 / 100 → **Quiet**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 1 |
| Watch | 0 |
| Info | 0 |

Top flags:
- **Alert** — Lagos, NG: Robust MAD z-score |z|>=5 (outlier-resistant)

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
