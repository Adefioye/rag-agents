import base64
from src.chain.graph_state import AgentState

def encode_image(image_path: str) -> str:

    with open(image_path, "rb") as image_file:
        image_b64_str = base64.b64encode(image_file.read()).decode("utf-8")
    
    return image_b64_str

def image_encoder(state: AgentState) -> AgentState:
    image_location = state.get("image_location", "").strip()
    image_base64 = encode_image(image_location)
    new_state = state.copy()

    # Update image_base64 state
    new_state["image_base64"] = image_base64

    return new_state