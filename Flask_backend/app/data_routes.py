from flask import Flask, request, jsonify, render_template
from app import app

from flask import Flask, render_template, send_from_directory,jsonify
# import subprocess
import requests
import json

import uuid


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


NODE_API_URL = f"{app.config["Atlas_data"]}"



@app.route('/item_detail/<mintid>', methods=['GET'])
def get_item_detials_by_mint_id(mintid):
    
    
    if mintid in app.config["Item_data"]:
        return jsonify(app.config["Item_data"][mintid])
    
    return jsonify({"error": "Item not found"})







@app.route('/player_details/<account>')
def player_details(account):
    
    account = str(account)
    
    star_atlas_url = f"https://galaxy.staratlas.com/players/{account}"
    
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

    
@app.route('/profile_details/<account>')
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


@app.route('/transaction_details.json')
def transaction_details():
    return send_from_directory('static', 'transaction_details.json')