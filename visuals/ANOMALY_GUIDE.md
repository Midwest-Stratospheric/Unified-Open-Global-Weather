# Anomaly detection guide (next to the graph)

This page sits with the daily **Anomaly severity** chart in [`latest/CHARTS.md`](./latest/CHARTS.md).

## What the graph means

The anomaly chart counts **research flags** for the current daily sample set — not National Weather Service warnings.

| Severity | Meaning |
|----------|---------|
| **Alert** | Strong outlier vs absolute thresholds or baseline (e.g. extreme heat/cold, \|z\| ≥ 3, very high waves). |
| **Watch** | Elevated interest — hot/cold, strong wind, low pressure, or \|z\| ≥ 2.5 vs the recent 7-day baseline. |
| **Info** | Notable but lower urgency (hot + very dry, strong high pressure, warm water sample). |

## How flags are made

1. **Absolute thresholds** — configured in [`analytics/anomaly-thresholds.json`](../analytics/anomaly-thresholds.json) (heat/cold, MSLP, wind, waves, dry-hot compound, Casey diurnal range).
2. **Z-scores vs 7-day baseline** — population z is the primary trigger; sample z and MAD (robust) z are also reported.
3. **Site rules** — e.g. large day/night temperature swing at Casey, IL.

## Files

| File | Role |
|------|------|
| [`data/latest/anomaly-report.json`](../data/latest/anomaly-report.json) | Today’s flags + methods metadata |
| [`docs/ANOMALY_METHODS.md`](../docs/ANOMALY_METHODS.md) | Full method write-up + worked examples |
| [`data/latest/science-analytics.json`](../data/latest/science-analytics.json) | Hub digest including anomaly counts |

## Important

UOGW anomaly detection is **for research screening and education**. Always treat official forecasts and warnings from national meteorological services as authoritative.
