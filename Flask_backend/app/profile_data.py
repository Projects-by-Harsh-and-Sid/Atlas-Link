
from flask import Flask, request, jsonify, render_template,send_from_directory
from app import app
# import subprocess
import requests
import json
import uuid

from app.helper_functions.open_ai_request_mapper import extract_account

from app.helper_functions.profile_data import fetch_star_atlas_data, format_player_data, process_player_items


NODE_API_URL = f"{app.config["Atlas_data"]}"



@app.route('/validate_authentication_route', methods=['GET'])
@extract_account
def validate_authentication(account):
    if account:
        # If account is present, it means the user is authenticated
        return jsonify({
            "public_key": str(account),
            "is_authenticated": True
        }), 200
    else:
        # If account is None, it means the user is not authenticated
        return jsonify({
            "public_key": None,
            "is_authenticated": False
        }), 200  # Note: Returning 200 even for non-authenticated users, as this is a validation check


@app.route('/player_details')
@extract_account
def player_details(account):
    try:
        data = fetch_star_atlas_data(str(account))
        formatted_data = format_player_data(data)
        formatted_data["items"] = process_player_items(data, app.config["reverse_map"])
        return jsonify(formatted_data), 200
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
    

