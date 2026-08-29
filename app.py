import requests
import time

url = "https://example.com"

for check in range(1, 6):
    print("Check", check)

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print("Status: UP")
            print("Status code:", response.status_code)
        else:
            print("Status: DOWN")
            print("Status code:", response.status_code)

    except requests.exeptions.RequestException as e:
         print("Status: DOWN")
         print("Request failed:", e)

    print("-------------------")
    time.sleep(5)
