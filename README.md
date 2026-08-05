# Unified Open Global Weather (UOGW)

**An open atmospheric data commons for research — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://www.midwestsds.com/portal.html)
[![Catalog](https://img.shields.io/badge/catalog-25%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Daily data](https://img.shields.io/badge/daily-data%2Fentries-success)](./data/entries/)
[![Anomaly detection](https://img.shields.io/badge/analytics-anomaly%20detection-orange)](./data/latest/anomaly-report.json)
[![Satellite index](https://img.shields.io/badge/satellite-radiance%20index-purple)](./data/latest/satellite-radiance-index.json)
[![Wiki](https://img.shields.io/badge/wiki-docs%2F-0a1628)](./docs/Home.md)

> **Mission:** Deliver a practical, versioned, multi-layer open atmospheric package every day — surface, marine, upper-air indexes, anomaly screens, satellite radiance discovery, and MSDS near-space flight data — so researchers, educators, and builders can work from one coherent commons.

**Start here for analysis:** [`data/latest/science-package.json`](./data/latest/science-package.json) · [`data/latest/research-summary.json`](./data/latest/research-summary.json)

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
| First-party flight layer | MSDS X2Griffon near-space profiles as flown |

**We fly instruments.** HAB profiles enter the same commons as public indexes — not a private vault.

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

All jobs also support **Actions → Run workflow**.

Independence: automations run on GitHub Actions inside this repository. They do **not** require midwestsds.com to be online.

---

## Where the data lives

```
data/
  entries/YYYY-MM-DD/     # Immutable-ish daily research folder
  latest/                 # Stable paths for notebooks & pipelines
layers/                   # Layered indexes + samples
docs/                     # Wiki, data dictionary, science contributing guide
catalog/catalog.json      # Machine catalog
sources/registry.json     # US + foreign authorities
```

### Stable analysis URLs

```text
.../data/latest/science-package.json
.../data/latest/research-summary.json
.../data/latest/global-cities.json
.../data/latest/ndbc-realtime.json
.../data/latest/casey-hourly.json
.../data/latest/anomaly-report.json
.../data/latest/rolling-baseline.json
.../data/latest/satellite-radiance-index.json
.../data/latest/fair-metadata.json
```

Base: `https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/`

---

## Polished science components

### 1) Automated anomaly detection
Research-oriented screening (not official warnings):
- Absolute thresholds (extreme heat/cold, low pressure, high wind, high waves)
- Optional **z-scores** vs the 7-day rolling baseline
- Written daily to `data/latest/anomaly-report.json`

### 2) Satellite radiance integration (discovery layer)
Full radiance archives are multi-TB and belong on AWS/NOAA/NASA. UOGW publishes a **daily open radiance index** for GOES ABI L1b, JPSS VIIRS paths, COSMIC RO, and MERRA-2 entry points — so multi-layer studies can start from one map.

### 3) Three additional polish components
| Component | Path | Role |
|-----------|------|------|
| **Rolling baseline** | `data/latest/rolling-baseline.json` | 7-day observational means/std for context & z-scores |
| **FAIR metadata + citation** | `data/latest/fair-metadata.json`, `citation-bundle.json` | Findable, accessible, interoperable, reusable daily package |
| **Data dictionary** | `docs/data-dictionary.json`, `docs/DATA_DICTIONARY.md` | Variable definitions, units, product roles |

---

## Layers at a glance

| Layer | UOGW provides |
|-------|----------------|
| **Ground** | Casey archive, global city obs, GHCN index, foreign registry |
| **Marine** | NDBC station index + parsed realtime samples |
| **Upper-air** | IGRA station + Y2D indexes |
| **Stratosphere** | Catalog links (SWOOSH, WOUDC, SHADOZ, QBO) |
| **Satellite** | Open radiance / product discovery index |
| **Flight** | MSDS X2Griffon packages |
| **Analytics** | Anomalies, baselines, research summaries |

Full dataset table: see prior catalog section in git history or [`catalog/catalog.json`](./catalog/catalog.json).

---

## Honest scope

| We do | We do not |
|-------|-----------|
| Commit daily observation payloads + research summaries | Claim to be the global system of record |
| Screen anomalies for research context | Issue official public weather warnings |
| Index open satellite radiance product families | Host full GOES/JPSS radiance archives in git |
| Publish FAIR metadata and a data dictionary | Hide upstream licenses or provenance |
| Include foreign open authorities | Mirror every national archive in bulk |

---

## Documentation

| Doc | Link |
|-----|------|
| Project wiki home | [`docs/Home.md`](./docs/Home.md) |
| Data dictionary | [`docs/DATA_DICTIONARY.md`](./docs/DATA_DICTIONARY.md) |
| Science contributing guide | [`docs/CONTRIBUTING_SCIENCE.md`](./docs/CONTRIBUTING_SCIENCE.md) |
| Actual data README | [`data/README.md`](./data/README.md) |
| Machine catalog | [`catalog/catalog.json`](./catalog/catalog.json) |
| Source registry | [`sources/registry.json`](./sources/registry.json) |

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always also cite upstream providers (Open-Meteo, NOAA NDBC, NOAA NCEI, NASA, etc.). Daily packages include a `citation-bundle.json`.

---

## Contact

**Midwest Stratospheric Data Systems**  
Casey, Illinois, USA  
launchcontrol@midwestsds.com  
https://www.midwestsds.com  

NASA GLOBE: **GO-4VW9B** · Ham: **KE9CFY**

---

*Open atmosphere. Daily packages. Research-ready. Midwest-made flight data for everyone.*
