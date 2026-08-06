# UOGW Charts — 2026-08-06

Temperatures shown in **Fahrenheit (°F)**. Generated automatically from repository data.

_Generated at 2026-08-06T02:57:24Z UTC · Midwest Stratospheric Data Systems_

## PNG charts

### Global city temperatures (°F)

![Global city temperatures (°F)](./global-city-temperatures.png)

### City temperature map (°F)

![City temperature map (°F)](./global-city-temp-map.png)

### Casey hourly temperature (°F)

![Casey hourly temperature (°F)](./casey-hourly-temperature.png)

### NDBC marine samples

![NDBC marine samples](./ndbc-marine-samples.png)

### Global city relative humidity (%)

![Global city relative humidity (%)](./global-city-humidity.png)

### Anomaly severity

![Anomaly severity](./anomaly-severity.png)

#### Anomaly detection guide (what this graph means)

UOGW counts **research flags** for the daily sample set — **not** National Weather Service warnings.

| Severity | Meaning |
|----------|---------|
| **Alert** | Strong outlier vs thresholds or baseline (extreme heat/cold, |z| >= 3, very high waves). |
| **Watch** | Elevated interest — heat/cold, wind, low pressure, or |z| >= 2.5 vs the 7-day baseline. |
| **Info** | Lower urgency (hot + very dry, strong high, warm water sample). |

**How flags are made:** (1) absolute thresholds in `analytics/anomaly-thresholds.json`, (2) z-scores vs rolling baseline (population z primary; MAD z also reported), (3) site rules such as large Casey diurnal range.

Today: **alert 1** · **watch 2** · **info 0** · total **3**

Full methods: [docs/ANOMALY_METHODS.md](../../docs/ANOMALY_METHODS.md) · short guide: [ANOMALY_GUIDE.md](../ANOMALY_GUIDE.md) · data: [anomaly-report.json](../../data/latest/anomaly-report.json)

### Research cities Tmin/Tmax (°F)

![Research cities Tmin/Tmax (°F)](./research-cities-tminmax.png)

### Daily summary card

![Daily summary card](./daily-summary-card.png)

## Anomaly severity (Mermaid)

```mermaid
pie showData
  title Anomaly flags 2026-08-06
  "alert" : 1
  "watch" : 2
  "info" : 0
```

## Snapshot table (°F)

| Metric | Value |
|--------|-------|
| Date UTC | 2026-08-06 |
| Cities OK | 32 |
| City T min/max °F | 49.3 / 106.0 |
| Anomaly total | 3 |
| Casey hours | 24 |
| NDBC samples | 7 |

Source observation files remain metric; charts are °F for display.

