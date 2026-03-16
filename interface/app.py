import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.build_graph import build_graph

graph = build_graph()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="SwarmAI | Agentic Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@500;700&display=swap');

    :root {
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --accent-color: #6366f1;
        --text-main: #e2e8f0;
    }

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Header */
    .app-header {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid var(--glass-border);
    }
    
    .sidebar-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
    }

    /* Chat Styling */
    .stChatMessage {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 1rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(5px);
    }

    .stChatMessage[data-testid="stChatMessageUser"] {
        background: rgba(99, 102, 241, 0.1) !important;
    }

    /* Override buttons and inputs */
    .stButton>button {
        border-radius: 0.5rem;
        background: var(--accent-color);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---

# Header Section
with st.container():
    st.markdown("""
        <div class='app-header'>
            <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🤖 SwarmAI Assistant</h1>
            <p style='font-size: 1.2rem; opacity: 0.8;'>Precise • Agentic • Scalable</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("I am **SwarmAI**, your multi-agent assistant. I can **search the web**, **send emails**, and **schedule calendar events** powered by official **MCP servers**.")
    with col2:
        st.info("🚀 System is **Online** & ready to assist.")

st.divider()

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "plan": [],
        "completed_steps": []
    }

# Sidebar for Agent Activity
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛠️ Control Room</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        if st.session_state.state["plan"]:
            st.subheader("Current Mission")
            for step in st.session_state.state["plan"]:
                status = "✅" if step in st.session_state.state["completed_steps"] else "🕒"
                label = step.replace('_', ' ').title()
                st.write(f"{status} **{label}**")
        else:
            st.write("🌌 No active missions.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v2.0 Beta | Powered by Groq & MCP")

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# user input
user_input = st.chat_input("Enter your command...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # update graph state
    st.session_state.state["query"] = user_input
    st.session_state.state["plan"] = []
    st.session_state.state["completed_steps"] = []

    with st.spinner("SwarmAI Orchestration in progress..."):
        result = graph.invoke(st.session_state.state)
        
        # Sync the internal state back to session state for the sidebar display
        st.session_state.state["plan"] = result.get("plan", [])
        st.session_state.state["completed_steps"] = result.get("completed_steps", [])

    answer = result.get("final_answer", "Sorry, I couldn't generate a final answer.")

    # show assistant response
    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # update conversation memory
    st.session_state.state["messages"].append(f"User: {user_input}")
    st.session_state.state["messages"].append(f"Assistant: {answer}")
    
    st.rerun()