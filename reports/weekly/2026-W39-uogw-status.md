# UOGW Weekly Status Report — 2026-W39

**Generated:** 2026-09-21 16:09 UTC
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
| NDBC stations indexed | **1,939** |
| GHCN stations indexed | **132,503** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **7** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **2** (1 Alert · 1 Watch) |
| Pre-tornado Clark Co. score | **30 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 45.5 °F → **101.8 °F**
  Mean ≈ 70.3 °F · Median ≈ 68.2 °F
- Hottest sample: **Dubai, AE** (101.8 °F)
- Coldest sample: **Anchorage, AK, US** (45.5 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 101.8 | 34 | **108.4** | danger |
| Singapore, SG | 85.5 | 77 | **96.9** | extreme_caution |
| Mumbai, IN | 84.2 | 76 | **93.0** | extreme_caution |
| Bangkok, TH | 81.9 | 87 | **90.4** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 71.1 – 88.3 °F (mean 78.8 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 30 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 1 |
| Watch | 1 |
| Info | 0 |

Top flags:
- **Watch** — Dubai, AE: High heat: T>=35C (example: 36.2C mid-latitude hot day)
- **Alert** — Johannesburg, ZA: Robust MAD z-score |z|>=5 (outlier-resistant)

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
