from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/derive", methods=["GET"])
def derive():
    path = request.args.get("path")
    if path == "xagentpwd":
        return "test@pwd"
    else:
        return jsonify({"error": "Invalid path"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1100, debug=True)