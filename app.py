from flask import Flask, render_template, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html",
        host=socket.gethostname(),
        time=datetime.datetime.now()
    )

@app.route("/api/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is running"
    })

@app.route("/api/info")
def info():
    return jsonify({
        "project": "CI/CD Pipeline",
        "developer": "RIETHURAM A K",
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
