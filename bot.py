import os
import tweepy
import feedparser

# 1. Setup X (Twitter) Client using GitHub Secrets
# These names inside the quotes MUST match the names you give your secrets in GitHub
client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"]
)

# 2. Check MetService for Kumeū/Auckland Alerts
METSERVICE_FEED = "https://alerts.metservice.com/cap/rss"

def check_alerts():
    feed = feedparser.parse(METSERVICE_FEED)
    for entry in feed.entries:
        # Check title and summary for local keywords
        content = (entry.title + entry.summary).lower()
        if "auckland" in content or "kumeu" in content or "huapai" in content:
            return f"⚠️ METSERVICE ALERT: {entry.title}\n\nKumeū residents, stay safe! Check your local drains and road conditions. #Kumeu #AucklandStorm"
    return None

# 3. Execution
alert = check_alerts()
if alert:
    try:
        client.create_tweet(text=alert)
        print("Successfully tweeted the alert!")
    except Exception as e:
        print(f"Error tweeting: {e}")
else:
    print("No active local alerts found right now.")
