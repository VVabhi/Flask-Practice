from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
app=Flask(__name__)

client = MongoClient('localhost', 27017)
db = client["Abhi_db"]
developer = db["developer"]
# client = MongoClient('localhost', 27017)

@app.route("/", methods = ['GET', 'POST'])
def Home_Page():
   print("request_method : ",request.method)
   if request.method == "POST":
       name = request.form['name']
       place = request.form['place']
       year = request.form['year']
       developer.insert_one({'name': name, 'place': place, 'year': year})
       return redirect(url_for('index'))
   return render_template("student.html")

@app.route('/app', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        name = request.form['name']
        place = request.form['place']
        year = request.form['year']
        developer.insert_one({'name': name, 'place': place, 'year': year})
        return redirect(url_for('index'))

    all_documents = developer.find()
    all_documents = list(all_documents)
    return render_template('create.html', developer=all_documents)

if __name__ == "__main__":
   app.run(debug=True)