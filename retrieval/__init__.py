import requests
import glob
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings

# Constants
OLLAMA_BASE_URL = "http://192.168.18.215:11434/"
EMBEDDING_MODEL = "nomic-embed-text"
DOC_PATH = "./data/*.md"
PERSIST_DIRECTORY = "./chroma_db"
TOP_K = 4  # Number of relevant docs to retrieve

print(f"OLLAMA_BASE_URL at '{OLLAMA_BASE_URL}'")

# Step 1: Custom Embedding class using Ollama
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
    
    



# Initialize vector DB
embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)

retriever = vectordb.as_retriever(search_kwargs={"k":TOP_K})


def generate_and_store_vector_embeddings():
    
    # Step 2: Load markdown files
    documents = []
    for path in glob.glob(DOC_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": path}))

    # Step 3: Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)


    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )

    vectordb.persist()
    print(f"✅ Chroma vector store created and saved to '{PERSIST_DIRECTORY}'")
    
    


from graph import State
def retrieve(state: State):
    print("---RETRIEVE---")
    
    last_message = state["messages"][-1]

    # Retrieval
    documents = retriever.invoke(last_message.content)
    # state["documents"].extend(documents)
    return {"documents": documents}