from flask import Flask, request, jsonify, render_template
from app import app

from flask import Flask, render_template, send_from_directory,jsonify
# import subprocess
import requests
import json

import uuid

from functools import wraps 




NODE_API_URL = f"{app.config["Atlas_data"]}"



@app.route('/item_detail/<mintid>', methods=['GET'])
def get_item_detials_by_mint_id(mintid):
    
    
    if mintid in app.config["Item_data"]:
        return jsonify(app.config["Item_data"][mintid])
    
    return jsonify({"error": "Item not found"})




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



@app.route('/player_details')
@extract_account
def player_details(account):
    account = str(account)
    
    star_atlas_url = f"https://galaxy.staratlas.com/players/{account}"
    
    print(star_atlas_url)
    
    try:
        # Send a GET request to the Star Atlas API
        response = requests.get(star_atlas_url)

        print(response)
        
        # If the request was successful, return the response from Star Atlas
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Star Atlas API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/profile_details')
@extract_account
def profile_details(account):
    account = str(account)
    
    star_atlas_url = f"https://galaxy.staratlas.com/profiles/{account}"
    
    try:
        # Send a GET request to the Star Atlas API
        response = requests.get(star_atlas_url)

        # If the request was successful, return the response from Star Atlas
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Star Atlas API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rewards_details/<account>')
def rewards_details(account):
    account = str(account)
    
    star_atlas_url = f"https://galaxy.staratlas.com/rewards/{account}"
    
    try:
        # Send a GET request to the Star Atlas API
        response = requests.get(star_atlas_url)

        # If the request was successful, return the response from Star Atlas
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Star Atlas API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


