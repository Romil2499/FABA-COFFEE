import json
import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =========================
# SETTINGS FILE HANDLING
# =========================

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
       data = {
    "password": "11",
    "cheat_code": "freeway",
    "recovery_code": "",
    "security_question": "What is your favorite coffee?",
    "security_answer": "latte"
}

        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)

        return data


def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# RANDOM RECOVERY CODE
# =========================

def generate_code():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=12)
    )


@app.route("/generate-recovery", methods=["POST"])
def generate_recovery():
    settings = load_settings()

    code = generate_code()
    settings["recovery_code"] = code

    save_settings(settings)

    return jsonify({
        "success": True,
        "code": code
    })


# =========================
# PAGES
# =========================
@app.route("/verify-answer", methods=["POST"])
def verify_answer():

    data = request.get_json()
    settings = load_settings()

    if (
        data["answer"].lower()
        ==
        settings["security_answer"].lower()
    ):

        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False
    })
@app.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    settings = load_settings()

    settings["password"] = data["password"]

    save_settings(settings)

    return jsonify({
        "success": True
    })

    data = request.get_json()

    settings = load_settings()

    settings["password"] = data["password"]

    save_settings(settings)

    return jsonify({
        "success": True
    })
@app.route("/verify-recovery", methods=["POST"])
def verify_recovery():

    data = request.get_json()
    settings = load_settings()

    if data["recovery_code"] == settings["recovery_code"]:

        return jsonify({
            "success": True,
            "question": settings["security_question"]
        })

    return jsonify({
        "success": False
    })
@app.route("/recover.html")
def recover():
    return render_template("recover.html")
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
        data.get("email") == "1"
        and data.get("password") == settings["password"]
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

    if data.get("code") == cheat_code:
        return jsonify({"success": True})

    return jsonify({"success": False})


# =========================
# SAVE SETTINGS
# =========================

@app.route("/save-settings", methods=["POST"])
def save_settings_route():
    data = request.get_json()
    settings = load_settings()

    settings["password"] = data.get("password", settings["password"])
    settings["cheat_code"] = data.get("cheat_code", settings["cheat_code"])

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
    return jsonify(load_settings())


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
