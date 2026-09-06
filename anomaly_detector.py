import psutil
import time

print("AIOps Anomaly Detector Started")

while True:
     cpu = psutil.cpu_percent(interval=1)
     ram = psutil.virtual_memory().percent

     if cpu > 80 or ram > 80:
         print(f"ANOMALY DETECTED! CPU: {cpu}% RAM: {ram}%")
     else:
         print(f"Normal | CPU: {cpu}% RAM: {ram}%")

     time.sleep(2)
