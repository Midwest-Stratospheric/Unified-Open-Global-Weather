# UOGW feature catalog

See the full hub ↔ GitHub map in [HUB_FEATURES.md](./HUB_FEATURES.md).

## Layers

1. **Ground** — surface stations, Casey daily, GLOBE
2. **Marine** — NDBC samples
3. **Upper-air** — IGRA index, Illinois radiosonde counts
4. **Stratospheric / space** — SWPC Kp, GOES X-rays (via space-gfs snapshot)
5. **Satellite / model** — GFS seamless fields for research charts
6. **Flight** — MSDS X2Griffon products (msds-data)

## Research modules

- Multi-method anomaly detection
- Pre-tornado condition score (Clark County IL)
- Ozone health snapshot
- Science analytics digest
- Self-healing latest pointers (`heal_latest.py`)
- Health-monitor PR automation

## Automations

All under `.github/workflows/` — schedule + `workflow_dispatch`.
