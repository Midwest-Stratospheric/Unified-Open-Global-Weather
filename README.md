# Unified Open Global Weather (UOGW)

**An open atmospheric data commons for research — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://midwestsds.com/msds-data-hub.html)
[![Catalog](https://img.shields.io/badge/catalog-25%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Anomaly detection](https://img.shields.io/badge/analytics-anomaly%20detection-orange)](./data/latest/anomaly-report.json)
[![Science analytics](https://img.shields.io/badge/analytics-science%20package-blue)](./data/latest/science-analytics.json)
[![Visuals](https://img.shields.io/badge/charts-°F-00d4ff)](./visuals/latest/)

**Start here:** [`science-package.json`](./data/latest/science-package.json) · [`science-analytics.json`](./data/latest/science-analytics.json) · [`hub-endpoints.json`](./data/latest/hub-endpoints.json)  
**Data Hub:** https://midwestsds.com/msds-data-hub.html

---

## Built-in graphs and charts (°F)

### Global city temperatures

![Global city temperatures](./visuals/latest/global-city-temperatures.png)

Horizontal bar chart of current surface air temperature for each successful global city sample. Bars are sorted cold→hot; warmer colors mark heat (≥86°F / ≥95°F).

### City temperature map

![City temperature map](./visuals/latest/global-city-temp-map.png)

Scatter map of the same city samples by longitude/latitude, colored by temperature (°F). Shows geographic pattern of the daily open sample set.

### Casey, IL hourly temperature

![Casey hourly temperature](./visuals/latest/casey-hourly-temperature.png)

24-hour temperature trace for Casey, Illinois (MSDS home site). Useful for diurnal range and local extremes that feed anomaly rules.

### NDBC marine samples

![NDBC marine samples](./visuals/latest/ndbc-marine-samples.png)

NOAA NDBC buoy sample panel: wave height (meters) plus water and air temperature (°F) for stations included in today's marine pull.

### Global city relative humidity

![Global city humidity](./visuals/latest/global-city-humidity.png)

Relative humidity (%) for the same global city sample network. Dry+hot combinations can contribute to compound research flags.

### Anomaly severity

![Anomaly severity](./visuals/latest/anomaly-severity.png)

Count of UOGW research anomaly flags by severity (alert / watch / info). **Not** an NWS warning product.

#### Anomaly detection guide

| Severity | Meaning |
|----------|---------|
| **Alert** | Strong outlier vs thresholds or baseline (extreme heat/cold, \|z\| ≥ 3, very high waves). |
| **Watch** | Elevated interest — heat/cold, wind, low pressure, or \|z\| ≥ 2.5 vs the 7-day baseline. |
| **Info** | Lower urgency (hot + very dry, strong high, warm water sample). |

Methods: [`docs/ANOMALY_METHODS.md`](./docs/ANOMALY_METHODS.md) · [`visuals/ANOMALY_GUIDE.md`](./visuals/ANOMALY_GUIDE.md) · [`anomaly-report.json`](./data/latest/anomaly-report.json)

### Research cities daily Tmin / Tmax

![Research cities Tmin/Tmax](./visuals/latest/research-cities-tminmax.png)

Daily minimum and maximum temperatures for the research climate city set. Compares day-range width across selected locations.

### Daily summary card

![Daily summary card](./visuals/latest/daily-summary-card.png)

One-page snapshot of today's visual package: city count, temperature span, Casey hours, NDBC samples, and anomaly total.

Full descriptions: [`visuals/CHART_DESCRIPTIONS.md`](./visuals/CHART_DESCRIPTIONS.md) · gallery: [`visuals/latest/CHARTS.md`](./visuals/latest/CHARTS.md)

---

## Feature highlights

| Area | What you get |
|------|----------------|
| Daily science package | Combined observations + summary |
| Science analytics | Extremes, coverage, heat-index flags |
| Anomaly detection | Threshold + multi-method z-scores (research only) |
| Charts automation | °F PNGs + markdown after data workflows |
| Hub endpoints map | `data/latest/hub-endpoints.json` |
| Health / rollback | Self-heal, alert PRs, rollback docs |

See [`docs/FEATURES.md`](./docs/FEATURES.md).

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always cite upstream providers (Open-Meteo, NOAA NDBC, NOAA NCEI, NASA, etc.).

---

**Midwest Stratospheric Data Systems** · Casey, Illinois · launchcontrol@midwestsds.com · NASA GLOBE **GO-4VW9B** · Ham **KE9CFY**
