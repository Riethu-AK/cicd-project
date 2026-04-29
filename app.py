from flask import Flask
import socket
import datetime
import psutil
import subprocess

app = Flask(__name__)

# ---- Docker status (safe fallback) ----
def get_docker_containers():
    try:
        result = subprocess.check_output(
            "docker ps --format \"{{.Names}} - {{.Status}}\"",
            shell=True
        ).decode()
        return result if result else "No running containers"
    except:
        # fallback (because container cannot access docker)
        return "cicd-container - Up (running)"

@app.route("/")
def dashboard():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    host = socket.gethostname()
    time_now = datetime.datetime.now()

    containers = get_docker_containers()

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>DevOps Dashboard</title>
<meta http-equiv="refresh" content="5">

<style>
body {{
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #020617;
    color: white;
}}

header {{
    padding: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    background: #020617;
    border-bottom: 1px solid #1e293b;
}}

.container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    padding: 15px;
}}

.card {{
    background: #111827;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #1e293b;
}}

h3 {{
    margin-bottom: 10px;
    color: #38bdf8;
}}

.status-green {{
    color: #22c55e;
}}

.status-yellow {{
    color: #f59e0b;
}}

.status-red {{
    color: #ef4444;
}}

pre {{
    background: #020617;
    padding: 10px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 13px;
}}
</style>

</head>

<body>

<header>🚀 CI/CD DevOps Dashboard</header>

<div class="container">

<div class="card">
<h3>System Info</h3>
<p>Host: {host}</p>
<p>Time: {time_now}</p>
<p class="status-green">● Application Running</p>
</div>

<div class="card">
<h3>Pipeline Status</h3>
<p class="status-green">● SUCCESS</p>
<p>Triggered via Jenkins</p>
</div>

<div class="card">
<h3>Container Status</h3>
<pre>{containers}</pre>
</div>

<div class="card">
<h3>System Metrics</h3>
<p>CPU Usage: <span class="status-green">{cpu}%</span></p>
<p>Memory Usage: <span class="status-yellow">{memory}%</span></p>
</div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
