from flask import Flask, request, render_template
import os
import pickle
import numpy as np
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/statics',
            template_folder='web/templates')

model = pickle.load(open('models/phishing.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template("email_form.html")

@app.route('/form', methods=['POST'])
def submitform():
    # Get the JSON data from the request
    email_title = request.form.get('email-title')
    email_content = request.form.get('email-content')
    data = email_title + email_content
    features = [np.array([email_title,email_content])]
    prediction = model.predict(features)
    result = prediction[0]
    return render_template("email_form.html", prediction=result)

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