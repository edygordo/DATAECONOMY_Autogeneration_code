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
    python_code: str = Field(description="A python code from structured requirements")

structured_code_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an experienced coding agent. You will be provided with a requirement set and you would have to generate a python code from it." \
"Make sure the code is well written and is logically correct."

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The requirements are:- {requirements}")
    ]
)

requirements_to_code: RunnableSequence = answer_prompt | structured_code_extraction