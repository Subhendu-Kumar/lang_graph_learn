from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


# create a state
class LLMState(TypedDict):
    question: str
    answer: str


def llm_qa(state: LLMState) -> LLMState:
    # extract the question from state
    question = state["question"]

    # form a prompt
    prompt = f"Answer the following question {question}"

    # ask that question to the LLM
    answer = gemini.invoke(prompt).content

    # update the answer in the state
    state["answer"] = answer

    return state


# create our graph
graph = StateGraph(LLMState)

# add nodes
graph.add_node("llm_qa", llm_qa)

# add edges
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

# compile
workflow = graph.compile()

# execute
intial_state = {"question": "How far is moon from the earth?"}

final_state = workflow.invoke(intial_state)

print(final_state)
