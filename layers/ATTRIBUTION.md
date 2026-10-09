# Attribution and licensing (UOGW)

UOGW, mirrored daily to the Hugging Face dataset `aerostratospheric/uogw`, mixes Aerostratospheric's own data with third-party data. Licensing is per source:

- **Aerostratospheric first-party data and documentation:** CC BY 4.0. See [`LICENSE`](./LICENSE).
- **Third-party data, and products derived from it:** each source keeps its own terms. Aerostratospheric does not relicense it. Cite the original provider.
- **Code** (scripts, workflows, other software): not licensed under CC BY 4.0.

This file covers `layers/`, plus the `data/` and `snapshots/` trees (daily copies and rollback copies of the same products), since Hugging Face mirrors all three.

## First-party data (CC BY 4.0)

Cite as: Aerostratospheric (2026). Unified Open Global Weather (UOGW). https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather

| Data | Paths |
|---|---|
| Casey GMC-800 radiation station (CPM, µSv/h) | `layers/ground/casey/gmc-800/` |
| Casey X-Sense indoor temperature/humidity logger | `layers/ground/casey/xsense/`, `data/latest/casey-xsense.json`, `data/latest/summary-xsense.json`, matching `snapshots/` copies |
| Aerostratospheric balloon flight products and xLiveFlights closed-flight captures (place names city level only) | `layers/flight/` |
| Index of links to open weather authorities (URLs only) | `layers/ground/international/` |
| Documentation (`README.md` files, `docs/`) | — |

## Excluded: KILCASEY47 (Weather Underground API data)

`layers/ground/casey/wunderground/`, `data/latest/casey-wu.json` and `snapshots/rollback-points/*/casey-wu.json` hold observations from Aerostratospheric's station **KILCASEY47**, retrieved through the Weather Underground / The Weather Company API.

- **Not licensed:** they are **not** licensed under CC BY 4.0 or any other license from Aerostratospheric while the Weather Underground API terms are reviewed (https://www.wunderground.com/company/legal).
- **No longer republished:** they are no longer added to new snapshots.

## Third-party sources (their own terms apply)

| Source | Where it appears | Terms | Attribution |
|---|---|---|---|
| **Open-Meteo** weather API (model data, including Casey, Illinois model series and GFS-seamless fields) | `layers/ground/casey/daily/`, `layers/ground/casey/latest.json`, `layers/ground/samples/`, `data/latest/casey-hourly.json`, `data/*/global-cities.json`, `data/*/space-gfs-snapshot.json` (Casey fields) | **CC BY 4.0**: https://open-meteo.com/en/license | "Weather data by Open-Meteo.com, CC BY 4.0." The Casey series is model data, **not** observations from an Aerostratospheric station. |
| **Copernicus Atmosphere Monitoring Service (CAMS)**, via the Open-Meteo Air Quality API | `data/*/ozone-health.json`, matching `snapshots/` copies | **Copernicus licence**: https://apps.ecmwf.int/datasets/licences/copernicus/ (API: https://open-meteo.com/en/docs/air-quality-api) | "Contains modified Copernicus Atmosphere Monitoring Service information [year]", plus Open-Meteo |
| **NOAA National Weather Service** (KMTO ASOS surface station, alerts, SPC) | `layers/ground/casey/external/`, `layers/ground/casey/internal-external.json` (external part), `surface_observation` in `layers/flight/*.json`, `data/latest/casey-external.json` | U.S. government data, public domain: https://www.weather.gov/disclaimer | NOAA National Weather Service |
| **NOAA NCEI: GHCN-Daily** (station index) | `layers/ground/ghcn/`, `data/` and `snapshots/` copies | NOAA open data. Some non-U.S. station data carry WMO Resolution 40 limits: https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily | NOAA NCEI GHCN-Daily |
| **NOAA NCEI: IGRA** (radiosonde index) | `layers/upper-air/igra/`, `data/*/igra-index.json`, `snapshots/` copies | NOAA open data: https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive | NOAA NCEI IGRA v2 |
| **NOAA National Data Buoy Center** | `layers/marine/ndbc/`, `data/*/ndbc-realtime.json`, `data/*/marine-snapshot.json`, `snapshots/` copies | U.S. government data, public domain: https://www.weather.gov/disclaimer (NDBC's disclaimer page redirects there) | NOAA NDBC |
| **NOAA Space Weather Prediction Center** (Kp, GOES X-ray) | `data/*/space-gfs-snapshot.json`, `snapshots/` copies | U.S. government data, public domain: https://www.swpc.noaa.gov/ and https://www.weather.gov/disclaimer | NOAA SWPC |
| **NOAA NCEP GFS** via NOMADS | `data/*/space-gfs-snapshot.json`, `snapshots/` copies | U.S. government data, public domain: https://nomads.ncep.noaa.gov/ | NOAA NCEP |
| **Iowa Environmental Mesonet, Iowa State University** (NWS radiosonde launch counts) | `layers/upper-air/illinois-radiosonde-count-latest.json`, `data/*/illinois-radiosonde-count.json`, `snapshots/` copies | Per IEM terms: https://mesonet.agron.iastate.edu/disclaimer.php | Iowa Environmental Mesonet, Iowa State University |
| **NOAA and NASA satellite catalogs** (GOES, JPSS, MERRA-2, COSMIC; product names and paths only, no imagery) | `layers/satellite/`, `data/*/satellite-radiance-index.json`, `snapshots/` copies | https://registry.opendata.aws/noaa-goes/ · https://registry.opendata.aws/noaa-jpss/ · https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance | NOAA NESDIS / NASA |

## Derived products

The following are Aerostratospheric computations on the third-party inputs above, mainly Open-Meteo and NOAA:

- `layers/analytics/`, `layers/hazards/` and `layers/research/`
- in `data/`: the anomaly, baseline, science-analytics, science-package, pre-tornado, heat-humidity, pressure-wind and summary files
- their `snapshots/` copies

Our methods and structure are CC BY 4.0. The underlying values stay under the source terms above, so cite those providers as well.
