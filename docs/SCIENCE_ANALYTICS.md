# UOGW Science Analytics

Daily derived analytics for research and the MSDS Data Hub UI.

## Output

| Path | Role |
|------|------|
| `data/latest/science-analytics.json` | Stable hub/research endpoint |
| `data/entries/YYYY-MM-DD/science-analytics.json` | Dated archive |
| `status/science-analytics.json` | Ops health |

## Contents

- Coverage counts (cities, Casey hours, NDBC, anomalies)
- Surface stats in **°C and °F** (temp, humidity, pressure, wind)
- Marine wave / water / air stats
- Hottest / coldest sample cities
- Research heat-index flags (NOAA-style approximation, °F)
- Anomaly count digest + top events
- Hub highlight cards for UI

## Automation

`science-analytics-daily.yml`

- 09:45 and 12:15 UTC
- Also after Research Package, Anomaly, Global Samples, or Charts succeed

## Hub

https://midwestsds.com/msds-data-hub.html loads `science-analytics.json` for the analytics panel.
