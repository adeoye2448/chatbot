from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model = "openai/gpt-oss-20b", api_key = os.getenv("GROQ_API_KEY"))

def feedback_llm(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a feedback bot. Thank the user for their feedback."),
        ("user", "issue: {issue}")
    ])

    chain = prompt | llm
    user_msg = state["messages"][-2].content
    response = chain.invoke({"issue": user_msg})

    return {"messages": state["messages"] + [response]}