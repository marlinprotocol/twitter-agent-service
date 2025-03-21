import json
import hashlib
from os import path, getenv
from flask import Flask, jsonify
import requests
from actions import generate_keys_and_access_tokens_actions

app = Flask(__name__)

def derive_kms_password():
    kms_endpoint = getenv("KMS_ENDPOINT", "http://127.0.0.1:1100")
    url=kms_endpoint+"/derive?path=xagentpwd"
    response = requests.get(url)
    if response.status_code == 200:
        binary_data = response.content
        hashed_password = hashlib.sha256(binary_data).hexdigest()
        return hashed_password
    else:
        raise Exception("Failed to fetch binary data")

# Store the hashed password in the app state
app.config['KMS_GENERATED_PASSWORD'] = derive_kms_password()

@app.route("/generate_keys_and_access_tokens", methods=["GET"])
async def generate_keys_and_access_tokens():
    kms_generated_password = app.config['KMS_GENERATED_PASSWORD']
    api_keys, access_tokens, timestamp = await generate_keys_and_access_tokens_actions(kms_generated_password)
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
    if path.exists("/app/shared_data/keys.json"):
        with open("/app/shared_data/keys.json", "r") as f:
            data = json.load(f)
            if data:
                return jsonify(data)
            else:
                return jsonify({"error": "Access tokens and API keys are not present"}), 404
    else:
        return jsonify({"error": "Access tokens and API keys not found, try generating them with the /generate_keys_and_access_tokens endpoint."}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)