# UOGW Weekly Status Report — 2026-W41

**Generated:** 2026-10-05 19:01 UTC
**Curator:** Midwest Stratospheric Data Systems (Aerostratospheric)
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **26** |
| Global city samples (OK) | **34 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,940** |
| GHCN stations indexed | **133,039** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **2** (0 Alert · 2 Watch) |
| Pre-tornado Clark Co. score | **26 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 39.2 °F → **94.5 °F**
  Mean ≈ 67.0 °F · Median ≈ 67.1 °F
- Hottest sample: **Dubai, AE** (94.5 °F)
- Coldest sample: **Anchorage, AK, US** (39.2 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 94.5 | 70 | **120.8** | danger |
| Mumbai, IN | 88.0 | 63 | **96.6** | extreme_caution |
| Bangkok, TH | 84.6 | 74 | **93.3** | extreme_caution |
| Jakarta, ID | 84.9 | 70 | **92.5** | extreme_caution |
| Singapore, SG | 83.8 | 76 | **92.0** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 44.6 – 81.0 °F (mean 62.2 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 26 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 0 |
| Watch | 2 |
| Info | 0 |

Top flags:
- **Watch** — Seoul, KR: Robust MAD z-score |z|>=3.5
- **Watch** — Casey, IL: Diurnal range >= 20C (example: -2C to 19C => 21C)

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
