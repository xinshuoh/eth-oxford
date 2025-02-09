# **CryptX: AI-Powered Crypto Twitter Debate Analyzer**  

![CryptX UI Preview](frontend/public/screenshot.jpg)

🚀 **CryptX** is an **AI-driven debate analysis platform** that tracks, analyzes, and summarizes **Crypto Twitter discussions**. Using **machine learning, sentiment analysis, and NLP**, CryptX provides structured insights into key debates, helping users navigate the **fast-moving crypto landscape**.



## **📌 Features**  

✅ **Real-Time Twitter Data Retrieval**  
- Fetches tweets using the **Datura AI API**, tracking **debates and conflicts**.  
- Groups discussions by **conversation_id** for structured analysis.  

✅ **Debate & Conflict Detection**  
- Identifies **high-impact debates** between influential crypto figures.  
- Detects **reply chains, mentions, and quote tweets** to map discussions.  

✅ **Sentiment & Stance Classification**  
- Uses **VADER Sentiment Analysis** to categorize tweets as **pro, anti, or neutral**.  
- Measures **influence of participants** based on engagement & follower count.  

✅ **AI-Powered Summarization**  
- Generates **concise summaries** using **Mistral AI** to highlight **key arguments**.  
- Contextualizes debates within **broader crypto trends**.  

✅ **Influence & Narrative Tracking**  
- Scores **debates by engagement** (likes, retweets, replies).  
- Identifies **key voices shaping crypto discourse**.  

✅ **Modern Web Interface**  
- **React + Vite** frontend with **interactive debate filtering**.  
- **Stylish card-based UI** for easy browsing of crypto debates.  


## **🛠️ Tech Stack**  

### **Backend**  
- **FastAPI** (Python) for data processing  
- **SQLite** for structured storage of debates  
- **VADER Sentiment Analysis** for stance classification  
- **Mistral AI API** for generating summaries  

### **Frontend**  
- **React + Vite** for a fast and responsive UI  
- **TailwindCSS / Custom CSS** for modern styling  


## **🚀 Installation & Setup**  

1. Clone the repository.
2. Install dependencies.
```bash
cd backend
pip install -r requirements.txt
```
3. Set up the environment variables.
Create a `.env` file in the backend directory and add the following:
```bash
DATURA_API_KEY=your_datura_api_key
MISTRAL_API_KEY=your_mistral_api_key
```
4. Run the backend server.
```bash
uvicorn main:app --reload
```
5. Install the frontend dependencies.
```bash
cd frontend
npm install
```
6. Run the frontend server.
```bash
npm run dev
```

## 🔍 Use Cases
🔹 Stay ahead of market narratives & trends

🔹 Detect emerging crypto controversies

🔹 Analyze sentiment-driven discussions

🔹 Track influential crypto voices

🚀 CryptX: Turning Crypto Twitter into Actionable Insights 🔍
