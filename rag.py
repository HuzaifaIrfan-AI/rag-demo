from langchain_ollama import OllamaLLM
import requests
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document

# Constants
OLLAMA_BASE_URL = "http://192.168.18.215:11434/"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
PERSIST_DIRECTORY = "./chroma_db"
TOP_K = 4  # Number of relevant docs to retrieve

# Custom Embedding class (same as before)
class OllamaEmbeddings(Embeddings):
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434/"):
        self.model = model
        self.base_url = base_url

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = requests.post(
                f"{self.base_url}api/embeddings",
                json={"model": self.model, "prompt": text}
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]


llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1
)

# Ollama LLM call
def call_ollama_llm(prompt: str, model: str = LLM_MODEL, base_url: str = OLLAMA_BASE_URL) -> str:
    response= llm.invoke(prompt)
    return response

# Initialize vector DB
embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)

# RAG function
def rag_ask(question: str) -> str:
    # Step 1: Retrieve relevant documents
    docs = vectordb.similarity_search(question, k=TOP_K)

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

# 🔍 Example usage
if __name__ == "__main__":
    while(1):
        query = input("Ask a question: ")
        response = rag_ask(query)
        print("\n💬 Answer:")
        print(response)
