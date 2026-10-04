#!/usr/bin/env python3
"""
Refresh live indicators for the diesel import reduction framework.

Writes diesel-framework/data/live.json. Each source is fetched independently;
if one fails, its last good value is kept and marked stale, so the page and
Joule always have something to show.

Sources (no API keys needed):
  - Brent crude, US Gulf Coast ultra-low sulfur diesel, USD per AUD: FRED CSV
  - NEM wholesale price and demand by region: AEMO data dashboard API
  - Retail diesel price and stock outlook: fuelplan.gov.au
  - Australian diesel stock (ML and days): best-effort parse of fuelplan.gov.au
    and DCCEEW pages; currently published in words only, so the last known
    figure is kept and marked stale

Standard library only, so the GitHub Action needs no installs.
Author: Andrew Baker
"""

import csv
import io
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "diesel-framework" / "data" / "live.json"
UA = "Mozilla/5.0 (diesel-framework live data; github.com/ajcbWIPs/energy-policy)"
LITRES_PER_BARREL = 158.987
LITRES_PER_US_GALLON = 3.78541

FRED_SERIES = {
    "brent_usd_bbl": "DCOILBRENTEU",
    "us_gulf_ulsd_usd_gal": "DDFUELUSGULF",
    "usd_per_aud": "DEXUSAL",
}
AEMO_URL = "https://visualisations.aemo.com.au/aemo/apps/api/report/ELEC_NEM_SUMMARY"
STOCK_PAGES = [
    "https://fuelplan.gov.au/fuel-statistics",
    "https://www.dcceew.gov.au/energy/security/australias-fuel-security/minimum-stockholding-obligation/statistics",
]


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_fred_csv(text):
    """Return (date, value) of the latest non-missing observation."""
    rows = list(csv.reader(io.StringIO(text)))
    for row in reversed(rows[1:]):
        if len(row) >= 2 and row[1] not in ("", "."):
            return row[0], float(row[1])
    raise ValueError("no observations")


def fetch_fred(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    date, value = parse_fred_csv(get(url))
    return {"value": value, "as_of": date, "source": f"https://fred.stlouisfed.org/series/{series_id}"}


def parse_aemo(payload):
    rows = payload.get("ELEC_NEM_SUMMARY") or []
    regions = {}
    for r in rows:
        region = r.get("REGIONID")
        if not region:
            continue
        regions[region] = {
            "price_aud_mwh": r.get("PRICE"),
            "demand_mw": r.get("TOTALDEMAND"),
            "as_of": r.get("SETTLEMENTDATE"),
        }
    if not regions:
        raise ValueError("no NEM regions in response")
    return regions


def fetch_aemo():
    regions = parse_aemo(json.loads(get(AEMO_URL)))
    return {"regions": regions, "source": "https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem"}


def html_to_text(html):
    html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text)


def parse_diesel_stock(text):
    """Find the diesel stock in ML and days of cover in page text.

    Looks for 'diesel' followed closely by an 'N,NNN ML' figure and an 'NN days'
    figure, in either order. Rejects implausible values.
    """
    matches = list(re.finditer(r"(?i)diesel", text))
    # Prefer figures after the word, then fall back to a sentence that names them first.
    for before in (0, 150):
        for m in matches:
            window = text[max(0, m.start() - before): m.start() + 400]
            ml = re.search(r"(\d{1,2},\d{3}|\d{3,5})\s*(?:ML|megalitres)", window, re.I)
            days = re.search(r"(\d{1,3}(?:\.\d)?)\s*days", window, re.I)
            if ml and days:
                ml_v = float(ml.group(1).replace(",", ""))
                days_v = float(days.group(1))
                if 500 <= ml_v <= 10000 and 3 <= days_v <= 120:
                    return ml_v, days_v
    raise ValueError("diesel stock figures not found")


