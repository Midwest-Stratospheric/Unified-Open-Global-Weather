# UOGW Weekly Status Report — 2026-W46

**Generated:** 2026-11-09 20:22 UTC
**Curator:** Aerostratospheric
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **38** |
| Global city samples (OK) | **33 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,945** |
| GHCN stations indexed | **133,041** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **2** (1 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **25 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 26.6 °F → **90.3 °F**
  Mean ≈ 58.9 °F · Median ≈ 58.5 °F
- Hottest sample: **Mumbai, IN** (90.3 °F)
- Coldest sample: **Anchorage, AK, US** (26.6 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Lagos, NG | 86.0 | 73 | **96.4** | extreme_caution |
| Dubai, AE | 87.3 | 55 | **91.7** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 31.6 – 63.5 °F (mean 46.1 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 25 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 1 |
| Watch | 1 |
| Info | 0 |

Top flags:
- **Alert** — Lima, PE: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Watch** — Honolulu, HI, US: Robust MAD z-score |z|>=3.5

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
