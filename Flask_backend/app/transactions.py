from flask import Flask, request, jsonify, render_template, url_for, redirect
import requests
from app import app

import uuid

from app.data_routes import extract_account

EXPRESS_SERVER_URL = 'http://localhost:3000'

# Hardcoded transaction parameters
TRANSACTION_PARAMS = {
    'orderCreator': '6Senu4mrPDM1Mb1xJYFXSDg2CggWkFLC9VCNzp1LEHBX',
    'itemMint': 'Ev3xUhc1Leqi4qR2E5VoG9pcxCvHHmnAaSRVPg485xAT',
    'quoteMint': 'ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx',
    'quantity': '1',
    'uiPrice': '10.5',
    'programId': 'traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg',
    'orderSide': 'sell'
}
@app.route('/create_order/<transaction_type>/<mint_id>/', methods=['GET'])
@extract_account
def create_order(account,transaction_type, mint_id):
    
    if transaction_type not in ('buy','sell'):
        return jsonify({'error': 'Invalid transaction type'}), 400
        
    
    temp_code = str(uuid.uuid4())
    
    transaction_paramaerter = {
        "orderCreator": account,
        "itemMint": mint_id,
        'quoteMint': 'ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx',
        "orderSide": transaction_type,
        'programId': 'traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg',
        "quantity": "__get_from_request__",
        "uiPrice": "__get_from_request__"
        
    }
    
    app.config["build_transactions"][temp_code] = transaction_paramaerter
    
    login_url = f"{app.config['URL']}/review_create_order/{temp_code}"
    return jsonify({"login_url": login_url, "transaction_code": temp_code})

@app.route('/review_create_order/<transaction_id>', methods=['GET', 'POST'])
def review_create_order(transaction_id):
    
    if transaction_id not in app.config["build_transactions"]:
        return jsonify({'error': 'Invalid transaction code'}), 400
    
    if request.method == 'GET':
        # also find item meta data to display using the item_data_mint_id_map
        transaction_parameters = app.config["build_transactions"][transaction_id]
        # also find item meta data to display using the item_data_mint_id_map
        item_information = app.config["reverse_map"][transaction_parameters['itemMint']] 
        return render_template('transaction_.html', transaction_parameters=transaction_parameters, item_information= item_information)
    
    
    if request.method == 'POST':
        
        transaction_parameters = app.config["build_transactions"][transaction_id]
        transaction_parameters['quantity'] = request.form.get('quantity')
        transaction_parameters['uiPrice'] = request.form.get('uiPrice')
        
        try:

            redirect_url = url_for('perform_transaction', transaction_id=transaction_id)
            redirect(redirect_url)
            
        except requests.RequestException as e:
            return jsonify({'error': str(e)}), 500

    

@app.route('/perform_transaction/<transaction_id>', methods=['GET'])
def index(transaction_id):
        
    if transaction_id not in app.config["build_transactions"]:
        return jsonify({'error': 'Invalid transaction code'}), 400    
        
    return render_template('transaction_items.html')



@app.route('/initiate_transaction/<transaction_id>', methods=['GET'])
def initiate_transaction(transaction_id):
    try:
        
        print (transaction_id)
        
        if transaction_id not in app.config["build_transactions"]:
            return jsonify({'error': 'Invalid transaction code'}), 400
        
        TRANSACTION_PARAMS = app.config["build_transactions"][transaction_id]
        
        # Make a request to the Express.js server with hardcoded parameters
        response = requests.get(f'{EXPRESS_SERVER_URL}/api/initiate_transaction', params=TRANSACTION_PARAMS)
        
        # get the 'trasaction field from json
    
        # Check if the request was successful
        response.raise_for_status()

        # Return the response from the Express.js server
        return jsonify(response.json()), response.status_code

    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        return jsonify({'error': str(e)}), 500