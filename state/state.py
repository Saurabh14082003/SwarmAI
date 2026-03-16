from typing import TypedDict, List, Optional


class GraphState(TypedDict):

    query: str
    messages: List[str]

    plan: List[str]
    completed_steps: List[str]

    next: Optional[str]

    research_result: Optional[str]
    email_result: Optional[str]
    calendar_result: Optional[str]

    final_answer: Optional[str]