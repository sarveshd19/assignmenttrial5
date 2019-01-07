"""Main file for CRUD operations of student"""
import time
import datetime
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

APP = Flask(__name__)
# mysql db connection string
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sarvesh@localhost/mytest1'
APP.config['SECRET_KEY'] = "sarveshdineshdeshmukh"

DB = SQLAlchemy(APP)


# creating table student
class Student(DB.Model):  # pylint: disable=too-few-public-methods
    """Creating table student"""
    __tablename__ = 'student'
    student_id = DB.Column('id', DB.Integer, primary_key=True)
    student_name = DB.Column(DB.String(100))
    # Adding foreign key reference to class
    class_id = DB.Column(DB.Integer, DB.ForeignKey('classroom.id'))
    classroom = DB.relationship("Classroom", foreign_keys='Classroom.class_leader')
    created_on = DB.Column(DB.String(50))
    updated_on = DB.Column(DB.String(50))

    def __init__(self, student_id, student_name, class_id, created_on, updated_on):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id
        self.created_on = created_on
        self.updated_on = updated_on


# Creating table classroom
class Classroom(DB.Model):  # pylint: disable=too-few-public-methods
    """Creating table classroom"""
    __tablename__ = "classroom"
    class_id = DB.Column('id', DB.Integer, primary_key=True)
    class_name = DB.Column(DB.String(100))
    # Creating relationship with student entity
    student = DB.relationship("Student", backref="class_leader", foreign_keys='Student.class_id')
    class_leader = DB.Column(DB.Integer, DB.ForeignKey('student.id'))
    created_on = DB.Column(DB.String(50))
    updated_on = DB.Column(DB.String(50))

    def __init__(self, class_id, class_name, class_leader, created_on, updated_on):
        self.class_id = class_id
        self.class_name = class_name
        self.class_leader = class_leader
        self.created_on = created_on
        self.updated_on = updated_on


@APP.route('/')
def show_all():
    """Method to display all students"""
    return render_template('show_all.html', students=Student.query.all())


# Method for adding new student
@APP.route('/new', methods=['GET', 'POST'])
def new():
    """Method for adding new student"""
    if request.method == 'POST':
        if not request.form['name'] or not request.form['student_id']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when new user is created
            raw_time = time.time()
            timestamp = datetime.datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M:%S')
            date_add = timestamp
            class_leader = request.form.get("class_leader")
            if class_leader == "Yes":
                student = Student(request.form['student_id'], request.form["name"],
                                  request.form['selected_id'], date_add,
                                  date_add)
                class_info = Classroom.query.filter_by(class_id=request.form['selected_id']).first()
                class_info.class_leader = student.student_id
                DB.session.add(class_info)

            else:
                student = Student(request.form['student_id'], request.form['name'],
                                  request.form['selected_id'], date_add,
                                  date_add)

            DB.session.add(student)
            DB.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html', class_details=Classroom.query.all())


# Method for updating student information
@APP.route('/update', methods=['POST', 'GET'])
def update():
    """Method for updating student information"""
    if request.method == 'POST':
        if not request.form['name'] or not request.form['student_id'] \
                or not request.form['class_id']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when student is updated
            raw_time = time.time()
            timestamp = datetime.datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M:%S')
            date_mod = timestamp
            old_id = request.form['old_id']
            class_id = request.form['class_id']
            class_leader = request.form.get("class_leader")
            if class_leader == "Yes":
                class_update = Classroom.query.filter_by(class_id=class_id).first()
                class_update.class_leader = request.form['student_id']
            student = Student.query.filter_by(student_id=old_id).first()
            student.student_name = request.form['name']
            student.class_id = request.form['class_id']
            student.student_id = request.form['student_id']
            student.updated_on = date_mod
            DB.session.commit()
            flash('Record was successfully updated')
            return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))


# Method for passing selected student's data for updating
@APP.route('/update_record', methods=['post', 'get'])
def update_record():
    """Method for passing selected student's data for updating"""
    current_id = request.form.get("student_id")
    student_update = Student.query.filter_by(student_id=current_id).first()

    return render_template("update_record.html", student=student_update)


# Method for deleting student
@APP.route("/delete", methods=["POST"])
def delete():
    """Method for deleting student"""
    student_id = request.form.get("id")
    student = Student.query.filter_by(student_id=student_id).first()
    try:
        DB.session.delete(student)
        DB.session.commit()
        return redirect(url_for('show_all'))
    except IntegrityError:
        flash('The Student you are trying to delete is the current Class Leader.'
              ' Kindly appoint another Class Leader and try again.')
        return redirect(url_for('show_all'))


# Method for displaying classes
@APP.route("/view_class")
def view_class():
    """Method for displaying classes"""
    return render_template("view_class.html", classes=Classroom.query.all())


if __name__ == '__main__':
    DB.create_all()
    APP.run(debug=True)
