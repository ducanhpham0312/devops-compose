import os
import json
import requests
import docker
from flask import Flask, Response
from time import sleep
app = Flask(__name__)

SERVICE2_REQUEST_URL = "http://service2:8200/info"

def get_service1_info():
    try:
        service2_response = requests.get(SERVICE2_REQUEST_URL)
        if service2_response.status_code != 200:
            return service2_response.text
        else:
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
    except Exception as e:
        return e
    
def get_service2_info():
    try:
        service2_response = requests.get(SERVICE2_REQUEST_URL)
        if service2_response.status_code == 503:
            return "Service2 is not in RUNNING state: " + service2_response.reason
        elif service2_response.status_code != 200:
            return "Error when sending a GET request to service2: " + service2_response.text
        else:
            return service2_response.json()
    
    except Exception as e:
        return e

@app.route('/')
def index():
    # Fetch system info for Service1
    service1_info = get_service1_info()
    
    # Fetch system info from Service2
    try:
        service2_info = get_service2_info()
    except Exception as e:
        error_response = str(e)
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
    service2_response = get_service2_info()
    # Get information from this container
    service1_info = get_service1_info()
    # Add 2-second delay before responding
    sleep(2)
    info_response = {
        "service1": service1_info,
        "service2": service2_response
    }
    return Response(json.dumps(info_response), status=200, mimetype='application/json')

@app.route('/stop', methods=['POST'])
def stop_containers():
    client = docker.from_env()
    for container in client.containers.list():
      container.stop()
    client.close()
    return "Containers stopped", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)
