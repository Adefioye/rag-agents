from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.pydantic_v1 import BaseModel, Field  
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from chain.graph_state import AgentState
from chain.helpers.get_payment_methods import get_payment_methods

PAYMENT_METHODS_ENDPOINT = "http://localhost:8000/payment_methods"

# Create ExpenseSchema data
class ReceiptSchema(BaseModel):
    """Information about the receipt"""
    date: str = Field(description="The date the receipt was made. Format should be MM-DD-YYYY")
    description: str = Field(description="A brief description of the receipt")
    amount: float = Field(description="The total amount paid")
    vat: float = Field(description="The total VAT (taxes) paid")
    business_personal: str = Field(description="Indicating whether the receipt is business or personal")
    payment_method: str = Field(description="Indicate the payment method")


def get_receipt_data_with_llm(image_b64: str, state: AgentState):
    vision_model_name = state.get("vision_model_name", "gpt-4-vision-preview") 

    payment_methods = get_payment_methods()
    # Define the prompt
    SYSTEM_PROMPT_TEMPLATE = """
    You are an expert extraction algorithm.  
    Extract the following information from the text:  
    - Date  
    - Description  
    - Amount  
    - VAT  
    - Whether the expense is for business or personal use  
    - Payment method (options: {payment_methods})  
    If you do not know the value of an attribute asked to extract, you may omit the attribute's value.
    """

    prompt = ChatPromptTemplate.from_messages([
        ["system", SYSTEM_PROMPT_TEMPLATE.format(payment_methods = ", ".join(payment_methods))]
    ])

    structured_llm = ChatOpenAI(temperature=0, model=vision_model_name).with_structured_output(ReceiptSchema)

    image_message = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_b64}"
        }
    }

    prompt_message = {
        "type": "text",
        "text": prompt
    }

    messages = HumanMessage(content=[prompt_message, image_message])

    response = structured_llm.invoke([messages])

    return response.dict()

def json_parser(state: AgentState) -> AgentState:

    new_state = state.copy()
    image_b64 = state.get("image_base64", "").strip()
    receipt_data = get_receipt_data_with_llm(image_b64, state)
    
    # Update, date, description, amount, vat, business_personal and payment_method
    new_state["date"] = receipt_data.get("date", None)
    new_state["description"] = receipt_data.get("description", None)
    new_state["amount"] = receipt_data.get("amount", None)
    new_state["vat"] = receipt_data.get("vat", None)
    new_state["business_personal"] = receipt_data.get("business_personal", None)
    new_state["payment_method"] = receipt_data.get("payment_method", None)

    print("New agent state after updating with receipt data: ", new_state)

    return new_state
