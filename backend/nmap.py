from flask import Blueprint, jsonify, request, send_from_directory
import subprocess

nmap_routes = Blueprint('nmap', __name__, static_folder='static')

@nmap_routes.route('/')
def nmap_page():
    return send_from_directory(nmap_routes.static_folder, 'nmap.html') 

@nmap_routes.route('/run', methods=['POST'])
def run_nmap():
    target = request.json.get('target', '127.0.0.1')
    result = subprocess.run(['nmap', target], capture_output=True, text=True)
    return jsonify({'output': result.stdout})
