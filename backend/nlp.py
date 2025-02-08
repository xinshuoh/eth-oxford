from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_stored_tweets


def analyze_tweets():
    tweets = get_stored_tweets()
    analyzer = SentimentIntensityAnalyzer()
    results = []
    for tweet in tweets:
        sentiment_scores = analyzer.polarity_scores(tweet["content"])
        sentiment = (
            "positive"
            if sentiment_scores["compound"] > 0.05
            else "negative" if sentiment_scores["compound"] < -0.05 else "neutral"
        )
        results.append(
            {"user": tweet["user"], "content": tweet["content"], "sentiment": sentiment}
        )
    return results
