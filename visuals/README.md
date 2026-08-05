# UOGW Visuals

Charts are **generated daily from data in this repository** (not external dashboards).

## Latest charts

| Chart | File |
|-------|------|
| Global city temperatures | [`latest/global-city-temperatures.png`](./latest/global-city-temperatures.png) |
| City temperature map | [`latest/global-city-temp-map.png`](./latest/global-city-temp-map.png) |
| Casey hourly temperature | [`latest/casey-hourly-temperature.png`](./latest/casey-hourly-temperature.png) |
| NDBC marine samples | [`latest/ndbc-marine-samples.png`](./latest/ndbc-marine-samples.png) |
| Anomaly severity | [`latest/anomaly-severity.png`](./latest/anomaly-severity.png) |
| Research cities Tmin/Tmax | [`latest/research-cities-tminmax.png`](./latest/research-cities-tminmax.png) |
| Daily summary card | [`latest/daily-summary-card.png`](./latest/daily-summary-card.png) |

## Interactive dashboard

Open [`dashboard.html`](./dashboard.html) (best via GitHub Pages or local browser).

## Automation

Workflow: `.github/workflows/charts-daily.yml` — runs **11:00 UTC** daily and on demand.

Source data:
- `data/latest/global-cities.json`
- `data/latest/casey-hourly.json`
- `data/latest/ndbc-realtime.json`
- `data/latest/anomaly-report.json`
- `data/latest/research-summary.json`
- `data/latest/daily-climate.json`
