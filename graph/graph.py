from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from graph.consts import INPUT_TO_REQUIREMENT, CODING_AGENT, TEST_CASE_GENERATOR,VERIFIER, DOCUMENTATION_GENERATOR
from graph.nodes import user_input_to_requirement, coding_agent, test_case_generator, verifier, documentation_generator
from graph.state import GraphState

load_dotenv()

def decide_if_generated_code_correct(state: GraphState)->str:
    is_code_executable_and_correct: bool = state.get("is_executable_and_correct")
    if is_code_executable_and_correct:
        return DOCUMENTATION_GENERATOR
    else:
        return CODING_AGENT


workflow = StateGraph(GraphState)

# Add Node to Graph
workflow.add_edge(START, INPUT_TO_REQUIREMENT)
workflow.add_node(INPUT_TO_REQUIREMENT, user_input_to_requirement)
workflow.add_node(CODING_AGENT, coding_agent)
workflow.add_node(TEST_CASE_GENERATOR, test_case_generator)
workflow.add_node(VERIFIER, verifier)
workflow.add_node(DOCUMENTATION_GENERATOR, documentation_generator)

# Add connections between nodes in the Graph
workflow.set_entry_point(INPUT_TO_REQUIREMENT) 
workflow.add_edge(INPUT_TO_REQUIREMENT, CODING_AGENT)
workflow.add_edge(CODING_AGENT, TEST_CASE_GENERATOR)
workflow.add_edge(TEST_CASE_GENERATOR, VERIFIER)

workflow.add_conditional_edges(
    VERIFIER,
    decide_if_generated_code_correct,
    {
        DOCUMENTATION_GENERATOR: DOCUMENTATION_GENERATOR,
        CODING_AGENT: CODING_AGENT
    }    
)

workflow.add_edge(DOCUMENTATION_GENERATOR, END)

app = workflow.compile()

# Generate a diagram
app.get_graph().draw_mermaid_png(output_file_path="Automatic_Codegenerator.png")