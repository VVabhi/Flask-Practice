from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from pyArango.connection import Connection



app=Flask(__name__)

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.data
mongo_student = mongo_db.student
mongo_teacher = mongo_db.teacher

arango_conn = Connection(arangoURL='http://localhost:8529', username='root', password='')
arango_db = arango_conn['data']
arango_student = arango_db['student']
arango_teacher = arango_db['teacher']

@app.route("/", methods = ['GET', 'POST'])
def Home_Page():
    return render_template("Home.html")   

@app.route('/submit', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        placeofstudent = request.form['place_of_student']
        classname = request.form['class_name']
        graduatedyear = request.form['graduated_year']
        cgpa = request.form['cgpa']
        mongo_student.insert_one({'first_name': firstname, 'last_name': lastname, 'place_of_student': placeofstudent, 'class_name': classname, 'graduated_year': graduatedyear, 'cgpa': cgpa})
        arango_student.createDocument({
            'first_name':firstname,
            'last_name':lastname,
            'place_of_student':placeofstudent,
            'class_name':classname,
            'graduated_year':graduatedyear,
            'cgpa':cgpa
        }).save()
        all_documents = mongo_student.find()
        all_documents = list(all_documents)
        return render_template('result.html', student=all_documents)
    

@app.route('/return', methods=('GET', 'POST'))
def index2():
    if request.method=='POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        classname = request.form['class_name']
        dealingsubject = request.form['dealing_subject']
        mongo_teacher.insert_one({'first_name': firstname, 'last_name': lastname, 'class_name': classname, 'dealing_subject': dealingsubject})
        arango_teacher.createDocument({
            'first_name':firstname,
            'last_name':lastname,
            'class_name':classname,
            'dealing_subject':dealingsubject
        }).save()
        all_documents = mongo_teacher.find()
        all_documents = list(all_documents)
        return render_template('data.html', teacher=all_documents)


@app.route('/search2', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['Search_2']
        classname = request.form['class_name']
        query = {
            "$or": [
            {
                "class_name": classname
            }, 
            {
                "first_name": search
            },
            {
                "place_of_student": search
            },
            {
                "last_name": search
            },
            {
                "graduated_year": search
            },
            {
                "cgpa": search
            }

            ]
            }
        # teacher_data = teacher.aggregate(query)
        teacher_data = mongo_teacher.find(query)
        fresult = list(teacher_data)


        print("fresult : ",fresult)
        return render_template('data.html', results=fresult)
    else:
        return redirect(url_for('index'))

@app.route('/search1', methods=['GET','POST'])
def search1():
    if request.method == 'POST':
        search = request.form['Search_1']
        classname = request.form['class_name']
        query = {
            "$or": [
            {
                "class_name": classname
            }, 
            {
                "first_name": search
            },
            {
                "place_of_student": search
            },
            {
                "last_name": search
            },
            {
                "graduated_year": search
            },
            {
                "cgpa": search
            }

            ]
            }
        student_data = mongo_student.find(query)
        result = list(student_data)
        print("result: ", result)
        return render_template('result.html', results=result)
    else:
        return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True)

