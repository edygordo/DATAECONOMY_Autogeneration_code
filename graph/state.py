from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        user_input: takes user input as a string
        structured_requirement: This will contain a step by step process of how to convert the user_input to a python code in English language 
        python_code: This will contain the resultant python code which uses structured_requirement as an input
        test_case: This will contain the test case for the generated python code
        expected_output_for_test_case: This will contain the expected output for the test case
        executable_code: This will contain the executable version of the python code which has the test case augmented into it
        is_executable_and_correct: This will be a boolean variable which will say True if the code is executable and correct else false
        documentation: Simple documentation of the python_code
    """
    user_input: str
    structured_requirement: str
    python_code: str
    test_case: str
    expected_output_for_test_case: str
    is_executable_and_correct: bool
    documentation: str

