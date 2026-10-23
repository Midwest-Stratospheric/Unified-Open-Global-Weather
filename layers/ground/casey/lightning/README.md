# Casey lightning detector (Ecowitt gateway)

First-party **nearby lightning** observations from an Ecowitt gateway with a lightning sensor at the Aerostratospheric fixed station in Casey, Illinois.

## What is recorded

| Field | Meaning |
|-------|---------|
| `last_strike_distance_mi` / `_km` | Distance of the most recent strike as estimated by the sensor (mi from the gateway, km converted) |
| `last_strike_utc` / `_local` | Time of the most recent strike (local = America/Chicago) |
| `daily_count` | Strikes counted today (resets at local midnight) |
| `daily_min_distance_mi`, `one_hour_min_distance_mi` | Closest strike today / in the last hour |
| `pressure` | Gateway barometer (relative and absolute, inHg; hPa converted) |

The sensor reports counts and distance only. It does not report strike energy or bearing. The gateway reports no temperature or humidity.

## Files

| File | Role |
|------|------|
| `station.json` | Site and instrument metadata |
| `latest.json` | Latest reading |
| `events.csv` | Strike log: one row each time the last-strike time changes (strikes between polls can be missed) |

## Dedicated dataset

This stream also has its own Hugging Face dataset with a full dataset card: https://huggingface.co/datasets/aerostratospheric/casey-lightning

## Source and license

Data: Aerostratospheric. CC BY 4.0, attribution "Aerostratospheric (midwestsds.com)". Live panel: https://www.midwestsds.com/msds-data-hub.html#lightning
