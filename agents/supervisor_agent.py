import json
from utils.llm import get_llm

llm = get_llm()

AVAILABLE_AGENTS = [
    "research_agent",
    "email_agent",
    "calendar_agent"
]


def fallback_planner(query: str):

    plan = []

    if any(word in query.lower() for word in ["email", "gmail", "mail", "send"]):
        plan.append("email_agent")

    if any(word in query.lower() for word in ["calendar", "schedule", "meeting", "appointment"]):
        plan.append("calendar_agent")

    plan.insert(0, "research_agent")

    return plan


def supervisor_planner(state):

    if state.get("plan"):
        return {"plan": state["plan"]}

    query = state["query"]

    prompt = f"""
You are a planner AI.

Available agents:
research_agent
email_agent
calendar_agent

Create a step-by-step plan using only these agents.

User request:
{query}

Return JSON list.
"""

    try:

        response = llm.invoke(prompt)
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        plan = json.loads(text.strip())

        if not isinstance(plan, list):
            raise ValueError("Invalid plan")

        for step in plan:
            if step not in AVAILABLE_AGENTS:
                raise ValueError("Invalid agent")

        return {"plan": plan, "completed_steps": []}

    except Exception:

        plan = fallback_planner(query)

        return {"plan": plan, "completed_steps": []}