import requests
ENDPOINT = "http://localhost:8000/api/products/1/update/"
data = {
    "title":"Suki Court",
    "price":100.98
}
get_response = requests.put(ENDPOINT, json=data)
print(get_response.json())
