from graph.state import GraphState
from graph.chains import requirements_to_code
from typing import Dict, Any


def coding_agent(state: GraphState)->Dict[str,Any]:
    print("-- CODING AGENT --")
    structured_requirement = state.get("structured_requirement")
    result_object = requirements_to_code.invoke({"requirements": structured_requirement}) # This will return a pydantic object
    python_code = result_object.python_code
    return {**state, "python_code": python_code}