from flask import Flask, request, render_template
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from blacklist_trie import BlackListTrie
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/statics',
            template_folder='web/templates')

blacklisttrie = BlackListTrie()
model_naive = pickle.load(open('web/statics/models/phishing_model_naivebayes.pkl', 'rb'))
with open('web/statics/models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
#model_forest = pickle.load(open('web/statics/models/phishing_model_randomforest.pkl', 'rb'))

def coin_word_check(email_subject,email_content):
    coined_words = {'urgent', 'quick', 'job', 'needed', 'account', 'verification',
               'security', 'alert', 'confirm', 'information', 'suspicious',
               'login', 'update', 'prize', 'winner', 'unusual activity',
               'payment required'}
    subject = str(email_subject.lower())
    content = str(email_content.lower())
    found_words = []
    for word in coined_words:
        if word in subject or word in content:
            found_words.append(word)
            
    if found_words:
        return ', '.join(found_words)
    else:
        return 'na'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template("email_form.html")

@app.route('/form', methods=['POST'])
def submitform():
    email_subject = request.form.get('email-subject')
    email_url = request.form.get('email-url')
    email_content = request.form.get('email-content')
    #email_closing = request.form.get('email-closing')
    coined_word = coin_word_check(email_subject,email_content)
    if blacklisttrie.search(email_url):
        return render_template("email_form.html", prediction='Your Email is a Phishing Email!', subprediction='URL was found in our Blacklist!')
    else:     
    #input_data = pd.DataFrame({'Email_Subject': [email_subject], 'Email_Content': [email_content],'URL_Title':[email_url],'Coined.Word':[coined_word],'Closing_Remarks':[email_closing]})
        input_data = str(email_subject) + " " + str(email_content) + " " + str(coined_word)
        input_data_list =[input_data]
        user_input_encoded = vectorizer.transform(input_data_list)

        result = model_naive.predict(user_input_encoded)
        if(result == 'Y'):
            return render_template("results.html", prediction='Your Email may or may not be a Phishing Email.',subprediction='Your URL is not in our Blacklist but the content suggest it is a Phishing email! Enter at your own risk!')
        else:
            return render_template("results.html", prediction='Your Email is not a Phishing email!',subprediction='')
    
@app.route('/add')
def add():
    return render_template("blacklist_add.html")

@app.route('/add', methods=['POST'])
def submitadd():
    url = request.form.get('url')
    blacklisttrie.insert(url)
    return render_template("results.html", prediction='The URL has been added to the Blacklist!')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))