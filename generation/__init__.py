

from langchain_ollama import OllamaLLM
import requests
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document

# Constants
OLLAMA_BASE_URL = "http://192.168.18.215:11434/"
LLM_MODEL = "llama3.2"





llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1
)

# Ollama LLM call
def call_ollama_llm(prompt: str, model: str = LLM_MODEL, base_url: str = OLLAMA_BASE_URL) -> str:
    response= llm.invoke(prompt)
    return response



# RAG function
def generate(question: str, docs: list) -> str:


    # Step 2: Construct prompt for LLM
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""You are customer chatbot assistant on Middlehost web hosting platform.
Give short reply
If unsure, reply "handover" to transfer the conversation to human support.
If the customer want to talk to human reply "handover"
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:"""

    # Step 3: Get response from LLM
    answer = call_ollama_llm(prompt)
    return answer