import pandas as pd
import re
import praw
from praw.models import MoreComments
 
reddit_read_only = praw.Reddit(client_id="AUdenJ8dFGlyW0B5PBezew",client_secret="PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q",user_agent="scrapetest")      
 
# URL of the post
url = "https://www.reddit.com/r/movies/comments/17c17wa/official_discussion_killers_of_the_flower_moon/"

#input('Provide a valid reddit post url:')

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

post_comments = []

for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
    comment_txt = data_cleaner(comment.body)
    post_comments.append(comment_txt)
 
# creating a dataframe
comments_df = pd.DataFrame(post_comments, columns=['Comments'])
comments_df.to_csv("Subreddit comments.csv", index=True, sep=';')


