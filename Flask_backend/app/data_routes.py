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

@app.route('/all_orders')
def all_order_data():
    # try:
    #     # Run the Node.js script and capture the output
    #     result = subprocess.run(
    #         ['node', '../node_backend/data.js'],  # Replace with your actual path to Node.js script
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE
    #     )
        
    #     # Check if the Node.js script ran successfully
    #     if result.returncode != 0:
    #         return jsonify({"error": result.stderr.decode('utf-8')}), 500

    #     # Read the JSON output file generated by the Node.js script
    #     with open('open_orders.json', 'r') as file:
    #         open_orders = json.load(file)

    #     return jsonify(open_orders), 200

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    
    Node_All_Data_API_URL = f"{app.config["Atlas_data"]}/api/get_all_open_orders"
    
    try:
        # Send a GET request to the Node.js API
        response = requests.get(Node_All_Data_API_URL)

        # If the request was successful, return the response from Node.js
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Node.js API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/item_detail/<mintid>', methods=['GET'])
def get_item_detials_by_mint_id(mintid):
    
    
    if mintid in app.config["Item_data"]:
        return jsonify(app.config["Item_data"][mintid])
    
    return jsonify({"error": "Item not found"})



@app.route('/orders_by_assets/<assets>', methods=['GET'])
def order_data_by_assets(assets):

    
    #  add asset_id to the request query
    assets = str(assets)
    
    
    Node_All_Data_API_URL = f"{app.config["Atlas_data"]}/api/get_open_orders_from_asset"
    
    
    try:
        # Send a GET request to the Node.js API
        response = requests.post(Node_All_Data_API_URL, params={"asset_id": assets})

        # If the request was successful, return the response from Node.js
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Node.js API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

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