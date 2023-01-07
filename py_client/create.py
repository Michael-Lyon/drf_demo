import requests
ENDPOINT = "http://localhost:8000/api/products/"
# ENDPOINT = "http://localhost:8000/api/products/create/"

data = {"title": "Prodcut CReated with token"}
headers = {'Authorization': 'Bearer f3eb070da243f8902ddb587325016f6da541a878'}

get_response = requests.post(ENDPOINT, json=data, headers=headers)
print(get_response.json())
