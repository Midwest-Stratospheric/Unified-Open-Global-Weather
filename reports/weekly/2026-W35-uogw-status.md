# UOGW Weekly Status Report — 2026-W35

**Generated:** 2026-08-24 11:13 UTC
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
| Anomaly flags (research) | **1** (1 Alert · 0 Watch) |
| Pre-tornado Clark Co. score | **19 / 100 (Quiet)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 42.6 °F → **91.2 °F**
  Mean ≈ 69.3 °F · Median ≈ 64.7 °F
- Hottest sample: **Bangkok, TH** (91.2 °F)
- Coldest sample: **Buenos Aires, AR** (42.6 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Beijing, CN | 88.0 | 67 | **98.6** | extreme_caution |
| Bangkok, TH | 91.2 | 53 | **98.5** | extreme_caution |
| Singapore, SG | 89.6 | 55 | **96.2** | extreme_caution |
| Seoul, KR | 86.5 | 68 | **95.4** | extreme_caution |
| Mumbai, IN | 84.4 | 77 | **93.9** | extreme_caution |
| Jakarta, ID | 90.1 | 47 | **93.5** | extreme_caution |
| Tokyo, JP | 84.7 | 72 | **92.8** | extreme_caution |
| Cairo, EG | 85.6 | 59 | **90.0** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 59.2 – 79.2 °F (mean 68.8 °F)
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
- **Alert** — Nairobi, KE: Robust MAD z-score |z|>=5 (outlier-resistant)

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
