# UOGW Operations — Health Monitor

## Purpose

Automatically **check** that daily data products exist and are fresh, **self-heal** missing `data/latest` pointers when a layer copy exists, **re-dispatch** failed/stale workflows, and **open a GitHub Issue** if critical data is still missing.

## Workflow

- File: `.github/workflows/health-monitor.yml`
- Schedule: **12:00 UTC** and **18:00 UTC** daily (+ manual run)
- Permissions: `contents`, `actions`, `issues`

## Checks

| ID | Critical | Max age | Re-dispatch |
|----|----------|---------|-------------|
| global-cities | yes | 36h | global-samples-daily.yml |
| casey-hourly | yes | 48h | msds-ground-daily.yml |
| ndbc-realtime | yes | 36h | ndbc-marine-daily.yml |
| research-summary | yes | 36h | daily-research-package.yml |
| science-package | yes | 36h | daily-research-package.yml |
| anomaly-report | no | 36h | anomaly-detection-daily.yml |
| rolling-baseline | no | 48h | rolling-baseline-daily.yml |
| satellite-index | no | 48h | satellite-radiance-daily.yml |
| fair-metadata | no | 48h | fair-metadata-daily.yml |
| charts-markdown | no | 48h | charts-daily.yml |
| catalog | yes | — | — |

## Intervention order

1. **Self-heal** — copy `layers/.../latest` → `data/latest/...` when the latest pointer is missing  
2. **Commit** health report + healed files  
3. **Re-dispatch** workflows for missing/stale products  
4. **Issue** — open/update label `uogw-health` on critical failure; auto-close when healthy  

## Reports

- `data/latest/health-report.json`
- `status/health.json`
- `data/entries/YYYY-MM-DD/health-report.json`

## Manual run

Actions → **Health Monitor** → Run workflow.
