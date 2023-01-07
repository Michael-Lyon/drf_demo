import requests
ENDPOINT = "http://localhost:8000/api/products/900/"

get_response = requests.get(ENDPOINT)
print(get_response.json())
