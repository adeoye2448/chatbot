from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

language = ChatGroq(model = "openai/gpt-oss-20b", api_key = os.getenv("GROQ_API_KEY"))

def student_llm(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a student assistant bot. Classify the issue as department, courses or classes."),
        ("user", "issue: {issue}")
    ])

    chain = prompt | language
    user_msg = state["messages"][-1].content
    response = chain.invoke({"issue": user_msg})

    return {"messages": state["messages"] + [response]}


def router_decision(state):
    classification = state["messages"][-1].content.lower().strip()

    if "department" in classification:
        return "department_node"
    elif "courses" in classification:
        return "courses_node"
    elif "classes" in classification:
        return "classes_node"
    else:
        return "classes_node"