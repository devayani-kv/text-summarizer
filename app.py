from flask import Flask, render_template, request 
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from text_rank import text_rank

app = Flask(__name__)

def get_data_from_url(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/entire', methods=['GET', 'POST'])
def entire():
    link = ""
    p_text = ""
    option = ""
    text = ""
    if request.method == "POST":
        link = request.form["link"]
        p_text = request.form["inputtext_"]
        option = request.form["option"]
        global ans
        ans = link + " " + p_text + " " + option
    
    if link != "" and p_text == "":
        text = get_data_from_url(link)
    elif link == "" and p_text != "":
        text = p_text 
    if option == "Extractive":
        ans = text_rank(text) 
    #elif option == "Abstractive":
        #ans = summ(text)
    
    return render_template('index.html', final_summary = ans)

if __name__ == "__main__":
    app.run()