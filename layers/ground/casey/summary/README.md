# Casey ground station daily summary

One row per local day (America/Chicago) combining the Casey ground station streams. Empty cells mean that stream has no data for that day.

| Column group | Source | Notes |
|--------------|--------|-------|
| `wu_*`, `temp_f_*`, `humidity_pct_*`, `wind_*`, `pressure_in_*`, `precip_total_in`, `uv_max`, `solar_wm2_max` | Weather station KILCASEY47 | min / max / mean over the day's observations; `precip_total_in` is the day's accumulated precipitation; `wu_hours_covered` is the number of local hours with observations |
| `gmc800_*` | GMC-800 radiation (`../gmc-800/compilation/`) | CPM and µSv/h mean/max, `gmc800_n` samples. The radiation feed has no samples after 2026-10-09 |
| `lightning_strikes_logged`, `lightning_closest_mi` | Lightning detector (`../lightning/`) | Stream began 2026-10-22 |

Files are named with the first and last date they cover. Licensing: the `gmc800_*` and `lightning_*` columns are Aerostratospheric first-party data, CC BY 4.0, attribution: Aerostratospheric (midwestsds.com). For the weather-station columns, licence: not yet specified for this layer; credit Aerostratospheric Fixed Weather Station KILCASEY47.

Station data is provided to NOAA through the Citizen Weather Observer Program (CWOP) via KE9CFY.
