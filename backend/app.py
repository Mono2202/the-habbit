import json

from functools import wraps

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HABIT_DIFFICULTIES = {
    "Easy": 1,
    "Medium": 3,
    "Hard": 5,
    "Extreme": 10
}

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
    return jsonify({"level": app.config["user"]["level"]})

@app.route("/api/xp/get_xp")
@user_context
def get_xp():
    return jsonify({"xp": app.config["user"]["xp"]})

@app.route("/api/xp/get_xp_goal")
@user_context
def get_xp_goal():
    return jsonify({"xp_goal": app.config["user"]["xp_goal"]})

@app.route("/api/xp/gain_xp", methods=["GET"])
@user_context
def gain_xp():
    xp_to_add = request.args.get("xp", type=int)

    if xp_to_add is None:
        return jsonify({"error": "Missing xp"}), 400
    
    gain_xp_handle(xp_to_add)
    return Response(status=200)

@app.route("/api/xp/complete_habit", methods=["GET"])
@user_context
def complete_habit():
    habit_difficulty = request.args.get("difficulty", type=str)

    if habit_difficulty is None:
        return jsonify({"error": "Missing habit difficulty"}), 400
    
    gain_xp_handle(HABIT_DIFFICULTIES[habit_difficulty])
    return Response(status=200)

def gain_xp_handle(xp_to_add: int):
    app.config["user"]["xp"] += xp_to_add
    app.config["user"]["overall_xp"] += xp_to_add

    while app.config["user"]["xp"] >= app.config["user"]["xp_goal"]:
        app.config["user"]["level"] += 1
        app.config["user"]["xp"] -= app.config["user"]["xp_goal"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)
