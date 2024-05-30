import yaml
import requests

CONFIG_FILE_PATH = "config.yml"
BASE_URL = "http://localhost:8000"
CATEGORIES_ENDPOINT = f"{BASE_URL}/categories"
PAYMENT_METHODS_ENDPOINT = f"{BASE_URL}/payment_methods"


with open(CONFIG_FILE_PATH, "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

categories = config.get("categories", [])
payment_methods = config.get("payment_methods", [])

def save_data_to_db(endpoint, data):
    response = requests.post(endpoint, json=data)
    if response.status_code in (200, 201):
        print(f"Successfully created: {data}")
    else:
        print(f"Error creating {data}: {response.status_code}")

for category in categories:
    category_data = {"category_name": category }
    save_data_to_db(CATEGORIES_ENDPOINT, category_data)

for payment_method in payment_methods:
    payment_method_data = {"payment_method_name": payment_method }
    save_data_to_db(PAYMENT_METHODS_ENDPOINT, payment_method_data)