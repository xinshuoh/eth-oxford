import vaderSentiment.vaderSentiment as vader
import networkx as nx

# Sentiment analyzer
analyzer = vader.SentimentIntensityAnalyzer()

def detect_debates(tweets):
    G = nx.Graph()
    
    for tweet in tweets:
        user = tweet["user"]
        G.add_node(user)
        for mention in tweet["mentions"]:
            G.add_edge(user, mention)

    debate_clusters = [list(component) for component in nx.connected_components(G)]
    
    debates = []
    for cluster in debate_clusters:
        debate_tweets = [t for t in tweets if t["user"] in cluster]
        text = " ".join([t["text"] for t in debate_tweets])
        sentiment = analyzer.polarity_scores(text)
        stance = "Pro" if sentiment["compound"] > 0 else "Anti" if sentiment["compound"] < 0 else "Neutral"
        summary = f"Debate on {debate_tweets[0]['topic']}. Main sentiment: {stance}."

        debates.append({"topic": debate_tweets[0]['topic'], "tweets": debate_tweets, "summary": summary})
    
    return debates
