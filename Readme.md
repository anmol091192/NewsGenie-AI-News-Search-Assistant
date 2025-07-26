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
- **Robust Error Handling:** Graceful fallbacks for missing API keys, network issues, or no news results.
- **Easy-to-use UI:** Interactive Streamlit web interface for chatting with NewsGenie.

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

```

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

### 4. **Configure environment variables**

```bash
GEMINI_API_KEY=your_google_gemini_api_key
GNEWS_API_KEY=your_gnews_api_key
SERPER_API_KEY=your_serper_api_key
```

Get free API keys from:
	•	Google Gemini API: https://aistudio.google.com/app/apikey
	•	GNews API: https://gnews.io/
	•	Serper.dev: https://serper.dev/

### 5. **Run the app**

```bash
streamlit run main.py
```
The app will open in your browser (typically at http://localhost:8501).

## ✨ How To Use
	-	Ask anything: Type your question or pick a news category.
	-	Latest News: Select a category like “technology” or “sports” to get the latest headlines.
	-	Web Search: Ask factual questions (“What is MCP server?”) for live internet answers.
	-	Robust: If the APIs are unavailable, the app notifies you gracefully.
	-	All-in-one: Both news and search queries are handled in one interface.

⸻

## 🧩 Tech Stack
	-	Streamlit: UI framework
	-	AutoGen: Agent orchestration
	-	LangGraph: Workflow routing
	-	Google Gemini: LLM
	-	GNews API: Real-time news
	-	Serper API: Web search

## Screenshots

<img width="811" height="920" alt="Screenshot 2025-07-22 at 12 19 17 PM" src="https://github.com/user-attachments/assets/ef2ccbbd-1be0-4b6e-9c8a-98df8091e060" />

⸻

<img width="1029" height="781" alt="Screenshot 2025-07-22 at 12 20 07 PM" src="https://github.com/user-attachments/assets/7ff17254-6f39-4663-a26b-966994c70c30" />

⸻


<img width="870" height="838" alt="Screenshot 2025-07-22 at 12 19 45 PM" src="https://github.com/user-attachments/assets/4299912e-6557-4741-a6b4-03aad68ff03e" />

⸻


<img width="645" height="887" alt="Screenshot 2025-07-22 at 5 26 56 PM" src="https://github.com/user-attachments/assets/04bcd595-f9ea-4ff3-a306-242adb76ac5b" />

⸻


<img width="852" height="918" alt="Screenshot 2025-07-22 at 5 25 28 PM" src="https://github.com/user-attachments/assets/ac3b3b27-07be-485a-8086-ac28e5be9f3a" />
