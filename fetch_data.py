"""
fetch_data.py — standalone script to fetch and display wine data from the API.
Run with: python fetch_data.py
"""

import requests

API_BASE_URL = "https://my-json-server.typicode.com/GITHUB_USERNAME/REPO_NAME"


def fetch_wines():
    response = requests.get(f"{API_BASE_URL}/wines")
    response.raise_for_status()
    return response.json()


def fetch_countries():
    response = requests.get(f"{API_BASE_URL}/countries")
    response.raise_for_status()
    return response.json()


def print_separator(char="-", length=60):
    print(char * length)


def format_price(price):
    if price is None:
        return "n.v.t."
    return f"€{price:.2f}"


def print_wine(wine, index=None):
    prefix = f"  [{index}] " if index is not None else "  "
    print(f"{prefix}{wine['name']} ({wine.get('vintage', '?')})")
    print(f"      Stijl      : {wine.get('style', '?')}")
    print(f"      Druif      : {wine.get('grapes', '?')}")
    print(f"      Regio      : {wine.get('region', '?')}")
    print(f"      Per fles   : {format_price(wine.get('priceBottle'))}")
    if wine.get("byGlass"):
        print(f"      Per glas   : {format_price(wine.get('priceGlass'))}")
    print()


def main():
    print("=" * 60)
    print("  HouseYourWine — Gegevens ophalen via API")
    print("=" * 60)

    print("\nLanden ophalen...")
    countries = fetch_countries()
    country_map = {c["id"]: c["name"] for c in countries}

    print(f"  {len(countries)} landen gevonden.\n")
    print_separator()
    print("LANDEN:")
    print_separator()
    for country in countries:
        print(f"  [{country['id']}] {country['name']}")
    print()

    print("Wijnen ophalen...")
    wines = fetch_wines()
    print(f"  {len(wines)} wijnen gevonden.\n")

    print_separator("=")
    print("ALLE WIJNEN:")
    print_separator("=")
    for i, wine in enumerate(wines, start=1):
        print_wine(wine, index=i)

    print_separator("=")
    print("WIJNEN PER LAND:")
    print_separator("=")

    wines_by_country = {}
    for wine in wines:
        cid = wine.get("countryId")
        wines_by_country.setdefault(cid, []).append(wine)

    for country in countries:
        cid = country["id"]
        country_wines = wines_by_country.get(cid, [])
        if not country_wines:
            continue
        print(f"\n{country['name'].upper()} ({len(country_wines)} wijn(en)):")
        print_separator()
        for wine in country_wines:
            print_wine(wine)

    print_separator("=")
    print(f"Totaal: {len(wines)} wijnen uit {len(countries)} landen.")
    print_separator("=")


if __name__ == "__main__":
    main()
