# Pre-tornado research conditions — Clark County, IL

**Research screening only. Not an NWS watch, warning, or probability of tornado occurrence.**

## What it is

Automated composite score (0–100) near **Casey / Clark County, Illinois** using Open-Meteo fields:

| Factor | Role in score |
|--------|----------------|
| CAPE | Buoyant instability |
| Lifted index | Environmental instability |
| CIN | Whether storms can surface-root |
| Dewpoint | Boundary-layer moisture |
| Wind / gusts | Rough organization proxy (not deep-layer shear) |
| 3-hour pressure tendency | Falling pressure signal |

## Levels

| Level | Score | Meaning |
|-------|-------|--------|
| quiet | 0–24 | Background |
| elevated | 25–44 | Rising factors |
| watch | 45–64 | Multiple concurrent factors |
| high | 65–100 | Strong stacked research signals |

## Outputs

- `data/latest/pre-tornado-clark.json`
- `visuals/latest/pre-tornado-clark-trend.png`
- Workflow: `pre-tornado-clark.yml` (about every 30 minutes)

## Official sources

Always use [weather.gov](https://www.weather.gov/), [SPC](https://www.spc.noaa.gov/), and local emergency management for life-safety decisions.
