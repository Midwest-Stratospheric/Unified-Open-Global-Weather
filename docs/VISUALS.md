# UOGW Chart Automation

Charts are generated **automatically** — no manual steps required for daily updates.

## Triggers

| Trigger | When |
|---------|------|
| Cron | **11:00 UTC** and **13:30 UTC** daily |
| `workflow_run` | After **Daily Research Package**, **Global Samples**, **NDBC Marine**, **MSDS Ground**, or **Anomaly Detection** completes successfully |
| Manual | Actions → **Charts Daily** → Run workflow |

## Script

`scripts/generate_charts.py`

Reads `data/latest/` (with layer fallbacks) and writes:

- `visuals/latest/*.png`
- `visuals/latest/CHARTS.md`
- `visuals/YYYY-MM-DD/` dated copy
- `data/latest/visuals-manifest.json`
- `status/charts.json`

## README

The main [README](../README.md) embeds all `visuals/latest/*.png` images. When this workflow commits new PNGs, the README graphs update automatically on the next page load.

## Local run

```bash
pip install matplotlib numpy
python3 scripts/generate_charts.py
```
