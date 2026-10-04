# Joule

> Copied from [Rexcat1/DataHack2026](https://github.com/Rexcat1/DataHack2026) (April 2026) and extended nationwide in October 2026. Pick any state or territory to get its real train, metro, light rail, tram, ferry, bus and coach lines for the capital and main regional centres, plus fares, capital-city fuel prices and NEM wholesale power. The gauge, diesel cover, Brent and prices come from [`../diesel-framework/data/live.json`](../diesel-framework/data/live.json), refreshed every 6 hours, with the April 2026 values as a fallback. Line names are real; trip distances, loads and fares are indicative estimates. Diesel trains, ferries and electric buses are scored by their actual fuel.

**A real-time fuel security gauge for New South Wales.**

Joule is a public-facing dashboard concept styled in the Transport for NSW livery. It gives individual travellers a live reading of how their next trip affects the state's liquid-fuel reserve — without telling them not to travel. Every choice is scored from 0 to 100, and a single actionable swap is offered when one would make a material difference.

Joule is not a substitute for the Trip Planner. It's an energy-accounting layer alongside it.

---

## Why this exists

Australia imports roughly 90% of its refined liquid fuels. As of April 2026, the national stockhold sits at **39 days of petrol and 29 days of diesel** — well below the IEA's 90-day guidance. The Strait of Hormuz closure in March–April 2026 exposed the vulnerability in real time: Sydney petrol prices peaked above 258 c/L before the federal half-excise relief and a momentary reopening of the strait pulled them back toward 213 c/L.

Joule translates this national-scale fragility into a single, legible gauge and a trip-level score so that individual behaviour and state resilience are visible on the same page.

---

## What's in this repo

| File           | Purpose                                                         |
|----------------|-----------------------------------------------------------------|
| `index.html`   | The complete dashboard — single-file, zero build, zero backend. |
| `.nojekyll`    | Tells GitHub Pages not to run Jekyll processing on the HTML.    |
| `README.md`    | This file.                                                      |
| `LICENSE`      | MIT.                                                            |

Everything runs client-side. No dependencies beyond Google Fonts (Public Sans) loaded from CDN.

---

## Deploy to GitHub Pages

1. **Create a new GitHub repository** (public or private — Pages works with both on paid plans; public only on free).
2. **Upload the three files** (`index.html`, `.nojekyll`, `README.md`, `LICENSE`) to the repository root. The easiest way:
   ```bash
   git init
   git add index.html .nojekyll README.md LICENSE
   git commit -m "Initial Joule deployment"
   git branch -M main
   git remote add origin https://github.com/<your-user>/<your-repo>.git
   git push -u origin main
   ```
3. **Enable GitHub Pages:**
   - Go to your repo → **Settings** → **Pages**.
   - Under **Source**, select **Deploy from a branch**.
   - Under **Branch**, select **main** and folder **/ (root)**. Click **Save**.
4. **Wait 1–2 minutes.** GitHub Pages will build and publish. Your site will be live at:
   ```
   https://<your-user>.github.io/<your-repo>/
   ```

To use a custom domain, add a `CNAME` file with the domain name and configure your DNS.

---

## What the numbers are

All live figures in the dashboard are drawn from published April 2026 sources:

| Figure                              | Value                | Source                                    |
|-------------------------------------|----------------------|-------------------------------------------|
| Australia petrol stockhold          | 39 days              | DCCEEW / DISER Australian Petroleum Statistics |
| Australia diesel stockhold          | 29 days              | DCCEEW / DISER                            |
| Australia jet fuel stockhold        | 30 days              | DCCEEW / DISER                            |
| Sydney ULP average                  | 213.1 c/L            | NRMA Weekly Fuel Report, 18 Apr 2026      |
| Sydney diesel average               | 318.1 c/L            | NRMA Weekly Fuel Report, week to 14 Apr   |
| Brent crude                         | US$90.89/bbl         | ICE futures live, 18 Apr 2026             |
| Federal excise (temporarily halved) | 26.3 c/L             | Federal Cabinet decision, effective 1 Apr – 30 Jun 2026 |
| NSW VPP incentive                   | up to $1,500/hh      | NSW Peak Demand Reduction Scheme          |
| NSW peak grid demand (indicative)   | ~10.2 GW             | AEMO NEM data dashboard                   |
| VPP firming (indicative)            | 412 MW               | NSW PDRS programme reporting              |

In a production build, these are live-fetched from the respective open APIs (DCCEEW APS, AEMO NEM data, NSW FuelCheck, ACCC Fuel Price Monitoring) and refreshed every 15 minutes. In this static concept, the values are hard-coded with a small random walk on the Fuel Security Index to simulate live behaviour.

---

## How the Joule score is calculated

The score for a given trip is a weighted composite:

```
score = 0.60 × fuel_impact  +  0.25 × corridor_load  +  0.15 × time_cost
```

- **Fuel impact (60%)** — kWh-equivalent of the trip, benchmarked against a solo car on the same route at the same frequency. Active and electric transit score highest.
- **Corridor load (25%)** — how much spare capacity the recommended transit service has on the chosen corridor. A train with empty seats is worth more per walk-on than one already crowded.
- **Time cost (15%)** — a friction term that prevents the score from pretending a 3-hour coach trip is a free swap for a 90-minute drive.

Full scoring logic is in `index.html` under the `calcJouleScore` function.

---

## Corridor and route data

The planner covers **26 Sydney and NSW transport routes** in two groups:

**Train corridors (12):** T1 Western (Blacktown, Penrith, Mount Druitt, Parramatta), T8 Airport & South (Campbelltown), T2 Inner West (Liverpool), T3 (Bankstown), Metro North West (Chatswood), Central Coast & Newcastle, South Coast (Wollongong), Blue Mountains (Lithgow), Central West Coach (Bathurst), and an Inner Sydney multi-mode option.

**Bus routes (13):** B1 B-Line (Mona Vale → Wynyard), 350 (Bondi Jct → Airport), 380 (Bondi Beach → Circular Quay), 333 (Bondi PrePay), 400 (Bondi Jct → Eastgardens), 370 (Coogee → Leichhardt), 891 (Central → UNSW), M90 (Liverpool → Burwood), M91 (Parramatta → Hurstville), T80 (Liverpool ↔ Parramatta T-Way), 545 (Chatswood → Parramatta), 500 (Central → Olympic Park), 610X (Castle Hill → Wynyard), L90 (Palm Beach → City).

Each route carries four calibration attributes used in scoring:

- Representative transit line and official TfNSW colour
- Typical end-to-end distance (km)
- Peak-hour service frequency
- Peak load factor (fraction of seated capacity used)
- Car-dependence score for the residential catchment (0–1)

Sources: Transport for NSW route timetables and GTFS data (April 2026 snapshot), NRMA/BusNSW route histories, Rome2Rio trip-time data for individual stop-to-stop distances, and ABS 2021 Census journey-to-work mode share by LGA. For routes with real-time load data available through the Transport for NSW Data Hub, the load factor would be refreshed live; for others, close estimates are used based on published patronage data.

For a production deployment, these would be replaced with live GTFS feed consumption so that engineering works or disruptions on a line immediately re-weight the score for trips on that corridor.

---

## Accessibility & privacy

- Built with WCAG 2.2 AA colour contrast ratios throughout.
- Public Sans typography (Transport for NSW's digital typeface).
- No tracking, cookies, or analytics. No trips are logged.
- Works fully client-side with no backend beyond CDN font loading.

---

## Licence

MIT — see `LICENSE`. Transport for NSW brand marks and NSW Government visual identity remain the property of the State of New South Wales; this repository uses the design system's published colour tokens under fair use for a non-commercial concept demonstration.

---

## AI acknowledgement

Parts of this project were built with the assistance of [Claude](https://claude.ai) (Anthropic). All prompting, direction, and editorial decisions were made by the project authors.

| Feature | Tool |
|---|---|
| Gauge cleanup — needle sizing, tick alignment, band opacity | Claude (Anthropic) |
| Zone labels (STRESSED / MODERATE / HEALTHY) repositioned inside arc | Claude (Anthropic) |
| Seamless ticker loop (JS `requestAnimationFrame` approach) | Claude (Anthropic) |

---

by Unit 8200
