from datetime import date
from decimal import Decimal
from typing import TypedDict, Dict, Optional, Union
from api.payment_methods_routes import get_payment_methods
from chain.helpers.get_categories import get_categories
from langgraph.graph import StateGraph

from src.chain.nodes.image_encoder import image_encoder
from src.chain.nodes.json_parser import json_parser
from src.chain.nodes.categorizer import categorizer
from src.chain.nodes.human_checker import human_checker
from src.chain.nodes.modifier import modifier
from src.chain.nodes.save_expense_to_db import save_expense_to_db

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

def create_graph_state() -> AgentState:

    categories = get_categories()
    payment_methods = get_payment_methods()

    return {
        "user_decision": None,
        "image_base64": None,
        "image_location": None,
        "date": None,
        "category_id": None,
        "description": None,
        "amount": None,
        "vat": None,
        "payment_method_id": None,
        "business_personal": None,
        "category": None,
        "payment_method": None,
        "payment_methods": payment_methods,
        "categories": categories,
        "vision_model_name": "gpt-4-vision-preview",
        "categorizer_model_name": "gpt-4-turbo"
    }

def setup_agent_graph():
    agentState = create_graph_state()
    graph = StateGraph(agentState)

    graph.add_node("image_encoder", image_encoder)
    graph.add_node("json_parser", json_parser)
    graph.add_node("categorizer", categorizer)
    graph.add_node("human_checker", human_checker)
    graph.add_node("modifier", modifier)
    graph.add_node("save_expense_to_db", save_expense_to_db)

    graph.add_edge("image_encoder", "json_parser")
    graph.add_edge("json_parser", "categorizer")
    graph.add_edge("categorizer", "human_checker")

    def decide_after_human_checker(state: AgentState) -> Union[str, None]:

        if state["user_decision"] == "accept":
            return "save_expense_to_db"
        elif state["user_decision"] == "change_model":
            return "json_parser"
        elif state["user_decision"] == "revise":
            return "modifier"
        else:
            return None


    graph.add_conditional_edges(
        "human_checker", 
        decide_after_human_checker,
        {
            "save_expense_to_db": "save_expense_to_db",
            "json_parser": "json_parser",
            "modifier": "modifier"
        }
    )

    graph.add_edge("modifier", "human_checker")

    graph.set_entry_point("image_encoder")
    graph.set_finish_point("save_expense_to_db")

    return graph

# def main():

    # initial_graph_state = create_graph_state()
    # graph = setup_agent_graph()

    # TODO Set image location for agent state
    # initial_graph_state["image_location"] 

    # workflow = graph.compile()

    # app = workflow.invoke(initial_graph_state)

    # print("Agent finish running")

# if __name__ == "__main__":
#     main()