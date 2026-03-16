def finish_agent(state):

    if state.get("calendar_result"):
        answer = state["calendar_result"]

    elif state.get("email_result"):
        answer = state["email_result"]

    elif state.get("research_result"):
        answer = state["research_result"]

    else:
        answer = "Task completed."

    return {
        "final_answer": answer
    }