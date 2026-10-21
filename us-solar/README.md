# US Rooftop Solar Adoption

Static dashboard, no build step. Served by GitHub Pages from this folder.

- `index.html`: residential rooftop solar and battery adoption by state. Disposable income, electricity bills, annual PV yield, payback, NPV and an adoption propensity index.
- `datacentres.html`: rooftop PV technical potential by state, distance to data centre hubs, and the cost of renting rooftops vs owning utility-scale PV, gas or grid supply for a data centre load.

## Updating the data

Drop a `data/states.csv` file in this folder with columns `code,price,kwh_mo,dpi,yield,pen,attach`. Any value present overrides the embedded dataset in `index.html` on load. The page's Export CSV button produces the right format to start from.

## Sources

EIA residential prices and consumption (2024), BEA disposable personal income (2024), NREL PVWatts yields, NREL TP-6A20-65298 rooftop technical potential, Lazard LCOE+ (June 2026), DCMap pipeline figures via Next Move Strategy Consulting (Aug 2026). Penetration and battery attachment rates are indicative estimates.
