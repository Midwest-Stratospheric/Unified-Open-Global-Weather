# UOGW Explicit Rollback Procedures

Use these when `data/latest` is wrong, partially missing, or corrupted after a bad automation run.

---

## Principles

1. **Never force-push `main`** for data recovery unless legal/security emergency.  
2. Prefer **restore into `data/latest`** from dated entries or rollback points.  
3. Take a **new rollback point** before overwriting (automated by heal/rollback workflows).  
4. After rollback, run **Health Monitor**, then only re-dispatch the specific bad producer.  
5. Agency source data is upstream — UOGW rollback restores *our curated pointers and packages*, not NOAA archives.

---

## Quick decision tree

| Symptom | First action |
|---------|----------------|
| One `data/latest/*.json` missing | Run **Health Monitor** (self-heal + re-dispatch) |
| Many latest files wrong after today’s run | **Rollback data/latest** from yesterday’s `data/entries/YYYY-MM-DD` |
| Heal made it worse | **Rollback data/latest** mode `rollback-point` → `LATEST` |
| Workflow YAML broken | Revert the workflow file commit; do not rollback data unless products are bad |
| Charts only broken | Re-run **Charts Daily**; data rollback usually unnecessary |

---

## Procedure A — Automated self-heal (preferred first step)

1. GitHub → **Actions** → **Health Monitor** → **Run workflow**  
2. Wait for completion  
3. Inspect:
   - `data/latest/health-report.json`
   - `status/heal.json`
4. If `critical_fail: false` → done  
5. If still failing → Procedure B or C  

What heal does:

- Copies layer `*-latest.json` into `data/latest/` when missing/outdated  
- Rebuilds a minimal `science-package.json` if missing  
- Writes a timestamped folder under `snapshots/rollback-points/`  
- Re-dispatches producer workflows for still-bad products  
- Opens/updates Issue label `uogw-health` on critical failure  

---

## Procedure B — Rollback `data/latest` from a dated entry

**When:** Today’s package is bad; yesterday’s `data/entries/YYYY-MM-DD` is good.

1. Actions → **Rollback data/latest** → Run workflow  
2. Inputs:
   - `mode`: `entry-date`  
   - `entry_date`: e.g. `2026-08-04`  
   - `confirm`: `ROLLBACK` (exactly)  
3. Workflow will:
   - Snapshot current latest into `snapshots/rollback-points/<timestamp>/`  
   - Copy known files from `data/entries/<date>/` into `data/latest/`  
   - Commit with message `ops(rollback): ...`  
4. Verify `data/latest/_restored_from.json`  
5. Run **Health Monitor**  
6. Re-dispatch only the producers you still need refreshed (optional)  

---

## Procedure C — Rollback from automatic rollback-point

**When:** You need the pre-heal or pre-rollback snapshot.

1. List points (repo browser): `snapshots/rollback-points/`  
2. Actions → **Rollback data/latest**  
3. Inputs:
   - `mode`: `rollback-point`  
   - `rollback_point`: `LATEST` or a timestamp folder name  
   - `confirm`: `ROLLBACK`  
4. Verify and run Health Monitor  

---

## Procedure D — Manual git file restore (surgical)

**When:** Only one file is bad and you know a good commit.

```bash
# clone main
git clone https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather.git
cd Unified-Open-Global-Weather

# find history for one path
git log --oneline -- data/latest/science-package.json

# restore file from commit SHA
git checkout <SHA> -- data/latest/science-package.json
git commit -m "ops(rollback): restore science-package from <SHA>"
git push origin main
```

Then run Health Monitor.

---

## Procedure E — Workflow code rollback

**When:** A workflow YAML change breaks producers.

1. GitHub → commits → open the bad commit  
2. Revert commit (preferred) or restore previous `.github/workflows/<file>.yml`  
3. Do **not** delete `data/entries` history  
4. Re-run the fixed workflow  
5. Health Monitor  

---

## Post-rollback checklist

- [ ] `data/latest/health-report.json` → `critical_fail: false`  
- [ ] `data/latest/science-package.json` present  
- [ ] `data/latest/global-cities.json` present  
- [ ] `visuals/latest/CHARTS.md` acceptable (re-run Charts if needed)  
- [ ] Close or confirm auto-close of `uogw-health` issue  
- [ ] Note what failed in commit message / issue comment for future tuning  

---

## What not to do

| Avoid | Why |
|-------|-----|
| `git push --force` on `main` | Destroys shared history and entry audit trail |
| Deleting `data/entries/` | Removes recovery sources |
| Re-running all workflows blindly in a loop | Worsens race conditions; use Health Monitor redispatches |
| Committing multi-TB satellite granules | Out of scope; index only |

---

## Contacts

Midwest Stratospheric Data Systems — launchcontrol@midwestsds.com  
Repo: https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather
