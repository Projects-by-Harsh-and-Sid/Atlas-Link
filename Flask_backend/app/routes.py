from flask import Flask, request, jsonify, render_template, send_from_directory
from app import app
from app.helper_functions.open_ai_request_mapper import extract_account

import uuid


# In-memory stores (use a database in production)
temp_codes = {}  # Stores temp codes and pairing ke



@app.route('/')
def home():
    return render_template('main.html')

# Route to generate login link with temp_code and pairing key
@app.route('/getlogin', methods=['GET'])
def get_login():
    """
    Curl command to test this route:
    curl -X GET -H "Openai-Conversation-Id: abc123" http://localhost:5000/getlogin
    
    """
    
    pairing_key = str(request.headers.get("Openai-Conversation-Id")) #  Openai-Ephemeral-User-Id
    
    temp_code = str(uuid.uuid4())  # Generate a unique temp code
    # pairing_key = str(uuid.uuid4())  # Generate a unique pairing key
    temp_codes[temp_code] = pairing_key  # Save pairing key linked to temp_code

    # # Return the login URL with the temp_code and the pairing key
    login_url = f"{app.config['URL']}/login/{temp_code}"
    return jsonify({"login_url": login_url, "pairing_key": pairing_key})
    



@app.route('/login/<temp_code>', methods=['POST', 'GET'])
def login(temp_code):
    
    
    if temp_code not in temp_codes:
        return jsonify({"error": "Invalid temp code"}), 400

    try:
        if request.method == 'GET':
            return render_template('wallet_login.html',  temp_code=temp_code)
        
        data = request.get_json()
        public_key = data.get('publicKey')
        balance = data.get('balance')
        
        print(public_key)
        print(balance)

        if not public_key:
            return jsonify({"error": "Public key is required"}), 400

        # Here you might want to add logic to handle the public key
        
        pairing_key = temp_codes[temp_code]
        user_id = public_key  # In practice, map this to a real user ID

        # Store the mapping of pairing_key to user ID
        app.config["user_pairs"][pairing_key] = user_id
        
        # For example, storing it in a database or associating it with a user

        return jsonify({
            "message": "Logged in successfully with wallet!",
            "publicKey": public_key
        }), 200
        
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
    
    





@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/transaction_details.json')
def transaction_details():
    return send_from_directory('static', 'transaction_details.json')


@app.route('/connect_wallet', methods=['GET','POST'])
def connect_wallet():
    data = request.json
    public_key = data.get('publicKey')
    
    if public_key:
        # session['wallet_public_key'] = public_key
        print(public_key)
        return jsonify({"status": "success", "message": f"Connected with public key: {public_key}"})
    else:
        return jsonify({"status": "error", "message": "No public key provided"}), 400

@app.route('/get_wallet_status')
def get_wallet_status():
    # public_key = session.get('wallet_public_key')
    public_key = None
    if public_key:
        return jsonify({"status": "connected", "publicKey": public_key})
    else:
        return jsonify({"status": "disconnected"})


