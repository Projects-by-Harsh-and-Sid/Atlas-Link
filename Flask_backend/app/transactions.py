from flask import Flask, request, jsonify, render_template
import requests
from app import app

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


@app.route('/perform_transaction')
def index():
    return render_template('transaction_items.html')

@app.route('/initiate_transaction', methods=['GET'])
def initiate_transaction():
    try:
        
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