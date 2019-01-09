import pytest
import main
import flask
from main import *
from flask.testing import FlaskClient

# Connection to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:sarvesh@localhost/testcheck'
app.config['SECRET_KEY'] = "sarvesh"
db = SQLAlchemy(app)
main.DB.create_all()


@pytest.fixture(scope='module')
def new_home():
    student = Student(id=45, name="BodduBhai", class_id=102, createdon="null", updatedon="null")
    # classdet = Class(id=102, name="10th B", class_leader=45, createdon="null", updatedon="null")
    return student


@pytest.fixture(scope='module')
def test_resp_code():
    client = main.APP.test_client()
    main.DB.create_all()
    return client
