# Data Types

What UOGW indexes and samples, and how fields are typically expressed.

| Type | Typical variables | Common units | Layers |
|------|-------------------|--------------|--------|
| **Surface meteorology** | temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m, wind_direction_10m, pressure_msl | °C, %, mm, m/s, °, hPa | ground |
| **Station inventory** | station id, name, lat, lon, country, elevation | degrees, m | ground, upper-air, marine |
| **Sounding / profile** | pressure levels, height, temperature, dewpoint, wind u/v | hPa, m, °C, m/s | upper-air, flight |
| **Marine** | wave height, water temperature, air temperature, wind, pressure | m, °C, m/s, hPa | marine |
| **Ozone / stratospheric** | total ozone, ozone profile, water vapor mixing ratio | DU, ppmv | stratospheric |
| **Satellite / RO** | brightness temperature, refractivity, bending angle | K, N-units | satellite |
| **Reanalysis** | gridded T, humidity, wind, height on model levels | various | satellite / model |
| **Status / health** | ok, generated_at_utc, counts, error | ISO-8601 | `status/` |

## City samples

Daily worldwide city snapshots use **Open-Meteo** current conditions (CC BY 4.0). When republishing, cite Open-Meteo and the underlying NWP sources.

Files:

- `layers/ground/samples/cities-latest.json`
- `layers/ground/samples/cities-YYYY-MM-DD.json`
