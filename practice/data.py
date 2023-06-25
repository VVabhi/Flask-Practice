
from flask import Flask, render_template, request
from pyArango.connection import *
import pandas as pd

app = Flask(__name__)
conn = Connection(username='root', password='')
db = conn['summary']

@app.route('/')
def index():
    return render_template('cf.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_excel(file)
    collection = db['cdr2']

    
    data = df.to_dict(orient='records')
    
    for record in data:
        document = collection.createDocument()
        for column, value in record.items():
            document[column] = str(value)
        document.save()
    
    return render_template('cx.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
