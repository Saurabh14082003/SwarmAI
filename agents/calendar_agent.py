import json
from utils.llm import get_llm
from tools.tool_registry import run_tool

llm = get_llm()


def calendar_agent(state):

    query = state["query"]

    prompt = f"""
Extract meeting details from the user request.

User request:
{query}

Return JSON:

{{
 "title": "meeting title",
 "time": "YYYY-MM-DDTHH:MM"
}}
"""

    response = llm.invoke(prompt)

    try:
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        data = json.loads(text.strip())

        title = data["title"]
        time = data["time"]

    except:

        title = "Meeting"
        time = "2026-03-15T10:00"

    result = run_tool(
        "calendar",
        summary=title,
        start_time=time
    )

    return {
        "calendar_result": result,
        "completed_steps": state["completed_steps"] + ["calendar_agent"]
    }