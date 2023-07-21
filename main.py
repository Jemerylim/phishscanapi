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
        return render_template("results.html", prediction='This email has been flagged as potentially phishing-related.', subprediction='We have cross-checked the URL of this email against our Blacklist database, and there was a match. (Head to our Blacklist Page to find out more!)', subtext="To safeguard your personal information and prevent any potential security risks, we strongly advise you to exercise extreme caution when interacting with the content of this email. Avoid clicking on any suspicious links or providing sensitive information until the legitimacy of the sender and the email's contents can be verified.",footnote='Stay Vigilant!')
    else:     
    #input_data = pd.DataFrame({'Email_Subject': [email_subject], 'Email_Content': [email_content],'URL_Title':[email_url],'Coined.Word':[coined_word],'Closing_Remarks':[email_closing]})
        input_data = str(email_subject) + " " + str(email_content) + " " + str(coined_word)
        input_data_list =[input_data]
        user_input_encoded = vectorizer.transform(input_data_list)

        result = model_naive.predict(user_input_encoded)
        if(result == 'Y'):
            return render_template("results.html", prediction='Your Email may or may not be a Phishing Email.',subprediction='The URL entered is not a match with our Blacklist database. However, after thorough assessment, some elements of the email content may be phishing-related. ',subtext="Please be caution and stay vigilant when interacting with the content of this email. Phishing attempts often evolve and might not always trigger Blacklist matches, making it essential to scrutinize any unexpected or suspicious emails. ",footnote="Stay Vigilant!")
        else:
            return render_template("results.html", prediction='Hooray! This email is free from any phishing concerns.',subprediction='We have thoroughly assessed the email content and cross-checked the URL against our Blacklist database, and it has been verified to be safe.',subtext="You can proceed with confidence and safety when interacting with this email. However, it's always prudent to remain vigilant and exercise caution when dealing with any unsolicited emails or unexpected attachments.",footnote='Stay Vigilant!')
    
@app.route('/add')
def add():
    return render_template("blacklist_add.html")

@app.route('/add', methods=['POST'])
def submitadd():
    url = request.form.get('url')
    blacklisttrie.insert(url)
    return render_template("results.html", prediction='Thank you for submitting this URL, it will be added to our Blacklist database.',subprediction="Your contribution plays a crucial role in fortifying the security measures and protecting our community from potential threats and malicious activities.")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))