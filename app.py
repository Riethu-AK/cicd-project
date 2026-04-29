from flask import Flask, jsonify
import socket
import datetime
import subprocess

app = Flask(__name__)

def get_docker_status():
    try:
        result = subprocess.check_output("docker ps", shell=True).decode()
        return result
    except:
        return "Docker not running"

@app.route("/")
def dashboard():
    return f"""
    <html>
    <head>
        <title>DevOps Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
            }}
            .card {{
                background: #1e293b;
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
            }}
            .status {{
                color: lightgreen;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>

    <h1>🚀 CI/CD DevOps Dashboard</h1>

    <div class="card">
        <h2>System Info</h2>
        <p>Host: {socket.gethostname()}</p>
        <p>Time: {datetime.datetime.now()}</p>
        <p class="status">✔ Application Running</p>
    </div>

    <div class="card">
        <h2>Pipeline Status</h2>
        <p class="status">✔ Last Build: SUCCESS</p>
        <p>Build Number: #7</p>
    </div>

    <div class="card">
        <h2>Container Status</h2>
        <pre>{get_docker_status()}</pre>
    </div>

    <div class="card">
        <h2>Metrics</h2>
        <p>CPU Usage: 25%</p>
        <p>Memory Usage: 120MB</p>
        <p>Requests Handled: 150</p>
    </div>

    <div class="card">
        <h2>Deployment Info</h2>
        <p>Last Deployment: {datetime.datetime.now()}</p>
    </div>

    </body>
    </html>
    """

@app.route("/api/health")
def health():
    return jsonify({"status": "UP"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
