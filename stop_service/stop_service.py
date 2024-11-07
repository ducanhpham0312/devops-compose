import docker
from flask import Flask

app = Flask(__name__)

@app.route('/stop', methods=['POST'])
def stop_containers():
    client = docker.from_env()
    for container in client.containers.list():
      container.kill()
    client.close()
    return "Containers stopped", 200

# Add this to run the Flask app and keep the container running
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