def parse_fuelplan(text):
    """Read retail diesel prices and the stock outlook from fuelplan.gov.au.

    The page gives stock levels in words (no ML or days figures), plus a retail
    price table: 'Retail prices <date> ... Petrol Diesel 5 largest cities* $P (+x%) $D (+y%)'.
    """
    m = re.search(
        r"Retail prices\s+(\d{1,2} \w+ \d{4}).*?5 largest cities\*?\s+\$(\d+\.\d{2})\s*\(([+-]?\d+)%\)\s+\$(\d+\.\d{2})\s*\(([+-]?\d+)%\)",
        text, re.I | re.S)
    if not m:
        raise ValueError("retail price table not found")
    date = datetime.strptime(m.group(1), "%d %B %Y").date().isoformat()
    diesel = float(m.group(4))
    if not 1.0 <= diesel <= 6.0:
        raise ValueError(f"implausible diesel price {diesel}")
    out = {
        "retail_diesel_aud_l": diesel,
        "retail_diesel_change_7d_pct": int(m.group(5)),
        "retail_petrol_aud_l": float(m.group(2)),
        "as_of": date,
        "source": STOCK_PAGES[0],
    }
    # City rows follow the 5-city average, e.g. 'SYD $2.39 (+6%) $2.85 (+7%)'.
    cities = {}
    table = text[m.start(): m.start() + 1500]
    for code, petrol, pchg, dsl, dchg in re.findall(
            r"\b([A-Z]{3})\*?\s+\$(\d+\.\d{2})\s*\(([+-]?\d+)%\)\s+\$(\d+\.\d{2})\s*\(([+-]?\d+)%\)", table):
        if 1.0 <= float(dsl) <= 6.0 and 1.0 <= float(petrol) <= 6.0:
            cities.setdefault(code, {
                "petrol_aud_l": float(petrol), "petrol_change_7d_pct": int(pchg),
                "diesel_aud_l": float(dsl), "diesel_change_7d_pct": int(dchg),
            })
    out["cities"] = cities
    print(f"retail price table on fuelplan: {table[:700]!r}")
    outlook = re.search(r"([^.]*\bdiesel\b[^.]*stocks?[^.]*\.|[^.]*stocks?[^.]*\bdiesel\b[^.]*\.)", text, re.I)
    if outlook:
        out["stock_outlook"] = outlook.group(1).strip()
    return out


def fetch_fuelplan():
    return parse_fuelplan(html_to_text(get(STOCK_PAGES[0])))


def fetch_stock():
    errors = []
    for url in STOCK_PAGES:
        html = ""
        try:
            html = get(url)
            ml, days = parse_diesel_stock(html_to_text(html))
            return {"diesel_ml": ml, "diesel_days": days, "source": url}
        except Exception as e:  # keep trying the next page
            errors.append(f"{url}: {e}")
            # Pages that render figures in the browser load them from a data file;
            # list candidates in the run log so the parser can be pointed at one.
            hints = sorted(set(re.findall(r"""["'(]([^"'()\s]*(?:\.json|\.csv|\.xlsx|/api/)[^"'()\s]*)""", html)))
            if hints:
                print(f"data file candidates on {url}: {hints[:20]}")
            m = re.search(r"(?i)diesel", html_to_text(html))
            if m:
                text = html_to_text(html)
                print(f"text near 'diesel' on {url}: {text[max(0, m.start() - 100): m.start() + 300]!r}")
    raise RuntimeError("; ".join(errors))


def derived(ind):
    """Convert benchmark prices to Australian cents per litre."""
    out = {}
    aud = ind.get("usd_per_aud", {}).get("value")
    if not aud:
        return out
    brent = ind.get("brent_usd_bbl", {}).get("value")
    ulsd = ind.get("us_gulf_ulsd_usd_gal", {}).get("value")
    if brent:
        out["brent_aud_c_per_l"] = round(brent / aud / LITRES_PER_BARREL * 100, 1)
    if ulsd:
        out["us_gulf_ulsd_aud_c_per_l"] = round(ulsd / aud / LITRES_PER_US_GALLON * 100, 1)
    return out


def refresh(previous):
    ind = dict(previous.get("indicators", {}))
    status = {}

    def run(key, fn):
        try:
            ind[key] = {**fn(), "fetched": now_iso(), "stale": False}
            status[key] = "ok"
        except Exception as e:
            if key in ind:
                ind[key] = {**ind[key], "stale": True}
            status[key] = f"failed: {e}"

    for key, series in FRED_SERIES.items():
        run(key, lambda s=series: fetch_fred(s))
    run("nem", fetch_aemo)
    run("retail_fuel", fetch_fuelplan)
    run("diesel_stock", fetch_stock)

    return {
        "updated": now_iso(),
        "framework_doc": previous.get("framework_doc"),
        "indicators": ind,
        "derived": derived(ind),
        "status": status,
    }


def main():
    previous = json.loads(OUT.read_text()) if OUT.exists() else {}
    data = refresh(previous)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    for key, s in data["status"].items():
        print(f"{key}: {s}")
    # Fail the run only if every source failed, so one outage doesn't page anyone.
    if all(s != "ok" for s in data["status"].values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
