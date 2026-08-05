# UOGW Visuals — GitHub-native only

Charts are meant to be viewed **inside GitHub**, not on an external site.

## How to view

Open this file on GitHub:

**[visuals/latest/CHARTS.md](../visuals/latest/CHARTS.md)**

It contains:

1. **Markdown image embeds** — `![...](./file.png)` for PNG charts stored in the repo  
2. **Mermaid charts** — pie + xychart blocks that GitHub renders in markdown  
3. **Snapshot tables** — pure markdown tables  

No CDN, no separate web app, no extra hosting.

## Files

| Path | Role |
|------|------|
| `visuals/latest/CHARTS.md` | Primary gallery (view on GitHub) |
| `visuals/latest/*.png` | Chart images |
| `visuals/YYYY-MM-DD/` | Dated snapshot |
| `visuals/README.md` | Index |

## Automation

`charts-daily.yml` · daily **11:00 UTC** · writes markdown + PNGs from `data/latest/`.
