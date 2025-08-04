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

# Get free APIs from environment (will be set in Streamlit Cloud)
gnews_api_key = os.getenv("GNEWS_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Check if free APIs are available in environment
free_apis_missing = [k for k, v in [("GNEWS_API_KEY", gnews_api_key), ("SERPER_API_KEY", serper_api_key)] if not v]
if free_apis_missing:
    st.error(f"Service temporarily unavailable. Missing: {', '.join(free_apis_missing)}")
    st.stop()

# --------- STREAMLIT UI FOR API KEY INPUT ---------
st.title("📰 NewsGenie: Your AI News & Search Assistant")
st.markdown("Ask for the latest news (by category), or any web information!")

# API Key Input Section
with st.expander("🔑 API Configuration", expanded=not st.session_state.get("gemini_api_key")):
    st.markdown("""
    **To use NewsGenie, you need a Gemini API key:**
    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Create a free account and generate an API key
    3. Paste it below
    
    *Your API key is stored only in your browser session and is not saved anywhere.*
    """)
    
    gemini_api_key_input = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        placeholder="Your Gemini API key here...",
        help="Get your free API key from Google AI Studio"
    )
    
    if st.button("Set API Key"):
        if gemini_api_key_input.strip():
            st.session_state.gemini_api_key = gemini_api_key_input.strip()
            st.success("✅ API key set successfully!")
            st.rerun()
        else:
            st.error("Please enter a valid API key")

# Check if Gemini API key is set
if not st.session_state.get("gemini_api_key"):
    st.warning("🔑 Please set your Gemini API key above to start using NewsGenie.")
    st.stop()

gemini_api_key = st.session_state.gemini_api_key

# --------- AGENTS ----------
try:
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
    
except Exception as e:
    st.error(f"❌ Invalid API key. Please check your Gemini API key and try again.")
    if st.button("Reset API Key"):
        del st.session_state.gemini_api_key
        st.rerun()
    st.stop()

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
        return {"category": state["category"], "user_input": state["user_input"], "response": "No news found or API error."}
    return {"category": state["category"], "user_input": state["user_input"], "response": response}

def search_or_llm_node(state: QueryState) -> QueryState:
    """Use search tool for generic queries, else let LLM answer."""
    keywords = ["who", "what", "when", "where", "why", "how", "find", "show", "search"]
    if any(k in state["user_input"].lower() for k in keywords):
        response = search_the_internet(state["user_input"])
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

# --------- MAIN UI ---------
# Show current API status
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Change API Key"):
        del st.session_state.gemini_api_key
        st.rerun()

st.markdown("---")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask NewsGenie anything:")
category = st.selectbox(
    "Or pick a news category:",
    ["None", "business", "technology", "sports", "finance", "health", "entertainment", "science", "world", "politics"]
)

# Auto-reset logic: if user types something, reset category to None
if user_input.strip() and category != "None":
    st.info("💡 Category automatically reset to 'None' since you entered a text query.")
    category = "None"

# Auto-reset logic: if user selects category, clear text input
if category != "None" and user_input.strip():
    st.info("💡 Text input will be ignored since you selected a news category.")
    user_input = ""

if st.button("Submit Query"):
    if not user_input.strip() and category == "None":
        st.warning("Please enter a question or select a news category.")
    else:
        with st.spinner("Fetching response..."):
            try:
                query_state = QueryState(category=category, user_input=user_input, response="")
                result = workflow.invoke(query_state)
                # Display in history
                st.session_state.history.insert(0, ("NewsGenie", result["response"]))
                st.session_state.history.insert(0, ("User", user_input if category == "None" else f"News in {category}"))
            except Exception as e:
                st.error(f"Error processing your request: {str(e)}")

# Display conversation history
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 💬 Conversation")
    
for role, msg in st.session_state.history:
    if role == "User":
        st.markdown(f"**You:** {msg}")
    elif role == "NewsGenie":
        st.markdown(f"**NewsGenie:** {msg}")
        st.markdown("---")

# Clear history button
if st.session_state.history:
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()