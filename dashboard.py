from flask import Flask
import psutil
import requests

app = Flask(__name__)

@app.route("/")
def dashboard():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    try:
        response = requests.get("https://example.com", timeout=5)
        website = "UP" if response.status_code == 200 else "DOWN"
    except:
        website = "DOWN"

    if cpu >= 80 or ram >= 80:
        health = "CRITICAL"
    elif cpu >= 50 or ram >= 50:
        health = "WARNING"
    else:
        health = "HEALTHY"

    return f"""
    <html>
    <head>
        <title>AIOps Dashboard</title>
    </head>
    <body>
        <h1>AIOps Monitoring
Dashboard</h1>
        <hr>
        <h2>Website: {website}</h2>
        <h2>CPU: {cpu}%</h2>
        <h2>RAM: {ram}%</h2>
        <h2>Overall Status: {health}</h2>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
