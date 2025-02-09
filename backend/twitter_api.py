import requests
import os
from dotenv import load_dotenv
from database import TWEETS_DB_FILE, get_conversation_ids, store_tweets

load_dotenv()
API_URL = "https://apis.datura.ai/twitter"
API_KEY = os.getenv("DATURA_API_KEY")

def fetch_tweets():
    if not API_KEY:
        raise ValueError("API_KEY is missing. Ensure it's set in the .env file.")
    payload = {
        "query": f"(crypto OR bitcoin OR ethereum OR defi OR nft OR \"web3\") filter:replies min_replies:10 min_retweets:5 lang:en -filter:links since:2024-02-01"
    }
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", API_URL, json=payload, headers=headers)
    store_tweets(response.json())
    print(f"Stored {len(response.json())} tweets.")
    return response.json()

def fetch_related_conversations():
    conversation_ids = get_conversation_ids()

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }

    list_of_tweets = []

    for conversation_id in conversation_ids:
        print(f"Fetching more tweets for conversation: {conversation_id}")
        payload = {"query": f"conversation_id:{conversation_id}"}
        response = requests.request("POST", API_URL, headers=headers, json=payload)

        tweets = response.json()
        list_of_tweets.append(tweets)
        store_tweets(tweets)
        print(f"Stored {len(tweets)} more tweets for conversation {conversation_id}.")

    return list_of_tweets
