import requests

CATEGORIES_ENDPOINT_URL = 'http://localhost:8000/categories'

def get_categories() -> dict:
    response = requests.get(CATEGORIES_ENDPOINT_URL, headers={"accept": "application/json"})

    if response.status_code == 200:
        categories = response.json()
        categories_dict = {
            item["category_id"]: item["category_name"]
            for item in categories
        }
        return categories_dict
    else:
        raise Exception("Failed to fetch categories. Status code: {}".format(response.status_code))