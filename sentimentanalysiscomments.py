import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import praw
import pandas as pd
import re


#praw instance creation
reddit_read_only = praw.Reddit(client_id="AUdenJ8dFGlyW0B5PBezew",client_secret="PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q",user_agent="scrapetest")

# URL of the post
url = "https://www.reddit.com/r/movies/comments/155ag1m/official_discussion_oppenheimer_spoilers/"
 
def data_cleaner(data):
	#lowercase
	data = data.lower()
	# Removing URLs with a regular expression
	url_pattern = re.compile(r'https?://\S+|www\.\S+')
	data = url_pattern.sub(r'', data)
	# Remove Emails
	data = re.sub('\S*@\S*\s?', '', data)
	# Remove new line characters
	data = re.sub('\s+', ' ', data)
	# Remove single quotes
	data = re.sub("\'", "", data)
	data = re.sub(r'\d+', '', data)  # remove digits
	data = re.sub(r'[^\w\s]', '', data)  # remove special character
	return data

# Creating a submission object
submission = reddit_read_only.submission(url=url)
from praw.models import MoreComments
 
post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
    comment_txt = data_cleaner(comment.body)
 
    post_comments.append(comment_txt)
 

 
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


# List to store compound scores
compound_scores = []

# Calculate compound score for each text
for text in post_comments:
    # Get sentiment scores for each text
    scores = analyzer.polarity_scores(text)
    # Append the compound score to the list
    compound_scores.append(scores['compound'])

# Calculate the average of compound scores
if compound_scores:
    average_score = sum(compound_scores) / len(compound_scores)
    print("Average Compound Score:", average_score)
else:
    print("No scores to calculate the average.")

