# from pyArango.connection import*
import warnings
warnings.filterwarnings("ignore")
from arango import ArangoClient
from flask import Flask,render_template,request
from flask_arangodb import ArangoDB


app = Flask(__name__)
app.config.from_object(__name__)
arango = ArangoDB(app)

@app.route("/", methods = ['GET', 'POST'])
def Home_Page():
    return render_template("number.html")

@app.route('/print',methods=['GET','POST'])
def get_page():
   if request.method == 'POST':
      name=request.form['name']
      mobilenum=request.form['mobilenum']
      date=request.form['date']
      Data.insert({'name':name,'mobilenum':mobilenum, 'date':date})
      cursor1= db.aql.execute('FOR doc IN data RETURN doc')

      final_list = list()
      for result in cursor1:
         fdict = dict()
         fdict["name"] = result["name"]
         fdict["mobilenum"] = result["mobilenum"]
         fdict["date"] = result["date"]
         final_list.append(fdict)
      # list_names=[]
      # list_numbers=[]
      # list_date=[]    
      # for result in cursor1:
      #    name=result['name']
      #    numbers=result['mobilenum']
      #    date=result['date'] 
      #    list_names.append(name) 
      #    list_numbers.append(numbers)
      # fresult=dict(zip(list_names,list_numbers,list_date))
      print(final_list)
      return render_template('number1.html',data=final_list)

@app.route('/daterange', methods=['GET','POST'])
def daterange():
   if request.method == 'POST':
      start_date = request.form['start_date']
      end_date = request.form['end_date']
      bind_vars = {
      "lookup1": start_date,"lookup2": end_date
      } 
      cursor2=db.aql.execute('FOR doc IN students FILTER doc.date>=@lookup1 && doc.date<=@lookup2 RETURN doc',bind_vars=bind_vars)
      bwn_names=[]
      bwn_numbers=[]  
      for output in cursor2:
         fname=output['name']
         # fdate=output['date']
         fnumbers=output['numbers']
         bwn_names.append(fname)
         bwn_numbers.append(fnumbers)
      bwnresult=dict(zip(bwn_names,bwn_numbers))
      print(bwnresult) 
      return render_template('number1.html',data= bwnresult)
      
if __name__ == '__main__':
   client = ArangoClient()
   sys_db = client.db('_system', username='root')
   if not sys_db.has_database('call'):
      sys_db.create_database('call')
   db = client.db('call', username='root')
   if db.has_collection('data'):
      Data = db.collection('data')
   else:
      Data = db.create_collection('data')
   
   app.run(debug=True)
