# Contributing to UOGW

## Adding a source

1. Propose the source in an issue with: authority URL, license, cadence, layer.
2. Add an entry to `sources/registry.json` and `catalog/catalog.json`.
3. Prefer **index automation** over bulk mirrors.
4. Never strip attribution.

## Running automations

Workflows under `.github/workflows/` use public HTTP endpoints and commit indexes back to this repository (except `msds-ground-daily`, which targets `msds-data`).

## Code of conduct for data

- Respect upstream terms of use.
- Do not commit credentials.
- Do not commit multi-GB binary dumps without maintainer approval.
