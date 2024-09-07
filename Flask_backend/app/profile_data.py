
from flask import Flask, request, jsonify, render_template,send_from_directory
from app import app
# import subprocess
import requests
import json
import uuid

from app.helper_functions.open_ai_request_mapper import extract_account




NODE_API_URL = f"{app.config["Atlas_data"]}"



# Route to get user information based on pairing key
@app.route('/get_user_info', methods=['GET'])
@extract_account
def get_user_info(account):
    pairing_key = str(account)

    user_id = app.config["user_pairs"][pairing_key]
    # Simulate fetching user info
    user_info = {
        "user_id": user_id,
        "account_info": "Some account-related info here."
    }
    return jsonify(user_info)
    





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

@app.route('/rewards_details')
@extract_account
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
    

