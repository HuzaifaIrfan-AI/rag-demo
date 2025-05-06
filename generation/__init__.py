

from langchain_ollama import OllamaLLM
import requests
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser

# Constants
OLLAMA_BASE_URL = "http://192.168.18.215:11434/"
LLM_MODEL = "llama3.2"





llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1
)

from State import State
def generate(state: State):    
    print("---GENERATE---")
    
    last_message = state["messages"][-1]
    documents = state["documents"]
    message=f"""
Context:
{documents}

Question:
{last_message.content}
    """
    
    messages = [
        {"role": "system",
         "content": """You are customer chatbot assistant on Middlehost web hosting platform.
Give short reply.
If unsure, reply "handover" to transfer the conversation to human support.
If the customer want to talk to human reply "handover"
Answer the question using only the context below."""
         }
    ]
    
    # messages.extend(state["messages"])
    messages.extend([{
            "role": "user",
            "content": message
        }])
    
    generation = llm.invoke(messages)
    
    return {"messages": [{"role": "assistant", "content": generation}]}