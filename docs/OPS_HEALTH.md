# UOGW Operations — Health Monitor & Alert PRs

## Purpose

1. **Check** daily products (present, valid, not stale)  
2. **Self-heal** `data/latest` pointers  
3. **Re-dispatch** broken producers  
4. **Log failures as a Pull Request** on branch `ops/uogw-health-alert`  
5. **Clear** that PR automatically when health recovers  

## Alert PR lifecycle

| State | What happens |
|-------|----------------|
| Critical failure detected | Push branch `ops/uogw-health-alert` with `ops/HEALTH_ALERT.md` + `ops/health-report.json`. Open PR **UOGW health alert — critical data issue** (or comment on existing open PR). |
| Still failing on later runs | Force-update branch + comment with fresh report (PR stays open = logged history). |
| All critical checks OK | Comment **Recovered** and **close** the PR automatically. |

Do **not** merge the alert PR unless you intentionally want the alert log on `main`. Closing is the normal clear path.

## Schedule

- `health-monitor.yml`: **12:00** and **18:00 UTC** (+ manual)  

## Related

- Rollback procedures: [`docs/ROLLBACK.md`](./ROLLBACK.md)  
- Heal script: `scripts/heal_latest.py`  
- Status: `data/latest/health-report.json`, `status/health.json`, `status/heal.json`  
