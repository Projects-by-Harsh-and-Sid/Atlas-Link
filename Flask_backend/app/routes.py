from flask import Flask, request, jsonify, render_template
from app import app

import uuid


# In-memory stores (use a database in production)
temp_codes = {}  # Stores temp codes and pairing keys
user_sessions = {}  # Maps pairing keys to user IDs

# Route to generate login link with temp_code and pairing key
@app.route('/getlogin', methods=['GET'])
def get_login():
    
    pairing_key = str(request.headers.get("Openai-Conversation-Id")) #  Openai-Ephemeral-User-Id
    
    temp_code = str(uuid.uuid4())  # Generate a unique temp code
    # pairing_key = str(uuid.uuid4())  # Generate a unique pairing key
    temp_codes[temp_code] = pairing_key  # Save pairing key linked to temp_code

    # Return the login URL with the temp_code and the pairing key
    login_url = f"{app.config["URL"]}/login/{temp_code}"
    return jsonify({"login_url": login_url, "pairing_key": pairing_key})



@app.route('/login/<temp_code>', methods=['POST', 'GET'])
def login(temp_code):
    if request.method == 'GET':
        # Render the login form when the page is visited
        return render_template('login.html', temp_code=temp_code)
    
    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')  # Get username from form

        if temp_code in temp_codes:
            # Assume successful login, associate pairing key with user ID
            pairing_key = temp_codes[temp_code]
            user_id = username  # In practice, map this to a real user ID

            # Store the mapping of pairing_key to user ID
            user_sessions[pairing_key] = user_id

            return jsonify({"message": f"User {username} logged in successfully!"})

    return jsonify({"error": "Invalid or expired temp code"}), 400


# Route to get user information based on pairing key
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    pairing_key = str(request.headers.get("Openai-Conversation-Id"))

    if pairing_key in user_sessions:
        user_id = user_sessions[pairing_key]
        # Simulate fetching user info
        user_info = {
            "user_id": user_id,
            "account_info": "Some account-related info here."
        }
        return jsonify(user_info)
    
    return jsonify({"error": "Invalid or missing pairing key"}), 401