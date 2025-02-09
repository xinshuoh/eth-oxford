import sqlite3
import vaderSentiment.vaderSentiment as vader
from collections import defaultdict
from database import TWEETS_DB_FILE, get_conversation_ids, store_debate_summary
from mistral import summarize_text

analyzer = vader.SentimentIntensityAnalyzer()

def get_debate_summaries():
    """ Fetch tweets grouped by conversation_id and analyze debates """
    
    conn = sqlite3.connect(TWEETS_DB_FILE)
    cursor = conn.cursor()
    
    # Fetch all tweets grouped by conversation_id
    cursor.execute("""
        SELECT conversation_id, user_id, username, text, reply_count, retweet_count, like_count
        FROM tweets
        WHERE conversation_id IS NOT NULL
        ORDER BY conversation_id, reply_count DESC
    """)
    
    tweets = cursor.fetchall()
    conn.close()
    
    # Organize tweets into debates grouped by conversation_id
    debates = defaultdict(list)
    for conversation_id, user_id, username, text, reply_count, retweet_count, like_count in tweets:
        debates[conversation_id].append({
            "user_id": user_id,
            "username": username,
            "text": text,
            "reply_count": reply_count,
            "retweet_count": retweet_count,
            "like_count": like_count
        })
    
    # Analyze each debate
    debate_summaries = []
    for conversation_id, debate_tweets in debates.items():
        summary = analyze_debate(conversation_id, debate_tweets)
        debate_summaries.append(summary)
    
    return debate_summaries

def analyze_debate(conversation_id, tweets):
    """ Analyze a debate and summarize the main arguments """

    # Track stances and arguments
    pro_side = []
    anti_side = []
    
    for tweet in tweets:
        sentiment_score = analyzer.polarity_scores(tweet["text"])["compound"]
        
        if sentiment_score > 0:
            pro_side.append(tweet)
        elif sentiment_score < 0:
            anti_side.append(tweet)

    # Sort by engagement
    pro_side = sorted(pro_side, key=lambda x: x["reply_count"] + x["retweet_count"] + x["like_count"], reverse=True)
    anti_side = sorted(anti_side, key=lambda x: x["reply_count"] + x["retweet_count"] + x["like_count"], reverse=True)

    # Get the top arguments
    top_pro = pro_side[0]["text"] if pro_side else "No clear pro argument."
    top_anti = anti_side[0]["text"] if anti_side else "No clear anti argument."

    # Summarize the conversation
    debate_summary = summarize_conversation(conversation_id)
    print(debate_summary)

    # Generate a title from the most engaging tweet
    most_engaged_tweet = sorted(tweets, key=lambda x: x["reply_count"] + x["retweet_count"] + x["like_count"], reverse=True)[0]
    title = f"{most_engaged_tweet['text'][:50]}..."  # Shortened version of key tweet

    # Store debate summary in database
    store_debate_summary(conversation_id=conversation_id, title=title, summary=debate_summary, tweets=tweets)

    return {
        "conversation_id": conversation_id,
        "title": title,
        "summary": debate_summary,
        "top_pro_argument": top_pro,
        "top_anti_argument": top_anti,
        "participants": [tweet["username"] for tweet in tweets]
    }


def get_conversation_text(conversation_id):
    """ Retrieve full conversation text from the database """
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, text FROM tweets
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))
    
    tweets = cursor.fetchall()
    conn.close()

    # Combine messages into a readable conversation format
    conversation_text = "\n".join([f"{user}: {text}" for user, text in tweets])
    return conversation_text

def summarize_conversation(conversation_id):
    summary = summarize_text(get_conversation_text(conversation_id))
    return summary

if __name__ == "__main__":
    print(get_conversation_ids())
    debates = get_debate_summaries()
    for debate in debates[:5]:  # Show first 5 debates
        print(debate)
