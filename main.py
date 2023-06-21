from flask import Flask, request, render_template
import os
app = Flask(__name__,
            static_url_path='', 
            static_folder='/statics',
            template_folder='/templates')

#railway
incomes = [
    { 'description': 'salary', 'amount': 5000 }
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))