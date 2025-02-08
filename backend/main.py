from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3
import json
from debate_analysis import detect_debates
from database import (
    init_db,
    store_tweets,
    get_stored_tweets,
    clear_databases,
    DB_FILE,
    TWEETS_DB_FILE,
)
from nlp import analyze_tweets
from twitter_api import fetch_tweets
import uvicorn
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    clear_databases()


app = FastAPI(lifespan=lifespan)

# CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze/")
def analyze_debates(tweets: List[dict]):
    detected_debates = detect_debates(tweets)

    summaries = []
    for debate in detected_debates:
        topic = debate.get("topic", "Unknown Topic")
        summary = debate["summary"]

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO debates (topic, tweets, summary) VALUES (?, ?, ?)",
            (topic, json.dumps(debate["tweets"]), summary),
        )
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


@app.get("/fetch")
def fetch_and_store(query: str = "crypto"):
    tweets = fetch_tweets(query)
    store_tweets(tweets)
    return {"message": f"Tweets for query: '{query}' fetched and stored"}


@app.get("/tweets")
def get_tweets():
    tweets = get_stored_tweets()
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
