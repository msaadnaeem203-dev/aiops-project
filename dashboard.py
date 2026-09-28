from flask import Flask
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def dashboard():
    health_result = subprocess.run(
        [sys.executable, "health_summary.py"],
        capture_output=True,
        text=True
    )

    health_output = health_result.stdout.strip()

    alert_result = subprocess.run(
        [sys.executable, "alert_classifier.py"],
        capture_output=True,
        text=True
    )

    alert_output = alert_result.stdout.strip()

    alert_lines = alert_output.splitlines()

    classified_lines = [
        line.strip().split()[-1]
        for line in alert_lines
        if line.strip()
        and line.strip().split()[-1]
    in ("INFO", "WARNING", "CRITICAL")
    ]

    latest_alert = classified_lines[-1] if classified_lines else "NONE"

    recent_alerts = classified_lines[-5:]

    info_count = sum(
        1 for alert in classified_lines
        if alert == "INFO"
    )

    warning_count = sum(
        1 for alert in classified_lines
        if alert == "WARNING"
    )

    critical_count = sum(
        1 for alert in classified_lines
        if alert == "CRITICAL"
    )

    total_alerts = info_count + warning_count + critical_count

    return f"""
    <html>
    <head>
        <title>AIOps Health Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>

    <body>
        <h1>AIOps Health Dashboard</h1>

        <h2>System Status</h2>
        <pre>{health_output}</pre>

        <h2>Live Health Summary</h2>
        <pre>{health_output}</pre>

        <h2>Alert Summary</h2>
        <p>Total Alerts: {total_alerts}</p>
        <p>INFO: {info_count} | WARNING: {warning_count} | CRITICAL: {critical_count}</p>
        <p>Latest Alert: {latest_alert}</p>

        <h2>Alert History</h2>
        <pre>{"<br>".join(recent_alerts)}</pre>

        <h2>Alert Classification</h2>
        <pre>{alert_output}</pre>

        <p>Dashboard refreshes every 5 seconds.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
