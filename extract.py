from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from heapq import nlargest
import nltk

def get_ip(link, text, option):
    ##### LOOK AT THE LINK AND OPTION PART LATER ######
    ans = generate_summary(text, 3)
    return ans 

def generate_summary(text, n):
    sentences = sent_tokenize(text)

    # Create the TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Compute the cosine similarity between each sentence and the document
    sentence_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

    # Select the top n sentences with the highest scores
    summary_sentences = nlargest(n, range(len(sentence_scores)), key=sentence_scores.__getitem__)

    summary_tfidf = ' '.join([sentences[i] for i in sorted(summary_sentences)])

    return summary_tfidf

text = '''
Weather is the day-to-day or hour-to-hour change in the atmosphere. 
Weather includes wind, lightning, storms, hurricanes, tornadoes (also known as twisters), rain, hail, snow, and lots more. 
Energy from the Sun affects the weather too. 
Climate tells us what kinds of weather usually happen in an area at different times of the year. 
Changes in weather can affect our mood and life. We wear different clothes and do different things in different weather conditions. 
We choose different foods in different seasons.
Weather stations around the world measure different parts of weather. 
Ways to measure weather are wind speed, wind direction, temperature and humidity. 
People try to use these measurements to make weather forecasts for the future. 
These people are scientists that are called meteorologists. 
They use computers to build large mathematical models to follow weather trends.'''

sentences = sent_tokenize(text)
n = len(sentences)
print(n)
n = int(0.7*n)
summary = generate_summary(text,n)
summary_sentences = summary.split('. ')
formatted_summary = '.\n'.join(summary_sentences)
print(formatted_summary)