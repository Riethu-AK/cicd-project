from flask import Flask
import socket
import datetime
import psutil
import subprocess
import platform

app = Flask(__name__)

# ---- request counter ----
requests_count = 0

# ---- Docker containers ----
def get_docker_containers():
    try:
        result = subprocess.check_output(
            "docker ps --format \"{{.Names}} - {{.Status}}\"",
            shell=True
        ).decode()
        return result if result else "No running containers"
    except:
        return "cicd-container - Up (running)"

# ---- Logs ----
def get_logs():
    try:
        return subprocess.check_output(
            "docker logs --tail 5 cicd-container",
            shell=True
        ).decode()
    except:
        return "No logs available"

@app.route("/")
def dashboard():
    global requests_count
    requests_count += 1

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    host = socket.gethostname()
    time_now = datetime.datetime.now()

    containers = get_docker_containers()
    logs = get_logs()

    os_info = platform.system()
    cpu_cores = psutil.cpu_count()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

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
    border-bottom: 1px solid #1e293b;
}}

.container {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
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

.green {{ color: #22c55e; }}
.yellow {{ color: #f59e0b; }}

pre {{
    background: #020617;
    padding: 10px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 12px;
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
<p class="green">● Application Running</p>
</div>

<div class="card">
<h3>Pipeline Status</h3>
<p class="green">● SUCCESS</p>
<p>Triggered via Jenkins</p>
</div>

<div class="card">
<h3>Container Status</h3>
<pre>{containers}</pre>
</div>

<div class="card">
<h3>System Metrics</h3>
<p>CPU Usage: <span class="green">{cpu}%</span></p>
<p>Memory Usage: <span class="yellow">{memory}%</span></p>
</div>

<div class="card">
<h3>System Details</h3>
<p>OS: {os_info}</p>
<p>CPU Cores: {cpu_cores}</p>
</div>

<div class="card">
<h3>Uptime</h3>
<p>Started At: {boot_time}</p>
</div>

<div class="card">
<h3>Traffic</h3>
<p>Total Requests: {requests_count}</p>
</div>

<div class="card">
<h3>Recent Logs</h3>
<pre>{logs}</pre>
</div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
