from src.chain.graph_state import AgentState


def human_checker(state: AgentState) -> AgentState:

    receipt_date = state.get("date", None).strip()
    receipt_description = state.get("description", None).strip()
    receipt_amount = state.get("amount", None).strip()
    receipt_vat = state.get("vat", None).strip()
    receipt_business_personal = state.get("business_personal", None).strip()
    receipt_payment_method = state.get("payment_method", None).strip()

    RECEIPT_INFORMATION = f"""
    The following is a summary information of the receipt 
    - date = {receipt_date}
    - description = {receipt_description}
    - amount = {receipt_amount} 
    - vat = {receipt_vat} 
    - business_personal = {receipt_business_personal}
    - payment_method = {receipt_payment_method} 
    """
    
    # This shows receipt information to the human in the loop for verification
    print(RECEIPT_INFORMATION)

    new_state = state.copy()

    choice = input("Choose a(accept), change_model(m) or r(revise): ")

    if choice.strip() == "a":
        new_state["user_decision"] = "accept"
    elif choice.strip() == "m":
        new_state["user_decision"] = "change_model"
        # TODO: Change the vision_model_name in the agent state
    elif choice.strip() == "r":
        new_state["user_decision"] = "revise"
    else:
        new_state["user_decision"] = None

    return new_state
