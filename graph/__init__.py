

from retrieval import retrieve

from generation import generate


from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from .State import State
    
graph_builder = StateGraph(State)

# Define the nodes
graph_builder.add_node("retrieve", retrieve) # retrieve
graph_builder.add_node("generate", generate) # generatae 

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile()




if __name__ == "__main__":
    png_bytes = graph.get_graph().draw_png()  # Returns a graphviz.Digraph object
    # Write the bytes to a file
    with open("langgraph_output.png", "wb") as f:
        f.write(png_bytes)