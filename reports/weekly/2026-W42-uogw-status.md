# UOGW Weekly Status Report — 2026-W42

**Generated:** 2026-10-12 19:35 UTC
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
| Anomaly flags (research) | **5** (3 Alert · 2 Watch) |
| Pre-tornado Clark Co. score | **36 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 39.6 °F → **93.2 °F**
  Mean ≈ 68.5 °F · Median ≈ 69.2 °F
- Hottest sample: **Mumbai, IN** (93.2 °F)
- Coldest sample: **Anchorage, AK, US** (39.6 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 90.9 | 70 | **108.7** | danger |
| Mumbai, IN | 93.2 | 44 | **97.7** | extreme_caution |
| Lagos, NG | 84.2 | 77 | **93.4** | extreme_caution |
| Jakarta, ID | 85.6 | 67 | **92.9** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 57.6 – 82.4 °F (mean 66.4 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 36 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 3 |
| Watch | 2 |
| Info | 0 |

Top flags:
- **Watch** — Lima, PE: Robust MAD z-score |z|>=3.5
- **Alert** — Madrid, ES: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Watch** — Dubai, AE: Robust MAD z-score |z|>=3.5
- **Alert** — Beijing, CN: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Singapore, SG: Robust MAD z-score |z|>=5 (outlier-resistant)

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
