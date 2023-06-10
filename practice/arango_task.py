from pyArango.connection import*
import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask,render_template,request
from flask_arangodb import ArangoDB
import pandas as pd


app = Flask(__name__)
app.config.from_object(__name__)
arango = ArangoDB(app)

@app.route("/", methods = ['GET', 'POST'])
def Home_Page():
    return render_template("Home.html")

@app.route('/route',methods=['GET','POST'])
def get_page():
   if request.method == 'POST':
      name=request.form['name']
      date=request.form['date']
      students.insert({'name':name,'date':date})
      cursor1= db.aql.execute('FOR doc IN students RETURN doc') 
      list_names=[]
      list_dates=[]     
      for result in cursor1:
         name=result['name']
         date=result['date'] 
         list_names.append(name) 
         list_dates.append(date)
      fresult=dict(zip(list_names,list_dates))
      print(fresult)
      return render_template('submit.html',students=fresult)

@app.route('/daterange', methods=['GET','POST'])
def daterange():
   if request.method == 'POST':
      start_date = request.form['start_date']
      end_date = request.form['end_date']
      df = pd.DataFrame()
      bind_vars = {
      "lookup1": start_date,"lookup2": end_date
      }
      daterange = pd.date_range(start_date, end_date)
      cursor2=db.aql.execute('FOR doc IN students FILTER doc.date>=@lookup1 && doc.date<=@lookup2 RETURN doc',bind_vars=bind_vars)
      bwn_names=[]
      bwn_dates=[]  
      for output in cursor2:
         fname=output['name']
         fdate=output['date']
         bwn_names.append(fname)
         bwn_dates.append(fdate)
      bwnresult=dict(zip(bwn_names,bwn_dates))
      print(bwnresult) 
      return render_template('submit.html',students= bwnresult)
      
if __name__ == '__main__':
   client = ArangoClient()
   sys_db = client.db('_system', username='root')
   if not sys_db.has_database('test'):
      sys_db.create_database('test')
   db = client.db('test', username='root')
   if db.has_collection('students'):
      students = db.collection('students')
   else:
      students = db.create_collection('students')
   
   app.run(debug=True)
