import pandas as pd
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence


comments_df = pd.read_csv('Subreddit comments.csv', usecols=[1], names=['Comments'], sep=';', header=0)
comments_df['Comments'].fillna('None', inplace=True)

# Define functions to get sentiment scores
def vader_sentiment_scores(comment):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(comment)
    vader_compound_scores.append(sentiment['compound'])
    return sentiment

def flair_sentiment_scores(comment):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(comment)
    classifier.predict(sentence)
    sentiment = sentence.labels[0].value
    score = sentence.labels[0].score
    flair_count_scores.append(sentiment)
    return sentiment, score

#define lists to store compund scores
vader_compound_scores = []
flair_count_scores = []

# apply the sentiment analysis function to the comments column and store the results in new columns
comments_df['Vader sentiment scores'] = comments_df['Comments'].apply(vader_sentiment_scores)
comments_df['Flair sentiment scores'] = comments_df['Comments'].apply(flair_sentiment_scores)

average_score = sum(vader_compound_scores) / len(vader_compound_scores)
comments_df.loc['Averages','Vader sentiment scores'] = average_score

x, y = flair_count_scores.count('POSITIVE'), flair_count_scores.count('NEGATIVE')
comments_df.loc['Averages','Flair sentiment scores'] = (f'n positives: {x}, n negatives: {y}')

comments_df.to_csv("Comments sentiment analysis.csv", index=True, sep=';')
