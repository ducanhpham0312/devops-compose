import os
import json
import requests
import subprocess
from flask import Flask, Response
from time import sleep
app = Flask(__name__)

# Function to fetch system information
def get_system_info():
    ip_address = os.popen("hostname -i").read().strip()
    processes = os.popen("ps -ax").read()
    disk_space = os.popen("df").read()
    uptime = os.popen("uptime").read().strip()
    
    return {
        "ip_address": ip_address,
        "processes": processes,
        "disk_space": disk_space,
        "uptime": uptime
    }

@app.route('/')
def index():
    # Fetch system info for Service1
    service1_info = get_system_info()
    
    # Fetch system info from Service2
    try:
        service2_info = requests.get('http://service2:8200/info').json()
    except Exception as e:
        error_response = {"error": str(e)}
        return Response(json.dumps(error_response), status=500, mimetype='application/json')

    # Combine Service1 and Service2 info
    combined_info = {
        "service1": service1_info,
        "service2": service2_info
    }
    
    return Response(json.dumps(combined_info, indent=2), mimetype='application/json')

@app.route('/info', methods=['GET'])
def info():
    # Get information from Service2
    service2_response = requests.get('http://service2:8200/info').json()
    # Get information from this container
    service1_info = get_system_info()
    # Add 2-second delay before responding
    sleep(2)
    info_response = {
        "service1": service1_info,
        "service2": service2_response
    }
    return Response(json.dumps(info_response), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)
