import praw
import pandas as pd
 
reddit_read_only = praw.Reddit(client_id="AUdenJ8dFGlyW0B5PBezew",client_secret="PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q",user_agent="scrapetest")        
 
 
subreddit = reddit_read_only.subreddit("OppenheimerMovie")

#for post in subreddit.hot(limit=50):
    #print(post.selftext)
    #print()

posts_dict = {"Title": [], "Post Text": []}
 
for post in subreddit.hot(limit=50):
    posts_dict["Title"].append(post.title)
    posts_dict["Post Text"].append(post.selftext)

top_posts_oppenheimer = pd.DataFrame(posts_dict)
top_posts_oppenheimer

top_posts_oppenheimer.to_csv("Top Posts Oppenheimer.csv", index=True)