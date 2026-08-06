# Data vs live telemetry

UOGW mixes several **different kinds of data**. They are not interchangeable.

| Class | What it is | Examples on UOGW / hub | Live packet stream? |
|-------|------------|-------------------------|---------------------|
| **Live telemetry** | Packets from a vehicle or instrument in flight | MSDS X2Griffon APRS / WSPR / GPS when a flight is active | Yes, during flight only |
| **Near-real-time products** | Operational sensors republished on short delay | NOAA SWPC Kp, GOES X-rays | No (product feed) |
| **In-situ archive observations** | Logged station reports after the fact | Illinois radiosonde 3-day counts (IEM/RAOB), NDBC samples | No |
| **NWP model forecast** | Predicted atmosphere on a grid | NOAA GFS via Open-Meteo or NOMADS GRIB2 | No |
| **Research composites** | Derived scores from models/obs | Pre-tornado Clark County score, anomaly flags | No |

## NOAA GFS

- **Authoritative distribution:** [NCEP NOMADS](https://nomads.ncep.noaa.gov/) GFS cycles (GRIB2).
- **Hub convenience subset:** Open-Meteo `gfs_seamless` for Casey charts.
- GFS is a **forecast model**, not a radiosonde and not MSDS balloon telemetry.

## Radiosondes

- Launch times in the Illinois count product are **archive schedule/valid times**.
- “Devices likely aloft” is a **time-window estimate** (~2 h after launch), not a tracked GPS path for each balloon.

## MSDS flights

When X2Griffon is flying, live positions come from the flight trackers (APRS/WSPR/etc.). Those streams are separate from GFS, SWPC, and daily archive indexes.
