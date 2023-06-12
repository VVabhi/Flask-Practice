import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

client = ArangoClient()
db = client.db('summary')
coll = db.collection('data')

@app.route('/', methods = ['GET','POST'])
def Home_page():
    return render_template('Home.svelte')

@app.route('/submit', methods=('GET', 'POST'))
def get_page():
    if request.method=='POST':
        phone1 = request.form['phone1']
        f=coll.find({'phone1':phone1})
        query_obj = f'FOR doc IN data FILTER doc.phone1 == "{phone1}" RETURN doc'
        query = db.aql.execute(query_obj)
        finalList = list()
        for result in query:
            d = dict()
            d["first_name"] = result['first_name']
            d["county"] = result['county']
            d["city"] = result['city']
            d["zip"] = result['zip']
            d["email"] = result['email']
            d["web"] = result['web']
            d["address"] = result['address']
            finalList.append(d)
        return render_template('try.html', fresult=finalList)


if __name__ == '__main__':
    app.run(debug=True)