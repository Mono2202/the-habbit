import json

from functools import wraps

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def user_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open("db.json", "r") as db_file:
            app.config["user"] = json.load(db_file)
        result = func(*args, **kwargs)
        with open("db.json", "w") as db_file:
            json.dump(app.config["user"], db_file, indent=4)
        return result
    return wrapper

@app.route("/api/xp/get_level")
@user_context
def get_level():
    return jsonify({"level": f"{app.config["user"]["level"]}"})

@app.route("/api/xp/get_xp")
@user_context
def get_xp():
    return jsonify({"xp": f"{app.config["user"]["xp"]}"})

@app.route("/api/xp/get_xp_goal")
@user_context
def get_xp_goal():
    return jsonify({"xp_goal": f"{app.config["user"]["xp_goal"]}"})

@app.route("/api/xp/gain_xp", methods=["GET"])
@user_context
def gain_xp():
    xp_to_add = request.args.get("xp", type=int)

    if xp_to_add is None:
        return jsonify({"error": "Missing xp"}), 400
    
    gain_xp_handle(xp_to_add)
    return Response(status=200)

def gain_xp_handle(xp_to_add: int):
    app.config["user"]["xp"] += xp_to_add
    app.config["user"]["overall_xp"] += xp_to_add

    while app.config["user"]["xp"] >= app.config["user"]["xp_goal"]:
        app.config["user"]["level"] += 1
        app.config["user"]["xp"] -= app.config["user"]["xp_goal"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)
