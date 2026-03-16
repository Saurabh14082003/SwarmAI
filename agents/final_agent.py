def final_agent(state):

    if state.get("research_result"):
        final = state["research_result"]

    elif state.get("email_result"):
        final = state["email_result"]

    elif state.get("calendar_result"):
        final = state["calendar_result"]

    else:
        final = "Task completed."

    return {"final_answer": final}