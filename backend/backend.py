import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from nmap import nmap_routes
from photon import photon_routes
from nikto import nikto_routes
import subprocess

app = Flask(__name__, static_folder='static')

app.register_blueprint(nmap_routes, url_prefix="/nmap")
app.register_blueprint(photon_routes, url_prefix="/photon")
app.register_blueprint(nikto_routes, url_prefix="/nikto")

# Endpoint pour servir l'interface
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
    

@app.route('/ifconfig', methods=['GET'])
def get_ifconfig():
    try:
        result = subprocess.run(['curl', 'https://ifconfig.me'], capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/curl', methods=['GET'])
def serve_curl():
    return send_from_directory(app.static_folder, 'curl.html') 

@app.route('/curl', methods=['POST'])
def run_curl():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/vpn', methods=['get'])
def start_vpn():
    # Assurez-vous que le fichier de configuration OpenVPN est présent
    if not os.path.exists('/etc/openvpn/config.ovpn'):
        return jsonify({'error': 'VPN configuration file not found'}), 404

    # Exécutez OpenVPN avec la configuration spécifiée
    subprocess.Popen(['openvpn', '--config', '/etc/openvpn/config.ovpn'])
    return jsonify({'message': 'VPN started successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
