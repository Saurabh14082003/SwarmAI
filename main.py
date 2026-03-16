from graph.build_graph import build_graph

graph = build_graph()

state = {
    "messages": [],
    "plan": [],
    "completed_steps": []
}

while True:

    query = input("You: ")

    state["query"] = query

    result = graph.invoke(state)

    answer = result["final_answer"]

    print("Assistant:", answer)

    state["messages"].append(f"User: {query}")
    state["messages"].append(f"Assistant: {answer}")