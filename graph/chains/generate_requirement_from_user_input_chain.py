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
    structured_requirement: str = Field(description="Proper decomposition of user's requirement in a structural way for converting the input into a code.")

structured_requirement_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an experienced project manager. You would be given a user input in english form and you have to convert it into a proper " \
"defined structure. This defined structure would be used to generate a code so leave no area ambiguos if any field is ambiguos then make proper " \
"assumptions and proceed."


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The query:- {user_input}")
    ]
)

generate_requirement_from_user_input: RunnableSequence = answer_prompt | structured_requirement_extraction