#!/usr/bin/env python3
"""
Simple test server to diagnose network connectivity issues
"""
from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    return f"""
    <h1>Flask Test Server</h1>
    <p>✅ Server is running!</p>
    <p>Hostname: {socket.gethostname()}</p>
    <p>If you can see this, the server is accessible.</p>
    """

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Server is healthy'}

if __name__ == '__main__':
    print("Starting test server on http://0.0.0.0:5000")
    print("You should be able to access it at:")
    print("- http://localhost:5000 (local)")
    print("- http://your-ec2-ip:5000 (external)")
    app.run(debug=False, host='0.0.0.0', port=5000) 