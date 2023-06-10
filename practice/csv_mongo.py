from flask import Flask,render_template,request
from pymongo import MongoClient
import pandas as pd
client = MongoClient()
col = client['sample']['text']

app = Flask(__name__)

@app.route("/")
def Home_page():
    
    data = pd.read_csv("https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/people/people-100.csv")
    rows = data.values.tolist()
    cols = data.columns.tolist()
    data_dict = data.to_dict("records")
    

    col.insert_many(data_dict)
    

    return render_template("sample.html", rows=rows, cols=cols)

if __name__ == "__main__":
    app.run(debug=True)

