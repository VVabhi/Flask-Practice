import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

client = ArangoClient()
db = client.db('mydb')
coll = db.collection('mycollection')

@app.route("/")
def Home_page():
    df = pd.read_csv('https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/people/people-100.csv')
    data = df.to_dict("records")
    coll.insert(data)
    rows = coll.all()
    cols = df.columns.tolist()
    return render_template('test.html', rows=rows, cols=cols)

if __name__ == '__main__':
    sys_db = client.db('_system', username='root')
    if not sys_db.has_database('mydb'):
        sys_db.create_database('mydb')
    if db.has_collection('mycollection'):
        coll = db.collection('mycollection')
    else:
        coll = db.create_collection('mycollection')
    app.run(debug=True)
