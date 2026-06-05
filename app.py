import json
import os
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
            "cheat_code": "freeway",
            "gallery": []
        }
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)
        return data


def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin.html")
def admin():
    return render_template("admin.html")

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

    if data["email"] == "1" and data["password"] == settings["password"]:
        return jsonify({"success": True})

    return jsonify({"success": False})


# =========================
# SETTINGS GET
# =========================

@app.route("/get-settings")
def get_settings():
    return jsonify(load_settings())


# =========================
# SETTINGS SAVE (FIXED)
# =========================

@app.route("/save-settings", methods=["POST"])
def save_settings_route():
    data = request.get_json()
    settings = load_settings()

    settings["password"] = data.get("password", settings["password"])
    settings["cheat_code"] = data.get("cheat_code", settings["cheat_code"])

    save_settings(settings)

    return jsonify({"success": True})


# =========================
# CHEAT CODE
# =========================

@app.route("/check-cheat", methods=["POST"])
def check_cheat():
    data = request.get_json()
    settings = load_settings()

    if not data:
        return jsonify({"success": False})

    if data.get("code") == settings["cheat_code"]:
        return jsonify({"success": True})

    return jsonify({"success": False})


# =========================
# GALLERY
# =========================

@app.route("/get-gallery")
def get_gallery():
    return jsonify(load_settings().get("gallery", []))


@app.route("/save-gallery", methods=["POST"])
def save_gallery():
    data = request.get_json()
    settings = load_settings()

    settings["gallery"] = data.get("gallery", [])

    save_settings(settings)

    return jsonify({"success": True})


# =========================
# RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
