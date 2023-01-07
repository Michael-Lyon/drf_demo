import requests
ENDPOINT = "http://localhost:8000/api/products/10"

get_response = requests.get(ENDPOINT, json={"pk": 1})
print(get_response.json())
    