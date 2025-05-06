

from retrieval import retrieve

from generation import generate


def rag_ask(query):
    docs=retrieve(query)
    res=generate(query, docs)
    return res
    

# 🔍 Example usage
if __name__ == "__main__":
    while(1):
        query = input("Ask a question: ")
        response = rag_ask(query)
        print("\n💬 Answer:")
        print(response)
