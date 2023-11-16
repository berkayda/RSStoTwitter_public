import feedparser
import tweepy
import time
from datetime import datetime
import pytz

istanbul_timezone = pytz.timezone("Europe/Istanbul")

api_key = "WRITEYOURS"
api_secret = "WRITEYOURS"
access_token = "WRITE-YOURS"
access_token_secret = "WRITEYOURS"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

rss_urls = {"Coin Telegraph": "https://cointelegraph.com/rss",
            "Coin Desk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
            "Blockworks": "https://blockworks.co/rss",
            "Bitcoin Magazine": "https://bitcoinmagazine.com/.rss/full/",
            "Zerohedge": "http://feeds.feedburner.com/zerohedge/feed"}

def check_rss_feeds():
    for site_name, rss_url in rss_urls.items():
        feed = feedparser.parse(rss_url)

        # share a tweet
        for entry in feed.entries:
            tweet_text = site_name + ": " + entry.title + " " + "#Bitcoin" + "\n" + entry.link
            # change type of published_time to type 
            published_time = datetime(*entry.published_parsed[:6])

            now = datetime.utcnow()
            now = now.replace(tzinfo=pytz.utc)  # convert timezone
            time_of_calculation = now.astimezone(istanbul_timezone).strftime("%d-%m-%Y %H:%M:%S TSİ")

            # compare dates
            current_time = datetime.utcnow()
            time_difference = current_time - published_time

            with open("tweets.txt", "r") as f:
                if tweet_text not in f.read() and time_difference.total_seconds() < 600:
                    time.sleep(30)
                    api.update_status(status=tweet_text)
                    print(site_name + ": " + entry.title + " @ " + time_of_calculation)
                    with open("tweets.txt", "a") as f:
                        f.write(tweet_text + "\n")

while True:
    check_rss_feeds()
    time.sleep(60)
