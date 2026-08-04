# Unified Open Global Weather (UOGW)

**An open atmospheric data commons — curated by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Hub](https://img.shields.io/badge/Data%20Hub-midwestsds.com-00d4ff)](https://www.midwestsds.com/portal.html)
[![Catalog](https://img.shields.io/badge/catalog-25%2B%20datasets-0a1628)](./catalog/catalog.json)
[![Automations](https://img.shields.io/badge/automations-GitHub%20Actions-success)](./.github/workflows/)
[![Coverage](https://img.shields.io/badge/coverage-global%20%2B%20foreign-blue)](./layers/ground/international/)
[![Wiki](https://img.shields.io/badge/wiki-docs%2F-0a1628)](./docs/Home.md)

> **Mission:** Build one of the most complete *open, multi-layer, versioned* discovery layers for global ground, marine, upper-air, stratospheric, satellite, and near-space atmospheric observations — with independent automation, full attribution, international sources, and a public Data Hub.

**Project wiki:** [`docs/Home.md`](./docs/Home.md) — catalog, data types, layers, international coverage, automations, API/status, citation.

---

## Why UOGW is different

Most weather portals are **single-agency** or **model-only**. UOGW is a **commons** spanning six layers, US and foreign authorities, and first-party near-space flight data.

**We fly instruments.** That is rare among open-data curators. When X2Griffon recovers, profiles enter the same commons as IGRA and NDBC — not a private vault.

### Independence

Automations run on **GitHub Actions** inside this repository. They do **not** depend on the midwestsds.com web host being up. If the website is offline, indexes and MSDS ground files still update.

---

## Comprehensive data list

### By layer

| Layer | Data types | What UOGW provides |
|-------|------------|--------------------|
| **Ground** | Surface temperature, humidity, precip, wind, pressure, citizen science | Station indexes, daily city samples (30+ global cities), Casey IL archive, source registry |
| **Marine** | Buoy observations, ocean profiles, tides, ship reports | NDBC station indexes + sample obs, links to Argo / ICOADS / CO-OPS |
| **Upper-air** | Radiosonde soundings, pilot balloons, reference networks | IGRA station + Y2D file indexes (~2,900 stations), links to GRUAN / CUON / UW |
| **Stratosphere** | Ozone, water vapor, QBO winds | Catalog links to SWOOSH, WOUDC, SHADOZ, QBO products |
| **Satellite** | Imagery products, reanalysis, radio occultation | Catalog links to GOES open, MERRA-2, COSMIC, Copernicus/ECMWF |
| **Flight** | High-altitude balloon vertical profiles | MSDS X2Griffon packages (first-party near-space) |

### Machine-readable catalog entries (`catalog/catalog.json`)

| ID | Layer | Title | Status |
|----|-------|-------|--------|
| `msds-ground-casey` | ground | Casey, Illinois Ground Weather (MSDS) | active daily |
| `msds-globe-site` | ground | NASA GLOBE — MSDS Site 422147 | active |
| `msds-flights` | flight | X2Griffon / MSDS High-Altitude Flight Packages | active / expanding |
| `noaa-igra` | upper-air | NOAA Integrated Global Radiosonde Archive (IGRA) | active daily index |
| `copernicus-cuon` | upper-air | Copernicus Comprehensive Upper-air Observation Network | catalog |
| `gruan` | upper-air | GRUAN Reference Upper-Air Network | catalog |
| `uwyo-soundings` | upper-air | University of Wyoming Atmospheric Soundings | catalog |
| `noaa-ghcnd` | ground | NOAA Global Historical Climatology Network daily (GHCNd) | active daily index |
| `iem-asos` | ground | Iowa Environmental Mesonet ASOS/METAR Archive | catalog |
| `open-meteo` | ground | Open-Meteo Open Weather API | active daily samples |
| `nasa-power` | ground | NASA POWER Agroclimatology / Meteorology | catalog |
| `cwop` | ground | Citizen Weather Observer Program (CWOP) | catalog |
| `ndbc-buoys` | marine | NOAA National Data Buoy Center (NDBC) | active daily index |
| `argo` | marine | Argo Global Ocean Profiling Float Array | catalog |
| `icoads` | marine | International Comprehensive Ocean-Atmosphere Data Set | catalog |
| `noaa-tides` | marine | NOAA CO-OPS Water Levels / Tide Gauges | catalog |
| `swoosh` | stratospheric | NASA SWOOSH Stratospheric Water and Ozone | catalog |
| `qbo` | stratospheric | Quasi-Biennial Oscillation (tropical stratospheric winds) | catalog |
| `woudc-ozone` | stratospheric | WOUDC Ozone Sonde / Total Ozone Network | catalog |
| `shadoz` | stratospheric | SHADOZ Southern Hemisphere Additional Ozonesondes | catalog |
| `merra2` | satellite | NASA MERRA-2 Reanalysis (open products) | catalog |
| `goes-open` | satellite | NOAA GOES Open Data (ABI / products) | catalog |
| `cosmic-ro` | satellite | COSMIC / GNSS Radio Occultation | catalog |
| `arm` | ground | DOE Atmospheric Radiation Measurement (ARM) | catalog |
| `ecmwf-open` | satellite | ECMWF / Copernicus Open Datasets (selected) | catalog |

**Status key**
- **active daily** — GitHub Action writes fresh files into `layers/` every day  
- **active** — live or regularly used in the Data Hub  
- **catalog** — fully described in the machine catalog with authority URLs; bulk data stays at the source  

---

## Data types (what variables mean)

| Type | Typical variables | Units (common) | Layers |
|------|-------------------|----------------|--------|
| **Surface meteorology** | temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m, wind_direction_10m, pressure_msl | °C, %, mm, m/s, °, hPa | ground |
| **Station inventory** | station id, name, lat, lon, country/elevation | degrees, m | ground, upper-air, marine |
| **Sounding / profile** | pressure levels, geopotential height, temp, dewpoint, wind u/v | hPa, m, °C, m/s | upper-air, flight |
| **Marine** | wave height, water temp, air temp, wind, pressure | m, °C, m/s, hPa | marine |
| **Ozone / stratospheric** | total ozone, ozone profile, water vapor mixing ratio | DU, ppmv | stratospheric |
| **Satellite / RO** | brightness temperature, refractivity, bending angle | K, N-units | satellite |
| **Reanalysis** | gridded T, q, wind, height on model levels | various | satellite / model |
| **Status / health** | ok, generated_at_utc, counts, error | ISO-8601 timestamps | status/ |

Daily **city samples** use Open-Meteo current conditions (CC BY 4.0). Always cite Open-Meteo and underlying NWP sources when republishing.

---

## International & foreign coverage

UOGW is not US-only. Indexes and samples intentionally include foreign and international networks.

### Daily worldwide city samples (`layers/ground/samples/`)

Surface snapshots for **30+ cities** across:

| Region | Examples |
|--------|----------|
| North America | Casey IL, Chicago, Houston, Toronto, Mexico City, Honolulu, Anchorage |
| South America | São Paulo, Buenos Aires, Lima |
| Europe | London, Paris, Berlin, Madrid, Rome, Oslo, Stockholm, Reykjavik, Moscow, Istanbul |
| Africa | Cairo, Nairobi, Johannesburg, Lagos |
| Middle East | Dubai |
| Asia | Mumbai, Beijing, Tokyo, Seoul, Singapore, Bangkok, Jakarta |
| Oceania | Sydney, Auckland |

### Global station index — GHCN (`layers/ground/ghcn/`)

NOAA **GHCNd** station inventory is global (US + foreign). UOGW stores daily **counts by country**, top-country summaries, and sample stations — with a pointer to the full NOAA list for complete inventory.

### Foreign / international open authorities (`layers/ground/international/`)

Curated registry includes (non-exhaustive):

| Source | Country / scope |
|--------|-----------------|
| Deutscher Wetterdienst (DWD) Open Data | Germany / Europe |
| MET Norway / Yr | Norway / Nordic / API |
| Environment and Climate Change Canada | Canada |
| Bureau of Meteorology | Australia |
| Japan Meteorological Agency | Japan |
| Météo-France Open Data | France |
| KNMI | Netherlands |
| SMHI | Sweden |
| UK Met Office | United Kingdom |
| India Meteorological Department | India |
| China Meteorological Administration | China |
| South African Weather Service | South Africa |
| INMET | Brazil |
| WMO OSCAR | Global observing systems |
| WOUDC | Global ozone |
| Argo | Global ocean |
| Copernicus Climate Data Store | EU / global |
| Open-Meteo | Global |

Full machine list: [`sources/registry.json`](./sources/registry.json).

---

## Honest scope

| We do | We do not |
|-------|-----------|
| Index 25+ major open global sources | Claim ownership of NOAA/NASA/ECMWF/DWD observations |
| Snapshot station lists & directory indexes daily | Host multi-TB bulk archives |
| Publish Midwest HAB + Casey ground fast | Require API keys for basic public use |
| Include foreign met services in the registry | Mirror every national archive in full |
| Keep full citation chains | Pretend one small org replaces NCEI or WMO |
| Version everything in Git | Guarantee second-by-second global completeness |

Agencies remain the **system of record**. UOGW is the **open discovery + MSDS contribution pipeline**.

---

## Quick links

| Resource | URL |
|----------|-----|
| **This repository** | https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather |
| **Project wiki** | [`docs/Home.md`](./docs/Home.md) |
| **Data Hub** | https://www.midwestsds.com/portal.html |
| **API catalog** | https://midwestsds.com/data/v1/catalog.json |
| **MSDS flight & ground data** | https://github.com/Midwest-Stratospheric/msds-data |
| **IGDR (upper-air)** | https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository |
| **Machine catalog** | [`catalog/catalog.json`](./catalog/catalog.json) |
| **Source registry** | [`sources/registry.json`](./sources/registry.json) |
| **Live status** | [`status/last_update.json`](./status/last_update.json) |
| **International sources** | [`layers/ground/international/sources-latest.json`](./layers/ground/international/sources-latest.json) |
| **Global city samples** | [`layers/ground/samples/cities-latest.json`](./layers/ground/samples/cities-latest.json) |

---

## Repository layout

```
├── catalog/catalog.json          # Master machine-readable dataset list
├── sources/registry.json         # US + foreign authority registry
├── docs/                         # Project wiki
├── layers/
│   ├── ground/
│   │   ├── casey/                # MSDS local ground
│   │   ├── samples/              # Worldwide city surface samples
│   │   ├── ghcn/                 # GHCNd global station index
│   │   └── international/        # Foreign open-source registry snapshots
│   ├── marine/ndbc/
│   ├── upper-air/igra/
│   ├── stratospheric/
│   ├── satellite/
│   └── flight/
├── snapshots/YYYY-MM-DD/
├── status/                       # Per-source health + last_update rollup
├── .github/workflows/
└── docs/
```

---

## Automations (independent)

| Workflow | Schedule | Output |
|----------|----------|--------|
| `msds-ground-daily.yml` | Daily | Casey ground JSON → msds-data + UOGW `layers/ground/casey/` |
| `igra-index-daily.yml` | Daily | IGRA station + Y2D index → `layers/upper-air/igra/` |
| `ndbc-marine-daily.yml` | Daily | NDBC station table → `layers/marine/ndbc/` |
| `global-samples-daily.yml` | Daily | 30+ worldwide city surface samples → `layers/ground/samples/` |
| `international-indexes-daily.yml` | Daily | GHCN country index + foreign source registry → `layers/ground/ghcn/` + `international/` |
| `catalog-rebuild.yml` | Daily + on data push | `status/last_update.json` rollup |

Optional secret: `MSDS_DATA_TOKEN` (PAT with write access to `msds-data`) for cross-repo ground commits.

---

## Citation

> Midwest Stratospheric Data Systems (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

Always also cite original providers (IGRA, Open-Meteo, GLOBE, NDBC, DWD, JMA, etc.).

---

## Contact

**Midwest Stratospheric Data Systems**  
Casey, Illinois, USA  
launchcontrol@midwestsds.com  
https://www.midwestsds.com  

NASA GLOBE: **GO-4VW9B** · Ham context: **KE9CFY**

---

*Open atmosphere. Open archives. Midwest-made flight data for everyone.*
