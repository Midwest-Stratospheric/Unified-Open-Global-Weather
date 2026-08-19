# Security Policy

## Supported surface

UOGW is an **open data commons** with many scheduled GitHub Actions. The security surface is primarily the automation scripts, workflow permissions, and integrity of committed JSON/status pointers on `main`.

## Reporting a vulnerability

If you find an issue that could compromise repository integrity, leak secrets, or allow malicious content injection into automated artifacts:

1. **Do not** file a public issue with full exploit details.
2. Email **launchcontrol@midwestsds.com** with a clear description and reproduction steps if available.
3. Allow reasonable time for triage before public disclosure.

## Out of scope

- Defects in upstream agency feeds (NOAA, NASA, Open-Meteo, etc.) — report to those operators.
- Requests for proprietary or restricted datasets.
- Speculative scenarios unrelated to code or data in this repository.

## Secrets

API keys and tokens belong in GitHub Actions secrets only. Rotate any credential that appears in logs or history.
