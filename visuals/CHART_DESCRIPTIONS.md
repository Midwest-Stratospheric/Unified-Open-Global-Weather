# UOGW chart descriptions

Short plain-language notes for each automated graph. Charts display temperatures in **°F** unless noted.

| Chart file | Description |
|------------|-------------|
| `global-city-temperatures.png` | Horizontal bar chart of current surface air temperature for each successful global city sample. Bars are sorted cold→hot; warmer colors mark heat (≥86°F / ≥95°F). |
| `global-city-temp-map.png` | Scatter map of the same city samples by longitude/latitude, colored by temperature (°F). Shows geographic pattern of the daily open sample set. |
| `casey-hourly-temperature.png` | 24-hour temperature trace for Casey, Illinois (MSDS home site). Useful for diurnal range and local extremes that feed anomaly rules. |
| `research-cities-tminmax.png` | Daily minimum and maximum temperatures for the research climate city set. Compares day-range width across selected locations. |
| `ndbc-marine-samples.png` | NOAA NDBC buoy sample panel: wave height (meters) plus water and air temperature (°F) for stations included in today's marine pull. |
| `global-city-humidity.png` | Relative humidity (%) for the same global city sample network. Dry+hot combinations can contribute to compound research flags. |
| `anomaly-severity.png` | Count of UOGW research anomaly flags by severity (alert / watch / info). **Not** an NWS warning product. See [ANOMALY_GUIDE.md](./ANOMALY_GUIDE.md). |
| `daily-summary-card.png` | One-page snapshot of today's visual package: city count, temperature span, Casey hours, NDBC samples, and anomaly total. |

These descriptions are also embedded under each image in [`latest/CHARTS.md`](./latest/CHARTS.md) and on the [MSDS Data Hub](https://midwestsds.com/msds-data-hub.html).
