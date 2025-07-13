#!/usr/bin/env python3
"""
Flask web interface for the orchestrator
"""

from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import threading
import os
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cybersec-orchestrator-2025'

# Global variables for tracking scans
active_scan = None
scan_status = {
    'running': False,
    'target': None,
    'progress': 0,
    'commands_executed': 0,
    'start_time': None,
    'output': []
}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/start_scan', methods=['POST'])
def start_scan():
    global active_scan, scan_status
    
    data = request.json
    target = data.get('target')
    max_iterations = data.get('max_iterations', 10)
    
    if scan_status['running']:
        return jsonify({'error': 'Scan already running'}), 400
    
    # Start the scan in a separate thread
    def run_scan():
        global scan_status
        try:
            scan_status['running'] = True
            scan_status['target'] = target
            scan_status['progress'] = 0
            scan_status['commands_executed'] = 0
            scan_status['output'] = []
            
            # Run the orchestrator
            cmd = f"python ../orchestrator.py --target {target} --max-iterations {max_iterations}"
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                cwd='..'
            )
            
            # Monitor the process
            for line in process.stdout:
                scan_status['output'].append(line.strip())
                if 'Executing command' in line:
                    scan_status['commands_executed'] += 1
                    scan_status['progress'] = min(100, (scan_status['commands_executed'] / max_iterations) * 100)
            
            process.wait()
            scan_status['running'] = False
            
        except Exception as e:
            scan_status['output'].append(f"Error: {str(e)}")
            scan_status['running'] = False
    
    threading.Thread(target=run_scan, daemon=True).start()
    
    return jsonify({'status': 'started', 'target': target})

@app.route('/api/scan_status')
def get_scan_status():
    return jsonify(scan_status)

@app.route('/api/stop_scan', methods=['POST'])
def stop_scan():
    global active_scan, scan_status
    
    if active_scan:
        active_scan.terminate()
        active_scan = None
    
    scan_status['running'] = False
    return jsonify({'status': 'stopped'})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    try:
        # Run the professional report generator located at project root
        try:
            project_root = Path(__file__).resolve().parent.parent
            script = project_root / 'generate_comprehensive_report.py'
            subprocess.run(['python', str(script)], check=True, cwd=project_root)
        except FileNotFoundError:
            return jsonify({'error': 'professional_report_generator.py not found'}), 500
        return jsonify({'status': 'success', 'file': 'COMPREHENSIVE_REPORT.pdf'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_report')
def download_report():
    project_root = Path(__file__).resolve().parent.parent
    report_path = project_root / 'pentest_results' / 'COMPREHENSIVE_REPORT.pdf'
    if report_path.exists():
        return send_file(report_path, as_attachment=True)
    else:
        return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    # Create web interface directory
    os.makedirs('web_interface', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)