import os
from flask import Flask, request, jsonify, send_from_directory, send_file
import subprocess

app = Flask(__name__, static_folder='static')

# Endpoint pour servir l'interface
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoint pour scanner un réseau avec Nmap
@app.route('/nmap', methods=['POST'])
def run_nmap():
    target = request.json.get('target', '127.0.0.1')
    result = subprocess.run(['nmap','-sV', '-p-', target], capture_output=True, text=True)
    return jsonify({'output': result.stdout})

@app.route('/photon', methods=['POST'])
def run_photon():
    target = request.json.get('target', 'http://example.com')
    output_dir = '/app/photon_output'
    
    # Exécuter Photon avec subprocess
    result = subprocess.run(
        ['python3', '/opt/photon/photon.py', '-u', target, '-o', output_dir],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return jsonify({'output': f'Scan completed. Results saved in {output_dir}'})
    else:
        return jsonify({'error': result.stderr}), 500

# Endpoint pour lister les fichiers générés par Photon
@app.route('/photon/results', methods=['GET'])
def list_photon_results():
    output_dir = '/app/photon_output'
    try:
        files = os.listdir(output_dir)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint pour afficher le contenu d'un fichier Photon
@app.route('/photon/results/<filename>', methods=['GET'])
def get_photon_result_file(filename):
    output_dir = '/app/photon_output'
    file_path = os.path.join(output_dir, filename)
    try:
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/nikto', methods=['POST'])
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
