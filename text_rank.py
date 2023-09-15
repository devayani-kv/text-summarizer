import numpy as np
import pandas as pd
import nltk
import re
import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

word_embeddings = {}
f = open('D:\summarizer\glove.6B\glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()
print(len(word_embeddings))

#def text_rank(text):
def preprocess_text(text):
    sentences = sent_tokenize(text)
    #clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.replace("[^a-zA-Z]", " ") for s in sentences]
    clean_sentences = [s.lower() for s in clean_sentences]
    def remove_stopwords(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    return sentences, clean_sentences

def vector_representation(clean_sentences):
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
    return sentence_vectors 

def similarity_matrix(sentences, sentence_vectors):
    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    return sim_mat

def page_rank(sim_mat, sentences):
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    summary = []
    for i in range(5):
        summary.append(ranked_sentences[i][1])
    return summary

def text_rank(text):
    sentences, clean_sentences = preprocess_text(text)
    vector_rep = vector_representation(clean_sentences)
    sim_mat = similarity_matrix(sentences, vector_rep)
    summary = page_rank(sim_mat, sentences)
    ans = ""
    for i in summary:
        ans += i
    return ans 



