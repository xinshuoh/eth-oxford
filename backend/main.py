from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3
import json
from debate_analysis import get_debate_summaries
from database import (
    get_stored_debates,
    init_db,
    store_tweets,
    get_stored_tweets,
    clear_databases,
    DB_FILE,
    TWEETS_DB_FILE,
)
from nlp import analyze_tweets
from twitter_api import fetch_related_conversations, fetch_tweets
import uvicorn
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # clear_databases()


app = FastAPI(lifespan=lifespan)

# CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debates/")
def get_debates():
    debates = get_stored_debates()
    return {"debates": debates}

@app.get("/analyze-debates/")
def analyze_debates():
    get_debate_summaries()
    return {"status": "ok"}


@app.get("/fetch")
def fetch_and_store():
    initial_tweets = fetch_tweets()
    related_conversations = fetch_related_conversations()
    return {
        "initial_tweets": initial_tweets,
        "related_conversations": related_conversations,
    }


@app.get("/tweets")
def get_tweets():
    tweets = get_stored_tweets()
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/test")
def test():
    tweets = fetch_tweets()
    return tweets


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
