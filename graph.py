from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from agents.student import student_llm, router_decision
from agents.department import department_llm
from agents.courses import courses_llm
from agents.classes import classes_llm

class State(TypedDict):
    messages : Annotated[list, add_messages]

def create_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("interface_node", student_llm)
    graph_builder.add_node("department_node", department_llm)
    graph_builder.add_node("courses_node", courses_llm)
    graph_builder.add_node("classes_node", classes_llm)

    graph_builder.add_edge(START, "student_node")

    graph_builder.add_conditional_edges(
        "student_node",
        router_decision,
        {
            "department_node": "department_node",
            "courses_node": "courses_node",
            "classes_node": "classes_node",
        }
    )

    graph_builder.add_edge("department_node", END)
    graph_builder.add_edge("courses_node", END)
    graph_builder.add_edge("classes_node", END)

    return graph_builder.compile()

graph = create_graph()