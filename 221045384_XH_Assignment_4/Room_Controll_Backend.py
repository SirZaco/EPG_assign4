from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

control_data = {
    "auto": True,
    "led_on": False,
    "fan_on": False,
    "motion": False
}

@app.route("/api/control", methods=["GET"])
def get_control():
    return jsonify({
        "auto": control_data["auto"],
        "led_on": control_data["led_on"],
        "fan_on": control_data["fan_on"]
    })

@app.route("/api/control", methods=["POST"])
def set_control():
    data = request.json
    control_data["auto"] = data.get("auto", control_data["auto"])
    control_data["led_on"] = data.get("led_on", control_data["led_on"])
    control_data["fan_on"] = data.get("fan_on", control_data["fan_on"])
    return jsonify({"status": "updated"})

@app.route("/api/motion", methods=["POST"])
def update_motion():
    data = request.json
    control_data["motion"] = data.get("motion", False)
    return jsonify({"status": "motion updated"})

@app.route("/api/motion", methods=["GET"])
def get_motion():
    return jsonify({"motion": control_data["motion"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5000)
