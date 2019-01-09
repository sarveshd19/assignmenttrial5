import os
import tempfile
import time
# import datetime
import pytest
from main import *
#
#
# @pytest.fixture
# def test_client():
#     flask_app = Flask(__name__)
#
#     # Flask provides a way to test your application by exposing the Werkzeug test Client
#     # and handling the context locals for you.
#     testing_client = flask_app.test_client()
#
#     # Establish an application context before running the tests.
#     ctx = flask_app.app_context()
#     ctx.push()
#
#     yield testing_client  # this is where the testing happens!
#
#     ctx.pop()
#
#
# @pytest.fixture(scope='module')
# def init_database():
#     # Create the database and the database table
#     DB.create_all()
#     raw_time = time.time()
#     timestamp = datetime.datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M:%S')
#     # Insert user data
#     student1 = Student(111, "Mike", 1, timestamp, timestamp)
#     class1 = Classroom(10, "BE EXTC A", 101, timestamp, timestamp)
#     DB.session.add(student1)
#     DB.session.add(class1)
#
#     # Commit the changes for the users
#     DB.session.commit()
#
#     yield DB  # this is where the testing happens!
#
#     DB.drop_all()
#
#
# def test_show_all(test_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/')
#     assert response.status_code == 200
#
#
# def test_new(client):
#     response = client.get(url_for('new'))
#     assert response.status_code == 200

TESTDB = 'mytest2.ibd'
TESTDB_PATH = "C:/Program Files/MariaDB 10.3/data{}".format(TESTDB)
TEST_DATABASE_URI = 'mysql://root:sarvesh@localhost/' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(__name__, settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
