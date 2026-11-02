# Space weather layer

Near-real-time space environment data from the **NOAA Space Weather Prediction Center (SWPC)**, https://www.swpc.noaa.gov/.
**License:** US Government work, public domain in the US. Credit: NOAA Space Weather Prediction Center.
**Script:** `scripts/fetch_swpc_space_weather.py` · **Cadence:** Daily at 11:40 UTC (5:40 AM CST) via `.github/workflows/open-sources-daily.yml`; one dated file per UTC day plus `latest.*`.

| Folder | Source endpoint | Fields (units) |
|---|---|---|
| `kp-index/` | `products/noaa-planetary-k-index.json` (last ~7 days, 3-hourly) | `time_tag` (UTC), `Kp` (0–9), `a_running` (nT-equivalent ap), `station_count` |
| `solar-wind/` | `json/rtsw/rtsw_wind_1m.json` + `rtsw_mag_1m.json` (active spacecraft, 1-min, ~1 day) | `proton_speed_km_s` (km/s), `proton_density_cm3` (p/cm³), `proton_temperature_K` (K), `bt_nT`, `bz_gsm_nT`, `by_gsm_nT` (nT) |
| `xray-flux/` | `json/goes/primary/xrays-1-day.json` (GOES primary, 1-min) | `time_tag` (UTC), `satellite`, `energy` (0.05-0.4nm / 0.1-0.8nm), `flux_W_m2` (W/m²) |
| `f107-solar-flux/` | `json/f107_cm_flux.json` | `time_tag` (UTC), `flux_sfu` (solar flux units), `frequency_MHz` (2800), `reporting_schedule` |
| `geomagnetic-summary/` | `products/noaa-scales.json` + `text/3-day-forecast.txt` | NOAA R/S/G scale levels (current, predicted) and the SWPC 3-day Kp / aurora-relevant geomagnetic forecast text |

Values are passed through unchanged except for column renames shown above. Missing values are empty.
