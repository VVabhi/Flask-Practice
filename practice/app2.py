from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import datetime

app=Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.test_db
sample = db.sample
client = MongoClient('localhost', 27017)

@app.route("/", methods = ['GET', 'POST'])
def Home_Page():
    return render_template("main.html")
   

@app.route('/submit', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        name = request.form['name']
        date = request.form['date']
        sample.insert_one({'name': name, 'date': date})
        all_documents = sample.find()
        all_documents = list(all_documents)
        return render_template('result.html', sample=all_documents)
       
@app.route('/daterange', methods=['GET', 'POST'])
def daterange():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        results = sample.find({'date': {'$gte': start_date, '$lte': end_date}})
        output=[result for result in results]
        return render_template('result.html', sample=output)
    

if __name__ == "__main__":
   app.run(debug=True)




