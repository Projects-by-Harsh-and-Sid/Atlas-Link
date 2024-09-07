
from flask import Flask, request, jsonify, render_template
from app import app

from flask import Flask, render_template, send_from_directory,jsonify
# import subprocess
import requests
import json

from app.helper_functions.order_book import process_orders_assets, calculate_orderbook_summary


import uuid

@app.route('/all_orders')
def all_order_data():

    
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


@app.route('/orders_by_assets_raw/<assets>', methods=['GET'])
def order_data_by_assets_raw(assets):

    
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






@app.route('/orders_by_assets/<mint_id>', methods=['GET'])
def order_data_by_assets(mint_id):

    
    #  add asset_id to the request query
    assets = str(mint_id)
    
    
    Node_All_Data_API_URL = f"{app.config["Atlas_data"]}/api/get_open_orders_from_asset"
    
    
    try:
        # Send a GET request to the Node.js API
        response = requests.post(Node_All_Data_API_URL, params={"asset_id": assets})

        # If the request was successful, return the response from Node.js
        if response.status_code == 200:
            
            data = response.json()
            
            if data.get('count')<1:
                return jsonify({
                    "error": "No orders found",
                    "status_code": response.status_code
                }), response.status_code
                
            processed_orders_assets = process_orders_assets(data)
            return processed_orders_assets, 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Node.js API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500






@app.route('/orderbook_summary/<mint_id>', methods=['GET'])
def get_orderbook_summary(mint_id):
    Node_All_Data_API_URL = f"{app.config['Atlas_data']}/api/get_open_orders_from_asset"
    
    try:
        response = requests.post(Node_All_Data_API_URL, params={"asset_id": mint_id})
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('count', 0) < 1:
                return jsonify({
                    "error": "No orders found",
                    "status_code": response.status_code
                }), 404
            
            processed_orders = process_orders_assets(data)
            buy_orders = processed_orders['buy_orders']
            sell_orders = processed_orders['sell_orders']
            
            summary = {
                'buy_orders': calculate_orderbook_summary(buy_orders),
                'sell_orders': calculate_orderbook_summary(sell_orders),
                'spread': float(sell_orders[0]['price_usdc'] - buy_orders[0]['price_usdc']) if sell_orders and buy_orders else None,
                'mid_price': float((sell_orders[0]['price_usdc'] + buy_orders[0]['price_usdc']) / 2) if sell_orders and buy_orders else None,
            }
            
            return jsonify(summary), 200
        else:
            return jsonify({
                "error": "Failed to fetch data from Node.js API",
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500