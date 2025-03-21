import json
import hashlib
from os import getenv, path, urandom
from flask import Flask, jsonify
from actions import verify_encumbrance_actions
import requests

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

@app.route("/verify_encumbrance", methods=["GET"])
async def verify_encumbrance():
    username = getenv("USERNAME")

    kms_generated_password = app.config['KMS_GENERATED_PASSWORD']
    print(f"KMS generated password: {kms_generated_password}")
    if not await verify_encumbrance_actions(kms_generated_password):
        return jsonify({"message": "Accounts are not encumbered"})
    else:
        if path.exists("/app/shared_data/keys.json"):
            with open("/app/shared_data/keys.json", "r") as f:
                data = json.load(f)
                timestamp = data.get("timestamp", "unknown time")
                return jsonify({"message": f"Twitter account {username} is encumbered and the api keys and access tokens were generated on {timestamp}"})
        else:
            return jsonify({"message": f"No timestamp for keys and tokens generation was found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)