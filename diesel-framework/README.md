# Diesel Import Reduction Framework

A framework for cutting Australia's net diesel imports towards zero by growing domestic supply (halophytes on degraded saline land, renewable diesel from canola and tallow) and electrifying demand (mining, heavy freight with battery swapping, remote power, buses, utes and cars). Written in October 2026 under a planning scenario of Strait of Hormuz and Red Sea disruption, Russian refinery outages and a possible US diesel export ban.

**Headline:** net imports fall from about 29 GL to about 15.5 GL a year by 2035 and approach zero by about 2045.

| File | What it is |
| --- | --- |
| `index.html` | Framework page with live fuel security indicators and the two key charts |
| `FRAMEWORK.md` | The full framework, with sources |
| `data/live.json` | Live indicators, refreshed every 6 hours by `.github/workflows/diesel-live-data.yml` |

## Live data

`scripts/fetch_diesel_live.py` (standard library only) refreshes:

| Indicator | Source |
| --- | --- |
| Diesel stock (ML, days of cover) | DCCEEW weekly figures, read from [fuelplan.gov.au](https://fuelplan.gov.au/fuel-statistics) |
| Brent crude | [FRED DCOILBRENTEU](https://fred.stlouisfed.org/series/DCOILBRENTEU) |
| US Gulf Coast ultra-low sulfur diesel | [FRED DDFUELUSGULF](https://fred.stlouisfed.org/series/DDFUELUSGULF) |
| USD per AUD | [FRED DEXUSAL](https://fred.stlouisfed.org/series/DEXUSAL) |
| NEM wholesale price and demand by region | [AEMO data dashboard](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem) |

Each source is fetched separately. If one fails, its last good value is kept and flagged `"stale": true`, and `status` records the error. Run it locally with `python scripts/fetch_diesel_live.py`.

The diesel stock figure is parsed from page text, so it can break if the page layout changes; check `status.diesel_stock` in `live.json` if it goes stale.

## Publishing the page

Turn on GitHub Pages under **Settings → Pages → Deploy from a branch → `main` / root**. The page is then at `https://ajcbwips.github.io/energy-policy/diesel-framework/`.

## Joule

A copy of [Joule](https://github.com/Rexcat1/DataHack2026) lives in `../joule/`. Its diesel cover and Brent figures read `data/live.json` from this folder and keep their April 2026 values if the fetch fails. Once Pages is on, it is at `https://ajcbwips.github.io/energy-policy/joule/`.
