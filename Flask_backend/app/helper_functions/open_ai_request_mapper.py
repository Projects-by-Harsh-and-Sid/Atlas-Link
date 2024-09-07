
from app import app
from flask import Flask, request, jsonify, render_template
from functools import wraps 
import requests



# create a wrapper class that takes the reqest headers and gets the user id
# then fetches the user data from the star atlas api
# and returns the data to the user
def extract_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pairing_key = str(request.headers.get("Openai-Conversation-Id"))

        if pairing_key not in app.config["user_pairs"]:
            return jsonify({"error": "Invalid or missing pairing key"}), 400

        account = app.config["user_pairs"][pairing_key]
        return f(account, *args, **kwargs)

    return decorated_function