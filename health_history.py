import psutil
from datetime import datetime

HEALTH_HISTORY_FILE = "health_history.log"

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent

health_status = "HEALTHY"

if cpu> 80 or ram > 80:
    health_status = "UNHEALTHY"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(HEALTH_HISTORY_FILE, "a") as file:

    file.write(
        f"{timestamp} | {health_status} | CPU: {cpu}% | RAM: {ram}%\n"
    )

print("Health history recorded successfully.")
print(f"CPU: {cpu}%")
print(f"RAM: {ram}%")
