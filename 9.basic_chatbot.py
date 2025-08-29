from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage

load_dotenv()

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    # take user query from state
    messages = state["messages"]

    # send to llm
    response = gemini.invoke(messages)

    # response store state
    return {"messages": [response]}


graph = StateGraph(ChatState)

# add nodes
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile()


initial_state = {"messages": [HumanMessage(content="What is the capital of india")]}

result = chatbot.invoke(initial_state)

print(result)
