import requests
from chain.graph_state import AgentState


EXPENSE_ENDPOINT_URL = "http://localhost:8000/expenses"

def save_expense_to_db(state: AgentState) -> AgentState:
    receipt_date = state.get("date", None)
    receipt_category_id = state.get("category_id", None)
    receipt_description = state.get("description", None)
    receipt_amount = state.get("amount", None)
    receipt_vat = state.get("vat", None)
    receipt_payment_method_id = state.get("payment_method_id", None)
    receipt_business_personal = state.get("business_personal", None)

    expense_data = {
        "date": receipt_date,
        "category_id": receipt_category_id,
        "description": receipt_description,
        "amount": receipt_amount,
        "vat": receipt_vat,
        "payment_method_id": receipt_payment_method_id,
        "business_personal": receipt_business_personal
    }

    response = requests.post(EXPENSE_ENDPOINT_URL, json=expense_data)

    if response.status_code in (200, 201):
        print("Expense data succesfully saved into DB")
    else:
        print(f"Failure to save expense data in DB with status code: {response.status_code}")