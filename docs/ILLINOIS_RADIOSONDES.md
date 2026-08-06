# Illinois radiosonde activity

Live research product counting NWS radiosonde launches for Illinois.

## Station

| ID | Name | Role |
|----|------|------|
| KILX | Lincoln, IL (ILX) | Primary NWS upper-air site in Illinois |

Typical schedule: **00Z** and **12Z** daily (sometimes special launches).

## Metrics

| Field | Meaning |
|-------|--------|
| `counts.launches_3_days` | Soundings with valid time in the last 72 hours |
| `counts.devices_likely_aloft` | Launches within the last ~2 hours (estimate only) |

## Source

Iowa Environmental Mesonet: `/api/1/raobs_by_year.json`

## Output

`data/latest/illinois-radiosonde-count.json`
