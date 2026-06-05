import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =========================
# SETTINGS FILE HANDLER
# =========================

def load_settings():
    if not os.path.exists("settings.json"):
        data = {
            "password": "11",
            "cheat_code": "freeway",
            "gallery": [],
            "achievements": []
        }
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)
        return data

    with open("settings.json", "r") as f:
        return json.load(f)


def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# PAGES
# =========================
@app.route("/check-cheat", methods=["POST"])
def check_cheat():
    data = request.get_json()

    settings = load_settings()
    cheat_code = settings.get("cheat_code", "freeway")

    # SAFE CHECK (prevent server crash)
    if not data or "code" not in data:
        return jsonify({"success": False, "error": "No code sent"})

    if data["code"] == cheat_code:
        return jsonify({"success": True})

    return jsonify({"success": False})
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin.html")
def admin():
    return render_template("admin.html")

@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")

@app.route("/history.html")
def history():
    return render_template("history.html")

@app.route("/achievements.html")
def achievements():
    return render_template("achievements.html")

@app.route("/maze.html")
def maze():
    return render_template("maze.html")


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
# SETTINGS API
# =========================

@app.route("/get-settings")
def get_settings():
    return jsonify(load_settings())


@app.route("/save-settings", methods=["POST"])
def save_settings_route():
    data = request.get_json()
    settings = load_settings()

    settings["password"] = data["password"]
    settings["cheat_code"] = data["cheat_code"]

    save_settings(settings)
    return jsonify({"success": True})


# =========================
# GALLERY API
# =========================

@app.route("/get-gallery")
def get_gallery():
    return jsonify(load_settings().get("gallery", []))


@app.route("/save-gallery", methods=["POST"])
def save_gallery():
    data = request.get_json()
    settings = load_settings()

    settings["gallery"] = data["gallery"]

    save_settings(settings)
    return jsonify({"success": True})


# =========================
# ACHIEVEMENTS API
# =========================

@app.route("/get-achievements")
def get_achievements():
    return jsonify(load_settings().get("achievements", []))


@app.route("/save-achievements", methods=["POST"])
def save_achievements():
    data = request.get_json()
    settings = load_settings()

    settings["achievements"] = data["achievements"]

    save_settings(settings)
    return jsonify({"success": True})


# =========================
# RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
