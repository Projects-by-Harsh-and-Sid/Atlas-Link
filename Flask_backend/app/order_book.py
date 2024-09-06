
from flask import Flask, request, jsonify, render_template
from app import app

from flask import Flask, render_template, send_from_directory,jsonify
# import subprocess
import requests
import json

import uuid

import numpy as np

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




def process_orders_assets(data):
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    buy_orders = []
    sell_orders = []

    for order in data.get('orders', []):
        if order['currencyMint'] == usdc_mint:
            price_usdc = int(order['price'], 16) / 10**order['currencyDecimals']
            processed_order = {
                'id': order['id'],
                'price_usdc': price_usdc,
                'quantity': order['orderQtyRemaining']
            }
            
            if order['orderType'] == 'buy':
                buy_orders.append(processed_order)
            elif order['orderType'] == 'sell':
                sell_orders.append(processed_order)

    return {
        'buy_orders': sorted(buy_orders, key=lambda x: x['price_usdc'], reverse=True),
        'sell_orders': sorted(sell_orders, key=lambda x: x['price_usdc'])
    }


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




def calculate_orderbook_summary(orders):
    if not orders:
        return {
            'count': 0,
            'min_price': None,
            'max_price': None,
            'avg_price': None,
            'median_price': None,
            'total_quantity': 0,
            'price_quartiles': None,
            'price_histogram': None,
        }
    
    prices = [order['price_usdc'] for order in orders]
    quantities = [order['quantity'] for order in orders]
    
    hist, bin_edges = np.histogram(prices, bins=10)
    
    return {
        'count': len(orders),
        'min_price': float(min(prices)),
        'max_price': float(max(prices)),
        'avg_price': float(np.mean(prices)),
        'median_price': float(np.median(prices)),
        'total_quantity': int(sum(quantities)),
        'price_quartiles': [float(q) for q in np.percentile(prices, [25, 50, 75])],
        'price_histogram': {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist()
        },
    }

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