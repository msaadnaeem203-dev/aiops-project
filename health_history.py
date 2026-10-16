import psutil
from datetime import datetime

HEALTH_HISTORY_FILE = "health_history.log"

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

health_status = "HEALTHY"

if cpu > 80 or ram > 80 or disk >= 80:
    health_status = "UNHEALTHY"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(HEALTH_HISTORY_FILE, "a") as file:

    file.write(
        f"{timestamp} | {health_status} | CPU: {cpu}% | RAM: {ram}% | DISK: {disk}% \n"
    )

print(f"Health history recorded successfully.")
print(f"Status: {health_status}")
print(f"CPU: {cpu}% | RAM: {ram}% | DISK : {disk}%")
