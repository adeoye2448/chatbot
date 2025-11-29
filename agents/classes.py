from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

language = ChatGroq(model = "openai/gpt-oss-20b", api_key = os.getenv("GROQ_API_KEY"))

def classes_llm(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a class bot. Help the user with class allocation issues(from class A-D) according to deparment."),
        ("user", "issue: {issue}")
    ])

    chain = prompt | language
    user_msg = state["messages"][-2].content
    response = chain.invoke({"issue": user_msg})

    return {"messages": state["messages"] + [response]}