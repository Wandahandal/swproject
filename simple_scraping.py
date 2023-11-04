import pandas as pd
import snscrape.modules.twitter as sntwitter

#extract tweet data
scraper = sntwitter.TwitterSearchScraper('#python')
tweets = []
for i, tweet in enumerate(scraper.get_items()):
    data = [
        tweet.date,
        tweet.id,
        tweet.content,
        tweet.likeCount,
        tweet.retweetCount,
    ]
    tweets.append(data)
    if i > 50 :
        break

tweet_df = pd.DataFrame(tweets, columns=['date', 'id', 'content','like_ count','retweet_count'])
tweet_df
#tweet_df.to_csv('')
print('hello')
