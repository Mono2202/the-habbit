import json

from flask import Flask, jsonify
from flask_cors import CORS
from functools import wraps

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

@app.route("/api/xp/get_goal_xp")
@user_context
def get_goal_xp():
    return jsonify({"goal_xp": 50})

@app.route("/api/add_<xp>")
@user_context
def gain_xp(xp):
    global user_xp
    user_xp += int(xp)
    print(user_xp)
    return jsonify({"XP GAIN": f"{xp}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)
