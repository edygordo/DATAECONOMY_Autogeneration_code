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
    documentation: str = Field(description="A detailed documentation of how to use the code and what it does along with time complexity analysis.")


documentation_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an experience code reviewer. Your job will be to generate a detailed documentation on what the code does how it has been implemented" \
"and how can another person use it. You should give time complexity analysis of the provided code and also inform other user's on how to use it for their" \
"purpose."


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The python code:- {code}.")
    ]
)

code_to_documentation_chain: RunnableSequence = answer_prompt | documentation_extraction