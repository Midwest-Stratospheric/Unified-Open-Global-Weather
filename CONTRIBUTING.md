# Contributing to Unified Open Global Weather (UOGW)

Thank you for interest in the open multi-layer atmospheric commons.

## Scope

UOGW indexes and samples **public, redistributable** atmospheric data (ground, marine, upper-air, stratospheric, satellite/model, and MSDS flight products). We do not accept proprietary, restricted, or non-redistributable bulk archives into this tree.

## Ways to contribute

1. **Catalog / source suggestions** — Propose additional open authority endpoints with license and attribution notes.
2. **Bug reports** — Broken latest pointers, failed workflows, chart errors: open an issue with timestamps and paths.
3. **Scripts & docs** — Improvements to ingest, anomaly methods, heal/rollback, or documentation.
4. **Attribution** — Corrections to upstream credits in catalog or docs.

## Development notes

- Prefer Python 3.10+ and minimal dependencies where possible.
- Do not commit API keys or secrets; use GitHub Actions secrets.
- Keep layer boundaries clear (`layers/`, `data/latest/`, `catalog/`, `status/`).
- Commit message style: `feat:`, `fix:`, `docs:`, `chore:`.

## Pull requests

Describe what changed and why. Call out any new external dependency or license impact. Confirm contributions stay within open/redistributable bounds.

## Code of conduct

Be respectful. This is a research commons focused on transparent, versioned open atmosphere data.

## License

Contributions are expected under terms compatible with the repository’s open licensing and upstream attribution requirements (see README and catalog). CC BY 4.0 is used for many derived science products; always retain upstream provider terms.
