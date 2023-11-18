import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import praw
import pandas as pd


#praw instance creation
reddit_read_only = praw.Reddit(client_id="AUdenJ8dFGlyW0B5PBezew",client_secret="PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q",user_agent="scrapetest")

# URL of the post
url = "https://www.reddit.com/r/movies/comments/155ag1m/official_discussion_oppenheimer_spoilers/"
 
# Creating a submission object
submission = reddit_read_only.submission(url=url)
from praw.models import MoreComments
 
post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
 
    post_comments.append(comment.body)
 
# creating a dataframe
comments_df = pd.DataFrame(post_comments, columns=['comment'])


analyzer = SentimentIntensityAnalyzer()

# Define a function to get sentiment scores
def get_sentiment_scores(comment):
    sentiment = analyzer.polarity_scores(comment)
    return sentiment

# Apply the sentiment analysis function to the 'text' column and store the results in new columns
comments_df['sentiment_scores'] = comments_df['comment'].apply(get_sentiment_scores)
comments_df.to_csv("OppenheimerCommentsAnalysis.csv", index=True)
