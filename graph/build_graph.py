from langgraph.graph import StateGraph, END
from state.state import GraphState
from agents.supervisor_agent import supervisor_planner
from agents.researcher_agent import research_agent
from agents.finish_agent import finish_agent
from agents.controller import controller
from agents.email_agent import email_agent
from agents.calendar_agent import calendar_agent

def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("planner", supervisor_planner)
    workflow.add_node("controller", controller)

    workflow.add_node("research_agent", research_agent)
    workflow.add_node("email_agent", email_agent)
    workflow.add_node("calendar_agent", calendar_agent)
    workflow.add_node("finish", finish_agent)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "controller")

    workflow.add_conditional_edges(
        "controller",
        lambda state: state["next"],
        {
    "research_agent": "research_agent",
    "email_agent": "email_agent",
    "calendar_agent": "calendar_agent",
    "finish": "finish"
}
    )

    workflow.add_edge("research_agent", "controller")
    workflow.add_edge("email_agent", "controller")
    workflow.add_edge("calendar_agent", "controller")

    workflow.add_edge("finish", END)

    return workflow.compile()