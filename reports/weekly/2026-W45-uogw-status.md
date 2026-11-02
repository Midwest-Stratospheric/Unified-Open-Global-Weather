# UOGW Weekly Status Report — 2026-W45

**Generated:** 2026-11-02 19:56 UTC
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
| NDBC stations indexed | **1,940** |
| GHCN stations indexed | **133,041** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **3** (3 Alert · 0 Watch) |
| Pre-tornado Clark Co. score | **33 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 30.7 °F → **88.7 °F**
  Mean ≈ 63.3 °F · Median ≈ 61.5 °F
- Hottest sample: **Cairo, EG** (88.7 °F)
- Coldest sample: **Anchorage, AK, US** (30.7 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Dubai, AE | 88.7 | 64 | **98.7** | extreme_caution |
| Bangkok, TH | 87.6 | 68 | **98.1** | extreme_caution |
| Jakarta, ID | 86.5 | 68 | **95.4** | extreme_caution |
| Mumbai, IN | 87.3 | 55 | **91.7** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 56.1 – 69.8 °F (mean 61.2 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 33 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 3 |
| Watch | 0 |
| Info | 0 |

Top flags:
- **Alert** — Lima, PE: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Cairo, EG: Robust MAD z-score |z|>=5 (outlier-resistant)
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
