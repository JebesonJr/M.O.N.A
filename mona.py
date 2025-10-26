from flask import Flask, render_template, request, redirect, jsonify
import json, os

app = Flask(__name__)

DATA_PATH = "accounts.json"
GLOBAL_PATH = "global_data.json"

def load_data(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_data(DATA_PATH)
        username = request.form["username"]
        email = request.form["email"]
        users[username] = {"email": email, "approved": False}
        save_data(DATA_PATH, users)
        return redirect("/validate")
    return render_template("register.html")

@app.route("/validate")
def validate():
    return render_template("validate.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == "@Brasil1248":
            return redirect("/admin_panel")
    return render_template("admin_login.html")

@app.route("/admin_panel")
def admin_panel():
    users = load_data(DATA_PATH)
    return render_template("admin_panel.html", users=users)

@app.route("/approve/<username>")
def approve(username):
    users = load_data(DATA_PATH)
    if username in users:
        users[username]["approved"] = True
        save_data(DATA_PATH, users)
    return redirect("/admin_panel")

@app.route("/api/global")
def global_data():
    return jsonify(load_data(GLOBAL_PATH))

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
