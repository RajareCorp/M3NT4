from flask import Blueprint, jsonify, request, send_from_directory
import subprocess

nikto_routes = Blueprint('nikto', __name__, static_folder='static')

@nikto_routes.route('/')
def nmap_page():
    return send_from_directory(nikto_routes.static_folder, 'nmap.html') 

@nikto_routes.route('/run', methods=['POST'])
def run_nikto():
    data = request.json
    host = data.get('host')
    options = data.get('options', '')  # Options Nikto sous forme de chaîne
    if not host:
        return jsonify({'error': 'Host is required'}), 400

    try:
        command = f"./nikto.pl -h {host} {options}"
        process = subprocess.run(command, shell=True, cwd="/opt/nikto/program", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode == 0:
            return jsonify({'output': process.stdout})
        else:
            return jsonify({'error': process.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
