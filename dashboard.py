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

    if os.path.exists("alerts.log"):
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
    chart_disk = []

    for line in history_lines:
         parts = line.split("|")

         if len(parts) >= 5:
            try:

                chart_labels.append(str(len(chart_labels) + 1))

                cpu_value = float(parts[2].split(":")[1].replace("%", "").strip())
                ram_value = float(parts[3].split(":")[1].replace("%", "").strip())
                disk_value = float(parts[4].split(":")[1].replace("%", "").strip())

                chart_cpu.append(cpu_value)
                chart_ram.append(ram_value)
                chart_disk.append(disk_value)

            except (ValueError, IndexError):
                continue

    chart_labels_json = json.dumps(chart_labels)
    chart_cpu_json = json.dumps(chart_cpu)
    chart_ram_json = json.dumps(chart_ram)
    chart_disk_json = json.dumps(chart_disk)

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

        <h2>AIOps Overview</h2>

        <pre>
        Website Monitoring: Active
        CPU monitoring: Active
        RAM Monitoring: Active
        Alert Classification: Active
        Health History: Recording
        </pre>

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
                        label: 'CPU Usage (%)',
                        data:  {chart_cpu_json},
                        borderColor: 'blue',
                        tension: 0.3,
                        fill: false
                    }},
                    {{
                        label: 'RAM Usage (%)',
                        data:  {chart_ram_json},
                        borderColor: 'green',
                        tension: 0.3,
                        fill: false
                    }},
                    {{
                        label: 'Disk Usage (%)',
                        data: {chart_disk_json},
                        borderColor: 'red',
                        tension: 0.3,
                        fill: false
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        min: 0,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Usage (%)'
                        }}
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
