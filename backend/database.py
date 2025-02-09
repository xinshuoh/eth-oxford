import sqlite3

DB_FILE = "debates.db"
TWEETS_DB_FILE = "tweets.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS debates (
            id TEXT PRIMARY KEY,
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
            id TEXT PRIMARY KEY,
            user_id TEXT,
            username TEXT,
            text TEXT,
            created_at TEXT,
            reply_count INTEGER,
            retweet_count INTEGER,
            like_count INTEGER,
            quote_count INTEGER,
            in_reply_to_user_id TEXT,
            in_reply_to_status_id TEXT,
            conversation_id TEXT,
            lang TEXT,
            user_followers_count INTEGER,
            user_verified BOOLEAN,
            user_is_blue_verified BOOLEAN,
            user_tweet_count INTEGER,
            user_profile_url TEXT,
            url TEXT)
    """
    )
    conn.commit()
    conn.close()


def store_tweets(tweets):
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    for tweet in tweets:
        cursor.execute(
            """
            INSERT OR IGNORE INTO tweets (
                id, user_id, username, text, created_at, reply_count,
                retweet_count, like_count, quote_count, in_reply_to_user_id,
                in_reply_to_status_id, conversation_id, lang, user_followers_count,
                user_verified, user_is_blue_verified, user_tweet_count, user_profile_url, url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                tweet["id"],
                tweet["user"]["id"],
                tweet["user"]["username"],
                tweet["text"],
                tweet["created_at"],
                tweet["reply_count"],
                tweet["retweet_count"],
                tweet["like_count"],
                tweet["quote_count"],
                tweet["in_reply_to_user_id"],
                tweet["in_reply_to_status_id"],
                tweet["conversation_id"],
                tweet["lang"],
                tweet["user"]["followers_count"],
                tweet["user"]["verified"],
                tweet["user"]["is_blue_verified"],
                tweet["user"]["statuses_count"],
                tweet["user"]["profile_image_url"],
                tweet["url"],
            ),
        )
    conn.commit()
    conn.close()


def get_stored_tweets():
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets")
    tweets = cursor.fetchall()
    conn.close()
    return tweets


def clear_databases():
    # Connect to debates database and clear data
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS debates")
    conn.commit()
    conn.close()

    # Connect to tweets database and clear data
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tweets")
    conn.commit()
    conn.close()

    print("Tables deleted.")


def get_conversation_ids():
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT conversation_id FROM tweets WHERE conversation_id IS NOT NULL")
    conversation_ids = cursor.fetchall()
    conn.close()
    return [id[0] for id in conversation_ids]

def store_debate_summary(conversation_id, title, summary, tweets):
    """ Store the summarized debate in the debates.db database """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO debates (id, topic, tweets, summary)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, title, str(tweets), summary))  # Convert tweets list to string for storage

    conn.commit()
    conn.close()
    print(f"Stored summary for conversation {conversation_id}.")

def get_stored_debates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debates")
    debates = cursor.fetchall()
    conn.close()
    return debates

if __name__ == "__main__":
    init_db()
    print("Database initialized.")