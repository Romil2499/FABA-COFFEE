import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =========================
# SETTINGS
# =========================

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        data = {
            "password": "11",
            "cheat_code": "freeway"
        }

        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)

        return data


def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# PAGES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/maze.html")
def maze():
    return render_template("maze.html")


@app.route("/admin.html")
def admin():
    return render_template("admin.html")


@app.route("/history.html")
def history():
    return render_template("history.html")


@app.route("/achievements.html")
def achievements():
    return render_template("achievements.html")


@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    settings = load_settings()

    if (
        data["email"] == "1"
        and data["password"] == settings["password"]
    ):
        return jsonify({"success": True})

    return jsonify({"success": False})


# =========================
# CHEAT CHECK
# =========================

@app.route("/check-cheat", methods=["POST"])
def check_cheat():

    data = request.get_json()
    settings = load_settings()

    cheat_code = settings.get("cheat_code", "freeway")

    if data["code"] == cheat_code:
        return jsonify({"success": True})

    return jsonify({"success": False})
# =========================
# SAVE SETTINGS
# =========================

@app.route("/save-settings", methods=["POST"])
def save_settings_route():

    data = request.get_json()

    settings = load_settings()

    settings["password"] = data["password"]
    settings["cheat_code"] = data["cheat_code"]

    save_settings(settings)

    return jsonify({
        "success": True,
        "message": "Settings Saved"
    })


# =========================
# GET SETTINGS
# =========================

@app.route("/get-settings")
def get_settings():

    settings = load_settings()

    return jsonify(settings)


if __name__ == "__main__":
    app.run(debug=True)