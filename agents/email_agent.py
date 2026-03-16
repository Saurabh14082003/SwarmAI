import json
import re
from utils.llm import get_llm
from tools.tool_registry import run_tool
from utils.contacts import CONTACTS

llm = get_llm()


def extract_email(text):
    if not isinstance(text, str):
        return None
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    if match:
        return match.group()
    return None


def resolve_contact(name):

    name = name.lower()

    if name in CONTACTS:
        return CONTACTS[name]

    return None


def email_agent(state):

    query = state["query"]
    research = state.get("research_result", "")
    history = "\n".join(state["messages"])


    prompt = f"""
You are an email extraction agent.
You MUST extract email instructions and output ONLY valid JSON.
IMPORTANT: If the user refers to themselves (e.g., "me", "my"), use their name from the conversation history as the recipient.

Conversation history:
{history}

User request:
{query}

You MUST return exactly one valid JSON object in the following format, with NO conversational text:
{{
 "recipient": "name_or_email",
 "subject": "email subject"
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

        try:
            data = json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback: hunt for the JSON object
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                data = json.loads(text[start_idx:end_idx+1])
            else:
                raise ValueError("No JSON object found")

        recipient = data["recipient"]
        subject = data["subject"]

    except Exception as e:
        print(f"DEBUG EMAIL AGENT ERROR: {e}")
        
        # Try to find an email in the raw text response
        raw_text = getattr(response, 'content', str(response))
        email_from_text = extract_email(raw_text)
        
        if email_from_text:
            recipient = email_from_text
        else:
            # Try to find an email in the user query
            email_from_query = extract_email(query)
            if email_from_query:
                recipient = email_from_query
            else:
                recipient = "saurabh"

        subject = "AI Summary"

    # check if user directly gave email
    email = extract_email(recipient)

    if not email:

        email = resolve_contact(recipient)

    if not email:

        email = "saurabh.saini0904@gmail.com"

    result = run_tool(
        "email",
        to=email,
        subject=subject,
        message=research
    )

    return {
        "email_result": result,
        "completed_steps": state["completed_steps"] + ["email_agent"]
    }