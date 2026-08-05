# UOGW Built-in Visuals

Visuals are generated **from data already in the repository**, then committed back under `visuals/`.

## Chart set (daily)

1. **Global city temperatures** — horizontal bar chart  
2. **City temperature map** — lon/lat scatter colored by °C  
3. **Casey hourly temperature** — line (+ RH when present)  
4. **NDBC marine samples** — wave height + water/air temp  
5. **Anomaly severity** — alert / watch / info counts  
6. **Research cities Tmin/Tmax** — daily climate block  
7. **Daily summary card** — text dashboard image  

## Paths

- Latest PNGs: `visuals/latest/`
- Dated PNGs: `visuals/YYYY-MM-DD/`
- Interactive HTML: `visuals/dashboard.html`
- Manifest: `visuals/latest/manifest.json`

## Automation

`.github/workflows/charts-daily.yml` — **11:00 UTC** daily.

Uses Python **matplotlib** on GitHub Actions. No external BI tool required.

## Theme

MSDS navy / cyan (`#0a1628` / `#00d4ff`) to match midwestsds.com.
