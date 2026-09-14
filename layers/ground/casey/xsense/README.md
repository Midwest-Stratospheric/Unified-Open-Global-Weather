# Casey X-Sense in-situ ground station

First-party temperature and relative humidity from the MSDS Casey, IL thermo-hygrometer.

## Flow (git does the work)

1. X-Sense emails a CSV export to the station inbox (`support@x-sense-iot.com`).
2. A thin Grok Gmail trigger drops the attachment into `raw/` and stops.
3. GitHub Action `Ingest X-Sense Ground` parses the CSV and writes products.

```
layers/ground/casey/xsense/
  raw/YYYY-MM-DD.csv     # unmodified email attachment
  YYYY-MM-DD.json        # hourly rollup + daily stats
  latest.json            # newest product
data/entries/YYYY-MM-DD/casey-xsense.json
data/latest/casey-xsense.json
status/msds-xsense.json
```

Companion dual-write (when `MSDS_DATA_TOKEN` is present):

`Midwest-Stratospheric/msds-data/ground-weather/xsense/`

Native interval is 1 minute. Published product is hourly means with min/max.
