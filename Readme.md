# 📰 NewsGenie: AI News & Web Search Assistant

**NewsGenie** is an AI-powered Streamlit app that lets you chat with a smart assistant to:
- Get the latest news headlines by category (like technology, sports, business, etc.)
- Search the web for answers to general queries
- Benefit from a robust workflow with error handling and fallback logic
- Powered by Google Gemini LLM, GNews API, Serper search, AutoGen, and LangGraph for agentic workflows

---

## 🚀 Features

- **AI Chatbot:** Handles both news and generic information queries in natural language.
- **News Integration:** Fetches real-time news using GNews API.
- **Web Search:** Answers factual questions via Serper Google Search API.
- **LangGraph Workflow:** Node-based decision routing for reliable, optimized query handling.
- **User-Friendly API Key Input:** Secure interface for users to input their own Gemini API key.
- **Robust Error Handling:** Graceful fallbacks for missing API keys, network issues, or no news results.
- **Interactive UI:** Clean Streamlit interface with conversation history and latest responses shown first.
- **Mutual Exclusivity:** Smart input handling - either text query OR news category, not both.

---

## 📂 Project Structure

```plaintext
NewsGenie/
├── tools/
│   ├── news_tool.py          # Fetches news using GNews API
│   └── search_tool.py        # Performs web search using Serper API
├── venv/                     # Python virtual environment
├── .env                      # API keys (not checked into GitHub)
├── main.py                   # Main Streamlit app, agent setup, workflow logic
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore               # Git ignore file
```

---

## 🛠️ Setup Instructions

### 1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/NewsGenie.git
cd NewsGenie
```

### 2. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate       # On macOS/Linux
# or
venv\Scripts\activate          # On Windows
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Configure environment variables (For Local Development)**

Create a `.env` file in the project root:

```bash
# Only needed for local development
GNEWS_API_KEY=your_gnews_api_key
SERPER_API_KEY=your_serper_api_key
```

**Note:** You don't need to add `GEMINI_API_KEY` to the `.env` file as users will input it directly in the app interface.

Get free API keys from:
- **GNews API:** https://gnews.io/
- **Serper.dev:** https://serper.dev/

### 5. **Run the app**

```bash
streamlit run main.py
```
The app will open in your browser (typically at http://localhost:8501).

---

## 🌐 Live Demo

**Try NewsGenie without any setup:** [Deployed on Streamlit Cloud]

*Just bring your own Gemini API key!*

---

## ✨ How To Use

### **Getting Started**
1. **Get a Gemini API Key:** Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free account to get your API key.
2. **Enter API Key:** Paste your Gemini API key in the secure input field (stored only in your browser session).
3. **Start Chatting:** Ask questions or select news categories!

### **Features**
- **Latest News:** Select a category like "technology" or "sports" to get the latest headlines.
- **Web Search:** Ask factual questions ("What is MCP server?") for live internet answers.
- **Smart Input:** The app automatically handles either text queries OR news categories (not both).
- **Conversation History:** Latest responses appear at the top for easy viewing.
- **Clear History:** Reset your conversation anytime.
- **Robust:** If APIs are unavailable, the app notifies you gracefully.

### **Example Queries**
- *"News in technology"* → Gets latest tech headlines
- *"What is artificial intelligence?"* → Web search for comprehensive answer
- *"Who won the latest sports match?"* → Live search results
- Select "business" category → Latest business news

---

## 🏗️ Architecture

### **Query Processing Workflow**
1. **User submits a query** (typed message or selected category)
2. **Query routed:**
   - If news category chosen → Calls `get_news` tool
   - Else → Routes to search/LLM node based on keywords
3. **Tool executes** (fetches news or web results)
4. **Response displayed** with conversation history
5. **History logged** with latest first

### **Tech Components**
- **LangGraph StateGraph:** Routes queries intelligently
- **AutoGen Agents:** Orchestrates tool usage
- **Tool Integration:** News and search APIs
- **Streamlit UI:** Interactive web interface

---

## 🧩 Tech Stack

- **Frontend:** Streamlit (Interactive web UI)
- **AI Framework:** AutoGen (Agent orchestration)
- **Workflow:** LangGraph (State-based routing)
- **LLM:** Google Gemini 2.5 Flash
- **News API:** GNews (Real-time headlines)
- **Search API:** Serper (Google search results)
- **Deployment:** Streamlit Community Cloud

---

## 🚀 Deployment

### **Streamlit Community Cloud (Recommended)**

1. **Push to GitHub:** Make sure your code is in a GitHub repository
2. **Deploy:** Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. **Set Environment Variables:**
   ```
   GNEWS_API_KEY=your_gnews_api_key
   SERPER_API_KEY=your_serper_api_key
   ```
4. **Users provide their own Gemini API key** through the app interface

### **Local Development**
```bash
streamlit run main.py
```

---

## 🔒 Privacy & Security

- **API Key Security:** User's Gemini API key is stored only in browser session (not saved anywhere)
- **No Data Storage:** Conversations are not permanently stored
- **Open Source:** Full transparency with public code
- **Free APIs:** GNews and Serper APIs are provided free for users

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** for powerful LLM capabilities
- **AutoGen** for agent orchestration
- **LangGraph** for workflow management
- **Streamlit** for the amazing web framework
- **GNews & Serper** for reliable API services
