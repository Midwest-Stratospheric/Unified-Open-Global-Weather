# Data Catalog

Machine-readable source of truth: [`catalog/catalog.json`](../catalog/catalog.json)

## All datasets

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
| `qbo` | stratospheric | Quasi-Biennial Oscillation | catalog |
| `woudc-ozone` | stratospheric | WOUDC Ozone Sonde / Total Ozone Network | catalog |
| `shadoz` | stratospheric | SHADOZ Southern Hemisphere Additional Ozonesondes | catalog |
| `merra2` | satellite | NASA MERRA-2 Reanalysis | catalog |
| `goes-open` | satellite | NOAA GOES Open Data | catalog |
| `cosmic-ro` | satellite | COSMIC / GNSS Radio Occultation | catalog |
| `arm` | ground | DOE Atmospheric Radiation Measurement (ARM) | catalog |
| `ecmwf-open` | satellite | ECMWF / Copernicus Open Datasets | catalog |

### Status meanings

- **active daily** — GitHub Action writes fresh files under `layers/` every day
- **active** — used live on the Data Hub or updated regularly
- **catalog** — fully described with authority URLs; bulk data remains at the source

## Related files

- [`sources/registry.json`](../sources/registry.json) — US + foreign authority registry
- [`status/last_update.json`](../status/last_update.json) — rollup health
