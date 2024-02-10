from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from heapq import nlargest
from bs4 import BeautifulSoup
from urllib.request import urlopen
import nltk
import transformers
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


def get_data_from_url(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

def generate_summary_extractive(text, n):
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

def generate_summary_abstractive(text):

    model_name = "google/pegasus-xsum"
    tokenizer =  PegasusTokenizer.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

    #model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    #tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-xsum-12-1")
    #model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-xsum-12-1")

    text = "summarize the following text: " +text
    tokenized_text = tokenizer.encode(text, return_tensors='pt', max_length=512).to(device)
    summary_ = model.generate(tokenized_text, min_length=30, max_length=300)
    summary = tokenizer.decode(summary_[0], skip_special_tokens=True)
    #inputs = tokenizer(text, max_length=1024, return_tensors="pt")
    #summary_ids = model.generate(inputs["input_ids"])
    #summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=20)
    #summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return summary
