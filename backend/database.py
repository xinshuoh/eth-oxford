import sqlite3

DB_FILE = "debates.db"
TWEETS_DB_FILE = "tweets.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS debates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            tweets TEXT,
            summary TEXT
        )
    """
    )
    conn.commit()
    conn.close()

    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT
        )
    """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")


def store_tweets(tweets):
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    for tweet in tweets:
        cursor.execute(
            "INSERT INTO tweets (user, text) VALUES (?, ?)",
            (tweet["user"]["name"], tweet["text"]),
        )
    conn.commit()
    conn.close()


def get_stored_tweets():
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user, text FROM tweets")
    tweets = cursor.fetchall()
    conn.close()
    return [{"user": row[0], "text": row[1]} for row in tweets]


def clear_databases():
    # Connect to debates database and clear data
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debates")
    conn.commit()
    conn.close()

    # Connect to tweets database and clear data
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tweets")
    conn.commit()
    conn.close()

    print("Databases cleared.")
