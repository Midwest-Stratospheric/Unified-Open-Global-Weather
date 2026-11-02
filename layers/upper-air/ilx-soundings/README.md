# Lincoln, IL (NWS ILX) radiosonde soundings

**Source:** NOAA NCEI Integrated Global Radiosonde Archive (IGRA v2.2), station `USM00074560`, year-to-date file `data-y2d/USM00074560-data-beg2026.txt.zip`. https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive
**License:** US Government work, public domain. Credit: NOAA NCEI IGRA (Durre et al.).
**Script:** `scripts/fetch_igra_ilx.py` · **Cadence:** daily (files overwritten). IGRA y2d typically lags a few days.

- `recent-soundings.csv` — every level of the latest 28 soundings (about two weeks of 00Z/12Z launches).
- `index.json` — retrieval time, source URL, soundings in archive, list of kept sounding times.

**Fields:** `sounding_time_utc`; `level_type` (IGRA LVLTYP1+2: 1x standard, 2x significant thermo, 3x wind-only; x1 surface, x0 other); `pressure_hPa`; `geopotential_height_m` (m); `temperature_C`; `relative_humidity_pct` (%); `dewpoint_depression_C`; `wind_direction_deg`; `wind_speed_m_s` (m/s). IGRA missing codes (-9999/-8888) are empty. Values are as archived by NCEI; quality flags are not reproduced.
