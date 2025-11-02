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
    executable_code: str = Field(description="Executable version of python code which has test case as parameters in it and the funtion calling has been done to generate output on stdout screen.")

augmented_code_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an experienced coder. You will be given a code and a test case. Your role would be to just re-write the existing code such that" \
" the code can be directly executed by a python subprocess while being passed as a string. Note the output of the test case should be printed out to the console" \
"such that the output is captured by stdout screen."


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The python code:- {python_code}. The test case for augmentation is:- {test_case}")
    ]
)

augment_code_with_testcase_chain: RunnableSequence = answer_prompt | augmented_code_extraction