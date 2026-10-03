from datetime import datetime

HEALTH_HISTORY_FILE = "health_history.log"

health_status = "HEALTHY"
cpu = 20.5
ram = 35.2

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(HEALTH_HISTORY_FILE, "a") as file:
    file.write(
        f"{timestamp} | {health_status} | CPU: {cpu}% | RAM: {ram}%\n"
    )

print("Health history recorded successfully.")
