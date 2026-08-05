# UOGW Data Dictionary

Machine-readable twin: [`data-dictionary.json`](./data-dictionary.json)

## Core variables

| ID | Name | Units | Layers |
|----|------|-------|--------|
| `temperature_c` | Air temperature | °C | ground, marine, flight |
| `relative_humidity_pct` | Relative humidity | % | ground |
| `precipitation_mm` | Precipitation | mm | ground |
| `pressure_msl_hpa` | MSL pressure | hPa | ground, marine |
| `wind_speed_ms` | Wind speed | m/s | ground, marine, flight |
| `wind_direction_deg` | Wind direction | ° | ground, marine |
| `wave_height_m` | Significant wave height | m | marine |
| `water_temp_c` | Water temperature | °C | marine |
| `et0_mm` | FAO-56 ET0 | mm | ground |
| `shortwave_radiation_mj_m2` | Shortwave radiation sum | MJ/m² | ground |
| `temperature_c_zscore` | Temp z-score vs baseline | 1 | analytics |

## Primary research products

| Path | Role |
|------|------|
| `data/latest/science-package.json` | Primary daily research package |
| `data/latest/research-summary.json` | Multi-source generalized summary |
| `data/latest/anomaly-report.json` | Automated anomaly screening |
| `data/latest/rolling-baseline.json` | 7-day observational baseline |
| `data/latest/satellite-radiance-index.json` | Open satellite radiance index |
| `data/latest/fair-metadata.json` | FAIR-aligned daily metadata |
