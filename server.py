from flask import Flask, jsonify, request, render_template, redirect
import json
import os

CONFIG_FILE = "config.json"

app = Flask(__name__)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    configs = load_config()
    return render_template("index.html", configs=configs)

@app.route("/update/<worker>", methods=["POST"])
def update(worker):
    configs = load_config()
    if worker not in configs:
        return "Worker not found", 404
    configs[worker]["algo"] = request.form["algo"]
    configs[worker]["pool"] = request.form["pool"]
    configs[worker]["wallet"] = request.form["wallet"]
    configs[worker]["threads"] = int(request.form["threads"])
    save_config(configs)
    return redirect("/")

@app.route("/api/config")
def api_config():
    worker = request.args.get("worker")
    configs = load_config()
    if not worker or worker not in configs:
        return jsonify({"error": "Worker not found"}), 404
    return jsonify(configs[worker])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
