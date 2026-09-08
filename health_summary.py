import psutil
import requests

URL = "https://example.com"
THRESHOLD = 80

try:
    response = requests.get(URL, timeout=5)

    website_status = "UP" if response.status_code == 200 else "DOWN"
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    cpu_status = "ANOMALY" if cpu > THRESHOLD else "Normal"
    ram_status = "ANOMALY" if ram > THRESHOLD else "Normal"

    if website_status == "UP" and cpu_status == "Normal" and ram_status == "Normal":
        overall_status = "HEALTHY"
    else:
        overall_status = "ATTENTION REQUIRED"

    print("AIOps Health Summary")
    print("--------------------")
    print(f"Website: {website_status}")
    print(f"CPU: {cpu:.1f}% - {cpu_status}")
    print(f"RAM: {ram:.1f}% - {cpu_status}")
    print(f"Overall Status: {overall_status}")

except requests.RequestException as e:
    print("AIOps Health Summary")
    print("--------------------")
    print("Website: DOWN")
    print("Overall Status: ATTENTION REQUIRED")
    print(f"Error: {e}")
