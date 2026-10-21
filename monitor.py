import requests
import time
import psutil
from datetime import datetime

url = "https://example.com/"
INTERVAL = 5
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_WARNING = 80
DISK_CRITICAL = 90

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response_time = time.time() - start_time

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        alerts = []

        if cpu > CPU_THRESHOLD:
            alerts.append("WARNING: High CPU")

        if ram > RAM_THRESHOLD:
            alerts.append("WARNING: High RAM")

        if disk >= DISK_CRITICAL:
            alerts.append("CRITICAL: High DISK")
        elif disk >= DISK_WARNING:
            alerts.append("WARNING: High DISK")

        if response.status_code != 200:
            alerts.append("WARNING: Website HTTP error")

        if response.status_code == 200:
            message = (
                f"Website: UP | Response: {response_time:.2f}s"
                f" | CPU: {cpu}% | RAM: {ram}% | DISK: {disk}%"
            )
        else:
            message = (
                f"Website: DOWxN | HTTP: {response.status_code}"
                f" | CPU: {cpu}% | RAM: {ram}% | DISK: {disk}%"
            )

        if alerts:
            severity = (
                "CRITICAL"
                if any(alert.startswith("CRITICAL") for alert in alerts)
                else "WARNING"
            )
            message += f" | {severity} | " + ", ".join(alerts)
        else:
            severity = "INFO"
            message += " | INFO | All checks normal"

    except requests.RequestException as error:
        message = f"Website: DOWN | Network error: {error}"
        severity = "WARNING"

    except Exception as error:
        message = f"Monitoring error: {error}"
        severity = "ERROR"

    print(f"{timestamp} | {message}", flush=True)

    with open("monitor.log", "a") as log:
        log.write(f"{timestamp} | {message}\n")

    if severity in ("WARNING", "CRITICAL", "ERROR"):
        with open("alerts.log", "a") as alert_log:
            alert_log.write(f"{timestamp} | {message}\n")

    time.sleep(INTERVAL)
