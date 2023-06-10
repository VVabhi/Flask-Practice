import requests
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from pprint import pprint
from flask import Flask,render_template,request


app = Flask(__name__)

@app.route("/")
def display():
    page = request.args.get('page',1,type=int)
    response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key=2f89096ba58d4500ef539e035743ae3c&language=en-US&page={page}")
    data = json.loads(response.text)
    movie = []
    for result in data['results'][:15]:
        movie.append(result['title'])
    df = pd.DataFrame(data=movie)
    print(df)
    return render_template("datatable.html", data=df, page=page)
if __name__ == "__main__":
    app.run(debug=True)