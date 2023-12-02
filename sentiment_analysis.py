import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence

def clean_data(data):
    # Lowercase
    data = data.lower()
    # Removing URLs with a regular expression
    data = re.sub(r'https?://\S+|www\.\S+', '', data)
    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)
    # Remove new line characters
    data = re.sub('\s+', ' ', data)
    # Remove single quotes
    data = re.sub("\'", "", data)
    data = re.sub(r'\d+', '', data)  # remove digits
    data = re.sub(r'[^\w\s]', '', data)  # remove special characters
    return data

def get_vader_sentiment_scores(comment, vader_compound_scores):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(comment)
    vader_compound_scores.append(sentiment['compound'])
    return sentiment

def get_flair_sentiment_scores(comment, flair_count_scores):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(comment)
    classifier.predict(sentence)
    sentiment = sentence.labels[0].value
    score = sentence.labels[0].score
    flair_count_scores.append(sentiment)
    return sentiment, score

# Read CSV file into a DataFrame
comments_df = pd.read_csv('Subreddit comments.csv', usecols=[1], names=['Comments'], sep=';', header=0)

# Clean data
comments_df['Comments'] = comments_df['Comments'].fillna('None').apply(clean_data)

# Lists to store compound scores
vader_compound_scores = []
flair_count_scores = []

# Apply sentiment analysis functions and store results in new columns
comments_df['Vader sentiment scores'] = comments_df['Comments'].apply(lambda x: get_vader_sentiment_scores(x, vader_compound_scores))
comments_df['Flair sentiment scores'] = comments_df['Comments'].apply(lambda x: get_flair_sentiment_scores(x, flair_count_scores))

# Calculate average Vader compound score
average_score = sum(vader_compound_scores) / len(vader_compound_scores)
comments_df.loc['Averages', 'Vader sentiment scores'] = average_score
print(f'Vader - the average value for the submitted post is {average_score}')

# Count positive and negative Flair sentiment scores
x, y = flair_count_scores.count('POSITIVE'), flair_count_scores.count('NEGATIVE')
comments_df.loc['Averages', 'Flair sentiment scores'] = (f'n positives: {x}, n negatives: {y}')
print(f'Flair - the positive and negative comments for the submitted post are, respectively: {x} positives, {y} negatives')

# Save results to CSV file
comments_df.to_csv("Comments sentiment analysis.csv", index=True, sep=';')
