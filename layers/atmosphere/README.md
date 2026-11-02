# Atmosphere layer (UV and ozone)

## `uv-index/casey/` — UV index forecast
**Source:** EPA Envirofacts UV Index hourly forecast for ZIP 62420 (Casey, IL), produced by the NOAA Climate Prediction Center with EPA. `https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/ZIP/62420/JSON`
**License:** US Government work, public domain. Credit: NOAA CPC / US EPA.
**Fields:** `local_time` (America/Chicago), `city`, `state`, `uv_index` (WHO UV index, unitless). Forecast for the current day.

## `ozone/{casey,birds}/` — modeled surface ozone and air quality
**Source:** Open-Meteo Air Quality API (CAMS global model). `https://air-quality-api.open-meteo.com/v1/air-quality`
**License:** CC BY 4.0. Credit: "Air quality data by Open-Meteo.com", generated using Copernicus Atmosphere Monitoring Service information.
**Fields:** `local_time`; `ozone`, `nitrogen_dioxide`, `pm2_5` (μg/m³); `uv_index`, `uv_index_clear_sky` (unitless). 2 past days + 3 forecast days, hourly. Model output, not measurements.

**Scripts:** `scripts/fetch_uv_ozone.py` · **Cadence:** Daily at 11:40 UTC (5:40 AM CST) via `.github/workflows/open-sources-daily.yml`; one dated file per UTC day plus `latest.*`.
