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
    return render_template('summary.html')

# @app.route("/")
# def index():
#     df = pd.read_csv(r'C:\Users\HOME\Desktop\task\us-500\us-500.csv')
#     data = df.to_dict("records")
#     coll.insert(data)
#     rows = coll.all()
#     cols = df.columns.tolist()
#     return render_template('results.html', rows=rows, cols=cols)

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
            # d["first_name"] = result['first_name']
            # d["county"] = result['county']
            # d["city"] = result['city']
            d["zip"] = result['zip']
            d["email"] = result['email']
            d["web"] = result['web']
            d["address"] = result['address']
            finalList.append(d)
        return render_template('try.html', fresult=finalList)


if __name__ == '__main__':
    sys_db = client.db('_system', username='root')
    if not sys_db.has_database('summary'):
        sys_db.create_database('summary')
    if db.has_collection('data'):
        coll = db.collection('data')
    else:
        coll = db.create_collection('data')
    app.run(debug=True)