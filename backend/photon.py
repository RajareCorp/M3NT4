from flask import Blueprint, jsonify, request, send_from_directory, send_file
import subprocess
import os

photon_routes = Blueprint('photon', __name__, static_folder='static')

@photon_routes.route('/')
def photon_page():
    return send_from_directory(photon_routes.static_folder, 'photon.html') 

# Endpoint pour lister les fichiers générés par Photon
@photon_routes.route('/results', methods=['GET'])
def list_photon_results():
    output_dir = '/app/photon_output'
    try:
        files = os.listdir(output_dir)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Endpoint pour afficher le contenu d'un fichier Photon
@photon_routes.route('/results/<filename>', methods=['GET'])
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

@photon_routes.route('/run', methods=['POST'])
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