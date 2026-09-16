# Ground layer

Surface land observations, citizen science, and first-party Casey site products — including **surface ionizing radiation**.

- **MSDS Casey daily meteorology** — published to `msds-data` (see automation)
- **Casey GMC-800 radiation** — fixed-site CPM / µSv/h from a GQ GMC-800 at 39.2974 N, −87.9818 W → [`layers/ground/casey/gmc-800/`](./casey/gmc-800/)
- **Casey X-Sense / external** — indoor building average and outdoor KMTO/NWS pairing under `layers/ground/casey/`
- **NASA GLOBE** — MSDS site 422147
- **GHCNd, IEM ASOS, Open-Meteo, ARM, NASA POWER, CWOP** — registry + catalog entries

Radiation data on this layer is **in-situ surface dose rate** (background monitoring), not a flight payload and not a health-alert service. Catalog id: `msds-gmc800-casey`.

First-party automated meteorology also lives in the companion repo:
https://github.com/Midwest-Stratospheric/msds-data/tree/main/ground-weather
