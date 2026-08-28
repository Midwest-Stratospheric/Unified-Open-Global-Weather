# UOGW Health Alert — 2026-08-28

Generated: `2026-08-28T21:59:06Z`
Critical failure: **True**

## Summary
```json
{
  "total": 11,
  "ok": 9,
  "missing": 0,
  "stale": 2,
  "invalid_json": 0
}
```

## Checks
| ID | Status | Critical | Path | Reasons | Workflow |
|----|--------|----------|------|---------|----------|
| global-cities | `ok` | True | `data/latest/global-cities.json` | — | `global-samples-daily.yml` |
| casey-hourly | `ok` | True | `data/latest/casey-hourly.json` | — | `msds-ground-daily.yml` |
| ndbc-realtime | `ok` | True | `data/latest/ndbc-realtime.json` | — | `ndbc-marine-daily.yml` |
| research-summary | `stale` | True | `data/latest/research-summary.json` | age 59.1h > 36h | `daily-research-package.yml` |
| science-package | `stale` | True | `data/latest/science-package.json` | age 59.1h > 36h | `daily-research-package.yml` |
| anomaly-report | `ok` | False | `data/latest/anomaly-report.json` | — | `anomaly-detection-daily.yml` |
| rolling-baseline | `ok` | False | `data/latest/rolling-baseline.json` | — | `rolling-baseline-daily.yml` |
| satellite-index | `ok` | False | `data/latest/satellite-radiance-index.json` | — | `satellite-radiance-daily.yml` |
| fair-metadata | `ok` | False | `data/latest/fair-metadata.json` | — | `fair-metadata-daily.yml` |
| charts-markdown | `ok` | False | `visuals/latest/CHARTS.md` | — | `charts-daily.yml` |
| catalog | `ok` | True | `catalog/catalog.json` | — | `—` |

## Re-dispatch queue

- `daily-research-package.yml`

## Recovery

This PR is opened automatically when critical health checks fail.
It is **closed automatically** when Health Monitor reports recovery.

Manual steps if it does not clear:
1. Re-run **Health Monitor**
2. Follow [docs/ROLLBACK.md](../docs/ROLLBACK.md)
3. Actions → **Rollback data/latest** (confirm `ROLLBACK`) if needed

