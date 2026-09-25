from flask import Flask
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def dashboard():
    health = subprocess.run(
        [sys.executable, "health_summary.py"],
        capture_output=True,
        text=True
    )

    alerts = subprocess.run(
        [sys.executable, "alert_classifier.py"],
        capture_output=True,
        text=True
    )

    health_output = health.stdout.strip()
    alert_output = alerts.stdout.strip()

    return f"""
    <html>
    <head>
        <title>AIOps Health Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>AIOps Health Dashboard</h1>

        <h2>Live Health Summary</h2>
        <pre>{health_output}</pre>

        <h2>Alert Classification</h2>
        <pre>{alert_output}</pre>


        <p>Dashboard refreshes every 5 seconds.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
