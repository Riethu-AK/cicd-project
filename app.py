from flask import Flask
import socket
import datetime
import psutil
import subprocess

app = Flask(__name__)

def get_docker_containers():
    try:
        result = subprocess.check_output("docker ps --format \"{{.Names}} - {{.Status}}\"", shell=True).decode()
        return result if result else "No running containers"
    except:
        return "Docker not running"

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

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {{
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0f172a;
                color: white;
            }}

            header {{
                padding: 20px;
                text-align: center;
                background: #020617;
                font-size: 24px;
                font-weight: bold;
            }}

            .container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }}

            .card {{
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}

            .status {{
                color: #22c55e;
                font-weight: bold;
            }}

            canvas {{
                width: 100% !important;
            }}

            pre {{
                text-align: left;
                background: #020617;
                padding: 10px;
                border-radius: 8px;
                overflow-x: auto;
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
            <p class="status">✔ Application Running</p>
        </div>

        <div class="card">
            <h3>Pipeline Status</h3>
            <p class="status">✔ Last Build: SUCCESS</p>
            <p>Auto-triggered via Jenkins</p>
        </div>

        <div class="card">
            <h3>Container Status</h3>
            <pre>{containers}</pre>
        </div>

        <div class="card">
            <h3>System Metrics</h3>
            <canvas id="chart"></canvas>
        </div>

    </div>

    <script>
        const ctx = document.getElementById('chart');

        new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['CPU Usage', 'Memory Usage'],
                datasets: [{{
                    data: [{cpu}, {memory}],
                    backgroundColor: ['#22c55e', '#3b82f6']
                }}]
            }}
        }});
    </script>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
