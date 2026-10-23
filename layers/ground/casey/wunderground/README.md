# Casey weather station KILCASEY47 (Weather Underground)

Fixed personal weather station **KILCASEY47** operated by Aerostratospheric at the Casey, Illinois ground station. Dashboard: https://www.wunderground.com/dashboard/pws/KILCASEY47

| File | Description |
|------|-------------|
| `latest.json` | Latest collection: current conditions and the day's observations (about every 5 minutes) |
| `hourly_2026-09-21_2026-10-22.csv` | Hourly aggregates (count, mean/min/max) of temperature, dew point, humidity, wind, gust, pressure, precipitation total, UV and solar, local time (America/Chicago) |
| `../summary/daily_2026-09-16_2026-10-22.csv` | Combined daily summary with the radiation and lightning columns |

Units are US customary (°F, mph, inHg, in, W/m²). Hours or days with missing observations show a smaller `n` or `wu_obs_count` (2026-09-22, 2026-10-05 and 2026-10-12 are partial days).

Source: Weather Underground / The Weather Company PWS observations from the Aerostratospheric station (KILCASEY47). Data retrieved through the Weather Underground API is not licensed by us while the WU API terms are reviewed, matching the note in the repository README. Please credit "Aerostratospheric Fixed Weather Station KILCASEY47" if you use it.
