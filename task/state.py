import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

client = ArangoClient()
db = client.db('excel')
coll = db.collection('data')


@app.route('/', methods = ['GET','POST'])
def Home_page():
    return render_template('state.html')

@app.route('/submit', methods=('GET', 'POST'))
def get_page():
    if request.method=='POST':
        phone1 = request.form['phone1']
        f=coll.find({'phone1':phone1})
        query_obj = f'FOR doc IN data FILTER doc.Number == "{phone1}" RETURN doc'
        query = db.aql.execute(query_obj)
        finalList = list()
        for result in query:
            d = dict()
            d["Date"] = result['Date']
            d["Number"] = result['Number']
            finalList.append(d)
        return render_template('try.html', fresult=finalList)

@app.route('/daterange', methods=['GET','POST'])
def daterange():
   if request.method == 'POST':
      start_date = request.form['start_date']
      end_date = request.form['end_date']
      bind_vars = {
      "lookup1": start_date,"lookup2": end_date
      } 
      print(bind_vars)
      query=db.aql.execute('FOR doc IN data FILTER doc.Date>=@lookup1 && doc.Date<=@lookup2 RETURN doc',bind_vars=bind_vars)
      bwn_numbers=[]
      bwn_dates=[] 
      for output in query:
        print(output) 
        fnumber=output['Number']
        fdate=output['Date']
        bwn_numbers.append(fnumber)
        bwn_dates.append(fdate)
      bwnresult=dict(zip(bwn_numbers,bwn_dates))
      return render_template('submit.html',data= bwnresult)



if __name__ == '__main__':
    sys_db = client.db('_system', username='root')
    if not sys_db.has_database('excel'):
        sys_db.create_database('excel')
    if db.has_collection('data'):
        coll = db.collection('data')
    else:
        coll = db.create_collection('data')
    app.run(debug=True)