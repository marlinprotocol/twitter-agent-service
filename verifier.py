import json
from os import getenv, path
from flask import Flask, jsonify, request
from actions import verify_encumbrance_actions

app = Flask(__name__)

@app.route("/verify_encumbrance", methods=["GET"])
async def verify_encumbrance():
    username = getenv("USERNAME")
    if not await verify_encumbrance_actions():
        return jsonify({"message": "Accounts are not encumbered"})
    else:
        if path.exists("keys.json"):
            with open("keys.json", "r") as f:
                data = json.load(f)
                timestamp = data.get("timestamp", "unknown time")
                return jsonify({"message": f"Twitter account {username} is encumbered and the api keys and access tokens were generated on {timestamp}"})
        else:
            return jsonify({"message": f"Twitter account {username} is encumbered, but no timestamp for keys and tokens generation was found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)