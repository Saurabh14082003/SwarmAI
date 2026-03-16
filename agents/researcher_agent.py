import json
from utils.llm import get_llm
from tools.tool_registry import run_tool, TOOLS

llm = get_llm()


def research_agent(state):

    query = state["query"]
    history = "\n".join(state["messages"])
    tool_prompt = f"""
You are an AI research agent.

Available tools:
search

Conversation history:
{history}

User query:
{query}

Use the history if needed to answer.
Decide which tool to use.

Return JSON:
{{
 "tool": "tool_name",
 "input": "tool_input"
}}
"""

    response = llm.invoke(tool_prompt)

    try:
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        decision = json.loads(text.strip())

        tool = decision["tool"]
        tool_input = decision["input"]

    except:
        tool = "search"
        tool_input = query

    tool_result = run_tool(tool, tool_input)

    answer_prompt = f"""
User query:
{query}

Tool results:
{tool_result}

Provide a clear summarized answer.
"""

    final = llm.invoke(answer_prompt)

    return {
        "research_result": final.content,
        "completed_steps": state["completed_steps"] + ["research_agent"]
    }