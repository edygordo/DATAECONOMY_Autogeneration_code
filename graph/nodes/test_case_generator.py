from graph.state import GraphState
from typing import Dict, Any
from graph.chains import code_to_testcase_chain

def test_case_generator(state:GraphState)->Dict[str, Any]:
    print("-- TESTCASE GENERATOR --")
    python_code = state.get("python_code")
    user_input = state.get("user_input")
    result_object = code_to_testcase_chain.invoke({"python_code": python_code, "user_input": user_input}) # It will return a pydantic object
    test_case = result_object.test_case
    expected_output_for_test_case = result_object.expected_output_for_test_case
    return {**state, "test_case": test_case, "expected_output_for_test_case": expected_output_for_test_case}

