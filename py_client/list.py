import requests
from basic import BASE as PRODUCT_BASE, MAIN_ENDPOINT
from getpass import getpass

AUTH_ENDPOINT = MAIN_ENDPOINT + 'auth/'
ENDPOINT = "list-create/"
URL = PRODUCT_BASE + ENDPOINT

username = input("Enter username: ").strip()
password = getpass("Enter password: ")


# CREATES TOKEN FOR THE USER
auth_response = requests.post(AUTH_ENDPOINT, json={
    'username': username,
    "password": password
})

print(auth_response.json())
if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"BEARER {token}"
    }

    get_response = requests.get(PRODUCT_BASE, headers=headers)
    print(get_response.json())
