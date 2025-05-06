

from graph import graph

def rag_ask(query):
    
    state = {"question": query, "documents": []}
    
    state = graph.invoke(state)
    
    print(state)

    return state.get("generation")
    

# 🔍 Example usage
if __name__ == "__main__":
    while(1):
        query = input("Ask a question: ")
        response = rag_ask(query)
        print("\n💬 Answer:")
        print(response)
