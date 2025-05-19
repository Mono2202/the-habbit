from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
user_xp = 0

@app.route("/")
def home():
    return jsonify({"message": "Hello, wekk!"})

@app.route("/api/add_<xp>")
def gain_xp(xp):
    global user_xp
    user_xp += int(xp)
    print(user_xp)
    return jsonify({"XP GAIN": f"{xp}"})

@app.route("/api/get_xp")
def get_xp():
    global user_xp
    return jsonify({"xp": f"{user_xp}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)
