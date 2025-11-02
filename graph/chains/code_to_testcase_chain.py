from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Go up two levels
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

google_api_key = os.getenv("GEMINI_API_KEY")
# llm = ChatOllama(model="llama3.2:1b")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)

class structuredExtraction(BaseModel):
    test_case: str = Field(description="The test case for the provided code.")
    expected_output_for_test_case: str = Field(description="The expected output of the generated test case.")

structured_testcase_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an experienced test case generator. You will be provided with user's input of what he wanted to design with a " \
"python code which implements user's input your role would be to generate a test case with it's expected output over the code."

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The user input is:- {user_input}. The python code which implement's the user input is:- {python_code}")
    ]
)

code_to_testcase_chain: RunnableSequence = answer_prompt | structured_testcase_extraction