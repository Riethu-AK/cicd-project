from flask import Flask
import socket
import datetime
import psutil
import subprocess
import platform
import requests

app = Flask(__name__)

# 🔐 CHANGE THIS
JENKINS_URL = "http://localhost:8080/job/cicd-pipeline/lastBuild/api/json"
JENKINS_USER = "your_username"
JENKINS_TOKEN = "your_api_token"

requests_count = 0

# ---- Jenkins real status ----
def get_jenkins_status():
    try:
        res = requests.get(JENKINS_URL, auth=(JENKINS_USER, JENKINS_TOKEN))
        data = res.json()
        return data["result"], data["number"]
    except:
        return "UNKNOWN", "N/A"

# ---- Docker ----
def get_docker():
    try:
        return subprocess.check_output(
            "docker ps --format \"{{.Names}} - {{.Status}}\"",
            shell=True
        ).decode()
    except:
        return "Docker access not available"

# ---- Logs ----
def get_logs():
    try:
        return subprocess.check_output(
            "docker logs --tail 5 cicd-container",
            shell=True
        ).decode()
    except:
        return "No logs"

@app.route("/")
def dashboard():
    global requests_count
    requests_count += 1

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    host = socket.gethostname()
    time_now = datetime.datetime.now()

    os_info = platform.system()
    cpu_cores = psutil.cpu_count()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    containers = get_docker()
    logs = get_logs()

    build_status, build_no = get_jenkins_status()

    color = "#22c55e" if build_status == "SUCCESS" else "#ef4444"

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Production DevOps Dashboard</title>
<meta http-equiv="refresh" content="5">

<style>
body {{
    margin: 0;
    font-family: Arial;
    background: #020617;
    color: white;
    display: flex;
}}

.sidebar {{
    width: 220px;
    background: #020617;
    border-right: 1px solid #1e293b;
    padding: 20px;
}}

.main {{
    flex: 1;
}}

.header {{
    padding: 15px;
    text-align: center;
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

h3 {{ color: #38bdf8; }}

pre {{
    background: #020617;
    padding: 10px;
    border-radius: 8px;
    font-size: 12px;
}}
</style>
</head>

<body>

<div class="sidebar">
<h2>DevOps</h2>
<p>Dashboard</p>
<p>Monitoring</p>
<p>CI/CD</p>
<p>Logs</p>
</div>

<div class="main">

<div class="header">🚀 Production DevOps Dashboard</div>

<div class="container">

<div class="card">
<h3>System</h3>
<p>{host}</p>
<p>{time_now}</p>
</div>

<div class="card">
<h3>Pipeline</h3>
<p style="color:{color}">● {build_status}</p>
<p>Build #{build_no}</p>
</div>

<div class="card">
<h3>Containers</h3>
<pre>{containers}</pre>
</div>

<div class="card">
<h3>Metrics</h3>
<p>CPU: {cpu}%</p>
<p>Memory: {memory}%</p>
</div>

<div class="card">
<h3>System Info</h3>
<p>{os_info}</p>
<p>Cores: {cpu_cores}</p>
</div>

<div class="card">
<h3>Uptime</h3>
<p>{boot_time}</p>
</div>

<div class="card">
<h3>Traffic</h3>
<p>{requests_count} hits</p>
</div>

<div class="card">
<h3>Logs</h3>
<pre>{logs}</pre>
</div>

</div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
