
# =============================================================================
# Bronnen
# =============================================================================
# - Canvas cursus: cursusmateriaal over REST API's, Flask en JSON-servers (31/03/2026)
#
# - Eigen project: HouseYourWine — een full-stack wijnbeheerapplicatie die ik
#   zelf aan het ontwikkelen ben. De wijndata en algemene structuur van deze
#   opdracht zijn gebaseerd op dat project.
#
# - my-json-server — gebruikt als nep-REST API voor de wijndata (31/03/2026)
# 
# - Claude Code (claude.ai) — gebruikt als AI-assistent bij de opmaak/stijl van
#   de website en het parsen van de JSON-tagstructuur (31/03/2026)
# =============================================================================

from flask import Flask, render_template, request, redirect, url_for, abort
import requests

app = Flask(__name__)

API_BASE_URL = "https://my-json-server.typicode.com/MichaelKaethoven/api_opdracht_4"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_wines():
    """Fetch all wines from the API. Returns a list; each item gets a 1-based id."""
    response = requests.get(f"{API_BASE_URL}/wines")
    response.raise_for_status()
    wines = response.json()
    # my-json-server assigns 1-based IDs by array position
    for i, wine in enumerate(wines, start=1):
        wine["id"] = i
    return wines


def get_countries():
    """Fetch all countries from the API."""
    response = requests.get(f"{API_BASE_URL}/countries")
    response.raise_for_status()
    return response.json()


def build_country_map(countries):
    return {c["id"]: c["name"] for c in countries}


def parse_tags(tags_str):
    """
    Parse the tags string into a structured dict.
    Example: "dry; body=medium; acidity=high; tannin=none; oak=none; profile=citrus,mineral"
    Returns: { "dry": True, "body": "medium", "acidity": "high", ... "profile": ["citrus","mineral"] }
    """
    result = {}
    if not tags_str:
        return result
    parts = [p.strip() for p in tags_str.split(";")]
    for part in parts:
        if "=" in part:
            key, _, value = part.partition("=")
            key = key.strip()
            value = value.strip()
            if key == "profile":
                result[key] = [v.replace("_", " ") for v in value.split(",")]
            elif key == "aging":
                result[key] = value.replace("_", " ")
            else:
                result[key] = value.replace("_", " ")
        else:
            result[part] = True
    return result


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("wines_list"))


@app.route("/wines")
def wines_list():
    style_filter = request.args.get("style", "").upper()
    country_filter = request.args.get("country", "")

    wines = get_wines()
    countries = get_countries()
    country_map = build_country_map(countries)

    # Apply filters
    if style_filter in ("WHITE", "RED", "ROSE"):
        wines = [w for w in wines if w.get("style") == style_filter]

    if country_filter:
        try:
            cid = int(country_filter)
            wines = [w for w in wines if w.get("countryId") == cid]
        except ValueError:
            pass

    return render_template(
        "wines.html",
        wines=wines,
        countries=countries,
        country_map=country_map,
        style_filter=style_filter,
        country_filter=country_filter,
    )


@app.route("/wines/<int:wine_id>")
def wine_detail(wine_id):
    wines = get_wines()
    countries = get_countries()
    country_map = build_country_map(countries)

    # wine_id is 1-based
    if wine_id < 1 or wine_id > len(wines):
        abort(404)

    wine = wines[wine_id - 1]
    tags = parse_tags(wine.get("tags", ""))

    return render_template(
        "wine_detail.html",
        wine=wine,
        country_map=country_map,
        tags=tags,
    )


@app.route("/countries")
def countries_list():
    wines = get_wines()
    countries = get_countries()

    # Count wines per country
    wine_counts = {}
    for wine in wines:
        cid = wine.get("countryId")
        wine_counts[cid] = wine_counts.get(cid, 0) + 1

    return render_template(
        "countries.html",
        countries=countries,
        wine_counts=wine_counts,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)