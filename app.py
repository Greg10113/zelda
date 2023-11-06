from flask import Flask, render_template
import requests

app = Flask(__name__)

zeldaURL = "https://zelda.fanapis.com/api/games"
characters_URL = "https://zelda.fanapis.com/api/characters?limit=100"
monster_URL = "https://zelda.fanapis.com/api/monsters?limit=100"
bossURL = "https://zelda.fanapis.com/api/bosses?limit=100"


def compendium_categories(category):
    URL = f"https://botw-compendium.herokuapp.com/api/v3/compendium/category/{category}"
    return URL


def fetch_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        return []


compendium_creatures = fetch_data(compendium_categories('creatures'))
compendium_equipment = fetch_data(compendium_categories('equipment'))
compendium_materials = fetch_data(compendium_categories('materials'))
compendium_monsters = fetch_data(compendium_categories('monsters'))
compendium_treasure = fetch_data(compendium_categories('treasure'))


zelda = fetch_data(zeldaURL)
characters = fetch_data(characters_URL)
monsters = fetch_data(monster_URL)
bosses = fetch_data(bossURL)

all_characters = []
for x in characters:
    all_characters.append(x)

# print(characters)


for x in zelda:
    b = x["developer"]
    if b == "Nintendo":
        print(b)

nintendo_dev = []
not_nintendo_dev = []

for x in zelda:
    if "Nintendo" in x["developer"]:
        nintendo_dev.append(x)
    else:
        not_nintendo_dev.append(x)


for x in nintendo_dev:
    print(x["developer"])

print("---------")

for x in not_nintendo_dev:
    print(x['developer'])


@app.route("/games")
def games():
    return render_template("index.html", nintendo_dev=nintendo_dev, not_nintendo_dev=not_nintendo_dev)


@app.route("/characters")
def characters():
    return render_template("characters.html", characters=all_characters, monsters=monsters, bosses=bosses)


@app.route("/compendium")
def compendium():
    return render_template("botw.html",
                           len=len,
                           creatures=compendium_creatures,
                           equipment=compendium_equipment,
                           materials=compendium_materials,
                           monsters=compendium_monsters,
                           treasure=compendium_treasure
                           )


if __name__ == "__main__":
    app.run(debug=True, port=8000)
