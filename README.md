# Unified Open Global Weather (UOGW)

**An open atmospheric data commons for research — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://midwestsds.com/msds-data-hub.html)
[![Catalog](https://img.shields.io/badge/catalog-25%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Daily data](https://img.shields.io/badge/daily-data%2Fentries-success)](./data/entries/)
[![Anomaly detection](https://img.shields.io/badge/analytics-anomaly%20detection-orange)](./data/latest/anomaly-report.json)
[![Science analytics](https://img.shields.io/badge/analytics-science%20package-blue)](./data/latest/science-analytics.json)
[![Visuals](https://img.shields.io/badge/charts-°F-00d4ff)](./visuals/latest/)
[![Features](https://img.shields.io/badge/docs-feature%20catalog-0a1628)](./docs/FEATURES.md)

> **Mission:** Deliver a practical, versioned, multi-layer open atmospheric package every day — surface, marine, upper-air indexes, anomaly screens, satellite radiance discovery, and MSDS near-space flight data.

**Start here:** [`science-package.json`](./data/latest/science-package.json) · [`science-analytics.json`](./data/latest/science-analytics.json) · [`hub-endpoints.json`](./data/latest/hub-endpoints.json)

**Data Hub UI:** https://midwestsds.com/msds-data-hub.html

---

## Built-in graphs and charts (°F)

### Global city temperatures

![Global city temperatures](./visuals/latest/global-city-temperatures.png)

### City temperature map

![City temperature map](./visuals/latest/global-city-temp-map.png)

### Casey, IL hourly temperature

![Casey hourly temperature](./visuals/latest/casey-hourly-temperature.png)

### NDBC marine samples

![NDBC marine samples](./visuals/latest/ndbc-marine-samples.png)

### Anomaly severity

![Anomaly severity](./visuals/latest/anomaly-severity.png)

#### Anomaly detection guide (what this graph means)

UOGW counts **research flags** for the daily sample set — **not** National Weather Service warnings.

| Severity | Meaning |
|----------|---------|
| **Alert** | Strong outlier vs thresholds or baseline (extreme heat/cold, \|z\| ≥ 3, very high waves). |
| **Watch** | Elevated interest — heat/cold, wind, low pressure, or \|z\| ≥ 2.5 vs the 7-day baseline. |
| **Info** | Lower urgency (hot + very dry, strong high, warm water sample). |

**How flags are made**

1. Absolute thresholds (`analytics/anomaly-thresholds.json`)
2. Z-scores vs rolling baseline (population z primary; MAD z also reported)
3. Site rules (e.g. large Casey day/night range)

Full methods: [`docs/ANOMALY_METHODS.md`](./docs/ANOMALY_METHODS.md) · short guide: [`visuals/ANOMALY_GUIDE.md`](./visuals/ANOMALY_GUIDE.md) · data: [`anomaly-report.json`](./data/latest/anomaly-report.json)

### Research cities daily Tmin / Tmax

![Research cities Tmin/Tmax](./visuals/latest/research-cities-tminmax.png)

### Daily summary card

![Daily summary card](./visuals/latest/daily-summary-card.png)

Full gallery + Mermaid: [`visuals/latest/CHARTS.md`](./visuals/latest/CHARTS.md)

---

## Feature highlights

| Area | What you get |
|------|----------------|
| Daily science package | Combined observations + summary |
| Science analytics | Extremes, coverage, heat-index flags, hub cards |
| Anomaly detection | Threshold + multi-method z-scores (research only) |
| Charts automation | °F PNGs + markdown after data workflows |
| Health / rollback | Self-heal, alert PRs, explicit rollback docs |
| Hub endpoints map | `data/latest/hub-endpoints.json` for the website |
| First-party flight layer | MSDS X2Griffon profiles as flown |

See the full list in [`docs/FEATURES.md`](./docs/FEATURES.md).

Raw observation JSON stays **metric** for science; **charts and hub highlights use °F** for readability.

---

## Daily automation (UTC)

| Time | Workflow |
|------|----------|
| 01:15 | MSDS Ground Daily |
| 05:00 | Global Samples Daily |
| 05:30 | International Indexes |
| 06:30 | IGRA Index Daily |
| 07:45 | NDBC Marine Daily |
| 08:00 | Catalog Rebuild |
| 09:00 | Daily Research Package |
| 09:15 | Rolling Baseline |
| 09:30 | Anomaly Detection |
| 09:45 | Science Analytics · FAIR Metadata |
| 10:00 | Satellite Radiance |
| 11:00 / 13:30 | Charts Daily |
| 12:00 / 18:00 | Health Monitor |

---

## Documentation

| Doc | Link |
|-----|------|
| Feature catalog | [`docs/FEATURES.md`](./docs/FEATURES.md) |
| Anomaly methods | [`docs/ANOMALY_METHODS.md`](./docs/ANOMALY_METHODS.md) |
| Anomaly guide (visuals) | [`visuals/ANOMALY_GUIDE.md`](./visuals/ANOMALY_GUIDE.md) |
| Science analytics | [`docs/SCIENCE_ANALYTICS.md`](./docs/SCIENCE_ANALYTICS.md) |
| Visuals | [`docs/VISUALS.md`](./docs/VISUALS.md) |
| Health / alert PRs | [`docs/OPS_HEALTH.md`](./docs/OPS_HEALTH.md) |
| Rollback | [`docs/ROLLBACK.md`](./docs/ROLLBACK.md) |

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always cite upstream providers (Open-Meteo, NOAA NDBC, NOAA NCEI, NASA, etc.).

---

## Contact

**Midwest Stratospheric Data Systems** · Casey, Illinois, USA · launchcontrol@midwestsds.com · https://www.midwestsds.com  
NASA GLOBE **GO-4VW9B** · Ham **KE9CFY**
