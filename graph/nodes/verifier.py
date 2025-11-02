from typing import Any, Dict
from graph.state import GraphState
from graph.helpers import checkValidityAndCorrectness
from graph.chains import augment_code_with_testcase_chain

def verifier(state: GraphState)->Dict[str, Any]:
    print("-- VERIFIER --")
    python_code = state.get("python_code")
    test_case = state.get("test_case")
    expected_output = state.get("expected_output_for_test_case")
    augmented_code = augment_code_with_testcase_chain.invoke({"python_code": python_code, "test_case": test_case})
    executable_code = augmented_code.executable_code
    is_executable_and_correct = checkValidityAndCorrectness(user_code=executable_code, expected_output=expected_output)
    return {**state, "is_executable_and_correct": is_executable_and_correct}