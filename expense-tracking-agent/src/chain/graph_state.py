from langgraph import Graph
from datetime import date
from decimal import Decimal
from typing import TypedDict, Dict, Optional

class AgentState(TypedDict):
    user_decision: Optional[list]
    image_base64: Optional[str]
    image_location: Optional[str]
    date: Optional[date]
    category_id: Optional[int]
    description: Optional[str]
    amount: Optional[Decimal]
    vat: Optional[Decimal]
    payment_method_id: Optional[int]
    business_personal: Optional[str]
    category: Optional[str]
    payment_method: Optional[str]
    payment_methods: Optional[Dict[int, str]]
    categories: Optional[Dict[int, str]]
    vision_model_name: Optional[str]
    categorizer_model_name: Optional[str]
