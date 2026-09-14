# Casey X-Sense — internal building temperature average

Indoor air from the X-Sense thermo-hygrometer inside the MSDS operations building at Casey, IL.

This is **not** outdoor ground weather. Outdoor Casey observations stay in `casey-hourly.json` (Open-Meteo).

The published product is the **time-average** of 1-minute indoor samples:
- daily `building_average.temperature_f` / `temperature_c`
- hourly means in `observations[]` (`building_temperature_f`)

## Flow (git does the work)

1. X-Sense emails a CSV export (`support@x-sense-iot.com`).
2. Thin Grok Gmail trigger drops it in `raw/` and stops.
3. Action `Ingest X-Sense Ground` writes the building-average product.

```
layers/ground/casey/xsense/
  raw/YYYY-MM-DD.csv
  YYYY-MM-DD.json          # indoor hourly means + daily building average
  latest.json
data/entries/YYYY-MM-DD/casey-xsense.json
data/latest/casey-xsense.json
status/msds-xsense.json
```
