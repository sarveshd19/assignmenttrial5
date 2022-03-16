"""Main file for CRUD operations of student"""
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import uuid

APP = Flask(__name__)
# mysql db connection string
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres'
APP.config['SECRET_KEY'] = "sarveshdineshdeshmukh"

DB = SQLAlchemy(APP)


# creating table student
class Student(DB.Model):  # pylint: disable=too-few-public-methods
    """Creating table student"""
    __tablename__ = 'student'
    student_id = DB.Column('id', DB.String(100), primary_key=True)
    student_name = DB.Column(DB.String(100))
    # Adding foreign key reference to class
    class_id = DB.Column(DB.String(100), DB.ForeignKey('classroom.id'))
    classroom = DB.relationship("Classroom", foreign_keys='Classroom.class_leader')
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())

    def __init__(self, student_id, student_name, class_id):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id


# Creating table classroom
class Classroom(DB.Model):  # pylint: disable=too-few-public-methods
    """Creating table classroom"""
    __tablename__ = "classroom"
    class_id = DB.Column('id', DB.String(100), primary_key=True)
    class_name = DB.Column(DB.String(100))
    # Creating relationship with student entity
    student = DB.relationship("Student", foreign_keys='Student.class_id')
    class_leader = DB.Column(DB.String(100), DB.ForeignKey('student.id'))
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())

    def __init__(self,class_id, class_name):
        self.class_id = class_id
        self.class_name = class_name


@APP.route('/', methods=['GET', 'POST'])
def show_all():
    """Method to display all students"""
    return render_template('show_all.html', students=Student.query.all())


# Method for adding new student
@APP.route('/new', methods=['GET', 'POST'])
def new():
    """Method for adding new student"""
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:

            class_leader = request.form.get("class_leader")
            if class_leader == "Yes":
                uid_id = uuid.uuid4()
                student = Student(str(uid_id), request.form["name"], request.form['selected_id'])
                class_info = Classroom.query.filter_by(class_id=request.form['selected_id']).first()
                DB.session.add(student)
                DB.session.commit()
                class_info.class_leader = student.student_id
                class_info.updated_on = DB.func.now()

                DB.session.add(class_info)
                DB.session.commit()

            else:
                uid_id = uuid.uuid4()
                student = Student(str(uid_id), request.form['name'],
                                  request.form['selected_id'])
                DB.session.add(student)
                DB.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html', class_details=Classroom.query.all())


# Method for updating student information
@APP.route('/update', methods=['POST'])
def update():
    """Method for updating student information"""
    if request.method == 'POST':
        if not request.form['student_name'] \
                or not request.form['class_id']:
            flash('Please enter all the fields', 'error')
        else:

            old_id = request.form['old_id']
            class_id = request.form['class_id']
            class_leader = request.form.get("class_leader")
            student_name = request.form.get("student_name")
            if class_leader == "Yes":
                class_update = Classroom.query.filter_by(class_id=class_id).first()
                class_update.class_leader = request.form['old_id']
            student = Student.query.filter_by(student_id=old_id).first()
            student.student_name = student_name
            student.class_id = class_id
            student.updated_on = DB.func.now()
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

    return render_template("update_record.html", student=student_update, class_room=Classroom.query.all())


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
@APP.route("/view_class", methods=['GET', 'POST'])
def view_class():
    """Method for displaying classes"""
    return render_template("view_class.html", classes=Classroom.query.all())


@APP.route("/new_class", methods=['GET', 'POST'])
def new_class():
    """Adding new class"""
    if request.method == 'POST':
        if not request.form['class_name']:
            flash('Please enter all details', 'error')
        else:
            uid_id = uuid.uuid4()
            class_info = Classroom(str(uid_id), request.form['class_name'])
            DB.session.add(class_info)
            DB.session.commit()
            return redirect(url_for('view_class'))
    return render_template('new_class.html', classes=Classroom.query.all())


# Method for deleting a class
@APP.route("/class", methods=["POST"])
def delete_class():
    """Method for deleting student"""
    class_id = request.form.get("id")
    try:
        current_class = Classroom.query.filter_by(class_id=class_id).first()
        DB.session.delete(current_class)
        DB.session.commit()
        return redirect(url_for('view_class'))
    except IntegrityError:
        flash('Error while deleting class')
        return redirect(url_for('view_class'))


if __name__ == '__main__':
    DB.create_all()
    APP.run(debug=True)
