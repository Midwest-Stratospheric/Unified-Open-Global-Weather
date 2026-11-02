# Regional ground observations (near Casey and Birds, IL)

## `nws/` — NOAA/NWS ASOS surface observations
**Source:** National Weather Service API, `https://api.weather.gov/stations/{id}/observations` · **License:** US Government work, public domain. Credit: NOAA National Weather Service.
**Stations:** KMTO (Mattoon/Charleston, IL), KLWV (Lawrenceville, IL), KHUF (Terre Haute, IN). Latest 100 observations per run.
**Script:** `scripts/fetch_nws_observations.py` · **Cadence:** Daily at 11:40 UTC (5:40 AM CST) via `.github/workflows/open-sources-daily.yml`; one dated file per UTC day plus `latest.*`.
**Fields:** `timestamp_utc`, `text`, `temperature_C` (°C), `dewpoint_C` (°C), `relative_humidity_pct` (%), `wind_direction_deg` (°), `wind_speed_km_h`, `wind_gust_km_h` (km/h), `pressure_Pa`, `sea_level_pressure_Pa` (Pa), `visibility_m` (m), `precip_last_hour_mm` (mm). Raw NWS values, not QC-adjusted.

## `open-meteo/` — Open-Meteo historical archive (reanalysis)
**Source:** https://open-meteo.com/ Historical Weather API (ERA5 / ERA5-Land based) · **License:** CC BY 4.0. Credit: "Weather data by Open-Meteo.com" (contains modified Copernicus Climate Change Service information).
**Sites:** `casey/` (39.299, -87.992), `birds/` (38.840, -87.667), city-level coordinates.
**File:** `daily-last-60d.csv` — rolling 60 days ending 6 days before run (archive lag). Model reanalysis, not station observations.
**Script:** `scripts/fetch_openmeteo_archive.py` · **Cadence:** daily (file overwritten).
**Fields:** `date` (local, America/Chicago); temperature max/min/mean (°C); precipitation, rain (mm); snowfall (cm); wind speed / gusts max (km/h); dominant wind direction (°); shortwave radiation sum (MJ/m²); ET0 (mm). Units are in each column header.
