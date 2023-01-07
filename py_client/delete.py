import requests

product_id = input("What id the product id you want to delete? ")
try:
    product_id = int(product_id)
except:
    product_id = None
    print(f"{product_id} is not a valid id")

if product_id:
    ENDPOINT = f"http://localhost:8000/api/products/{product_id}/delete/"

    get_response = requests.delete(ENDPOINT)
    print(get_response.json())
