from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  
from langchain_core.messages import HumanMessage

from chain.graph_state import AgentState
from chain.helpers.get_categories import get_categories  

class Category(BaseModel):
    "This contains information of the receipt category"
    category: str = Field(description="This describes the category of the receipt")


def categorizer(state: AgentState) -> AgentState:
    receipt_date = state.get("date", None)
    receipt_description = state.get("description", None)
    receipt_amount = state.get("amount", None)
    receipt_vat = state.get("vat", None)
    receipt_business_personal = state.get("business_personal", None)
    receipt_payment_method = state.get("payment_method", None)

    category_list = get_categories().values()

    SYSTEM_PROMPT_TEMPLATE = """
    The following is a summary information of the receipt 
    - date = {receipt_date}
    - description = {receipt_description}
    - amount = {receipt_amount} 
    - vat = {receipt_vat} 
    - business_personal = {receipt_business_personal}
    - payment_method = {receipt_payment_method} 
    
    Based on the information above, Please select the category best suited for the
    information in the following list:
    {category_list}
    """

    prompt = ChatPromptTemplate.format_messages([
        ["system", SYSTEM_PROMPT_TEMPLATE.format(
            receipt_date=receipt_date, receipt_description=receipt_description, receipt_amount=receipt_amount, 
            receipt_vat=receipt_vat, receipt_business_personal=receipt_business_personal, receipt_payment_method=receipt_payment_method,
            category_list=", ".join(category_list)
        )]
    ])

    categorizer_model_name = state.get("categorizer_model_name", "gpt-3.5-turbo")

    llm = ChatOpenAI(temperature=0, model=categorizer_model_name)
    structured_llm = llm.with_structured_output(Category)
    text_message = { "type": "text", "text": prompt}
    messages = HumanMessage(content=[text_message])
    response = structured_llm.invoke([messages])
    selected_category = response.dict().get("category", None)

    new_state = state.copy()

    new_state["category"] = selected_category

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
    
    print("New graph state after using categorizer: ", new_state)
    return new_state

