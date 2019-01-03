from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import time
import datetime

app = Flask(__name__)
# mysql db connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sarvesh@localhost/mytest1'
app.config['SECRET_KEY'] = "sarveshdineshdeshmukh"

db = SQLAlchemy(app)


# creating table student
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column('id', db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    # Adding foreign key reference to class
    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    created_on = db.Column(db.String(50))
    updated_on = db.Column(db.String(50))

    def __init__(self, student_id, student_name, class_id, created_on, updated_on):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id
        self.created_on = created_on
        self.updated_on = updated_on


# Creating table classroom
class Classroom(db.Model):
    __tablename__ = "classroom"
    class_id = db.Column('id', db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    # Creating relationship with student entity
    student = db.relationship("Student", backref="classroom", lazy="joined")
    created_on = db.Column(db.String(50))
    updated_on = db.Column(db.String(50))

    def __init__(self, class_id, class_name, class_leader, created_on, updated_on):
        self.class_id = class_id
        self.class_name = class_name
        self.class_leader = class_leader
        self.created_on = created_on
        self.updated_on = updated_on


@app.route('/')
def show_all():
    return render_template('show_all.html', students=Student.query.all())


# Method for adding new student
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['student_id'] or not request.form['class_id']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when new user is created
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            dateadd = timestamp
            student = Student(request.form['student_id'], request.form['name'], request.form['class_id'], dateadd,
                              dateadd)

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


# Method for updating student information
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['student_id'] or not request.form['class_id']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when student is updated
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            datemod = timestamp
            oldid = request.form['old_id']
            student = Student.query.filter_by(student_id=oldid).first()
            student.student_name = request.form['name']
            student.student_id = request.form['student_id']
            student.updated_on = datemod
            db.session.commit()
            flash('Record was successfully updated')
            return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))


# Method for passing selected student's data for updation
@app.route('/updaterecord', methods=['post', 'get'])
def updaterecord():
    currentid = request.form.get("student_id")
    studentupdate = Student.query.filter_by(student_id=currentid).first()

    return render_template("updaterecord.html", student=studentupdate)


# Method for deleting student
@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    student = Student.query.filter_by(student_id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('show_all'))


# Method for displaying classes
@app.route("/viewclass")
def viewclass():
    return render_template("viewclass.html", students=Classroom.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
