import pathlib
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import json
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['file']
collection = db['data']

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\HOME\Desktop\practice\uploads'

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('table.html')
    else:
        files = request.files.getlist('files[]')
        for file in files:
            fileName = file.filename
            purefilename = pathlib.Path(fileName).name
            print("purefilename : ",purefilename)

            file_name = pathlib.Path(fileName).stem + ".json"

            file_path=os.path.join(app.config['UPLOAD_FOLDER'],file_name)
            file.seek(0)
            file.save(file_path)
        return render_template("table.html")



if __name__ == '__main__':
    app.run(debug=True)