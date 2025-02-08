from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3
import json
from debate_analysis import detect_debates

app = FastAPI()

# CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_FILE = "debates.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            tweets TEXT,
            summary TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.post("/analyze/")
def analyze_debates(tweets: List[dict]):
    detected_debates = detect_debates(tweets)
    
    summaries = []
    for debate in detected_debates:
        topic = debate.get("topic", "Unknown Topic")
        summary = debate["summary"]

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO debates (topic, tweets, summary) VALUES (?, ?, ?)",
                       (topic, json.dumps(debate["tweets"]), summary))
        conn.commit()
        conn.close()
        
        summaries.append({"topic": topic, "summary": summary})

    return {"debates": summaries}

@app.get("/debates/")
def get_debates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT topic, summary FROM debates")
    debates = [{"topic": row[0], "summary": row[1]} for row in cursor.fetchall()]
    conn.close()
    return {"debates": debates}
