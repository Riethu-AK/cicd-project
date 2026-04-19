from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>CI/CD Dashboard</title>
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
            button {{
                padding: 10px 20px;
                margin: 10px;
                border: none;
                background: #22c55e;
                color: black;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>

        <h1>🚀 CI/CD Pipeline Dashboard</h1>

        <div class="card">
            <h2>System Info</h2>
            <p><b>Host:</b> {socket.gethostname()}</p>
            <p><b>Time:</b> {datetime.datetime.now()}</p>
        </div>

        <div class="card">
            <h2>API Controls</h2>
            <button onclick="getHealth()">Check Health</button>
            <button onclick="getInfo()">Get Info</button>
            <p id="output"></p>
        </div>

        <script>
        function getHealth() {{
            fetch('/api/health')
            .then(res => res.json())
            .then(data => {{
                document.getElementById("output").innerText =
                    "Health: " + data.status;
            }});
        }}

        function getInfo() {{
            fetch('/api/info')
            .then(res => res.json())
            .then(data => {{
                document.getElementById("output").innerText =
                    data.project + " | " + data.developer;
            }});
        }}
        </script>

    </body>
    </html>
    """

@app.route("/api/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is running"
    })

@app.route("/api/info")
def info():
    return jsonify({
        "project": "CI/CD Pipeline with Jenkins and Docker",
        "developer": "RIETHURAM A K",
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
