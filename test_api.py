import requests

try:
    response = requests.get("http://127.0.0.1:8000/api/events/upcoming/")
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
