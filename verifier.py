import json
import hashlib
from os import getenv, path, urandom
from flask import Flask, jsonify
from actions import verify_encumbrance_actions

app = Flask(__name__)

def derive_kms_password():
    binary_data = b'\xf0\x00\xad\tX\x0eYy\xc3M\xc9\x1bq\x86&\xfe\xe2\x91h\xe4\xbdg\x08\x90\xd8\xd9m#]\x93\x17\xc4' 
    hashed_password = hashlib.sha256(binary_data).hexdigest()
    return hashed_password

# Store the hashed password in the app state
app.config['KMS_GENERATED_PASSWORD'] = derive_kms_password()

@app.route("/verify_encumbrance", methods=["GET"])
async def verify_encumbrance():
    username = getenv("USERNAME")
    kms_generated_password = app.config['KMS_GENERATED_PASSWORD']

    if not await verify_encumbrance_actions(kms_generated_password):
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