# Layers

UOGW organizes the commons into six layers.

## Ground

Surface land stations, citizen science, model-driven dailies, and first-party Casey radiation.

| Path | Content |
|------|---------|
| `layers/ground/casey/` | MSDS Casey, IL daily + latest meteorology |
| `layers/ground/casey/gmc-800/` | **Fixed GMC-800 surface radiation** (CPM, µSv/h) at 39.2974 N, −87.9818 W |
| `layers/ground/casey/xsense/` | Indoor X-Sense building average |
| `layers/ground/casey/external/` | External / NWS pairing |
| `layers/ground/samples/` | Worldwide city surface samples |
| `layers/ground/ghcn/` | GHCNd global station index (counts + samples) |
| `layers/ground/international/` | Foreign open-source registry snapshots |

The GMC-800 series is ionizing-radiation background at a **fixed** weather station. It complements Casey meteorology; it does not replace it.

## Marine

Buoys, ships, ocean profiles, coastal water levels.

| Path | Content |
|------|---------|
| `layers/marine/ndbc/` | NDBC station indexes + sample stations |

Catalog also points to Argo, ICOADS, and NOAA CO-OPS tides.

## Upper-air

Radiosondes, pilot balloons, reference networks.

| Path | Content |
|------|---------|
| `layers/upper-air/igra/` | IGRA station list + year-to-date file index |

Catalog also points to GRUAN, CUON, and University of Wyoming soundings.

## Stratospheric

Ozone, water vapor, QBO, research networks.

Primarily **catalog links** today (SWOOSH, WOUDC, SHADOZ, QBO). Expand with MSDS near-space profiles as flights recover.

## Satellite

Open imagery products, reanalysis, GNSS radio occultation.

Catalog links: GOES open data, MERRA-2, COSMIC, ECMWF/Copernicus open products.

## Flight

First-party high-altitude balloon packages from Midwest Stratospheric Data Systems (X2Griffon and related).

This is UOGW’s unique contribution: vertical profiles that agencies do not publish the same way. Ground GMC-800 data is the surface radiation counterpart, not a flight file.
