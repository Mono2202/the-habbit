from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello, w!"})

@app.route("/api/receive", methods=["POST"])
def receive():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
