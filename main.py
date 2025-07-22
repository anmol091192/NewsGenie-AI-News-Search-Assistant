import streamlit as st
import os
from dotenv import load_dotenv
from typing import TypedDict
from autogen import AssistantAgent, ConversableAgent, register_function
from langgraph.graph import StateGraph, START
from tools.news_tool import get_news
from tools.search_tool import search_the_internet

# --------- ENV & KEY SETUP ----------
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gnews_api_key = os.getenv("GNEWS_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
missing_keys = [k for k, v in [("GEMINI_API_KEY", gemini_api_key), ("GNEWS_API_KEY", gnews_api_key), ("SERPER_API_KEY", serper_api_key)] if not v]
if missing_keys:
    st.error(f"Missing API keys: {', '.join(missing_keys)}. Please check your .env file.")
    st.stop()

# --------- AGENTS ----------
assistant = AssistantAgent(
    name="NewsGenie_Agent",
    system_message=(
        "You are NewsGenie, a smart AI assistant. "
        "Use the news tool to fetch latest news (by category). "
        "Use the search tool for web information. Answer normally otherwise."
    ),
    llm_config={
        "config_list": [
            {
                "model": "gemini-2.5-flash",                
                "api_type": "google",
                "api_key": gemini_api_key
            }
        ],
        "temperature": 0.7,
    },
)
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: bool(msg.get("content")),
    human_input_mode="NEVER",
)
register_function(get_news, caller=assistant, executor=user_proxy, name="get_news", description="Fetch the latest news by category.")
register_function(search_the_internet, caller=assistant, executor=user_proxy, name="search_the_internet", description="Web search tool.")

# --------- LANGGRAPH STATEGRAPH ---------
class QueryState(TypedDict):
    category: str
    user_input: str
    response: str

def route_query(state: QueryState) -> str:
    """Decide which node to go to based on user input/category."""
    if state['category'] and state['category'] != "None":
        return "NewsNode"
    elif state['user_input']:
        return "SearchOrLLMNode"
    else:
        return "FallbackNode"

def news_node(state: QueryState) -> QueryState:
    """Call get_news and handle error fallback."""
    response = get_news(state['category'])
    if "Unable to fetch news" in response or "No news articles found" in response:
        # fallback to default response
        return {"category": state["category"], "user_input": state["user_input"], "response": "No news found or API error."}
    return {"category": state["category"], "user_input": state["user_input"], "response": response}

def search_or_llm_node(state: QueryState) -> QueryState:
    """Use search tool for generic queries, else let LLM answer."""
    # Use search if the query looks like a fact lookup, else LLM
    keywords = ["who", "what", "when", "where", "why", "how", "find", "show", "search"]
    if any(k in state["user_input"].lower() for k in keywords):
        response = response = search_the_internet(state["user_input"])
        return {"category": state["category"], "user_input": state["user_input"], "response": response}
    else:
        # LLM direct answer
        user_proxy.initiate_chat(assistant, message=state["user_input"])
        last_msg = assistant.last_message()
        response = last_msg["content"] if last_msg and last_msg.get("content") else "No response generated."
        return {"category": state["category"], "user_input": state["user_input"], "response": response}


# Build StateGraph
graph = StateGraph(QueryState)
graph.add_node("NewsNode", news_node)
graph.add_node("SearchOrLLMNode", search_or_llm_node)

graph.add_conditional_edges(START, route_query)

workflow = graph.compile()

# --------- STREAMLIT UI ---------
st.title("📰 NewsGenie: Your AI News & Search Assistant (LangGraph Edition)")
st.markdown("Ask for the latest news (by category), or any web information!")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask NewsGenie anything:")
category = st.selectbox(
    "Or pick a news category:",
    ["None", "business", "technology", "sports", "finance", "health", "entertainment", "science", "world", "politics"]
)

if st.button("Submit Query"):
    with st.spinner("Fetching response..."):
        query_state = QueryState(category=category, user_input=user_input, response="")
        result = workflow.invoke(query_state)
        # Display in history
        st.session_state.history.append(("User", user_input if category == "None" else f"News in {category}"))
        st.session_state.history.append(("NewsGenie", result["response"]))

for role, msg in st.session_state.history:
    if role == "User":
        st.markdown(f"**You:** {msg}")
    elif role == "NewsGenie":
        st.markdown(f"**NewsGenie:** {msg}")