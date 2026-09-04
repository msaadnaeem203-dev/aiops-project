import requests
import time
import psutil
from datetime import datetime

url = "https://example.com/"

while True:
    try:
       start_time = time.time()
       response = requests.get(url, timeout=10)
       response_time = time.time() - start_time

       if response.status_code == 200:
           cpu = psutil.cpu_percent()
           ram = psutil.virtual_memory().percent

           message = f"Status: UP | Response time: {response_time:.2f} seconds | CPU: {cpu}% | RAM {ram}%"


           if cpu > 80 or ram > 80:
               message += " | ALERT: High Resource Usage!" 

       else:
            message = f"Status: DOWN | HTTP code: {response.status_code}"

    except requests.RequestException as error:
       message = f"Status: Down | Error: {error}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(timestamp, "|", message)

    with open("monitor.log", "a") as log:
         log.write(f"{timestamp} | {message}\n")

    time.sleep(5)
