from typing import Any, Dict
from graph.state import GraphState
from graph.chains import code_to_documentation_chain

def documentation_generator(state: GraphState) -> Dict[str, Any]:
    python_code = state.get("python_code")
    result_object = code_to_documentation_chain.invoke({"code": python_code}) # This will return a pydantic object
    documentation = result_object.documentation
    return {**state, "documentation": documentation}