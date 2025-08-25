from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal


class QuadState(TypedDict):
    a: int
    b: int
    c: int

    equation: str
    discriminant: float
    result: str


def show_equation(state: QuadState):
    equation = f"{state['a']}x^2 + {state['b']}x + {state['c']} = 0"
    return {"equation": equation}


def calc_discriminant(state: QuadState):
    discriminant = state["b"] ** 2 - (4 * state["a"] * state["c"])
    return {"discriminant": discriminant}


def real_roots(state: QuadState):
    root1 = (-state["b"] + state["discriminant"] ** 0.5) / (2 * state["a"])
    root2 = (-state["b"] - state["discriminant"] ** 0.5) / (2 * state["a"])
    return {"result": f"Real roots are: {root1} and {root2}"}


def repeated_roots(state: QuadState):
    root = -state["b"] / (2 * state["a"])
    return {"result": f"Repeated root is: {root}"}


def no_real_roots(state: QuadState):
    return {"result": "No real roots exist."}


def check_condition(
    state: QuadState,
) -> Literal["real_roots", "repeated_roots", "no_real_roots"]:
    if state["discriminant"] > 0:
        return "real_roots"
    elif state["discriminant"] == 0:
        return "repeated_roots"
    else:
        return "no_real_roots"


graph = StateGraph(QuadState)

graph.add_node("show_equation", show_equation)
graph.add_node("calc_discriminant", calc_discriminant)
graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)


graph.add_edge(START, "show_equation")
graph.add_edge("show_equation", "calc_discriminant")

graph.add_conditional_edges("calc_discriminant", check_condition)
graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)

workflow = graph.compile()

initial_state = {"a": 68, "b": 23, "c": 2}

result = workflow.invoke(initial_state)

print(result)
