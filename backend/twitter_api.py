import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_tweets(query: str):
    API_URL = "https://apis.datura.ai/twitter"
    API_KEY = os.getenv("DATURA_API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY is missing. Ensure it's set in the .env file.")
    payload = {"query": query}
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []
