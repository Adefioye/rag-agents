from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.pydantic_v1 import BaseModel, Field  
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from chain.graph_state import AgentState
from chain.helpers.get_categories import get_categories
from chain.helpers.get_payment_methods import get_payment_methods


# Create ExpenseSchema data
class ReceiptSchema(BaseModel):
    """Information about the receipt"""
    date: str = Field(description="The date the receipt was made. Format should be MM-DD-YYYY")
    description: str = Field(description="A brief description of the receipt")
    amount: float = Field(description="The total amount paid")
    vat: float = Field(description="The total VAT (taxes) paid")
    business_personal: str = Field(description="Indicating whether the receipt is business or personal")
    payment_method: str = Field(description="Indicate the payment method")
    category: str = Field(description="The category the receipt belongs to")


def get_modified_receipt_data(state: AgentState) -> AgentState:

    receipt_date = state.get("date", "").strip()
    receipt_description = state.get("description", "").strip()
    receipt_amount = state.get("amount", "").strip()
    receipt_vat = state.get("vat", "").strip()
    receipt_business_personal = state.get("business_personal", "").strip()
    receipt_payment_method = state.get("payment_method", "").strip()
    receipt_category = state.get("category", "")

    RECEIPT_INFORMATION = f"""
    The following is a summary information of the receipt 
    - date = {receipt_date}
    - description = {receipt_description}
    - amount = {receipt_amount} 
    - vat = {receipt_vat} 
    - business_personal = {receipt_business_personal}
    - payment_method = {receipt_payment_method} 
    """

    # Print summary of receipt so user can provide instruction to change necessary information
    print(RECEIPT_INFORMATION)

    instructions = input("Tell the LLM what to change in the summary of receipts provide")

    categories = get_categories()
    payment_methods = get_payment_methods()

    SYSTEM_PROMPT_TEMPLATE = """
    ## Here is a summary information of the receipt 
    - date = {receipt_date}
    - description = {receipt_description}
    - amount = {receipt_amount} 
    - vat = {receipt_vat} 
    - business_personal = {receipt_business_personal}
    - payment_method = {receipt_payment_method} 
    - category = {receipt_category}

    ### Please change the summary based on the user feed back below:
    {instructions}

    If user wants you to modify category, choose category information in the following list:
    {categories}
    If user wants you to modify payment_method, choose the payment method information in the following list:
    {payment_methods}
    """

    prompt = ChatPromptTemplate.from_messages([
        ["system", SYSTEM_PROMPT_TEMPLATE.format(
            receipt_date=receipt_date, receipt_description=receipt_description, receipt_amount=receipt_amount, receipt_vat=receipt_vat,
            receipt_business_personal=receipt_business_personal, receipt_payment_method=receipt_payment_method, receipt_category=receipt_category,
            instructions=instructions, categories=", ".join(categories), payment_methods = ", ".join(payment_methods)
        )]
    ])

    vision_model_name = state.get("vision_model_name", "gpt-4-vision-preview") 

    structured_llm = ChatOpenAI(temperature=0, model=vision_model_name).with_structured_output(ReceiptSchema)

    prompt_message = {
        "type": "text",
        "text": prompt
    }

    messages = HumanMessage(content=[prompt_message])

    response = structured_llm.invoke([messages])

    return response.dict()

def modifier(state: AgentState) -> AgentState:

    new_state = state.copy()
    modified_receipt_data = get_modified_receipt_data(state)
    
    # Update, date, description, amount, vat, business_personal and payment_method
    new_state["date"] = modified_receipt_data.get("date", None)
    new_state["description"] = modified_receipt_data.get("description", None)
    new_state["amount"] = modified_receipt_data.get("amount", None)
    new_state["vat"] = modified_receipt_data.get("vat", None)
    new_state["business_personal"] = modified_receipt_data.get("business_personal", None)
    new_state["payment_method"] = modified_receipt_data.get("payment_method", None)

    # Set category_id on new state
    if "category" in new_state and "categories" in new_state:
        categories = new_state["categories"]
        category = new_state["category"]

        for key, value in categories.items():
            if value == category:
                new_state["category_id"] = key 
                break

    # Set payment_method_id on new state
    if "payment_method" in new_state and "payment_methods" in new_state:
        payment_methods = new_state["payment_methods"]
        payment_method = new_state["payment_method"]

        for key, value in payment_methods.items():
            if value == payment_method:
                new_state["payment_method_id"] = key 
                break
    
    print("New agent state after modifying receipt data with LLM: ", new_state)

    return new_state
