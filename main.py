from flask import Flask, request, render_template
import os
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/statics',
            template_folder='web/templates')
#railway
incomes = [
    { 'description': 'salary', 'amount': 5000 }
]


@app.route('/')
def home():
    return render_template('/web/templates/index.html')


@app.route('/', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))