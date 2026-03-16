def controller(state):

    plan = state["plan"]
    completed = state["completed_steps"]

    if len(completed) >= len(plan):

        return {
            "next": "finish"
        }

    next_step = plan[len(completed)]

    return {
        "next": next_step
    }