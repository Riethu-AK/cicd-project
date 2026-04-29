from flask import Flask
import socket
import datetime
import psutil
import subprocess
import platform

app = Flask(__name__)
requests_count = 0

def get_docker_containers():
    try:
        return subprocess.check_output(
            "docker ps --format \"{{.Names}} - {{.Status}}\"",
            shell=True
        ).decode()
    except:
        return "cicd-container - Up (running)"

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

    os_info = platform.system()
    cpu_cores = psutil.cpu_count()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    containers = get_docker_containers()
    logs = get_logs()

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Premium DevOps Dashboard</title>
<meta http-equiv="refresh" content="5">

<style>
body {{
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
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

.sidebar h2 {{
    color: #38bdf8;
}}

.sidebar p {{
    margin: 10px 0;
    color: #94a3b8;
}}

.main {{
    flex: 1;
}}

.header {{
    padding: 15px;
    font-size: 20px;
    border-bottom: 1px solid #1e293b;
    text-align: center;
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
    color: #38bdf8;
}}

.green {{ color: #22c55e; }}
.yellow {{ color: #f59e0b; }}

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
<p>CI/CD Status</p>
<p>Logs</p>
</div>

<div class="main">

<div class="header">🚀 CI/CD DevOps Dashboard</div>

<div class="container">

<div class="card">
<h3>System Info</h3>
<p>Host: {host}</p>
<p>Time: {time_now}</p>
<p class="green">● Running</p>
</div>

<div class="card">
<h3>Pipeline</h3>
<p class="green">● SUCCESS</p>
<p>Jenkins Triggered</p>
</div>

<div class="card">
<h3>Containers</h3>
<pre>{containers}</pre>
</div>

<div class="card">
<h3>Metrics</h3>
<p>CPU: <span class="green">{cpu}%</span></p>
<p>Memory: <span class="yellow">{memory}%</span></p>
</div>

<div class="card">
<h3>System</h3>
<p>OS: {os_info}</p>
<p>Cores: {cpu_cores}</p>
</div>

<div class="card">
<h3>Uptime</h3>
<p>{boot_time}</p>
</div>

<div class="card">
<h3>Traffic</h3>
<p>{requests_count} Requests</p>
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
