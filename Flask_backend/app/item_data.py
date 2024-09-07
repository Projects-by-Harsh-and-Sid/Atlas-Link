
from flask import Flask, request, jsonify, render_template,send_from_directory
from app import app
# import subprocess
import requests
import json
import uuid

from app.helper_functions.open_ai_request_mapper import extract_account



@app.route('/item_detail/<mintid>', methods=['GET'])
def get_item_detials_by_mint_id(mintid):
    
    
    if mintid in app.config["Item_data"]:
        return jsonify(app.config["Item_data"][mintid])
    
    return jsonify({"error": "Item not found"})




