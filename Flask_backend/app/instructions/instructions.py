from flask import jsonify, current_app
from flask import send_from_directory

import os

from app import app

@app.route('/instructions/<instruction_name>')
def get_instructions(instruction_name):
    instructions = current_app.config['instructions']
    if instruction_name in instructions:
        return jsonify({'instructions': instructions[instruction_name]})
    else:
        return jsonify({'error': 'Instruction not found'}), 404
    

@app.route('/openapi_endpoints/<endpoint_name>')
def get_openapi_endpoint(endpoint_name):
    
    end_points_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi_endpoints")
    
    #filter for the yaml files
    end_points = [f  for f in os.listdir(end_points_dir) if f.endswith('.yaml')]
    if endpoint_name in end_points:
        # send yaml file
        return send_from_directory(end_points_dir, endpoint_name)
    
    return jsonify({'error': 'Endpoint not found'}), 404