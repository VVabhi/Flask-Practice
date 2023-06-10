from flask import Flask, render_template
import requests
from arango import ArangoClient

app = Flask(__name__)

client = ArangoClient()
db = client.db('cinema')
coll = db.collection('movies')

@app.route("/")
def display():
    response = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=2f89096ba58d4500ef539e035743ae3c&language=en-US&page')
    data = response.json()

    for item in data["results"]:
        coll.insert(item)
        print(data)

    results = coll.find({ })
    return render_template('movies.html', results=results)

if __name__ == "__main__":
    sys_db = client.db('_system', username='root')
    if not sys_db.has_database('cinema'):
        sys_db.create_database('cinema')
    if db.has_collection('movies'):
        coll = db.collection('movies')
    else:
        coll = db.create_collection('movies')
    app.run(debug=True)
