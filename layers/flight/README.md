# Flight layer (MSDS first-party)

High-altitude balloon packages from Midwest Stratospheric Data Systems / Aerostratospheric.

- Platform: **X2Griffon** (and successors)
- Target public release: **< 48 hours** after recovery
- Contents (planned): vertical profile (T/H/P/wind), track GeoJSON, summary, imagery index
- Storage: https://github.com/Midwest-Stratospheric/msds-data/tree/main/flights
- Live tracker archive: https://github.com/Midwest-Stratospheric/xliveflights-data

## xLiveFlights captures

When a tracked flight **closes** (tracker quiet or offline 60+ minutes), last-flight metrics are filed here as past-flight data:

- `xliveflights-captures.json` — rolling table of closed flights
- `xliveflights-captures-latest.json` — same file (stable latest alias)

A new row is appended for each closed flight id. Open / live motion is **not** written here. When the tracker moves again, the live page returns to live mode and this table stays as the past-flight record.
