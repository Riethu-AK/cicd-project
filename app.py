from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
    <h1>CI/CD Pipeline Working 🚀</h1>
    <p><b>Status:</b> Application is running successfully</p>
    <p><b>Host:</b> {socket.gethostname()}</p>
    <p><b>Time:</b> {datetime.datetime.now()}</p>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is healthy"
    })

@app.route("/info")
def info():
    return jsonify({
        "project": "CI/CD with Jenkins and Docker",
        "developer": "RIETHURAM A K",
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
