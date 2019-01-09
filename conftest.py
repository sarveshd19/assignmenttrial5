import pytest
import main
import flask
from main import *
from flask.testing import FlaskClient
from main import DB as _db

# Connection to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:sarvesh@localhost/testcheck'
app.config['SECRET_KEY'] = "sarvesh"
db = SQLAlchemy(app)
main.DB.create_all()


@pytest.fixture(scope='module')
def test_resp_code():
    client = main.APP.test_client()
    return client
