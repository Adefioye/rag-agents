import requests

PAYMENT_METHODS_ENDPOINT_URL = "http://localhost:8000/payment_methods"

def get_payment_methods() -> dict:
    
    response = requests.get(PAYMENT_METHODS_ENDPOINT_URL, headers={"accept": "application/json"})

    if response.status_code == 200:
        payment_methods = response.json()
        payment_methods_dict = {
            item["payment_method_id"]: item["payment_method_name"]
            for item in payment_methods
        }
        return payment_methods_dict
    else:
        raise Exception("Failed to fetch payment methods. Status code: {}".format(response.status_code))
