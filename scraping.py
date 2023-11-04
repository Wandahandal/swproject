import praw

def test_reddit_scraping():
    reddit = praw.Reddit(client_id='AUdenJ8dFGlyW0B5PBezew', client_secret='PMLVog-4HRSGXV9dUJ2JbLIPssgQ_Q', user_agent='scrapetest')
    hot_posts = list(reddit.subreddit('Machinelearning').hot(limit=10))
    assert hot_posts  # Check if hot posts are retrieved
    for post in hot_posts:
        print(post.title)

