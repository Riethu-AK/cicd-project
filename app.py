from flask import Flask
import socket
import datetime
import random

app = Flask(__name__)

@app.route("/")
def dashboard():
    cpu = random.randint(10, 70)
    memory = random.randint(100, 500)

    return f"""
    <html>
    <head>
        <title>DevOps Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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
            canvas {{
                max-width: 400px;
                margin: auto;
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
        <h2>Performance Metrics</h2>
        <canvas id="chart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('chart');

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: ['CPU %', 'Memory MB'],
                datasets: [{{
                    label: 'System Usage',
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
