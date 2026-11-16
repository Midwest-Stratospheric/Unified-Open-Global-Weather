# UOGW Weekly Status Report — 2026-W47

**Generated:** 2026-11-16 19:58 UTC
**Curator:** Aerostratospheric
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **38** |
| Global city samples (OK) | **31 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,945** |
| GHCN stations indexed | **133,041** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **2** (0 Alert · 2 Watch) |
| Pre-tornado Clark Co. score | **19 / 100 (Quiet)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 26.4 °F → **87.8 °F**
  Mean ≈ 61.7 °F · Median ≈ 60.6 °F
- Hottest sample: **Lagos, NG** (87.8 °F)
- Coldest sample: **Anchorage, AK, US** (26.4 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Lagos, NG | 87.8 | 68 | **98.6** | extreme_caution |
| Bangkok, TH | 86.4 | 68 | **95.2** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 24.6 – 52.5 °F (mean 37.1 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 19 / 100 → **Quiet**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 0 |
| Watch | 2 |
| Info | 0 |

Top flags:
- **Watch** — Anchorage, AK, US: Very low MSLP <= 980 hPa (example: 972 hPa deep low)
- **Watch** — Mumbai, IN: Robust MAD z-score |z|>=3.5

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
