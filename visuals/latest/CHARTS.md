# UOGW Charts - 2026-08-05

Generated from data in this repository. View on GitHub — no external webpage.

_Generated at 2026-08-05T05:38:44Z UTC · Midwest Stratospheric Data Systems_

## PNG charts

### Global city temperatures

![Global city temperatures](./global-city-temperatures.png)

### City temperature map

![City temperature map](./global-city-temp-map.png)

### Casey hourly temperature

![Casey hourly temperature](./casey-hourly-temperature.png)

### NDBC marine samples

![NDBC marine samples](./ndbc-marine-samples.png)

### Anomaly severity

![Anomaly severity](./anomaly-severity.png)

### Research cities Tmin/Tmax

![Research cities Tmin/Tmax](./research-cities-tminmax.png)

## Anomaly severity (Mermaid)

```mermaid
pie showData
  title Anomaly flags 2026-08-05
  "alert" : 0
  "watch" : 0
  "info" : 0
```

## City temperatures (Mermaid xychart)

```mermaid
xychart-beta
  title "City temperatures C - 2026-08-05"
  x-axis ["Jakarta", "Seoul", "Beijing", "Bangkok", "Berlin", "Casey", "Paris", "Rome", "Cairo", "Madrid", "Houston", "Dubai"]
  y-axis "Temp C"
  bar [26.3, 26.8, 27.5, 27.8, 28.9, 29.3, 30.1, 30.1, 30.7, 31.9, 35.0, 38.3]
```

## Casey hourly (Mermaid xychart)

```mermaid
xychart-beta
  title "Casey IL hourly C"
  x-axis ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]
  y-axis "Temp C"
  line [19.4, 18.6, 17.5, 16.2, 20.8, 25.1, 27.4, 29.1, 29.3, 28.4, 24.0, 20.7]
```

## Snapshot table

| Metric | Value |
|--------|-------|
| Date UTC | 2026-08-05 |
| Cities OK | 32 |
| City T min/max C | 5.6 / 38.3 |
| Anomaly total | 0 |
| Casey hours | 24 |
| NDBC samples | 7 |

Data sources: `data/latest/*.json` in this repo.

