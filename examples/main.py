import os
import json
from flask import Flask
from flask import request, jsonify, render_template

from murus import murus, Config
from murus import protected, limit
from murus import token

app = Flask(__name__)

config = Config()
config.REQUIRE_CLIENT_CERT = False # local

murus(app, config)

@app.route("/", methods = ["GET"])
@limit("1 per second")
def index():
    return render_template("index.html")

@app.route("/token", methods = ["POST"])
def generate_token():
    data = request.form
    if not data or "user_id" not in data:
        return jsonify({"error": "Missing 'user_id' in request."}), 400
    user_id = data["user_id"]
    additional_claims = json.loads(data.get("additional_claims", "{}"))
    generated = token.create(config, user_id = user_id, additional_claims = additional_claims)
    return render_template("generate_token.html", token = generated)

@app.route("/protected", methods = ["GET"])
@protected(token_func = lambda _: request.args.get("token"))
def protected_page(payload: dict):
    return render_template("protected.html", response = payload)

app.run(debug = True)

