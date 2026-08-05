# Unified Open Global Weather (UOGW)

**An open atmospheric data commons for research — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://www.midwestsds.com/portal.html)
[![Catalog](https://img.shields.io/badge/catalog-25%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Daily data](https://img.shields.io/badge/daily-data%2Fentries-success)](./data/entries/)
[![Anomaly detection](https://img.shields.io/badge/analytics-anomaly%20detection-orange)](./data/latest/anomaly-report.json)
[![Satellite index](https://img.shields.io/badge/satellite-radiance%20index-purple)](./data/latest/satellite-radiance-index.json)
[![Visuals](https://img.shields.io/badge/charts-°F-00d4ff)](./visuals/latest/)
[![Wiki](https://img.shields.io/badge/wiki-docs%2F-0a1628)](./docs/Home.md)

> **Mission:** Deliver a practical, versioned, multi-layer open atmospheric package every day — surface, marine, upper-air indexes, anomaly screens, satellite radiance discovery, and MSDS near-space flight data — so researchers, educators, and builders can work from one coherent commons.

**Start here for analysis:** [`data/latest/science-package.json`](./data/latest/science-package.json) · [`data/latest/research-summary.json`](./data/latest/research-summary.json)

**Graphs (°F):** embedded below · [`visuals/latest/CHARTS.md`](./visuals/latest/CHARTS.md)

---

## Built-in graphs and charts

All temperatures in charts are **Fahrenheit (°F)**. Graphs render in this README from `visuals/latest/`.

### Global city temperatures (°F)

![Global city temperatures](./visuals/latest/global-city-temperatures.png)

### City temperature map (°F)

![City temperature map](./visuals/latest/global-city-temp-map.png)

### Casey, IL hourly temperature (°F)

![Casey hourly temperature](./visuals/latest/casey-hourly-temperature.png)

### NDBC marine samples (waves m · temps °F)

![NDBC marine samples](./visuals/latest/ndbc-marine-samples.png)

### Anomaly severity

![Anomaly severity](./visuals/latest/anomaly-severity.png)

### Research cities daily Tmin / Tmax (°F)

![Research cities Tmin/Tmax](./visuals/latest/research-cities-tminmax.png)

### Daily summary card (°F)

![Daily summary card](./visuals/latest/daily-summary-card.png)

Full chart log + Mermaid: [`visuals/latest/CHARTS.md`](./visuals/latest/CHARTS.md) · Workflow: `charts-daily.yml`

---

## Why this contributes to science

Most open weather repos stop at a static list of links. UOGW is different because it **commits real observation payloads every day**, rolls them into a **research summary**, screens **anomalies**, indexes **open satellite radiance paths**, and publishes **FAIR metadata** with a **data dictionary** — while remaining honest that agencies are still the system of record.

| Capability | What researchers get |
|------------|----------------------|
| Daily science package | Combined observations + summary in one JSON |
| Global city samples | 30+ international surface observations |
| Marine realtime | Parsed NDBC buoy observations |
| Upper-air discovery | IGRA station + Y2D indexes with stats |
| Anomaly detection | Threshold + z-score screens (research only) |
| Rolling baseline | 7-day observational context |
| Satellite radiance index | GOES/JPSS/COSMIC/MERRA-2 open path map |
| FAIR + citation bundle | Reusable daily metadata |
| Built-in charts | Graphs in README (temperatures in °F) |
| First-party flight layer | MSDS X2Griffon near-space profiles as flown |

**We fly instruments.** HAB profiles enter the same commons as public indexes — not a private vault.

Raw JSON observation files stay in metric for science interoperability; **charts are Fahrenheit for display**.

---

## Daily automation (UTC)

| Time | Workflow | Output |
|------|----------|--------|
| 01:15 | MSDS Ground Daily | Casey hourly observations |
| 05:00 | Global Samples Daily | Worldwide city observations |
| 05:30 | International Indexes | GHCN + foreign sources |
| 06:30 | IGRA Index Daily | Upper-air research entry |
| 07:45 | NDBC Marine Daily | Buoy realtime observations |
| 08:00 | Catalog Rebuild | Status rollup |
| 09:00 | Daily Research Package | Science package + summary + climate |
| 09:15 | Rolling Baseline | 7-day baseline |
| 09:30 | Anomaly Detection | Anomaly report |
| 09:45 | FAIR Metadata | FAIR + citation bundle |
| 10:00 | Satellite Radiance | Open radiance product index |
| 11:00 / 13:30 | Charts Daily | PNG charts in °F |

All jobs also support **Actions → Run workflow**.

---

## Documentation

| Doc | Link |
|-----|------|
| Charts log | [`visuals/latest/CHARTS.md`](./visuals/latest/CHARTS.md) |
| Visuals guide | [`docs/VISUALS.md`](./docs/VISUALS.md) |
| Anomaly methods | [`docs/ANOMALY_METHODS.md`](./docs/ANOMALY_METHODS.md) |
| Health / alert PRs | [`docs/OPS_HEALTH.md`](./docs/OPS_HEALTH.md) |
| Rollback | [`docs/ROLLBACK.md`](./docs/ROLLBACK.md) |

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always also cite upstream providers (Open-Meteo, NOAA NDBC, NOAA NCEI, NASA, etc.).

---

## Contact

**Midwest Stratospheric Data Systems**  
Casey, Illinois, USA  
launchcontrol@midwestsds.com  
https://www.midwestsds.com  

NASA GLOBE: **GO-4VW9B** · Ham: **KE9CFY**
