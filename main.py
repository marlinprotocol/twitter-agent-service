import json
from os import getenv, path
from flask import Flask, jsonify, request
from actions import generate_keys_and_access_tokens_actions, verify_encumbrance_actions

app = Flask(__name__)

@app.route("/generate_keys_and_access_tokens", methods=["GET"])
async def generate_keys_and_access_tokens():
    api_keys, access_tokens, timestamp = await generate_keys_and_access_tokens_actions()
    if api_keys and access_tokens:
        return jsonify({
            "api_keys": api_keys,
            "access_tokens": access_tokens,
            "timestamp": timestamp
        })
    else:
        return jsonify({"error": "Failed to retrieve tokens"}), 500

@app.route("/fetch_keys_and_tokens", methods=["GET"])
def fetch_keys_and_tokens():
    if path.exists("keys.json"):
        with open("keys.json", "r") as f:
            data = json.load(f)
            if data:
                return jsonify(data)
            else:
                return jsonify({"error": "Access tokens and API keys are not present"}), 404
    else:
        return jsonify({"error": "Access tokens and API keys not found, try generating them with the /generate_keys_and_access_tokens endpoint."}), 404

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
    app.run(host="0.0.0.0", port=8000, debug=True)