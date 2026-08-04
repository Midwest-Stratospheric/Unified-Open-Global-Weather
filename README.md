# Unified Open Global Weather (UOGW)

**An open atmospheric data commons — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://www.midwestsds.com/portal.html)
[![Catalog](https://img.shields.io/badge/catalog-24%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Automations](https://img.shields.io/badge/automations-GitHub%20Actions-success)](./.github/workflows/)

> **Mission:** Build the most complete *open, multi-layer, versioned* discovery layer for global ground, marine, upper-air, stratospheric, satellite, and near-space atmospheric observations — with independent automation, full attribution, and a public Data Hub.

---

## Why UOGW is different

Most weather portals are **single-agency** or **model-only**. UOGW is a **commons**:

| Layer | What you get |
|-------|----------------|
| **Ground** | MSDS Casey daily archive · NASA GLOBE · GHCNd · ASOS/METAR discovery · Open-Meteo · ARM · NASA POWER |
| **Marine** | NDBC buoy indexes · Argo · ICOADS · CO-OPS tides |
| **Upper-air** | NOAA IGRA daily indexes · GRUAN · CUON · UW soundings |
| **Stratosphere** | SWOOSH · QBO · WOUDC ozone · SHADOZ |
| **Satellite** | GOES open data · MERRA-2 · COSMIC RO · ECMWF open |
| **Flight** | MSDS X2Griffon HAB packages (first-party vertical profiles) |

**We fly instruments.** That is rare among open-data curators. When X2Griffon recovers, profiles enter the same commons as IGRA and NDBC — not a private vault.

### Independence

Automations run on **GitHub Actions** inside this repository. They do **not** depend on the midwestsds.com web host being up. If the website is offline, indexes and MSDS ground files still update.

---

## Honest scope

| We do | We do not |
|-------|-----------|
| Index 20+ major open global sources | Claim ownership of NOAA/NASA/ECMWF observations |
| Snapshot station lists & directory indexes daily | Host multi-TB bulk archives |
| Publish Midwest HAB + Casey ground fast | Require API keys for basic public use |
| Keep full citation chains | Mirror proprietary commercial PWS networks |
| Version everything in Git | Pretend one small org replaces NCEI |

Agencies remain the **system of record**. UOGW is the **open discovery + MSDS contribution pipeline**.

---

## Quick links

| Resource | URL |
|----------|-----|
| **This repository** | https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather |
| **Data Hub** | https://www.midwestsds.com/portal.html |
| **API catalog** | https://midwestsds.com/data/v1/catalog.json |
| **MSDS flight & ground data** | https://github.com/Midwest-Stratospheric/msds-data |
| **IGDR (upper-air)** | https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository |
| **Machine catalog** | [`catalog/catalog.json`](./catalog/catalog.json) |
| **Source registry** | [`sources/registry.json`](./sources/registry.json) |
| **Live status** | [`status/last_update.json`](./status/last_update.json) |

---

## Repository layout

```
├── catalog/catalog.json
├── sources/registry.json
├── layers/
│   ├── ground/
│   ├── marine/ndbc/
│   ├── upper-air/igra/
│   ├── stratospheric/
│   ├── satellite/
│   └── flight/
├── snapshots/YYYY-MM-DD/
├── status/
├── .github/workflows/
└── docs/
```

---

## Automations (independent)

| Workflow | Schedule | Output |
|----------|----------|--------|
| `msds-ground-daily.yml` | Daily | Casey ground JSON → **msds-data** repo |
| `igra-index-daily.yml` | Daily | IGRA Y2D file index → `layers/upper-air/igra/` |
| `ndbc-marine-daily.yml` | Daily | NDBC station table → `layers/marine/ndbc/` |
| `catalog-rebuild.yml` | Daily + on push | `status/last_update.json` |

Optional secret: `MSDS_DATA_TOKEN` (PAT with write access to `msds-data`) for cross-repo ground commits.

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always also cite original providers (IGRA, Open-Meteo, GLOBE, NDBC, etc.).

---

## Contact

**Midwest Stratospheric Data Systems**  
Casey, Illinois, USA  
launchcontrol@midwestsds.com  
https://www.midwestsds.com  

NASA GLOBE: **GO-4VW9B** · Ham context: **KE9CFY**

---

*Open atmosphere. Open archives. Midwest-made flight data for everyone.*
