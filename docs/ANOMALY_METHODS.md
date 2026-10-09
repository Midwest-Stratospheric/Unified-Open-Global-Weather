# UOGW Anomaly Detection — Thresholds & Z-Score Methods

Research screening only. **Not** an official weather warning service.

Machine config twin: [`analytics/anomaly-thresholds.json`](../analytics/anomaly-thresholds.json)

---

## 1. Specific absolute threshold examples

These fire regardless of recent history. Values are chosen for **research flagging**, not NWS product definitions.

### Surface air temperature

| Example condition | Metric | Threshold | Severity | Why it matters |
|-------------------|--------|-----------|----------|----------------|
| Baghdad or Phoenix-class heat | `temperature_c` | **≥ 40 °C** | `alert` | Heat-stress / extremes research |
| Hot day (many mid-latitude summers) | `temperature_c` | **≥ 35 °C** | `watch` | Elevated heat |
| Arctic / continental cold | `temperature_c` | **≤ −30 °C** | `alert` | Extreme cold |
| Severe cold | `temperature_c` | **≤ −20 °C** | `watch` | Strong cold anomaly candidate |

**Example:** Tokyo report `temperature_c = 36.2` → `surface_heat` / `watch` (crosses 35, not 40).

### Mean sea-level pressure

| Example condition | Metric | Threshold | Severity | Notes |
|-------------------|--------|-----------|----------|-------|
| Deep cyclone / strong storm environment | `pressure_msl_hpa` | **≤ 980 hPa** | `watch` | Very low MSLP |
| Strong high | `pressure_msl_hpa` | **≥ 1040 hPa`** | `info` | Strong anticyclone |

**Example:** Reykjavik `pressure_msl_hpa = 972.4` → `low_pressure` / `watch`.

### Wind

| Example condition | Metric | Threshold | Severity | Rough class |
|-------------------|--------|-----------|----------|-------------|
| Strong wind | `wind_speed_ms` | **≥ 15 m/s** | `watch` | ~30+ kt |
| Gale-class sample | `wind_speed_ms` | **≥ 25 m/s** | `alert` | ~50+ kt |

**Example:** Coastal buoy-adjacent city sample `wind_speed_ms = 16.8` → `high_wind` / `watch`.

### Compound surface

| Example condition | Rule | Severity |
|-------------------|------|----------|
| Hot and very dry | `temperature_c ≥ 25` **and** `relative_humidity_pct ≤ 10` | `info` |

**Example:** Desert station `T=31 °C`, `RH=8%` → `dry_hot` / `info`.

### Marine (NDBC samples)

| Example condition | Metric | Threshold | Severity |
|-------------------|--------|-----------|----------|
| High waves | `wave_height_m` | **≥ 4 m** | `watch` |
| Very high waves | `wave_height_m` | **≥ 6 m** | `alert` |
| Very warm water sample | `water_temp_c` | **≥ 30 °C** | `info` |

**Example:** Station `41001` `wave_height_m = 4.7` → `high_waves` / `watch`.

### Local MSDS site (Casey, IL)

| Example condition | Metric | Threshold | Severity |
|-------------------|--------|-----------|----------|
| Large diurnal swing | `max(T) − min(T)` over hourly series | **≥ 20 °C** | `watch` |

**Example:** Hourly Casey series min −2 °C, max 19 °C → range 21 °C → `large_diurnal_range` / `watch`.

---

## 2. Z-score normalization methods

When a **rolling baseline** exists (`data/latest/rolling-baseline.json`), UOGW computes several normalizations for the same observation so researchers can compare methods.

For a value \(x\) with baseline samples \(x_1,\ldots,x_n\):

### A. Population z-score (default for alerts)

\[
z_{\mathrm{pop}} = \frac{x - \mu}{\sigma_{\mathrm{pop}}}, \quad
\mu = \frac{1}{n}\sum_i x_i, \quad
\sigma_{\mathrm{pop}} = \sqrt{\frac{1}{n}\sum_i (x_i-\mu)^2}
\]

- Matches `statistics.pstdev` style baselines.
- Stable when the 7-day window is treated as the full reference population for short-term screening.

**Alert rule (default):** \(|z_{\mathrm{pop}}| \ge 3\) → `alert`; \(|z_{\mathrm{pop}}| \ge 2.5\) → `watch`.

### B. Sample z-score (Bessel’s correction)

\[
z_{\mathrm{sample}} = \frac{x - \mu}{\sigma_{\mathrm{sample}}}, \quad
\sigma_{\mathrm{sample}} = \sqrt{\frac{1}{n-1}\sum_i (x_i-\mu)^2}
\]

- Slightly larger denominator uncertainty for small \(n\) (e.g. 3–7 days).
- Reported for transparency; not the primary trigger unless configured.

### C. Modified z-score (MAD, Iglewicz–Hoaglin style)

\[
z_{\mathrm{MAD}} = \frac{0.6745\,(x - \tilde{x})}{\mathrm{MAD}}, \quad
\mathrm{MAD} = \mathrm{median}_i(|x_i - \tilde{x}|)
\]

where \(\tilde{x}\) is the median of the baseline window.

- **Robust** to a single wild day already inside the baseline window.
- Preferred when the 7-day window may itself contain an outlier.
- Screening example: \(|z_{\mathrm{MAD}}| \ge 3.5\) often used in robust outlier literature; UOGW reports the value and flags at **3.5** for `watch`, **5.0** for `alert` on this method.

### D. Range-normalized score (min–max style)

\[
s_{\mathrm{range}} = \frac{x - \mu}{\max_i x_i - \min_i x_i + \varepsilon}
\]

- Not a classical z-score; useful when \(\sigma\approx 0\) but the window still has a small span.
- Reported as diagnostic only (no severity by itself).

### E. Percentile rank within baseline

Empirical rank of \(x\) among \(\{x_1,\ldots,x_n, x\}\).

- Interpretable: “hottest / coldest in the available window.”
- Complementary to z-scores when \(n\) is small.

---

## 3. Worked numerical example

Baseline 7-day temperatures for a city (°C):  `22.0, 23.5, 21.0, 24.0, 22.5, 23.0, 22.0`  
Today: `x = 29.0`

| Method | Result (approx.) | Interpretation |
|--------|------------------|----------------|
| Mean \(\mu\) | 22.57 | Center of window |
| \(\sigma_{\mathrm{pop}}\) | ~0.96 | |
| \(z_{\mathrm{pop}}\) | **~6.7** | Strong high outlier → alert |
| \(\sigma_{\mathrm{sample}}\) | ~1.04 | |
| \(z_{\mathrm{sample}}\) | **~6.2** | Same conclusion |
| Median \(\tilde{x}\) | 22.5 | |
| MAD | ~1.0 | |
| \(z_{\mathrm{MAD}}\) | **~4.4** | Above 3.5 → robust watch/alert band |
| Percentile | ~100% | Warmest vs window |

---

## 4. Outputs

| File | Content |
|------|---------|
| `data/latest/anomaly-report.json` | All flags + per-city z-method breakdown |
| `analytics/anomaly-thresholds.json` | Machine-readable thresholds |
| `status/anomaly.json` | Health + counts |

### Severity legend

| Severity | Meaning |
|----------|---------|
| `info` | Notable, low urgency |
| `watch` | Elevated research interest |
| `alert` | Extreme relative to configured research thresholds |

---

## 5. Limitations

- 7-day baselines are **not** climate normals (30-year).
- City samples are model/obs fusion (Open-Meteo) — good for monitoring, not legal/forensic met.
- Marine thresholds use a small buoy subset.
- Always cite upstream data providers.
