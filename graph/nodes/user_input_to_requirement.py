from typing import Any, Dict
from dotenv import load_dotenv
from graph.chains import generate_requirement_from_user_input

from graph.state import GraphState

load_dotenv()

def user_input_to_requirement(state: GraphState) -> Dict[str, Any]:
    print("---USER INPUT TO DEFINED REQUIREMENTS---")
    user_input = state.get("user_input")
    result_object = generate_requirement_from_user_input.invoke({"user_input": user_input}) # the answer will be a pydantic object
    structured_requirement = result_object.structured_requirement
    return {**state, "structured_requirement": structured_requirement}