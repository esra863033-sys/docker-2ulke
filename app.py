from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

COUNTRY_MAP = {
    "türkiye": "turkey",
    "almanya": "germany",
    "fransa": "france",
    "italya": "italy",
    "ispanya": "spain",
    "japonya": "japan",
    "kanada": "canada"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country")
def country():
    name = request.args.get("name", "").lower()
    api_name = COUNTRY_MAP.get(name, name)

    url = f"https://restcountries.com/v3.1/name/{api_name}"
    res = requests.get(url)

    if res.status_code != 200:
        return jsonify({"error": "Ülke bulunamadı"})

    data = res.json()[0]

    result = {
        "name": data["name"]["common"],
        "capital": data["capital"][0],
        "population": data["population"],
        "continent": data["continents"][0],
        "region": data["region"],
        "currency": list(data["currencies"].values())[0]["name"],
        "language": list(data["languages"].values())[0],
        "flag": data["flags"]["png"],
        "lat": data["latlng"][0],
        "lng": data["latlng"][1]
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
