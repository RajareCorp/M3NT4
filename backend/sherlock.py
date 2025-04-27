from flask import Blueprint, jsonify, request, send_from_directory
import subprocess

sherlock_routes = Blueprint('sherlock', __name__, static_folder='static')

@sherlock_routes.route('/')
def sherlock_page():
    return send_from_directory(sherlock_routes.static_folder, 'sherlock.html') 

@sherlock_routes.route('/run', methods=['POST'])
def run_sherlock():
    target = request.json.get('target', '')
    result = subprocess.run(['sherlock', target], capture_output=True, text=True)
    return jsonify({'output': result.stdout})
