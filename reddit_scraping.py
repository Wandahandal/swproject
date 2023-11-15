import praw
import pandas as pd
import re
from praw.models import MoreComments

reddit = praw.Reddit(client_id='AUdenJ8dFGlyW0B5PBezew', client_secret='PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q', user_agent='scrapetest')
# get 10 hot posts from the MachineLearning subreddit
hot_posts = reddit.subreddit('ClimateChange').hot(limit=20)


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

posts_dict = {"Title": [], "Post Text": [], "Total Comments": [], "Post Comments": []}

for post in hot_posts:
	# Title of each post
	posts_dict["Title"].append(post.title)
	# Text inside a post
	post_txt = data_cleaner(post.selftext)
	posts_dict["Post Text"].append(post_txt)
	# Total number of comments inside the post
	posts_dict["Total Comments"].append(post.num_comments)
	#comments of each post by creating a submission object
	submission = reddit.submission(post.id)
	post_comments = []
	for comment in submission.comments:
		if type(comment) == MoreComments:
			continue
		comment_txt = data_cleaner(comment.body)
		post_comments.append(comment_txt)
	comments = ' '.join(post_comments[:10]) #to keep only 10 comments because some posts have 500 of them + i transform the list of el in a unique string
	posts_dict["Post Comments"].append(comments)

# Saving the data in a pandas  and csv file
top_posts = pd.DataFrame(posts_dict, columns=['Title', 'Post Text', 'Total Comments','Post Comments'])
top_posts.to_csv("Top Posts.csv", index=True, sep = ';')












'''
#save top posts in panda df
posts = subreddit.top("month")  #Scraping the top posts of the current month

'''