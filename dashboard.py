from flask import Flask
import subprocess
import sys
import os
import json

app = Flask(__name__)


@app.route("/")
def dashboard():

    health_result = subprocess.run(
        [sys.executable, "health_summary.py"],
        capture_output=True,
        text=True
    )

    health_output = health_result.stdout.strip()

    alert_output = ""

    if os.path.exists("alert_classifier.py"):
        alert_result = subprocess.run(
             [sys.executable, "alert_classifier.py"],
             capture_output=True,
             text=True
    )
    alert_output = alert_result.stdout.strip()

    recent_alerts = []

    if os.path.exists("alerts_log"):
        with open("alerts.log", "r") as file:
            alert_lines = file.readlines()

        recent_alerts = [
            line.strip()
            for line in alert_lines
            if line.strip()
        ][-5:]

    health_history = ""

    if os.path.exists("health_history.py"):
         subprocess.run(
             [sys.executable, "health_history.py"],
             capture_output=True,
             text=True
             )

    if os.path.exists("health_history.log"):
        with open("health_history.log", "r") as file:

            health_history = file.read().strip()

    history_lines = health_history.splitlines()

    chart_labels = []
    chart_cpu = []
    chart_ram = []

    for line in history_lines:
         parts = line.split("|")

         if len(parts) >= 4:
            try:
                chart_labels.append(parts[0].strip())

                cpu_value = float(parts[2].split(":")[1].replace("%", "").strip())
                ram_value = float(parts[3].split(":")[1].replace("%", "").strip())

                chart_cpu.append(cpu_value)
                chart_ram.append(ram_value)

            except (ValueError, IndexError):
                continue

    chart_labels_json = json.dumps(chart_labels)
    chart_cpu_json = json.dumps(chart_cpu)
    chart_ram_json = json.dumps(chart_ram)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>AIOps Health Dashboard</title>

        <meta http-equiv="refresh" content="5">

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>

            body {{
                font-family: Arial,
    sans-serif;
                margin: 30px;
                background-color:
    #f5f5f5;
            }}

            h1 {{
                color: #444;
            }}

            pre {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
                white-space: pre-wrap;
            }}

            #healthChart {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }}

            </style>

        </head>

        <body>

        <h1>AIOps Health Dashboard</h1>

        <h2>System Status</h2>

        <pre>Dashboard is running successfully.</pre>

        <h2>Live Health Summary</h2>
        <pre>{health_output}</pre>

        <h2>Alert Summary</h2>
        <pre>{alert_output}</pre>

        <h2>Alert History</h2>
        <pre>{"<br>".join(recent_alerts)}</pre>

        <h2>Alert Classification</h2>
        <pre>{alert_output}</pre>

        <h2>Health History</h2>
        <pre>{health_history}</pre>

        <h2>Health History Chart</h2>

        <canvas id="healthChart"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <script>
        const ctx = document.getElementById('healthChart');

        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels:  {chart_labels_json},
                datasets: [
                    {{
                        label: 'CPU %',
                        data:  {chart_cpu_json},
                        borderColor: 'blue',
                        fill: false
                    }},
                    {{
                        label: 'RAM %',
                        data:  {chart_ram_json},
                        borderColor: 'green',
                        fill: false
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
    }});
    </script>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
