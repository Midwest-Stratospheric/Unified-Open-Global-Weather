# UOGW Weekly Status Report — 2026-W37

**Generated:** 2026-09-07 15:28 UTC
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
| Anomaly flags (research) | **3** (3 Alert · 0 Watch) |
| Pre-tornado Clark Co. score | **26 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 42.4 °F → **104.2 °F**
  Mean ≈ 69.7 °F · Median ≈ 69.5 °F
- Hottest sample: **Dubai, AE** (104.2 °F)
- Coldest sample: **Buenos Aires, AR** (42.4 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 104.2 | 37 | **116.3** | danger |
| Cairo, EG | 93.6 | 41 | **97.0** | extreme_caution |
| Singapore, SG | 87.8 | 58 | **93.8** | extreme_caution |
| Jakarta, ID | 87.8 | 50 | **90.7** | extreme_caution |
| Mumbai, IN | 83.3 | 74 | **90.2** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 65.8 – 85.6 °F (mean 75.7 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 26 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 3 |
| Watch | 0 |
| Info | 0 |

Top flags:
- **Alert** — Dubai, AE: Extreme heat: T>=40C (example: desert heat 42C)
- **Alert** — Casey, IL, US: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Chicago, IL, US: Robust MAD z-score |z|>=5 (outlier-resistant)

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
