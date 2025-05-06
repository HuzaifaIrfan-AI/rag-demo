

from graph import graph, State

def main():    
    state = State(messages=[],documents=[])

    while(1):
        query = input("Ask a question: ")
        
        state["messages"] = state.get("messages", []) + [
        {"role": "user", "content": query}
        ]
    
        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message.content}")
            




# 🔍 Example usage
if __name__ == "__main__":
    main()

        