import sqlite3
import json

DB_FILE = "debates.db"

sample_debates = [
    {
        "topic": "Bitcoin vs Ethereum",
        "tweets": [
            {"user": "Alice", "text": "Bitcoin is the only real decentralized money!", "mentions": ["Bob"]},
            {"user": "Bob", "text": "Ethereum has way more use cases than Bitcoin.", "mentions": ["Alice"]}
        ],
        "summary": "A debate between Bitcoin maximalists and Ethereum supporters."
    },
    {
        "topic": "NFTs Are a Scam?",
        "tweets": [
            {"user": "Charlie", "text": "NFTs are just JPEGs, they have no real value!", "mentions": ["David"]},
            {"user": "David", "text": "NFTs enable digital ownership, you don't get it.", "mentions": ["Charlie"]}
        ],
        "summary": "A heated discussion on the legitimacy of NFTs."
    }
]

def insert_sample_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for debate in sample_debates:
        cursor.execute("INSERT INTO debates (topic, tweets, summary) VALUES (?, ?, ?)",
                       (debate["topic"], json.dumps(debate["tweets"]), debate["summary"]))

    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
