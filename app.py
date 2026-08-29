import requests

url = "https://example.com"

try:
   response = requests.get(url, timeout=10)
   response.raise_for_status()

   if response.status_code == 200:
      print("Status: UP")
      print("Status code:", response.status_code)
      print("Website:", response.url)
   else:
      print("Status: DOWN")
      print("Status code:", response.status_code)

except requests.exeptions.RequestException as e:
     print("Status: DOWN")
     print("Request failed:", e)
