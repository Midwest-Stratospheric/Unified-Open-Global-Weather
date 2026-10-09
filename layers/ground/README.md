# Ground layer

Surface land observations, citizen science, Casey site products — including first-party **surface ionizing radiation** — and Open-Meteo model data.

- **Casey, Illinois daily/hourly weather (Open-Meteo model data)** — `layers/ground/casey/daily/` and `layers/ground/casey/latest.json`, also copied to `msds-data`. This is model data for the Casey grid point, **not** observations from our station. Weather data by Open-Meteo.com, CC BY 4.0.
- **Casey GMC-800 radiation** — fixed-site CPM / µSv/h from a GQ GMC-800 at 39.2974 N, −87.9818 W → [`layers/ground/casey/gmc-800/`](./casey/gmc-800/)
- **Casey X-Sense / external** — indoor building average and outdoor KMTO/NWS pairing under `layers/ground/casey/`
- **NASA GLOBE** — MSDS site 422147
- **GHCNd, IEM ASOS, Open-Meteo, ARM, NASA POWER, CWOP** — registry + catalog entries

Radiation data on this layer is **in-situ surface dose rate** (background monitoring), not a flight payload and not a health-alert service. Catalog id: `msds-gmc800-casey`.

First-party automated meteorology also lives in the companion repo:
https://github.com/Midwest-Stratospheric/msds-data/tree/main/ground-weather
