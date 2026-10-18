import psutil
import time
from datetime import datetime

print("AIOps Anomaly Detector Started")
print("Monitoring CPU, RAM, and Disk usage")
print("Press Ctrl+C to stop")

try:
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        alerts = []

        if cpu >= 90:
            alerts.append("CRITICAL: CPU")
        elif cpu >= 80:
            alerts.append("WARNING: CPU")

        if ram >= 90:
            alerts.append("CRITICAL: RAM")
        elif ram >= 80:
            alerts.append("WARNING: RAM")

        if disk >= 90:
            alerts.append("CRITICAL: DISK")
        elif disk >= 80:
            alerts.append("WARNING: DISK")

        if alerts:
            severity = (
                "CRITICAL" if any (

alert.startswith("CRITICAL")
                    for alert in alerts
                )
                else "WARNING"
            )

            print(
                f"{severity} | CPU: {cpu:.1f}% | "
                f"RAM: {ram:.1f}% | DISK: {disk:.1f}%"
            )

            with open("alerts.log", "a") as file:
                file.write(
                    f"{datetime.now()} | CPU: {cpu:.1f}% | "
                    f"RAM: {ram:.1f}% | DISK: {disk:.1f}% | "
                    f"{severity} | {', '.join(alerts)}\n"
                )
        else:
            print(
                f"INFO | CPU: {cpu:.1f}% | "
                f"RAM {ram:.1f}% | DISK: {disk:.1f}%"
            )

        time.sleep(2)

except KeyboardInterrupt:
    print("\nAIOps Anomaly Detector stopped.")
