import requests
url = "https://example.com"
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    print("Request successful!")
    print("Status code:", response.status_code)
    print("Website:", response.url)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)

