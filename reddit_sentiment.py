import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence

df = pd.read_csv('Top Posts.csv', usecols=[2, 4], names=['Post Text', 'Post Comments'], sep=';', header=0)
df['Post Text'].fillna('None', inplace = True)
df['Post Comments'].fillna('None', inplace = True)


def sentiment_analyzer(tool, column_text):
    print(column_text)
    for i in range(len(df)):
        el = df.loc[i, column_text]
        if el != 'None':
            if tool == 'textblob':  #sentiment analysis with textblob
                el_sentiment = TextBlob(el)
                print(i, el_sentiment.sentiment)
            elif tool == 'vader': #sentiment analysis with vader
                analyzer = SentimentIntensityAnalyzer()
                el_sentiment = analyzer.polarity_scores(el)
                print(i, el_sentiment)
            elif tool == 'flair': #sentiment analysis with flair
                classifier = TextClassifier.load('en-sentiment')
                sentence = Sentence(el)
                classifier.predict(sentence)
                print(i, sentence.labels[0].value, sentence.labels[0].score)

#here you call the function specifying the sentiment analysis tool you want to use and on which data to do the analysis(here is possible only on the text post and the post comments)
sentiment_analyzer('flair', 'Post Text') 
sentiment_analyzer('flair','Post Comments')
