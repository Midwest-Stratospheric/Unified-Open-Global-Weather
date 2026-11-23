# UOGW Weekly Status Report — 2026-W48

**Generated:** 2026-11-23 21:52 UTC
**Curator:** Aerostratospheric
**Repository:** https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Executive Snapshot

| Metric | Value |
|--------|-------|
| Catalog datasets | **38** |
| Global city samples (OK) | **34 / 34** |
| IGRA stations indexed | **2,931** |
| NDBC stations indexed | **1,945** |
| GHCN stations indexed | **133,041** |
| Casey hourly observations | **24** |
| NDBC realtime samples | **6** stations |
| Health checks | **11 / 11 OK** |
| Anomaly flags (research) | **7** (4 Alert · 3 Watch) |
| Pre-tornado Clark Co. score | **30 / 100 (Elevated)** |

---

## Surface Conditions (Global City Sample)

- **Temperature range:** 15.8 °F → **86.2 °F**
  Mean ≈ 57.5 °F · Median ≈ 59.1 °F
- Hottest sample: **Bangkok, TH** (86.2 °F)
- Coldest sample: **Anchorage, AK, US** (15.8 °F)

### Heat-Index Flags (research)

| City | T (°F) | RH % | Heat Index (°F) | Level |
|------|--------|------|-----------------|-------|
| Lagos, NG | 84.7 | 78 | **95.1** | extreme_caution |
| Bangkok, TH | 86.2 | 65 | **93.4** | extreme_caution |

---

## Local Midwest Focus — Casey, IL

- Daily range: 39.6 – 64.2 °F (mean 51.4 °F)
- NASA GLOBE registration: **GO-4VW9B**

### Pre-Tornado Research Score (Clark County)

- **Score:** 30 / 100 → **Elevated**
- **Disclaimer:** Research screening only. Not an NWS product.

---

## Anomaly Screening (Research Only)

| Severity | Count |
|----------|-------|
| Alert | 4 |
| Watch | 3 |
| Info | 0 |

Top flags:
- **Alert** — Mexico City, MX: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Buenos Aires, AR: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Alert** — Lima, PE: Robust MAD z-score |z|>=5 (outlier-resistant)
- **Watch** — Stockholm, SE: Robust MAD z-score |z|>=3.5
- **Watch** — Nairobi, KE: Robust MAD z-score |z|>=3.5

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
