from flask import Flask, request, render_template
import os
import pickle
import numpy as np
import pandas as pd
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/statics',
            template_folder='web/templates')

model = pickle.load(open('web/statics/models/phishing_model.pkl', 'rb'))

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
    email_closing = request.form.get('email-closing')
    coined_word = coin_word_check(email_subject,email_content)
    input_data = pd.DataFrame({'Email_Subject': [email_subject], 'Email_Content': [email_content],'URL_Title':[email_url],'Coined.Word':[coined_word],'Closing_Remarks':[email_closing]})
    # Get the JSON data from the request
    input_encoded = pd.get_dummies(input_data)
    #data = request.form
   #nested_list = [[data[key][nested_key] for nested_key in data[key]] for key in data]
    #prediction = model.predict([[np.array(nested_list)]])
    #data = [email_title,email_content]
    #data_encoded = pd.get_dummies(data)
    #features = np.array(data_encoded)
    #prediction = model.predict(features)
    #result = prediction[0]
    '''to_predict_list = request.form.to_dict()
    to_predict_list =list(to_predict_list.values())
    to_predict_list = pd.get_dummies(to_predict_list)
    to_predict_list = list(map(int,to_predict_list))
    to_predict = np.array(to_predict_list).reshape(1,12)'''
    training_columns = model.training_columns
    missing_columns = set(training_columns) - set(input_encoded.columns)
    X_test_encoded = pd.concat([input_encoded, pd.DataFrame(columns=list(missing_columns))], axis=1).fillna(0)
    X_test_encoded = X_test_encoded.reindex(columns=training_columns, fill_value=0)
    result = model.predict(X_test_encoded)


    return render_template("email_form.html", prediction=result)
    #return render_template("email_form.html", prediction=data)



'''@app.route('/predict',methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.json
    """ 
    # Preprocess the input data
    df = pd.DataFrame(data)
    df.drop(['Sender_Title', 'Sender_Email'], axis=1, inplace=True)
    df['Coined.Word'] = df.apply(check_words, axis=1)
    
    # Perform one-hot encoding on the input data
    encoded_data = pd.get_dummies(df)
    
    # Align the input data columns with the training dataset columns
    missing_columns = set(X_encoded.columns) - set(encoded_data.columns)
    encoded_data = pd.concat([encoded_data, pd.DataFrame(columns=missing_columns)], axis=1).fillna(0)
    encoded_data = encoded_data.reindex(columns=X_encoded.columns, fill_value=0)
    
    # Make predictions using the trained model
    predictions = rf_model.predict(encoded_data)
    
    # Return the predictions as JSON response
    response = {'predictions': predictions.tolist()}
    return jsonify(response) """
'''

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))